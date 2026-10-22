"""Store download counts in JSON and synchronize the member HTML tables."""

from datetime import datetime
import json
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo

import config
from utils import storage


def _validate_counts(counts_by_author: dict[str, dict[str, int]]) -> None:
    if not isinstance(counts_by_author, dict):
        raise ValueError("Report counts must be an object keyed by author name.")
    for author, counts in counts_by_author.items():
        if not isinstance(author, str) or not author.strip() or author == "updated_at":
            raise ValueError("Report author names must be nonempty strings other than updated_at.")
        if not isinstance(counts, dict):
            raise ValueError(f"Report counts for {author!r} must be an object keyed by source.")
        for source, count in counts.items():
            if not isinstance(source, str) or not source.strip():
                raise ValueError("Report source names must be nonempty strings.")
            if type(count) is not int or count < 0:
                raise ValueError(f"Publication count for {author!r} [{source}] must be a nonnegative integer.")


def _read_report_data() -> tuple[dict[str, dict[str, int]], datetime]:
    try:
        data = json.loads(config.REPORT_JSON_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"Cannot parse report JSON: {error}") from None
    if not isinstance(data, dict):
        raise ValueError("Report JSON must be an object.")
    timestamp = data.pop("updated_at", None)
    if not isinstance(timestamp, str):
        raise ValueError("Report JSON is missing its updated_at timestamp.")
    try:
        updated_at = datetime.fromisoformat(timestamp)
    except ValueError:
        raise ValueError("Report updated_at must be an ISO datetime with a timezone.") from None
    if updated_at.utcoffset() is None:
        raise ValueError("Report updated_at must include a timezone.")
    _validate_counts(data)
    return data, updated_at


def update_download_counts(counts_by_author: dict[str, dict[str, int]]) -> list[str]:
    """Merge successful download counts, retaining previous values on decreases."""
    _validate_counts(counts_by_author)
    saved_counts, _ = _read_report_data()
    warnings = []
    for author, counts in counts_by_author.items():
        if author not in saved_counts:
            raise ValueError(f"Author {author!r} is not listed in the report JSON.")
        for source, count in counts.items():
            previous_count = saved_counts[author].get(source)
            if previous_count is not None and count < previous_count:
                warnings.append(f"Publication count decreased for {author} [{source}]: "
                                f"{previous_count} to {count}; keeping {previous_count}.")
            else:
                saved_counts[author][source] = count

    now = datetime.now(ZoneInfo(config.DOWNLOAD_TIMEZONE))
    data = {"updated_at": now.isoformat(timespec="seconds"), **saved_counts}
    content = json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    storage.write_complete_file(config.REPORT_JSON_FILE, content, replace=True)
    return warnings


def update_report() -> None:
    """Render saved JSON counts and its timestamp into the existing member tables."""
    counts_by_author, updated_at = _read_report_data()
    try:
        tree = ET.parse(config.REPORT_HTML_FILE)
    except ET.ParseError as error:
        raise ValueError(f"Cannot parse report HTML: {error}") from None

    root = tree.getroot()
    tables = root.findall(".//table")
    rows = [row for table in tables for row in table.findall("./tbody/tr")]
    if {row.get("data-author") for row in rows} != set(counts_by_author):
        raise ValueError("Report JSON authors must match the HTML member tables.")
    updated = root.find(".//time[@id='last-updated']")
    if updated is None:
        raise ValueError("Report HTML is missing its last-updated timestamp.")
    sources = list(dict.fromkeys(source for counts in counts_by_author.values() for source in counts))

    for table in tables:
        header = table.find("./thead/tr")
        if header is None:
            raise ValueError("Report HTML is missing a table header.")
        columns = [column.attrib["data-source"] for column in header.findall("th[@data-source]")]
        for source in sources:
            if source not in columns:
                ET.SubElement(header, "th", {"scope": "col", "data-source": source}).text = source.upper()
                columns.append(source)
        for row in table.findall("./tbody/tr"):
            author_counts = counts_by_author[row.attrib["data-author"]]
            for source in columns:
                cell = next((cell for cell in row.findall("td") if cell.get("data-source") == source), None)
                if cell is None:
                    cell = ET.SubElement(row, "td", {"data-source": source})
                cell.text = str(author_counts[source]) if source in author_counts else ""
                cell.attrib.pop("class", None)
                for notice in list(cell):
                    cell.remove(notice)

    updated_at = updated_at.astimezone(ZoneInfo(config.DOWNLOAD_TIMEZONE))
    updated.text = updated_at.strftime(config.REPORT_DATETIME_FORMAT)
    updated.set("datetime", updated_at.isoformat(timespec="seconds"))
    ET.indent(tree, space="  ")
    # Explicit closing tags keep the external script valid when opened as HTML.
    document = "<!DOCTYPE html>\n" + ET.tostring(root, encoding="unicode", short_empty_elements=False) + "\n"
    storage.write_complete_file(config.REPORT_HTML_FILE, document, replace=True)
