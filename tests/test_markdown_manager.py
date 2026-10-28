"""Reviewed input selection, final publication, failure boundaries, and deletion."""

import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from support import AUTHOR_YAML
import config
from publication_model import Publication
from publication_markdown.markdown_builder import _render_publications
from publication_markdown.markdown_manager import run_markdown
from utils.storage import final_markdown_path, save_final_markdown


class MarkdownManagerTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.project = Path(directory.name)
        self.data = self.project / "data"
        authors = self.project / "authors.yaml"
        authors.write_text(AUTHOR_YAML, encoding="utf-8")
        for name, value in (("PROJECT_ROOT", self.project), ("DATA_DIRECTORY", self.data),
                            ("AUTHORS_FILE", authors), ("UPDATED_JSON_DIRECTORY_FORMAT", "{author_slug}/updated/")):
            patcher = patch.object(config, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.creation_times = {}
        timestamps = patch("publication_markdown.markdown_manager.get_creation_timestamp",
                           side_effect=lambda path: self.creation_times[path])
        timestamps.start()
        self.addCleanup(timestamps.stop)

    def review(self, records, name="Ada Researcher", timestamp="2026-10-28T14-30-00", directory=None, filename=None):
        if directory is None:
            directory = self.data / name.lower().replace(" ", "-") / "updated"
        path = directory / (filename or f"{name}-updated-{timestamp}.json")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")
        self.creation_times.setdefault(path, len(self.creation_times) + 1)
        return path

    def old_output(self, name="Ada Researcher"):
        return save_final_markdown(name.lower().replace(" ", "-"), name, "Previous final Markdown\n")

    def test_named_selection_is_case_insensitive_deduplicated_and_canonical(self):
        self.review([{"title": "René work"}], name="René Researcher")
        self.review([{"title": "Ada work"}])
        results = run_markdown(("RENÉ RESEARCHER", "ada researcher", "René Researcher"))
        self.assertEqual([result.author for result in results], ["René Researcher", "Ada Researcher"])
        self.assertEqual([result.status for result in results], ["generated", "generated"])
        self.assertEqual(results[0].markdown_path, self.data / "rené-researcher" / "final" / "René Researcher-final.md")

    def test_unknown_author_validates_before_any_generation(self):
        self.review([{"title": "Valid"}])
        with self.assertRaisesRegex(ValueError, "Unknown"), patch(
            "publication_markdown.markdown_manager._generate_markdown"
        ) as generate:
            run_markdown(("Ada Researcher", "Unknown"))
        generate.assert_not_called()

    def test_latest_creation_time_wins_over_filename_and_modification_time(self):
        older = self.review([{"title": "Older"}], timestamp="2099-10-27T23-59-59")
        latest = self.review([{"title": "Newest"}], timestamp="2000-10-28T14-30-00")
        os.utime(older, (2_000_000_000, 2_000_000_000))
        os.utime(latest, (1, 1))
        result, = run_markdown(("Ada Researcher",))
        self.assertEqual(result.reviewed_path, latest)
        self.assertEqual(result.markdown_path.read_text(), _render_publications([Publication(title="Newest")]))

    def test_configurable_review_directory_is_rooted_at_data_directory(self):
        for template in ("reviews/{author_slug}", str(self.project / "external reviews" / "{author_slug}")):
            with self.subTest(template=template), patch.object(config, "UPDATED_JSON_DIRECTORY_FORMAT", template):
                directory = self.data / template.format(author_slug="ada-researcher")
                review = self.review([{"title": "Custom input"}], directory=directory)
                result, = run_markdown(("Ada Researcher",))
                self.assertEqual(result.reviewed_path, review)
                self.assertEqual(result.status, "generated")
                self.assertEqual(result.markdown_path, final_markdown_path("ada-researcher", "Ada Researcher"))

    def test_review_edits_added_removed_order_and_duplicates_define_output(self):
        self.review([{"title": "Remove me"}, {"title": "Retain"}], timestamp="2026-10-27T14-30-00")
        result, = run_markdown(("Ada Researcher",))
        self.assertIn("Remove me", result.markdown_path.read_text())
        self.review([{"title": "Added", "authors": ["Someone Else"]}, {"title": "Retain"}, {"title": "Added"}])
        result, = run_markdown(("Ada Researcher",))
        expected = [Publication(title="Added", authors=("Someone Else",)), Publication(title="Retain"),
                    Publication(title="Added")]
        self.assertEqual(result.publication_count, 3)
        self.assertEqual(result.markdown_path.read_text(), _render_publications(expected))

    def test_no_review_never_falls_back_to_normalized_or_raw_and_preserves_final(self):
        destination = self.old_output()
        for folder in ("normalized", "download/ieee"):
            path = self.data / "ada-researcher" / folder / "data.json"
            path.parent.mkdir(parents=True)
            path.write_text('[{"title":"Unreviewed"}]')
        results = run_markdown("all")
        self.assertEqual([result.status for result in results], ["skipped", "skipped"])
        self.assertEqual(destination.read_text(), "Previous final Markdown\n")
        self.assertFalse((self.data / "rené-researcher").exists())

    def test_non_json_files_are_ignored(self):
        directory = self.data / "ada-researcher" / "updated"
        directory.mkdir(parents=True)
        (directory / "notes.md").write_text("Review notes")
        (directory / "subdirectory.json").mkdir()
        (directory / "subdirectory.json" / "nested.json").write_text("[]")
        result, = run_markdown(("Ada Researcher",))
        self.assertEqual(result.status, "skipped")

    def test_invalid_latest_review_does_not_fall_back_or_replace_final(self):
        destination = self.old_output()
        self.review([{"title": "Older valid"}], timestamp="2026-10-27T14-30-00")
        latest = self.review([])
        for content in ('[{', '[{"title":"Good"}, {"year":2026}]', '{}', '[{"extra":1}]', 'null'):
            with self.subTest(content=content):
                latest.write_text(content)
                result, = run_markdown(("Ada Researcher",))
                self.assertEqual(result.status, "failed")
                self.assertIn(str(latest), result.error)
                self.assertEqual(destination.read_text(), "Previous final Markdown\n")

    def test_arbitrary_json_filenames_are_supported(self):
        self.review([{"title": "Older"}])
        for name in ("other-author-updated-2026-10-28T14-30-00.json", "Ada Researcher-updated-bad.json",
                     "Ada Researcher-updated-2026-2-01T14-30-00.json",
                     "Ada Researcher-updated-2026-02-30T14-30-00.json", "reviewed.JSON"):
            latest = self.review([{"title": name}], filename=name)
            with self.subTest(name=name):
                result, = run_markdown(("Ada Researcher",))
                self.assertEqual(result.status, "generated")
                self.assertEqual(result.reviewed_path, latest)
                self.assertEqual(result.markdown_path.read_text(), _render_publications([Publication(title=name)]))

    def test_equal_creation_timestamps_use_filename_order(self):
        later_name = self.review([{"title": "Z"}], filename="z.json")
        first_name = self.review([{"title": "A"}], filename="a.json")
        self.creation_times[later_name] = self.creation_times[first_name] = 100.0
        result, = run_markdown(("Ada Researcher",))
        self.assertEqual(result.reviewed_path, first_name)
        self.assertEqual(result.markdown_path.read_text(), _render_publications([Publication(title="A")]))

    def test_creation_time_failure_preserves_final_without_fallback_and_continues(self):
        destination = self.old_output()
        self.review([{"title": "Older valid"}], filename="older.json")
        latest = self.review([{"title": "Latest"}], filename="latest.json")
        self.review([{"title": "Next author"}], name="René Researcher")

        def creation_time(path):
            if path == latest:
                raise ValueError(f"Creation timestamp unavailable for {path}.")
            return self.creation_times[path]

        with patch("publication_markdown.markdown_manager.get_creation_timestamp", side_effect=creation_time):
            results = run_markdown("all")
        self.assertEqual([result.status for result in results], ["failed", "generated"])
        self.assertIn(str(latest), results[0].error)
        self.assertEqual(destination.read_text(), "Previous final Markdown\n")

    def test_old_invalid_contents_are_not_read_after_selecting_latest(self):
        old = self.review([], timestamp="2026-10-27T14-30-00")
        old.write_text("Malformed old JSON")
        self.review([{"title": "Valid latest"}])
        result, = run_markdown(("Ada Researcher",))
        self.assertEqual(result.status, "generated")

    def test_unreadable_input_or_directory_error_preserves_final(self):
        destination = self.old_output()
        self.review([{"title": "Valid"}])
        for target in ("publication_markdown.markdown_manager.read_publications", "pathlib.Path.iterdir"):
            with self.subTest(target=target), patch(target, side_effect=PermissionError("Denied")):
                result, = run_markdown(("Ada Researcher",))
                self.assertEqual(result.status, "failed")
                self.assertIn("Denied", result.error)
                self.assertEqual(destination.read_text(), "Previous final Markdown\n")

    def test_input_path_must_be_a_directory(self):
        directory = self.data / "ada-researcher" / "updated"
        directory.parent.mkdir(parents=True)
        directory.write_text("Not a directory")
        result, = run_markdown(("Ada Researcher",))
        self.assertEqual(result.status, "failed")

    def test_empty_latest_review_deletes_only_exact_final_file(self):
        destination = self.old_output()
        sibling = destination.with_name("Another-final.md")
        sibling.write_text("Preserve sibling")
        self.review([{"title": "Old work"}], timestamp="2026-10-27T14-30-00")
        latest = self.review([])
        result, = run_markdown(("Ada Researcher",))
        self.assertEqual(result.status, "removed")
        self.assertEqual(result.reviewed_path, latest)
        self.assertEqual(result.markdown_path, destination)
        self.assertFalse(destination.exists())
        self.assertEqual(list(destination.parent.iterdir()), [sibling])
        self.assertEqual(sibling.read_text(), "Preserve sibling")
        self.assertEqual(latest.read_text(), "[]")

    def test_empty_review_absent_final_is_successful_noop_without_new_directories(self):
        self.review([])
        before = sorted(self.project.rglob("*"))
        for _ in range(2):
            result, = run_markdown(("Ada Researcher",))
            self.assertEqual(result.status, "removed")
            self.assertEqual(sorted(self.project.rglob("*")), before)
        self.assertFalse((self.data / "ada-researcher" / "final").exists())

    def test_removal_failure_preserves_previous_file_and_continues(self):
        destination = self.old_output()
        self.review([])
        self.review([{"title": "Next author"}], name="René Researcher")
        original_unlink = Path.unlink

        def fail_final(path, *args, **kwargs):
            if path == destination:
                raise PermissionError("Cannot remove final file")
            return original_unlink(path, *args, **kwargs)

        with patch.object(Path, "unlink", fail_final):
            results = run_markdown("all")
        self.assertEqual([result.status for result in results], ["failed", "generated"])
        self.assertIn("Final Markdown removal failed", results[0].error)
        self.assertEqual(destination.read_text(), "Previous final Markdown\n")

    def test_read_render_and_atomic_replace_failures_continue_other_authors(self):
        destination = self.old_output()
        self.review([{"title": "Replacement"}])
        self.review([{"title": "Next author"}], name="René Researcher")
        from publication_markdown import markdown_builder
        from utils import storage
        cases = (
            ("publication_markdown.markdown_manager.read_publications", None),
            ("publication_markdown.markdown_builder._render_publications", markdown_builder._render_publications),
            ("utils.storage.os.replace", storage.os.replace),
        )
        from publication_markdown.json_reader import read_publications
        for target, original in cases:
            original = original or read_publications
            calls = 0

            def fail_first(*args, **kwargs):
                nonlocal calls
                calls += 1
                if calls == 1:
                    raise OSError("First author failed")
                return original(*args, **kwargs)

            with self.subTest(target=target), patch(target, side_effect=fail_first):
                results = run_markdown("all")
            self.assertEqual([result.status for result in results], ["failed", "generated"])
            self.assertEqual(destination.read_text(), "Previous final Markdown\n")
            self.assertEqual(list(destination.parent.iterdir()), [destination])

    def test_raw_normalized_and_all_reviewed_files_remain_unchanged(self):
        review = self.review([{"title": "Über reviewed"}])
        old = self.review([{"title": "Older"}], timestamp="2026-10-27T14-30-00")
        inputs = [review, old]
        for folder in ("normalized", "download/ieee"):
            path = self.data / "ada-researcher" / folder / "original.json"
            path.parent.mkdir(parents=True)
            path.write_text('[{"title":"Original"}]')
            inputs.append(path)
        before = {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in inputs}
        result, = run_markdown(("Ada Researcher",))
        self.assertEqual(result.status, "generated")
        self.assertEqual({path: (path.read_bytes(), path.stat().st_mtime_ns) for path in inputs}, before)

    def test_atomic_replacement_publishes_complete_markdown_at_exact_path(self):
        destination = self.old_output()
        self.review([{"title": "Über replacement", "authors": ["René"]}])
        from utils import storage
        replace = storage.os.replace
        replacements = []

        def inspect_then_replace(source, target):
            self.assertEqual(destination.read_text(), "Previous final Markdown\n")
            self.assertEqual(Path(source).parent, destination.parent)
            self.assertEqual(Path(source).read_text(), _render_publications([
                Publication(title="Über replacement", authors=("René",)),
            ]))
            replacements.append(target)
            replace(source, target)

        with patch("utils.storage.os.replace", side_effect=inspect_then_replace):
            result, = run_markdown(("Ada Researcher",))
        self.assertEqual(result.status, "generated")
        self.assertEqual(replacements, [destination])
        self.assertEqual(list(destination.parent.iterdir()), [destination])
