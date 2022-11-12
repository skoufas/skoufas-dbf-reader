""" Utilities for conversions """
import os
from functools import cache
from typing import Any, Optional

import yaml


def read_yaml_data(code: str) -> Any:
    """Return the only object from a yaml file in the data directory"""
    with open(os.path.join(os.path.dirname(__file__), "data", f"{code}.yml"), "r", encoding="utf-8") as stream:
        parsed_yaml = yaml.safe_load(stream)
        return parsed_yaml[code]


def none_if_empty_or_stripped(i: Optional[str]) -> Optional[str]:
    """Cleanup"""
    if not i:
        return None
    if not i.strip():
        return None
    return i.strip()


@cache
def all_entries() -> list[dict[int, str]]:
    """All entries converted from a DBF file"""
    data = read_yaml_data("entries")
    for entry in data:
        for i in range(0, 31):
            if i not in entry:
                entry[i] = None
    return data


