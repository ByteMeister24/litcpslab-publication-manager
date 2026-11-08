"""Uniform IEEE source contract, direct file credentials, and normalization."""

import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tests.support import PROJECT_ROOT, full_article, page
import config
from publication_collector.source_downloaders.ieee_xplore import download
from publication_normalizer.source_normalizers.ieee_xplore import _normalize_article
from helpers.author_builder import Author
from publication_collector.download_models import DownloadConfirmation, DownloadError
from publication_model import Publication


class IEEESourceTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.env_file = Path(directory.name) / ".env"
        self.env_file.write_text("IEEE_API_KEY=file-key\n", encoding="utf-8")
        self.env_patch = patch.object(config, "ENV_FILE", self.env_file)
        self.env_patch.start()
        self.addCleanup(self.env_patch.stop)
        data_patch = patch.object(config, "DATA_DIRECTORY", self.env_file.parent / "data")
        data_patch.start()
        self.addCleanup(data_patch.stop)
        self.author = Author("Ada Researcher", ("University A",))

    @patch("publication_collector.source_downloaders.ieee_xplore._fetch_page")
    def test_download_returns_confirmation_and_unchanged_raw_pages(self, fetch):
        raw = {"total_records": 1, "articles": [full_article()]}
        expected_raw = copy.deepcopy(raw)
        fetch.return_value = raw
        result = download(self.author)
        assert isinstance(result, DownloadConfirmation)
        self.assertEqual((result.author, result.source, result.publication_count), (self.author.name, "ieee", 1))
        self.assertEqual(json.loads(result.raw_file_path.read_text(encoding="utf-8")), [expected_raw])
        self.assertEqual(set(vars(result)), {"author", "source", "publication_count", "raw_file_path"})

    @patch("publication_collector.source_downloaders.ieee_xplore._fetch_page", return_value=page(0, []))
    def test_zero_publications_returns_confirmation_and_saves_raw_metadata(self, fetch):
        result = download(self.author)
        assert isinstance(result, DownloadConfirmation)
        self.assertEqual((result.author, result.source, result.publication_count), (self.author.name, "ieee", 0))
        self.assertEqual(json.loads(result.raw_file_path.read_text()), [page(0, [])])

    @patch("publication_collector.source_downloaders.ieee_xplore._fetch_page", return_value=page(0, []))
    def test_file_key_wins_over_process_environment(self, fetch):
        with patch.dict(os.environ, {"IEEE_API_KEY": "environment-key"}):
            download(self.author)
        self.assertEqual(fetch.call_args.args[0], "file-key")

    @patch("publication_collector.source_downloaders.ieee_xplore._fetch_page", return_value=page(0, []))
    def test_file_interpolation_is_disabled(self, fetch):
        self.env_file.write_text('IEEE_API_KEY=${OTHER_KEY}\n', encoding="utf-8")
        with patch.dict(os.environ, {"OTHER_KEY": "environment-secret"}):
            download(self.author)
        self.assertEqual(fetch.call_args.args[0], "${OTHER_KEY}")

    @patch("publication_collector.source_downloaders.ieee_xplore._fetch_page")
    def test_missing_empty_or_unassigned_key_never_falls_back_to_environment(self, fetch):
        for text in ["", "OTHER=value\n", "IEEE_API_KEY=\n", "IEEE_API_KEY\n", "IEEE_API_KEY='  '\n"]:
            with self.subTest(text=text), patch.dict(os.environ, {"IEEE_API_KEY": "environment-key"}):
                self.env_file.write_text(text, encoding="utf-8")
                result = download(self.author)
                assert isinstance(result, DownloadError)
                self.assertEqual((result.author, result.source), (self.author.name, "ieee"))
                self.assertIn("missing or empty", result.error)
        fetch.assert_not_called()

    @patch("publication_collector.source_downloaders.ieee_xplore._fetch_page")
    def test_missing_and_unreadable_file_fail_without_network(self, fetch):
        with patch.object(config, "ENV_FILE", self.env_file.parent / "missing"):
            result = download(self.author)
            assert isinstance(result, DownloadError)
            self.assertIn("credential file is missing", result.error)
        with patch("publication_collector.source_downloaders.common.dotenv_values", side_effect=PermissionError("secret-key")):
            result = download(self.author)
        assert isinstance(result, DownloadError)
        self.assertIn("Cannot read IEEE credential file (PermissionError)", result.error)
        self.assertNotIn("secret-key", result.error)
        fetch.assert_not_called()

    @patch("publication_collector.source_downloaders.ieee_xplore._fetch_page", side_effect=RuntimeError("failure containing file-key"))
    def test_source_sanitizes_errors_before_middleware_receives_them(self, fetch):
        result = download(self.author)
        assert isinstance(result, DownloadError)
        self.assertEqual((result.author, result.source), (self.author.name, "ieee"))
        self.assertNotIn("file-key", result.error)
        self.assertIn("[REDACTED]", result.error)
        self.assertNotIn("raw saved:", result.error)

    def test_unexpected_source_exceptions_are_returned_as_errors(self):
        for error in [RuntimeError("service unavailable"), KeyError("bad response file-key")]:
            with self.subTest(error=error), patch("publication_collector.source_downloaders.ieee_xplore._download_pages", side_effect=error):
                result = download(self.author)
            assert isinstance(result, DownloadError)
            self.assertEqual((result.author, result.source), (self.author.name, "ieee"))
            self.assertIn("Download failed:", result.error)
            self.assertNotIn("file-key", result.error)

    @patch("publication_collector.source_downloaders.ieee_xplore._fetch_page")
    def test_metadata_needing_review_does_not_fail_a_completed_download(self, fetch):
        raw = page(1, [1])
        raw["articles"][0]["authors"] = "malformed"
        fetch.return_value = raw
        result = download(self.author)
        assert isinstance(result, DownloadConfirmation)
        paths = list(config.DATA_DIRECTORY.rglob("*.json"))
        self.assertEqual(len(paths), 1)
        self.assertEqual(json.loads(paths[0].read_text()), [raw])
        self.assertEqual(result.raw_file_path, paths[0])
        self.assertEqual(result.publication_count, 1)

    @patch("publication_collector.source_downloaders.ieee_xplore._fetch_page")
    def test_all_pages_are_saved_without_normalization(self, fetch):
        pages = [page(2, [1]), page(2, [2])]
        fetch.side_effect = pages

        with patch("publication_normalizer.source_normalizers.ieee_xplore._normalize_article") as normalize:
            result = download(self.author)
        assert isinstance(result, DownloadConfirmation)
        self.assertEqual(fetch.call_count, 2)
        self.assertEqual(json.loads(result.raw_file_path.read_text()), pages)
        normalize.assert_not_called()
        self.assertEqual(result.publication_count, 2)

    @patch("publication_collector.source_downloaders.ieee_xplore._fetch_page", side_effect=[page(2, [1]), RuntimeError("HTTP 503")])
    def test_incomplete_retrieval_never_saves_raw_or_normalizes(self, fetch):
        with patch("utils.storage.save_file") as save, patch("publication_normalizer.source_normalizers.ieee_xplore._normalize_article") as normalize:
            result = download(self.author)
        assert isinstance(result, DownloadError)
        self.assertNotIn("raw saved:", result.error)
        save.assert_not_called()
        normalize.assert_not_called()

    @patch("publication_collector.source_downloaders.ieee_xplore._fetch_page", return_value=page(1, [1]))
    def test_raw_storage_failure_is_sanitized_and_prevents_normalization(self, fetch):
        with patch("utils.storage.save_file", side_effect=OSError("disk error file-key")), \
             patch("publication_normalizer.source_normalizers.ieee_xplore._normalize_article") as normalize:
            result = download(self.author)
        assert isinstance(result, DownloadError)
        self.assertIn("Raw saving failed", result.error)
        self.assertNotIn("file-key", result.error)
        self.assertNotIn("raw saved:", result.error)
        normalize.assert_not_called()

    def test_imports_do_not_read_credentials(self):
        script = """
import sys
sys.path.insert(0, sys.argv[1])
from unittest.mock import patch
with patch('dotenv.dotenv_values', side_effect=AssertionError('credential read')):
    from publication_collector.source_downloaders import ieee_xplore
    from publication_collector import download_manager
    from publication_collector.cli import download_publications
print('imports OK')
"""
        result = subprocess.run([sys.executable, "-B", "-c", script, str(PROJECT_ROOT / "src")],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "imports OK")


class NormalizationTests(unittest.TestCase):
    def test_all_schema_fields_and_author_order(self):
        publication = _normalize_article(full_article())
        self.assertEqual(publication, Publication(
            title="Über Research\nAcross Systems", authors=("First Author", "Second Author"),
            affiliations=("University A", "Institute B"),
            keywords=("Author keyword", "Second keyword", "IEEE term"), abstract="An abstract.",
            publication_title="A Conference", year="2026", issn="1234-5678", isbn="978-1-2345-6789-0",
            doi="10.example/work", pdf_url="https://example.invalid/work.pdf", publisher="IEEE",
        ))

    def test_missing_metadata_is_empty_without_search_affiliation_substitution(self):
        self.assertEqual(_normalize_article({"article_number": "1"}), Publication())

    def test_author_order_falls_back_to_returned_order(self):
        article = full_article()
        del article["authors"]["authors"][0]["author_order"]
        self.assertEqual(_normalize_article(article).authors, ("Second Author", "First Author"))

    def test_multiple_affiliations_and_identifiers_are_preserved(self):
        article = {"authors": {"authors": [{"full_name": "A", "affiliation": ["X", "Y"]}]},
                   "isbn": ["123", "456"]}
        normalized = _normalize_article(article)
        self.assertEqual(normalized.affiliations, ("X", "Y"))
        self.assertEqual(normalized.isbn, "123; 456")

    def test_malformed_metadata_is_not_silently_rendered_as_missing(self):
        for fields in [{"authors": "text"}, {"authors": {"authors": [None]}},
                       {"index_terms": []}, {"index_terms": {"author_terms": {"terms": [False]}}},
                       {"abstract": {}}, {"publication_year": True},
                       {"authors": {"authors": [{"author_order": 1.5}]}},
                       {"authors": {"authors": [{"author_order": True}]}},
                       {"authors": {"authors": [{"author_order": "invalid"}]}}]:
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                _normalize_article(fields)
