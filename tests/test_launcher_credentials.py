"""Opt-in, memory-only credentials for both existing publisher downloaders."""

import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from support import page
import config
from author_builder import Author
from models import DownloadError, DownloadRecord
from source_downloaders import common, ieee_xplore, sciencedirect


SOURCES = (ieee_xplore, sciencedirect)


def empty_pages(source):
    if source is ieee_xplore:
        return [page(0, [])]
    return [{"search-results": {"opensearch:totalResults": "0", "entry": []}}]


class LauncherCredentialTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.env_file = self.root / ".env"
        self.author = Author("René Researcher", ("University A",))
        for name, value in (("ENV_FILE", self.env_file), ("DATA_DIRECTORY", self.root / "data")):
            context = patch.object(config, name, value)
            context.start()
            self.addCleanup(context.stop)

    def test_environment_mode_works_without_reading_or_creating_a_credential_file(self):
        for source in SOURCES:
            with self.subTest(source=source.SOURCE), patch.dict(os.environ, {
                config.CREDENTIAL_MODE_VARIABLE: "environment", source.API_KEY_NAME: "  run-only-key  "
            }, clear=True), patch.object(source, "download_pages", return_value=empty_pages(source)) as pages, \
                    patch.object(common, "dotenv_values", side_effect=AssertionError("Must not read .env")):
                result = source.download(self.author)
                self.assertIsInstance(result, DownloadRecord)
                self.assertEqual(pages.call_args.args[1], "run-only-key")
                self.assertFalse(self.env_file.exists())
                self.assertNotIn("run-only-key", result.raw_file_path.read_text(encoding="utf-8"))

    def test_missing_environment_keys_do_not_fall_back_to_a_valid_file(self):
        self.env_file.write_text("IEEE_API_KEY=file-key\nSCIENCEDIRECT_API_KEY=file-key\n", encoding="utf-8")
        before = self.env_file.read_bytes()
        for source in SOURCES:
            for values in ({}, {source.API_KEY_NAME: ""}, {source.API_KEY_NAME: "  "}):
                with self.subTest(source=source.SOURCE, values=values), patch.dict(os.environ, {
                    config.CREDENTIAL_MODE_VARIABLE: "environment", **values
                }, clear=True), patch.object(source, "download_pages") as pages:
                    result = source.download(self.author)
                    self.assertIsInstance(result, DownloadError)
                    self.assertIn("missing or empty in launcher credentials", result.error)
                    pages.assert_not_called()
        self.assertEqual(self.env_file.read_bytes(), before)
        self.assertFalse((self.root / "data").exists())

    def test_environment_mode_redacts_keys_in_returned_errors(self):
        for source in SOURCES:
            with self.subTest(source=source.SOURCE), patch.dict(os.environ, {
                config.CREDENTIAL_MODE_VARIABLE: "environment", source.API_KEY_NAME: "run-only-key"
            }, clear=True), patch.object(source, "download_pages", side_effect=RuntimeError("failure run-only-key")):
                result = source.download(self.author)
                self.assertIsInstance(result, DownloadError)
                self.assertNotIn("run-only-key", result.error)
                self.assertIn("[REDACTED]", result.error)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_normal_cli_still_uses_file_credentials(self):
        self.env_file.write_text("IEEE_API_KEY=file-key\nSCIENCEDIRECT_API_KEY=file-key\n", encoding="utf-8")
        for source in SOURCES:
            for mode in (None, "", "other"):
                values = {source.API_KEY_NAME: "ignored-environment-key"}
                if mode is not None:
                    values[config.CREDENTIAL_MODE_VARIABLE] = mode
                with self.subTest(source=source.SOURCE, mode=mode), patch.dict(os.environ, values, clear=True), \
                        patch.object(source, "download_pages", return_value=empty_pages(source)) as pages:
                    self.assertIsInstance(source.download(self.author), DownloadRecord)
                    self.assertEqual(pages.call_args.args[1], "file-key")
