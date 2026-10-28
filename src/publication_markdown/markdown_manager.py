"""Select the latest review and publish or remove each author's final file."""

from pathlib import Path

import config
from helpers.author_builder import Author, get_selected_authors
from publication_markdown.json_reader import read_publications
from publication_markdown.markdown_builder import build_markdown
from publication_markdown.markdown_models import MarkdownResult
from utils import storage
from utils.file_timestamps import get_creation_timestamp
from helpers.selection import Selection
from datetime import datetime
from zoneinfo import ZoneInfo



def _latest_review(directory: Path) -> Path | None:
    try:
        files = sorted(path for path in directory.iterdir()
                       if path.is_file() and path.suffix.lower() == ".json")
    except FileNotFoundError:
        return None
    
    return max(files, key=get_creation_timestamp) if files else None


def _generate_markdown(author: Author) -> MarkdownResult:
    reviewed_path = None
    stage = "Reviewed input selection"
    
    updated_directory = config.DATA_DIRECTORY / config.UPDATED_JSON_DIRECTORY_FORMAT.format(author_slug=author.slug)
    
    creation_date = datetime.now(ZoneInfo(config.DOWNLOAD_TIMEZONE)).strftime(config.FINAL_MARKDOWN_DATE_FORMAT)
    final_filename = config.FINAL_MARKDOWN_FILENAME_FORMAT.format(author_slug=author.slug, timestamp=creation_date)
    final_directory = config.DATA_DIRECTORY / config.FINAL_MARKDOWN_DIRECTORY_FORMAT.format(author_slug=author.slug)
    final_filepath = final_directory/final_filename
    
    try:    
        stage = f"Reviewed input selection ({updated_directory})"
        reviewed_path = _latest_review(updated_directory)
        
        if reviewed_path is None:
            return MarkdownResult(author.name, "skipped")
        
        stage = f"Reviewed JSON reading/validation ({reviewed_path})"
        publications = read_publications(reviewed_path)
        
        if not publications:
            stage = "Final Markdown removal"
            final_filepath.unlink(missing_ok=True)
            return MarkdownResult(author.name, "removed", markdown_path=final_filepath, reviewed_path=reviewed_path)
        
        stage = "Markdown generation"
        built = build_markdown(author, final_filepath, publications)
       
        if built.error is not None:
            return MarkdownResult(author.name, "failed", reviewed_path=reviewed_path, error=built.error)
        return MarkdownResult(author.name, "generated", len(publications), built.markdown_path, reviewed_path)
    except Exception as error:
        # Each author is an independent failure boundary; no fallback to older or unreviewed data.
        return MarkdownResult(author.name, "failed", reviewed_path=reviewed_path, error=f"{stage} failed: {error}")


def run_markdown(selection: Selection) -> list[MarkdownResult]:
    """Validate database selections before generating any author's Markdown."""
    authors = get_selected_authors(selection)
    return [_generate_markdown(author) for author in authors]
