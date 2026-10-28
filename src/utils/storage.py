"""Publish completed raw downloads and Markdown without exposing partial writes."""
import os
from pathlib import Path
import tempfile

def save_file(filepath: Path, content: str, replace: bool) -> None:
    filepath.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n",
                                         dir=filepath.parent, prefix=f".{filepath.stem}-",
                                         suffix=".tmp", delete=False) as temporary:
            temporary_path = Path(temporary.name)
            temporary.write(content)
        if replace:
            os.replace(temporary_path, filepath)
        else:
            # Unlike rename, link atomically publishes without overwriting history.
            os.link(temporary_path, filepath)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()
    

