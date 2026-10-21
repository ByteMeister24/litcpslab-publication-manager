"""Build selected authors from H2 sections and H3 affiliation subsections."""

from pathlib import Path
from typing import Optional

from markdown_it.tree import SyntaxTreeNode

import config
from markdown_reader import MarkdownDocument, MarkdownSection, read_markdown, text_content
from models import Author, Selection


def _invalid(path: Path, node: SyntaxTreeNode, message: str) -> ValueError:
    line = node.map[0] + 1 if node.map else "?"
    return ValueError(f"{path}:{line}: {message}")


def _read_text(node: SyntaxTreeNode, path: Path) -> str:
    allowed = {"heading", "paragraph", "inline", "text", "code_inline", "softbreak", "hardbreak",
               "em", "strong", "link"}
    if any(child.type not in allowed for child in node.walk()):
        raise _invalid(path, node, "Names and affiliations must be text without HTML or images.")
    value = text_content(node).strip()
    if not value or any(ord(character) < 32 for character in value):
        raise _invalid(path, node, "Names and affiliations must be nonempty text without control characters.")
    return value


def _list_items(section: MarkdownSection, path: Path) -> list[str]:
    items = []
    for block in section.content:
        if block.type != "bullet_list":
            raise _invalid(path, block, "Use flat bullet lists for names and affiliations.")
        for item in block.children:
            if len(item.children) != 1 or item.children[0].type != "paragraph":
                raise _invalid(path, item, "Each list item must contain one name or affiliation.")
            items.append(_read_text(item.children[0], path))
    return items


def _author_sections(document: MarkdownDocument, path: Path) -> dict[str, MarkdownSection]:
    if document.content:
        raise _invalid(path, document.content[0], "Content must be inside an H2 section.")
    sections = {}
    for section in document.sections:
        title = _read_text(section.heading, path)
        if section.level != 2 or title not in config.AUTHOR_SECTIONS or title in sections:
            raise _invalid(path, section.heading, f"Unknown, repeated, or non-H2 section: {title!r}.")
        if title != "Additional Affiliations" and section.subsections:
            raise _invalid(path, section.subsections[0].heading, "Only Additional Affiliations may have H3 subsections.")
        sections[title] = section
    missing = set(config.AUTHOR_SECTIONS) - set(sections)
    if missing:
        raise ValueError(f"{path}: Missing section(s): {', '.join(sorted(missing))}.")
    return sections


def _additional_affiliations(section: MarkdownSection, path: Path) -> dict[str, list[str]]:
    if section.content:
        raise _invalid(path, section.content[0], "Additional affiliations need an H3 full-author-name heading.")
    additional = {}
    for subsection in section.subsections:
        name = _read_text(subsection.heading, path)
        if subsection.level != 3 or subsection.subsections:
            raise _invalid(path, subsection.heading, "Additional affiliations must use H3 headings without subsections.")
        if name in additional:
            raise _invalid(path, subsection.heading, f"Repeated author heading: {name!r}.")
        additional[name] = _list_items(subsection, path)
    return additional


def _load_author_definitions() -> dict[str, tuple[str, ...]]:
    """Combine each author's common and additional affiliations in master order."""
    author_md_path = config.AUTHORS_FILE
    sections = _author_sections(read_markdown(author_md_path), author_md_path)
    names = _list_items(sections["Authors"], author_md_path)
    common = _list_items(sections["Common Affiliations"], author_md_path)
    additional = _additional_affiliations(sections["Additional Affiliations"], author_md_path)
    if not names:
        raise ValueError(f"{author_md_path}: Add at least one full name under Authors.")
    if len(names) != len(set(names)):
        raise ValueError(f"{author_md_path}: Author full names must be unique.")
    unknown = set(additional) - set(names)
    if unknown:
        raise ValueError(f"{author_md_path}: Additional Affiliations names not in Authors: {', '.join(sorted(unknown))}.")

    definitions = {}
    slugs = set()
    for name in names:
        slug = name.lower().replace(" ", "-")
        if name == "all" or slug in (".", "..") or any(character in name for character in "/\\"):
            raise ValueError(f"{author_md_path}: Author name cannot be used as a directory: {name!r}.")
        if slug in slugs:
            raise ValueError(f"{author_md_path}: Author names produce the same directory: {slug!r}.")
        affiliations = tuple(common + additional.get(name, []))
        if not affiliations:
            raise ValueError(f"{author_md_path}: No affiliations configured for {name!r}.")
        slugs.add(slug)
        definitions[name] = affiliations
    return definitions


def load_authors(author_selection: Selection) -> list[Author]:
    """Return selected authors with common plus author-specific affiliations."""
    if author_selection != "all" and (not isinstance(author_selection, tuple) or not author_selection
                              or any(not isinstance(name, str) or not name for name in author_selection)):
        raise ValueError("Expected author names or all.")
    
    definitions = _load_author_definitions()
    
    if author_selection == "all":
        names = tuple(definitions)
    else:
        unknown = set(author_selection) - set(definitions)
        if unknown:
            raise ValueError(f"Unknown author selection(s): {', '.join(sorted(unknown))}.")
        names = tuple(dict.fromkeys(author_selection))
    
    return [Author(name=name, affiliations=definitions[name]) for name in names]

