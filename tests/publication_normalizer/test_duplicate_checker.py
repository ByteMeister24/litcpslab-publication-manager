# Copyright (c) 2026 Mainak Majumder (@ByteMeister24)

"""DOI identities, title fallback, ambiguity, and unchanged first records."""

from itertools import permutations
import unittest

from publication_model import Publication
from publication_normalizer.duplicate_checker import remove_duplicates


class DuplicateCheckerTests(unittest.TestCase):
    def test_empty_input_returns_a_new_empty_list(self):
        publications = []
        cleaned = remove_duplicates(publications)
        self.assertEqual(cleaned, [])
        self.assertIsNot(cleaned, publications)

    def test_doi_variants_match_despite_different_titles(self):
        first = Publication(title="Original title", doi=" 10.1000/Example ")
        variants = (
            "10.1000/example",
            "  10.1000/EXAMPLE\t",
            "DOI: 10.1000/Example",
            "https://doi.org/10.1000/example",
            "HTTP://DOI.ORG/10.1000/EXAMPLE",
            "https://dx.doi.org/10.1000/example",
            "http://dx.doi.org/10.1000/example",
            "doi: https://doi.org/10.1000/example",
        )
        for doi in variants:
            with self.subTest(doi=doi):
                self.assertEqual(remove_duplicates([first, Publication(title="Other title", doi=doi)]), [first])

    def test_title_comparison_ignores_case_and_collapses_whitespace(self):
        first = Publication(title="  Über  research\twith\nsystems  ")
        duplicate = Publication(title="ÜBER research with systems")
        self.assertEqual(remove_duplicates([first, duplicate]), [first])

    def test_title_punctuation_remains_significant(self):
        publications = [Publication(title="Research: systems"), Publication(title="Research systems")]
        self.assertEqual(remove_duplicates(publications), publications)

    def test_title_fallback_keeps_the_first_copy_with_or_without_a_doi(self):
        without_doi = Publication(title="Same title", authors=("First author",))
        with_doi = Publication(title="SAME TITLE", doi="10.1000/shared", abstract="Later abstract")
        for publications in ([without_doi, with_doi], [with_doi, without_doi]):
            with self.subTest(first_doi=publications[0].doi):
                cleaned = remove_duplicates(publications)
                self.assertEqual(cleaned, publications[:1])
                self.assertIs(cleaned[0], publications[0])

    def test_different_nonempty_dois_remain_distinct_despite_matching_titles(self):
        publications = [Publication(title="Same title", doi="10.1000/one"),
                        Publication(title="Same title", doi="10.1000/two")]
        self.assertEqual(remove_duplicates(publications), publications)

    def test_ambiguous_title_keeps_a_separate_doi_less_copy_in_any_order(self):
        records = (Publication(title="Same title"),
                   Publication(title="Same title", doi="10.1000/one"),
                   Publication(title="Same title", doi="10.1000/two"))
        for ordering in permutations(records):
            with self.subTest(dois=[record.doi for record in ordering]):
                publications = [*ordering, Publication(title=" SAME  TITLE ")]
                self.assertEqual(remove_duplicates(publications), list(ordering))

    def test_doi_variants_do_not_make_title_fallback_ambiguous(self):
        first = Publication(title="Same title")
        publications = [first, Publication(title="Same title", doi="10.1000/shared"),
                        Publication(title="SAME TITLE", doi="HTTPS://DOI.ORG/10.1000/SHARED")]
        self.assertEqual(remove_duplicates(publications), [first])

    def test_title_fallback_matches_title_variants_from_all_copies_of_a_doi(self):
        first = Publication(title="Original title", doi="10.1000/shared")
        publications = [first, Publication(title="Different title", doi="10.1000/shared"),
                        Publication(title="Different title"), Publication(title="Original title")]
        self.assertEqual(remove_duplicates(publications), [first])

    def test_records_without_doi_or_title_are_all_retained(self):
        publications = [Publication(), Publication(title=" \t", doi=" \n"), Publication()]
        self.assertEqual(remove_duplicates(publications), publications)

    def test_doi_alone_is_enough_to_remove_duplicates(self):
        first = Publication(doi="10.1000/shared")
        self.assertEqual(remove_duplicates([first, Publication(doi="10.1000/shared")]), [first])

    def test_retained_records_keep_their_order_and_metadata_without_mutating_input(self):
        first = Publication(title="  First title  ", doi="DOI:10.1000/FIRST", authors=("First author",))
        second = Publication(title="Second title")
        duplicate = Publication(title="Replacement title", doi="10.1000/first", abstract="Do not merge")
        third = Publication(title="Third title", doi="10.1000/third")
        publications = [first, second, duplicate, third]
        before = publications.copy()

        cleaned = remove_duplicates(publications)

        self.assertEqual(publications, before)
        self.assertIsNot(cleaned, publications)
        self.assertEqual(cleaned, [first, second, third])
        for retained, original in zip(cleaned, (first, second, third)):
            self.assertIs(retained, original)
        self.assertEqual(first.doi, "DOI:10.1000/FIRST")
        self.assertEqual(first.title, "  First title  ")
        self.assertEqual(first.abstract, "")
