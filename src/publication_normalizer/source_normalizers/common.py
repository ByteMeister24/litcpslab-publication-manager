"""Read the native response-page arrays saved by the collector."""

import json
from pathlib import Path


def read_pages(path: Path) -> list[dict]:
    pages = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(pages, list) or not pages or any(not isinstance(page, dict) for page in pages):
        raise ValueError("Expected a nonempty JSON array of native response-page objects.")
    return pages
