""" Functions that extract information given specific strings """
import re
from functools import cache
from collections import OrderedDict
from typing import Optional

from skoufas_dbf_reader.utilities import none_if_empty_or_stripped, read_yaml_data


def has_author(a01: Optional[str]) -> bool:
    """Check values for marks of missing author"""
    if not a01:
        return False
    if a01 in no_author_values():
        return False
    return True


@cache
def no_author_values() -> list[str]:
    """List of values implying there's no author"""
    return read_yaml_data("no_author")


@cache
def language_codes() -> dict[str, str]:
    """Map of language codes in A01 to ISO language codes"""
    return read_yaml_data("language_codes")


@cache
def field04_corrections() -> dict[str, str]:
    """Map of invalid dewey codes found and manual overrides"""
    return read_yaml_data("field04_corrections")


@cache
def field06_corrections() -> dict[str, Optional[str | dict[str, str | bool]]]:
    """Map of invalid entry numbers found and manual overrides"""
    return read_yaml_data("field06_corrections")


@cache
def field07_corrections() -> dict[str, Optional[str | dict[str, str | bool]]]:
    """Map of entry numbers and manual overrides"""
    return read_yaml_data("field07_corrections")


@cache
def field08_corrections() -> dict[str, Optional[str | dict[str, str]]]:
    """Map of editors and manual overrides"""
    return read_yaml_data("field08_corrections")


@cache
def field09_corrections() -> dict[str, Optional[str | dict[str, str]]]:
    """Map of editor places and manual overrides"""
    return read_yaml_data("field09_corrections")


@cache
def field10_corrections() -> dict[str, Optional[str]]:
    """Map of year and manual overrides"""
    return read_yaml_data("field10_corrections")


@cache
def field11_corrections() -> dict[str, Optional[str]]:
    """Map of pages and manual overrides"""
    return read_yaml_data("field11_corrections")


@cache
def topic_replacements() -> dict[str, Optional[str]]:
    """Map of topic name manual overrides"""
    return read_yaml_data("topic_replacements")


@cache
def translator_corrections() -> dict[str, str]:
    """Map of translator names found and manual overrides"""
    return read_yaml_data("translator_corrections")


def has_language(a01: Optional[str]) -> bool:
    """Check values for language at the end"""
    if not a01:
        return False
    for code in language_codes().keys():
        if a01.endswith(f" {code}"):
            return True
    return False


def author_part_from_a01(a01: Optional[str]) -> Optional[str]:
    """Get author from A01 DBF record"""
    if not a01:
        return None
    if not has_author(a01):
        return None
    strip_finals = list(language_codes().keys()) + [
        " Ι",
        " .",
    ]
    for final in strip_finals:
        if a01.endswith(" " + final):
            a01 = a01.replace(final, "")
    return a01.strip()


def language_from_a01(a01: Optional[str]) -> Optional[str]:
    """Check values for language at the end"""
    if not a01:
        return None
    if has_language(a01):
        for language, isolanguage in language_codes().items():
            if a01.endswith(language):
                return isolanguage
    return None


def title_from_a02(a02: Optional[str]) -> Optional[str]:
    """Cleanup"""
    return none_if_empty_or_stripped(a02)


def subtitle_from_a03(a03: Optional[str]) -> Optional[str]:
    """Cleanup"""
    return none_if_empty_or_stripped(a03)


dewey_re1 = [
    re.compile(r"([0-9]{3})"),
    re.compile(r"([0-9]{3}\.[0-9]+)"),
]
dewey_re2 = [
    re.compile(r"([0-9]{3}\.[0-9]+)\s+([^0-9\.]*)"),
    re.compile(r"([0-9]{3}\.[0-9]+)([^0-9\.]*)"),
    re.compile(r"([0-9]{3})\s+([^0-9\.]*)"),
    re.compile(r"([0-9]{3})([^0-9\.]*)"),
]


def dewey_from_a04(a04: Optional[str]) -> Optional[str]:
    """Cleanup and replace known issues"""
    value = none_if_empty_or_stripped(a04)
    if not value:
        return None
    value = none_if_empty_or_stripped(field04_corrections().get(value, value))
    if not value:
        return None

    value = value.replace("Χ. Σ.", "ΧΣ")
    value = value.replace("Χ. Σ", "ΧΣ")

    value = value.replace("X.S.", "ΧΣ")
    value = value.replace("Χ.Σ.", "ΧΣ")

    value = value.replace("Χ.Σ", "ΧΣ")
    value = value.replace("X.S", "ΧΣ")
    value = value.replace("X.Σ", "ΧΣ")
    value = value.replace("Σ.Σ", "ΧΣ")

    value = value.replace("Χ.Χ.", "ΧΧ")
    value = value.replace("Χ.Χ", "ΧΧ")

    for dewey_re in dewey_re1:
        dewey_match = dewey_re.fullmatch(value)
        if dewey_match:
            return f"{dewey_match[1]}".strip()
    for dewey_re in dewey_re2:
        dewey_match = dewey_re.fullmatch(value)
        if dewey_match:
            return f"{dewey_match[1]} {dewey_match[2]}".strip()
    return None


def entry_numbers_from_a05_a06_a07_a08(
    a05: Optional[str], a06: Optional[str], a07: Optional[str], a08: Optional[str]
) -> list[str]:
    """Cleanup, read additional numbers from a06"""
    value5 = none_if_empty_or_stripped(a05)
    if not value5:
        value5 = ""
    value6 = none_if_empty_or_stripped(a06)
    if value6:
        if value6 in field06_corrections():
            correction = field06_corrections()[value6]
            if correction is None:
                value6 = ""
            elif isinstance(correction, str):
                value6 = "-" + str(correction)
            else:
                value6 = dict(correction).get("series", "")
                if not isinstance(value6, str):
                    raise Exception(f"Invalid correction for field A06 [{a06}]")
                if correction.get("use_dash", True):
                    value6 = "-" + value6
        else:
            value6 = ""
    else:
        value6 = ""

    value7 = none_if_empty_or_stripped(a07)
    if value7:
        if value7 in field07_corrections():
            correction = field07_corrections()[value7]
            if correction is None:
                value7 = ""
            elif isinstance(correction, str):
                value7 = ""
            else:
                value7 = dict(correction).get("series", "")
                if not isinstance(value7, str):
                    raise Exception(f"Invalid correction for field A07 [{a07}]")
                value7 = "-" + value7
        else:
            value7 = ""
    else:
        value7 = ""

    value8 = none_if_empty_or_stripped(a08)
    if value8:
        if value8 in field08_corrections():
            correction = field08_corrections()[value8]
            if correction is None:
                value8 = ""
            elif isinstance(correction, str):
                value8 = ""
            else:
                value8 = dict(correction).get("series", "")
                if not isinstance(value8, str):
                    raise Exception(f"Invalid correction for field A08 [{a08}]")
                value8 = "-" + value8
        else:
            value8 = ""
    else:
        value8 = ""

    value = value5 + value6 + value7 + value8
    entries = [v.strip() for v in value.split("-") if v.strip()]
    return entries


def translator_from_a06(a06: Optional[str]) -> Optional[str]:
    """Cleanup, replace special cases"""
    value = none_if_empty_or_stripped(a06)
    if not value:
        return None
    if value in field06_corrections():
        correction = field06_corrections()[value]
        if correction is None:
            return None
        elif isinstance(correction, str):
            return None
        else:
            value = dict(correction).get("translator", None)
            if not value:
                return None
            if not isinstance(value, str):
                raise Exception(f"Invalid correction for field A06 [{a06}]")
    value = translator_corrections().get(value, value)
    if not value:
        return None
    return value


def edition_from_a07(a07: Optional[str]) -> Optional[str]:
    """Cleanup, replace special cases"""
    value = none_if_empty_or_stripped(a07)
    if not value:
        return None
    if value in field07_corrections():
        value = field07_corrections().get(value)
        if not isinstance(value, str):
            return None
    if not value:
        return None
    return value


def editor_from_a08_a09(a08: Optional[str], a09: Optional[str]) -> Optional[tuple[Optional[str], Optional[str]]]:
    """Cleanup, replace special cases"""
    a08 = none_if_empty_or_stripped(a08)
    if not a08:
        a08 = None
    else:
        if a08 in field08_corrections():
            correction = field08_corrections().get(a08)
            if not correction:
                a08 = None
            elif isinstance(correction, dict):
                a08 = correction.get("editor", None)
            else:
                a08 = correction
    a09 = none_if_empty_or_stripped(a09)
    if not a09:
        a09 = None
    else:
        if a09 in field09_corrections():
            correction = field09_corrections().get(a09)
            if not correction:
                a09 = None
            elif isinstance(correction, dict):
                a09 = correction.get("place", None)
            else:
                a09 = correction
    if not a08 and not a09:
        return None
    return (a08, a09)


def edition_year_from_a09_a10(a09: Optional[str], a10: Optional[str]) -> Optional[int]:
    """Cleanup,handle special cases"""
    a09 = none_if_empty_or_stripped(a09)
    if a09 and a09 in field09_corrections():
        correction = field09_corrections().get(a09)
        if correction and isinstance(correction, dict) and "year" in correction:
            return int(correction["year"])

    a10 = none_if_empty_or_stripped(a10)
    if not a10:
        return None
    corrected = field10_corrections().get(a10, a10)
    if not corrected:
        return None
    if not corrected.isnumeric():
        raise Exception(f"invalid date [{a10}]")
    return int(corrected)


valid_pages_re = re.compile(r"(\d+)\s*(Σ|S|ΣΕΛ|Δ|Σ Ρ|ΣΑ|ΣΙΣ|Σ Ε|ΣΕΓ|Σ18|ΣΚΑ|ΣΑΜ|Σ Ο|s|Σ Λ|Σ  Α|Σ11|Σ#Ξ|Σ Ι|σ|Φ)*")


def pages_from_a11(a11: Optional[str]) -> Optional[int]:
    a11 = none_if_empty_or_stripped(a11)
    if not a11:
        return None
    corrected = field11_corrections().get(a11, a11)
    if not corrected:
        return None
    pages_match = valid_pages_re.fullmatch(corrected)
    if not pages_match:
        raise Exception(f"invalid pages [{a11}]")
    return int(pages_match.group(1))


topic_in_paren_re = re.compile(r".*?\((.*)\).*")


def topics_from_a12_to_a15(a12_a15: Optional[list[Optional[str]]]) -> list[str]:
    """Cleanup, make unique, handle special cases"""
    if not a12_a15:
        return []
    topics: OrderedDict[str, None] = OrderedDict()
    for line in a12_a15:
        line = none_if_empty_or_stripped(line)
        if line:
            match = topic_in_paren_re.fullmatch(line)
            if match:
                in_parenthesis = match[1].strip()
                in_parenthesis = topic_replacements().get(in_parenthesis, in_parenthesis).strip()
                topics[in_parenthesis] = None
                # remove match and parenthesis
                line = line.replace(match[1], "").replace("()", "")
            for topic in line.split("-"):
                if topic:
                    topic = topic_replacements().get(topic, topic)
                    if topic:
                        topics[topic.strip()] = None
    return list(topics.keys())


# def curator_from_a16(A16):
#     """Cleanup
#     >>> curator_from_a16(None) # None
#     >>> curator_from_a16('') # None
#     >>> curator_from_a16(' ') # None
#     >>> curator_from_a16('woo')
#     'woo'
#     >>> curator_from_a16('ΘΕΣΣΑΛΙΑ') # None
#     >>> curator_from_a16('#') # None
#     """
#     if not A16:
#         return None
#     if A16 in [
#         "ΘΕΣΣΑΛΙΑ",
#         "#",
#         "ΔΩΡΕΑ ΑΚΑΔΗΜΙΑ ΑΘΗΝΩ",
#     ]:
#         return None
#     if not A16.strip():
#         return None
#     return A16.strip()
