"""Portable staging excludes local state and preserves the report contracts."""

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from support import AUTHOR_YAML
from tools.build_portable import build, stage_resources


class PortableBuildTests(unittest.TestCase):
    def test_resources_are_copied_and_reports_reset_without_copying_private_state(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "checkout"
            bundle = Path(directory) / "portable folder René"
            for relative in ("db", "schema", "output", "docs", "data"):
                (project / relative).mkdir(parents=True)
            (project / "db" / "authors.yaml").write_text(AUTHOR_YAML, encoding="utf-8")
            (project / "schema" / "publication-schema.md").write_text("Schema reference", encoding="utf-8")
            html = '''<html><body><time id="last-updated" datetime="2020-01-01T00:00:00+00:00">old</time>
<table id="current"><thead><tr><th>Author</th><th data-source="ieee">IEEE</th></tr></thead>
<tbody><tr data-author="Ada Researcher"><th>Ada</th><td data-source="ieee">99</td></tr></tbody></table>
<table id="past"><thead><tr><th>Author</th><th data-source="ieee">IEEE</th></tr></thead>
<tbody><tr data-author="René Researcher"><th>René</th><td data-source="ieee">88</td></tr></tbody></table>
</body></html>'''
            (project / "output" / "report.html").write_text(html, encoding="utf-8")
            (project / "output" / "report.js").write_text("// report script", encoding="utf-8")
            (project / "output" / "report.json").write_text('{"private": 99}', encoding="utf-8")
            (project / "docs" / "desktop-app.md").write_text("Desktop guide", encoding="utf-8")
            (project / ".env").write_text("IEEE_API_KEY=must-not-share", encoding="utf-8")
            (project / "data" / "old.md").write_text("Previous download", encoding="utf-8")
            stage_resources(bundle, project)

            self.assertFalse((bundle / ".env").exists())
            self.assertEqual(list((bundle / "data").iterdir()), [])
            self.assertEqual((project / "output" / "report.html").read_text(encoding="utf-8"), html)
            self.assertEqual((project / "output" / "report.json").read_text(), '{"private": 99}')
            self.assertEqual((project / "db" / "authors.yaml").read_bytes(), (bundle / "db" / "authors.yaml").read_bytes())
            report = json.loads((bundle / "output" / "report.json").read_text(encoding="utf-8"))
            self.assertEqual(set(report), {"updated_at", "Ada Researcher", "René Researcher"})
            for author in ("Ada Researcher", "René Researcher"):
                self.assertEqual(report[author], {"ieee": 0, "sciencedirect": 0})
            root = ET.parse(bundle / "output" / "report.html").getroot()
            self.assertEqual([row.get("data-author") for row in root.findall(".//tbody/tr")],
                             ["Ada Researcher", "René Researcher"])
            self.assertTrue(all(cell.text == "0" for cell in root.findall(".//td[@data-source]")))
            self.assertEqual((bundle / "README.md").read_text(), "Desktop guide")
            for file in bundle.rglob("*"):
                if file.is_file():
                    self.assertNotIn("must-not-share", file.read_text(encoding="utf-8"))

    def test_build_refuses_existing_bundle_instead_of_overwriting_user_data(self):
        with tempfile.TemporaryDirectory() as directory, patch("tools.build_portable.platform.system", return_value="Linux"), \
                patch("tools.build_portable.platform.machine", return_value="x86_64"), \
                patch("tools.build_portable.importlib.util.find_spec", return_value=object()), \
                patch("tools.build_portable.subprocess.run") as run:
            destination = Path(directory) / "PublicationManager"
            destination.mkdir()
            data = destination / "keep.md"
            data.write_text("User data")
            with self.assertRaises(FileExistsError):
                build(Path(directory))
            self.assertEqual(data.read_text(), "User data")
            run.assert_not_called()

    def test_unsupported_build_platform_fails_explicitly(self):
        with patch("tools.build_portable.platform.system", return_value="Darwin"):
            with self.assertRaisesRegex(ValueError, "x64 Linux or x64 Windows"):
                build(Path("unused"))
