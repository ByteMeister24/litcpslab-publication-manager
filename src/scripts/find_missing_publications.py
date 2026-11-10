#!/usr/bin/env python3
# Copyright (c) 2026 Mainak Majumder (@ByteMeister24)

"""List ODT citations whose titles are absent from normalized publication JSON."""

import argparse
from collections.abc import Iterator
from dataclasses import dataclass
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
from zipfile import BadZipFile, ZipFile

from utils.storage import save_file

OFFICE_NAMESPACE = "{urn:oasis:names:tc:opendocument:xmlns:office:1.0}"
TEXT_NAMESPACE = "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}"
EXCLUDED_TEXT_ELEMENTS = {
    TEXT_NAMESPACE + "h",
    TEXT_NAMESPACE + "note",
    TEXT_NAMESPACE + "tracked-changes",
    OFFICE_NAMESPACE + "annotation",
}


@dataclass(frozen=True)
class Citation:
    title: str
    text: str


@dataclass(frozen=True)
class ComparisonResult:
    extracted_count: int
    matched_count: int
    missing_count: int
    output_path: Path


def _body_paragraphs(element: ET.Element) -> Iterator[ET.Element]:
    for child in element:
        if child.tag == TEXT_NAMESPACE + "p":
            yield child
        elif child.tag not in EXCLUDED_TEXT_ELEMENTS:
            yield from _body_paragraphs(child)


def _inline_text(element: ET.Element) -> str:
    if element.tag in EXCLUDED_TEXT_ELEMENTS:
        return ""
    if element.tag == TEXT_NAMESPACE + "s":
        count = int(element.get(TEXT_NAMESPACE + "c", "1"))
        if count < 1:
            raise ValueError("ODT space counts must be positive integers.")
        return " " * count
    if element.tag in (TEXT_NAMESPACE + "tab", TEXT_NAMESPACE + "line-break"):
        return " "

    parts = [element.text or ""]
    for child in element:
        parts.append(_inline_text(child))
        parts.append(child.tail or "")
    return "".join(parts)


def read_odt_citations(path: Path) -> list[Citation]:
    try:
        with ZipFile(path) as archive:
            root = ET.fromstring(archive.read("content.xml"))
    except (BadZipFile, KeyError, RuntimeError, ET.ParseError) as error:
        raise ValueError(f"Invalid ODT {path}: {error}") from error

    body = root.find(f"{OFFICE_NAMESPACE}body/{OFFICE_NAMESPACE}text")
    if body is None:
        raise ValueError(f"Invalid ODT {path}: missing document text body.")

    citations = []
    for index, paragraph in enumerate(_body_paragraphs(body), start=1):
        try:
            text = " ".join(_inline_text(paragraph).split())
        except ValueError as error:
            raise ValueError(f"{path}: paragraph {index}: {error}") from error
        _, colon, after_colon = text.partition(":")
        if not colon:
            continue

        # Deliberately use the first period, including for comma-delimited venues.
        title, period, _ = after_colon.partition(".")
        title = title.strip()
        if not period or not title:
            raise ValueError(
                f"{path}: paragraph {index}: expected a nonblank title "
                "between the first colon and the next period."
            )
        citations.append(Citation(title, text))

    if not citations:
        raise ValueError(f"{path}: no publication entries found.")
    return citations


def _title_key(title: str) -> str:
    return " ".join(title.split()).casefold()


def read_normalized_titles(path: Path) -> set[str]:
    with path.open(encoding="utf-8-sig") as stream:
        records = json.load(stream)
    if not isinstance(records, list):
        raise ValueError(
            f"{path}: normalized JSON must be an array of publication objects."
        )

    titles = set()
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            raise ValueError(f"{path}: record {index} must be a publication object.")
        title = record.get("title")
        if not isinstance(title, str) or not title.strip():
            raise ValueError(
                f"{path}: record {index} must have a nonblank string title."
            )
        titles.add(_title_key(title))
    return titles


def compare_publications(
    odt_path: Path, normalized_path: Path, output_path: Path
) -> ComparisonResult:
    if output_path.resolve() in (odt_path.resolve(), normalized_path.resolve()):
        raise ValueError("The output path must differ from both input paths.")

    citations = read_odt_citations(odt_path)
    normalized_titles = read_normalized_titles(normalized_path)
    missing = [
        citation
        for citation in citations
        if _title_key(citation.title) not in normalized_titles
    ]
    content = "\n\n".join(citation.text for citation in missing)
    if missing:
        content += "\n"
    save_file(output_path, content, replace=True)
    return ComparisonResult(
        len(citations), len(citations) - len(missing), len(missing), output_path
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Save ODT citations whose titles are missing from normalized JSON."
    )
    parser.add_argument("--odt", type=Path, required=True, help="ODT publication list.")
    parser.add_argument(
        "--normalized", type=Path, required=True, help="Normalized publication JSON."
    )
    parser.add_argument(
        "--output", type=Path, required=True, help="Missing-citation text report."
    )
    args = parser.parse_args(argv)

    try:
        result = compare_publications(args.odt, args.normalized, args.output)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(
        f"Extracted: {result.extracted_count}; matched: {result.matched_count}; "
        f"missing: {result.missing_count}"
    )
    print(f"Report: {result.output_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
