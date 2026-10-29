"""Select saved inputs, normalize them, and publish one combined file per author."""

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Literal

import config
from helpers.author_builder import Author, get_selected_authors
from publication_normalizer.source_normalizers import acm, ieee_xplore, sciencedirect, springer
from utils import storage
from utils.file_timestamps import get_creation_timestamp
from helpers.selection import Selection


@dataclass(frozen=True)
class NormalizationResult:
    author: str
    status: Literal["success", "partial", "failed", "skipped"]
    publication_count: int = 0
    normalized_path: Path | None = None
    errors: tuple[str, ...] = ()


# Registry order is the order of publications in the combined output.
SOURCE_NORMALIZERS = (
    ("ieee", (".json",), ieee_xplore.normalize_file),
    ("sciencedirect", (".json",), sciencedirect.normalize_file),
    ("springer", (".csv",), springer.normalize_file),
    ("acm", (".bib", ".bibtex"), acm.normalize_file),
)


def _select_file(directory: Path, extensions: tuple[str, ...]) -> Path | None:
    if not directory.exists():
        return None
    
    if not directory.is_dir():
        raise ValueError("Raw source path must be a directory.")
    
    files = sorted(path for path in directory.iterdir()
                   if path.is_file() and path.suffix.lower() in extensions)
    
    if not files:
        return None
    
    return max(files, key=get_creation_timestamp)


def _normalize_publications(author: Author) -> NormalizationResult:
    publications = []
    errors = []

    normalized_directory = config.DATA_DIRECTORY / "normalized"
    normalized_filename = config.NORMALIZED_FILENAME_FORMAT.format(author_slug=author.slug)
    normalized_filepath = normalized_directory / normalized_filename
    
    for source, extensions, normalize_file in SOURCE_NORMALIZERS:
        download_directory = config.DATA_DIRECTORY / config.DOWNLOAD_DIRECTORY_FORMAT.format(
            author_slug=author.slug, source=source,
        )
        try:
            source_file = _select_file(download_directory, extensions)
        except (OSError, ValueError) as error:
            errors.append(f"{download_directory}: {error}")
            continue
        
        if source_file is None:
            continue

        try:
            converted = normalize_file(source_file)
        except Exception as error:
            # A file is the failure boundary; never keep its partly converted rows.
            errors.append(f"{source_file}: {type(error).__name__}: {error}")
            continue

        publications.extend(converted)

    if not publications:
        return NormalizationResult(author.name, "failed" if errors else "skipped", errors=tuple(errors))

    try:
        content = json.dumps([asdict(publication) for publication in publications],
                             ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        storage.save_file(normalized_filepath, content, replace=True)
    except (OSError, UnicodeError, ValueError, TypeError) as error:
        errors.append(f"Normalized saving failed: {error}")
        return NormalizationResult(author.name, "failed", errors=tuple(errors))
    return NormalizationResult(
        author.name, "partial" if errors else "success", len(publications), normalized_filepath, tuple(errors),
    )


def run_normalization(selection: Selection) -> list[NormalizationResult]:
    """Validate all selected authors before processing any of their saved inputs."""
    authors = get_selected_authors(selection)
    return [_normalize_publications(author) for author in authors]
