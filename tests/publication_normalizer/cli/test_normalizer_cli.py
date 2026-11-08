"""CLI selections, exit codes, and credential-free execution outside the checkout."""

from contextlib import redirect_stderr, redirect_stdout
import csv
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tests.support import AUTHOR_YAML, PROJECT_ROOT
import config
from publication_normalizer.cli.normalize_publications import main, parse_request
from publication_normalizer.normalization_manager import NormalizationResult
from publication_normalizer.source_normalizers.springer import REQUIRED_COLUMNS


class NormalizerCLITests(unittest.TestCase):
    def test_all_and_comma_separated_author_selections(self):
        for args in (["all"], ["--author", "all"], ["--author", "all, all"]):
            with self.subTest(args=args):
                self.assertEqual(parse_request(args), "all")
        self.assertEqual(parse_request(["--author", " Ada Researcher, René Researcher, Ada Researcher "]),
                         ("Ada Researcher", "René Researcher"))

    def test_invalid_cli_arguments_exit_with_usage_code_two(self):
        cases = ([], ["Ada Researcher"], ["all", "--author", "all"], ["--author"],
                 ["--author", ""], ["--author", "A,,B"], ["--author", "all,A"],
                 ["--author", "A,"], ["--source", "ieee"], ["--unknown", "all"])
        for args in cases:
            with self.subTest(args=args), redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as caught:
                    parse_request(args)
                self.assertEqual(caught.exception.code, 2)

    def test_help_exits_without_running_normalization(self):
        with patch("publication_normalizer.cli.normalize_publications.run_normalization") as run, \
                redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as caught:
                main(["--help"])
        self.assertEqual(caught.exception.code, 0)
        run.assert_not_called()

    @patch("publication_normalizer.cli.normalize_publications.run_normalization")
    def test_successes_and_skips_print_counts_paths_and_return_zero(self, run):
        run.return_value = [NormalizationResult("Ada Researcher", "success", 2, Path("Ada Researcher-publications.json"),
                                               duplicates_removed=3),
                            NormalizationResult("René Researcher", "skipped")]
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            status = main(["--author", "Ada Researcher, René Researcher"])
        run.assert_called_once_with(("Ada Researcher", "René Researcher"))
        self.assertEqual(status, 0)
        self.assertIn("2 publication(s)", stdout.getvalue())
        self.assertIn("3 duplicate(s) removed", stdout.getvalue())
        self.assertIn("Ada Researcher-publications.json", stdout.getvalue())
        self.assertIn("Normalization skipped: René Researcher", stdout.getvalue())
        self.assertIn("1 succeeded; 0 partial; 0 failed; 1 skipped", stdout.getvalue())
        self.assertEqual(stderr.getvalue(), "")

    @patch("publication_normalizer.cli.normalize_publications.run_normalization")
    def test_success_reports_zero_duplicates_removed(self, run):
        run.return_value = [NormalizationResult("Ada Researcher", "success", 1, Path("normalized.json"))]
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            status = main(["--author", "Ada Researcher"])
        self.assertEqual(status, 0)
        self.assertIn("0 duplicate(s) removed", stdout.getvalue())

    @patch("publication_normalizer.cli.normalize_publications.run_normalization")
    def test_partial_and_failed_results_report_errors_and_return_one(self, run):
        run.return_value = [
            NormalizationResult("Ada Researcher", "partial", 1, Path("partial.json"), ("bad.csv: missing column",),
                                duplicates_removed=2),
            NormalizationResult("René Researcher", "failed", errors=("export.bib: malformed",)),
        ]
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            status = main(["all"])
        run.assert_called_once_with("all")
        self.assertEqual(status, 1)
        self.assertIn("Normalization partial: Ada Researcher", stdout.getvalue())
        self.assertIn("2 duplicate(s) removed", stdout.getvalue())
        self.assertIn("bad.csv: missing column", stderr.getvalue())
        self.assertIn("export.bib: malformed", stderr.getvalue())
        self.assertIn("previous normalized file retained", stderr.getvalue())
        self.assertIn("0 succeeded; 1 partial; 1 failed; 0 skipped", stdout.getvalue())

    @patch("publication_normalizer.cli.normalize_publications.run_normalization", side_effect=ValueError("Unknown author"))
    def test_validation_failure_has_no_traceback(self, run):
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            self.assertEqual(main(["all"]), 1)
        self.assertIn("Unknown author", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_package_help_from_another_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, "-B", "-m", "publication_normalizer", "--help"], cwd=directory,
                env={**os.environ, "PYTHONPATH": str(PROJECT_ROOT / "src")},
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("--author", result.stdout)
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_zero_publications_print_skip_and_return_zero_without_creating_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            authors = root / "authors.yaml"
            authors.write_text(AUTHOR_YAML, encoding="utf-8")
            empty = root / "data" / config.DOWNLOAD_DIRECTORY_FORMAT.format(
                author_slug="ada-researcher", source="acm",
            ) / "empty.bib"
            empty.parent.mkdir(parents=True)
            empty.write_text("", encoding="utf-8")
            stdout, stderr = io.StringIO(), io.StringIO()
            with patch.object(config, "AUTHORS_FILE", authors), patch.object(config, "DATA_DIRECTORY", root / "data"), \
                    patch("publication_normalizer.normalization_manager.get_creation_timestamp", return_value=1.0), \
                    redirect_stdout(stdout), redirect_stderr(stderr):
                status = main(["--author", "Ada Researcher"])
            self.assertEqual(status, 0)
            self.assertIn("Normalization skipped: Ada Researcher: no publications to normalize.", stdout.getvalue())
            self.assertIn("0 succeeded; 0 partial; 0 failed; 1 skipped", stdout.getvalue())
            self.assertEqual(stderr.getvalue(), "")
            self.assertFalse((root / "data" / "normalized").exists())

    def test_real_conversion_needs_no_api_modules_credentials_or_network(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "project with spaces René"
            shutil.copytree(PROJECT_ROOT / "src", project / "src",
                            ignore=shutil.ignore_patterns("__pycache__", "*.egg-info"))
            (project / "db").mkdir()
            (project / "db" / "authors.yaml").write_text(AUTHOR_YAML, encoding="utf-8")
            raw = project / "data" / config.DOWNLOAD_DIRECTORY_FORMAT.format(
                author_slug="ada-researcher", source="springer",
            ) / "SearchResults.csv"
            raw.parent.mkdir(parents=True)
            with raw.open("w", encoding="utf-8", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=REQUIRED_COLUMNS)
                writer.writeheader()
                writer.writerow({"Item Title": "Über research", "Item DOI": "10.1000/offline",
                                 "Authors": "Ada Researcher, René Researcher"})
                writer.writerow({"Item Title": "Later duplicate", "Item DOI": "https://doi.org/10.1000/offline"})
            before = raw.read_bytes()
            script = '''
from pathlib import Path
import sys
from unittest.mock import patch

def guard(event, args):
    if event == 'open' and isinstance(args[0], (str, bytes)) and Path(args[0]).name == '.env':
        raise AssertionError('Credentials must not be read')
    if event.startswith('socket.'):
        raise AssertionError('Network must not be used')

sys.addaudithook(guard)
with patch.dict(sys.modules, {name: None for name in (
    'publication_collector', 'dotenv', 'publication_markdown',
)}):
    from publication_normalizer.cli.normalize_publications import main
    raise SystemExit(main(['--author', 'ada researcher']))
'''
            result = subprocess.run(
                [sys.executable, "-B", "-c", script], cwd=directory, capture_output=True, text=True,
                env={**os.environ, "PYTHONPATH": str(project / "src")}, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Normalization completed: Ada Researcher", result.stdout)
            self.assertIn("1 publication(s)", result.stdout)
            self.assertIn("1 duplicate(s) removed", result.stdout)
            normalized = project / "data" / "normalized" / config.NORMALIZED_FILENAME_FORMAT.format(
                author_slug="ada-researcher",
            )
            records = json.loads(normalized.read_text())
            self.assertEqual([record["title"] for record in records], ["Über research"])
            self.assertEqual(raw.read_bytes(), before)
            self.assertFalse((project / ".env").exists())
            self.assertFalse(list((project / "data").rglob("*.md")))
