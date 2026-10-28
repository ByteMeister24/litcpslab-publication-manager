"""Publication data contracts shared by conversion utilities."""

from dataclasses import dataclass


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
