"""Run normalization with ``python -m publication_normalizer``."""

import sys

from publication_normalizer.cli.normalize_publications import main


if __name__ == "__main__":
    sys.exit(main())
