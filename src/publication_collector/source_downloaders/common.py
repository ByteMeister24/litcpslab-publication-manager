"""Shared download workflow; publisher modules supply queries and record counts."""

from collections.abc import Callable
from datetime import datetime
import json
from zoneinfo import ZoneInfo

from dotenv import dotenv_values

import config
from helpers.author_builder import Author
from publication_collector.download_models import DownloadConfirmation, DownloadError
from utils import storage


def _load_api_key(source_name: str, api_key_name: str) -> str:
    if not config.ENV_FILE.is_file():
        raise ValueError(
            f"{source_name} credential file is missing: {config.ENV_FILE}."
        )
    try:
        settings = dotenv_values(config.ENV_FILE, interpolate=False)
    except Exception as error:
        # Parser errors can contain credentials before a key is available for redaction.
        raise ValueError(
            f"Cannot read {source_name} credential file ({type(error).__name__})."
        ) from None
    api_key = (settings.get(api_key_name) or "").strip()
    if not api_key:
        raise ValueError(f"{api_key_name} is missing or empty in {config.ENV_FILE}.")
    return api_key


def download_source(
    author: Author,
    *,
    source: str,
    source_name: str,
    api_key_name: str,
    build_query: Callable[[Author], str],
    download_pages: Callable[[str, str], list[dict]],
    count_publications: Callable[[list[dict]], int],
) -> DownloadConfirmation | DownloadError:
    """Save complete native pages and return a confirmation or sanitized error."""
    api_key = ""
    stage = "Download"
    try:
        api_key = _load_api_key(source_name, api_key_name)
        query = build_query(author)
        pages = download_pages(query, api_key)
        publication_count = count_publications(pages)

        stage = "Raw saving"
        content = (
            json.dumps(pages, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        )
        timestamp = datetime.now(ZoneInfo(config.DOWNLOAD_TIMEZONE)).strftime(
            config.DOWNLOAD_TIMESTAMP_FORMAT
        )
        download_directory = (
            config.DATA_DIRECTORY
            / config.DOWNLOAD_DIRECTORY_FORMAT.format(
                author_slug=author.slug,
                source=source,
            )
        )
        filepath = download_directory / config.DOWNLOAD_FILENAME_FORMAT.format(
            author_slug=author.slug, source=source, timestamp=timestamp
        )
        storage.save_file(filepath, content, replace=False)

        return DownloadConfirmation(
            author=author.name,
            source=source,
            publication_count=publication_count,
            raw_file_path=filepath,
        )
    except Exception as error:
        message = f"{stage} failed: {error}"
        if api_key:
            message = message.replace(api_key, "[REDACTED]")
        return DownloadError(author=author.name, source=source, error=message)
