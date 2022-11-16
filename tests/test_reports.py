from __future__ import annotations

import os
import pytest
import yaml
from skoufas_dbf_reader.utilities import all_entries, romanize
from skoufas_dbf_reader.field_extractors import *
from collections import defaultdict


@pytest.fixture
def reports_directory() -> str:
    r = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "reports"))
    os.makedirs(r, exist_ok=True)
    return r


def minimal_entry(input_entry: dict[int, str], fields: list[int]) -> dict[int, str]:
    return {i: input_entry[i] for i in fields}


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
    field_values: defaultdict[str, list[str | list[str]]] = defaultdict(list)
    for entry in all_entries():
        author = author_part_from_a01(entry[1])
        if author:
            field_values["author"].append(author)
            if " " in author or "-" in author or author.count(",") != 1:
                field_values["weird_author"].append(author)
            else:
                field_values["plain_author"].append(author)
        language = language_from_a01(entry[1])
        if language:
            field_values["language"].append(language)
        title = title_from_a02(entry[2])
        if title:
            field_values["title"].append(title)
        subtitle = subtitle_from_a03(entry[3])
        if subtitle:
            field_values["subtitle"].append(subtitle)
        dewey = dewey_from_a04(entry[4])
        if dewey:
            field_values["dewey"].append(dewey)
        entry_numbers = entry_numbers_from_a05_a06_a07_a08(entry[5], entry[6], entry[7], entry[8])
        field_values["entry_number_lists"].append(entry_numbers)
        for entry_number in entry_numbers:
            field_values["entry_numbers"].append(entry_number)
        translator = translator_from_a06(entry[6])
        if translator:
            translators = translator.split("!!")
            for single_translator in translators:
                field_values["translator"].append(single_translator)
                translator_surname_name = single_translator.split(",", maxsplit=1)
                if len(translator_surname_name) == 2:
                    field_values["translator_family_name"].append(translator_surname_name[0])
                    if translator_surname_name[1].endswith("."):
                        field_values["translator_name_abbreviations"].append(translator_surname_name[1])
                    else:
                        field_values["translator_names"].append(translator_surname_name[1])
        edition = edition_from_a07(entry[7])
        if edition:
            field_values["edition"].append(edition)
        editor = editor_from_a08_a09(entry[8], entry[9])
        if editor:
            if not editor[0] or not editor[1]:
                field_values["editor"].append(f"{editor[0]} // {editor[1]} ({entry[0]})")
            else:
                field_values["editor"].append(f"{editor[0]} // {editor[1]}")
        edition_year = edition_year_from_a09_a10(entry[9], entry[10])
        if edition_year:
            field_values["edition_year"].append(str(edition_year))
        pages = pages_from_a11(entry[11])
        if pages:
            field_values["pages"].append(str(pages))
        topic_list = topics_from_a12_to_a15(
            [
                entry[12],
                entry[13],
                entry[14],
                entry[15],
            ]
        )
        field_values["topic_lists"].append(topic_list)
        for topic in topic_list:
            field_values["topics"].append(topic)
        curator = curator_from_a16(entry[16])
        if curator:
            field_values["curator"].append(curator)

    for k, values in field_values.items():
        with open(os.path.join(reports_directory, f"calculated_field_{k}.yml"), "w", encoding="utf-8") as outfile:
            if values and isinstance(values[0], list):
                yaml.dump(values, outfile, default_flow_style=False, allow_unicode=True)
            else:
                yaml.dump(
                    list(sorted(set(values), key=lambda x: romanize(x))),
                    outfile,
                    default_flow_style=False,
                    allow_unicode=True,
                )


def is_valid_dewey_strict(d: str):
    strict_dewey_res = [
        re.compile(r"[0-9]{3}\.[0-9]+ [^0-9]+"),
        re.compile(r"[0-9]{3}\.[0-9]+"),
        re.compile(r"[0-9]{3} [^0-9]+"),
        re.compile(r"[0-9]{3}"),
    ]
    for dewey_re in strict_dewey_res:
        if dewey_re.fullmatch(d):
            return True
    return False


def test_report_dewey(reports_directory: str):
    weird_dewey: list[dict[int, str]] = list()
    for entry in all_entries():
        dewey = dewey_from_a04(entry[4])
        if dewey:
            if not is_valid_dewey_strict(dewey):
                weird_dewey.append(minimal_entry(entry, [0, 1, 2, 4, 5, 6]))
        else:
            if none_if_empty_or_stripped(entry[4]):
                weird_dewey.append(minimal_entry(entry, [0, 1, 2, 4, 5, 6]))
    with open(os.path.join(reports_directory, f"weird_dewey.yml"), "w", encoding="utf-8") as outfile:
        yaml.dump(weird_dewey, outfile, default_flow_style=False, allow_unicode=True)


def test_report_entry_numbers(reports_directory: str):
    all_entry_numbers: dict[str, dict[int, str]] = dict()
    no_entry_numbers: list[dict[int, str]] = list()
    non_numeric: defaultdict[str, list[dict[int, str]]] = defaultdict(list)
    duplicate_entry_numbers: defaultdict[str, list[dict[int, str]]] = defaultdict(list)
    for entry in all_entries():
        entry_numbers = entry_numbers_from_a05_a06_a07_a08(entry[5], entry[6], entry[7], entry[8])
        if not entry_numbers:
            no_entry_numbers.append(minimal_entry(entry, [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 17, 18, 19]))
        else:
            for n in entry_numbers:
                if n in all_entry_numbers:
                    if not duplicate_entry_numbers[n]:
                        duplicate_entry_numbers[n].append(all_entry_numbers[n])
                    duplicate_entry_numbers[n].append(
                        minimal_entry(entry, [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 17, 18, 19])
                    )
                else:
                    all_entry_numbers[n] = minimal_entry(entry, [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 17, 18, 19])
                if not n.isnumeric():
                    non_numeric[n].append(minimal_entry(entry, [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 17, 18, 19]))
    with open(os.path.join(reports_directory, f"entry_numbers_no_entry_numbers.yml"), "w", encoding="utf-8") as outfile:
        yaml.dump(no_entry_numbers, outfile, default_flow_style=False, allow_unicode=True)
    with open(os.path.join(reports_directory, f"entry_numbers_non_numeric.yml"), "w", encoding="utf-8") as outfile:
        yaml.dump(dict(non_numeric), outfile, default_flow_style=False, allow_unicode=True)
    with open(os.path.join(reports_directory, f"entry_numbers_duplicate.yml"), "w", encoding="utf-8") as outfile:
        yaml.dump(dict(duplicate_entry_numbers), outfile, default_flow_style=False, allow_unicode=True)


def test_report_translators(reports_directory: str):
    weird_translators: list[str] = []
    valid_translator_re = re.compile(r"[Α-Ω\-]+,[Α-Ω\.]*\.?")
    for entry in all_entries():
        translator = translator_from_a06(entry[6])
        if translator:
            translators = translator.split("!!")
            for translator in translators:
                if not valid_translator_re.fullmatch(translator):
                    weird_translators.append(translator)
    with open(os.path.join(reports_directory, f"weird_translators.yml"), "w", encoding="utf-8") as outfile:
        yaml.dump(weird_translators, outfile, default_flow_style=False, allow_unicode=True)
