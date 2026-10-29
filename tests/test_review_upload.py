"""The optional coordinator helper preserves names and prepares read-only inputs."""

from contextlib import redirect_stderr, redirect_stdout
from dataclasses import asdict
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from support import AUTHOR_YAML
import config
from publication_model import Publication
from publication_review.prepare_upload import main, prepare_upload


class ReviewUploadTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.data = self.root / "data"
        self.output = self.root / "upload"
        authors = self.root / "authors.yaml"
        authors.write_text(AUTHOR_YAML, encoding="utf-8")
        for name, value in (("DATA_DIRECTORY", self.data), ("AUTHORS_FILE", authors),
                            ("NORMALIZED_DIRECTORY_FORMAT", "{author_slug}/normalized"),
                            ("NORMALIZED_FILENAME_FORMAT", "{author_slug}-publications.json")):
            patcher = patch.object(config, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def normalized(self, slug, records):
        path = self.data / slug / "normalized" / f"{slug}-publications.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")
        return path

    def test_bundle_preserves_canonical_names_unicode_order_duplicates_and_inputs(self):
        source = self.normalized("ada-researcher", [{"title": "Über work", "authors": ["René"]}, {"title": "Über work"}])
        second = self.normalized("rené-researcher", [])
        before = {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in (source, second)}
        count, skipped = prepare_upload(self.output)
        self.assertEqual((count, skipped), (2, []))
        manifest = json.loads((self.output / "authors.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest, {"version": 1, "authors": [
            {"id": "ada-researcher", "name": "Ada Researcher", "sourceFile": "ada-researcher-publications.json"},
            {"id": "rené-researcher", "name": "René Researcher", "sourceFile": "rené-researcher-publications.json"},
        ]})
        self.assertEqual(json.loads((self.output / "ada-researcher-publications.json").read_text()), [
            json.loads(json.dumps(asdict(Publication(title="Über work", authors=("René",))))),
            json.loads(json.dumps(asdict(Publication(title="Über work")))),
        ])
        self.assertEqual((self.output / "rené-researcher-publications.json").read_text(), "[]\n")
        self.assertEqual({path: (path.read_bytes(), path.stat().st_mtime_ns) for path in before}, before)

    def test_missing_author_inputs_are_skipped(self):
        self.normalized("ada-researcher", [])
        self.assertEqual(prepare_upload(self.output), (1, ["René Researcher"]))

    def test_missing_all_inputs_leaves_output_absent(self):
        with self.assertRaisesRegex(ValueError, "No normalized"):
            prepare_upload(self.output)
        self.assertFalse(self.output.exists())

    def test_invalid_input_does_not_create_a_partial_bundle(self):
        self.normalized("ada-researcher", [{"title": "Valid"}])
        self.normalized("rené-researcher", [{"year": 2026}])
        with self.assertRaisesRegex(ValueError, "year"):
            prepare_upload(self.output)
        self.assertFalse(self.output.exists())

    def test_existing_output_is_never_overwritten(self):
        self.output.mkdir()
        marker = self.output / "existing.txt"
        marker.write_text("Preserve me")
        with self.assertRaisesRegex(ValueError, "already exists"):
            prepare_upload(self.output)
        self.assertEqual(marker.read_text(), "Preserve me")

    def test_selection_is_case_insensitive_and_limits_the_bundle(self):
        self.normalized("ada-researcher", [])
        self.normalized("rené-researcher", [])
        count, skipped = prepare_upload(self.output, ("RENÉ RESEARCHER",))
        self.assertEqual((count, skipped), (1, []))
        manifest = json.loads((self.output / "authors.json").read_text())
        self.assertEqual([item["name"] for item in manifest["authors"]], ["René Researcher"])

    def test_cli_reports_success_failure_and_usage_errors(self):
        self.normalized("ada-researcher", [])
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            self.assertEqual(main(["--output", str(self.output)]), 0)
            self.assertEqual(main(["--output", str(self.output)]), 1)
            with self.assertRaises(SystemExit) as caught:
                main(["--author", "Ada Researcher"])
        self.assertEqual(caught.exception.code, 2)
        self.assertIn("Prepared 1 author(s)", stdout.getvalue())
        self.assertIn("already exists", stderr.getvalue())
