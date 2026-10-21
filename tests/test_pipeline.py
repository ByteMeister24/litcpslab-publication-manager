"""Offline CLI and middleware behavior, with source HTTP mocked."""

from contextlib import redirect_stderr, redirect_stdout
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import call, patch

from support import AUTHOR_TEXT, PROJECT_ROOT, full_article, page
import config
from main import main, parse_request
from models import Author, DownloadError, DownloadRequest, DownloadResult, MarkdownBuildResult, Publication, SourceDownload
from download_manager import run_download


class CLITests(unittest.TestCase):
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
        with patch("main.run_download") as run, redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as caught:
                main(["--help"])
        self.assertEqual(caught.exception.code, 0)
        run.assert_not_called()

    @patch("main.run_download")
    def test_cli_only_passes_request_and_reports_returned_results(self, run):
        run.return_value = [DownloadResult("Ada Researcher", "ieee", 2, Path("raw.json"), Path("output.md")),
                            DownloadResult("René Researcher", "ieee", error="Download failed: HTTP 503")]
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            status = main(["--author", "Ada Researcher, René Researcher", "--source", "ieee"])
        self.assertEqual(status, 1)
        run.assert_called_once_with(DownloadRequest(("Ada Researcher", "René Researcher"), ("ieee",)))
        self.assertIn("2 publication(s)", stdout.getvalue())
        self.assertIn("1 succeeded; 1 failed", stdout.getvalue())
        self.assertIn("René Researcher [ieee]", stderr.getvalue())

    @patch("main.run_download")
    def test_bare_all_reaches_middleware_as_a_download_request(self, run):
        run.return_value = []
        with redirect_stdout(io.StringIO()):
            self.assertEqual(main(["all"]), 0)
        run.assert_called_once_with(DownloadRequest(authors="all", sources="all"))

    @patch("main.run_download")
    def test_failed_markdown_report_identifies_retained_raw(self, run):
        run.return_value = [DownloadResult("Ada Researcher", "ieee", 1, Path("retained.json"),
                                           error="Markdown saving failed: disk error")]
        stderr = io.StringIO()
        with redirect_stdout(io.StringIO()), redirect_stderr(stderr):
            status = main(["all"])
        self.assertEqual(status, 1)
        self.assertIn("Markdown saving failed", stderr.getvalue())
        self.assertIn("raw saved: retained.json", stderr.getvalue())

    @patch("main.run_download")
    def test_success_and_request_failure_exit_codes(self, run):
        run.return_value = [DownloadResult("Ada Researcher", "ieee", 0, Path("raw"), Path("md"))]
        with redirect_stdout(io.StringIO()):
            self.assertEqual(main(["all"]), 0)
        run.side_effect = ValueError("Unknown author")
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            self.assertEqual(main(["all"]), 1)
        self.assertIn("Unknown author", stderr.getvalue())


class DownloadManagerTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.data = self.root / "data"
        self.data.mkdir()
        authors_file = self.data / "authors.md"
        authors_file.write_text(AUTHOR_TEXT, encoding="utf-8")
        env_file = self.root / ".env"
        env_file.write_text("IEEE_API_KEY=synthetic-key\n", encoding="utf-8")
        for name, value in [("DATA_DIRECTORY", self.data), ("AUTHORS_FILE", authors_file), ("ENV_FILE", env_file)]:
            patcher = patch.object(config, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def markdown_path(self, slug="ada-researcher"):
        return self.data / slug / f"{slug}-ieee.md"

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
        results, fetch = self.run_offline(DownloadRequest(("Ada Researcher",), ("ieee",)), [native])
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertIsNone(result.error)
        self.assertEqual(result.publication_count, 1)
        self.assertEqual(json.loads(result.raw_file_path.read_text()), [native])
        markdown = result.markdown_path.read_text(encoding="utf-8")
        self.assertIn("## Über Research Across Systems", markdown)
        self.assertIn("Authors: First Author; Second Author", markdown)
        self.assertIn("Keywords: Author keyword; Second keyword; IEEE term", markdown)
        fetch.assert_called_once()

    def test_manager_delegates_selected_authors_downloads_and_builds_without_writes(self):
        author = Author("Ada Researcher", ("University A",))
        publications = [Publication(title="A work")]
        response = SourceDownload(publications, Path("source-owned.json"))
        build = MarkdownBuildResult(markdown_path=Path("builder-owned.md"))
        with patch("download_manager.load_authors", return_value=[author]) as reader, \
             patch("ieee_xplore.download", return_value=response) as download, \
             patch("download_manager.build_markdown", return_value=build) as builder, \
             patch("storage.save_raw") as raw_save, patch("storage.save_markdown") as markdown_save:
            results = run_download(DownloadRequest((author.name,), ("ieee",)))
        reader.assert_called_once_with((author.name,))
        download.assert_called_once_with(author)
        builder.assert_called_once_with(author, "ieee", publications)
        raw_save.assert_not_called()
        markdown_save.assert_not_called()
        self.assertEqual(results, [DownloadResult(author.name, "ieee", 1,
                                                  response.raw_file_path, build.markdown_path)])

    def test_manager_returns_builder_error_and_continues_with_next_pair(self):
        authors = [Author("Ada Researcher", ("University A",)), Author("René Researcher", ("Institute B",))]
        downloads = [SourceDownload([Publication()], Path("first.json")), SourceDownload([], Path("second.json"))]
        builds = [MarkdownBuildResult(error="Markdown saving failed: disk error"),
                  MarkdownBuildResult(markdown_path=Path("second.md"))]
        with patch("download_manager.load_authors", return_value=authors), \
             patch("ieee_xplore.download", side_effect=downloads) as download, \
             patch("download_manager.build_markdown", side_effect=builds) as builder:
            results = run_download(DownloadRequest("all", "all"))
        self.assertEqual(download.call_count, 2)
        self.assertEqual(builder.call_count, 2)
        self.assertEqual(results, [
            DownloadResult("Ada Researcher", "ieee", 1, Path("first.json"), error=builds[0].error),
            DownloadResult("René Researcher", "ieee", 0, Path("second.json"), Path("second.md")),
        ])

    def test_manager_carries_source_error_path_without_calling_builder(self):
        author = Author("Ada Researcher", ("University A",))
        error = DownloadError("Normalization failed: invalid metadata", raw_file_path=Path("retained.json"))
        with patch("download_manager.load_authors", return_value=[author]), \
             patch("ieee_xplore.download", side_effect=error), patch("download_manager.build_markdown") as builder:
            results = run_download(DownloadRequest("all", "all"))
        builder.assert_not_called()
        self.assertEqual(results, [DownloadResult(author.name, "ieee", raw_file_path=Path("retained.json"),
                                                  error=str(error))])

    def test_all_authors_does_not_override_source_validation(self):
        with patch("ieee_xplore.download") as download, self.assertRaises(ValueError):
            run_download(DownloadRequest("all", ("sciencedirect",)))
        download.assert_not_called()

    def test_unknown_author_or_source_fails_before_any_request(self):
        requests = [DownloadRequest(("Ada Researcher", "Unknown"), "all"),
                    DownloadRequest(("Ada Researcher",), ("ieee", "unknown")),
                    DownloadRequest((), "all"), DownloadRequest("invalid", "all")]
        for request in requests:
            with self.subTest(request=request), patch("ieee_xplore.download") as download:
                with self.assertRaises(ValueError):
                    run_download(request)
                download.assert_not_called()
        self.assertEqual(list(self.data.iterdir()), [self.data / "authors.md"])

    def test_all_request_processes_master_order_and_source_calls_receive_authors(self):
        from models import SourceDownload
        response = SourceDownload([], Path("raw.json"))
        with patch("ieee_xplore.download", return_value=response) as download:
            results = run_download(DownloadRequest(authors="all", sources="all"))
        self.assertEqual(download.call_args_list, [
            call(Author("Ada Researcher", ("University A", "Institute B"))),
            call(Author("René Researcher", ("University A", "Institute B", "Former University"))),
        ])
        self.assertEqual([result.author for result in results], ["Ada Researcher", "René Researcher"])

    def test_middleware_rejects_bare_all_before_loading_authors(self):
        with patch("download_manager.load_authors") as load:
            with self.assertRaisesRegex(ValueError, "Expected DownloadRequest"):
                run_download("all")
        load.assert_not_called()

    def test_explicit_author_order_and_duplicates(self):
        results, fetch = self.run_offline(
            DownloadRequest(("René Researcher", "Ada Researcher", "René Researcher"), "all"),
            [page(0, []), page(0, [])],
        )
        self.assertEqual([result.author for result in results], ["René Researcher", "Ada Researcher"])
        self.assertEqual(fetch.call_count, 2)

    def test_zero_results_replaces_markdown_but_retains_prior_raw(self):
        self.run_offline(DownloadRequest(("Ada Researcher",), "all"), [page(1, [1])])
        old_raw = self.downloads()[0]
        original = old_raw.read_bytes()
        results, _ = self.run_offline(DownloadRequest(("Ada Researcher",), "all"), [page(0, [])])
        self.assertIsNone(results[0].error)
        self.assertEqual(results[0].publication_count, 0)
        self.assertEqual(self.markdown_path().read_text(), "")
        self.assertEqual(old_raw.read_bytes(), original)
        self.assertEqual(len(self.downloads()), 2)

    def test_later_page_failure_keeps_old_outputs_and_continues_other_authors(self):
        self.run_offline(DownloadRequest(("Ada Researcher",), "all"), [page(1, [99])])
        old_raw = self.downloads()
        old_markdown = self.markdown_path().read_bytes()
        results, fetch = self.run_offline(DownloadRequest(authors="all", sources="all"), [page(2, [1]), DownloadError("HTTP 503"), page(1, [3])])
        self.assertIn("Download failed", results[0].error)
        self.assertIsNone(results[0].raw_file_path)
        self.assertIsNone(results[1].error)
        self.assertEqual(self.downloads(), old_raw)
        self.assertEqual(self.markdown_path().read_bytes(), old_markdown)
        self.assertTrue(self.markdown_path("rené-researcher").exists())
        self.assertEqual(fetch.call_count, 3)

    def test_markdown_failure_retains_new_raw_and_previous_markdown(self):
        for target in ["markdown_builder.render_publications", "markdown_builder.storage.save_markdown"]:
            with self.subTest(target=target):
                destination = self.markdown_path()
                destination.parent.mkdir(exist_ok=True)
                destination.write_text("Previous Markdown", encoding="utf-8")
                with patch(target, side_effect=ValueError("Markdown failure")):
                    results, _ = self.run_offline(DownloadRequest(authors="all", sources="all"), [page(1, [1]), page(1, [2])])
                self.assertIn("Markdown", results[0].error)
                self.assertTrue(results[0].raw_file_path.exists())
                self.assertIsNone(results[0].markdown_path)
                self.assertEqual(destination.read_text(), "Previous Markdown")

    def test_markdown_failure_for_one_author_does_not_block_next(self):
        from markdown_builder import render_publications
        calls = 0

        def render(publications):
            nonlocal calls
            calls += 1
            if calls == 1:
                raise ValueError("first author failed")
            return render_publications(publications)

        with patch("markdown_builder.render_publications", side_effect=render):
            results, _ = self.run_offline(DownloadRequest(authors="all", sources="all"), [page(1, [1]), page(1, [2])])
        self.assertIsNotNone(results[0].error)
        self.assertIsNone(results[1].error)
        self.assertTrue(results[1].markdown_path.exists())

    def test_raw_write_failure_preserves_markdown_and_other_author_still_completes(self):
        (self.data / "ada-researcher").mkdir()
        (self.data / "ada-researcher" / "raw").write_text("occupied", encoding="utf-8")
        self.markdown_path().write_text("Previous Markdown", encoding="utf-8")
        results, _ = self.run_offline(DownloadRequest(authors="all", sources="all"), [page(1, [1]), page(1, [2])])
        self.assertIn("Raw saving failed", results[0].error)
        self.assertIsNone(results[1].error)
        self.assertEqual(self.markdown_path().read_text(), "Previous Markdown")

    def test_normalization_failure_retains_complete_raw_and_continues(self):
        self.run_offline(DownloadRequest(("Ada Researcher",), "all"), [page(1, [99])])
        old_raw = self.downloads()[0]
        old_raw_content = old_raw.read_bytes()
        old_markdown = self.markdown_path().read_bytes()
        bad = page(1, [1])
        bad["articles"][0]["abstract"] = []
        results, _ = self.run_offline(DownloadRequest(authors="all", sources="all"), [bad, page(0, [])])
        self.assertIsNotNone(results[0].error)
        self.assertEqual(json.loads(results[0].raw_file_path.read_text()), [bad])
        self.assertEqual(old_raw.read_bytes(), old_raw_content)
        self.assertEqual(self.markdown_path().read_bytes(), old_markdown)
        self.assertEqual(len(self.downloads()), 2)
        self.assertIsNone(results[1].error)

    def test_run_from_another_directory_uses_project_paths_and_file_credentials(self):
        project = self.root / "copied-project"
        shutil.copytree(PROJECT_ROOT / "src", project / "src", ignore=shutil.ignore_patterns("__pycache__"))
        (project / "data").mkdir()
        (project / "data" / "authors.md").write_text(AUTHOR_TEXT, encoding="utf-8")
        script = project / "src" / "main.py"
        result = subprocess.run([sys.executable, "-B", str(script), "--source", "ieee"],
                                cwd=self.root, capture_output=True, text=True, check=False,
                                env={**os.environ, "IEEE_API_KEY": "must-not-be-used"})
        self.assertEqual(result.returncode, 1)
        self.assertIn(str(project / ".env"), result.stderr)
        self.assertIn("0 succeeded; 2 failed", result.stdout)
        self.assertNotIn("Traceback", result.stderr)
        self.assertNotIn("must-not-be-used", result.stderr)
        self.assertFalse((project / "data" / "ada-researcher").exists())
