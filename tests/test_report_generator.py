"""JSON count history, HTML synchronization, and additive CLI integration."""

from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo

from support import PROJECT_ROOT
import config
from download_publications import main
from models import DownloadConfirmation, DownloadError
from report_generator import update_download_counts, update_report


REPORT_HTML = """<!DOCTYPE html>
<html lang="en">
  <head><meta charset="utf-8" /><title>Downloads</title><script src="report.js" defer="defer"></script></head>
  <body>
    <p>Last updated: <time id="last-updated">Not updated yet</time></p>
    <h2>Current Members</h2>
    <table id="current-members">
      <thead><tr><th>Author</th><th data-source="ieee">IEEE</th></tr></thead>
      <tbody><tr data-author="Ada Researcher"><th>Ada Researcher</th><td data-source="ieee">old value</td></tr></tbody>
    </table>
    <h2>Past Members</h2>
    <table id="past-members">
      <thead><tr><th>Author</th><th data-source="ieee">IEEE</th></tr></thead>
      <tbody><tr data-author="René Researcher"><th>René Researcher</th><td data-source="ieee"></td></tr></tbody>
    </table>
  </body>
</html>
"""


class ReportGeneratorTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.report_file = Path(directory.name) / "report.html"
        self.json_file = Path(directory.name) / "report.json"
        self.report_file.write_text(REPORT_HTML, encoding="utf-8")
        self.initial = {"updated_at": "2026-10-21T12:00:00+02:00",
                        "Ada Researcher": {"ieee": 0}, "René Researcher": {"ieee": 0}}
        self.write_json(self.initial)
        for name, path in [("REPORT_HTML_FILE", self.report_file), ("REPORT_JSON_FILE", self.json_file)]:
            destination = patch.object(config, name, path)
            destination.start()
            self.addCleanup(destination.stop)
        clock = patch("report_generator.datetime", wraps=datetime)
        self.clock = clock.start()
        self.clock.now.return_value = datetime(2026, 10, 22, 14, 30, tzinfo=ZoneInfo(config.DOWNLOAD_TIMEZONE))
        self.addCleanup(clock.stop)

    def write_json(self, data):
        self.json_file.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    def data(self):
        return json.loads(self.json_file.read_text(encoding="utf-8"))

    def root(self) -> ET.Element:
        return ET.parse(self.report_file).getroot()

    def cell(self, author: str, source: str = "ieee") -> ET.Element:
        row = next(row for row in self.root().findall(".//tbody/tr") if row.get("data-author") == author)
        return next(cell for cell in row.findall("td") if cell.get("data-source") == source)

    def test_initial_zero_counts_and_increases_are_saved_as_integers(self):
        self.assertEqual(update_download_counts({"Ada Researcher": {"ieee": 15}, "René Researcher": {"ieee": 0}}), [])
        self.assertEqual(self.data()["Ada Researcher"], {"ieee": 15})
        self.assertEqual(self.data()["René Researcher"], {"ieee": 0})
        self.assertIs(type(self.data()["René Researcher"]["ieee"]), int)
        self.assertEqual(self.report_file.read_text(encoding="utf-8"), REPORT_HTML)

    def test_same_count_and_empty_updates_refresh_timestamp_once_per_execution(self):
        for counts in ({"Ada Researcher": {"ieee": 0}}, {}):
            with self.subTest(counts=counts):
                self.write_json(self.initial)
                self.clock.now.reset_mock()
                self.assertEqual(update_download_counts(counts), [])
                self.assertEqual(self.data()["updated_at"], "2026-10-22T14:30:00+02:00")
                self.clock.now.assert_called_once_with(ZoneInfo(config.DOWNLOAD_TIMEZONE))
                self.assertEqual(self.data()["Ada Researcher"], {"ieee": 0})

    def test_decreases_retain_previous_counts_and_return_console_warnings_only(self):
        update_download_counts({"Ada Researcher": {"ieee": 15}})
        for count in (5, 0):
            with self.subTest(count=count):
                warnings = update_download_counts({"Ada Researcher": {"ieee": count}})
                self.assertEqual(warnings, [f"Publication count decreased for Ada Researcher [ieee]: "
                                            f"15 to {count}; keeping 15."])
                self.assertEqual(self.data()["Ada Researcher"], {"ieee": 15})
                self.assertEqual(set(self.data()), {"updated_at", "Ada Researcher", "René Researcher"})

    def test_recovered_and_higher_counts_do_not_return_previous_warnings(self):
        update_download_counts({"Ada Researcher": {"ieee": 15}})
        update_download_counts({"Ada Researcher": {"ieee": 5}})
        for count in (15, 20):
            self.assertEqual(update_download_counts({"Ada Researcher": {"ieee": count}}), [])
            self.assertEqual(self.data()["Ada Researcher"]["ieee"], count)

    def test_unprocessed_authors_and_sources_are_retained_and_new_source_zero_is_allowed(self):
        update_download_counts({"Ada Researcher": {"ieee": 3}, "René Researcher": {"other": 4}})
        update_download_counts({"Ada Researcher": {"new_source": 0}})
        self.assertEqual(self.data()["Ada Researcher"], {"ieee": 3, "new_source": 0})
        self.assertEqual(self.data()["René Researcher"], {"ieee": 0, "other": 4})

    def test_unknown_author_and_invalid_counts_do_not_replace_json(self):
        original = self.json_file.read_bytes()
        for counts in ({"Unknown": {"ieee": 5}}, {"Ada Researcher": {"ieee": -1}},
                       {"Ada Researcher": {"ieee": True}}, {"Ada Researcher": {"ieee": "5"}}):
            with self.subTest(counts=counts), self.assertRaises(ValueError):
                update_download_counts(counts)
            self.assertEqual(self.json_file.read_bytes(), original)

    def test_html_uses_json_counts_and_timestamp_and_preserves_member_groups(self):
        update_download_counts({"Ada Researcher": {"ieee": 15}})
        saved_json = self.json_file.read_bytes()
        update_report()
        self.clock.now.reset_mock()
        update_report()
        self.clock.now.assert_not_called()
        self.assertEqual(self.json_file.read_bytes(), saved_json)
        self.assertEqual(self.cell("Ada Researcher").text, "15")
        self.assertEqual(self.cell("René Researcher").text, "0")
        for group, author in [("current-members", "Ada Researcher"), ("past-members", "René Researcher")]:
            self.assertEqual([row.get("data-author") for row in self.root().findall(f".//table[@id='{group}']/tbody/tr")],
                             [author])
        updated = self.root().find(".//time[@id='last-updated']")
        assert updated is not None
        self.assertEqual(updated.text, "2026-10-22 14:30:00 CEST")
        self.assertEqual(updated.get("datetime"), self.data()["updated_at"])
        self.assertIn('<script src="report.js" defer="defer"></script>', self.report_file.read_text())

    def test_json_timestamp_is_displayed_in_vienna_including_winter_offset(self):
        self.initial["updated_at"] = "2026-12-01T12:00:00+00:00"
        self.write_json(self.initial)
        update_report()
        updated = self.root().find(".//time[@id='last-updated']")
        assert updated is not None
        self.assertEqual(updated.text, "2026-12-01 13:00:00 CET")

    def test_new_sources_add_columns_to_both_tables_and_keep_other_counts(self):
        update_download_counts({"Ada Researcher": {"ieee": 3}, "René Researcher": {"other": 4}})
        update_report()
        self.assertEqual(self.cell("Ada Researcher").text, "3")
        self.assertEqual(self.cell("René Researcher", "other").text, "4")
        self.assertIsNone(self.cell("Ada Researcher", "other").text)
        for table in self.root().findall(".//table"):
            self.assertEqual([column.get("data-source") for column in table.findall("./thead/tr/th")],
                             [None, "ieee", "other"])

    def test_sync_removes_old_html_warnings_and_ignores_old_cell_counts(self):
        self.report_file.write_text(REPORT_HTML.replace('>old value</td>',
                                    ' class="decreased">999<span class="warning">Old warning</span></td>'),
                                    encoding="utf-8")
        update_report()
        self.assertEqual(self.cell("Ada Researcher").text, "0")
        self.assertIsNone(self.cell("Ada Researcher").get("class"))
        self.assertIsNone(self.cell("Ada Researcher").find("span"))

    def test_unicode_and_html_characters_are_preserved_as_data(self):
        source = "research&<source>"
        update_download_counts({"René Researcher": {source: 7}})
        update_report()
        self.assertIn("René Researcher", self.json_file.read_text(encoding="utf-8"))
        self.assertEqual(self.cell("René Researcher", source).text, "7")
        self.assertIn("research&amp;&lt;source&gt;", self.report_file.read_text())

    def test_malformed_json_is_not_overwritten_and_does_not_change_html(self):
        invalid_documents = ["{", "[]", '{}', '{"updated_at":"invalid"}',
                             json.dumps({**self.initial, "updated_at": "2026-10-22T14:30:00"}),
                             json.dumps({**self.initial, "Ada Researcher": {"ieee": "invalid"}})]
        for content in invalid_documents:
            with self.subTest(content=content):
                self.json_file.write_text(content, encoding="utf-8")
                for operation in (lambda: update_download_counts({}), update_report):
                    with self.assertRaises(ValueError):
                        operation()
                    self.assertEqual(self.json_file.read_text(encoding="utf-8"), content)
                    self.assertEqual(self.report_file.read_text(encoding="utf-8"), REPORT_HTML)

    def test_malformed_html_or_membership_mismatch_is_not_overwritten(self):
        for content in ("<html>", REPORT_HTML.replace('id="last-updated"', 'id="other"'),
                        REPORT_HTML.replace('data-author="Ada Researcher"', 'data-author="Unknown"')):
            with self.subTest(content=content):
                self.report_file.write_text(content, encoding="utf-8")
                with self.assertRaises(ValueError):
                    update_report()
                self.assertEqual(self.report_file.read_text(encoding="utf-8"), content)

    def test_missing_json_is_reported_without_recreating_it(self):
        self.json_file.unlink()
        with self.assertRaises(FileNotFoundError):
            update_download_counts({})
        self.assertFalse(self.json_file.exists())

    def test_atomic_failures_preserve_previous_file_and_remove_temporary_files(self):
        for operation in (lambda: update_download_counts({"Ada Researcher": {"ieee": 5}}), update_report):
            with self.subTest(operation=operation):
                original_json, original_html = self.json_file.read_bytes(), self.report_file.read_bytes()
                with patch("utils.storage.os.replace", side_effect=OSError("cannot save report")):
                    with self.assertRaises(OSError):
                        operation()
                self.assertEqual(self.json_file.read_bytes(), original_json)
                self.assertEqual(self.report_file.read_bytes(), original_html)
                self.assertEqual(set(self.report_file.parent.iterdir()), {self.report_file, self.json_file})

    @patch("download_publications.run_download")
    def test_cli_updates_json_and_html_from_confirmations_and_preserves_failed_counts(self, run):
        update_download_counts({"Ada Researcher": {"ieee": 5}})
        run.return_value = [DownloadConfirmation("René Researcher", "ieee", 17, Path("rene.json")),
                            DownloadError("Ada Researcher", "ieee", "Download failed")]
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            status = main(["all"])
        self.assertEqual(status, 1)
        self.assertEqual(self.data()["Ada Researcher"]["ieee"], 5)
        self.assertEqual(self.data()["René Researcher"]["ieee"], 17)
        self.assertEqual(self.cell("Ada Researcher").text, "5")
        self.assertEqual(self.cell("René Researcher").text, "17")
        self.assertIn("Download report: 1 succeeded; 1 failed.", stdout.getvalue())
        self.assertNotIn("Markdown", stdout.getvalue())
        self.assertNotIn("Report update failed", stderr.getvalue())

    @patch("download_publications.run_download")
    def test_cli_keeps_json_when_html_save_fails(self, run):
        run.return_value = [DownloadConfirmation("Ada Researcher", "ieee", 7, Path("ada.json"))]
        self.report_file.write_text("<html>", encoding="utf-8")
        stderr = io.StringIO()
        with redirect_stdout(io.StringIO()), redirect_stderr(stderr):
            self.assertEqual(main(["all"]), 0)
        self.assertEqual(self.data()["Ada Researcher"]["ieee"], 7)
        self.assertEqual(self.report_file.read_text(), "<html>")
        self.assertIn("Report update failed", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
