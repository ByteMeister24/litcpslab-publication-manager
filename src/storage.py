"""Publish completed raw downloads and Markdown without exposing partial writes."""

from datetime import datetime
import json
import os
from pathlib import Path
import tempfile
from zoneinfo import ZoneInfo

import config


def write_complete_file(destination: Path, content: str, replace: bool) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n",
                                         dir=destination.parent, prefix=f".{destination.stem}-",
                                         suffix=".tmp", delete=False) as temporary:
            temporary_path = Path(temporary.name)
            temporary.write(content)
        if replace:
            os.replace(temporary_path, destination)
        else:
            # Unlike rename, link atomically publishes without overwriting history.
            os.link(temporary_path, destination)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def save_raw(author_slug: str, source: str, pages: list[dict]) -> Path:
    content = json.dumps(pages, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    timestamp = datetime.now(ZoneInfo(config.DOWNLOAD_TIMEZONE)).strftime(config.DOWNLOAD_TIMESTAMP_FORMAT)
    raw_directory = config.DATA_DIRECTORY / author_slug / "raw"
    sequence = 1
    while True:
        destination = raw_directory / config.RAW_FILENAME_FORMAT.format(
            author=author_slug, source=source, timestamp=timestamp,
            sequence="" if sequence == 1 else f"-{sequence}",
        )
        try:
            write_complete_file(destination, content, replace=False)
            return destination
        except FileExistsError:
            if not destination.exists() and not destination.is_symlink():
                raise
            sequence += 1


def save_markdown(author_slug: str, source: str, markdown: str) -> Path:
    filename = config.MARKDOWN_FILENAME_FORMAT.format(author=author_slug, source=source)
    destination = config.DATA_DIRECTORY / author_slug / filename
    write_complete_file(destination, markdown, replace=True)
    return destination
