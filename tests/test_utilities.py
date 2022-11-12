from __future__ import annotations

from skoufas_dbf_reader.utilities import read_yaml_data


def test_yaml_data():
    no_author = read_yaml_data("no_author")
    assert no_author
    assert type(no_author) == list
    assert len(no_author) > 0


def test_none_if_empty_or_stripped():
    assert none_if_empty_or_stripped(None) is None
    assert none_if_empty_or_stripped("") is None
    assert none_if_empty_or_stripped(" ") is None
    assert none_if_empty_or_stripped("   ") is None
    assert none_if_empty_or_stripped("foo") == "foo"
    assert none_if_empty_or_stripped("    foo ") == "foo"


