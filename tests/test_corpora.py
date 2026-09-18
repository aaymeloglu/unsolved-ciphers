from cipherkit.corpora import G, IA, MARKERS, RECIPES, clean_ocr, marker_counts


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
