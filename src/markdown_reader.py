"""Read Markdown into a navigable hierarchy of sections and syntax blocks."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode

import config


@dataclass
class MarkdownSection:
    heading: SyntaxTreeNode
    content: list[SyntaxTreeNode] = field(default_factory=list)
    subsections: list[MarkdownSection] = field(default_factory=list)

    @property
    def title(self) -> str:
        return text_content(self.heading).strip()

    @property
    def level(self) -> int:
        return int(self.heading.tag[1:])


@dataclass
class MarkdownDocument:
    content: list[SyntaxTreeNode] = field(default_factory=list)
    sections: list[MarkdownSection] = field(default_factory=list)


def text_content(node: SyntaxTreeNode) -> str:
    """Extract text, retaining inline text order and spacing across line breaks."""
    if node.type in ("softbreak", "hardbreak"):
        return " "
    if node.children:
        return "".join(text_content(child) for child in node.children)
    return "" if node.is_root else node.content


def read_markdown(path: Path) -> MarkdownDocument:
    """Group blocks under headings, nesting subsections by heading level.

    Content belongs to its nearest preceding heading. A heading ends at the next
    heading of the same or higher level. Content before any heading stays on the
    document, and duplicate headings remain distinct sections in source order.
    """
    text = path.read_text(encoding="utf-8-sig")
    tree = SyntaxTreeNode(MarkdownIt(config.MARKDOWN_PRESET).parse(text))
    document = MarkdownDocument()
    parents = []
    for block in tree.children:
        if block.type != "heading":
            target = parents[-1] if parents else document
            target.content.append(block)
            continue
        section = MarkdownSection(heading=block)
        while parents and parents[-1].level >= section.level:
            parents.pop()
        if parents:
            parents[-1].subsections.append(section)
        else:
            document.sections.append(section)
        parents.append(section)
    return document
