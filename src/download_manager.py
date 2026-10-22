"""Coordinate author/source downloads and Markdown builds without file writes."""
import ieee_xplore
from markdown_builder import build_markdown
from author_builder import get_selected_authors
from models import DownloadError, DownloadRecord, DownloadRequest, MarkdownBuildResult, Selection


SUPPORTED_SOURCES = ("ieee",)
DOWNLOADERS = {
    "ieee": ieee_xplore.download,
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


def run_download(request: DownloadRequest) -> tuple[list[DownloadRecord | DownloadError], list[MarkdownBuildResult]]:
    """Collect source records/errors and Markdown results for attempted builds.

    Failed downloads have no corresponding Markdown result. Each list retains
    processing order; records are identified by their author and source.
    """
    
    if not isinstance(request, DownloadRequest):
        raise ValueError("Expected DownloadRequest.")

    selected_authors = get_selected_authors(request.authors)
    selected_sources = _resolve_sources(request.sources)
    
    if any(source not in DOWNLOADERS for source in selected_sources):
        raise ValueError("The selected source is not supported.")

    download_results: list[DownloadRecord | DownloadError] = []
    markdown_results: list[MarkdownBuildResult] = []
    
    for author in selected_authors:
        for source in selected_sources:
            response = DOWNLOADERS[source](author)
            download_results.append(response)
            
            if isinstance(response, DownloadError):
                continue

            if response.publication_count == 0:
                continue

            build_report = build_markdown(author, source, response.publications)
            markdown_results.append(build_report)
    
    return download_results, markdown_results
