""" Functions that extract information given specific strings """
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

