"""CLI outcomes and independent, offline execution of reviewed JSON rendering."""

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
from unittest.mock import patch

from support import AUTHOR_YAML, PROJECT_ROOT
from publication_markdown.cli.generate_markdown import main, parse_request
from publication_markdown.markdown_models import MarkdownResult


class MarkdownCLITests(unittest.TestCase):
    def test_all_and_comma_separated_author_selection(self):
        for args in (["all"], ["--author", "all"], ["--author", "all, all"]):
            with self.subTest(args=args):
                self.assertEqual(parse_request(args), "all")
        self.assertEqual(parse_request(["--author", " Ada Researcher, René Researcher, Ada Researcher "]),
                         ("Ada Researcher", "René Researcher"))

    def test_usage_errors_have_exit_code_two_including_directory_arguments(self):
        for args in ([], ["Ada Researcher"], ["all", "--author", "all"], ["--author"], ["--author", ""],
                     ["--author", "A,,B"], ["--author", "all,A"], ["--author", "A,"], ["/tmp/reviews"],
                     ["--directory", "/tmp"], ["--source", "ieee"]):
            with self.subTest(args=args), redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as caught:
                    main(args)
                self.assertEqual(caught.exception.code, 2)

    def test_help_exits_without_processing(self):
        with patch("publication_markdown.cli.generate_markdown.run_markdown") as run, redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as caught:
                main(["--help"])
        self.assertEqual(caught.exception.code, 0)
        run.assert_not_called()

    @patch("publication_markdown.cli.generate_markdown.run_markdown")
    def test_generated_removed_and_skipped_outcomes_print_and_return_zero(self, run):
        run.return_value = [MarkdownResult("Ada Researcher", "generated", 2, Path("Ada Researcher-final.md")),
                            MarkdownResult("René Researcher", "removed", markdown_path=Path("René Researcher-final.md")),
                            MarkdownResult("Another Researcher", "skipped")]
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            status = main(["--author", "Ada Researcher, René Researcher"])
        run.assert_called_once_with(("Ada Researcher", "René Researcher"))
        self.assertEqual(status, 0)
        for value in ("Markdown generated: Ada Researcher", "2 publication(s)", "Ada Researcher-final.md",
                      "Markdown removed: René Researcher", "Markdown skipped: Another Researcher"):
            self.assertIn(value, stdout.getvalue())
        self.assertEqual(stderr.getvalue(), "")

    @patch("publication_markdown.cli.generate_markdown.run_markdown")
    def test_failed_outcome_reports_error_and_returns_one(self, run):
        run.return_value = [MarkdownResult("Ada Researcher", "failed", error="review.json: Invalid JSON"),
                            MarkdownResult("René Researcher", "skipped")]
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            self.assertEqual(main(["all"]), 1)
        run.assert_called_once_with("all")
        self.assertIn("Markdown failed: Ada Researcher", stderr.getvalue())
        self.assertIn("review.json: Invalid JSON", stderr.getvalue())
        self.assertIn("previous final file retained", stderr.getvalue())
        self.assertIn("Markdown skipped: René Researcher", stdout.getvalue())

    @patch("publication_markdown.cli.generate_markdown.run_markdown", side_effect=ValueError("Unknown author"))
    def test_database_validation_failure_has_no_traceback(self, run):
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            self.assertEqual(main(["all"]), 1)
        self.assertIn("Unknown author", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_module_entry_point_works_from_another_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, "-B", "-m", "publication_markdown", "--help"], cwd=directory,
                env={**os.environ, "PYTHONPATH": str(PROJECT_ROOT / "src")},
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("--author", result.stdout)
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_real_workflow_needs_no_credentials_network_or_other_workflows(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "project with spaces René"
            shutil.copytree(PROJECT_ROOT / "src", project / "src",
                            ignore=shutil.ignore_patterns("__pycache__", "*.egg-info"))
            (project / "db").mkdir()
            (project / "db" / "authors.yaml").write_text(AUTHOR_YAML, encoding="utf-8")
            reviewed = project / "data" / "ada-researcher" / "updated" / "reviewed-publications.json"
            reviewed.parent.mkdir(parents=True)
            reviewed.write_text(json.dumps([{"title": "Über reviewed work", "authors": ["René"]}],
                                            ensure_ascii=False), encoding="utf-8")
            before = reviewed.read_bytes()
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
    'publication_collector', 'publication_normalizer',
    'bibtexparser', 'dotenv',
)}):
    from publication_markdown.cli.generate_markdown import main
    raise SystemExit(main(['--author', 'ada researcher']))
'''
            result = subprocess.run(
                [sys.executable, "-B", "-c", script], cwd=directory, capture_output=True, text=True,
                env={**os.environ, "PYTHONPATH": str(project / "src")}, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Markdown generated: Ada Researcher", result.stdout)
            final = project / "data" / "ada-researcher" / "final" / "Ada Researcher-final.md"
            self.assertTrue(final.read_text(encoding="utf-8").startswith("## Über reviewed work\n\nAuthors: René\n"))
            self.assertEqual(reviewed.read_bytes(), before)
            self.assertFalse((project / ".env").exists())
            self.assertFalse((project / "output").exists())
            self.assertFalse(list((project / "data").rglob("normalized")))
