from cipherkit import EARLY_MODERN_FOLDS, GERMAN_FOLDS, normalize, strip_gutenberg


def test_accents_and_case():
    assert normalize("Élève, Ça!") == "eleveca"


def test_german_folds_before_accent_strip():
    assert normalize("Größe über", folds=GERMAN_FOLDS) == "groesseueber"
    # Without the German folds the umlauts lose their diaeresis instead.
    assert normalize("Größe über") == "grosseuber"


def test_early_modern_folds():
    assert normalize("Iuvenal vult", folds=EARLY_MODERN_FOLDS) == "iuuenaluult"


def test_keep_spaces_collapses_gaps():
    assert normalize("  Le  roy,\n\tluy - mesme. ", keep_spaces=True) == "le roy luy mesme"


def test_custom_alphabet():
    assert normalize("abc123 xyz", alphabet="abcxyz") == "abcxyz"


def test_strip_gutenberg():
    raw = "junk\n*** START OF THE PROJECT GUTENBERG EBOOK X ***\nbody text\n*** END OF THE PROJECT GUTENBERG EBOOK X ***\nlicence"
    assert strip_gutenberg(raw).strip() == "body text"
    assert strip_gutenberg("no markers") == "no markers"
