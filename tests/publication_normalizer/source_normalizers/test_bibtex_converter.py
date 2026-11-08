"""Offline tests for ACM BibTeX normalization."""

from contextlib import redirect_stderr, redirect_stdout
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tests import support
from publication_normalizer.source_normalizers.acm import normalize_file
from publication_model import Publication


class BibtexConverterTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.directory = Path(directory.name)
        self.input_path = self.directory / "publications.bib"

    def write_bibtex(self, content: str) -> Path:
        self.input_path.write_text(content, encoding="utf-8")
        return self.input_path

    def test_complete_entry_maps_to_existing_publication_dataclass(self):
        self.write_bibtex(r'''
@article{complete,
    title = {A {Protected} Title},
    author = {Smith, Ada and Doe, Ren{\'e}},
    affiliation = {University A; Institute B},
    keywords = {systems, testing, , verification},
    abstract = {A \textit{useful} abstract.},
    journal = {A Journal},
    booktitle = {A Conference},
    year = {2026},
    issn = {1234-5678},
    isbn = {978-1-2345-6789-0},
    doi = {10.example/a_b},
    url = {https://example.invalid/a_b?value=10%25&other={keep}},
    publisher = {Association for Computing Machinery},
    pages = {1--10}
}
''')
        publications = normalize_file(self.input_path)
        self.assertEqual(publications, [Publication(
            title="A Protected Title",
            authors=("Smith, Ada", "Doe, René"),
            affiliations=("University A; Institute B",),
            keywords=("systems", "testing", "verification"),
            abstract="A useful abstract.",
            publication_title="A Journal",
            year="2026",
            issn="1234-5678",
            isbn="978-1-2345-6789-0",
            doi="10.example/a_b",
            pdf_url="https://example.invalid/a_b?value=10%25&other={keep}",
            publisher="Association for Computing Machinery",
        )])

    def test_multiple_entries_keep_file_order_and_missing_field_defaults(self):
        self.write_bibtex('''
@inproceedings{z, title={First}, booktitle={A Conference}}
@article{a, title={Second}}
@misc{untitled}
''')
        self.assertEqual(normalize_file(self.input_path), [
            Publication(title="First", publication_title="A Conference"),
            Publication(title="Second"),
            Publication(),
        ])

    def test_blank_journal_falls_back_to_booktitle(self):
        self.write_bibtex('@inproceedings{k, journal={ }, booktitle={A Conference}}')
        self.assertEqual(normalize_file(self.input_path), [Publication(publication_title="A Conference")])

    def test_authors_split_before_decoding_protected_names(self):
        self.write_bibtex(r'''
@article{k,
    author = {M{\"u}ller, Anna and {Research and Development Group} AND de la Cruz, Jr., Juan}
}
''')
        self.assertEqual(normalize_file(self.input_path)[0].authors, (
            "Müller, Anna", "Research and Development Group", "de la Cruz, Jr., Juan",
        ))

    def test_nested_braces_accents_and_math_are_decoded_as_text(self):
        self.write_bibtex(r'''
@article{k,
    title = {{An {\textbf{Important}}} Study},
    abstract = {Gr{\"o}{\ss}e, caf{\'e}, and $x_{i}$.},
    affiliation = {Universit{\"a}t A},
    keywords = {\textit{control}, {systems}},
    publisher = {Research \& Development}
}
''')
        self.assertEqual(normalize_file(self.input_path), [Publication(
            title="An Important Study",
            abstract="Größe, café, and $x_{i}$.",
            affiliations=("Universität A",),
            keywords=("control", "systems"),
            publisher="Research & Development",
        )])

    def test_utf8_bom_and_uppercase_field_names_are_supported(self):
        self.write_bibtex('\ufeff@ARTICLE{k, TITLE={Über Research}, AUTHOR={Ada and René}, YEAR=2026}')
        self.assertEqual(normalize_file(self.input_path), [
            Publication(title="Über Research", authors=("Ada", "René"), year="2026"),
        ])

    def test_strings_are_resolved_and_comments_and_preambles_are_not_publications(self):
        self.write_bibtex('''
@string{venue = "A Journal"}
@comment{Comment only}
@preamble{"A preamble"}
@article{k, title="A Title", journal=venue}
''')
        self.assertEqual(normalize_file(self.input_path), [
            Publication(title="A Title", publication_title="A Journal"),
        ])

    def test_empty_or_comment_only_files_return_empty_lists(self):
        for content in ("", " \n\t", "@comment{Nothing to convert}"):
            with self.subTest(content=content):
                self.write_bibtex(content)
                self.assertEqual(normalize_file(self.input_path), [])

    def test_unexpanded_string_concatenation_raises_instead_of_returning_incorrect_text(self):
        for content in (
            '@article{k, title="A " # "Title"}',
            '@string{title = "A " # "Title"}\n@article{k, title=title}',
        ):
            with self.subTest(content=content):
                self.write_bibtex(content)
                with self.assertRaisesRegex(ValueError, "Entry 'k'.*concatenation.*unsupported"):
                    normalize_file(self.input_path)

    def test_literal_hashes_and_url_fragments_are_preserved(self):
        self.write_bibtex('@article{k, title={A # Title}, url={https://example.invalid/a#part}}')
        self.assertEqual(normalize_file(self.input_path), [
            Publication(title="A # Title", pdf_url="https://example.invalid/a#part"),
        ])

    def test_malformed_entry_rejects_the_whole_conversion(self):
        self.write_bibtex('@article{valid, title={Valid}}\n@article{broken, title={Never closed}')
        with self.assertLogs("bibtexparser", level="WARNING"), \
             self.assertRaisesRegex(ValueError, "parsing failed at line 2.*end of file"):
            normalize_file(self.input_path)

    def test_duplicate_entries_and_fields_are_rejected(self):
        cases = (
            ('@article{k, title={A}}\n@article{k, title={B}}', "Duplicate entry key"),
            ('@article{k, title={A}, title={B}}', "Duplicate field keys"),
            ('@article{k, title={A}, TITLE={B}}', "duplicate field"),
        )
        for content, message in cases:
            with self.subTest(content=content):
                self.write_bibtex(content)
                with self.assertRaisesRegex(ValueError, message):
                    normalize_file(self.input_path)

    def test_missing_unreadable_and_invalid_utf8_files_raise(self):
        with self.assertRaises(FileNotFoundError):
            normalize_file(self.input_path)
        with patch.object(Path, "read_text", side_effect=PermissionError("Access denied")):
            with self.assertRaises(PermissionError):
                normalize_file(self.input_path)
        self.input_path.write_bytes(b"\xff")
        with self.assertRaises(UnicodeError):
            normalize_file(self.input_path)

    def test_conversion_is_silent_and_does_not_write_files(self):
        content = '@article{k, title={A Title}}'
        self.write_bibtex(content)
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            publications = normalize_file(self.input_path)
        self.assertEqual(publications, [Publication(title="A Title")])
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(self.input_path.read_text(encoding="utf-8"), content)
        self.assertEqual(list(self.directory.iterdir()), [self.input_path])
