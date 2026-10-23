"""Offline ScienceDirect retrieval, normalization, and pipeline integration tests."""

import copy
from http.client import IncompleteRead
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlsplit

from support import PROJECT_ROOT
import config
import download_manager
from author_builder import Author
from download_publications import parse_request
from models import DownloadError, DownloadRecord, DownloadRequest, Publication
from source_downloaders.sciencedirect import PAGE_SIZE, build_query, download, download_pages, fetch_page, normalize_article


def article(number=1):
    # Field shapes follow Elsevier's Article Metadata migration example and views.
    return {
        "pii": f"S{number:016d}",
        "dc:title": "Über Research",
        "dc:creator": "First Author",
        "authors": {"author": [
            {"@_fa": "true", "given-name": "First", "surname": "Author"},
            {"@_fa": "true", "given-name": "Second", "surname": "Author"},
        ]},
        "prism:publicationName": "A Journal",
        "prism:coverDate": [{"@_fa": "true", "$": "2026-10-22"}],
        "prism:issn": "1234-5678",
        "prism:isbn": ["123", "456"],
        "prism:doi": f"10.example/{number}",
        "dc:description": "An abstract.",
        "authkeywords": "Control | Systems",
        "link": [{"@ref": "scidir", "@href": "https://www.sciencedirect.com/science/article/pii/example"}],
        "native_field": {"preserved": [True, "é"]},
    }


def page(total, entries, start=0):
    return {"search-results": {
        "opensearch:totalResults": str(total),
        "opensearch:startIndex": str(start),
        "opensearch:itemsPerPage": str(len(entries)),
        "entry": entries,
    }}


class ScienceDirectSourceTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.env_file = self.root / ".env"
        self.env_file.write_text("SCIENCEDIRECT_API_KEY=file-key\n", encoding="utf-8")
        self.data = self.root / "data"
        for name, value in [("ENV_FILE", self.env_file), ("DATA_DIRECTORY", self.data)]:
            patcher = patch.object(config, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        guard = patch("source_downloaders.sciencedirect.urlopen", side_effect=AssertionError("Unexpected network access"))
        guard.start()
        self.addCleanup(guard.stop)
        self.author = Author("Ada Researcher", ("University A", "Institute B"))

    @patch("source_downloaders.sciencedirect.fetch_page")
    def test_complete_download_saves_native_pages_before_normalization(self, fetch):
        pages = [page(2, [article(1)]), page(2, [article(2)], start=1)]
        original = copy.deepcopy(pages)
        fetch.side_effect = pages
        normalize = normalize_article

        def normalize_after_save(entry):
            self.assertEqual(fetch.call_count, 2)
            paths = list(self.data.glob("*/raw/*.json"))
            self.assertEqual(len(paths), 1)
            self.assertEqual(json.loads(paths[0].read_text()), original)
            return normalize(entry)

        with patch("source_downloaders.sciencedirect.normalize_article", side_effect=normalize_after_save):
            result = download(self.author)
        self.assertIsInstance(result, DownloadRecord)
        self.assertEqual((result.author, result.source, result.publication_count),
                         (self.author.name, "sciencedirect", 2))
        self.assertEqual(result.publications, [normalize(article(1)), normalize(article(2))])
        self.assertEqual(pages, original)
        self.assertEqual([request.args[2] for request in fetch.call_args_list], [0, 1])

    def test_zero_results_save_raw_and_skip_markdown(self):
        empty_pages = [page(0, []), page(0, [{"@_fa": "true", "error": "Result set was empty"}]),
                       {"search-results": {"opensearch:totalResults": "0", "opensearch:startIndex": "0"}}]
        for native in empty_pages:
            with self.subTest(native=native), patch("source_downloaders.sciencedirect.fetch_page", return_value=native), \
                 patch("download_manager.get_selected_authors", return_value=[self.author]), \
                 patch("download_manager.build_markdown") as builder:
                downloads, builds = download_manager.run_download(DownloadRequest("all", ("sciencedirect",)))
                result = downloads[0]
                self.assertIsInstance(result, DownloadRecord)
                self.assertEqual((result.publication_count, result.publications), (0, []))
                self.assertEqual(json.loads(result.raw_file_path.read_text()), [native])
                self.assertEqual(builds, [])
                builder.assert_not_called()

    @patch("source_downloaders.sciencedirect.urlopen")
    def test_mainak_download_sends_given_and_surname_with_affiliation_group(self, open_url):
        native = article()
        native["prism:doi"] = "10.1016/j.ifacol.2022.04.231"
        response = page(1, [native])
        open_url.return_value.__enter__.return_value = io.BytesIO(json.dumps(response).encode())
        author = Author("Mainak Majumder", ("JKU Linz", "Technische Hochschule Ostwestfalen-Lippe"))

        result = download(author)

        self.assertIsInstance(result, DownloadRecord)
        self.assertEqual(result.publication_count, 1)
        self.assertEqual(result.publications[0].doi, "10.1016/j.ifacol.2022.04.231")
        request = open_url.call_args.args[0]
        self.assertEqual(parse_qs(urlsplit(request.full_url).query)["query"],
                         ['(authfirst("Mainak") AND authlastname("Majumder")) '
                          'AND (aff("JKU Linz") OR aff("Technische Hochschule Ostwestfalen-Lippe"))'])
        self.assertEqual(json.loads(result.raw_file_path.read_text()), [response])

    @patch("source_downloaders.sciencedirect.fetch_page", return_value=page(0, []))
    def test_credentials_use_only_file_and_disable_interpolation(self, fetch):
        with patch.dict(os.environ, {"SCIENCEDIRECT_API_KEY": "environment-key", "OTHER": "secret"}):
            self.assertIsInstance(download(self.author), DownloadRecord)
            self.assertEqual(fetch.call_args.args[0], "file-key")
            self.env_file.write_text("SCIENCEDIRECT_API_KEY=${OTHER}\n", encoding="utf-8")
            self.assertIsInstance(download(self.author), DownloadRecord)
            self.assertEqual(fetch.call_args.args[0], "${OTHER}")

    @patch("source_downloaders.sciencedirect.fetch_page")
    def test_missing_or_blank_credentials_fail_before_network(self, fetch):
        values = ["", "OTHER=value\n", "SCIENCEDIRECT_API_KEY\n", "SCIENCEDIRECT_API_KEY=\n",
                  "SCIENCEDIRECT_API_KEY='  '\n"]
        for value in values:
            with self.subTest(value=value), patch.dict(os.environ, {"SCIENCEDIRECT_API_KEY": "environment-key"}):
                self.env_file.write_text(value, encoding="utf-8")
                result = download(self.author)
                self.assertIsInstance(result, DownloadError)
                self.assertIn("missing or empty", result.error)
        fetch.assert_not_called()
        self.assertFalse(self.data.exists())

    @patch("source_downloaders.sciencedirect.fetch_page")
    def test_missing_or_unreadable_credential_file_is_safe(self, fetch):
        with patch.object(config, "ENV_FILE", self.root / "missing"):
            result = download(self.author)
            self.assertIsInstance(result, DownloadError)
            self.assertIn("credential file is missing", result.error)
        with patch("source_downloaders.sciencedirect.dotenv_values", side_effect=PermissionError("unknown-secret")):
            result = download(self.author)
        self.assertIsInstance(result, DownloadError)
        self.assertIn("PermissionError", result.error)
        self.assertNotIn("unknown-secret", result.error)
        fetch.assert_not_called()

    @patch("source_downloaders.sciencedirect.fetch_page", side_effect=[page(2, [article()]), RuntimeError("failure file-key")])
    def test_partial_retrieval_returns_sanitized_error_without_saving(self, fetch):
        with patch("source_downloaders.sciencedirect.storage.save_raw") as save, patch("source_downloaders.sciencedirect.normalize_article") as normalize:
            result = download(self.author)
        self.assertIsInstance(result, DownloadError)
        self.assertIn("Download failed", result.error)
        self.assertIn("[REDACTED]", result.error)
        self.assertNotIn("file-key", result.error)
        save.assert_not_called()
        normalize.assert_not_called()

    @patch("source_downloaders.sciencedirect.fetch_page", return_value=page(1, [article()]))
    def test_raw_save_failure_prevents_normalization(self, fetch):
        with patch("source_downloaders.sciencedirect.storage.save_raw", side_effect=OSError("disk error file-key")), \
             patch("source_downloaders.sciencedirect.normalize_article") as normalize:
            result = download(self.author)
        self.assertIsInstance(result, DownloadError)
        self.assertIn("Raw saving failed", result.error)
        self.assertNotIn("file-key", result.error)
        normalize.assert_not_called()

    @patch("source_downloaders.sciencedirect.fetch_page")
    def test_normalization_failure_retains_raw_and_previous_markdown(self, fetch):
        native = page(1, [article()])
        native["search-results"]["entry"][0]["dc:description"] = False
        fetch.return_value = native
        destination = self.data / self.author.slug / "previous.md"
        destination.parent.mkdir(parents=True)
        destination.write_text("Previous export", encoding="utf-8")
        result = download(self.author)
        self.assertIsInstance(result, DownloadError)
        paths = list(self.data.glob("*/raw/*.json"))
        self.assertEqual(len(paths), 1)
        self.assertEqual(json.loads(paths[0].read_text()), [native])
        self.assertIn("Normalization failed", result.error)
        self.assertIn(f"raw saved: {paths[0]}", result.error)
        self.assertEqual(destination.read_text(), "Previous export")

    @patch("source_downloaders.sciencedirect.fetch_page", return_value=page(1, [article()]))
    def test_normalization_exception_redacts_key_and_keeps_raw_path(self, fetch):
        with patch("source_downloaders.sciencedirect.normalize_article", side_effect=ValueError("bad metadata file-key")):
            result = download(self.author)
        self.assertIsInstance(result, DownloadError)
        self.assertNotIn("file-key", result.error)
        self.assertIn("[REDACTED]", result.error)
        self.assertIn("raw saved:", result.error)

    def test_imports_do_not_read_credentials(self):
        script = """
import sys
sys.path.insert(0, sys.argv[1])
from unittest.mock import patch
with patch('dotenv.dotenv_values', side_effect=AssertionError('credential read')):
    from source_downloaders import sciencedirect
    import download_manager
    import download_publications
"""
        result = subprocess.run([sys.executable, "-B", "-c", script, str(PROJECT_ROOT / "src")],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_registered_source_works_explicitly_and_through_all(self):
        self.assertEqual(download_manager.SUPPORTED_SOURCES, ("ieee", "sciencedirect"))
        self.assertIs(download_manager.DOWNLOADERS["sciencedirect"], download)
        for source in ["sciencedirect", "all"]:
            with self.subTest(source=source):
                ieee = Mock(return_value=DownloadRecord(self.author.name, "ieee", 0, [], Path("ieee.json")))
                request = parse_request(["--author", self.author.name, "--source", source])
                with patch("source_downloaders.sciencedirect.fetch_page", return_value=page(1, [article()])) as fetch, \
                     patch("download_manager.get_selected_authors", return_value=[self.author]), \
                     patch.dict(download_manager.DOWNLOADERS, {"ieee": ieee}):
                    downloads, builds = download_manager.run_download(request)
                expected = ["ieee", "sciencedirect"] if source == "all" else ["sciencedirect"]
                self.assertEqual([result.source for result in downloads], expected)
                self.assertEqual(len(builds), 1)
                self.assertIsNone(builds[0].error)
                text = builds[0].markdown_path.read_text(encoding="utf-8")
                self.assertIn("## Über Research", text)
                self.assertIn("Authors: First Author; Second Author", text)
                self.assertIn("Keywords: Control; Systems", text)
                self.assertIn("Year: 2026", text)
                fetch.assert_called_once()
                self.assertEqual(ieee.call_count, int(source == "all"))


class ScienceDirectRequestTests(unittest.TestCase):
    def test_query_uses_full_name_and_any_affiliation_without_date_filter(self):
        author = Author("René O'Neil", ("R&D University", "Institute B"))
        self.assertEqual(build_query(author),
                         '(authfirst("René") AND authlastname("O\'Neil")) '
                         'AND (aff("R&D University") OR aff("Institute B"))')

    def test_compound_names_keep_each_possible_given_and_family_split(self):
        author = Author("Ada van Researcher", ("University",))
        self.assertEqual(build_query(author),
                         '((authfirst("Ada") AND authlastname("van Researcher")) OR '
                         '(authfirst("Ada van") AND authlastname("Researcher"))) '
                         'AND (aff("University"))')

    def test_single_name_uses_surname_field(self):
        self.assertEqual(build_query(Author("Researcher", ("University",))),
                         'authlastname("Researcher") AND (aff("University"))')

    def test_invalid_search_literals_are_rejected(self):
        invalid = [Author("", ("University",)), Author("Ada", ()), Author("Ada", ("",))]
        invalid.extend(Author("Ada", (value,)) for value in ['A" OR authors(*)', "A\\B", "A*", "A?", "A\nB", "{A}"])
        for author in invalid:
            with self.subTest(author=author), self.assertRaises(ValueError):
                build_query(author)

    @patch("source_downloaders.sciencedirect.urlopen")
    def test_request_uses_complete_json_encoded_query_and_header_credentials(self, open_url):
        native = page(0, [], start=25)
        open_url.return_value.__enter__.return_value = io.BytesIO(json.dumps(native).encode())
        query = build_query(Author("René Researcher", ("R&D",)))
        self.assertEqual(fetch_page("secret-key", query, 25), native)
        request = open_url.call_args.args[0]
        url = urlsplit(request.full_url)
        self.assertEqual((url.scheme, url.netloc, url.path),
                         ("https", "api.elsevier.com", "/content/metadata/article"))
        self.assertEqual(parse_qs(url.query), {"query": [query], "view": ["COMPLETE"], "start": ["25"], "count": ["25"]})
        self.assertEqual(dict((key.lower(), value) for key, value in request.header_items()),
                         {"accept": "application/json", "x-els-apikey": "secret-key"})
        self.assertNotIn("secret-key", request.full_url)
        self.assertEqual(open_url.call_args.kwargs, {"timeout": 30})

    def test_transport_errors_are_safe_and_not_retried(self):
        secret = "https://example.invalid/secret-key"
        errors = [HTTPError(secret, code, secret, {}, None) for code in [401, 403, 429, 503]]
        errors.extend([URLError(secret), TimeoutError(secret), IncompleteRead(b"partial")])
        for error in errors:
            with self.subTest(error=error), patch("source_downloaders.sciencedirect.urlopen", side_effect=error) as open_url:
                with self.assertRaises(RuntimeError) as caught:
                    fetch_page("secret-key", "query", 0)
                self.assertNotIn("secret-key", str(caught.exception))
                self.assertNotIn("https://", str(caught.exception))
                open_url.assert_called_once()

    @patch("source_downloaders.sciencedirect.urlopen")
    def test_invalid_json_and_encoding_fail(self, open_url):
        for content in [b"<html>Bad gateway</html>", b"\xff"]:
            with self.subTest(content=content):
                open_url.return_value.__enter__.return_value = io.BytesIO(content)
                with self.assertRaises(ValueError):
                    fetch_page("secret-key", "query", 0)

    @patch("source_downloaders.sciencedirect.fetch_page")
    def test_complete_pagination_advances_by_actual_page_length(self, fetch):
        pages = [page(27, [article(i) for i in range(PAGE_SIZE)]),
                 page(27, [article(25)], start=25), page(27, [article(26)], start=26)]
        original = copy.deepcopy(pages)
        fetch.side_effect = pages
        self.assertEqual(download_pages("query", "key"), original)
        self.assertEqual(pages, original)
        self.assertEqual([request.args[2] for request in fetch.call_args_list], [0, 25, 26])

    @patch("source_downloaders.sciencedirect.fetch_page")
    def test_exact_page_boundary_stops_without_another_request(self, fetch):
        fetch.return_value = page(PAGE_SIZE, [article(i) for i in range(PAGE_SIZE)])
        self.assertEqual(len(download_pages("query", "key")), 1)
        fetch.assert_called_once()

    def test_invalid_counts_offsets_entries_and_api_errors_fail(self):
        invalid = [[], {}, {"error-response": {"error-code": "AUTHENTICATION_ERROR"}},
                   {"service-error": {"status": {"statusCode": "INVALID_INPUT"}}},
                   {"search-results": []}, page(0, [article()]), page(1, []), page(2, [article(), article()]),
                   page(1, [None]), page(1, [{}]), page(1, [{"error": "service unavailable"}]),
                   page(26, [article(i) for i in range(26)]), page(1, [article()], start=1)]
        for field in ["opensearch:totalResults", "opensearch:startIndex"]:
            for value in [None, True, -1, 1.5, "unknown"]:
                native = page(1, [article()])
                native["search-results"][field] = value
                invalid.append(native)
        for entries in [None, {}, "invalid"]:
            native = page(1, [])
            native["search-results"]["entry"] = entries
            invalid.append(native)
        for native in invalid:
            with self.subTest(native=native), patch("source_downloaders.sciencedirect.fetch_page", return_value=native):
                with self.assertRaises(ValueError):
                    download_pages("query", "key")

    def test_incomplete_changed_or_repeated_later_pages_fail(self):
        for pages in [[page(2, [article()]), page(2, [], start=1)],
                      [page(2, [article()]), page(3, [article(2)], start=1)],
                      [page(2, [article()]), page(2, [article()], start=1)]]:
            with self.subTest(pages=pages), patch("source_downloaders.sciencedirect.fetch_page", side_effect=pages):
                with self.assertRaises(ValueError):
                    download_pages("query", "key")


class ScienceDirectNormalizationTests(unittest.TestCase):
    def test_documented_fields_and_returned_author_order(self):
        self.assertEqual(normalize_article(article()), Publication(
            title="Über Research", authors=("First Author", "Second Author"), keywords=("Control", "Systems"),
            abstract="An abstract.", publication_title="A Journal", year="2026", issn="1234-5678",
            isbn="123; 456", doi="10.example/1",
        ))

    def test_missing_metadata_is_empty_without_inferred_affiliations_publisher_or_pdf(self):
        self.assertEqual(normalize_article({"pii": "S1"}), Publication())

    def test_single_author_creator_and_text_wrappers(self):
        native = {"authors": {"author": {"given-name": "Ada", "surname": "Researcher"}},
                  "dc:title": {"$": "Title"}, "authkeywords": [{"$": "A"}, "B"], "prism:coverDate": "2026-01-02"}
        self.assertEqual(normalize_article(native),
                         Publication(title="Title", authors=("Ada Researcher",), keywords=("A", "B"), year="2026"))
        self.assertEqual(normalize_article({"dc:creator": "Known Author"}).authors, ("Known Author",))

    def test_malformed_metadata_fails_instead_of_becoming_empty(self):
        for native in [{"authors": "bad"}, {"authors": {"author": [None]}},
                       {"authors": {"author": {"surname": False}}}, {"dc:title": {}},
                       {"dc:description": False}, {"authkeywords": [False]},
                       {"prism:coverDate": "unknown"}, {"prism:coverDate": [False]}]:
            with self.subTest(native=native), self.assertRaises(ValueError):
                normalize_article(native)
