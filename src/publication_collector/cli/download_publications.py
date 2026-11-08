#!/usr/bin/env python3
"""CLI for downloading publication metadata."""

import argparse
import sys
from typing import Optional

from publication_collector.download_models import DownloadError, DownloadRequest
from publication_collector.download_manager import run_download
from helpers.selection import parse_selection


def parse_request(argv: Optional[list[str]] = None) -> DownloadRequest:
    parser = argparse.ArgumentParser(description="Download publication metadata.")
    parser.add_argument(
        "selection",
        nargs="?",
        choices=("all",),
        help="all authors and sources; exclusive with flags.",
    )
    parser.add_argument(
        "--author", help="Comma-separated full author names, or all. Omitted means all."
    )
    parser.add_argument(
        "--source", help="Comma-separated source keywords, or all. Omitted means all."
    )
    args = parser.parse_args(argv)

    if args.selection is not None:
        if args.author is not None or args.source is not None:
            parser.error(
                "Invalid arguments! all cannot be combined with --author or --source."
            )
        return DownloadRequest(authors="all", sources="all")

    if args.author is None and args.source is None:
        parser.error("Invalid arguments! provide all, --author, or --source.")

    try:
        return DownloadRequest(
            authors="all" if args.author is None else parse_selection(args.author),
            sources=(
                "all"
                if args.source is None
                else parse_selection(args.source, lowercase=True)
            ),
        )
    except ValueError as error:
        parser.error(str(error))


def main(argv: Optional[list[str]] = None) -> int:
    request = parse_request(argv)

    try:
        download_results = run_download(request)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    download_failures = 0
    for result in download_results:
        if isinstance(result, DownloadError):
            download_failures += 1
            print(
                f"Download failed: {result.author} [{result.source}]: {result.error}",
                file=sys.stderr,
            )
        else:
            print(
                f"Download completed: {result.author} [{result.source}]: {result.publication_count} publication(s); "
                f"download location: {result.raw_file_path}"
            )

    print(
        f"Download report: {len(download_results) - download_failures} succeeded; {download_failures} failed."
    )

    return 1 if download_failures else 0
