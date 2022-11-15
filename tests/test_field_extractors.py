from __future__ import annotations

from skoufas_dbf_reader.field_extractors import (
    author_part_from_a01,
    dewey_from_a04,
    edition_from_a07,
    editor_from_a08_a09,
    entry_numbers_from_a05_a06_a07_a08,
    has_author,
    has_language,
    language_codes,
    language_from_a01,
    no_author_values,
    subtitle_from_a03,
    title_from_a02,
    translator_from_a06,
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
    assert dewey_from_a04("O.50ΠΕΡ") == "050 ΠΕΡ"
    assert dewey_from_a04("624.183Χ.Σ") == "624.183 ΧΣ"
    assert dewey_from_a04("320ΤΣΟ") == "320 ΤΣΟ"

    assert dewey_from_a04("HOEMANN") is None


def test_entry_numbers_from_a05_a06_a07_a08():
    assert entry_numbers_from_a05_a06_a07_a08(None, None, None, None) == []
    assert entry_numbers_from_a05_a06_a07_a08("", "", "", "") == []
    assert entry_numbers_from_a05_a06_a07_a08(" ", None, "", "") == []
    assert entry_numbers_from_a05_a06_a07_a08(None, "", "", "") == []
    assert entry_numbers_from_a05_a06_a07_a08("2710-2709", None, None, None) == ["2710", "2709"]
    assert entry_numbers_from_a05_a06_a07_a08("2710-2709", "foobar", "baz", "yum") == ["2710", "2709"]
    assert entry_numbers_from_a05_a06_a07_a08("2710-2709", "-", "baz", "yum") == ["2710", "2709"]
    assert entry_numbers_from_a05_a06_a07_a08("2710-2709", "-10450", "baz", "yum") == ["2710", "2709", "10450"]
    assert entry_numbers_from_a05_a06_a07_a08("2710-2709", "1747-1746-1745-", "baz", "yum") == [
        "2710",
        "2709",
        "1747",
        "1746",
        "1745",
    ]
    assert entry_numbers_from_a05_a06_a07_a08("10-1", "4", "baz", "yum") == ["10", "14"]
    assert entry_numbers_from_a05_a06_a07_a08("10-1", "5", "baz", "yum") == ["10", "15"]
    assert entry_numbers_from_a05_a06_a07_a08("10-1", "448 ΚΩΣΤΑΣ ΦΙΛΙΝΗΣ", "baz", "yum") == ["10", "1448"]
    assert entry_numbers_from_a05_a06_a07_a08(
        "4225-4226-4228-4229-", "4227-4290-4536-4535-", "4537", "ΕΥΡΩΠΑΙΚ.ΚΕΝΤΡ.ΤΕΧΝΗ"
    ) == ["4225", "4226", "4228", "4229", "4227", "4290", "4536", "4535", "4537"]
    assert entry_numbers_from_a05_a06_a07_a08(
        "5280-5285-5286-5283-",
        "5284-5278-5277-5279-",
        "5281-",
        "5282-6548-6547",
    ) == "5280-5285-5286-5283-5284-5278-5277-5279-5281-5282-6548-6547".split("-")


def test_translator_from_a06():
    assert translator_from_a06(None) is None
    assert translator_from_a06("") is None
    assert translator_from_a06(" ") is None
    assert translator_from_a06("hello") == "hello"
    # Part of field06_corrections
    assert translator_from_a06("-") is None
    assert translator_from_a06("1203") is None
    assert translator_from_a06("3ΕΚΔ") is None
    assert translator_from_a06("2847 ΠΑΠΑΡΡΟΔΟΥ,ΝΙΚ") == "ΠΑΠΑΡΡΟΔΟΥ,ΝΙΚΟΛΑΟΣ"


def test_edition_from_a07():
    assert edition_from_a07(None) is None
    assert edition_from_a07("") is None
    assert edition_from_a07(" ") is None
    assert edition_from_a07("2") == "2"
    assert edition_from_a07("6ΕΚΔ") == "6"
    # invalid
    assert edition_from_a07("ΠΡΟΣΚΗ") is None
    # year
    assert edition_from_a07("1932") is None
    # series
    assert edition_from_a07("4537") is None


def test_editor_from_a08_a09():
    assert editor_from_a08_a09(None, None) is None
    assert editor_from_a08_a09("", "") is None
    assert editor_from_a08_a09(" ", " ") is None
    assert editor_from_a08_a09("hello", " ") == ("hello", None)
    assert editor_from_a08_a09("", "city") == (None, "city")
    assert editor_from_a08_a09("5282-6548-6547", "city") == (None, "city")
    assert editor_from_a08_a09('"Η ΔΑΜΑΣΚΟΣ"', "city") == ("Η ΔΑΜΑΣΚΟΣ", "city")
    assert editor_from_a08_a09("X.E", "city") == (None, "city")
    assert editor_from_a08_a09("hello", "1867") == ("hello", None)
    assert editor_from_a08_a09("hello", "AMSTERDAN") == ("hello", "AMSTERDAM")
    assert editor_from_a08_a09("hello", "ΑΘΗΝΑ 1984") == ("hello", "ΑΘΗΝΑ")
    assert editor_from_a08_a09("hello", "X.T") == ("hello", None)
