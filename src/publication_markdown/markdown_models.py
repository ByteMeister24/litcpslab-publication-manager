# Copyright (c) 2026 Mainak Majumder (@ByteMeister24)

"""Builder and per-author workflow outcomes."""

from dataclasses import dataclass
from pathlib import Path
from typing import Literal


@dataclass(frozen=True)
class MarkdownBuildResult:
    author: str
    markdown_path: Path | None = None
    error: str | None = None


@dataclass(frozen=True)
class MarkdownResult:
    author: str
    status: Literal["generated", "removed", "skipped", "failed"]
    publication_count: int = 0
    markdown_path: Path | None = None
    reviewed_path: Path | None = None
    error: str | None = None
