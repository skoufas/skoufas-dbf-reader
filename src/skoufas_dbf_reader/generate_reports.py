from __future__ import annotations

import os
import pprint
import shutil
from collections import defaultdict

import yaml
from snakemd import Document, InlineText, MDCheckList, MDList, Table

from skoufas_dbf_reader.correction_data import plain_author_re
from skoufas_dbf_reader.field_extractors import *
from skoufas_dbf_reader.utilities import all_entries, check_ean, check_isbn, check_issn, is_valid_dewey_strict, romanize


def report_single_fields(reports_directory: str):
    field_values: list[set[str]] = [set() for _ in range(31)]
    os.makedirs(os.path.join(reports_directory, "single-field"), exist_ok=True)
    for entry in all_entries():
        for i in range(1, 31):
            if i in entry and entry[i] and entry[i].strip():
                field_values[i].add(entry[i].strip())
    for i in range(1, 31):
        doc = Document(f"Τιμές στη θέση {i:02}")
        doc.add_header(f"Τιμές στη θέση {i:02}")
        doc.add_unordered_list([f"`{v}`" for v in sorted(field_values[i])])
        with open(
            os.path.join(reports_directory, "single-field", f"field_{i:02}.md"), "w", encoding="utf-8"
        ) as outfile:
            outfile.write(str(doc))


def report_single_extracted_fields(reports_directory: str):
    field_values: defaultdict[str, list[str | list[str]]] = defaultdict(list)
    for entry in all_entries():

        authors = authors_from_a01(entry[1])
        for author in authors:
            field_values["author"].append(author)
            if plain_author_re.fullmatch(author) or author in author_corrections().values():
                field_values["plain_author"].append(author)
            else:
                field_values["weird_author"].append(author)

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

        entry_numbers = entry_numbers_from_a05_a06_a07_a08_a18_a19(
            entry[5], entry[6], entry[7], entry[8], entry[18], entry[19]
        )

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

        topic_list = topics_from_a12_to_a15_a20_a22_to_a24(
            [
                entry[12],
                entry[13],
                entry[14],
                entry[15],
                entry[20],
                entry[22],
                entry[23],
                entry[24],
            ]
        )
        field_values["topic_lists"].append(topic_list)
        for topic in topic_list:
            field_values["topics"].append(topic)

        curator = curator_from_a16(entry[16])
        if curator:
            field_values["curator"].append(curator)

        copies = copies_from_a17_a18_a30(entry[17], entry[18], entry[30])
        if copies:
            field_values["copies"].append(str(copies))

        donation = donation_from_a17_a30(entry[17], entry[30])
        if donation:
            field_values["donation"].append(donation)

        volume = volume_from_a17_a18_a20_a30(entry[17], entry[18], entry[20], entry[30])
        if volume:
            field_values["volume"].append(volume)

        material = material_from_a18_a30(entry[18], entry[30])
        if material:
            field_values["material"].append(material)

        notes = notes_from_a17_a18_a21_a30(entry[17], entry[18], entry[21], entry[30])
        if notes:
            field_values["notes"].append(notes)

        isbn = isbn_from_a17_a18_a19_a22_a30(entry[17], entry[18], entry[19], entry[22], entry[30])
        if isbn:
            if not check_isbn(isbn):
                field_values["isbn"].append(isbn)
            if not check_issn(isbn):
                field_values["issn"].append(isbn)
            if not check_ean(isbn):
                field_values["ean"].append(isbn)

    os.makedirs(os.path.join(reports_directory, "calculated-field"), exist_ok=True)

    for k, values in field_values.items():
        values = [pprint.pformat(value) for value in values]
        with open(
            os.path.join(reports_directory, "calculated-field", f"calculated_field_{k}.md"), "w", encoding="utf-8"
        ) as outfile:
            doc = Document(f"Υπολογισμένες τιμές για την ιδιότητα {k}")
            doc.add_header(f"Υπολογισμένες τιμές για την ιδιότητα {k}, αλφαβητικά")
            doc.add_unordered_list([f"`{v}`" for v in sorted(set(values))])
            outfile.write(str(doc))
        with open(
            os.path.join(reports_directory, "calculated-field", f"calculated_field_{k}_romanize_sort.md"),
            "w",
            encoding="utf-8",
        ) as outfile:
            doc = Document(f"Υπολογισμένες τιμές για την ιδιότητα {k}")
            doc.add_header(f"Υπολογισμένες τιμές για την ιδιότητα {k}, φωνητικά")
            doc.add_unordered_list([f"`{v}` # *{romanize(v)}*" for v in sorted(set(values), key=romanize)])
            outfile.write(str(doc))


def report_invalid_dewey(reports_directory: str):
    invalid_output_dewey: defaultdict[str, list[str]] = defaultdict(list)
    no_output_dewey: defaultdict[str, list[str]] = defaultdict(list)
    for entry in all_entries():
        dewey = dewey_from_a04(entry[4])
        if dewey:
            if not is_valid_dewey_strict(dewey):
                invalid_output_dewey[dewey].append(str(entry[0]))
        else:
            if none_if_empty_or_stripped(entry[4]):
                no_output_dewey[entry[4]].append(str(entry[0]))

    os.makedirs(os.path.join(reports_directory, "checks"), exist_ok=True)
    with open(os.path.join(reports_directory, "checks", "invalid_dewey.md"), "w", encoding="utf-8") as outfile:
        doc = Document("Dewey με προβληματικές τιμές")
        doc.add_header("Dewey με προβληματικές τιμές στην έξοδο")
        for k, v in sorted(invalid_output_dewey.items()):
            doc.add_header(k, level=2)
            doc.add_unordered_list(
                [InlineText(entry, code=True, url="../entries/entry_{entry:05}.md").render() for entry in v]
            )
        doc.add_header("Dewey στην είσοδο που δεν βγαίνουν στην έξοδο")
        for k, v in sorted(no_output_dewey.items()):
            doc.add_header(k, level=2)
            doc.add_unordered_list(
                [InlineText(entry, code=True, url="../entries/entry_{entry:05}.md").render() for entry in v]
            )
        outfile.write(str(doc))


def report_entry_numbers(reports_directory: str):
    all_entry_numbers: dict[str, dict[int, str]] = dict()

    no_entry_numbers = Document("Καρτέλες χωρίς αριθμό εισαγωγής")
    no_entry_numbers.add_header("Καρτέλες χωρίς αριθμό εισαγωγής")

    non_numeric = Document("Καρτέλες με μή αριθμητικό αριθμό εισαγωγής")
    non_numeric.add_header("Καρτέλες με μή αριθμητικό αριθμό εισαγωγής")

    duplicate_entry_numbers: defaultdict[str, list[dict[int, str]]] = defaultdict(list)

    for entry in all_entries():
        entry_numbers = entry_numbers_from_a05_a06_a07_a08_a18_a19(
            entry[5], entry[6], entry[7], entry[8], entry[18], entry[19]
        )
        if not entry_numbers:
            no_entry_numbers.add_horizontal_rule()
            no_entry_numbers.add_code(entry_as_yaml(entry), lang="yaml")
        else:
            for n in entry_numbers:
                if n in all_entry_numbers:
                    if not duplicate_entry_numbers[n]:
                        duplicate_entry_numbers[n].append(all_entry_numbers[n])
                    duplicate_entry_numbers[n].append(entry)
                else:
                    all_entry_numbers[n] = entry
                if not n.isnumeric():
                    non_numeric.add_horizontal_rule()
                    non_numeric.add_paragraph(n)
                    non_numeric.add_code(entry_as_yaml(entry), lang="yaml")

    os.makedirs(os.path.join(reports_directory, "checks"), exist_ok=True)
    with open(os.path.join(reports_directory, "checks", "no_entry_numbers.md"), "w", encoding="utf-8") as outfile:
        outfile.write(str(no_entry_numbers))
    with open(
        os.path.join(reports_directory, "checks", "non_numeric_entry_numbers.md"), "w", encoding="utf-8"
    ) as outfile:
        outfile.write(str(no_entry_numbers))

    with open(
        os.path.join(reports_directory, "checks", f"duplicate_entry_numbers.md"), "w", encoding="utf-8"
    ) as outfile:
        dup = Document("Καρτέλες με διπλοπερασμένο αριθμητικό αριθμό εισαγωγής")
        dup.add_header("Καρτέλες με διπλοπερασμένο αριθμητικό αριθμό εισαγωγής")
        for entry_number, entries in duplicate_entry_numbers.items():
            dup.add_horizontal_rule()
            dup.add_paragraph(entry_number)
            for entry in entries:
                dup.add_code(entry_as_yaml(entry), lang="yaml")
        outfile.write(str(dup))


def entry_as_yaml(entry: dict[int, str]) -> str:
    """return an entry for a code section"""
    return yaml.dump(entry, default_flow_style=False, allow_unicode=True)


def report_entries(reports_directory: str):
    os.makedirs(os.path.join(reports_directory, "entries"), exist_ok=True)

    for entry in all_entries():
        translator = translator_from_a06(entry[6])
        translators: list[str] = []
        if translator:
            for single_translator in translator.split("!!"):
                translator_surname_name = single_translator.split(",", maxsplit=1)
                if len(translator_surname_name) == 2:
                    if translator_surname_name[1].endswith("."):
                        translators.append(
                            f"Επίθετο:{translator_surname_name[0]}, Μή πλήρες όνομα: {translator_surname_name[1]}"
                        )
                    else:
                        translators.append(f"Επίθετο:{translator_surname_name[0]}, Oνομα: {translator_surname_name[1]}")
                else:
                    translators.append(f"{single_translator}")

        donation = donation_from_a17_a30(entry[17], entry[30])
        donors: list[str] = []
        if donation:
            donors = donation.split("!!")

        editor = editor_from_a08_a09(entry[8], entry[9])
        if editor:
            editor = f"{editor[0]} ({editor[1]})"

        topic_list = topics_from_a12_to_a15_a20_a22_to_a24(
            [
                entry[12],
                entry[13],
                entry[14],
                entry[15],
                entry[20],
                entry[22],
                entry[23],
                entry[24],
            ]
        )

        isbn_issn_ean = isbn_from_a17_a18_a19_a22_a30(entry[17], entry[18], entry[19], entry[22], entry[30])
        isbn = ""
        issn = ""
        ean = ""
        if isbn_issn_ean:
            if not check_isbn(isbn_issn_ean):
                isbn = isbn_issn_ean
            if not check_issn(isbn_issn_ean):
                issn = isbn_issn_ean
            if not check_ean(isbn_issn_ean):
                ean = isbn_issn_ean

        doc = Document(f"entry_{entry[0]:05}")

        doc.add_header("Τίτλος")
        doc.add_paragraph(str(title_from_a02(entry[2])))
        doc.add_paragraph(str(subtitle_from_a03(entry[3])))

        doc.add_header("Συγγραφείς", level=2)
        doc.add_unordered_list(authors_from_a01(entry[1]))

        doc.add_header("Αριθμοί Εισαγωγης", level=2)
        doc.add_unordered_list(
            entry_numbers_from_a05_a06_a07_a08_a18_a19(entry[5], entry[6], entry[7], entry[8], entry[18], entry[19])
        )

        doc.add_table(
            ["Πεδίο", "Τιμή"],
            [
                ["dbase_number", str(entry[0])],
                ["Γλώσσα", str(language_from_a01(entry[1]))],
                ["Dewey", str(dewey_from_a04(entry[4]))],
                ["Έκδοση", str(edition_from_a07(entry[7]))],
                ["Εκδότης (Πόλη)", f"{editor}"],
                ["Χρόνος έκδοσης", f"{edition_year_from_a09_a10(entry[9], entry[10])}"],
                ["Σελίδες", f"{pages_from_a11(entry[11])}"],
                ["Επιμελητής", f"{curator_from_a16(entry[16])}"],
                ["Αντίτυπα", f"{copies_from_a17_a18_a30(entry[17], entry[18], entry[30])}"],
                ["Δωρητές", MDList(donors).render()],
                ["Τεύχος/Τόμος", f"{volume_from_a17_a18_a20_a30(entry[17], entry[18], entry[20], entry[30])}"],
                ["Υλικό", f"{material_from_a18_a30(entry[18], entry[30])}"],
                ["Σημειώσεις", f"{notes_from_a17_a18_a21_a30(entry[17], entry[18], entry[21], entry[30])}"],
                ["ISBN", isbn],
                ["ISSN", issn],
                ["EAN", ean],
            ],
            [Table.Align.LEFT, Table.Align.RIGHT],
            0,
        )

        doc.add_paragraph("Μεταφραστές")
        doc.add_unordered_list(translators)

        doc.add_paragraph("Θέματα")
        doc.add_unordered_list(topic_list)

        doc.add_paragraph("Ιδιότητες")
        doc.add_element(
            MDCheckList(
                ["Εχει CD"],
                checked=has_cd_from_a02_a03_a12_a13_a14_a17_a18_a22_a30(
                    [
                        entry[2],
                        entry[3],
                        entry[12],
                        entry[13],
                        entry[14],
                        entry[17],
                        entry[18],
                        entry[22],
                        entry[30],
                    ]
                ),
            )
        )

        doc.add_element(
            MDCheckList(
                ["Εχει DVD"],
                checked=has_dvd_from_a30(
                    [
                        entry[30],
                    ]
                ),
            )
        )

        doc.add_element(MDCheckList(["Ανάτυπο"], checked=offprint_from_a17_a21_a30(entry[17], entry[21], entry[30])))

        doc.add_header("Αρχική Καρτέλα στο DBASE", level=1)
        doc.add_code(code=entry_as_yaml(entry), lang="yaml")

        with open(
            os.path.join(reports_directory, "entries", f"entry_{entry[0]:05}.md"), "w", encoding="utf-8"
        ) as outfile:
            outfile.write(str(doc))


def main():
    """Create markdown reports"""
    md_report_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, "md_reports")
    shutil.rmtree(md_report_dir, ignore_errors=True)
    report_entry_numbers(md_report_dir)
    report_entries(md_report_dir)
    report_single_fields(md_report_dir)
    report_single_extracted_fields(md_report_dir)
    report_invalid_dewey(md_report_dir)


if __name__ == "__main__":
    main()


