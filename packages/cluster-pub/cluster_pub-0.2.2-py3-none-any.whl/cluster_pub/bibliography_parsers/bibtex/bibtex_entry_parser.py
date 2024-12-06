from typing import Dict


def parse_bibtex_entry(bibtex_entry: Dict) -> Dict:

    parsed_bibtex_entry = {
        "title": bibtex_entry.get("title"),
        "abstract": bibtex_entry.get("abstract"),
        "book_title": bibtex_entry.get("booktitle"),
    }

    return parsed_bibtex_entry
