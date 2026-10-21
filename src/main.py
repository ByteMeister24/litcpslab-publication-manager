#!/usr/bin/env python3
"""CLI for downloading publication metadata and generating Markdown."""

import argparse
import sys
from typing import Optional

from models import DownloadRequest, Selection
from download_manager import run_download


def parse_selection(value: str, lowercase: bool = False) -> Selection:
    items = [item.strip() for item in value.split(",")]
    
    if lowercase:
        items = [item.lower() for item in items]
    
    if not all(items):
        raise ValueError("Selections must not contain empty comma-separated items.")
    
    items = list(dict.fromkeys(items))
    if "all" in items:
        if len(items) != 1:
            raise ValueError("all cannot be mixed with named selections.")
        return "all"
    
    return tuple(dict.fromkeys(items))


def parse_request(argv: Optional[list[str]] = None) -> DownloadRequest:
    parser = argparse.ArgumentParser(description="Download metadata and generate publication Markdown.")
    parser.add_argument("selection", nargs="?", choices=("all",), help="all authors and sources; exclusive with flags.")
    parser.add_argument("--author", help="Comma-separated full author names, or all. Omitted means all.")
    parser.add_argument("--source", help="Comma-separated source keywords, or all. Omitted means all.")
    args = parser.parse_args(argv)
    
    if args.selection is not None:
        if args.author is not None or args.source is not None:
            parser.error("Invalid arguments! all cannot be combined with --author or --source.")
        return DownloadRequest(authors="all", sources="all")
    
    if args.author is None and args.source is None:
        parser.error("Invalid arguments! provide all, --author, or --source.")
    
    try:
        return DownloadRequest(
            authors="all" if args.author is None else parse_selection(args.author),
            sources="all" if args.source is None else parse_selection(args.source, lowercase=True),
        )
    except ValueError as error:
        parser.error(str(error))


def main(argv: Optional[list[str]] = None) -> int:
    request = parse_request(argv)
    
    try:
        results = run_download(request)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    failures = 0
    for result in results:
        if result.error is not None:
            failures += 1
            saved = f"; raw saved: {result.raw_file_path}" if result.raw_file_path is not None else ""
            print(f"Failed: {result.author} [{result.source}]: {result.error}{saved}", file=sys.stderr)
        else:
            print(f"Completed: {result.author} [{result.source}]: {result.publication_count} publication(s); "
                  f"raw: {result.raw_file_path}; Markdown: {result.markdown_path}")
    print(f"Download report: {len(results) - failures} succeeded; {failures} failed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
