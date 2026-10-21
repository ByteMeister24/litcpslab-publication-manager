"""Small data contracts shared by the CLI, middleware, and source modules."""

from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Optional, Union


Selection = Union[tuple[str, ...], Literal["all"]]


@dataclass(frozen=True)
class Author:
    name: str
    affiliations: tuple[str, ...]

    @property
    def slug(self) -> str:
        return self.name.lower().replace(" ", "-")


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
class SourceDownload:
    publications: list[Publication]
    raw_file_path: Path


@dataclass(frozen=True)
class MarkdownBuildResult:
    markdown_path: Optional[Path] = None
    error: Optional[str] = None


@dataclass(frozen=True)
class DownloadResult:
    author: str
    source: str
    publication_count: Optional[int] = None
    raw_file_path: Optional[Path] = None
    markdown_path: Optional[Path] = None
    error: Optional[str] = None


class DownloadError(Exception):
    """A safe source error, optionally identifying a saved raw download."""

    def __init__(self, message: str, raw_file_path: Optional[Path] = None):
        super().__init__(message)
        self.raw_file_path = raw_file_path
