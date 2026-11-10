# Copyright (c) 2026 Mainak Majumder (@ByteMeister24)

"""Convert saved sciencedirect metadata into Publication instances."""

from datetime import date
from pathlib import Path

from publication_model import Publication
from publication_normalizer.source_normalizers.common import read_pages


def normalize_file(path: Path) -> list[Publication]:
    publications = []
    for page in read_pages(path):
        if any(page.get(key) for key in ("error", "errors", "error-response", "service-error")):
            raise ValueError("ScienceDirect page contains an API error.")
        results = page.get("search-results")
        if not isinstance(results, dict):
            raise ValueError("ScienceDirect page must contain a search-results object.")
        count = results.get("opensearch:totalResults")
        entries = results.get("entry")
        if count in (0, "0") and not isinstance(count, bool):
            if entries is None or (isinstance(entries, list) and len(entries) == 1
                                   and isinstance(entries[0], dict)
                                   and entries[0].get("error") == "Result set was empty"):
                entries = []
        if not isinstance(entries, list) or any(not isinstance(entry, dict) or entry.get("error") for entry in entries):
            raise ValueError("ScienceDirect page must contain an entry array of article objects.")
        publications.extend(_normalize_article(entry) for entry in entries)
    return publications


def _text(value, field: str) -> str:
    if isinstance(value, dict) and "$" in value:
        value = value["$"]
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    raise ValueError(f"ScienceDirect field {field} must be text or an integer.")

def _strings(value, field: str) -> tuple[str, ...]:
    values = value if isinstance(value, list) else [value]
    return tuple(text for item in values if (text := _text(item, field)))

def _normalize_article(article: dict) -> Publication:
    """Map Article Metadata fields, leaving fields absent from this API empty."""
    authors = article.get("authors")
    if authors is None:
        names = _strings(article.get("dc:creator"), "dc:creator")
    else:
        if not isinstance(authors, dict):
            raise ValueError("ScienceDirect authors must be an object.")
        entries = authors.get("author", [])
        if isinstance(entries, dict):
            entries = [entries]
        if not isinstance(entries, list) or any(not isinstance(author, dict) for author in entries):
            raise ValueError("ScienceDirect authors must contain author objects.")
        author_names = []
        for author in entries:
            given_name = _text(author.get("given-name"), "given-name")
            surname = _text(author.get("surname"), "surname")
            name = " ".join(part for part in (given_name, surname) if part)
            if name:
                author_names.append(name)
        names = tuple(author_names)

    dates = _strings(article.get("prism:coverDate"), "prism:coverDate")
    year = str(date.fromisoformat(dates[0]).year) if dates else ""
    keywords = tuple(keyword.strip() for text in _strings(article.get("authkeywords"), "authkeywords")
                     for keyword in text.split("|") if keyword.strip())
    # The metadata API's scidir/self links are article pages/API URLs, not PDF URLs.
    return Publication(
        title=_text(article.get("dc:title"), "dc:title"),
        authors=names,
        keywords=keywords,
        abstract=_text(article.get("dc:description"), "dc:description"),
        publication_title=_text(article.get("prism:publicationName"), "prism:publicationName"),
        year=year,
        issn="; ".join(_strings(article.get("prism:issn"), "prism:issn")),
        isbn="; ".join(_strings(article.get("prism:isbn"), "prism:isbn")),
        doi=_text(article.get("prism:doi"), "prism:doi"),
    )
