# Copyright (c) 2026 Mainak Majumder (@ByteMeister24)

"""Load the complete YAML author mapping into Author dataclasses."""

from dataclasses import dataclass
import config
from utils.yaml_loader import convert_yaml_to_dict
from helpers.selection import Selection

@dataclass(frozen=True)
class Author:
    name: str
    affiliations: tuple[str, ...]

    @property
    def slug(self) -> str:
        return self.name.lower().replace(" ", "-")

def _load_author_list() -> list[Author]:
    author_file_path = config.AUTHORS_FILE
    author_list = convert_yaml_to_dict(author_file_path)
    authors = []
    
    for name, affiliations in author_list.items():
            
        if not name.strip() or any(ord(character) < 32 for character in name):
            raise ValueError(f"{author_file_path}: Author names must be non-empty text without control characters.")
            
        if not isinstance(affiliations, list) or not affiliations:
            raise ValueError(f"{author_file_path}: {name!r} needs a non-empty list of affiliations.")
            
        if any(not isinstance(value, str) or not value.strip()
                or any(ord(character) < 32 for character in value) for value in affiliations):
            raise ValueError(f"{author_file_path}: Affiliations for {name!r} must be non-empty strings without control characters.")
            
        author = Author(name=name, affiliations=tuple(affiliations))
        authors.append(author)
    
    return authors
            
           
def get_selected_authors(author_selection: Selection) -> list[Author]:
    author_list = _load_author_list()
    
    if author_selection == "all":
        return author_list
       
    if (not isinstance(author_selection, tuple) or not author_selection
            or any(not isinstance(name, str) or not name for name in author_selection)):
        raise ValueError("Expected author names or all.")
    
    authors_by_name = {author.name.casefold(): author for author in author_list}
    
    if len(authors_by_name) != len(author_list):
        raise ValueError("Author selection is ambiguous: database names must be unique regardless of capitalization.")

    unknown = {name 
               for name in author_selection 
               if name.casefold() not in authors_by_name}
    
    if unknown:
        raise ValueError(f"Unknown author selection(s): {', '.join(sorted(unknown))}.")
    
    return [authors_by_name[name] for name in dict.fromkeys(name.casefold() for name in author_selection)]
