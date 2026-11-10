# Copyright (c) 2026 Mainak Majumder (@ByteMeister24)

"""Read filesystem creation timestamps."""

from datetime import datetime
from pathlib import Path
import subprocess


def get_creation_timestamp(path: Path) -> float:
    """Return the file's creation time as seconds since the Unix epoch."""
    timestamp = getattr(path.stat(), "st_birthtime", None)
    if timestamp is not None:
        return timestamp

    # Linux's os.stat() omits birth time; GNU stat exposes it when supported.
    try:
        result = subprocess.run(
            ["stat", "--dereference", "--format=%w", "--", str(path)],
            capture_output=True, text=True, check=True,
        )
    except subprocess.CalledProcessError as error:
        raise OSError(f"Cannot read creation timestamp for {path}: {error.stderr.strip()}") from error

    creation_time = result.stdout.strip()
    if creation_time == "-":
        raise ValueError(f"Creation timestamp unavailable for {path}.")
    return datetime.fromisoformat(creation_time).timestamp()
