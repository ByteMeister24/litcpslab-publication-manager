# Copyright (c) 2026 Mainak Majumder (@ByteMeister24)

"""Filesystem creation times and explicit failures when they are unavailable."""

from pathlib import Path
import subprocess
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from tests.support import PROJECT_ROOT
from utils.file_timestamps import get_creation_timestamp


class FileTimestampTests(unittest.TestCase):
    def setUp(self):
        self.path = PROJECT_ROOT / "input with spaces.json"
        metadata = patch("utils.file_timestamps.Path.stat", return_value=SimpleNamespace(
            st_ctime=900.0, st_mtime=800.0,
        ))
        self.metadata = metadata.start()
        self.addCleanup(metadata.stop)
        command = patch("utils.file_timestamps.subprocess.run")
        self.command = command.start()
        self.addCleanup(command.stop)

    def test_native_creation_time_is_used_without_running_a_command(self):
        self.metadata.return_value = SimpleNamespace(st_birthtime=100.25, st_ctime=900.0, st_mtime=800.0)
        self.assertEqual(get_creation_timestamp(self.path), 100.25)
        self.command.assert_not_called()

    def test_stat_birth_time_preserves_subseconds_and_timezone(self):
        self.command.return_value = subprocess.CompletedProcess(
            [], 0, stdout="1970-01-01 01:00:00.250000000 +0100\n", stderr="",
        )
        self.assertEqual(get_creation_timestamp(self.path), 0.25)

    def test_unavailable_creation_time_is_an_error(self):
        self.command.return_value = subprocess.CompletedProcess([], 0, stdout="-\n", stderr="")
        with self.assertRaisesRegex(ValueError, "Creation timestamp unavailable"):
            get_creation_timestamp(self.path)

    def test_stat_failure_is_reported_as_a_file_error(self):
        self.command.side_effect = subprocess.CalledProcessError(1, ["stat"], stderr="Permission denied")
        with self.assertRaisesRegex(OSError, "Permission denied"):
            get_creation_timestamp(self.path)

    def test_missing_stat_command_is_an_error(self):
        self.command.side_effect = FileNotFoundError("stat unavailable")
        with self.assertRaisesRegex(FileNotFoundError, "stat unavailable"):
            get_creation_timestamp(self.path)
