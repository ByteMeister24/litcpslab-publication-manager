"""Selection, partial results, immutable raw inputs, and atomic normalized output."""

from dataclasses import asdict
import csv
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from support import AUTHOR_YAML, page
import config
from publication_model import Publication
from publication_normalizer.normalization_manager import run_normalization
from publication_normalizer.source_normalizers.springer import REQUIRED_COLUMNS
from helpers.author_builder import Author
from publication_collector.download_models import DownloadConfirmation
from publication_collector.source_downloaders.common import download_source


class NormalizationManagerTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.data = self.root / "data"
        self.creation_times: dict[Path, float] = {}
        timestamps = patch("publication_normalizer.normalization_manager.get_creation_timestamp",
                           side_effect=self.creation_times.__getitem__)
        timestamps.start()
        self.addCleanup(timestamps.stop)
        authors = self.root / "authors.yaml"
        authors.write_text(AUTHOR_YAML, encoding="utf-8")
        for setting, value in (("AUTHORS_FILE", authors), ("DATA_DIRECTORY", self.data),
                               ("ENV_FILE", self.root / "must-not-read.env")):
            context = patch.object(config, setting, value)
            context.start()
            self.addCleanup(context.stop)
        guard = patch("urllib.request.urlopen", side_effect=AssertionError("Normalization must not access HTTP"))
        self.http = guard.start()
        self.addCleanup(guard.stop)

    def source_file(self, source, filename, content, slug="ada-researcher"):
        path = config.DATA_DIRECTORY / slug / "download" / source / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        self.creation_times.setdefault(path, float(len(self.creation_times) + 1))
        return path

    def api_file(self, source="ieee", payload=None, timestamp="2026-10-27T14-30-00.000000+0100",
                 slug="ada-researcher"):
        if payload is None:
            payload = [page(1, [1])]
        filename = f"{slug}-{source}-{timestamp}.json"
        return self.source_file(source, filename, json.dumps(payload, ensure_ascii=False), slug)

    def springer_file(self, slug="ada-researcher", title="Springer"):
        path = self.source_file("springer", "SearchResults.csv", "", slug)
        with path.open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=REQUIRED_COLUMNS)
            writer.writeheader()
            writer.writerow({"Item Title": title, "Authors": "Ada Researcher, René Researcher"})
        return path

    def normalized_file(self, slug="ada-researcher", name="Ada Researcher"):
        return self.data / slug / "normalized" / f"{name}-publications.json"

    def existing_output(self, content="Previous normalized JSON"):
        path = self.normalized_file()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def read_result(self, result):
        return json.loads(result.normalized_path.read_text(encoding="utf-8"))

    def test_four_sources_combined_in_order_with_exact_dataclass_fields(self):
        self.api_file(payload=[{"articles": [{"title": "Same title", "authors": {"authors": [
            {"full_name": "Another Author"}]}}]}])
        self.api_file("sciencedirect", [{"search-results": {"entry": [{"dc:title": "ScienceDirect"}]}}])
        self.springer_file(title="Same title")
        self.source_file("acm", "export.BIB", '@article{one,title={Über ACM}}')
        raw_files = {path: path.read_bytes() for path in self.data.rglob("*") if path.is_file()}
        result = run_normalization(("ADA RESEARCHER", "ada researcher"))[0]
        self.assertEqual(result.status, "success")
        self.assertEqual(result.author, "Ada Researcher")
        self.assertEqual(result.publication_count, 4)
        self.assertEqual(result.normalized_path, self.normalized_file())
        records = self.read_result(result)
        self.assertEqual([record["title"] for record in records],
                         ["Same title", "ScienceDirect", "Same title", "Über ACM"])
        for record in records:
            self.assertEqual(set(record), set(asdict(Publication())))
            for field in ("authors", "affiliations", "keywords"):
                self.assertIsInstance(record[field], list)
        self.assertEqual(records[0]["authors"], ["Another Author"])
        self.assertIn("Über", result.normalized_path.read_text(encoding="utf-8"))
        self.assertEqual({path: path.read_bytes() for path in raw_files}, raw_files)
        self.http.assert_not_called()
        self.assertFalse(config.ENV_FILE.exists())

    def test_download_and_normalization_use_the_configured_download_directory(self):
        with patch.object(config, "DOWNLOAD_DIRECTORY_FORMAT", "{source}/incoming/{author_slug}"):
            with patch("publication_collector.source_downloaders.common._load_api_key", return_value="test-key"):
                confirmation = download_source(
                    Author("Ada Researcher", ("University A",)),
                    source="ieee", source_name="IEEE", api_key_name="IEEE_API_KEY",
                    build_query=lambda author: "query", download_pages=lambda query, key: [page(1, [1])],
                    count_publications=lambda pages: 1,
                )
            self.assertIsInstance(confirmation, DownloadConfirmation)
            download = confirmation.raw_file_path
            self.creation_times[download] = 1.0
            self.assertEqual(download.parent, self.data / "ieee" / "incoming" / "ada-researcher")
            result = run_normalization(("Ada Researcher",))[0]
        self.assertEqual((result.status, result.publication_count), ("success", 1))
        self.assertEqual(len(self.read_result(result)), 1)

    def test_latest_api_uses_creation_time_instead_of_filename_or_modification_time(self):
        old = self.api_file(payload=[{"articles": [{"title": "Old"}]}],
                            timestamp="2099-10-26T14-30-00.000000+0100")
        new = self.api_file(payload=[{"articles": [{"title": "Latest"}]}],
                            timestamp="2000-10-26T14-30-00.000000+0100")
        os.utime(old, (2000000000, 2000000000))
        os.utime(new, (1000000000, 1000000000))
        self.assertEqual(self.read_result(run_normalization("all")[0])[0]["title"], "Latest")

    def test_latest_created_file_is_selected_for_every_source_format(self):
        cases = (
            ("ieee", "old.json", "new.JSON", json.dumps([{"articles": [{"title": "Latest"}]}])),
            ("sciencedirect", "old.json", "new.JSON", json.dumps([
                {"search-results": {"entry": [{"dc:title": "Latest"}]}}
            ])),
            ("springer", "old.csv", "new.CSV",
             "Item Title,Publication Title,Item DOI,Authors,Publication Year,URL\nLatest,,,,,\n"),
            ("acm", "old.bib", "new.BIBTEX", '@article{latest,title={Latest}}'),
        )
        for source, older_name, latest_name, content in cases:
            with self.subTest(source=source), tempfile.TemporaryDirectory() as directory, \
                    patch.object(config, "DATA_DIRECTORY", Path(directory)):
                self.source_file(source, older_name, "Invalid older contents must be ignored")
                self.source_file(source, latest_name, content)
                result = run_normalization(("Ada Researcher",))[0]
                self.assertEqual((result.status, result.publication_count), ("success", 1))
                self.assertEqual(self.read_result(result)[0]["title"], "Latest")

    def test_malformed_latest_does_not_fall_back_and_other_sources_are_saved(self):
        self.api_file(timestamp="2026-10-26T14-30-00.000000+0100")
        latest = self.api_file()
        latest.write_text("invalid JSON", encoding="utf-8")
        self.springer_file()
        result = run_normalization(("Ada Researcher",))[0]
        self.assertEqual((result.status, result.publication_count), ("partial", 1))
        self.assertEqual(self.read_result(result)[0]["title"], "Springer")
        self.assertIn(str(latest), result.errors[0])

    def test_unavailable_creation_time_is_reported_and_other_sources_are_saved(self):
        unavailable = self.api_file()
        self.springer_file()

        def creation_timestamp(path):
            if path == unavailable:
                raise ValueError("Creation timestamp unavailable.")
            return self.creation_times[path]

        with patch("publication_normalizer.normalization_manager.get_creation_timestamp",
                   side_effect=creation_timestamp):
            result = run_normalization(("Ada Researcher",))[0]
        self.assertEqual((result.status, result.publication_count), ("partial", 1))
        self.assertEqual(self.read_result(result)[0]["title"], "Springer")
        self.assertIn(str(unavailable.parent), result.errors[0])
        self.assertIn("Creation timestamp unavailable", result.errors[0])

    def test_missing_supported_inputs_and_legacy_layout_skip_without_replacing_output(self):
        previous = self.existing_output()
        legacy = self.data / "ada-researcher" / "download" / "older-ieee.json"
        legacy.parent.mkdir()
        legacy.write_text(json.dumps([page(1, [1])]), encoding="utf-8")
        self.source_file("springer", "notes.txt", "unsupported")
        results = run_normalization("all")
        self.assertEqual([result.status for result in results], ["skipped", "skipped"])
        self.assertEqual(previous.read_text(), "Previous normalized JSON")
        self.assertFalse((self.data / "rené-researcher").exists())

    def test_successful_zero_result_file_replaces_existing_output_with_empty_array(self):
        previous = self.existing_output()
        self.api_file(payload=[page(0, [])])
        result = run_normalization(("Ada Researcher",))[0]
        self.assertEqual((result.status, result.publication_count), ("success", 0))
        self.assertEqual(json.loads(previous.read_text()), [])

    def test_all_failed_inputs_preserve_previous_json_and_continue_other_authors(self):
        previous = self.existing_output()
        malformed = self.api_file()
        malformed.write_text("not JSON", encoding="utf-8")
        self.source_file("springer", "broken.csv", "Wrong header\nvalue\n")
        self.springer_file(slug="rené-researcher")
        results = run_normalization("all")
        self.assertEqual([result.status for result in results], ["failed", "success"])
        self.assertEqual(previous.read_text(), "Previous normalized JSON")
        self.assertEqual(results[1].normalized_path.name, "René Researcher-publications.json")
        self.assertEqual(len(results[0].errors), 2)

    def test_error_in_one_article_discards_all_records_from_that_file(self):
        self.api_file(payload=[{"articles": [{"title": "Must be discarded"}, {"authors": "invalid"}]}])
        self.springer_file()
        result = run_normalization(("Ada Researcher",))[0]
        self.assertEqual(result.status, "partial")
        self.assertEqual([record["title"] for record in self.read_result(result)], ["Springer"])

    def test_successful_empty_file_plus_failed_file_saves_empty_partial_result(self):
        self.existing_output()
        self.api_file(payload=[page(0, [])])
        self.source_file("acm", "invalid.bib", '@article{unterminated, title={broken')
        with self.assertLogs("bibtexparser", level="WARNING"):
            result = run_normalization(("Ada Researcher",))[0]
        self.assertEqual((result.status, result.publication_count), ("partial", 0))
        self.assertEqual(self.read_result(result), [])

    def test_reruns_replace_instead_of_append_and_are_deterministic(self):
        self.springer_file()
        first = run_normalization(("Ada Researcher",))[0]
        original = first.normalized_path.read_bytes()
        second = run_normalization(("Ada Researcher",))[0]
        self.assertEqual(second.publication_count, 1)
        self.assertEqual(second.normalized_path.read_bytes(), original)

    def test_api_filename_without_embedded_timestamp_is_accepted(self):
        self.source_file("ieee", "unknown.json", json.dumps([page(1, [1])]))
        result = run_normalization(("Ada Researcher",))[0]
        self.assertEqual((result.status, result.publication_count), ("success", 1))
        self.assertEqual(result.errors, ())

    def test_save_failure_preserves_previous_file_cleans_temporary_files_and_continues(self):
        previous = self.existing_output()
        self.springer_file()
        self.springer_file(slug="rené-researcher")
        replace = os.replace

        def fail_first(source, destination):
            if destination == previous:
                raise OSError("disk full")
            return replace(source, destination)

        with patch("utils.storage.os.replace", side_effect=fail_first):
            results = run_normalization("all")
        self.assertEqual([result.status for result in results], ["failed", "success"])
        self.assertEqual(previous.read_text(), "Previous normalized JSON")
        self.assertEqual(list(previous.parent.iterdir()), [previous])
        self.assertIn("disk full", results[0].errors[-1])

    def test_unknown_authors_fail_before_normalizing_any_inputs(self):
        with patch("publication_normalizer.normalization_manager._normalize_publications") as normalize:
            with self.assertRaises(ValueError):
                run_normalization(("Ada Researcher", "Unknown"))
        normalize.assert_not_called()

    def test_explicit_author_order_and_case_duplicates_follow_database_spelling(self):
        self.springer_file()
        self.springer_file(slug="rené-researcher")
        results = run_normalization(("RENÉ RESEARCHER", "ada researcher", "René Researcher"))
        self.assertEqual([result.author for result in results], ["René Researcher", "Ada Researcher"])
