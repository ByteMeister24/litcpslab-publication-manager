"""Persisted JSON, Springer CSV, and ACM BibTeX conversion contracts."""

import csv
from dataclasses import asdict
import json
from pathlib import Path
import tempfile
import unittest

from support import full_article, page
from publication_model import Publication
from publication_normalizer.source_normalizers import acm, ieee_xplore, sciencedirect, springer


class SourceNormalizerTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)

    def json_file(self, payload):
        path = self.root / "download.json"
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return path

    def csv_file(self, rows, columns=springer.REQUIRED_COLUMNS):
        path = self.root / "SearchResults.csv"
        with path.open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)
        return path

    def test_ieee_reads_all_pages_in_record_order(self):
        first, second = full_article(), {"title": "Second", "article_number": "11"}
        path = self.json_file([{"total_records": 2, "articles": [first]},
                               {"total_records": 2, "articles": [second]}])
        before = path.read_bytes()
        result = ieee_xplore.normalize_file(path)
        self.assertEqual(result, [ieee_xplore._normalize_article(first), Publication(title="Second")])
        self.assertEqual(path.read_bytes(), before)

    def test_sciencedirect_reads_all_pages_and_returned_metadata_only(self):
        path = self.json_file([
            {"search-results": {"entry": [{"dc:title": "First", "dc:creator": "René", "authkeywords": "A|B"}]}},
            {"search-results": {"entry": [{"dc:title": "Second", "prism:coverDate": "2026-10-27"}]}},
        ])
        self.assertEqual(sciencedirect.normalize_file(path), [
            Publication(title="First", authors=("René",), keywords=("A", "B")),
            Publication(title="Second", year="2026"),
        ])

    def test_zero_result_api_shapes_produce_empty_lists(self):
        cases = (
            (ieee_xplore, [{"total_records": 0}]),
            (ieee_xplore, [page(0, [])]),
            (ieee_xplore, [{"totalfound": "0"}]),
            (sciencedirect, [{"search-results": {"opensearch:totalResults": "0"}}]),
            (sciencedirect, [{"search-results": {"opensearch:totalResults": "0", "entry": []}}]),
            (sciencedirect, [{"search-results": {"opensearch:totalResults": "0", "entry": [
                {"error": "Result set was empty"}]}}]),
        )
        for normalizer, payload in cases:
            with self.subTest(normalizer=normalizer, payload=payload):
                self.assertEqual(normalizer.normalize_file(self.json_file(payload)), [])

    def test_api_files_reject_invalid_page_and_article_shapes(self):
        for normalizer in (ieee_xplore, sciencedirect):
            for payload in ([], {}, [None], [{"error": "failed"}]):
                with self.subTest(normalizer=normalizer, payload=payload), self.assertRaises(ValueError):
                    normalizer.normalize_file(self.json_file(payload))
        for normalizer, payload in (
            (ieee_xplore, [{"articles": [None]}]),
            (sciencedirect, [{"search-results": {"entry": [None]}}]),
            (sciencedirect, [{"search-results": {"entry": [{"error": "failed"}]}}]),
        ):
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                normalizer.normalize_file(self.json_file(payload))

    def test_malformed_article_rejects_the_entire_file(self):
        path = self.json_file([{"articles": [{"title": "Valid"}, {"authors": "invalid"}]}])
        with self.assertRaises(ValueError):
            ieee_xplore.normalize_file(path)

    def test_springer_maps_only_agreed_fields_and_preserves_content_types(self):
        columns = (*springer.REQUIRED_COLUMNS, "Content Type", "Book Series Title", "Publisher", "Abstract")
        path = self.csv_file([
            {"Item Title": " Über research\nwith systems ", "Publication Title": " A Journal ",
             "Item DOI": "10.example/one", "Authors": "Mainak Majumder, Alois Zoitl, , René Researcher",
             "Publication Year": "2026", "URL": "https://link.springer.com/article/10.example/one",
             "Content Type": "Article", "Book Series Title": "Not the containing publication",
             "Publisher": "Unmapped publisher", "Abstract": "Unmapped abstract"},
            {"Item Title": "Collection", "Item DOI": "collection-id", "Content Type": "Collection"},
        ], columns)
        original = path.read_bytes()
        self.assertEqual(springer.normalize_file(path), [
            Publication(title="Über research\nwith systems", publication_title="A Journal", doi="10.example/one",
                        authors=("Mainak Majumder", "Alois Zoitl", "René Researcher"), year="2026",
                        pdf_url="https://link.springer.com/article/10.example/one"),
            Publication(title="Collection", doi="collection-id"),
        ])
        self.assertEqual(path.read_bytes(), original)

    def test_springer_does_not_guess_boundaries_in_author_text(self):
        result = springer.normalize_file(self.csv_file([
            {"Item Title": "A", "Authors": "Mainak MajumderAlois Zoitl"}]))
        self.assertEqual(result[0].authors, ("Mainak MajumderAlois Zoitl",))

    def test_header_only_and_blank_csv_rows_are_successful_empty_inputs(self):
        self.assertEqual(springer.normalize_file(self.csv_file([])), [])
        self.assertEqual(springer.normalize_file(self.csv_file([{}])), [])

    def test_springer_rejects_missing_duplicate_and_malformed_columns(self):
        cases = ("", "Item Title\nA\n", "Item Title,Item Title\nA,B\n",
                 ",".join(springer.REQUIRED_COLUMNS) + '\n"unterminated',
                 ",".join(springer.REQUIRED_COLUMNS) + "\nA,B,C,D,E,F,extra\n")
        for content in cases:
            path = self.root / "invalid.csv"
            path.write_text(content, encoding="utf-8")
            with self.subTest(content=content), self.assertRaises(ValueError):
                springer.normalize_file(path)

    def test_acm_reuses_existing_bibtex_mapping(self):
        path = self.root / "export.bib"
        path.write_text('@inproceedings{one, title={Über Systems}, author={Ada and René}, '
                        'booktitle={A Conference}, year={2026}, url={https://example.invalid/work}}', encoding="utf-8")
        self.assertEqual(acm.normalize_file(path), [Publication(
            title="Über Systems", authors=("Ada", "René"), publication_title="A Conference",
            year="2026", pdf_url="https://example.invalid/work")])
        self.assertEqual(set(asdict(acm.normalize_file(path)[0])), set(asdict(Publication())))
