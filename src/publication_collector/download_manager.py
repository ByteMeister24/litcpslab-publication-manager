"""Coordinate author/source downloads without file writes."""
from helpers.author_builder import get_selected_authors
from helpers.selection import Selection
from publication_collector.download_models import DownloadConfirmation, DownloadError, DownloadRequest
from publication_collector.source_downloaders import ieee_xplore, sciencedirect


SUPPORTED_SOURCES = ("ieee", "sciencedirect")
DOWNLOADERS = {
    "ieee": ieee_xplore.download,
    "sciencedirect": sciencedirect.download,
}

def _resolve_sources(source_selection: Selection) -> tuple[str, ...]:
    if source_selection == "all":
        return SUPPORTED_SOURCES
    
    if (not isinstance(source_selection, tuple) or not source_selection
            or any(not isinstance(item, str) or not item for item in source_selection)):
        raise ValueError("Expected source names or all.")
    
    unknown = set(source_selection) - set(SUPPORTED_SOURCES)
    
    if unknown:
        raise ValueError(f"Unknown source selection(s): {', '.join(sorted(unknown))}.")
    
    return tuple(dict.fromkeys(source_selection))


def run_download(request: DownloadRequest) -> list[DownloadConfirmation | DownloadError]:
    """Collect source confirmations/errors in author and source processing order."""
    
    if not isinstance(request, DownloadRequest):
        raise ValueError("Expected DownloadRequest.")

    selected_authors = get_selected_authors(request.authors)
    selected_sources = _resolve_sources(request.sources)
    
    if any(source not in DOWNLOADERS for source in selected_sources):
        raise ValueError("The selected source is not supported.")

    download_results: list[DownloadConfirmation | DownloadError] = []
    
    for author in selected_authors:
        for source in selected_sources:
            response = DOWNLOADERS[source](author)
            download_results.append(response)
    
    return download_results
