"""Synthetic fixtures shared by offline pipeline tests."""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

AUTHOR_TEXT = """## Authors

- Ada Researcher
- René Researcher

## Common Affiliations

- University A
- Institute B

## Additional Affiliations

### René Researcher

- Former University
"""


def page(total, numbers):
    return {
        "total_records": total,
        "total_searched": 999,
        "articles": [{"article_number": str(number), "title": f"Work {number}"} for number in numbers],
    }


def full_article():
    """Representative synthetic JSON, including the nested IEEE metadata groups."""
    return {
        "article_number": "10",
        "title": "Über Research\nAcross Systems",
        "authors": {"authors": [
            {"full_name": "Second Author", "affiliation": "Institute B", "author_order": 2},
            {"full_name": "First Author", "affiliation": "University A", "author_order": 1},
        ]},
        "index_terms": {
            "author_terms": {"terms": ["Author keyword", "Second keyword"]},
            "ieee_terms": {"terms": ["IEEE term"]},
            "mesh_terms": {"terms": ["Not part of the agreed keyword groups"]},
        },
        "abstract": "An abstract.",
        "publication_title": "A Conference",
        "publication_year": 2026,
        "issn": "1234-5678",
        "isbn": "978-1-2345-6789-0",
        "doi": "10.example/work",
        "pdf_url": "https://example.invalid/work.pdf",
        "publisher": "IEEE",
        "unknown_native_field": {"preserve": True},
    }
