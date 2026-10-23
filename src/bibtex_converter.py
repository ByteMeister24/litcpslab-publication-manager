"""Convert a BibTeX file into the project's Publication instances."""

import argparse
import logging
from pathlib import Path
import sys

import bibtexparser
from bibtexparser.middlewares.names import split_multiple_persons_names
from bibtexparser.model import Entry
from pylatexenc.latex2text import LatexNodes2Text

from models import Publication


def convert_bibtex(input_path: Path) -> list[Publication]:
    """Read all entries in file order, raising on parsing or conversion errors."""
    library = bibtexparser.parse_string(input_path.read_text(encoding="utf-8-sig"))
    if library.failed_blocks:
        failed = library.failed_blocks[0]
        location = f" at line {failed.start_line + 1}" if failed.start_line is not None else ""
        reason = str(failed.error) or getattr(failed.error, "abort_reason", "Invalid BibTeX")
        raise ValueError(f"{input_path}: BibTeX parsing failed{location}: {reason}")

    decoder = LatexNodes2Text(math_mode="verbatim")
    return [_entry_to_publication(entry, decoder) for entry in library.entries]


def _entry_to_publication(entry: Entry, decoder: LatexNodes2Text) -> Publication:
    fields = {}
    for field in entry.fields:
        key = field.key.lower()
        if key in fields:
            raise ValueError(f"Entry {entry.key!r}: duplicate field {key!r}.")
        fields[key] = field

    def value(key: str) -> str:
        field = fields.get(key)
        if field is None:
            return ""
        # The pinned parser retains concatenation expressions without expanding them.
        if field.enclosing == "no-enclosing" and "#" in field.value:
            raise ValueError(f"Entry {entry.key!r}: BibTeX string concatenation in {key!r} is unsupported.")
        return field.value.strip()

    def text(key: str) -> str:
        return decoder.latex_to_text(value(key)).strip()

    # Decode after splitting so braces still protect names containing 'and'.
    authors = tuple(
        decoder.latex_to_text(name).strip()
        for name in split_multiple_persons_names(value("author"))
    )
    affiliation = text("affiliation")
    keywords = tuple(keyword.strip() for keyword in text("keywords").split(",") if keyword.strip())

    return Publication(
        title=text("title"),
        authors=authors,
        affiliations=(affiliation,) if affiliation else (),
        keywords=keywords,
        abstract=text("abstract"),
        publication_title=text("journal") or text("booktitle"),
        year=text("year"),
        issn=text("issn"),
        isbn=text("isbn"),
        doi=value("doi"),
        # URLs are identifiers, so LaTeX decoding could change their contents.
        pdf_url=value("url"),
        publisher=text("publisher"),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert BibTeX entries to Publication instances.")
    parser.add_argument("input_path", type=Path, help="Path to the input BibTeX file.")
    args = parser.parse_args()

    # Report parser failures through the single console error below.
    logging.getLogger("bibtexparser").addHandler(logging.NullHandler())
    try:
        publications = convert_bibtex(args.input_path)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Converted {len(publications)} publication(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
