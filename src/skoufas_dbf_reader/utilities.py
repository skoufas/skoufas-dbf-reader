""" Utilities for conversions """
import os
from typing import Any

import yaml


def read_yaml_data(code: str) -> Any:
    """Return the only object from a yaml file in the data directory"""
    with open(os.path.join(os.path.dirname(__file__), "data", f"{code}.yml"), "r", encoding="utf-8") as stream:
        parsed_yaml = yaml.safe_load(stream)
        return parsed_yaml[code]

