"""Atomic publication of new files and replacement of existing files."""

from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from utils.storage import save_file


class StorageTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)

    def test_history_cannot_be_overwritten_and_temporary_files_are_removed(self):
        destination = self.root / "raw.json"
        save_file(destination, "original", replace=False)
        with self.assertRaises(FileExistsError):
            save_file(destination, "replacement", replace=False)
        self.assertEqual(destination.read_text(), "original")
        self.assertEqual(list(self.root.iterdir()), [destination])

    def test_replacement_saves_utf8_and_preserves_other_files(self):
        destination = self.root / "nested" / "output.md"
        save_file(destination, "Previous export", replace=True)
        sibling = destination.with_name("other.md")
        sibling.write_text("Preserve sibling", encoding="utf-8")

        save_file(destination, "Über replacement\n", replace=True)

        self.assertEqual(destination.read_bytes(), "Über replacement\n".encode("utf-8"))
        self.assertEqual(sibling.read_text(), "Preserve sibling")
        self.assertEqual(set(destination.parent.iterdir()), {destination, sibling})

    def test_failed_replacement_preserves_existing_file_and_cleans_temporary_files(self):
        destination = self.root / "output.md"
        save_file(destination, "Über old\n", replace=True)
        with patch("utils.storage.os.replace", side_effect=OSError("disk error")):
            with self.assertRaises(OSError):
                save_file(destination, "new", replace=True)
        self.assertEqual(destination.read_text(encoding="utf-8"), "Über old\n")
        self.assertEqual(list(self.root.iterdir()), [destination])
        save_file(destination, "new", replace=True)
        self.assertEqual(destination.read_text(), "new")

    def test_failed_raw_publication_leaves_no_incomplete_file(self):
        destination = self.root / "raw" / "result.json"
        with patch("utils.storage.os.link", side_effect=OSError("disk error")):
            with self.assertRaises(OSError):
                save_file(destination, "complete", replace=False)
        self.assertEqual(list(destination.parent.iterdir()), [])
