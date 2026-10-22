"""Offline CLI and middleware behavior, with source HTTP mocked."""

from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime
import io
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
from download_publications import main, parse_request
from author_builder import Author
from models import DownloadError, DownloadRequest, MarkdownBuildResult, Publication, Selection, DownloadRecord
from download_manager import run_download


class CLITests(unittest.TestCase):
    def setUp(self):
        report = patch("download_publications.update_report", return_value=None)
        self.report = report.start()
        self.addCleanup(report.stop)
        counts = patch("download_publications.update_download_counts", return_value=[])
        self.counts = counts.start()
        self.addCleanup(counts.stop)

    def test_bare_all_is_normalized_into_a_download_request(self):
        self.assertEqual(parse_request(["all"]), DownloadRequest(authors="all", sources="all"))

    def test_comma_lists_are_trimmed_deduplicated_and_sources_lowercased(self):
        request = parse_request(["--author", " Ada Researcher, René Researcher, Ada Researcher ",
                                 "--source", " IEEE, sciencedirect, ieee "])
        self.assertEqual(request, DownloadRequest(("Ada Researcher", "René Researcher"),
                                                  ("ieee", "sciencedirect")))

    def test_independent_all_and_omitted_flags(self):
        cases = [
            (["--author", "Ada Researcher"], DownloadRequest(("Ada Researcher",), "all")),
            (["--source", "ieee"], DownloadRequest("all", ("ieee",))),
            (["--author", "all", "--source", "ieee"], DownloadRequest("all", ("ieee",))),
            (["--author", "Ada Researcher", "--source", "all"], DownloadRequest(("Ada Researcher",), "all")),
            (["--author", "all", "--source", "all"], DownloadRequest("all", "all")),
            (["--author", "all, all"], DownloadRequest("all", "all")),
        ]
        for args, expected in cases:
            with self.subTest(args=args):
                self.assertEqual(parse_request(args), expected)

    def test_invalid_arguments_exit_with_usage_code_two(self):
        cases = [[], ["Ada Researcher"], ["all", "--author", "all"], ["all", "--source", "ieee"],
                 ["--author", "Ada Researcher", "all"], ["--author", ""], ["--author", "A,,B"],
                 ["--author", "all,A"], ["--source", "all,ieee"], ["--source", "ieee,"],
                 ["--author"], ["--author", "--source"], ["Ada Researcher", "ieee"], ["--source", " "], ["--unknown", "ieee"]]
        for args in cases:
            with self.subTest(args=args), redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as caught:
                    parse_request(args)
                self.assertEqual(caught.exception.code, 2)

    def test_help_succeeds_without_running_middleware(self):
        with patch("download_publications.run_download") as run, redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as caught:
                main(["--help"])
        self.assertEqual(caught.exception.code, 0)
        run.assert_not_called()

    @patch("download_publications.run_download")
    def test_cli_only_passes_request_and_reports_returned_results(self, run):
        run.return_value = (
            [DownloadRecord("Ada Researcher", "ieee", 2, [Publication(), Publication()], Path("raw.json")),
             DownloadError("René Researcher", "ieee", "Download failed: HTTP 503")],
            [MarkdownBuildResult("Ada Researcher", "ieee", Path("output.md"))],
        )
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            status = main(["--author", "Ada Researcher, René Researcher", "--source", "ieee"])
        self.assertEqual(status, 1)
        run.assert_called_once_with(DownloadRequest(("Ada Researcher", "René Researcher"), ("ieee",)))
        self.assertIn("2 publication(s)", stdout.getvalue())
        self.assertIn("Download report: 1 succeeded; 1 failed.", stdout.getvalue())
        self.assertIn("Markdown report: 1 succeeded; 0 failed; 1 skipped.", stdout.getvalue())
        self.assertIn("Markdown completed: Ada Researcher [ieee]: output.md", stdout.getvalue())
        self.assertIn("Download failed: René Researcher [ieee]", stderr.getvalue())

    @patch("download_publications.run_download")
    def test_bare_all_reaches_middleware_as_a_download_request(self, run):
        run.return_value = ([], [])
        with redirect_stdout(io.StringIO()):
            self.assertEqual(main(["all"]), 0)
        run.assert_called_once_with(DownloadRequest(authors="all", sources="all"))

    @patch("download_publications.run_download")
    def test_markdown_failure_does_not_mark_download_as_failed(self, run):
        run.return_value = (
            [DownloadRecord("Ada Researcher", "ieee", 1, [Publication()], Path("retained.json"))],
            [MarkdownBuildResult("Ada Researcher", "ieee", error="Markdown saving failed: disk error")],
        )
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            status = main(["all"])
        self.assertEqual(status, 1)
        self.assertIn("Download completed: Ada Researcher [ieee]", stdout.getvalue())
        self.assertIn("raw: retained.json", stdout.getvalue())
        self.assertIn("Download report: 1 succeeded; 0 failed.", stdout.getvalue())
        self.assertIn("Markdown report: 0 succeeded; 1 failed; 0 skipped.", stdout.getvalue())
        self.assertIn("Markdown failed: Ada Researcher [ieee]", stderr.getvalue())
        self.assertIn("Markdown saving failed", stderr.getvalue())
        self.assertNotIn("Download failed:", stderr.getvalue())

    @patch("download_publications.run_download")
    def test_failed_download_reports_retained_raw_and_skipped_markdown(self, run):
        run.return_value = (
            [DownloadError("Ada Researcher", "ieee", "Normalization failed: invalid metadata; raw saved: retained.json")],
            [],
        )
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            status = main(["all"])
        self.assertEqual(status, 1)
        self.assertIn("raw saved: retained.json", stderr.getvalue())
        self.assertIn("Download report: 0 succeeded; 1 failed.", stdout.getvalue())
        self.assertIn("Markdown report: 0 succeeded; 0 failed; 1 skipped.", stdout.getvalue())
        self.assertNotIn("Markdown failed:", stderr.getvalue())

    @patch("download_publications.run_download")
    def test_success_and_request_failure_exit_codes(self, run):
        run.return_value = (
            [DownloadRecord("Ada Researcher", "ieee", 0, [], Path("raw"))],
            [],
        )
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            self.assertEqual(main(["all"]), 0)
        self.assertIn("0 publication(s)", stdout.getvalue())
        self.assertIn("Download report: 1 succeeded; 0 failed.", stdout.getvalue())
        self.assertIn("Markdown report: 0 succeeded; 0 failed; 1 skipped.", stdout.getvalue())
        run.side_effect = ValueError("Unknown author")
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            self.assertEqual(main(["all"]), 1)
        self.assertIn("Unknown author", stderr.getvalue())

    @patch("download_publications.run_download")
    def test_json_then_html_updates_use_successful_counts_after_markdown_reports(self, run):
        run.return_value = (
            [DownloadRecord("Ada Researcher", "ieee", 0, [], Path("ada.json")),
             DownloadError("Other Researcher", "ieee", "Download failed"),
             DownloadRecord("René Researcher", "ieee", 17, [], Path("rene.json"))],
            [MarkdownBuildResult("René Researcher", "ieee", Path("rene.md"))],
        )
        stdout, stderr = io.StringIO(), io.StringIO()

        def counts_after_summary(counts):
            self.assertIn("Markdown report: 1 succeeded; 0 failed; 2 skipped.", stdout.getvalue())
            self.report.assert_not_called()
            return ["Count decreased"]

        def html_after_counts():
            self.counts.assert_called_once_with({"Ada Researcher": {"ieee": 0}, "René Researcher": {"ieee": 17}})
            self.assertIn("Warning: Count decreased", stderr.getvalue())

        self.counts.side_effect = counts_after_summary
        self.report.side_effect = html_after_counts
        with redirect_stdout(stdout), redirect_stderr(stderr):
            status = main(["all"])
        self.assertEqual(status, 1)
        self.report.assert_called_once_with()
        self.assertIn("Warning: Count decreased", stderr.getvalue())
        self.assertIn("Download report: 2 succeeded; 1 failed.", stdout.getvalue())

    @patch("download_publications.run_download")
    def test_failed_only_execution_still_updates_report_timestamp(self, run):
        run.return_value = ([DownloadError("Ada Researcher", "ieee", "Unavailable")], [])
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(main(["all"]), 1)
        self.counts.assert_called_once_with({})
        self.report.assert_called_once_with()

    @patch("download_publications.run_download")
    def test_json_update_failure_skips_html_and_preserves_exit_code(self, run):
        run.return_value = ([DownloadRecord("Ada Researcher", "ieee", 0, [], Path("raw.json"))], [])
        self.counts.side_effect = ValueError("invalid JSON")
        stderr = io.StringIO()
        with redirect_stdout(io.StringIO()), redirect_stderr(stderr):
            self.assertEqual(main(["all"]), 0)
        self.report.assert_not_called()
        self.assertIn("Report update failed: invalid JSON", stderr.getvalue())

    @patch("download_publications.run_download")
    def test_report_errors_are_printed_without_changing_existing_exit_codes(self, run):
        for error, extra_downloads, expected_status in [
            (OSError("cannot save HTML"), [], 0),
            (ValueError("invalid HTML"), [DownloadError("Other Researcher", "ieee", "Download failed")], 1),
        ]:
            with self.subTest(error=error):
                run.return_value = ([DownloadRecord("Ada Researcher", "ieee", 0, [], Path("raw.json"))]
                                    + extra_downloads, [])
                self.report.side_effect = error
                stdout, stderr = io.StringIO(), io.StringIO()
                with redirect_stdout(stdout), redirect_stderr(stderr):
                    status = main(["all"])
                self.assertEqual(status, expected_status)
                self.assertIn(f"Report update failed: {error}", stderr.getvalue())


class DownloadManagerTests(unittest.TestCase):
    def setUp(self):
        sources = patch("download_manager.SUPPORTED_SOURCES", ("ieee",))
        sources.start()
        self.addCleanup(sources.stop)
        report = patch("download_publications.update_report", return_value=None)
        report.start()
        self.addCleanup(report.stop)
        counts = patch("download_publications.update_download_counts", return_value=[])
        counts.start()
        self.addCleanup(counts.stop)
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.data = self.root / "data"
        self.data.mkdir()
        clock = patch("utils.storage.datetime")
        clock.start().now.return_value = datetime(2026, 10, 22, 14, 30, tzinfo=ZoneInfo(config.DOWNLOAD_TIMEZONE))
        self.addCleanup(clock.stop)
        network_guard = patch("ieee_xplore.urlopen", side_effect=AssertionError("Unexpected network access in offline tests"))
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
        return sorted((self.data / slug / "raw").glob("*.json"))

    def run_offline(self, request, responses):
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch("ieee_xplore.fetch_page", side_effect=responses) as fetch, \
             redirect_stdout(stdout), redirect_stderr(stderr):
            results = run_download(request)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "")
        return results, fetch

    def test_complete_flow_saves_raw_and_markdown(self):
        native = {"total_records": 1, "articles": [full_article()]}
        (downloads, markdowns), fetch = self.run_offline(DownloadRequest(("Ada Researcher",), ("ieee",)), [native])
        self.assertEqual(len(downloads), 1)
        self.assertEqual(len(markdowns), 1)
        download, build = downloads[0], markdowns[0]
        assert isinstance(download, DownloadRecord)
        self.assertIsNone(build.error)
        self.assertEqual(download.publication_count, 1)
        self.assertEqual((build.author, build.source), (download.author, download.source))
        assert build.markdown_path is not None
        self.assertEqual(json.loads(download.raw_file_path.read_text()), [native])
        markdown = build.markdown_path.read_text(encoding="utf-8")
        self.assertIn("## Über Research Across Systems", markdown)
        self.assertIn("Authors: First Author; Second Author", markdown)
        self.assertIn("Keywords: Author keyword; Second keyword; IEEE term", markdown)
        fetch.assert_called_once()

    @patch("ieee_xplore.fetch_page", return_value=page(1, [1]))
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

    def test_manager_delegates_selected_authors_downloads_and_builds_without_writes(self):
        author = Author("Ada Researcher", ("University A",))
        publications = [Publication(title="A work")]
        response = DownloadRecord(author.name, "ieee", 1, publications, Path("source-owned.json"))
        build = MarkdownBuildResult(author.name, "ieee", Path("builder-owned.md"))
        download = Mock(return_value=response)
        with patch("download_manager.get_selected_authors", return_value=[author]) as reader, \
             patch.dict("download_manager.DOWNLOADERS", {"ieee": download}), \
             patch("download_manager.build_markdown", return_value=build) as builder, \
             patch("utils.storage.save_raw") as raw_save, patch("utils.storage.save_markdown") as markdown_save:
            results = run_download(DownloadRequest((author.name,), ("ieee",)))
        reader.assert_called_once_with((author.name,))
        download.assert_called_once_with(author)
        builder.assert_called_once_with(author, "ieee", publications)
        raw_save.assert_not_called()
        markdown_save.assert_not_called()
        self.assertEqual(results, ([response], [build]))
        self.assertIs(results[0][0], response)

    def test_manager_returns_builder_error_and_continues_with_next_pair(self):
        authors = [Author("Ada Researcher", ("University A",)), Author("René Researcher", ("Institute B",))]
        records = [DownloadRecord(authors[0].name, "ieee", 1, [Publication()], Path("first.json")),
                   DownloadRecord(authors[1].name, "ieee", 1, [Publication()], Path("second.json"))]
        builds = [MarkdownBuildResult(authors[0].name, "ieee", error="Markdown saving failed: disk error"),
                  MarkdownBuildResult(authors[1].name, "ieee", Path("second.md"))]
        download = Mock(side_effect=records)
        with patch("download_manager.get_selected_authors", return_value=authors), \
             patch.dict("download_manager.DOWNLOADERS", {"ieee": download}), \
             patch("download_manager.build_markdown", side_effect=builds) as builder:
            downloads, markdowns = run_download(DownloadRequest("all", "all"))
        self.assertEqual(download.call_count, 2)
        self.assertEqual(builder.call_count, 2)
        self.assertEqual(downloads, records)
        self.assertEqual(markdowns, builds)

    def test_manager_returns_source_error_unchanged_without_calling_builder(self):
        author = Author("Ada Researcher", ("University A",))
        error = DownloadError(author.name, "ieee", "Normalization failed: invalid metadata; raw saved: retained.json")
        with patch("download_manager.get_selected_authors", return_value=[author]), \
             patch.dict("download_manager.DOWNLOADERS", {"ieee": Mock(return_value=error)}), \
             patch("download_manager.build_markdown") as builder:
            results = run_download(DownloadRequest("all", "all"))
        builder.assert_not_called()
        self.assertEqual(results, ([error], []))
        self.assertIs(results[0][0], error)

    def test_returned_download_error_skips_markdown_and_continues(self):
        error = DownloadError("Ada Researcher", "ieee", "Download failed: disk error")
        record = DownloadRecord("René Researcher", "ieee", 1, [Publication()], Path("second.json"))
        download = Mock(side_effect=[error, record])
        build = MarkdownBuildResult("René Researcher", "ieee", Path("second.md"))
        with patch.dict("download_manager.DOWNLOADERS", {"ieee": download}), \
             patch("download_manager.build_markdown", return_value=build) as builder:
            downloads, markdowns = run_download(DownloadRequest("all", "all"))
        self.assertEqual(downloads, [error, record])
        self.assertEqual(markdowns, [build])
        builder.assert_called_once_with(Author("René Researcher", ("University A", "Institute B", "Former University")),
                                        "ieee", record.publications)

    def test_all_authors_does_not_override_source_validation(self):
        download = Mock()
        with patch.dict("download_manager.DOWNLOADERS", {"ieee": download}), self.assertRaises(ValueError):
            run_download(DownloadRequest("all", ("unknown",)))
        download.assert_not_called()

    def test_unknown_author_or_source_fails_before_any_request(self):
        requests = [DownloadRequest(("Ada Researcher", "Unknown"), "all"),
                    DownloadRequest(("Ada Researcher",), ("ieee", "unknown")),
                    DownloadRequest((), "all"), DownloadRequest(cast(Selection, "invalid"), "all")]
        for request in requests:
            download = Mock()
            with self.subTest(request=request), patch.dict("download_manager.DOWNLOADERS", {"ieee": download}):
                with self.assertRaises(ValueError):
                    run_download(request)
                download.assert_not_called()
        self.assertEqual(list(self.data.iterdir()), [self.data / "authors.yaml"])

    def test_entire_yaml_file_is_validated_before_any_download(self):
        config.AUTHORS_FILE.write_text(AUTHOR_YAML + "\nOther Researcher: []\n", encoding="utf-8")
        download = Mock()
        with patch.dict("download_manager.DOWNLOADERS", {"ieee": download}), self.assertRaises(ValueError):
            run_download(DownloadRequest(("Ada Researcher",), "all"))
        download.assert_not_called()

    def test_invalid_yaml_is_reported_by_cli_without_requests_or_traceback(self):
        config.AUTHORS_FILE.write_text("Ada Researcher: [unfinished\n", encoding="utf-8")
        stderr = io.StringIO()
        with patch("ieee_xplore.fetch_page") as fetch, redirect_stderr(stderr):
            status = main(["all"])
        self.assertEqual(status, 1)
        self.assertIn(str(config.AUTHORS_FILE), stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())
        fetch.assert_not_called()

    def test_all_request_processes_master_order_and_source_calls_receive_authors(self):
        download = Mock(side_effect=lambda author: DownloadRecord(author.name, "ieee", 0, [], Path("raw.json")))
        with patch.dict("download_manager.DOWNLOADERS", {"ieee": download}), \
             patch("download_manager.build_markdown") as builder:
            downloads, markdowns = run_download(DownloadRequest(authors="all", sources="all"))
        self.assertEqual(download.call_args_list, [
            call(Author("Ada Researcher", ("University A", "Institute B"))),
            call(Author("René Researcher", ("University A", "Institute B", "Former University"))),
        ])
        self.assertEqual([result.author for result in downloads], ["Ada Researcher", "René Researcher"])
        self.assertEqual(markdowns, [])
        builder.assert_not_called()

    def test_middleware_rejects_bare_all_before_loading_authors(self):
        with patch("download_manager.get_selected_authors") as load:
            with self.assertRaisesRegex(ValueError, "Expected DownloadRequest"):
                run_download(cast(DownloadRequest, "all"))
        load.assert_not_called()

    def test_explicit_author_order_and_duplicates(self):
        (downloads, markdowns), fetch = self.run_offline(
            DownloadRequest(("René Researcher", "Ada Researcher", "René Researcher"), "all"),
            [page(1, [1]), page(1, [2])],
        )
        self.assertEqual([result.author for result in downloads], ["René Researcher", "Ada Researcher"])
        self.assertEqual([result.author for result in markdowns], ["René Researcher", "Ada Researcher"])
        self.assertEqual(fetch.call_count, 2)

    def test_zero_results_skip_markdown_and_preserve_previous_outputs(self):
        self.run_offline(DownloadRequest(("Ada Researcher",), "all"), [page(1, [1])])
        old_raw = self.downloads()[0]
        original = old_raw.read_bytes()
        old_markdown = self.markdown_path().read_bytes()
        with patch("download_manager.build_markdown") as builder:
            (downloads, markdowns), _ = self.run_offline(DownloadRequest(("Ada Researcher",), "all"), [page(0, [])])
        assert isinstance(downloads[0], DownloadRecord)
        self.assertEqual(downloads[0].publication_count, 0)
        self.assertEqual(downloads[0].publications, [])
        self.assertEqual(json.loads(downloads[0].raw_file_path.read_text()), [page(0, [])])
        self.assertEqual(markdowns, [])
        builder.assert_not_called()
        self.assertEqual(self.markdown_path().read_bytes(), old_markdown)
        self.assertEqual(old_raw.read_bytes(), original)
        self.assertEqual(len(self.downloads()), 2)

    def test_zero_results_save_raw_without_creating_markdown(self):
        with patch("download_manager.build_markdown") as builder:
            (downloads, markdowns), _ = self.run_offline(DownloadRequest(("Ada Researcher",), "all"), [page(0, [])])
        assert isinstance(downloads[0], DownloadRecord)
        self.assertEqual(downloads[0].publication_count, 0)
        self.assertEqual(json.loads(downloads[0].raw_file_path.read_text()), [page(0, [])])
        self.assertEqual(markdowns, [])
        self.assertFalse(self.markdown_path().exists())
        builder.assert_not_called()

    def test_later_page_failure_keeps_old_outputs_and_continues_other_authors(self):
        self.run_offline(DownloadRequest(("Ada Researcher",), "all"), [page(1, [99])])
        old_raw = self.downloads()
        old_markdown = self.markdown_path().read_bytes()
        (downloads, markdowns), fetch = self.run_offline(DownloadRequest("all", "all"),
                                                       [page(2, [1]), RuntimeError("HTTP 503"), page(1, [3])])
        assert isinstance(downloads[0], DownloadError)
        self.assertIn("Download failed", downloads[0].error)
        self.assertNotIn("raw saved:", downloads[0].error)
        self.assertIsInstance(downloads[1], DownloadRecord)
        self.assertEqual([result.author for result in markdowns], ["René Researcher"])
        self.assertEqual(self.downloads(), old_raw)
        self.assertEqual(self.markdown_path().read_bytes(), old_markdown)
        self.assertTrue(self.markdown_path("rené-researcher").exists())
        self.assertEqual(fetch.call_count, 3)

    def test_markdown_failure_retains_new_raw_and_previous_markdown(self):
        for target in ["markdown_builder._render_publications", "markdown_builder.storage.save_markdown"]:
            with self.subTest(target=target):
                destination = self.markdown_path()
                destination.parent.mkdir(exist_ok=True)
                destination.write_text("Previous Markdown", encoding="utf-8")
                with patch(target, side_effect=ValueError("Markdown failure")):
                    (downloads, markdowns), _ = self.run_offline(DownloadRequest("all", "all"),
                                                               [page(1, [1]), page(1, [2])])
                assert isinstance(downloads[0], DownloadRecord)
                assert markdowns[0].error is not None
                self.assertIn("Markdown", markdowns[0].error)
                self.assertTrue(downloads[0].raw_file_path.exists())
                self.assertIsNone(markdowns[0].markdown_path)
                self.assertEqual(len(markdowns), 2)
                self.assertEqual(destination.read_text(), "Previous Markdown")

    def test_markdown_failure_for_one_author_does_not_block_next(self):
        from markdown_builder import _render_publications
        calls = 0

        def render(publications):
            nonlocal calls
            calls += 1
            if calls == 1:
                raise ValueError("first author failed")
            return _render_publications(publications)

        with patch("markdown_builder._render_publications", side_effect=render):
            (downloads, markdowns), _ = self.run_offline(DownloadRequest("all", "all"), [page(1, [1]), page(1, [2])])
        self.assertTrue(all(isinstance(result, DownloadRecord) for result in downloads))
        self.assertIsNotNone(markdowns[0].error)
        self.assertIsNone(markdowns[1].error)
        assert markdowns[1].markdown_path is not None
        self.assertTrue(markdowns[1].markdown_path.exists())

    def test_raw_write_failure_preserves_markdown_and_other_author_still_completes(self):
        (self.data / "ada-researcher").mkdir()
        (self.data / "ada-researcher" / "raw").write_text("occupied", encoding="utf-8")
        self.markdown_path().write_text("Previous Markdown", encoding="utf-8")
        (downloads, markdowns), _ = self.run_offline(DownloadRequest("all", "all"), [page(1, [1]), page(1, [2])])
        assert isinstance(downloads[0], DownloadError)
        self.assertIn("Raw saving failed", downloads[0].error)
        self.assertIsInstance(downloads[1], DownloadRecord)
        self.assertEqual([result.author for result in markdowns], ["René Researcher"])
        self.assertEqual(self.markdown_path().read_text(), "Previous Markdown")

    def test_normalization_failure_retains_complete_raw_and_continues(self):
        self.run_offline(DownloadRequest(("Ada Researcher",), "all"), [page(1, [99])])
        old_raw = self.downloads()[0]
        old_raw_content = old_raw.read_bytes()
        old_markdown = self.markdown_path().read_bytes()
        bad = page(1, [1])
        bad["articles"][0]["abstract"] = []
        (downloads, markdowns), _ = self.run_offline(DownloadRequest("all", "all"), [bad, page(0, [])])
        assert isinstance(downloads[0], DownloadError)
        saved_raw = next(path for path in self.downloads() if path != old_raw)
        self.assertEqual(json.loads(saved_raw.read_text()), [bad])
        self.assertIn(f"raw saved: {saved_raw}", downloads[0].error)
        self.assertEqual(old_raw.read_bytes(), old_raw_content)
        self.assertEqual(self.markdown_path().read_bytes(), old_markdown)
        self.assertEqual(len(self.downloads()), 2)
        assert isinstance(downloads[1], DownloadRecord)
        self.assertEqual(downloads[1].publication_count, 0)
        self.assertEqual(json.loads(downloads[1].raw_file_path.read_text()), [page(0, [])])
        self.assertEqual(markdowns, [])
        self.assertFalse(self.markdown_path("rené-researcher").exists())

    def test_multiple_authors_and_sources_keep_independent_results_in_processing_order(self):
        ieee_records = [DownloadRecord("Ada Researcher", "ieee", 1, [Publication()], Path("ada-ieee.json")),
                        DownloadError("René Researcher", "ieee", "Download failed: unavailable")]
        other_records = [DownloadRecord("Ada Researcher", "test_source", 0, [], Path("ada-other.json")),
                         DownloadRecord("René Researcher", "test_source", 1, [Publication()], Path("rene-other.json"))]
        ieee = Mock(side_effect=ieee_records)
        other = Mock(side_effect=other_records)
        builds = [MarkdownBuildResult("Ada Researcher", "ieee", Path("ada-ieee.md")),
                  MarkdownBuildResult("René Researcher", "test_source", error="Markdown saving failed: disk error")]
        with patch("download_manager.SUPPORTED_SOURCES", ("ieee", "test_source")), \
             patch.dict("download_manager.DOWNLOADERS", {"ieee": ieee, "test_source": other}), \
             patch("download_manager.build_markdown", side_effect=builds) as builder:
            downloads, markdowns = run_download(DownloadRequest("all", "all"))
        self.assertEqual([(result.author, result.source) for result in downloads], [
            ("Ada Researcher", "ieee"), ("Ada Researcher", "test_source"),
            ("René Researcher", "ieee"), ("René Researcher", "test_source"),
        ])
        self.assertEqual(downloads, [ieee_records[0], other_records[0], ieee_records[1], other_records[1]])
        self.assertEqual(markdowns, builds)
        self.assertEqual(builder.call_args_list, [
            call(Author("Ada Researcher", ("University A", "Institute B")), "ieee", [Publication()]),
            call(Author("René Researcher", ("University A", "Institute B", "Former University")),
                 "test_source", [Publication()]),
        ])
        self.assertEqual(ieee.call_count, 2)
        self.assertEqual(other.call_count, 2)

    def test_run_from_another_directory_uses_project_paths_and_file_credentials(self):
        project = self.root / "copied-project"
        shutil.copytree(PROJECT_ROOT / "src", project / "src", ignore=shutil.ignore_patterns("__pycache__"))
        (project / "db").mkdir()
        (project / "db" / "authors.yaml").write_text(AUTHOR_YAML, encoding="utf-8")
        script = project / "src" / "download_publications.py"
        result = subprocess.run([sys.executable, "-B", str(script), "--source", "ieee"],
                                cwd=self.root, capture_output=True, text=True, check=False,
                                env={**os.environ, "IEEE_API_KEY": "must-not-be-used"})
        self.assertEqual(result.returncode, 1)
        self.assertIn(str(project / ".env"), result.stderr)
        self.assertIn("Download report: 0 succeeded; 2 failed.", result.stdout)
        self.assertIn("Markdown report: 0 succeeded; 0 failed; 2 skipped.", result.stdout)
        self.assertNotIn("Traceback", result.stderr)
        self.assertNotIn("must-not-be-used", result.stderr)
        self.assertFalse((project / "data" / "ada-researcher").exists())
