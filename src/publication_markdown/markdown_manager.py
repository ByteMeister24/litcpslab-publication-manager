"""Match reviewed JSON to each author and publish or remove their final file."""

from pathlib import Path

import config
from helpers.author_builder import Author, get_selected_authors
from publication_markdown.json_reader import read_publications
from publication_markdown.markdown_builder import build_markdown
from publication_markdown.markdown_models import MarkdownResult
from helpers.selection import Selection
from datetime import datetime
from zoneinfo import ZoneInfo


def _review_for_author(directory: Path, author_slug: str) -> Path | None:
    try:
        # Export filenames identify the owner; publication coauthors do not.
        files = sorted(
            path
            for path in directory.iterdir()
            if path.is_file()
            and path.suffix.lower() == ".json"
            and path.stem.rpartition("-reviewed-")[0] == author_slug
        )
    except FileNotFoundError:
        return None

    if len(files) > 1:
        raise ValueError(f"Multiple reviewed JSON files for {author_slug}; expected one exported review.")
    return files[0] if files else None


def _generate_markdown(author: Author) -> MarkdownResult:
    reviewed_path = None

    reviewed_directory = config.DATA_DIRECTORY / "reviewed/"

    creation_date = datetime.now(ZoneInfo(config.DOWNLOAD_TIMEZONE)).strftime(
        config.FINAL_MARKDOWN_DATE_FORMAT
    )
    final_filename = config.FINAL_MARKDOWN_FILENAME_FORMAT.format(
        author_slug=author.slug, timestamp=creation_date
    )
    final_directory = config.DATA_DIRECTORY / "final"
    final_filepath = final_directory / final_filename

    stage = f"Reviewed input selection ({reviewed_directory})"
    try:
        reviewed_path = _review_for_author(reviewed_directory, author.slug)

        if reviewed_path is None:
            return MarkdownResult(author.name, "skipped")

        stage = f"Reviewed JSON reading/validation ({reviewed_path})"
        publications = read_publications(reviewed_path)

        if not publications:
            stage = "Final Markdown removal"
            final_filepath.unlink(missing_ok=True)
            return MarkdownResult(
                author.name,
                "removed",
                markdown_path=final_filepath,
                reviewed_path=reviewed_path,
            )

        stage = "Markdown generation"
        built = build_markdown(author, final_filepath, publications)

        if built.error is not None:
            return MarkdownResult(
                author.name, "failed", reviewed_path=reviewed_path, error=built.error
            )
        return MarkdownResult(
            author.name,
            "generated",
            len(publications),
            built.markdown_path,
            reviewed_path,
        )
    except Exception as error:
        # Each author is an independent failure boundary; no fallback to older or unreviewed data.
        return MarkdownResult(
            author.name,
            "failed",
            reviewed_path=reviewed_path,
            error=f"{stage} failed: {error}",
        )


def run_markdown(selection: Selection) -> list[MarkdownResult]:
    """Validate database selections before generating any author's Markdown."""
    authors = get_selected_authors(selection)
    return [_generate_markdown(author) for author in authors]
