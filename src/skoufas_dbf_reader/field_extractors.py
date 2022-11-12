""" Functions that extract information given specific strings """
from functools import cache
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
def dewey_corrections() -> dict[str, str]:
    """Map of invalid dewey codes found and manual overrides"""
    return read_yaml_data("invalid_dewey")


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


def dewey_from_a04(a04: Optional[str]) -> Optional[str]:
    """Cleanup and replace known issues"""
    value = none_if_empty_or_stripped(a04)
    if value:
        return none_if_empty_or_stripped(dewey_corrections().get(value, value))
    return None




