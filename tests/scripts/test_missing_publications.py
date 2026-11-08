"""ODT title extraction, exact matching, and atomic missing-citation reports."""

from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from xml.sax.saxutils import escape
from zipfile import ZipFile

from tests.support import PROJECT_ROOT
from scripts.find_missing_publications import (
    Citation,
    compare_publications,
    main,
    read_odt_citations,
)


EXAMPLE_TITLE = (
    "Complexity Index-Based Graph Network Estimation for Adapting Control "
    "Programs in Cyber-Physical Production Systems"
)
EXAMPLE_CITATION = (
    "Mabkhot, M. M., Fadhlillah, H.S., Rabiser, R., Zoitl, A., Lohse, N., "
    f"Ferreira, P.: {EXAMPLE_TITLE}. "
    "International Journal of Computer Integrated Manufacturing, 2026."
)
ODT_PREFIX = (
    '<office:document-content '
    'xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '
    'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">'
    '<office:body><office:text>'
)
ODT_SUFFIX = '</office:text></office:body></office:document-content>'


class MissingPublicationTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.odt = self.root / "publications.odt"
        self.normalized = self.root / "normalized.json"
        self.output = self.root / "reports" / "missing.txt"
        self.write_citations("Ada: Present. Journal, 2026.")
        self.write_normalized([{"title": "Present"}])

    def write_odt(self, body):
        with ZipFile(self.odt, "w") as archive:
            archive.writestr("content.xml", ODT_PREFIX + body + ODT_SUFFIX)

    def write_citations(self, *citations):
        self.write_odt("".join(f"<text:p>{escape(text)}</text:p>" for text in citations))

    def write_normalized(self, records):
        self.normalized.write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")

    def existing_report(self):
        self.output.parent.mkdir(parents=True, exist_ok=True)
        self.output.write_text("Previous report\n", encoding="utf-8")
        return self.output.read_bytes()

    def run_cli(self):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = main([
                "--odt", str(self.odt),
                "--normalized", str(self.normalized),
                "--output", str(self.output),
            ])
        return code, stdout.getvalue(), stderr.getvalue()

    def test_supplied_example_extracts_the_title_and_full_citation(self):
        self.write_citations(EXAMPLE_CITATION)
        self.assertEqual(read_odt_citations(self.odt), [Citation(EXAMPLE_TITLE, EXAMPLE_CITATION)])

    def test_matching_ignores_case_and_whitespace_but_not_punctuation(self):
        present = "Ada: Über Control, Software: IEC - Systems. Journal, 2026."
        absent = "Ada: Über Control Software: IEC - Systems. Journal, 2026."
        self.write_citations(present, absent)
        self.write_normalized([{
            "title": "  ÜBER\tcontrol,\nsoftware: IEC - systems\u00a0 ",
            "doi": "10.example/unused",
        }])
        result = compare_publications(self.odt, self.normalized, self.output)
        self.assertEqual((result.extracted_count, result.matched_count, result.missing_count), (2, 1, 1))
        self.assertEqual(self.output.read_text(encoding="utf-8"), absent + "\n")

    def test_similar_titles_and_different_dash_characters_remain_missing(self):
        citations = (
            "Ada: Control Systems - A Study. Journal.",
            "Ada: Control Systems – A Study. Journal.",
            "Ada: Control System - A Study. Journal.",
        )
        self.write_citations(*citations)
        self.write_normalized([{"title": "Control Systems - A Study"}])
        result = compare_publications(self.odt, self.normalized, self.output)
        self.assertEqual(result.missing_count, 2)
        self.assertEqual(self.output.read_text(encoding="utf-8"), "\n\n".join(citations[1:]) + "\n")

    def test_first_colon_and_next_period_are_used_without_corrections(self):
        citations = (
            "Ada: Title: Subtitle, with a dash - here. Journal.",
            "Ada: Title, Journal of Research, vol. 3, 2026.",
            "Ada: Title. Another sentence. Journal.",
            "Ada:: Title. Journal.",
        )
        self.write_citations(*citations)
        self.assertEqual(
            [citation.title for citation in read_odt_citations(self.odt)],
            ["Title: Subtitle, with a dash - here", "Title, Journal of Research, vol", "Title", ": Title"],
        )

    def test_styled_text_spaces_tabs_and_line_breaks_preserve_words(self):
        self.write_odt(
            '<text:h>Publications (1 total: 1 paper)</text:h>'
            '<text:p>Journals</text:p><text:p> </text:p>'
            '<text:p>Ada:<text:s text:c="3"/>'
            '<text:span>Über Con</text:span><text:span>trol</text:span>'
            '<text:s/>Systems<text:tab/>with<text:line-break/>'
            '<text:a>IEC 61499</text:a>. <text:span>Journal</text:span>, 2026.</text:p>'
        )
        self.assertEqual(read_odt_citations(self.odt), [Citation(
            "Über Control Systems with IEC 61499",
            "Ada: Über Control Systems with IEC 61499. Journal, 2026.",
        )])

    def test_nested_paragraphs_keep_document_order_without_notes_or_comments(self):
        self.write_odt(
            '<text:p>Ada: First<text:note><text:note-body>'
            '<text:p>Note: Not a publication.</text:p>'
            '</text:note-body></text:note>. Journal.</text:p>'
            '<office:annotation><text:p>Comment: Ignore.</text:p></office:annotation>'
            '<text:tracked-changes><text:p>Deleted: Ignore.</text:p></text:tracked-changes>'
            '<text:section><text:list><text:list-item>'
            '<text:p>Ada: Second. Journal.</text:p>'
            '</text:list-item></text:list></text:section>'
            '<text:p>Ada: Third. Journal.</text:p>'
        )
        self.assertEqual(
            [citation.title for citation in read_odt_citations(self.odt)],
            ["First", "Second", "Third"],
        )

    def test_report_keeps_full_citations_order_duplicates_and_input_bytes(self):
        citations = (
            "Ada: Über Missing. Journal, 2026.",
            "Ada: Present. Journal, 2025.",
            "Ada: Another Missing. Conference, 2024.",
            "Ada: Über Missing. Journal, 2026.",
        )
        self.write_citations(*citations)
        self.write_normalized([{"title": "present"}, {"title": "PRESENT"}])
        original_inputs = (self.odt.read_bytes(), self.normalized.read_bytes())
        code, stdout, stderr = self.run_cli()
        self.assertEqual(code, 0, stderr)
        self.assertIn("Extracted: 4; matched: 1; missing: 3", stdout)
        self.assertIn(str(self.output), stdout)
        self.assertEqual(stderr, "")
        self.assertEqual(
            self.output.read_text(encoding="utf-8"),
            "\n\n".join((citations[0], citations[2], citations[3])) + "\n",
        )
        self.assertEqual((self.odt.read_bytes(), self.normalized.read_bytes()), original_inputs)

    def test_zero_missing_replaces_previous_report_with_an_empty_file(self):
        self.existing_report()
        code, stdout, stderr = self.run_cli()
        self.assertEqual(code, 0, stderr)
        self.assertIn("Extracted: 1; matched: 1; missing: 0", stdout)
        self.assertEqual(self.output.read_bytes(), b"")

    def test_empty_normalized_array_means_every_citation_is_missing(self):
        self.write_normalized([])
        result = compare_publications(self.odt, self.normalized, self.output)
        self.assertEqual((result.matched_count, result.missing_count), (0, 1))
        self.assertEqual(self.output.read_text(), "Ada: Present. Journal, 2026.\n")

    def test_normalized_utf8_bom_is_accepted(self):
        self.normalized.write_text('\ufeff[{"title": "PRESENT"}]', encoding="utf-8")
        self.assertEqual(compare_publications(self.odt, self.normalized, self.output).missing_count, 0)

    def test_invalid_normalized_inputs_preserve_existing_report(self):
        before = self.existing_report()
        for content in (
            '[{', '{}', 'null', '"text"', '[null]', '[[]]', '["title"]',
            '[{}]', '[{"title": null}]', '[{"title": 2026}]',
            '[{"title": []}]', '[{"title": "  "}]',
            '[{"title": "Valid"}, {"title": false}]',
        ):
            with self.subTest(content=content):
                self.normalized.write_text(content, encoding="utf-8")
                code, stdout, stderr = self.run_cli()
                self.assertEqual(code, 1)
                self.assertEqual(stdout, "")
                self.assertIn("Error:", stderr)
                self.assertNotIn("Traceback", stderr)
                self.assertEqual(self.output.read_bytes(), before)

    def test_malformed_odt_entries_preserve_existing_report(self):
        before = self.existing_report()
        for body in (
            '<text:p>Ada: No period</text:p>',
            '<text:p>Ada: . Journal.</text:p>',
            '<text:p>Ada:</text:p>',
            '<text:p>Ada: Valid. Journal.</text:p><text:p>Ada: Invalid</text:p>',
            '<text:p>Ada:<text:s text:c="bad"/>Title. Journal.</text:p>',
            '<text:p>Ada:<text:s text:c="0"/>Title. Journal.</text:p>',
            '<text:h>Heading: No entries</text:h><text:p>Journals</text:p>',
        ):
            with self.subTest(body=body):
                self.write_odt(body)
                code, stdout, stderr = self.run_cli()
                self.assertEqual(code, 1)
                self.assertEqual(stdout, "")
                self.assertIn(str(self.odt), stderr)
                self.assertEqual(self.output.read_bytes(), before)

    def test_invalid_odt_archives_and_xml_report_clear_errors(self):
        before = self.existing_report()
        self.odt.write_bytes(b"Not a ZIP file")
        self.assertEqual(self.run_cli()[0], 1)
        for contents in ({}, {"content.xml": "<broken"}, {"content.xml": "<wrong/>"}):
            with self.subTest(contents=contents):
                with ZipFile(self.odt, "w") as archive:
                    for name, content in contents.items():
                        archive.writestr(name, content)
                code, stdout, stderr = self.run_cli()
                self.assertEqual(code, 1)
                self.assertEqual(stdout, "")
                self.assertIn("Invalid ODT", stderr)
                self.assertEqual(self.output.read_bytes(), before)

    def test_validation_failure_does_not_create_the_report_directory(self):
        self.normalized.write_text("invalid", encoding="utf-8")
        self.assertEqual(self.run_cli()[0], 1)
        self.assertFalse(self.output.parent.exists())

    def test_missing_input_preserves_existing_report(self):
        before = self.existing_report()
        for missing in (self.root / "missing.odt", self.root / "missing.json"):
            with self.subTest(missing=missing), self.assertRaises(OSError):
                if missing.suffix == ".odt":
                    compare_publications(missing, self.normalized, self.output)
                else:
                    compare_publications(self.odt, missing, self.output)
            self.assertEqual(self.output.read_bytes(), before)

    def test_output_cannot_overwrite_either_input_or_a_symlink_to_it(self):
        alias = self.root / "alias.txt"
        alias.symlink_to(self.normalized)
        original_inputs = (self.odt.read_bytes(), self.normalized.read_bytes())
        for output in (self.odt, self.normalized, alias):
            with self.subTest(output=output), self.assertRaisesRegex(ValueError, "differ"):
                compare_publications(self.odt, self.normalized, output)
        self.assertEqual((self.odt.read_bytes(), self.normalized.read_bytes()), original_inputs)

    def test_saving_failure_preserves_previous_report_and_cleans_temporary_file(self):
        before = self.existing_report()
        with patch("utils.storage.os.replace", side_effect=OSError("Cannot save report")):
            code, stdout, stderr = self.run_cli()
        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertIn("Cannot save report", stderr)
        self.assertEqual(self.output.read_bytes(), before)
        self.assertEqual(list(self.output.parent.iterdir()), [self.output])

    def test_each_cli_path_is_required(self):
        for args in ([], ["--odt", str(self.odt)], ["--odt", str(self.odt), "--normalized", str(self.normalized)]):
            with self.subTest(args=args), redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as caught:
                    main(args)
                self.assertEqual(caught.exception.code, 2)

    def test_script_runs_from_another_directory(self):
        result = subprocess.run([
            sys.executable, "-B",
            str(PROJECT_ROOT / "src" / "scripts" / "find_missing_publications.py"),
            "--odt", str(self.odt),
            "--normalized", str(self.normalized),
            "--output", str(self.output),
        ], cwd=self.root, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("missing: 0", result.stdout)
        self.assertEqual(self.output.read_bytes(), b"")


if __name__ == "__main__":
    unittest.main()
