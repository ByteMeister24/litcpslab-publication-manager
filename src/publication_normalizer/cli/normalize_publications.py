# Copyright (c) 2026 Mainak Majumder (@ByteMeister24)

"""Select database authors and report normalized JSON results in the console."""

import argparse
import logging
import sys

from publication_normalizer.normalization_manager import run_normalization
from helpers.selection import Selection, parse_selection


def parse_request(argv: list[str] | None = None) -> Selection:
    parser = argparse.ArgumentParser(
        description="Normalize saved publication lists into per-author JSON."
    )
    parser.add_argument(
        "selection",
        nargs="?",
        choices=("all",),
        help="All database authors; exclusive with --author.",
    )
    parser.add_argument("--author", help="Comma-separated full author names, or all.")
    args = parser.parse_args(argv)

    if args.selection is not None:
        if args.author is not None:
            parser.error("all cannot be combined with --author.")
        return "all"

    if args.author is None:
        parser.error("Provide all or --author.")

    try:
        return parse_selection(args.author)
    except ValueError as error:
        parser.error(str(error))


def main(argv: list[str] | None = None) -> int:
    selection = parse_request(argv)
    # Parser failures are reported with their input path through the results below.
    logging.getLogger("bibtexparser").addHandler(logging.NullHandler())
    try:
        results = run_normalization(selection)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    for result in results:
        for error in result.errors:
            print(f"Normalization error: {result.author}: {error}", file=sys.stderr)
        if result.status == "skipped":
            print(
                f"Normalization skipped: {result.author}: no publications to normalize."
            )
        elif result.normalized_path is not None:
            label = "partial" if result.status == "partial" else "completed"
            print(
                f"Normalization {label}: {result.author}: {result.publication_count} publication(s); "
                f"{result.duplicates_removed} duplicate(s) removed; "
                f"normalized: {result.normalized_path}"
            )
        else:
            print(
                f"Normalization failed: {result.author}; previous normalized file retained.",
                file=sys.stderr,
            )

    counts = {
        status: sum(result.status == status for result in results)
        for status in ("success", "partial", "failed", "skipped")
    }
    print(
        f"Normalization report: {counts['success']} succeeded; {counts['partial']} partial; "
        f"{counts['failed']} failed; {counts['skipped']} skipped."
    )
    return 1 if counts["partial"] or counts["failed"] else 0
