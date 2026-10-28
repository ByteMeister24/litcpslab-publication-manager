"""Shared comma-separated CLI selection parsing."""

from typing import Literal


Selection = tuple[str, ...] | Literal["all"]


def parse_selection(value: str, lowercase: bool = False) -> Selection:
    items = [item.strip() for item in value.split(",")]

    if lowercase:
        items = [item.lower() for item in items]

    if not all(items):
        raise ValueError("Selections must not contain empty comma-separated items.")

    items = list(dict.fromkeys(items))
    if "all" in items:
        if len(items) != 1:
            raise ValueError("all cannot be mixed with named selections.")
        return "all"

    return tuple(dict.fromkeys(items))
