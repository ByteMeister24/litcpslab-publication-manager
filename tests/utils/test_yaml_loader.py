"""Unit tests for parsing complete YAML files into author mappings."""

from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tests.support import AUTHOR_YAML
from utils.yaml_loader import convert_yaml_to_dict


class YAMLLoaderTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / "authors.yaml"

    def read_yaml(self, text=AUTHOR_YAML):
        self.path.write_text(text, encoding="utf-8")
        return convert_yaml_to_dict(self.path)

    def test_entire_yaml_file_becomes_a_dictionary_of_affiliation_lists(self):
        authors = self.read_yaml()
        self.assertIsInstance(authors, dict)
        self.assertEqual(authors, {
            "Ada Researcher": ["University A", "Institute B"],
            "René Researcher": ["University A", "Institute B", "Former University"],
        })
        self.assertEqual(list(authors), ["Ada Researcher", "René Researcher"])

    def test_duplicate_author_keys_are_rejected_with_file_and_line(self):
        with self.assertRaises(ValueError) as caught:
            self.read_yaml("Ada Researcher: [University A]\nAda Researcher: [Institute B]\n")
        self.assertIn("Repeated author name", str(caught.exception))
        self.assertIn(str(self.path), str(caught.exception))
        self.assertIn("line 2", str(caught.exception))

    def test_shared_and_repeated_affiliation_values_are_preserved(self):
        authors = self.read_yaml("Ada Researcher: [University A, University A]\nRené Researcher: [University A]\n")
        self.assertEqual(authors, {
            "Ada Researcher": ["University A", "University A"],
            "René Researcher": ["University A"],
        })

    def test_bom_unicode_comments_and_quoted_values_are_supported(self):
        authors = self.read_yaml('\ufeff# Definitions\n"René Researcher":\n  - "Université A: research #1"\n')
        self.assertEqual(authors, {"René Researcher": ["Université A: research #1"]})

    def test_missing_file_error_is_propagated(self):
        with self.assertRaises(FileNotFoundError):
            convert_yaml_to_dict(self.path)

    def test_permission_error_is_propagated(self):
        with patch.object(Path, "open", side_effect=PermissionError("Cannot read file")):
            with self.assertRaises(PermissionError):
                convert_yaml_to_dict(self.path)

    def test_invalid_yaml_is_a_value_error_identifying_the_file(self):
        with self.assertRaises(ValueError) as caught:
            self.read_yaml("Ada Researcher: [unfinished\n")
        self.assertIn(str(self.path), str(caught.exception))

    def test_empty_files_and_non_mapping_documents_are_rejected(self):
        for text in ["", "# Only a comment\n", "{}", "null", "42", "text", "- Ada Researcher\n", "!!map [1]"]:
            with self.subTest(text=text), self.assertRaises(ValueError):
                self.read_yaml(text)

    def test_non_string_keys_are_rejected(self):
        for key in ["42", "true", "null"]:
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "Author names must be strings"):
                self.read_yaml(f"{key}: [University A]\n")

    def test_python_object_tags_are_rejected(self):
        with self.assertRaises(ValueError):
            self.read_yaml('Ada Researcher: !!python/tuple [University A]\n')

    def test_multiple_yaml_documents_are_rejected(self):
        with self.assertRaises(ValueError):
            self.read_yaml("Ada Researcher: [University A]\n---\nRené Researcher: [Institute B]\n")
