# Copyright (c) 2026 Mainak Majumder (@ByteMeister24)

"""Requests and outcomes for the publication download workflow."""

from dataclasses import dataclass
from pathlib import Path

from helpers.selection import Selection


@dataclass(frozen=True)
class DownloadRequest:
    authors: Selection
    sources: Selection


@dataclass(frozen=True)
class DownloadConfirmation:
    author: str
    source: str
    publication_count: int
    raw_file_path: Path


@dataclass(frozen=True)
class DownloadError:
    author: str
    source: str
    error: str
