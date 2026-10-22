"""Retrieve ScienceDirect article metadata while preserving native JSON pages."""

from datetime import date
from http.client import HTTPException
import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from dotenv import dotenv_values

import config
from author_builder import Author
from models import DownloadError, DownloadRecord, Publication
from utils import storage


SOURCE = "sciencedirect"
API_URL = "https://api.elsevier.com/content/metadata/article"
API_KEY_NAME = "SCIENCEDIRECT_API_KEY"
PAGE_SIZE = 25
REQUEST_TIMEOUT_SECONDS = 30


def download(author: Author) -> DownloadRecord | DownloadError:
    """Return a complete download or a sanitized, stage-specific error."""
    api_key = ""
    raw_file_path = None
    stage = "Download"
    try:
        if not config.ENV_FILE.is_file():
            raise ValueError(f"ScienceDirect credential file is missing: {config.ENV_FILE}.")
        try:
            settings = dotenv_values(config.ENV_FILE, interpolate=False)
        except Exception as error:
            raise ValueError(f"Cannot read ScienceDirect credential file ({type(error).__name__}).") from None
        api_key = (settings.get(API_KEY_NAME) or "").strip()
        if not api_key:
            raise ValueError(f"{API_KEY_NAME} is missing or empty in {config.ENV_FILE}.")

        pages = download_pages(build_query(author), api_key)
        stage = "Raw saving"
        raw_file_path = storage.save_raw(author.slug, SOURCE, pages)
        stage = "Normalization"
        publications = [normalize_article(article) for page in pages if record_count(page) > 0
                        for article in page["search-results"]["entry"]]
        return DownloadRecord(author=author.name, source=SOURCE, publication_count=len(publications),
                              publications=publications, raw_file_path=raw_file_path)
    except Exception as error:
        message = f"{stage} failed: {error}"
        if raw_file_path is not None:
            message += f"; raw saved: {raw_file_path}"
        if api_key:
            message = message.replace(api_key, "[REDACTED]")
        return DownloadError(author=author.name, source=SOURCE, error=message)


def build_query(author: Author) -> str:
    """Search the canonical author name and any configured affiliation."""
    if not author.name.strip() or not author.affiliations:
        raise ValueError("An author name and at least one affiliation are required.")
    for value in (author.name,) + author.affiliations:
        # Keep configured values literal rather than admitting query syntax.
        if not value.strip() or any(char in value for char in '"\\*?{}') or any(ord(char) < 32 for char in value):
            raise ValueError("Search names and affiliations must be non-empty literal text "
                             "without double quotes, backslashes, wildcards, braces, or control characters.")
    affiliations = " OR ".join(f'aff("{value}")' for value in author.affiliations)
    return f'authors("{author.name}") AND ({affiliations})'


def fetch_page(api_key: str, query: str, start: int) -> dict:
    """Send credentials only in a header; never expose HTTP response bodies."""
    parameters = {"query": query, "view": "COMPLETE", "start": start, "count": PAGE_SIZE}
    request = Request(API_URL + "?" + urlencode(parameters),
                      headers={"Accept": "application/json", "X-ELS-APIKey": api_key})
    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            return json.load(response)
    except HTTPError as error:
        error.close()
        raise RuntimeError(f"ScienceDirect returned HTTP {error.code} at offset {start}.") from None
    except (URLError, OSError, HTTPException) as error:
        raise RuntimeError(f"ScienceDirect request failed at offset {start} "
                           f"({type(error).__name__}).") from None
    except (ValueError, UnicodeError):
        raise ValueError(f"ScienceDirect returned invalid JSON at offset {start}.") from None


def _count(value, field: str) -> int:
    if isinstance(value, str) and value.isdecimal():
        value = int(value)
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"ScienceDirect response is missing a valid {field}.")
    return value


def record_count(page: dict) -> int:
    if not isinstance(page, dict):
        raise ValueError("ScienceDirect response must be a JSON object.")
    if any(page.get(key) for key in ("error", "errors", "error-response", "service-error")):
        raise ValueError("ScienceDirect returned an API error response.")
    results = page.get("search-results")
    if not isinstance(results, dict):
        raise ValueError("ScienceDirect response is missing search-results.")
    return _count(results.get("opensearch:totalResults"), "total result count")


def download_pages(query: str, api_key: str) -> list[dict]:
    """Reject partial, changing, repeated, or incorrectly offset result sets."""
    pages = []
    identifiers = set()
    total = None
    retrieved = 0
    while total is None or retrieved < total:
        page = fetch_page(api_key, query, retrieved)
        count = record_count(page)
        if total is None:
            total = count
        elif count != total:
            raise ValueError("ScienceDirect result count changed during retrieval; rerun the download.")

        results = page["search-results"]
        if _count(results.get("opensearch:startIndex"), "start index") != retrieved:
            raise ValueError("ScienceDirect returned an unexpected page offset.")
        articles = results.get("entry", [] if total == 0 else None)
        # Elsevier also represents an empty result set with this sentinel entry.
        if (total == 0 and isinstance(articles, list) and len(articles) == 1
                and isinstance(articles[0], dict) and articles[0].get("error") == "Result set was empty"):
            articles = []
        if not isinstance(articles, list) or len(articles) > PAGE_SIZE:
            raise ValueError("ScienceDirect response has an invalid entry list.")
        if retrieved + len(articles) > total or (not articles and retrieved < total):
            raise ValueError("ScienceDirect returned incomplete or inconsistent search results.")
        for article in articles:
            if not isinstance(article, dict) or article.get("error"):
                raise ValueError("ScienceDirect returned an invalid article entry.")
            identifier = article.get("pii")
            if not isinstance(identifier, str) or not identifier.strip():
                raise ValueError("ScienceDirect returned an article without a pii.")
            identifier = identifier.strip()
            if identifier in identifiers:
                raise ValueError("ScienceDirect repeated an article during pagination; rerun the download.")
            identifiers.add(identifier)
        retrieved += len(articles)
        pages.append(page)
    return pages


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


def normalize_article(article: dict) -> Publication:
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
