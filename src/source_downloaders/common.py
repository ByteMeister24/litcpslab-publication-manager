"""Shared download workflow; publisher modules supply queries and record counts."""

from collections.abc import Callable
import os

from dotenv import dotenv_values

import config
from author_builder import Author
from models import DownloadConfirmation, DownloadError
from utils import storage


def _load_api_key(source_name: str, api_key_name: str) -> str:
    if os.environ.get(config.CREDENTIAL_MODE_VARIABLE) == "environment":
        api_key = os.environ.get(api_key_name, "").strip()
        if not api_key:
            raise ValueError(f"{api_key_name} is missing or empty in launcher credentials.")
        return api_key

    if not config.ENV_FILE.is_file():
        raise ValueError(f"{source_name} credential file is missing: {config.ENV_FILE}.")
    try:
        settings = dotenv_values(config.ENV_FILE, interpolate=False)
    except Exception as error:
        # Parser errors can contain credentials before a key is available for redaction.
        raise ValueError(f"Cannot read {source_name} credential file ({type(error).__name__}).") from None
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
    raw_file_path = None
    stage = "Download"
    try:
        api_key = _load_api_key(source_name, api_key_name)
        query = build_query(author)
        pages = download_pages(query, api_key)
        publication_count = count_publications(pages)

        stage = "Raw saving"
        raw_file_path = storage.save_raw(author.slug, source, pages)

        return DownloadConfirmation(author=author.name, source=source, publication_count=publication_count,
                                    raw_file_path=raw_file_path)
    except Exception as error:
        message = f"{stage} failed: {error}"
        if raw_file_path is not None:
            message += f"; raw saved: {raw_file_path}"
        if api_key:
            message = message.replace(api_key, "[REDACTED]")
        return DownloadError(author=author.name, source=source, error=message)
