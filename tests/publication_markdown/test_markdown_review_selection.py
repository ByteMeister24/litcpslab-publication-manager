# Copyright (c) 2026 Mainak Majumder (@ByteMeister24)

"""Author isolation for Google app exports in the shared reviewed directory."""

from datetime import datetime
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from zoneinfo import ZoneInfo

from tests.support import AUTHOR_YAML
import config
from publication_markdown.markdown_manager import run_markdown


class SharedReviewSelectionTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.data = self.root / "data"
        authors = self.root / "authors.yaml"
        authors.write_text(AUTHOR_YAML, encoding="utf-8")
        for name, value in (("DATA_DIRECTORY", self.data), ("AUTHORS_FILE", authors)):
            context = patch.object(config, name, value)
            context.start()
            self.addCleanup(context.stop)
        clock = patch("publication_markdown.markdown_manager.datetime")
        clock.start().now.return_value = datetime(2026, 10, 29, 12, tzinfo=ZoneInfo("Europe/Vienna"))
        self.addCleanup(clock.stop)

    def review(self, slug, records, timestamp="2026-10-29T10-00-00", extension=".json"):
        path = self.data / "reviewed" / f"{slug}-reviewed-{timestamp}{extension}"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")
        return path

    def final_path(self, slug):
        return self.data / "final" / f"{slug}-final-2026-10-29.md"

    def previous_final(self, slug):
        path = self.final_path(slug)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("Previous final Markdown", encoding="utf-8")
        return path

    def test_each_author_uses_only_their_export_and_inputs_are_preserved(self):
        ada = self.review("ada-researcher", [{"title": "Ada work", "authors": ["René Researcher"]}])
        rene = self.review("rené-researcher", [{"title": "René work"}], timestamp="2026-10-29T11-00-00")
        before = {path: path.read_bytes() for path in (ada, rene)}

        results = run_markdown("all")

        self.assertEqual([result.status for result in results], ["generated", "generated"])
        self.assertEqual([result.reviewed_path for result in results], [ada, rene])
        for result, slug, title in zip(results, ("ada-researcher", "rené-researcher"), ("Ada work", "René work")):
            self.assertEqual(result.markdown_path, self.final_path(slug))
            self.assertTrue(result.markdown_path.read_text(encoding="utf-8").startswith(f"## {title}\n"))
        self.assertEqual({path: path.read_bytes() for path in before}, before)

    def test_missing_author_review_skips_and_preserves_their_final(self):
        destination = self.previous_final("ada-researcher")
        self.review("rené-researcher", [{"title": "René work"}])

        result, = run_markdown(("Ada Researcher",))

        self.assertEqual(result.status, "skipped")
        self.assertIsNone(result.reviewed_path)
        self.assertEqual(destination.read_text(), "Previous final Markdown")

    def test_empty_review_removes_only_its_owners_current_final(self):
        self.previous_final("ada-researcher")
        rene_final = self.previous_final("rené-researcher")
        earlier = rene_final.with_name("rené-researcher-final-2026-10-28.md")
        earlier.write_text("Earlier final", encoding="utf-8")
        self.review("ada-researcher", [{"title": "Ada work"}])
        empty = self.review("rené-researcher", [], timestamp="2026-10-29T11-00-00")

        results = run_markdown("all")

        self.assertEqual([result.status for result in results], ["generated", "removed"])
        self.assertIn("## Ada work", self.final_path("ada-researcher").read_text())
        self.assertFalse(rene_final.exists())
        self.assertEqual(earlier.read_text(), "Earlier final")
        self.assertEqual(empty.read_text(), "[]")

    def test_invalid_review_fails_only_its_owner_and_preserves_their_final(self):
        self.review("ada-researcher", [{"title": "Ada work"}])
        invalid = self.review("rené-researcher", [{"year": 2026}])
        previous = self.previous_final("rené-researcher")

        results = run_markdown("all")

        self.assertEqual([result.status for result in results], ["generated", "failed"])
        self.assertEqual(results[1].reviewed_path, invalid)
        self.assertEqual(previous.read_text(), "Previous final Markdown")

    def test_duplicate_author_exports_fail_without_affecting_other_authors(self):
        self.review("ada-researcher", [{"title": "Older"}])
        self.review("ada-researcher", [{"title": "Newer"}], timestamp="2026-10-29T11-00-00")
        self.review("rené-researcher", [{"title": "René work"}])
        previous = self.previous_final("ada-researcher")

        results = run_markdown("all")

        self.assertEqual([result.status for result in results], ["failed", "generated"])
        self.assertIn("Multiple reviewed JSON files for ada-researcher", results[0].error)
        self.assertEqual(previous.read_text(), "Previous final Markdown")

    def test_unmatched_files_and_subdirectories_are_ignored(self):
        directory = self.data / "reviewed"
        directory.mkdir(parents=True)
        for name in ("reviewed-publications.json", "ada-researcher.json", "ada-researcher-reviewed-work.txt"):
            (directory / name).write_text("Invalid unrelated contents", encoding="utf-8")
        (directory / "ada-researcher-reviewed-nested.json").mkdir()

        results = run_markdown("all")

        self.assertEqual([result.status for result in results], ["skipped", "skipped"])
        self.assertFalse((self.data / "final").exists())

    def test_collision_suffix_and_uppercase_json_extension_are_supported(self):
        reviewed = self.review("ada-researcher", [{"title": "Ada work"}],
                               timestamp="2026-10-29T10-00-00-2", extension=".JSON")

        result, = run_markdown(("ADA RESEARCHER",))

        self.assertEqual(result.status, "generated")
        self.assertEqual(result.reviewed_path, reviewed)

    def test_review_marker_in_another_author_slug_does_not_match(self):
        self.review("ada-researcher-reviewed-junior", [{"title": "Another author's work"}])

        result, = run_markdown(("Ada Researcher",))

        self.assertEqual(result.status, "skipped")
