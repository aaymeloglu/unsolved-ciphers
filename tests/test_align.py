import pytest

from cipherkit.align import Assignment, align_rows, apply, holdout, read_tsv


def test_align_rows_majority_and_conflicts():
    rows = [{"id": "A", "cipher": "1 2 3", "plain": "abc", "evidence": ""},
            {"id": "B", "cipher": "1 2 4", "plain": "abd", "evidence": ""},
            {"id": "C", "cipher": "1 5", "plain": "xz", "evidence": ""}]
    key = align_rows(rows)
    assert key["1"].plain == "a" and key["1"].conflicts == [("C:1", "x")]
    assert key["4"].occurrences == ["B:3"]


def test_align_rows_majority_ties_first_seen_and_all_occurrences_kept():
    rows = [{"id": "A", "cipher": "7", "plain": "x", "evidence": ""},
            {"id": "B", "cipher": "7", "plain": "y", "evidence": ""}]
    key = align_rows(rows)
    assert key["7"].plain == "x"
    assert key["7"].occurrences == ["A:1", "B:1"]
    assert key["7"].conflicts == [("B:1", "y")]
    assert isinstance(key["7"], Assignment) and key["7"].symbol == "7"


def test_align_rows_fold_applies_to_plain():
    rows = [{"id": "A", "cipher": "1 2", "plain": "vu", "evidence": ""}]
    key = align_rows(rows, fold=lambda s: s.replace("v", "u"))
    assert key["1"].plain == "u" and key["2"].plain == "u"


def test_align_rows_length_mismatch_names_row():
    with pytest.raises(ValueError, match="B"):
        align_rows([{"id": "B", "cipher": "1 2", "plain": "abc", "evidence": ""}])


def test_apply_and_unknown():
    assert apply(["1", "9", "2"], {"1": "a", "2": "b"}) == "a?b"
    assert apply(["1", "9"], {"1": "a"}, unknown="_") == "a_"
    key = align_rows([{"id": "A", "cipher": "1 2", "plain": "ab", "evidence": ""}])
    assert apply(["2", "1"], {s: a.plain for s, a in key.items()}) == "ba"


def test_holdout_counts():
    key = {"1": "a", "2": "b"}
    r = holdout([{"id": "V", "cipher": "1 2 1", "plain": "abz", "evidence": ""}], key)
    assert r["positions"] == 3 and r["agree"] == 2 and r["mismatches"][0][3:] == ("z", "a")


def test_holdout_unknown_units_and_fold():
    key = {"1": "u"}
    r = holdout([{"id": "V", "cipher": "1 9", "plain": "vb", "evidence": ""}], key,
                fold=lambda s: s.replace("v", "u"))
    assert r["positions"] == 2 and r["agree"] == 1
    assert r["mismatches"] == [("V", 2, "9", "b", None)]


def test_holdout_length_mismatch_names_row():
    with pytest.raises(ValueError, match="V9"):
        holdout([{"id": "V9", "cipher": "1", "plain": "ab", "evidence": ""}], {"1": "a"})


def test_read_tsv(tmp_path):
    p = tmp_path / "rows.tsv"
    p.write_text("id\tcipher\tplain\tevidence\nA01\t0 4\tad\tR954 L09\n")
    rows = read_tsv(p)
    assert rows == [{"id": "A01", "cipher": "0 4", "plain": "ad", "evidence": "R954 L09"}]
    key = align_rows(rows)
    assert key["0"].plain == "a" and key["4"].occurrences == ["A01:2"]
