"""Unit tests for author validation and selection using parsed mappings."""

from typing import cast
import unittest
from unittest.mock import patch

from support import PROJECT_ROOT
import config
from helpers.author_builder import Author, get_selected_authors
from helpers.selection import Selection


class AuthorBuilderTests(unittest.TestCase):
    def setUp(self):
        self.path = PROJECT_ROOT / "synthetic-authors.yaml"
        patcher = patch.object(config, "AUTHORS_FILE", self.path)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.definitions = {
            "Ada Researcher": ["University A", "Institute B"],
            "René Researcher": ["University A", "Institute B", "Former University"],
        }
        self.ada = Author("Ada Researcher", ("University A", "Institute B"))
        self.rene = Author("René Researcher", ("University A", "Institute B", "Former University"))

    def test_all_returns_author_instances_in_database_order(self):
        with patch("helpers.author_builder.convert_yaml_to_dict", return_value=self.definitions) as loader:
            authors = get_selected_authors("all")
        loader.assert_called_once_with(self.path)
        self.assertIsInstance(authors, list)
        self.assertTrue(all(isinstance(author, Author) for author in authors))
        self.assertEqual(authors, [self.ada, self.rene])

    def test_single_selected_name_returns_only_its_author(self):
        with patch("helpers.author_builder.convert_yaml_to_dict", return_value=self.definitions):
            self.assertEqual(get_selected_authors(("René Researcher",)), [self.rene])

    def test_multiple_selections_preserve_requested_order_and_remove_duplicates(self):
        with patch("helpers.author_builder.convert_yaml_to_dict", return_value=self.definitions) as loader:
            authors = get_selected_authors(("René Researcher", "Ada Researcher", "René Researcher"))
        loader.assert_called_once_with(self.path)
        self.assertEqual(authors, [self.rene, self.ada])

    def test_affiliations_are_used_directly_without_merging_or_deduplication(self):
        definitions = {"Ada Researcher": ["University A", "University A"], "René Researcher": ["Institute B"]}
        with patch("helpers.author_builder.convert_yaml_to_dict", return_value=definitions):
            authors = get_selected_authors("all")
        self.assertEqual(authors, [Author("Ada Researcher", ("University A", "University A")),
                                   Author("René Researcher", ("Institute B",))])

    def test_author_name_matching_ignores_case_and_keeps_database_capitalization(self):
        for selection, expected in [(("ada researcher",), [self.ada]),
                                    (("ADA RESEARCHER",), [self.ada]),
                                    (("rEnÉ rEsEaRcHeR",), [self.rene])]:
            with self.subTest(selection=selection), \
                 patch("helpers.author_builder.convert_yaml_to_dict", return_value=self.definitions):
                self.assertEqual(get_selected_authors(selection), expected)

    def test_case_variants_are_deduplicated_in_first_selected_order(self):
        with patch("helpers.author_builder.convert_yaml_to_dict", return_value=self.definitions):
            authors = get_selected_authors(("rené researcher", "ADA RESEARCHER", "RENÉ RESEARCHER", "ada researcher"))
        self.assertEqual(authors, [self.rene, self.ada])

    def test_name_capitalization_comes_from_database_including_hyphens_and_internal_capitals(self):
        definitions = {"Jean-Luc McDonald": ["University A"]}
        with patch("helpers.author_builder.convert_yaml_to_dict", return_value=definitions):
            authors = get_selected_authors(("jean-luc mcdonald",))
        self.assertEqual(authors, [Author("Jean-Luc McDonald", ("University A",))])

    def test_case_insensitive_selection_rejects_ambiguous_database_names(self):
        definitions = {"Ada Researcher": ["University A"], "ADA RESEARCHER": ["Institute B"]}
        with patch("helpers.author_builder.convert_yaml_to_dict", return_value=definitions):
            with self.assertRaisesRegex(ValueError, "ambiguous"):
                get_selected_authors(("ada researcher",))

    def test_unknown_names_are_reported_in_sorted_order(self):
        with patch("helpers.author_builder.convert_yaml_to_dict", return_value=self.definitions):
            with self.assertRaises(ValueError) as caught:
                get_selected_authors(("Unknown Z", "Ada Researcher", "Unknown A"))
        self.assertEqual(str(caught.exception), "Unknown author selection(s): Unknown A, Unknown Z.")

    def test_invalid_selections_are_rejected(self):
        invalid_selections = [(), "Ada Researcher", "invalid", None, ["Ada Researcher"],
                              ("",), ("Ada Researcher", ""), (42,), ("all",)]
        with patch("helpers.author_builder.convert_yaml_to_dict", return_value=self.definitions):
            for selection in invalid_selections:
                with self.subTest(selection=selection), self.assertRaises(ValueError):
                    get_selected_authors(cast(Selection, selection))

    def test_blank_names_and_control_characters_are_rejected(self):
        for name in ["", "   ", "Ada\tResearcher", "Ada\nResearcher", "Ada\x00Researcher"]:
            with self.subTest(name=name), patch("helpers.author_builder.convert_yaml_to_dict", return_value={name: ["University A"]}):
                with self.assertRaises(ValueError):
                    get_selected_authors("all")

    def test_affiliations_must_be_a_nonempty_list_of_nonempty_strings(self):
        invalid_values = [None, "University A", {}, (), [], [""], [" "], ["University A", None],
                          [True], [42], [{}], [["University A"]], ["University A\tDepartment"],
                          ["University A\nDepartment"], ["University A\x00Department"]]
        for affiliations in invalid_values:
            with self.subTest(affiliations=affiliations), \
                 patch("helpers.author_builder.convert_yaml_to_dict", return_value={"Ada Researcher": affiliations}):
                with self.assertRaises(ValueError):
                    get_selected_authors("all")

    def test_invalid_unselected_author_is_rejected_before_returning_selected_authors(self):
        definitions = {**self.definitions, "Other Researcher": []}
        with patch("helpers.author_builder.convert_yaml_to_dict", return_value=definitions):
            with self.assertRaises(ValueError):
                get_selected_authors(("Ada Researcher",))

    def test_loader_errors_are_propagated(self):
        for error in [FileNotFoundError("Missing file"), ValueError("Invalid YAML")]:
            with self.subTest(error=error), patch("helpers.author_builder.convert_yaml_to_dict", side_effect=error):
                with self.assertRaises(type(error)) as caught:
                    get_selected_authors("all")
                self.assertIs(caught.exception, error)
