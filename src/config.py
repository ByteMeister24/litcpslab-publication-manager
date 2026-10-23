"""Project-wide configuration; API settings belong to their source modules."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIRECTORY = PROJECT_ROOT / "data"
DATABASE_DIRECTORY = PROJECT_ROOT / "db"
AUTHORS_FILE = DATABASE_DIRECTORY / "authors.yaml"
ENV_FILE = PROJECT_ROOT / ".env"
REPORT_HTML_FILE = PROJECT_ROOT / "output" / "report.html"
REPORT_JSON_FILE = PROJECT_ROOT / "output" / "report.json"
CREDENTIAL_MODE_VARIABLE = "PUBLICATION_MANAGER_CREDENTIAL_MODE"

DOWNLOAD_TIMEZONE = "Europe/Vienna"
DOWNLOAD_TIMESTAMP_FORMAT = "%Y-%m-%dT%H-%M-%S.%f%z"
RAW_FILENAME_FORMAT = "{author}-{source}{sequence}-{timestamp}.json"
MARKDOWN_DATE_FORMAT = "%Y-%m-%d"
MARKDOWN_FILENAME_FORMAT = "{author}-{source}-{date}.md"
REPORT_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S %Z"

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
