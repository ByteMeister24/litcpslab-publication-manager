# Copyright (c) 2026 Mainak Majumder (@ByteMeister24)

"""Map a manually exported Springer Nature search-results CSV to Publication."""

import csv
from pathlib import Path

from publication_model import Publication


REQUIRED_COLUMNS = ("Item Title", "Publication Title", "Item DOI", "Authors", "Publication Year", "URL")


def normalize_file(path: Path) -> list[Publication]:
    publications = []
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, strict=True)
        try:
            if reader.fieldnames is None:
                raise ValueError("Springer CSV is empty or has no header row.")
            reader.fieldnames = [name.strip() for name in reader.fieldnames]
            if len(reader.fieldnames) != len(set(reader.fieldnames)):
                raise ValueError("Springer CSV contains duplicate column headers.")
            missing = set(REQUIRED_COLUMNS) - set(reader.fieldnames)
            if missing:
                raise ValueError("Springer CSV is missing column(s): " + ", ".join(sorted(missing)))

            for row in reader:
                if None in row:
                    raise ValueError(f"Springer CSV record ending at line {reader.line_num} has extra values.")
                if not any(value and value.strip() for value in row.values()):
                    continue
                publications.append(_normalize_row(row))
        except csv.Error as error:
            raise ValueError(f"Invalid Springer CSV near line {reader.line_num}: {error}") from None
    return publications


def _normalize_row(row: dict[str, str | None]) -> Publication:
    def text(column: str) -> str:
        return (row.get(column) or "").strip()

    return Publication(
        title=text("Item Title"),
        publication_title=text("Publication Title"),
        doi=text("Item DOI"),
        authors=tuple(name.strip() for name in text("Authors").split(",") if name.strip()),
        year=text("Publication Year"),
        # The agreed mapping retains the supplied Springer page URL in this field.
        pdf_url=text("URL"),
    )
