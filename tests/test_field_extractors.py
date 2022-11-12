from __future__ import annotations

from skoufas_dbf_reader.field_extractors import has_author, no_author_values


def test_no_author():
    no_author = no_author_values()
    assert no_author
    assert type(no_author) == list
    assert len(no_author) > 0


def test_has_author():
    assert not has_author(None)
    assert not has_author("")
    assert has_author("BLA")
    assert not has_author("ΧΣ")
    assert not has_author("X,S")
    assert not has_author("X.S.")
    assert not has_author("X.S")
    assert not has_author("X . Σ.")
    assert not has_author("X.Σ.")
    assert not has_author("X.Σ")
    assert not has_author("Χ.Σ")
    assert not has_author("Χ.Σ.")
    assert not has_author("Χ. Σ .")
    assert not has_author("Χ,Σ")
    assert not has_author("Χ. Σ.")
    assert not has_author("Χ.Χ")
    assert not has_author("Χ.Χ.")
