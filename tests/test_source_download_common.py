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
from models import DownloadConfirmation, DownloadError
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

    def test_arbitrary_native_pages_are_saved_unchanged_with_source_count(self):
        pages = [
            {"items": [{"heading": "First"}], "next": "cursor-two"},
            {"items": [{"heading": "Second"}], "next": None},
        ]
        query = Mock(return_value="source-specific query")
        retrieve = Mock(return_value=pages)

        count = Mock(return_value=2)

        result = download_source(
            self.author, source="example", source_name="Example", api_key_name="EXAMPLE_API_KEY",
            build_query=query, download_pages=retrieve, count_publications=count,
        )
        self.assertIsInstance(result, DownloadConfirmation)
        self.assertEqual((result.author, result.source, result.publication_count), (self.author.name, "example", 2))
        self.assertEqual(json.loads(result.raw_file_path.read_text(encoding="utf-8")), pages)
        self.assertFalse(hasattr(result, "publications"))
        query.assert_called_once_with(self.author)
        retrieve.assert_called_once_with("source-specific query", "run-only-key")
        count.assert_called_once_with(pages)
        self.assertFalse((self.root / ".env").exists())
        self.assertNotIn("run-only-key", result.raw_file_path.read_text(encoding="utf-8"))

    def test_stage_failures_are_redacted_and_short_circuit_later_work(self):
        for failure, stage in (("query", "Download"), ("retrieve", "Download"),
                               ("count", "Download"), ("save", "Raw saving")):
            with self.subTest(failure=failure):
                query = Mock(return_value="query")
                retrieve = Mock(return_value=[{"items": []}])
                save = Mock(return_value=self.root / "retained.json")
                count = Mock(return_value=0)
                callbacks = {"query": query, "retrieve": retrieve, "save": save, "count": count}
                callbacks[failure].side_effect = RuntimeError("failure containing run-only-key")
                with patch("source_downloaders.common.storage.save_raw", save):
                    result = download_source(
                        self.author, source="example", source_name="Example", api_key_name="EXAMPLE_API_KEY",
                        build_query=query, download_pages=retrieve, count_publications=count,
                    )
                self.assertIsInstance(result, DownloadError)
                self.assertEqual((result.author, result.source), (self.author.name, "example"))
                self.assertTrue(result.error.startswith(f"{stage} failed:"))
                self.assertNotIn("run-only-key", result.error)
                self.assertIn("[REDACTED]", result.error)
                self.assertNotIn("raw saved:", result.error)
                if failure in ("query", "retrieve", "count"):
                    save.assert_not_called()
                if failure in ("query", "retrieve"):
                    count.assert_not_called()
                if failure == "query":
                    retrieve.assert_not_called()
