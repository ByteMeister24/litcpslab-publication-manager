"""Retrieve ScienceDirect article metadata while preserving native JSON pages."""

from http.client import HTTPException
import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from helpers.author_builder import Author
from publication_collector.download_models import DownloadConfirmation, DownloadError
from publication_collector.source_downloaders.common import download_source


__all__ = ["download"]


SOURCE = "sciencedirect"
API_URL = "https://api.elsevier.com/content/metadata/article"
API_KEY_NAME = "SCIENCEDIRECT_API_KEY"
PAGE_SIZE = 25
REQUEST_TIMEOUT_SECONDS = 30


def download(author: Author) -> DownloadConfirmation | DownloadError:
    """Return a saved-download confirmation or a sanitized, stage-specific error."""
    return download_source(
        author,
        source=SOURCE,
        source_name="ScienceDirect",
        api_key_name=API_KEY_NAME,
        build_query=_build_query,
        download_pages=_download_pages,
        count_publications=_count_publications,
    )


def _count_publications(pages: list[dict]) -> int:
    return _record_count(pages[0])


def _build_query(author: Author) -> str:
    """Search the canonical author name and any configured affiliation."""
    if not author.name.strip() or not author.affiliations:
        raise ValueError("An author name and at least one affiliation are required.")
    for value in (author.name,) + author.affiliations:
        # Keep configured values literal rather than admitting query syntax.
        if not value.strip() or any(char in value for char in '"\\*?{}') or any(ord(char) < 32 for char in value):
            raise ValueError("Search names and affiliations must be non-empty literal text "
                             "without double quotes, backslashes, wildcards, braces, or control characters.")
    name_parts = author.name.split()
    name_queries = []
    # Full names have no surname boundary; retain each possible given/family split.
    for boundary in range(1, len(name_parts)):
        given_name = " ".join(name_parts[:boundary])
        surname = " ".join(name_parts[boundary:])
        name_queries.append(f'(authfirst("{given_name}") AND authlastname("{surname}"))')
    if not name_queries:
        name_queries.append(f'authlastname("{name_parts[0]}")')
    author_query = " OR ".join(name_queries)
    if len(name_queries) > 1:
        author_query = f"({author_query})"
    affiliations = " OR ".join(f'aff("{value}")' for value in author.affiliations)
    return f'{author_query} AND ({affiliations})'


def _fetch_page(api_key: str, query: str, start: int) -> dict:
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


def _record_count(page: dict) -> int:
    if not isinstance(page, dict):
        raise ValueError("ScienceDirect response must be a JSON object.")
    if any(page.get(key) for key in ("error", "errors", "error-response", "service-error")):
        raise ValueError("ScienceDirect returned an API error response.")
    results = page.get("search-results")
    if not isinstance(results, dict):
        raise ValueError("ScienceDirect response is missing search-results.")
    return _count(results.get("opensearch:totalResults"), "total result count")


def _download_pages(query: str, api_key: str) -> list[dict]:
    """Reject partial, changing, repeated, or incorrectly offset result sets."""
    pages = []
    identifiers = set()
    total = None
    retrieved = 0
    while total is None or retrieved < total:
        page = _fetch_page(api_key, query, retrieved)
        count = _record_count(page)
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


