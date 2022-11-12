from __future__ import annotations

import os
import pytest
import yaml
from skoufas_dbf_reader.utilities import all_entries
from skoufas_dbf_reader.field_extractors import *
from collections import defaultdict


@pytest.fixture
def reports_directory() -> str:
    r = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "reports"))
    os.makedirs(r, exist_ok=True)
    return r


def test_report_single_fields(reports_directory: str):
    field_values: list[set[str]] = [set() for _ in range(31)]
    for entry in all_entries():
        for i in range(1, 31):
            if i in entry and entry[i] and entry[i].strip():
                field_values[i].add(entry[i].strip())
    for i in range(1, 31):
        with open(os.path.join(reports_directory, f"fields_{i:02}.yml"), "w", encoding="utf-8") as outfile:
            yaml.dump(list(sorted(field_values[i])), outfile, default_flow_style=False, allow_unicode=True)


def test_report_single_extracted_fields(reports_directory: str):
    field_values: defaultdict[str, set[str]] = defaultdict(set[str])
    for entry in all_entries():
        author = author_part_from_a01(entry[1])
        if author:
            field_values["author"].add(author)
            if " " in author or "-" in author or author.count(",") != 1:
                field_values["weird_author"].add(author)
            else:
                field_values["plain_author"].add(author)
        language = language_from_a01(entry[1])
        if language:
            field_values["language"].add(language)
        title = title_from_a02(entry[2])
        if title:
            field_values["title"].add(title)
        subtitle = subtitle_from_a03(entry[3])
        if subtitle:
            field_values["subtitle"].add(subtitle)
        dewey = dewey_from_a04(entry[4])
        if dewey:
            field_values["dewey"].add(dewey)
    for k, values in field_values.items():
        with open(os.path.join(reports_directory, f"calculated_field_{k}.yml"), "w", encoding="utf-8") as outfile:
            yaml.dump(list(sorted(values)), outfile, default_flow_style=False, allow_unicode=True)


def test_report_entry_numbers(reports_directory: str):
    non_numeric: set[str] = set()
    all_entry_numbers: set[str] = set()
    duplicate_entry_numbers: set[str] = set()
    for entry in all_entries():
        if not entry[5]:
            continue
        entry_numbers = [number.strip() for number in entry[5].strip().split("-")]
        for n in entry_numbers:
            if n in all_entry_numbers:
                duplicate_entry_numbers.add(n)
            else:
                all_entry_numbers.add(n)
            if not n.isnumeric():
                non_numeric.add(n)
    with open(os.path.join(reports_directory, f"non_numeric_entry_numbers.yml"), "w", encoding="utf-8") as outfile:
        yaml.dump(list(sorted(non_numeric)), outfile, default_flow_style=False, allow_unicode=True)
    with open(os.path.join(reports_directory, f"duplicate_entry_numbers.yml"), "w", encoding="utf-8") as outfile:
        yaml.dump(list(sorted(duplicate_entry_numbers)), outfile, default_flow_style=False, allow_unicode=True)
