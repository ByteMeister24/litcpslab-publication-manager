"""Markdown syntax and author-definition validation, with no production data."""

from pathlib import Path
import tempfile
import unittest

from support import AUTHOR_TEXT
from author_builder import load_authors
from models import Author


class AuthorBuilderTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / "authors.md"

    def read_config(self, text=AUTHOR_TEXT):
        self.path.write_text(text, encoding="utf-8")
        return load_authors("all", self.path)

    def test_common_and_additional_affiliations_preserve_master_order(self):
        definitions = self.read_config()
        self.assertEqual(definitions, [
            Author("Ada Researcher", ("University A", "Institute B")),
            Author("René Researcher", ("University A", "Institute B", "Former University")),
        ])

    def test_author_specific_affiliations_without_common_ones(self):
        text = ("## Authors\n- Ada Researcher\n## Common Affiliations\n"
                "## Additional Affiliations\n### Ada Researcher\n- University A\n")
        self.assertEqual(self.read_config(text), [Author("Ada Researcher", ("University A",))])

    def test_section_order_does_not_change_effective_affiliations(self):
        authors, rest = AUTHOR_TEXT.split("## Common Affiliations", 1)
        common, additional = rest.split("## Additional Affiliations", 1)
        reordered = "## Additional Affiliations" + additional + authors + "## Common Affiliations" + common
        self.assertEqual(self.read_config(reordered), self.read_config())

    def test_commonmark_heading_forms_and_inline_text(self):
        text = AUTHOR_TEXT.replace("## Authors", "Authors\n-------")
        text = text.replace("- University A", "- **University A**")
        text = text.replace("- Institute B", "* [Institute B](https://example.invalid)")
        self.assertEqual(self.read_config(text)[0].affiliations, ("University A", "Institute B"))

    def test_utf8_bom_and_mixed_bullet_markers(self):
        definitions = self.read_config("\ufeff" + AUTHOR_TEXT.replace("- Institute B", "+ Institute B"))
        self.assertIn("René Researcher", [author.name for author in definitions])

    def test_selected_names_preserve_order_and_are_constructed_once(self):
        self.read_config()
        authors = load_authors(("René Researcher", "Ada Researcher", "René Researcher"), self.path)
        self.assertEqual(authors, [
            Author("René Researcher", ("University A", "Institute B", "Former University")),
            Author("Ada Researcher", ("University A", "Institute B")),
        ])

    def test_unknown_or_invalid_selection_fails_without_partial_results(self):
        self.read_config()
        for selection in [("Ada Researcher", "Unknown"), (), "Ada Researcher", ("all",), ("",)]:
            with self.subTest(selection=selection), self.assertRaises(ValueError):
                load_authors(selection, self.path)

    def test_invalid_configuration_fails_explicitly(self):
        invalid_texts = [
            "",
            "# Lab Researchers\n" + AUTHOR_TEXT,
            "Introductory prose\n\n" + AUTHOR_TEXT,
            AUTHOR_TEXT.replace("### René Researcher", "#### René Researcher"),
            AUTHOR_TEXT + "\n#### Nested affiliation heading\n- University C\n",
            AUTHOR_TEXT.replace("## Authors", "## Authors\n### Unexpected subsection"),
            AUTHOR_TEXT.replace("## Common Affiliations", "## Common Affiliations\n### Unexpected subsection"),
            AUTHOR_TEXT.replace("- René Researcher\n", ""),
            AUTHOR_TEXT.replace("### René Researcher", "### Unknown Researcher"),
            AUTHOR_TEXT.replace("- René Researcher", "- Ada Researcher"),
            AUTHOR_TEXT.replace("- René Researcher", "- ADA RESEARCHER"),
            AUTHOR_TEXT.replace("- Ada Researcher", "- ../../elsewhere"),
            AUTHOR_TEXT.replace("- Ada Researcher", "- all"),
            AUTHOR_TEXT.replace("- Ada Researcher", "- Ada\tResearcher"),
            AUTHOR_TEXT.replace("- Ada Researcher", "Ada Researcher"),
            AUTHOR_TEXT.replace("## Authors", "## Authors\n## Authors"),
            AUTHOR_TEXT.replace("### René Researcher", "### René Researcher\n### René Researcher"),
            AUTHOR_TEXT.replace("## Common Affiliations", "## Other"),
            AUTHOR_TEXT.replace("### René Researcher\n", ""),
            AUTHOR_TEXT.replace("- University A\n", "").replace("- Institute B\n", ""),
            AUTHOR_TEXT.replace("- Ada Researcher", "- Ada Researcher\n  - Nested name"),
            AUTHOR_TEXT.replace("- Ada Researcher", "- Ada Researcher\n\n  Extra paragraph"),
            AUTHOR_TEXT.replace("- Ada Researcher", "- "),
            AUTHOR_TEXT.replace("- Ada Researcher", "> - Ada Researcher"),
            AUTHOR_TEXT.replace("- Ada Researcher", "```\n- Ada Researcher\n```"),
            AUTHOR_TEXT.replace("- Ada Researcher", "1. Ada Researcher"),
            AUTHOR_TEXT.replace("- Ada Researcher", '- <span>Ada Researcher</span>'),
            AUTHOR_TEXT.replace("- Ada Researcher", "- ![Ada](image.png)"),
            "## Authors\n## Common Affiliations\n## Additional Affiliations\n",
        ]
        for text in invalid_texts:
            with self.subTest(text=text), self.assertRaises(ValueError):
                self.read_config(text)
