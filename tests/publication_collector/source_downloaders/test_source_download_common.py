"""Publisher-independent workflow and failure contracts."""

import json
from datetime import datetime
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
from zoneinfo import ZoneInfo

from tests.support import PROJECT_ROOT
import config
from helpers.author_builder import Author
from publication_collector.download_models import DownloadConfirmation, DownloadError
from publication_collector.source_downloaders.common import download_source


class SharedDownloadTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.author = Author("René Researcher", ("University A",))
        (self.root / ".env").write_text("EXAMPLE_API_KEY=run-only-key\n", encoding="utf-8")
        for context in (
            patch.object(config, "DATA_DIRECTORY", self.root / "data"),
            patch.object(config, "ENV_FILE", self.root / ".env"),
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
        self.assertNotIn("run-only-key", result.raw_file_path.read_text(encoding="utf-8"))

    def test_configured_filepath_and_native_json_are_passed_to_save_file(self):
        pages = [{"title": "Über research", "native": {"values": [True, None]}}]
        with patch.object(config, "DOWNLOAD_DIRECTORY_FORMAT", "{source}/archive/{author_slug}"), \
             patch.object(config, "DOWNLOAD_FILENAME_FORMAT", "{source}-{author_slug}-{timestamp}.json"), \
             patch("publication_collector.source_downloaders.common.datetime") as clock, \
             patch("publication_collector.source_downloaders.common.storage.save_file") as save:
            clock.now.return_value = datetime(2026, 10, 28, 14, 30, tzinfo=ZoneInfo(config.DOWNLOAD_TIMEZONE))
            result = download_source(
                self.author, source="example", source_name="Example", api_key_name="EXAMPLE_API_KEY",
                build_query=Mock(return_value="query"), download_pages=Mock(return_value=pages),
                count_publications=Mock(return_value=1),
            )
        assert isinstance(result, DownloadConfirmation)
        expected = (self.root / "data" / "example" / "archive" / self.author.slug
                    / "example-rené-researcher-2026-10-28T14-30-00.000000+0100.json")
        self.assertEqual(result.raw_file_path, expected)
        save.assert_called_once()
        filepath, content = save.call_args.args
        self.assertEqual(filepath, expected)
        self.assertEqual(json.loads(content), pages)
        self.assertIn("Über research", content)
        self.assertTrue(content.endswith("\n"))
        self.assertEqual(save.call_args.kwargs, {"replace": False})

    def test_identical_download_timestamps_preserve_existing_native_file(self):
        pages = [{"title": "Original native record"}]
        retrieve = Mock(return_value=pages)
        with patch("publication_collector.source_downloaders.common.datetime") as clock:
            clock.now.return_value = datetime(2026, 10, 21, 14, 30, tzinfo=ZoneInfo(config.DOWNLOAD_TIMEZONE))
            arguments = dict(
                source="example", source_name="Example", api_key_name="EXAMPLE_API_KEY",
                build_query=Mock(return_value="query"), download_pages=retrieve,
                count_publications=Mock(return_value=1),
            )
            first = download_source(self.author, **arguments)
            retrieve.return_value = [{"title": "Replacement must not be saved"}]
            second = download_source(self.author, **arguments)
        self.assertIsInstance(first, DownloadConfirmation)
        self.assertIsInstance(second, DownloadError)
        self.assertTrue(second.error.startswith("Raw saving failed:"))
        self.assertEqual(json.loads(first.raw_file_path.read_text(encoding="utf-8")), pages)
        self.assertEqual(list(first.raw_file_path.parent.iterdir()), [first.raw_file_path])

    def test_invalid_json_is_reported_before_saving(self):
        with patch("publication_collector.source_downloaders.common.storage.save_file") as save:
            result = download_source(
                self.author, source="example", source_name="Example", api_key_name="EXAMPLE_API_KEY",
                build_query=Mock(return_value="query"),
                download_pages=Mock(return_value=[{"invalid": float("nan")}]),
                count_publications=Mock(return_value=0),
            )
        assert isinstance(result, DownloadError)
        self.assertTrue(result.error.startswith("Raw saving failed:"))
        self.assertNotIn("raw saved:", result.error)
        save.assert_not_called()

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
                with patch("publication_collector.source_downloaders.common.storage.save_file", save):
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
