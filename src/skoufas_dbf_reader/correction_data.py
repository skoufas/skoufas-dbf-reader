""" Functions that extract information given specific strings """
import re
from functools import cache
from typing import Optional

from skoufas_dbf_reader.utilities import read_yaml_data


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
def field16_corrections() -> dict[str, Optional[str]]:
    """Map of curators and manual overrides"""
    return read_yaml_data("field16_corrections")


@cache
def topic_replacements() -> dict[str, Optional[str]]:
    """Map of topic name manual overrides"""
    return read_yaml_data("topic_replacements")


@cache
def translator_corrections() -> dict[str, str]:
    """Map of translator names found and manual overrides"""
    return read_yaml_data("translator_corrections")


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

valid_pages_re = re.compile(r"(\d+)\s*(Σ|S|ΣΕΛ|Δ|Σ Ρ|ΣΑ|ΣΙΣ|Σ Ε|ΣΕΓ|Σ18|ΣΚΑ|ΣΑΜ|Σ Ο|s|Σ Λ|Σ  Α|Σ11|Σ#Ξ|Σ Ι|σ|Φ)*")

topic_in_paren_re = re.compile(r".*?\((.*)\).*")

has_cd_re = re.compile(r"\bCD\b", re.IGNORECASE)

has_dvd_re = re.compile(r"\bDVD\b", re.IGNORECASE)
