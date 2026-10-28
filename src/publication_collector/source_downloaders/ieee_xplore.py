"""Retrieve complete IEEE Xplore metadata while keeping native response pages."""

from http.client import HTTPException
import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from helpers.author_builder import Author
from publication_collector.download_models import DownloadConfirmation, DownloadError
from publication_collector.source_downloaders.common import download_source


__all__ = ["download"]


SOURCE = "ieee"
API_URL = "https://ieeexploreapi.ieee.org/api/v1/search/articles"
PAGE_SIZE = 200
REQUEST_TIMEOUT_SECONDS = 30
API_KEY_NAME = "IEEE_API_KEY"


def download(author: Author) -> DownloadConfirmation | DownloadError:
    """Return a saved-download confirmation or a sanitized, stage-specific error."""
    return download_source(
        author,
        source=SOURCE,
        source_name="IEEE",
        api_key_name=API_KEY_NAME,
        build_query=_build_query,
        download_pages=_download_pages,
        count_publications=_count_publications,
    )


def _count_publications(pages: list[dict]) -> int:
    return _record_count(pages[0])


def _build_query(author: Author) -> str:
    """Constrain the full author name and every affiliation to their own fields."""
    if not author.name.strip() or not author.affiliations:
        raise ValueError("An author name and at least one affiliation are required.")
    
    for value in (author.name,) + author.affiliations:
        # IEEE does not document escaping embedded quotation marks in phrases.
        if not value.strip() or any(char in value for char in '"\\*?') or any(ord(char) < 32 for char in value):
            raise ValueError("Search names and affiliations must be non-empty literal text "
                                "without double quotes, backslashes, wildcards, or control characters.")
    
    affiliations = " OR ".join(f'"Author Affiliations":"{value}"' for value in author.affiliations)
    
    return f'"Authors":"{author.name}" AND ({affiliations})'


def _fetch_page(api_key: str, query: str, start_record: int) -> dict:
    """Keep the credential-bearing URL out of errors and persisted metadata."""
    parameters = {
        "apikey": api_key,
        "format": "json",
        "querytext": query,
        "start_record": start_record,
        "max_records": PAGE_SIZE,
        # Stable ordering prevents relevance ties from shuffling between pages.
        "sort_field": "article_number",
        "sort_order": "asc",
    }
    request = Request(API_URL + "?" + urlencode(parameters), headers={"Accept": "application/json"})
    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            return json.load(response)
    except HTTPError as error:
        error.close()
        raise RuntimeError(f"IEEE returned HTTP {error.code} at record {start_record}.") from None
    except (URLError, OSError, HTTPException) as error:
        # Exception messages can include the full URL; expose only the error type.
        raise RuntimeError(f"IEEE request failed at record {start_record} "
                            f"({type(error).__name__}).") from None
    except (ValueError, UnicodeError):
        raise ValueError(f"IEEE returned invalid JSON at record {start_record}.") from None


def _record_count(page: dict) -> int:
    """Accept the JSON count and the totalfound name in IEEE's field reference."""
    if not isinstance(page, dict):
        raise ValueError("IEEE response must be a JSON object.")
    if page.get("error") or page.get("errors"):
        raise ValueError("IEEE returned an API error response.")
    value = page.get("total_records", page.get("totalfound"))
    if isinstance(value, str) and value.isdecimal():
        value = int(value)
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError("IEEE response is missing a valid total record count.")
    return value


def _download_pages(query: str, api_key: str) -> list[dict]:
    """Fail on incomplete or inconsistent pagination instead of saving a subset."""
    pages = []
    article_numbers = set()
    total = None
    retrieved = 0

    while total is None or retrieved < total:
        page = _fetch_page(api_key, query, retrieved + 1)
        count = _record_count(page)
        
        if total is None:
            total = count
        elif count != total:
            raise ValueError("IEEE result count changed during retrieval; rerun the download.")

        articles = page.get("articles", [] if total == 0 else None)
        
        if not isinstance(articles, list) or len(articles) > PAGE_SIZE:
            raise ValueError("IEEE response has an invalid articles list.")
        
        if retrieved + len(articles) > total or (not articles and retrieved < total):
            raise ValueError("IEEE returned incomplete or inconsistent search results.")
        
        for article in articles:
            number = article.get("article_number") if isinstance(article, dict) else None
            
            if isinstance(number, int) and not isinstance(number, bool) and number > 0:
                number = str(number)
            
            if not isinstance(number, str) or not number.strip():
                raise ValueError("IEEE returned an article without an article_number.")
            
            if number in article_numbers:
                raise ValueError("IEEE repeated an article during pagination; rerun the download.")
            
            article_numbers.add(number)

        retrieved += len(articles)
        pages.append(page)
    
    return pages
