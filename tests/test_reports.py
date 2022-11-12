from __future__ import annotations

import os
import pytest
import yaml
from skoufas_dbf_reader.utilities import all_entries


@pytest.fixture
def reports_directory() -> str:
    r = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "reports"))
    os.makedirs(r, exist_ok=True)
    return r


def test_report_single_fields(reports_directory: str):
    field_values: list[set[str]] = [set() for _ in range(31)]
    for entry in all_entries():
        for i in range(1, 31):
            if i in entry and entry[i].strip():
                field_values[i].add(entry[i].strip())
    for i in range(1, 31):
        with open(os.path.join(reports_directory, f"fields_{i:02}.yml"), "w", encoding="utf-8") as outfile:
            yaml.dump(list(sorted(field_values[i])), outfile, default_flow_style=False, allow_unicode=True)
