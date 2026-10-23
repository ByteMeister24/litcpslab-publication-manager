"""Publisher-independent workflow and failure contracts."""

import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from support import PROJECT_ROOT
import config
from author_builder import Author
from models import DownloadError, DownloadRecord, Publication
from source_downloaders.common import download_source


class SharedDownloadTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.author = Author("René Researcher", ("University A",))
        for context in (
            patch.object(config, "DATA_DIRECTORY", self.root / "data"),
            patch.object(config, "ENV_FILE", self.root / ".env"),
            patch.dict(os.environ, {
                config.CREDENTIAL_MODE_VARIABLE: "environment", "EXAMPLE_API_KEY": "run-only-key"
            }, clear=True),
        ):
            context.start()
            self.addCleanup(context.stop)

    def test_arbitrary_native_pages_are_saved_unchanged_before_source_normalization(self):
        pages = [
            {"items": [{"heading": "First"}], "next": "cursor-two"},
            {"items": [{"heading": "Second"}], "next": None},
        ]
        query = Mock(return_value="source-specific query")
        retrieve = Mock(return_value=pages)

        def normalize(native_pages):
            raw_files = list((self.root / "data").glob("*/raw/*.json"))
            self.assertEqual(len(raw_files), 1)
            self.assertEqual(json.loads(raw_files[0].read_text(encoding="utf-8")), pages)
            return [Publication(title=item["heading"]) for page in native_pages for item in page["items"]]

        result = download_source(
            self.author, source="example", source_name="Example", api_key_name="EXAMPLE_API_KEY",
            build_query=query, download_pages=retrieve, normalize_pages=normalize,
        )
        self.assertIsInstance(result, DownloadRecord)
        self.assertEqual((result.author, result.source, result.publication_count), (self.author.name, "example", 2))
        self.assertEqual(result.publications, [Publication(title="First"), Publication(title="Second")])
        query.assert_called_once_with(self.author)
        retrieve.assert_called_once_with("source-specific query", "run-only-key")
        self.assertFalse((self.root / ".env").exists())
        self.assertNotIn("run-only-key", result.raw_file_path.read_text(encoding="utf-8"))

    def test_stage_failures_are_redacted_and_short_circuit_later_work(self):
        for failure, stage in (("query", "Download"), ("retrieve", "Download"),
                               ("save", "Raw saving"), ("normalize", "Normalization")):
            with self.subTest(failure=failure):
                query = Mock(return_value="query")
                retrieve = Mock(return_value=[{"items": []}])
                save = Mock(return_value=self.root / "retained.json")
                normalize = Mock(return_value=[])
                callbacks = {"query": query, "retrieve": retrieve, "save": save, "normalize": normalize}
                callbacks[failure].side_effect = RuntimeError("failure containing run-only-key")
                with patch("source_downloaders.common.storage.save_raw", save):
                    result = download_source(
                        self.author, source="example", source_name="Example", api_key_name="EXAMPLE_API_KEY",
                        build_query=query, download_pages=retrieve, normalize_pages=normalize,
                    )
                self.assertIsInstance(result, DownloadError)
                self.assertEqual((result.author, result.source), (self.author.name, "example"))
                self.assertTrue(result.error.startswith(f"{stage} failed:"))
                self.assertNotIn("run-only-key", result.error)
                self.assertIn("[REDACTED]", result.error)
                if failure == "normalize":
                    self.assertIn(f"raw saved: {self.root / 'retained.json'}", result.error)
                else:
                    self.assertNotIn("raw saved:", result.error)
                    normalize.assert_not_called()
                if failure in ("query", "retrieve"):
                    save.assert_not_called()
                if failure == "query":
                    retrieve.assert_not_called()
