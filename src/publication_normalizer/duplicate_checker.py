"""Remove repeated publications using comparison keys without changing metadata."""

from publication_model import Publication

_DOI_RESOLVER_PREFIXES = (
    "https://doi.org/",
    "http://doi.org/",
    "https://dx.doi.org/",
    "http://dx.doi.org/",
)


def _doi_key(doi: str) -> str:
    key = doi.strip().casefold().removeprefix("doi:").strip()
    for prefix in _DOI_RESOLVER_PREFIXES:
        if key.startswith(prefix):
            return key.removeprefix(prefix).strip()
    return key


def _title_key(title: str) -> str:
    return " ".join(title.split()).casefold()


def remove_duplicates(publications: list[Publication]) -> list[Publication]:
    """Keep the first record for each DOI, with unambiguous title fallback.

    A title shared by distinct DOIs cannot identify a DOI-less record. Such
    records form a separate title group. Records without either key all survive.
    """
    dois_by_title: dict[str, set[str]] = {}
    for publication in publications:
        doi = _doi_key(publication.doi)
        title = _title_key(publication.title)
        if doi and title:
            dois_by_title.setdefault(title, set()).add(doi)

    cleaned = []
    seen: set[tuple[str, str]] = set()
    for publication in publications:
        doi = _doi_key(publication.doi)
        title = _title_key(publication.title)
        if not doi and title:
            matching_dois = dois_by_title.get(title, set())
            if len(matching_dois) == 1:
                doi = next(iter(matching_dois))

        if doi:
            identity = ("doi", doi)
        elif title:
            identity = ("title", title)
        else:
            cleaned.append(publication)
            continue

        if identity not in seen:
            seen.add(identity)
            cleaned.append(publication)

    return cleaned
