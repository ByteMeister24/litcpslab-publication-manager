# Copyright (c) 2026 Mainak Majumder (@ByteMeister24)

"""Markdown schema rendering and publication to an explicitly supplied path."""

from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tests.support import full_article
from publication_normalizer.source_normalizers.ieee_xplore import _normalize_article
from helpers.author_builder import Author
from publication_model import Publication
from publication_markdown.markdown_models import MarkdownBuildResult
from publication_markdown.markdown_builder import build_markdown, _render_publications


class MarkdownTests(unittest.TestCase):
    def test_exact_existing_schema_including_all_labels_and_spacing(self):
        markdown = _render_publications([_normalize_article(full_article())])
        expected = """## Über Research Across Systems

Authors: First Author; Second Author

Author Affiliations: University A; Institute B

Keywords: Author keyword; Second keyword; IEEE term

Abstract: An abstract.

Publication: A Conference

Year: 2026

ISSN: 1234-5678

ISBN: 978-1-2345-6789-0

DOI: 10.example/work

Link: https://example.invalid/work.pdf

Publisher: IEEE
"""
        self.assertEqual(markdown, expected)

    def test_missing_fields_keep_labels_and_empty_dataset_is_empty(self):
        expected = ("## Title\n\nAuthors:\n\nAuthor Affiliations:\n\nKeywords:\n\nAbstract:\n\n"
                    "Publication:\n\nYear:\n\nISSN:\n\nISBN:\n\nDOI:\n\nLink:\n\nPublisher:\n")
        self.assertEqual(_render_publications([Publication(title="Title")]), expected)
        self.assertEqual(_render_publications([]), "")

    def test_record_order_is_preserved(self):
        markdown = _render_publications([Publication(title="First"), Publication(title="Second")])
        self.assertLess(markdown.index("## First"), markdown.index("## Second"))


class MarkdownBuilderTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.data = Path(directory.name)
        self.destination = self.data / "custom output" / "reviewed.md"
        self.author = Author("Ada Researcher", ("University A",))

    def previous_markdown(self):
        self.destination.parent.mkdir(parents=True)
        self.destination.write_text("Previous Markdown", encoding="utf-8")
        return self.destination

    def test_builder_returns_saved_markdown_path(self):
        result = build_markdown(self.author, self.destination, [Publication(title="Über Research")])
        destination = self.destination
        self.assertEqual(result, MarkdownBuildResult(self.author.name, markdown_path=destination))
        self.assertEqual(destination.read_text(encoding="utf-8"), _render_publications([Publication(title="Über Research")]))

    def test_successful_export_replaces_previous_final_markdown(self):
        destination = self.previous_markdown()
        result = build_markdown(self.author, destination, [Publication(title="Replacement")])
        self.assertEqual(result, MarkdownBuildResult(self.author.name, markdown_path=destination))
        self.assertEqual(destination.read_text(), _render_publications([Publication(title="Replacement")]))

    def test_builder_reports_failed_stage_and_preserves_previous_markdown(self):
        destination = self.previous_markdown()
        for target, stage in [("publication_markdown.markdown_builder._render_publications", "Markdown generation"),
                              ("utils.storage.os.replace", "Markdown saving")]:
            with self.subTest(stage=stage), patch(target, side_effect=OSError("disk error")):
                result = build_markdown(self.author, destination, [Publication(title="New work")])
            self.assertEqual(result, MarkdownBuildResult(self.author.name, error=f"{stage} failed: disk error"))
            self.assertEqual(destination.read_text(), "Previous Markdown")
            self.assertEqual(list(destination.parent.iterdir()), [destination])

    def test_generation_failure_does_not_call_storage(self):
        with patch("publication_markdown.markdown_builder._render_publications", side_effect=ValueError("invalid publication")), \
             patch("utils.storage.save_file") as save:
            result = build_markdown(self.author, self.destination, [Publication()])
        self.assertEqual(result.error, "Markdown generation failed: invalid publication")
        save.assert_not_called()
