"""Coordinate author/source downloads and Markdown builds without file writes."""

import config
import ieee_xplore
from markdown_builder import build_markdown
from author_builder import load_authors
from models import DownloadError, DownloadRequest, DownloadResult, Selection


def _resolve_sources(source_selection: Selection) -> tuple[str, ...]:
    if source_selection == "all":
        return config.SUPPORTED_SOURCES
    
    if (not isinstance(source_selection, tuple) or not source_selection
            or any(not isinstance(item, str) or not item for item in source_selection)):
        raise ValueError("Expected source names or all.")
    
    unknown = set(source_selection) - set(config.SUPPORTED_SOURCES)
    if unknown:
        raise ValueError(f"Unknown source selection(s): {', '.join(sorted(unknown))}.")
    return tuple(dict.fromkeys(source_selection))


def run_download(request: DownloadRequest) -> list[DownloadResult]:
    
    if not isinstance(request, DownloadRequest):
        raise ValueError("Expected DownloadRequest.")

    authors = load_authors(request.authors)
    
    sources = _resolve_sources(request.sources)
    downloaders = {"ieee": ieee_xplore.download}
    
    if any(source not in downloaders for source in sources):
        raise ValueError("A configured source has no downloader.")

    results = []
    for author in authors:
        for source in sources:
            try:
                response = downloaders[source](author)
            except DownloadError as error:
                results.append(DownloadResult(author.name, source,
                                              raw_file_path=error.raw_file_path, error=str(error)))
                continue
            except (OSError, UnicodeError, ValueError, TypeError) as error:
                results.append(DownloadResult(author.name, source, error=f"Download failed: {error}"))
                continue

            build = build_markdown(author, source, response.publications)
            results.append(DownloadResult(
                author=author.name,
                source=source,
                publication_count=len(response.publications),
                raw_file_path=response.raw_file_path,
                markdown_path=build.markdown_path,
                error=build.error,
            ))
    return results
