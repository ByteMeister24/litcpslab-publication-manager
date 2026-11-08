"""Reviewed JSON validates the complete Publication contract without changing inputs."""

from dataclasses import asdict
import json
from pathlib import Path
import tempfile
import unittest

from tests import support
from publication_model import Publication
from publication_markdown.json_reader import read_publications


class MarkdownReaderTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / "review.json"

    def read(self, value):
        self.path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
        before = self.path.read_bytes()
        try:
            return read_publications(self.path)
        finally:
            self.assertEqual(self.path.read_bytes(), before)

    def test_all_fields_unicode_tuples_and_empty_defaults(self):
        publication = Publication(
            title="Über research\nReviewed", authors=("René", "Ada"), affiliations=("University A",),
            keywords=("control", "systems"), abstract="Reviewed abstract", publication_title="Journal",
            year="2026", issn="1234", isbn="5678", doi="10.example/review", pdf_url="https://example.invalid",
            publisher="Publisher",
        )
        self.assertEqual(self.read([asdict(publication), {}]), [publication, Publication()])
        self.assertEqual(self.read([]), [])

    def test_order_duplicates_and_missing_fields_are_preserved(self):
        records = [{"title": "Second", "authors": []}, {"title": "First"}, {"title": "Second", "authors": []}]
        self.assertEqual(self.read(records), [Publication(title="Second"), Publication(title="First"),
                                              Publication(title="Second")])

    def test_invalid_document_and_record_structures(self):
        for value in ({}, None, "text", 12, [None], [[]], ["title"], [True]):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.read(value)

    def test_every_field_rejects_incorrect_types(self):
        for name in asdict(Publication()):
            values = (None, 2026, True, {}, "Ada") if name in ("authors", "affiliations", "keywords") else (
                None, 2026, True, {}, [], ["Ada"], 1.5,
            )
            for value in values:
                with self.subTest(name=name, value=value), self.assertRaisesRegex(ValueError, name):
                    self.read([{name: value}])
        for name in ("authors", "affiliations", "keywords"):
            for value in (["Ada", None], [False], [2], [["Ada"]], [{}]):
                with self.subTest(name=name, value=value), self.assertRaisesRegex(ValueError, name):
                    self.read([{name: value}])

    def test_unknown_field_and_invalid_later_record_reject_entire_input(self):
        with self.assertRaisesRegex(ValueError, "Record 2 has unknown fields: extra"):
            self.read([{"title": "Valid"}, {"extra": "unsupported"}])
        with self.assertRaisesRegex(ValueError, "Record 2: year must be a string"):
            self.read([{"title": "Valid"}, {"year": 2026}])

    def test_bom_supported_and_invalid_json_or_encoding_rejected(self):
        self.path.write_text('\ufeff[{"title": "René"}]', encoding="utf-8")
        self.assertEqual(read_publications(self.path), [Publication(title="René")])
        for value in (b"[{", b"\xff"):
            self.path.write_bytes(value)
            with self.subTest(value=value), self.assertRaises((ValueError, UnicodeError)):
                read_publications(self.path)
            self.assertEqual(self.path.read_bytes(), value)
