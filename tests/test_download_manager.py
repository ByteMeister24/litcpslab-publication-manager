"""Offline author/source coordination, raw storage, and failure handling."""

from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timedelta
import io
from itertools import count
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from typing import cast
import unittest
from unittest.mock import Mock, call, patch
from zoneinfo import ZoneInfo

from support import AUTHOR_YAML, PROJECT_ROOT, full_article, page
import config
from helpers.author_builder import Author
from helpers.selection import Selection
from publication_collector.cli.download_publications import main
from publication_collector.download_manager import run_download
from publication_collector.download_models import DownloadConfirmation, DownloadError, DownloadRequest


class DownloadManagerTests(unittest.TestCase):
    def setUp(self):
        sources = patch("publication_collector.download_manager.SUPPORTED_SOURCES", ("ieee",))
        sources.start()
        self.addCleanup(sources.stop)
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.data = self.root / "data"
        self.data.mkdir()
        clock = patch("publication_collector.source_downloaders.common.datetime")
        start = datetime(2026, 10, 22, 14, 30, tzinfo=ZoneInfo(config.DOWNLOAD_TIMEZONE))
        clock.start().now.side_effect = (start + timedelta(microseconds=step) for step in count())
        self.addCleanup(clock.stop)
        network_guard = patch("publication_collector.source_downloaders.ieee_xplore.urlopen", side_effect=AssertionError("Unexpected network access in offline tests"))
        network_guard.start()
        self.addCleanup(network_guard.stop)
        authors_file = self.data / "authors.yaml"
        authors_file.write_text(AUTHOR_YAML, encoding="utf-8")
        env_file = self.root / ".env"
        env_file.write_text("IEEE_API_KEY=synthetic-key\n", encoding="utf-8")
        for name, value in [("DATA_DIRECTORY", self.data), ("AUTHORS_FILE", authors_file), ("ENV_FILE", env_file)]:
            patcher = patch.object(config, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def markdown_path(self, slug="ada-researcher"):
        return self.data / slug / f"{slug}-ieee-2026-10-22.md"

    def downloads(self, slug="ada-researcher"):
        return sorted((self.data / slug / "download" / "ieee").glob("*.json"))

    def run_offline(self, request, responses):
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch("publication_collector.source_downloaders.ieee_xplore._fetch_page", side_effect=responses) as fetch, \
             redirect_stdout(stdout), redirect_stderr(stderr):
            results = run_download(request)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "")
        return results, fetch

    def test_complete_flow_saves_raw_without_building_markdown(self):
        native = {"total_records": 1, "articles": [full_article()]}
        with patch("publication_markdown.markdown_builder.build_markdown") as builder:
            downloads, fetch = self.run_offline(DownloadRequest(("Ada Researcher",), ("ieee",)), [native])
        self.assertEqual(len(downloads), 1)
        download = downloads[0]
        assert isinstance(download, DownloadConfirmation)
        self.assertEqual(download.publication_count, 1)
        self.assertEqual(json.loads(download.raw_file_path.read_text()), [native])
        self.assertFalse(self.markdown_path().exists())
        builder.assert_not_called()
        fetch.assert_called_once()

    @patch("publication_collector.source_downloaders.ieee_xplore._fetch_page", return_value=page(1, [1]))
    def test_cli_accepts_lowercase_and_mixed_case_authors_and_uses_database_names(self, fetch):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            status = main(["--author", "ada researcher, ADA RESEARCHER, rENÉ rESEARCHER", "--source", "ieee"])
        self.assertEqual(status, 0)
        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(fetch.call_count, 2)
        queries = [request.args[1] for request in fetch.call_args_list]
        self.assertIn('"Authors":"Ada Researcher"', queries[0])
        self.assertIn('"Authors":"René Researcher"', queries[1])
        self.assertIn("Download completed: Ada Researcher [ieee]", stdout.getvalue())
        self.assertIn("Download completed: René Researcher [ieee]", stdout.getvalue())
        self.assertIn("Download report: 2 succeeded; 0 failed.", stdout.getvalue())

    def test_manager_delegates_selected_authors_and_returns_download_outcomes_without_writes(self):
        author = Author("Ada Researcher", ("University A",))
        response = DownloadConfirmation(author.name, "ieee", 1, Path("source-owned.json"))
        download = Mock(return_value=response)
        with patch("publication_collector.download_manager.get_selected_authors", return_value=[author]) as reader, \
             patch.dict("publication_collector.download_manager.DOWNLOADERS", {"ieee": download}), \
             patch("utils.storage.save_file") as raw_save, patch("utils.storage.save_final_markdown") as markdown_save:
            results = run_download(DownloadRequest((author.name,), ("ieee",)))
        reader.assert_called_once_with((author.name,))
        download.assert_called_once_with(author)
        raw_save.assert_not_called()
        markdown_save.assert_not_called()
        self.assertEqual(results, [response])
        self.assertIs(results[0], response)

    def test_manager_returns_source_error_unchanged_without_calling_builder(self):
        author = Author("Ada Researcher", ("University A",))
        error = DownloadError(author.name, "ieee", "Download failed: unavailable")
        with patch("publication_collector.download_manager.get_selected_authors", return_value=[author]), \
             patch.dict("publication_collector.download_manager.DOWNLOADERS", {"ieee": Mock(return_value=error)}), \
             patch("publication_markdown.markdown_builder.build_markdown") as builder:
            results = run_download(DownloadRequest("all", "all"))
        builder.assert_not_called()
        self.assertEqual(results, [error])
        self.assertIs(results[0], error)

    def test_returned_download_error_skips_markdown_and_continues(self):
        error = DownloadError("Ada Researcher", "ieee", "Download failed: disk error")
        record = DownloadConfirmation("René Researcher", "ieee", 1, Path("second.json"))
        download = Mock(side_effect=[error, record])
        with patch.dict("publication_collector.download_manager.DOWNLOADERS", {"ieee": download}), \
             patch("publication_markdown.markdown_builder.build_markdown") as builder:
            downloads = run_download(DownloadRequest("all", "all"))
        self.assertEqual(downloads, [error, record])
        self.assertEqual(download.call_count, 2)
        builder.assert_not_called()

    def test_all_authors_does_not_override_source_validation(self):
        download = Mock()
        with patch.dict("publication_collector.download_manager.DOWNLOADERS", {"ieee": download}), self.assertRaises(ValueError):
            run_download(DownloadRequest("all", ("unknown",)))
        download.assert_not_called()

    def test_unknown_author_or_source_fails_before_any_request(self):
        requests = [DownloadRequest(("Ada Researcher", "Unknown"), "all"),
                    DownloadRequest(("Ada Researcher",), ("ieee", "unknown")),
                    DownloadRequest((), "all"), DownloadRequest(cast(Selection, "invalid"), "all")]
        for request in requests:
            download = Mock()
            with self.subTest(request=request), patch.dict("publication_collector.download_manager.DOWNLOADERS", {"ieee": download}):
                with self.assertRaises(ValueError):
                    run_download(request)
                download.assert_not_called()
        self.assertEqual(list(self.data.iterdir()), [self.data / "authors.yaml"])

    def test_entire_yaml_file_is_validated_before_any_download(self):
        config.AUTHORS_FILE.write_text(AUTHOR_YAML + "\nOther Researcher: []\n", encoding="utf-8")
        download = Mock()
        with patch.dict("publication_collector.download_manager.DOWNLOADERS", {"ieee": download}), self.assertRaises(ValueError):
            run_download(DownloadRequest(("Ada Researcher",), "all"))
        download.assert_not_called()

    def test_invalid_yaml_is_reported_by_cli_without_requests_or_traceback(self):
        config.AUTHORS_FILE.write_text("Ada Researcher: [unfinished\n", encoding="utf-8")
        stderr = io.StringIO()
        with patch("publication_collector.source_downloaders.ieee_xplore._fetch_page") as fetch, redirect_stderr(stderr):
            status = main(["all"])
        self.assertEqual(status, 1)
        self.assertIn(str(config.AUTHORS_FILE), stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())
        fetch.assert_not_called()

    def test_all_request_processes_master_order_and_source_calls_receive_authors(self):
        download = Mock(side_effect=lambda author: DownloadConfirmation(author.name, "ieee", 0, Path("raw.json")))
        with patch.dict("publication_collector.download_manager.DOWNLOADERS", {"ieee": download}), \
             patch("publication_markdown.markdown_builder.build_markdown") as builder:
            downloads = run_download(DownloadRequest(authors="all", sources="all"))
        self.assertEqual(download.call_args_list, [
            call(Author("Ada Researcher", ("University A", "Institute B"))),
            call(Author("René Researcher", ("University A", "Institute B", "Former University"))),
        ])
        self.assertEqual([result.author for result in downloads], ["Ada Researcher", "René Researcher"])
        builder.assert_not_called()

    def test_middleware_rejects_bare_all_before_loading_authors(self):
        with patch("publication_collector.download_manager.get_selected_authors") as load:
            with self.assertRaisesRegex(ValueError, "Expected DownloadRequest"):
                run_download(cast(DownloadRequest, "all"))
        load.assert_not_called()

    def test_explicit_author_order_and_duplicates(self):
        downloads, fetch = self.run_offline(
            DownloadRequest(("René Researcher", "Ada Researcher", "René Researcher"), "all"),
            [page(1, [1]), page(1, [2])],
        )
        self.assertEqual([result.author for result in downloads], ["René Researcher", "Ada Researcher"])
        self.assertEqual(fetch.call_count, 2)

    def test_zero_results_preserve_previous_outputs(self):
        self.run_offline(DownloadRequest(("Ada Researcher",), "all"), [page(1, [1])])
        old_raw = self.downloads()[0]
        original = old_raw.read_bytes()
        self.markdown_path().write_text("Previous Markdown", encoding="utf-8")
        old_markdown = self.markdown_path().read_bytes()
        downloads, _ = self.run_offline(DownloadRequest(("Ada Researcher",), "all"), [page(0, [])])
        assert isinstance(downloads[0], DownloadConfirmation)
        self.assertEqual(downloads[0].publication_count, 0)
        self.assertEqual(json.loads(downloads[0].raw_file_path.read_text()), [page(0, [])])
        self.assertEqual(self.markdown_path().read_bytes(), old_markdown)
        self.assertEqual(old_raw.read_bytes(), original)
        self.assertEqual(len(self.downloads()), 2)

    def test_zero_results_save_raw_without_creating_markdown(self):
        downloads, _ = self.run_offline(DownloadRequest(("Ada Researcher",), "all"), [page(0, [])])
        assert isinstance(downloads[0], DownloadConfirmation)
        self.assertEqual(downloads[0].publication_count, 0)
        self.assertEqual(json.loads(downloads[0].raw_file_path.read_text()), [page(0, [])])
        self.assertFalse(self.markdown_path().exists())

    def test_later_page_failure_keeps_old_outputs_and_continues_other_authors(self):
        self.run_offline(DownloadRequest(("Ada Researcher",), "all"), [page(1, [99])])
        old_raw = self.downloads()
        self.markdown_path().write_text("Previous Markdown", encoding="utf-8")
        old_markdown = self.markdown_path().read_bytes()
        downloads, fetch = self.run_offline(DownloadRequest("all", "all"),
                                            [page(2, [1]), RuntimeError("HTTP 503"), page(1, [3])])
        assert isinstance(downloads[0], DownloadError)
        self.assertIn("Download failed", downloads[0].error)
        self.assertNotIn("raw saved:", downloads[0].error)
        assert isinstance(downloads[1], DownloadConfirmation)
        self.assertTrue(downloads[1].raw_file_path.exists())
        self.assertEqual(self.downloads(), old_raw)
        self.assertEqual(self.markdown_path().read_bytes(), old_markdown)
        self.assertFalse(self.markdown_path("rené-researcher").exists())
        self.assertEqual(fetch.call_count, 3)

    def test_nonempty_downloads_preserve_previous_markdown(self):
        destination = self.markdown_path()
        destination.parent.mkdir()
        destination.write_text("Previous Markdown", encoding="utf-8")
        with patch("utils.storage.save_final_markdown") as save:
            downloads, _ = self.run_offline(DownloadRequest("all", "all"), [page(1, [1]), page(1, [2])])
        for result in downloads:
            assert isinstance(result, DownloadConfirmation)
            self.assertTrue(result.raw_file_path.exists())
        self.assertEqual(destination.read_text(), "Previous Markdown")
        self.assertFalse(self.markdown_path("rené-researcher").exists())
        save.assert_not_called()

    def test_raw_write_failure_preserves_markdown_and_other_author_still_completes(self):
        (self.data / "ada-researcher").mkdir()
        (self.data / "ada-researcher" / "download").write_text("occupied", encoding="utf-8")
        self.markdown_path().write_text("Previous Markdown", encoding="utf-8")
        downloads, _ = self.run_offline(DownloadRequest("all", "all"), [page(1, [1]), page(1, [2])])
        assert isinstance(downloads[0], DownloadError)
        self.assertIn("Raw saving failed", downloads[0].error)
        assert isinstance(downloads[1], DownloadConfirmation)
        self.assertTrue(downloads[1].raw_file_path.exists())
        self.assertEqual(self.markdown_path().read_text(), "Previous Markdown")

    def test_metadata_needing_review_is_saved_without_normalization(self):
        self.run_offline(DownloadRequest(("Ada Researcher",), "all"), [page(1, [99])])
        old_raw = self.downloads()[0]
        old_raw_content = old_raw.read_bytes()
        self.markdown_path().write_text("Previous Markdown", encoding="utf-8")
        old_markdown = self.markdown_path().read_bytes()
        bad = page(1, [1])
        bad["articles"][0]["abstract"] = []
        downloads, _ = self.run_offline(DownloadRequest("all", "all"), [bad, page(0, [])])
        assert isinstance(downloads[0], DownloadConfirmation)
        saved_raw = next(path for path in self.downloads() if path != old_raw)
        self.assertEqual(json.loads(saved_raw.read_text()), [bad])
        self.assertEqual(downloads[0].raw_file_path, saved_raw)
        self.assertEqual(old_raw.read_bytes(), old_raw_content)
        self.assertEqual(self.markdown_path().read_bytes(), old_markdown)
        self.assertEqual(len(self.downloads()), 2)
        assert isinstance(downloads[1], DownloadConfirmation)
        self.assertEqual(downloads[1].publication_count, 0)
        self.assertEqual(json.loads(downloads[1].raw_file_path.read_text()), [page(0, [])])
        self.assertFalse(self.markdown_path("rené-researcher").exists())

    def test_multiple_authors_and_sources_keep_independent_results_in_processing_order(self):
        ieee_records = [DownloadConfirmation("Ada Researcher", "ieee", 1, Path("ada-ieee.json")),
                        DownloadError("René Researcher", "ieee", "Download failed: unavailable")]
        other_records = [DownloadConfirmation("Ada Researcher", "test_source", 0, Path("ada-other.json")),
                         DownloadConfirmation("René Researcher", "test_source", 1, Path("rene-other.json"))]
        ieee = Mock(side_effect=ieee_records)
        other = Mock(side_effect=other_records)
        with patch("publication_collector.download_manager.SUPPORTED_SOURCES", ("ieee", "test_source")), \
             patch.dict("publication_collector.download_manager.DOWNLOADERS", {"ieee": ieee, "test_source": other}):
            downloads = run_download(DownloadRequest("all", "all"))
        self.assertEqual([(result.author, result.source) for result in downloads], [
            ("Ada Researcher", "ieee"), ("Ada Researcher", "test_source"),
            ("René Researcher", "ieee"), ("René Researcher", "test_source"),
        ])
        self.assertEqual(downloads, [ieee_records[0], other_records[0], ieee_records[1], other_records[1]])
        self.assertEqual(ieee.call_count, 2)
        self.assertEqual(other.call_count, 2)

    def test_run_from_another_directory_uses_project_paths_and_file_credentials(self):
        project = self.root / "copied-project"
        shutil.copytree(PROJECT_ROOT / "src", project / "src", ignore=shutil.ignore_patterns("__pycache__"))
        (project / "db").mkdir()
        (project / "db" / "authors.yaml").write_text(AUTHOR_YAML, encoding="utf-8")
        result = subprocess.run([sys.executable, "-B", "-m", "publication_collector", "--source", "ieee"],
                                cwd=self.root, capture_output=True, text=True, check=False,
                                env={**os.environ, "PYTHONPATH": str(project / "src"),
                                     "IEEE_API_KEY": "must-not-be-used"})
        self.assertEqual(result.returncode, 1)
        self.assertIn(str(project / ".env"), result.stderr)
        self.assertIn("Download report: 0 succeeded; 2 failed.", result.stdout)
        self.assertNotIn("Markdown", result.stdout)
        self.assertNotIn("Traceback", result.stderr)
        self.assertNotIn("must-not-be-used", result.stderr)
        self.assertFalse((project / "data" / "ada-researcher").exists())
