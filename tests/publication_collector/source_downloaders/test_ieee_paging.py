# Copyright (c) 2026 Mainak Majumder (@ByteMeister24)

"""IEEE transport and pagination regression tests; all HTTP is mocked."""

from http.client import IncompleteRead
import io
import json
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlsplit

from tests.support import page
from helpers.author_builder import Author
from publication_collector.source_downloaders.ieee_xplore import PAGE_SIZE, _build_query, _download_pages, _fetch_page


class IEEEDownloadTests(unittest.TestCase):
    def setUp(self):
        self.author = Author("Ada Researcher", ("University A", "Institute B"))

    def test_query_scopes_each_term_and_groups_affiliations(self):
        self.assertEqual(_build_query(self.author),
                         '"Authors":"Ada Researcher" AND '
                         '("Author Affiliations":"University A" OR "Author Affiliations":"Institute B")')

    def test_unsupported_search_syntax_is_rejected(self):
        for author in [Author("", ("University",)), Author("Ada", ()),
                       Author('Ada "Researcher"', ("University",)),
                       Author("Ada", ("University*",)), Author("Ada", ("",))]:
            with self.subTest(author=author), self.assertRaises(ValueError):
                _build_query(author)

    @patch("publication_collector.source_downloaders.ieee_xplore.urlopen")
    def test_request_uses_encoded_query_paging_and_https(self, open_url):
        response = page(1, [10])
        open_url.return_value.__enter__.return_value = io.BytesIO(json.dumps(response).encode())
        author = Author("René O'Neil", ("R&D University",))
        self.assertEqual(_fetch_page("test-key", _build_query(author), 201), response)
        request = open_url.call_args.args[0]
        url = urlsplit(request.full_url)
        self.assertEqual((url.scheme, url.netloc), ("https", "ieeexploreapi.ieee.org"))
        parameters = parse_qs(url.query)
        self.assertEqual(parameters, {
            "apikey": ["test-key"], "format": ["json"], "querytext": [_build_query(author)],
            "start_record": ["201"], "max_records": ["200"],
            "sort_field": ["article_number"], "sort_order": ["asc"],
        })
        self.assertGreater(open_url.call_args.kwargs["timeout"], 0)

    @patch("publication_collector.source_downloaders.ieee_xplore._fetch_page")
    def test_all_pages_and_unknown_native_metadata_are_preserved(self, fetch):
        pages = [page(201, range(1, 201)), page(201, [201])]
        pages[0]["extra_native_field"] = {"untouched": ["é", True]}
        fetch.side_effect = pages
        self.assertEqual(_download_pages(self.author, "test-key"), pages)
        self.assertEqual([call.args[2] for call in fetch.call_args_list], [1, 201])

    @patch("publication_collector.source_downloaders.ieee_xplore._fetch_page")
    def test_short_intermediate_pages_advance_by_actual_record_count(self, fetch):
        pages = [page(3, [1]), page(3, [2, 3])]
        fetch.side_effect = pages
        self.assertEqual(_download_pages(self.author, "test-key"), pages)
        self.assertEqual([call.args[2] for call in fetch.call_args_list], [1, 2])

    @patch("publication_collector.source_downloaders.ieee_xplore._fetch_page")
    def test_exact_page_boundary_does_not_request_an_extra_page(self, fetch):
        fetch.return_value = page(PAGE_SIZE, range(PAGE_SIZE))
        self.assertEqual(len(_download_pages(self.author, "test-key")), 1)
        fetch.assert_called_once()

    @patch("publication_collector.source_downloaders.ieee_xplore._fetch_page")
    def test_zero_results_can_omit_the_unpopulated_articles_field(self, fetch):
        fetch.return_value = {"total_records": 0}
        self.assertEqual(_download_pages(self.author, "test-key"), [{"total_records": 0}])
        fetch.assert_called_once()

    @patch("publication_collector.source_downloaders.ieee_xplore._fetch_page")
    def test_documented_count_name_and_string_count(self, fetch):
        fetch.return_value = {"totalfound": "1", "articles": [{"article_number": 10}]}
        self.assertEqual(len(_download_pages(self.author, "test-key")), 1)

    def test_malformed_and_error_responses_fail(self):
        invalid_pages = [
            [], {}, {"error": "invalid key"}, {"errors": ["quota exceeded"]},
            {"total_records": -1}, {"total_records": True}, {"total_records": 1.5},
            {"total_records": "unknown"}, {"total_records": 1},
            {"total_records": 1, "articles": {}}, {"total_records": 1, "articles": [None]},
            {"total_records": 1, "articles": [{}]},
            page(0, [1]), page(1, []), page(2, [1, 1]),
            page(PAGE_SIZE + 1, range(PAGE_SIZE + 1)),
        ]
        for invalid in invalid_pages:
            with self.subTest(response=invalid), patch("publication_collector.source_downloaders.ieee_xplore._fetch_page", return_value=invalid):
                with self.assertRaises(ValueError):
                    _download_pages(self.author, "test-key")

    def test_incomplete_changed_or_repeated_later_pages_fail(self):
        for responses in [[page(2, [1]), page(2, [])],
                          [page(2, [1]), page(3, [2])],
                          [page(2, [1]), page(2, [1])]]:
            with self.subTest(responses=responses), patch("publication_collector.source_downloaders.ieee_xplore._fetch_page", side_effect=responses):
                with self.assertRaises(ValueError):
                    _download_pages(self.author, "test-key")

    def test_transport_errors_do_not_disclose_key_or_request_url(self):
        secret_url = "https://example.invalid/?apikey=secret-key"
        errors = [HTTPError(secret_url, 429, secret_url, {}, None), URLError(secret_url),
                  TimeoutError(secret_url), IncompleteRead(b"partial")]
        for error in errors:
            with self.subTest(error=error), patch("publication_collector.source_downloaders.ieee_xplore.urlopen", side_effect=error):
                with self.assertRaises(RuntimeError) as caught:
                    _fetch_page("secret-key", "query", 1)
                self.assertNotIn("secret-key", str(caught.exception))
                self.assertNotIn("https://", str(caught.exception))

    @patch("publication_collector.source_downloaders.ieee_xplore.urlopen")
    def test_invalid_json_and_encoding_fail(self, open_url):
        for content in [b"<html>Bad gateway</html>", b"\xff"]:
            with self.subTest(content=content):
                open_url.return_value.__enter__.return_value = io.BytesIO(content)
                with self.assertRaises(ValueError):
                    _fetch_page("test-key", "query", 1)
