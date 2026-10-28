"""Render and save common publications using the project's Markdown schema."""

import config
from utils import storage
from helpers.author_builder import Author
from publication_model import Publication
from publication_markdown.markdown_models import MarkdownBuildResult
from pathlib import Path

def build_markdown(author: Author, final_filepath: Path, publications: list[Publication]) -> MarkdownBuildResult:
    stage = "Markdown generation"
    try:
        markdown = _render_publications(publications)
        stage = "Markdown saving"
        storage.save_file(final_filepath, markdown, replace=True)
        return MarkdownBuildResult(author=author.name, markdown_path=final_filepath)
    except Exception as error:
        return MarkdownBuildResult(author=author.name, error=f"{stage} failed: {error}")


def _render_publications(publications: list[Publication]) -> str:
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
