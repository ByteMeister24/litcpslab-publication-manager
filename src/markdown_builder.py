"""Render and save common publications using the project's Markdown schema."""

import config
import storage
from models import Author, MarkdownBuildResult, Publication


def build_markdown(author: Author, source: str, publications: list[Publication]) -> MarkdownBuildResult:
    stage = "Markdown generation"
    try:
        markdown = render_publications(publications)
        stage = "Markdown saving"
        path = storage.save_markdown(author.slug, source, markdown)
        return MarkdownBuildResult(markdown_path=path)
    except (OSError, UnicodeError, ValueError, TypeError) as error:
        return MarkdownBuildResult(error=f"{stage} failed: {error}")


def render_publications(publications: list[Publication]) -> str:
    entries = []
    for publication in publications:
        title = " ".join(publication.title.strip().splitlines())
        paragraphs = [f"## {title}"]
        for label, attribute in config.PUBLICATION_FIELDS:
            value = getattr(publication, attribute)
            if isinstance(value, tuple):
                value = "; ".join(item.strip() for item in value if item.strip())
            else:
                value = value.strip()
            paragraphs.append(f"{label}: {value}" if value else f"{label}:")
        entries.append("\n\n".join(paragraphs))
    return "\n\n".join(entries) + ("\n" if entries else "")
