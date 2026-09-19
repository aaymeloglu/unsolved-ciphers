from cipherkit.corpora import G, IA, MARKERS, RECIPES, clean_ocr, dehyphenate, marker_counts


MIXED_DE = """\
Der König schrieb an den Minister, dass die Sache nicht länger warten könne.
Le roi écrit au ministre que la chose ne peut plus attendre, et vous le savez.
Berlin, den 3. März 1763.
--- 214 --- |||| ..,, ;; 12 34 56 ~~~
Ich habe die Depesche erhalten und werde sie mit dem nächsten Kurier beantworten.
Nous avons reçu la dépêche et nous y répondrons avec le prochain courrier.
"""


def test_clean_ocr_drops_other_language_lines():
    kept = clean_ocr(MIXED_DE, "de").splitlines()
    assert any(line.startswith("Der König") for line in kept)
    assert any(line.startswith("Ich habe") for line in kept)
    assert not any("Le roi" in line or "Nous avons" in line for line in kept)


def test_clean_ocr_keeps_short_unmarked_lines_and_drops_garbage():
    kept = clean_ocr(MIXED_DE, "de").splitlines()
    assert "Berlin, den 3. März 1763." in kept
    assert not any("|||" in line for line in kept)


def test_clean_ocr_scots_keeps_english_function_words():
    text = "The lordis of the counsale ordanit that the samin be done, quhilk thai did.\n"
    assert clean_ocr(text, "sco").strip() == text.strip()
    # The same line is English to an English cleaner, and French is thrown out of Scots.
    assert clean_ocr("Le roi et la reine sont dans la ville avec vous.\n", "sco").strip() == ""


def test_dehyphenate_joins_lowercase_continuation():
    assert dehyphenate("the pre-\nlattis of\nRome") == "the prelattis of\nRome"


def test_dehyphenate_keeps_hyphen_before_capital():
    assert dehyphenate("Anglo-\nSaxon") == "Anglo-\nSaxon"


def test_dehyphenate_joins_across_blank_lines_and_trailing_space():
    assert dehyphenate("the pre- \n\nlattis") == "the prelattis"


def test_dehyphenate_leaves_a_hyphen_at_the_end_of_the_text():
    assert dehyphenate("the pre-") == "the pre-"
    assert dehyphenate("the pre-\n\n") == "the pre-\n\n"


def test_clean_ocr_applies_dehyphenate():
    out = clean_ocr("the pre-\nlattis of the kirk", "en")
    assert "prelattis" in out


def test_marker_counts():
    mc = marker_counts("les rois sont dans la ville; the king and the queen; también")
    assert mc["fr"] == 3 and mc["en"] == 3 and mc["es"] == 1


def test_recipes_are_well_formed():
    for lang, sources in RECIPES.items():
        assert lang in MARKERS
        ids = [s.id for s in sources]
        assert len(ids) == len(set(ids)), lang
        for s in sources:
            assert s.kind in (G, IA)
            assert s.id and s.label
            if s.kind == G:
                assert s.id.isdigit()


def test_markers_are_disjoint():
    seen = {}
    for lang, ms in MARKERS.items():
        for m in ms:
            assert m not in seen, f"{m!r} in both {seen.get(m)} and {lang}"
            seen[m] = lang


def test_cleaner_stamp_round_trip(tmp_path):
    from cipherkit.corpora import CLEANER_VERSION, read_stamp, write_stamp

    assert CLEANER_VERSION == 2
    lang_dir = tmp_path / "xx"
    lang_dir.mkdir()
    assert read_stamp(str(lang_dir)) is None
    write_stamp(str(lang_dir))
    assert read_stamp(str(lang_dir)) == CLEANER_VERSION
    assert (lang_dir / ".cleaner").read_text().strip() == str(CLEANER_VERSION)


def test_text_refuses_missing_or_stale_stamp(tmp_path):
    import pytest

    from cipherkit.corpora import CLEANER_VERSION, text, write_stamp

    lang_dir = tmp_path / "xx"
    lang_dir.mkdir()
    (lang_dir / "a.txt").write_text("some words\n")
    with pytest.raises(RuntimeError, match=r"fetch xx --force"):
        text("xx", dest=str(tmp_path))
    (lang_dir / ".cleaner").write_text(f"{CLEANER_VERSION - 1}\n")
    with pytest.raises(RuntimeError, match=r"cleaner 1\b.*fetch xx --force"):
        text("xx", dest=str(tmp_path))
    write_stamp(str(lang_dir))
    assert text("xx", dest=str(tmp_path)) == "some words\n"


def test_text_still_reports_a_missing_corpus(tmp_path):
    import pytest

    from cipherkit.corpora import text

    with pytest.raises(FileNotFoundError, match=r"fetch xx"):
        text("xx", dest=str(tmp_path))
