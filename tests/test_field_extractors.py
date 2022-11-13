from __future__ import annotations

from skoufas_dbf_reader.field_extractors import (
    author_part_from_a01,
    dewey_from_a04,
    entry_numbers_from_a05_a06,
    has_author,
    has_language,
    language_codes,
    language_from_a01,
    no_author_values,
    subtitle_from_a03,
    title_from_a02,
)


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


def test_language_codes():
    assert language_codes()
    assert type(language_codes()) == dict
    assert len(language_codes()) > 0


def test_has_language():
    assert not has_language(None)
    assert not has_language("")
    assert not has_language("GAL")
    assert not has_language("ΨΑΡΟΜΗΛΙΓΚΟΣ , ΛΑΖΟΥ , ΚΑΡΤΑΛΗΣ ")
    assert has_language("ΩUENEAU RAYMOND                    GAL")
    assert not has_language("ΚΕΛΕΣΙΔΗΣ, ΤΕΛΗΣ                       Ι")
    assert has_language("BITSIOS,DIMITRIS                  AGL")
    assert has_language("FINLAY GEORG                        GER")


def test_author_part_from_a01():
    assert not author_part_from_a01(None)
    assert not author_part_from_a01("")
    assert not author_part_from_a01("X,S")
    assert author_part_from_a01("GAL") == "GAL"
    assert author_part_from_a01("ΨΑΡΟΜΗΛΙΓΚΟΣ , ΛΑΖΟΥ , ΚΑΡΤΑΛΗΣ ") == "ΨΑΡΟΜΗΛΙΓΚΟΣ , ΛΑΖΟΥ , ΚΑΡΤΑΛΗΣ"
    assert author_part_from_a01("ΚΕΛΕΣΙΔΗΣ, ΤΕΛΗΣ                       Ι") == "ΚΕΛΕΣΙΔΗΣ, ΤΕΛΗΣ"
    assert author_part_from_a01("ΩUENEAU RAYMOND                    GAL") == "ΩUENEAU RAYMOND"
    assert author_part_from_a01("BITSIOS,DIMITRIS                  AGL") == "BITSIOS,DIMITRIS"
    assert author_part_from_a01("FINLAY GEORG                        GER") == "FINLAY GEORG"
    assert author_part_from_a01("ΑΝΑΓΝΩΣΤΑΚΗΣ,ΗΛΙΑΣ    .") == "ΑΝΑΓΝΩΣΤΑΚΗΣ,ΗΛΙΑΣ"


def test_language_from_a01():
    assert not language_from_a01(None)
    assert not language_from_a01("")
    assert not language_from_a01("GAL")
    assert not language_from_a01("ΨΑΡΟΜΗΛΙΓΚΟΣ , ΛΑΖΟΥ , ΚΑΡΤΑΛΗΣ ")
    assert not language_from_a01("ΚΕΛΕΣΙΔΗΣ, ΤΕΛΗΣ                       Ι")
    assert language_from_a01("ΩUENEAU RAYMOND                    GAL") == "FR"
    assert language_from_a01("BITSIOS,DIMITRIS                  AGL") == "EN"
    assert language_from_a01("FINLAY GEORG                        GER") == "DE"


def test_title_from_a02():
    assert title_from_a02(None) is None
    assert title_from_a02("") is None
    assert title_from_a02(" ") is None
    assert title_from_a02("GAL ") == "GAL"
    assert title_from_a02(" GAL") == "GAL"


def test_subtitle_from_a03():
    assert subtitle_from_a03(None) is None
    assert subtitle_from_a03("") is None
    assert subtitle_from_a03(" ") is None
    assert subtitle_from_a03("GAL ") == "GAL"
    assert subtitle_from_a03(" GAL") == "GAL"


def test_dewey_from_a04():
    assert dewey_from_a04(None) is None
    assert dewey_from_a04("") is None
    assert dewey_from_a04(" ") is None
    assert dewey_from_a04("001A") == "001 A"
    assert dewey_from_a04("001.009ΚΟΝ ") == "001.009 ΚΟΝ"
    assert dewey_from_a04(" 001.009ΚΟΝ") == "001.009 ΚΟΝ"
    assert dewey_from_a04("O.50ΠΕΡ") == "0.50 ΠΕΡ"
    assert dewey_from_a04("624.183Χ.Σ") == "624.183 ΧΣ"

    assert dewey_from_a04("HOEMANN") is None


def test_entry_numbers_from_a05_a06():
    assert entry_numbers_from_a05_a06(None, None) == []
    assert entry_numbers_from_a05_a06("", "") == []
    assert entry_numbers_from_a05_a06(" ", None) == []
    assert entry_numbers_from_a05_a06(None, "") == []
    assert entry_numbers_from_a05_a06("2710-2709", None) == ["2710", "2709"]
    assert entry_numbers_from_a05_a06("2710-2709", "foobar") == ["2710", "2709"]
    assert entry_numbers_from_a05_a06("2710-2709", "-") == ["2710", "2709"]
    assert entry_numbers_from_a05_a06("2710-2709", "-10450") == ["2710", "2709", "10450"]
    assert entry_numbers_from_a05_a06("2710-2709", "1747-1746-1745-") == ["2710", "2709", "1747", "1746", "1745"]
    assert entry_numbers_from_a05_a06("10-1", "4") == ["10", "14"]
    assert entry_numbers_from_a05_a06("10-1", "5") == ["10", "15"]
    assert entry_numbers_from_a05_a06("10-1", "448 ΚΩΣΤΑΣ ΦΙΛΙΝΗΣ") == ["10", "1448"]
