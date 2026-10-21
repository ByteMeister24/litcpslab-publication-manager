"""Reusable Markdown section navigation, independent of author definitions."""

from pathlib import Path
import tempfile
import unittest

from support import AUTHOR_TEXT
from markdown_reader import read_markdown, text_content


class MarkdownReaderTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / "document.md"

    def read(self, text):
        self.path.write_text(text, encoding="utf-8")
        return read_markdown(self.path)

    def test_h2_sections_expose_titles_levels_content_and_h3_subsections(self):
        document = self.read(AUTHOR_TEXT)
        self.assertEqual(document.content, [])
        self.assertEqual([section.title for section in document.sections],
                         ["Authors", "Common Affiliations", "Additional Affiliations"])
        self.assertEqual([section.level for section in document.sections], [2, 2, 2])
        authors = document.sections[0]
        self.assertEqual(authors.content[0].type, "bullet_list")
        self.assertEqual([text_content(item) for item in authors.content[0].children],
                         ["Ada Researcher", "René Researcher"])
        additional = document.sections[2]
        self.assertEqual(additional.content, [])
        self.assertEqual(additional.subsections[0].title, "René Researcher")
        self.assertEqual(additional.subsections[0].level, 3)
        self.assertEqual(text_content(additional.subsections[0].content[0]), "Former University")

    def test_heading_levels_determine_parents_and_section_boundaries(self):
        document = self.read("""Introductory prose.

# Guide
Guide introduction.
## First
First content.
### Child
Child content.
#### Grandchild
Nested content.
## Second
Second content.
# Other guide
Other content.
""")
        self.assertEqual(text_content(document.content[0]), "Introductory prose.")
        self.assertEqual([section.title for section in document.sections], ["Guide", "Other guide"])
        guide = document.sections[0]
        self.assertEqual(text_content(guide.content[0]), "Guide introduction.")
        self.assertEqual([section.title for section in guide.subsections], ["First", "Second"])
        first, second = guide.subsections
        child = first.subsections[0]
        self.assertEqual(text_content(first.content[0]), "First content.")
        self.assertEqual(text_content(child.content[0]), "Child content.")
        self.assertEqual(child.subsections[0].title, "Grandchild")
        self.assertEqual(text_content(second.content[0]), "Second content.")
        self.assertEqual(second.subsections, [])

    def test_duplicate_headings_are_preserved_and_skipped_levels_use_nearest_parent(self):
        document = self.read("## Same\nFirst.\n#### Deep\nDeep.\n### Child\nChild.\n## Same\nSecond.\n")
        self.assertEqual([section.title for section in document.sections], ["Same", "Same"])
        first, second = document.sections
        self.assertEqual([section.title for section in first.subsections], ["Deep", "Child"])
        self.assertEqual(text_content(second.content[0]), "Second.")

    def test_syntax_blocks_are_preserved_without_author_specific_restrictions(self):
        document = self.read("""## Content
A paragraph with **formatting**.

```markdown
# Inside a code block
```

> ### Inside a quote

- ### Inside a list

<div>HTML content</div>
""")
        self.assertEqual(len(document.sections), 1)
        section = document.sections[0]
        self.assertEqual(section.subsections, [])
        self.assertEqual([block.type for block in section.content],
                         ["paragraph", "fence", "blockquote", "bullet_list", "html_block"])
        self.assertEqual(text_content(section.content[0]), "A paragraph with formatting.")

    def test_bom_setext_headings_and_inline_formatting(self):
        document = self.read("\ufeff**Formatted** [heading](https://example.invalid)\n---\n\nText\ncontinued.\n")
        section = document.sections[0]
        self.assertEqual(section.title, "Formatted heading")
        self.assertEqual(section.level, 2)
        self.assertEqual(section.heading.map, (0, 2))
        self.assertEqual(text_content(section.content[0]), "Text continued.")

    def test_empty_document_and_heading_without_content(self):
        empty = self.read("")
        self.assertEqual(empty.sections, [])
        self.assertEqual(empty.content, [])
        section = self.read("## Empty\n").sections[0]
        self.assertEqual(section.title, "Empty")
        self.assertEqual(section.content, [])
        self.assertEqual(section.subsections, [])

    def test_missing_file_error_is_propagated(self):
        with self.assertRaises(FileNotFoundError):
            read_markdown(self.path)
