"""Project-wide configuration; API settings belong to their source modules."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIRECTORY = PROJECT_ROOT / "data"
AUTHORS_FILE = DATA_DIRECTORY / "authors.md"
ENV_FILE = PROJECT_ROOT / ".env"

AUTHOR_SECTIONS = ("Authors", "Common Affiliations", "Additional Affiliations")
SUPPORTED_SOURCES = ("ieee",)
MARKDOWN_PRESET = "commonmark"
DOWNLOAD_TIMEZONE = "Europe/Vienna"
DOWNLOAD_TIMESTAMP_FORMAT = "%Y-%m-%dT%H-%M-%S.%f%z"
RAW_FILENAME_FORMAT = "{author}-{source}{sequence}-{timestamp}.json"
MARKDOWN_FILENAME_FORMAT = "{author}-{source}.md"

# Markdown label and common Publication attribute, in schema order.
PUBLICATION_FIELDS = (
    ("Authors", "authors"),
    ("Author Affiliations", "affiliations"),
    ("Keywords", "keywords"),
    ("Abstract", "abstract"),
    ("Publication", "publication_title"),
    ("Year", "year"),
    ("ISSN", "issn"),
    ("ISBN", "isbn"),
    ("DOI", "doi"),
    ("Link", "pdf_url"),
    ("Publisher", "publisher"),
)
