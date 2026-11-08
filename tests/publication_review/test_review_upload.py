"""Index normalized publications without copying or modifying their files."""

from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tests.support import AUTHOR_YAML
import config
from publication_review.prepare_upload import main, prepare_upload


class ReviewUploadTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.data = self.root / "data"
        self.normalized_directory = self.data / "normalized"
        self.index_file = self.normalized_directory / "authors.json"
        authors = self.root / "authors.yaml"
        authors.write_text(AUTHOR_YAML, encoding="utf-8")
        for name, value in (("DATA_DIRECTORY", self.data), ("AUTHORS_FILE", authors)):
            patcher = patch.object(config, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def normalized(self, slug, records):
        path = self.normalized_directory / config.NORMALIZED_FILENAME_FORMAT.format(author_slug=slug)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")
        return path

    def test_index_preserves_canonical_names_order_and_existing_files(self):
        source = self.normalized("ada-researcher", [{"title": "Über work", "authors": ["René"]}, {"title": "Über work"}])
        second = self.normalized("rené-researcher", [])
        before = {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in (source, second)}
        count, skipped = prepare_upload()
        self.assertEqual((count, skipped), (2, []))
        manifest = json.loads(self.index_file.read_text(encoding="utf-8"))
        self.assertEqual(manifest, {"version": 1, "authors": [
            {"id": "ada-researcher", "name": "Ada Researcher", "sourceFile": source.name},
            {"id": "rené-researcher", "name": "René Researcher", "sourceFile": second.name},
        ]})
        self.assertEqual(set(self.normalized_directory.iterdir()), {source, second, self.index_file})
        self.assertEqual(set(self.data.iterdir()), {self.normalized_directory})
        self.assertEqual({path: (path.read_bytes(), path.stat().st_mtime_ns) for path in before}, before)

    def test_configured_filenames_are_referenced_without_renaming(self):
        with patch.object(config, "NORMALIZED_FILENAME_FORMAT", "publications {author_slug}.json"):
            source = self.normalized("ada-researcher", [])
            prepare_upload(("Ada Researcher",))
        manifest = json.loads(self.index_file.read_text(encoding="utf-8"))
        self.assertEqual(manifest["authors"][0]["sourceFile"], source.name)
        self.assertEqual(set(self.normalized_directory.iterdir()), {source, self.index_file})

    def test_missing_author_inputs_are_skipped(self):
        self.normalized("ada-researcher", [])
        self.assertEqual(prepare_upload(), (1, ["René Researcher"]))

    def test_missing_all_inputs_leaves_output_absent(self):
        with self.assertRaisesRegex(ValueError, "No normalized"):
            prepare_upload()
        self.assertFalse(self.normalized_directory.exists())

    def test_invalid_input_does_not_create_a_partial_index(self):
        self.normalized("ada-researcher", [{"title": "Valid"}])
        self.normalized("rené-researcher", [{"year": 2026}])
        with self.assertRaisesRegex(ValueError, "year"):
            prepare_upload()
        self.assertFalse(self.index_file.exists())

    def test_rerun_refreshes_index_and_preserves_other_files(self):
        source = self.normalized("ada-researcher", [])
        second = self.normalized("rené-researcher", [])
        prepare_upload()
        marker = self.normalized_directory / "existing.txt"
        marker.write_text("Preserve me")
        self.assertEqual(prepare_upload(("René Researcher",)), (1, []))
        manifest = json.loads(self.index_file.read_text(encoding="utf-8"))
        self.assertEqual([item["name"] for item in manifest["authors"]], ["René Researcher"])
        self.assertEqual(set(self.normalized_directory.iterdir()), {source, second, marker, self.index_file})
        self.assertEqual(marker.read_text(), "Preserve me")

    def test_invalid_input_preserves_existing_index(self):
        self.normalized("ada-researcher", [])
        self.normalized("rené-researcher", [])
        prepare_upload()
        before = self.index_file.read_bytes(), self.index_file.stat().st_mtime_ns
        self.normalized("rené-researcher", [{"year": 2026}])
        with self.assertRaisesRegex(ValueError, "year"):
            prepare_upload()
        self.assertEqual((self.index_file.read_bytes(), self.index_file.stat().st_mtime_ns), before)

    def test_save_failure_preserves_existing_index_and_cleans_temporary_files(self):
        source = self.normalized("ada-researcher", [])
        second = self.normalized("rené-researcher", [])
        prepare_upload()
        before = self.index_file.read_bytes(), self.index_file.stat().st_mtime_ns
        with patch("utils.storage.os.replace", side_effect=OSError("disk full")):
            with self.assertRaisesRegex(OSError, "disk full"):
                prepare_upload(("René Researcher",))
        self.assertEqual((self.index_file.read_bytes(), self.index_file.stat().st_mtime_ns), before)
        self.assertEqual(set(self.normalized_directory.iterdir()), {source, second, self.index_file})

    def test_selection_is_case_insensitive_and_limits_the_index(self):
        self.normalized("ada-researcher", [])
        self.normalized("rené-researcher", [])
        count, skipped = prepare_upload(("RENÉ RESEARCHER",))
        self.assertEqual((count, skipped), (1, []))
        manifest = json.loads(self.index_file.read_text(encoding="utf-8"))
        self.assertEqual([item["name"] for item in manifest["authors"]], ["René Researcher"])

    def test_cli_reports_success_failure_and_usage_errors(self):
        self.normalized("ada-researcher", [])
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            self.assertEqual(main([]), 0)
            self.assertEqual(main([]), 0)
            self.assertEqual(main(["--author", "Unknown Author"]), 1)
            with self.assertRaises(SystemExit) as caught:
                main(["--output", str(self.root / "upload")])
        self.assertEqual(caught.exception.code, 2)
        self.assertIn("Prepared index for 1 author(s)", stdout.getvalue())
        self.assertIn(str(self.index_file.resolve()), stdout.getvalue())
        self.assertIn("Skipped René Researcher", stdout.getvalue())
        self.assertIn("Unknown author", stderr.getvalue())
