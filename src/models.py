"""Small data contracts shared by the CLI, middleware, and source modules."""

from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Optional, Union

from author_builder import Author


Selection = Union[tuple[str, ...], Literal["all"]]


@dataclass(frozen=True)
class DownloadRequest:
    authors: Selection
    sources: Selection


@dataclass(frozen=True)
class Publication:
    title: str = ""
    authors: tuple[str, ...] = ()
    affiliations: tuple[str, ...] = ()
    keywords: tuple[str, ...] = ()
    abstract: str = ""
    publication_title: str = ""
    year: str = ""
    issn: str = ""
    isbn: str = ""
    doi: str = ""
    pdf_url: str = ""
    publisher: str = ""


@dataclass(frozen=True)
class DownloadRecord:
    author: str
    source: str
    publication_count: int
    publications: list[Publication]
    raw_file_path: Path


@dataclass(frozen=True)
class DownloadError:
    author: str
    source: str
    error: str


@dataclass(frozen=True)
class MarkdownBuildResult:
    author: str
    source: str
    markdown_path: Optional[Path] = None
    error: Optional[str] = None
