"""Offline publication-collector argument parsing and console behavior."""

from contextlib import redirect_stderr, redirect_stdout
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tests.support import PROJECT_ROOT
from publication_collector.cli.download_publications import main, parse_request
from publication_collector.download_models import DownloadConfirmation, DownloadError, DownloadRequest


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
        with patch("publication_collector.cli.download_publications.run_download") as run, redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as caught:
                main(["--help"])
        self.assertEqual(caught.exception.code, 0)
        run.assert_not_called()

    @patch("publication_collector.cli.download_publications.run_download")
    def test_cli_only_passes_request_and_reports_returned_results(self, run):
        run.return_value = [DownloadConfirmation("Ada Researcher", "ieee", 2, Path("raw.json")),
                            DownloadError("René Researcher", "ieee", "Download failed: HTTP 503")]
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            status = main(["--author", "Ada Researcher, René Researcher", "--source", "ieee"])
        self.assertEqual(status, 1)
        run.assert_called_once_with(DownloadRequest(("Ada Researcher", "René Researcher"), ("ieee",)))
        self.assertIn("2 publication(s)", stdout.getvalue())
        self.assertIn("Download report: 1 succeeded; 1 failed.", stdout.getvalue())
        self.assertIn("download location: raw.json", stdout.getvalue())
        self.assertNotIn("Markdown", stdout.getvalue())
        self.assertIn("Download failed: René Researcher [ieee]", stderr.getvalue())

    @patch("publication_collector.cli.download_publications.run_download")
    def test_bare_all_reaches_middleware_as_a_download_request(self, run):
        run.return_value = []
        with redirect_stdout(io.StringIO()):
            self.assertEqual(main(["all"]), 0)
        run.assert_called_once_with(DownloadRequest(authors="all", sources="all"))

    @patch("publication_collector.cli.download_publications.run_download")
    def test_failed_download_reports_source_error(self, run):
        run.return_value = [DownloadError("Ada Researcher", "ieee", "Raw saving failed: disk error")]
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            status = main(["all"])
        self.assertEqual(status, 1)
        self.assertIn("Raw saving failed: disk error", stderr.getvalue())
        self.assertIn("Download report: 0 succeeded; 1 failed.", stdout.getvalue())
        self.assertNotIn("Markdown", stdout.getvalue() + stderr.getvalue())

    @patch("publication_collector.cli.download_publications.run_download")
    def test_success_and_request_failure_exit_codes(self, run):
        run.return_value = [DownloadConfirmation("Ada Researcher", "ieee", 0, Path("raw"))]
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            self.assertEqual(main(["all"]), 0)
        self.assertIn("0 publication(s)", stdout.getvalue())
        self.assertIn("Download report: 1 succeeded; 0 failed.", stdout.getvalue())
        run.side_effect = ValueError("Unknown author")
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            self.assertEqual(main(["all"]), 1)
        self.assertIn("Unknown author", stderr.getvalue())

    def test_package_entry_point_shows_help_from_another_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, "-B", "-m", "publication_collector", "--help"],
                cwd=directory, capture_output=True, text=True, check=False,
                env={**os.environ, "PYTHONPATH": str(PROJECT_ROOT / "src")},
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Download publication metadata.", result.stdout)
            self.assertIn("--author", result.stdout)
            self.assertIn("--source", result.stdout)
            self.assertEqual(result.stderr, "")
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_collector_imports_without_normalization_or_markdown_modules(self):
        script = """
from unittest.mock import patch
import sys
with patch.dict(sys.modules, {name: None for name in (
    'publication_normalizer', 'publication_markdown',
)}):
    from publication_collector.cli.download_publications import main
    main(['--help'])
"""
        result = subprocess.run(
            [sys.executable, "-B", "-c", script], capture_output=True, text=True, check=False,
            env={**os.environ, "PYTHONPATH": str(PROJECT_ROOT / "src")},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
