"""Offline ACM query construction, author selection, and text output tests."""

from contextlib import redirect_stderr, redirect_stdout
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tests.support import AUTHOR_YAML, PROJECT_ROOT
import config
from scripts.generate_acm_queries import (
    build_query,
    generate_queries,
    main,
    parse_request,
)
from helpers.author_builder import Author


class ACMQueryTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.authors_file = self.root / "authors.yaml"
        self.authors_file.write_text(AUTHOR_YAML, encoding="utf-8")
        self.data_directory = self.root / "data"
        self.output = self.data_directory / "acm-queries" / "queries.txt"
        for name, value in (
            ("AUTHORS_FILE", self.authors_file),
            ("DATA_DIRECTORY", self.data_directory),
        ):
            patcher = patch.object(config, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_query_requires_author_and_any_affiliation(self):
        author = Author("Ada Researcher", ("University A", "Institute B"))
        self.assertEqual(
            build_query(author),
            'ContribAuthor:("Ada Researcher") AND Affiliation:("University A" OR "Institute B")',
        )

    def test_single_affiliation_and_unicode_are_preserved(self):
        self.assertEqual(
            build_query(Author("René Researcher", ("Université Österreich",))),
            'ContribAuthor:("René Researcher") AND Affiliation:("Université Österreich")',
        )

    def test_special_characters_are_escaped_as_literals_in_both_fields(self):
        text = '+ - && || ! ( ) { } [ ] ^ " ~ * ? : / \\'
        escaped = r"\+ \- \&\& \|\| \! \( \) \{ \} \[ \] \^ \" \~ \* \? \: \/ \\"
        self.assertEqual(
            build_query(Author(text, (text,))),
            f'ContribAuthor:("{escaped}") AND Affiliation:("{escaped}")',
        )

    def test_quotes_and_boolean_words_cannot_add_query_clauses(self):
        author = Author(
            'Ada "OR" Researcher', ("Research AND Development", "Jean-Luc's Lab")
        )
        self.assertEqual(
            build_query(author),
            'ContribAuthor:("Ada \\"OR\\" Researcher") AND '
            'Affiliation:("Research AND Development" OR "Jean\\-Luc\'s Lab")',
        )

    def test_one_or_multiple_names_and_all_use_shared_selection_syntax(self):
        self.assertEqual(
            parse_request(["--author", "Ada Researcher"]), ("Ada Researcher",)
        )
        self.assertEqual(
            parse_request(
                ["--author", " René Researcher, Ada Researcher, René Researcher "]
            ),
            ("René Researcher", "Ada Researcher"),
        )
        for args in (["all"], ["--author", "all"]):
            with self.subTest(args=args):
                self.assertEqual(parse_request(args), "all")

    def test_invalid_cli_arguments_exit_with_usage_code_two(self):
        cases = (
            [],
            ["Ada Researcher"],
            ["--author"],
            ["--author", ""],
            ["--author", "A,,B"],
            ["--author", "all,A"],
            ["all", "--author", "all"],
            ["--source", "acm"],
        )
        for args in cases:
            with self.subTest(args=args), redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as caught:
                    parse_request(args)
                self.assertEqual(caught.exception.code, 2)

    def test_selected_authors_keep_canonical_names_order_and_yaml_affiliations(self):
        result = generate_queries(
            ("rené researcher", "ADA RESEARCHER", "RENÉ RESEARCHER")
        )
        self.assertEqual(result, self.output)
        self.assertEqual(
            self.output.read_text(encoding="utf-8"),
            'ContribAuthor:("René Researcher") AND '
            'Affiliation:("University A" OR "Institute B" OR "Former University")\n'
            'ContribAuthor:("Ada Researcher") AND '
            'Affiliation:("University A" OR "Institute B")\n',
        )

    def test_all_writes_database_order_and_rerun_replaces_with_selected_author(self):
        generate_queries("all")
        lines = self.output.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 2)
        self.assertTrue(lines[0].startswith('ContribAuthor:("Ada Researcher")'))
        self.assertTrue(lines[1].startswith('ContribAuthor:("René Researcher")'))
        generate_queries(("Ada Researcher",))
        self.assertEqual(self.output.read_text(encoding="utf-8"), lines[0] + "\n")

    def test_unknown_author_preserves_previous_output_and_reports_failure(self):
        generate_queries("all")
        before = self.output.read_bytes()
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            self.assertEqual(main(["--author", "Ada Researcher, Unknown Author"]), 1)
        self.assertIn("Unknown Author", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())
        self.assertEqual(self.output.read_bytes(), before)

    def test_invalid_yaml_does_not_create_output(self):
        self.authors_file.write_text("Ada Researcher: []\n", encoding="utf-8")
        with redirect_stderr(io.StringIO()):
            self.assertEqual(main(["all"]), 1)
        self.assertFalse(self.output.exists())

    def test_saving_failure_preserves_previous_text_and_cleans_temporary_file(self):
        generate_queries("all")
        before = self.output.read_bytes()
        stderr = io.StringIO()
        with patch(
            "utils.storage.os.replace", side_effect=OSError("Cannot replace queries")
        ), redirect_stderr(stderr):
            self.assertEqual(main(["--author", "Ada Researcher"]), 1)
        self.assertIn("Cannot replace queries", stderr.getvalue())
        self.assertEqual(self.output.read_bytes(), before)
        self.assertEqual(list(self.output.parent.iterdir()), [self.output])

    def test_success_reports_output_path(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            self.assertEqual(main(["--author", "ada researcher"]), 0)
        self.assertIn(str(self.output), stdout.getvalue())
        self.assertEqual(len(self.output.read_text(encoding="utf-8").splitlines()), 1)

    def test_script_help_works_outside_project_directory(self):
        result = subprocess.run(
            [
                sys.executable,
                "-B",
                str(PROJECT_ROOT / "src" / "scripts" / "generate_acm_queries.py"),
                "--help",
            ],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--author", result.stdout)
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
