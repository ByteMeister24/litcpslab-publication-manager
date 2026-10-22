"""Schema rendering, publication history, and safe file publication."""

from datetime import datetime
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from zoneinfo import ZoneInfo

from support import full_article, page
import config
from csv_to_semantic_markdown import publication_to_markdown
from ieee_xplore import normalize_article
from author_builder import Author
from models import MarkdownBuildResult, Publication
from markdown_builder import build_markdown, _render_publications
from utils.storage import save_markdown, save_raw, write_complete_file


class MarkdownTests(unittest.TestCase):
    def test_exact_existing_schema_including_all_labels_and_spacing(self):
        markdown = _render_publications([normalize_article(full_article())])
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

    def test_record_order_and_legacy_csv_renderer_behavior(self):
        row = {"Document Title": " First\nTitle ", "Authors": "A; B", "Author Keywords": "X", "IEEE Terms": "Y"}
        common = Publication(title="First\nTitle", authors=("A", "B"), keywords=("X", "Y"))
        self.assertEqual(_render_publications([common]), publication_to_markdown(row) + "\n")
        markdown = _render_publications([Publication(title="First"), Publication(title="Second")])
        self.assertLess(markdown.index("## First"), markdown.index("## Second"))


class MarkdownBuilderTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.data = Path(directory.name)
        patcher = patch.object(config, "DATA_DIRECTORY", self.data)
        patcher.start()
        self.addCleanup(patcher.stop)
        clock = patch("utils.storage.datetime")
        clock.start().now.return_value = datetime(2026, 10, 22, 14, 30, tzinfo=ZoneInfo(config.DOWNLOAD_TIMEZONE))
        self.addCleanup(clock.stop)
        self.author = Author("Ada Researcher", ("University A",))

    def test_builder_returns_saved_markdown_path(self):
        result = build_markdown(self.author, "ieee", [Publication(title="Über Research")])
        destination = self.data / self.author.slug / "ada-researcher-ieee-2026-10-22.md"
        self.assertEqual(result, MarkdownBuildResult(self.author.name, "ieee", markdown_path=destination))
        self.assertEqual(destination.read_text(encoding="utf-8"), _render_publications([Publication(title="Über Research")]))

    def test_successful_empty_export_replaces_previous_markdown(self):
        destination = save_markdown(self.author.slug, "ieee", "Previous Markdown")
        result = build_markdown(self.author, "ieee", [])
        self.assertEqual(result, MarkdownBuildResult(self.author.name, "ieee", markdown_path=destination))
        self.assertEqual(destination.read_bytes(), b"")

    def test_builder_reports_failed_stage_and_preserves_previous_markdown(self):
        destination = save_markdown(self.author.slug, "ieee", "Previous Markdown")
        for target, stage in [("markdown_builder._render_publications", "Markdown generation"),
                              ("utils.storage.os.replace", "Markdown saving")]:
            with self.subTest(stage=stage), patch(target, side_effect=OSError("disk error")):
                result = build_markdown(self.author, "ieee", [Publication(title="New work")])
            self.assertEqual(result, MarkdownBuildResult(self.author.name, "ieee", error=f"{stage} failed: disk error"))
            self.assertEqual(destination.read_text(), "Previous Markdown")
            self.assertEqual(list(destination.parent.iterdir()), [destination])

    def test_generation_failure_does_not_call_storage(self):
        with patch("markdown_builder._render_publications", side_effect=ValueError("invalid publication")), \
             patch("utils.storage.save_markdown") as save:
            result = build_markdown(self.author, "ieee", [Publication()])
        self.assertEqual(result.error, "Markdown generation failed: invalid publication")
        save.assert_not_called()


class StorageTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.data = Path(directory.name)
        patcher = patch.object(config, "DATA_DIRECTORY", self.data)
        patcher.start()
        self.addCleanup(patcher.stop)
        clock = patch("utils.storage.datetime")
        self.clock = clock.start()
        self.clock.now.return_value = datetime(2026, 10, 22, 14, 30, tzinfo=ZoneInfo(config.DOWNLOAD_TIMEZONE))
        self.addCleanup(clock.stop)

    def test_markdown_filename_uses_creation_date_in_configured_timezone(self):
        self.clock.now.return_value = datetime(2026, 10, 22, 0, 30, tzinfo=ZoneInfo(config.DOWNLOAD_TIMEZONE))
        destination = save_markdown("ada-researcher", "ieee", "Über Research\n")
        self.clock.now.assert_called_once_with(ZoneInfo(config.DOWNLOAD_TIMEZONE))
        self.assertEqual(destination, self.data / "ada-researcher" / "ada-researcher-ieee-2026-10-22.md")
        self.assertEqual(destination.read_text(encoding="utf-8"), "Über Research\n")

    def test_markdown_exports_preserve_previous_dates_and_undated_files(self):
        author_directory = self.data / "ada-researcher"
        author_directory.mkdir()
        undated = author_directory / "ada-researcher-ieee.md"
        undated.write_text("Legacy export", encoding="utf-8")
        first = save_markdown("ada-researcher", "ieee", "First day")
        self.clock.now.return_value = datetime(2026, 10, 23, 14, 30, tzinfo=ZoneInfo(config.DOWNLOAD_TIMEZONE))
        second = save_markdown("ada-researcher", "ieee", "Second day")
        self.assertEqual(first.name, "ada-researcher-ieee-2026-10-22.md")
        self.assertEqual(second.name, "ada-researcher-ieee-2026-10-23.md")
        self.assertEqual(first.read_text(), "First day")
        self.assertEqual(second.read_text(), "Second day")
        self.assertEqual(undated.read_text(), "Legacy export")

    def test_identical_timestamps_produce_separate_dated_native_files(self):
        instant = datetime(2026, 10, 21, 14, 30, tzinfo=ZoneInfo(config.DOWNLOAD_TIMEZONE))
        with patch("utils.storage.datetime") as clock:
            clock.now.return_value = instant
            first = save_raw("ada-researcher", "ieee", [page(1, [1])])
            second = save_raw("ada-researcher", "ieee", [page(1, [2])])
        self.assertEqual(first.name, "ada-researcher-ieee-2026-10-21T14-30-00.000000+0200.json")
        self.assertEqual(second.name, "ada-researcher-ieee-2-2026-10-21T14-30-00.000000+0200.json")
        self.assertEqual(json.loads(first.read_text()), [page(1, [1])])
        self.assertEqual(json.loads(second.read_text()), [page(1, [2])])

    def test_history_cannot_be_overwritten_and_temporary_files_are_removed(self):
        destination = self.data / "raw.json"
        write_complete_file(destination, "original", replace=False)
        with self.assertRaises(FileExistsError):
            write_complete_file(destination, "replacement", replace=False)
        self.assertEqual(destination.read_text(), "original")
        self.assertEqual(list(self.data.iterdir()), [destination])

    def test_markdown_is_utf8_and_replaced_only_after_completed_write(self):
        destination = save_markdown("ada-researcher", "ieee", "Über old\n")
        with patch("utils.storage.os.replace", side_effect=OSError("disk error")):
            with self.assertRaises(OSError):
                save_markdown("ada-researcher", "ieee", "new")
        self.assertEqual(destination.read_text(encoding="utf-8"), "Über old\n")
        self.assertEqual(list(destination.parent.iterdir()), [destination])
        self.assertEqual(save_markdown("ada-researcher", "ieee", "new"), destination)
        self.assertEqual(destination.read_text(), "new")

    def test_failed_raw_publication_leaves_no_incomplete_file(self):
        destination = self.data / "raw" / "result.json"
        with patch("utils.storage.os.link", side_effect=OSError("disk error")):
            with self.assertRaises(OSError):
                write_complete_file(destination, "complete", replace=False)
        self.assertEqual(list(destination.parent.iterdir()), [])

    def test_invalid_json_is_not_published(self):
        with self.assertRaises(ValueError):
            save_raw("ada-researcher", "ieee", [{"invalid": float("nan")}])
        self.assertEqual(list(self.data.iterdir()), [])
