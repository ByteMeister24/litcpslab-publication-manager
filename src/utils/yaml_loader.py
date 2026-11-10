# Copyright (c) 2026 Mainak Majumder (@ByteMeister24)

import yaml
from pathlib import Path


class _UniqueAuthorLoader(yaml.SafeLoader):
    """Reject duplicate names instead of silently replacing earlier entries."""

    def construct_mapping(self, node, deep=False):
        if not isinstance(node, yaml.MappingNode):
            return super().construct_mapping(node, deep=deep)
        names = set()
        for key_node, _ in node.value:
            name = self.construct_object(key_node, deep=deep)
            
            if not isinstance(name, str):
                raise ValueError("Author names must be strings.")
            
            if name in names:
                raise ValueError(f"Repeated author name: {name!r} (line {key_node.start_mark.line + 1}).")
            names.add(name)
        
        return super().construct_mapping(node, deep=deep)

 # Parse the entire file; returns a dict with names as keys and affiliation list as values
def convert_yaml_to_dict(filepath:Path) -> dict[str, list[str]]: 
    try:
        with filepath.open(encoding="utf-8-sig") as stream:
            authors = yaml.load(stream, Loader=_UniqueAuthorLoader)
    except (yaml.YAMLError, ValueError) as error:
        raise ValueError(f"{filepath}: {error}") from None

    if not isinstance(authors, dict) or not authors:
        raise ValueError(f"{filepath}: Expected a nonempty mapping of author names to affiliation lists.")
    
    return authors