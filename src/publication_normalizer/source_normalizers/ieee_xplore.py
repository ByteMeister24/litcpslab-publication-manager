# Copyright (c) 2026 Mainak Majumder (@ByteMeister24)

"""Convert saved ieee_xplore metadata into Publication instances."""

from pathlib import Path

from publication_model import Publication
from publication_normalizer.source_normalizers.common import read_pages


def normalize_file(path: Path) -> list[Publication]:
    publications = []
    for page in read_pages(path):
        if page.get("error") or page.get("errors"):
            raise ValueError("IEEE page contains an API error.")
        articles = page.get("articles")
        count = page.get("total_records", page.get("totalfound"))
        if articles is None and count in (0, "0") and not isinstance(count, bool):
            articles = []
        if not isinstance(articles, list) or any(not isinstance(article, dict) for article in articles):
            raise ValueError("IEEE page must contain an articles array of objects.")
        publications.extend(_normalize_article(article) for article in articles)
    return publications


def _text(value, field: str) -> str:
    if value is None:
        return ""

    if isinstance(value, str):
        return value.strip()

    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)

    raise ValueError(f"IEEE field {field} must be text or an integer.")

def _strings(value, field: str) -> tuple[str, ...]:
    if value is None:
        return ()

    values = value if isinstance(value, list) else [value]
    return tuple(text for item in values if (text := _text(item, field)))

def _normalize_article(article: dict) -> Publication:
    """Map IEEE's nested fields into the common, source-independent record."""
    authors = article.get("authors")

    if authors is None:
        authors = []

    if isinstance(authors, dict):
        authors = authors.get("authors", authors.get("author", []))

    if not isinstance(authors, list) or any(not isinstance(author, dict) for author in authors):
        raise ValueError("IEEE authors must contain a list of author objects.")

    if authors and all(author.get("author_order") is not None for author in authors):
        if any(isinstance(author["author_order"], bool)
               or not isinstance(author["author_order"], (str, int)) for author in authors):
            raise ValueError("IEEE author_order must be an integer.")
        try:
            authors = sorted(authors, key=lambda author: int(author["author_order"]))
        except (TypeError, ValueError, OverflowError):
            raise ValueError("IEEE author_order must be an integer.") from None

    names = tuple(name for author in authors if (name := _text(author.get("full_name"), "full_name")))
    affiliations = tuple(value for author in authors
                         for value in _strings(author.get("affiliation"), "affiliation"))
    index_terms = article.get("index_terms")

    if index_terms is None:
        index_terms = {}

    if not isinstance(index_terms, dict):
        raise ValueError("IEEE index_terms must be an object.")

    keywords = []
    for group in ("author_terms", "ieee_terms"):
        terms = index_terms.get(group)

        if terms is None:
            terms = []

        if isinstance(terms, dict):
            terms = terms.get("terms", [])
        keywords.extend(_strings(terms, group))

    return Publication(
        title=_text(article.get("title"), "title"),
        authors=names,
        affiliations=affiliations,
        keywords=tuple(keywords),
        abstract=_text(article.get("abstract"), "abstract"),
        publication_title=_text(article.get("publication_title"), "publication_title"),
        year=_text(article.get("publication_year"), "publication_year"),
        issn="; ".join(_strings(article.get("issn"), "issn")),
        isbn="; ".join(_strings(article.get("isbn"), "isbn")),
        doi=_text(article.get("doi"), "doi"),
        pdf_url=_text(article.get("pdf_url"), "pdf_url"),
        publisher=_text(article.get("publisher"), "publisher"),
    )
