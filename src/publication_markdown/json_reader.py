# Copyright (c) 2026 Mainak Majumder (@ByteMeister24)

"""Read and validate a complete reviewed dataset before rendering any records."""

from dataclasses import fields
import json
from pathlib import Path

from publication_model import Publication


STRING_ARRAY_FIELDS = {"authors", "affiliations", "keywords"}
PUBLICATION_FIELD_NAMES = {field.name for field in fields(Publication)}


def read_publications(path: Path) -> list[Publication]:
    with path.open(encoding="utf-8-sig") as stream:
        records = json.load(stream)
    if not isinstance(records, list):
        raise ValueError("Reviewed JSON must be an array of publication objects.")

    publications = []
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            raise ValueError(f"Record {index} must be a publication object.")
        unknown = record.keys() - PUBLICATION_FIELD_NAMES
        if unknown:
            raise ValueError(f"Record {index} has unknown fields: {', '.join(sorted(unknown))}.")
        values = {}
        for name, value in record.items():
            if name in STRING_ARRAY_FIELDS:
                if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
                    raise ValueError(f"Record {index}: {name} must be an array of strings.")
                values[name] = tuple(value)
            else:
                if not isinstance(value, str):
                    raise ValueError(f"Record {index}: {name} must be a string.")
                values[name] = value
        publications.append(Publication(**values))
    return publications
