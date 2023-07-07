# Skoufas Library DBF Reader

Functions to read and convert from the DBF file used to track books in the Skoufas library

## Columns in DBF file

| Column | Name (english) | Name (Greek) |
|--------|----------------|--------------|
| A01 | Author surname, name, language | Επώνυμο, Όνομα συγγραφέα |
| A02 | title, has_cd | Τίτλος, έχει CD |
| A03 | subtitle, has_cd | Υπότιτλος, έχει CD |
| A04 | Dewey | Ταξινομικός αριθμός |
| A05 | entry_number | αριθμός εισαγωγής |
| A06 | translator, edition, entry_number | μεταφραστής, έκδοση, αριθμός εισαγωγής |
| A07 | edition, entry_number | έκδοση, αριθμός εισαγωγής |
| A08 | editor, entry_number | εκδότης, αριθμός εισαγωγής |
| A09 | editor place | τοπος έκδοσης |
| A10 | edition year | ετος έκδοσης |
| A11 | pages | σελιδες |
| A12 | topics, has_cd | θέματα, έχει CD |
| A13 | topics, has_cd | θέματα, έχει CD |
| A14 | topics, has_cd | θέματα, έχει CD |
| A15 | topics | θέματα |
| A16 | curator | επιμελητής |
| A17 | has_cd, copies, donations, offprint, volume, notes, isbn | έχει CD, αντίτυπα, δωρεές, ανάτυπα, τόμοι/τεύχη, σημειώσεις, isbn |
| A18 | material, entry_number, has_cd, copies, volume, notes, isbn | συνοδευτικό υλικό, έχει CD, αντίτυπα, τόμοι/τεύχη, σημειώσεις, isbn |
| A19 | isbn, entry_number | isbn, αριθμός εισαγωγής |
| A20 | topics, volume |  θέματα, τόμοι/τεύχη |
| A21 | offprint, notes | ανάτυπα, σημειώσεις |
| A22 | topics, has_cd, isbn| θέματα, έχει CD, isbn |
| A23 | topics| θέματα |
| A24 | topics| θέματα |
| A25 | | |
| A26 | | |
| A27 | | |
| A28 | | |
| A29 | | |
| A30 | has_cd, has_dvd, copies, donations, offprint, volume, material, notes, isbn | έχει CD, έχει DVD, αντίτυπα, δωρεές, ανάτυπα, τόμοι/τεύχη, συνοδευτικό υλικό, σημειώσεις, isbn |

## Extractor functions

- `def authors_from_a01(a01: Optional[str]) -> list[str]`
- `def copies_from_a17_a18_a30(a17: Optional[str], a18: Optional[str], a30: Optional[str]) -> Optional[int]`
- `def curator_from_a16(a16: Optional[str]) -> Optional[str]`
- `def dewey_from_a04_a05(a04: Optional[str], a05: Optional[str]) -> Optional[str]`
- `def donation_from_a17_a30(a17: Optional[str], a30: Optional[str]) -> Optional[str]`
- `def edition_from_a07(a07: Optional[str]) -> Optional[str]`
- `def edition_year_from_a09_a10(a09: Optional[str], a10: Optional[str]) -> Optional[int]`
- `def editor_from_a08_a09(a08: Optional[str], a09: Optional[str]) -> Optional[tuple[Optional[str], Optional[str]]]`
- `def entry_numbers_from_a04_a05_a06_a07_a08_a18_a19(a04: Optional[str], a05: Optional[str], a06: Optional[str],a07: Optional[str],a08: Optional[str],a18: Optional[str],a19: Optional[str],) -> list[str]`
- `def has_cd_from_a02_a03_a12_a13_a14_a17_a18_a22_a30(many_lines: Optional[list[Optional[str]]]) -> bool`
- `def has_dvd_from_a30(many_lines: Optional[list[Optional[str]]]) -> bool`
- `def isbn_from_a17_a18_a19_a22_a30(a17in: Optional[str], a18in: Optional[str], a19in: Optional[str], a22in: Optional[str], a30in: Optional[str]) -> Optional[str]`
- `language_from_a01_a02(a01: Optional[str], a02: Optional[str]) -> Optional[str]`
- `def material_from_a18_a30(a18: Optional[str], a30: Optional[str]) -> Optional[str]`
- `def notes_from_a17_a18_a21_a30(a17: Optional[str], a18: Optional[str], a21: Optional[str], a30: Optional[str]) -> Optional[str]`
- `def offprint_from_a17_a21_a30(a17: Optional[str], a21: Optional[str], a30: Optional[str]) -> bool`
- `def pages_from_a11(a11: Optional[str]) -> Optional[int]`
- `def subtitle_from_a03(a03: Optional[str]) -> Optional[str]`
- `def title_from_a02(a02: Optional[str]) -> Optional[str]`
- `def topics_from_a12_to_a15_a20_a22_to_a24( many_lines: Optional[list[Optional[str]]],) -> list[str]`
- `def translator_from_a06(a06: Optional[str]) -> Optional[str]`
- `def volume_from_a17_a18_a20_a30(a17: Optional[str], a18: Optional[str], a20: Optional[str], a30: Optional[str]) -> Optional[str]`

## Checks required

- Duplicated Entry Numbers (~800)
- Non-numeric entry numbers (~130)
- Missing entry numbers (~200)
- Weird deweys and replacements (~300)
- Translator corrections
- author corrections
- εκδοσεις
- εκδοτης (field8)
- field9
- field10
- isbn

## Columns required

### BookEntry

- Title - Τίτλος
- Subtitle - Υπότιτλος
- Dewey - Ταξινομικός Αριθμός Dewey
- Edition - Έκδοση
- EditionDate - Έτος Έκδοσης
- EditorId (FK: Editor)
- Pages - Σελίδες Αριθμητικά
- Volumes - Τόμοι/Τεύχη
- Notes - Σημειώσεις
- Material - Υλικό
- HasCD - Έχει
- HasDVD - Έχει
- ISBN
- ISSN
- EAN
- Offprint - ΑΝΑΤΥΠΟ

### Author - Συγγραφέας

- Name
- Surname
- Middlename
- Fullname

### Authorship (Many-to-Many)

- AuthorId (FK: Author)
- BookEntryId (FK: BookEntry)

### Translator - Μεταφραστής

- Name
- Surname
- Middlename
- Fullname

### Translation

- TranslatorId (FK: Translator)
- BookEntryId (FK: BookEntry)

### Curator - Επιμελητής

- Name
- Surname
- Middlename
- Fullname

### Curation

- CuratorId (FK: Curator)
- BookEntryId (FK: BookEntry)

### Editor

- Name
- Place

### Entry Numbers (one-to-many) - Αριθμοί Εισαγωγής

- EntryNumber (unique)
- BookEntryId (FK: BookEntry)
- Copies

### Topic - Θέμα

- Name

### BookInTopic (many-to-many)

- TopicId (FK: Topic)
- BookEntryId (FK: BookEntry)

### Donor - Δωρητής

- Name
- Surname
- Middlename
- Fullname

### Donation (Many-to-Many) - Δωρεά

- DonorId (FK: Donor)
- EntryNumberId (FK: EntryNumber)

### Customer - Πελάτες

- Name
- Surname
- Middlename
- FullName
- IdNumber
- IdType
- PhoneNumber
- Email
- Address

### Loan - Δανεισμός

- CustomerId (FK: Customer)
- EntryNumberId (FK: EntryNumber)
- StartDateTime
- ExpectedEndDateTime
- EndDateTime
- Note
