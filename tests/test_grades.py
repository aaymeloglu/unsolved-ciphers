import pytest

from cipherkit.grades import GRADES, Reading, apply_key, counts, grade_token, render, summary_line


def test_grade_order_matches_conventions():
    assert GRADES == ("H", "C", "S", "M", "I")


def test_counts_always_has_five_grades():
    assert counts([]) == {"H": 0, "C": 0, "S": 0, "M": 0, "I": 0}


def test_counts_tallies_in_grade_order():
    rs = [Reading("1", "a", "H"), Reading("2", "b", "M"), Reading("3", "c", "H")]
    c = counts(rs)
    assert list(c) == list(GRADES)
    assert c == {"H": 2, "C": 0, "S": 0, "M": 1, "I": 0}


def test_counts_rejects_unknown_grade():
    with pytest.raises(ValueError):
        counts([Reading("x", "a", "Q")])


def test_counts_rejects_legacy_dash():
    with pytest.raises(ValueError):
        counts([Reading("8", "", "-")])


def test_render_convention():
    rs = [Reading("1", "a", "H"), Reading("2", "b", "M"), Reading("3", "c", "I"), Reading("|", "|", "H")]
    assert render(rs) == "a(b)[c]|"


def test_render_c_and_s_are_bare():
    rs = [Reading("1", "x", "C"), Reading("2", "y", "S")]
    assert render(rs) == "xy"


def test_render_gap_token_passes_through_whatever_its_grade():
    rs = [Reading("1", "a", "H"), Reading("|", "|", "M"), Reading("2", "b", "H")]
    assert render(rs) == "a|b"
    assert render(rs, gap=" ") == "a(|)b"


def test_grade_token_reads_the_key_shape():
    key = {"1": {"value": "a", "grade": "H", "from": "Ziffra prima"}}
    assert grade_token("1", key) == Reading("1", "a", "H", "Ziffra prima")


def test_grade_token_missing_defaults_to_M():
    assert grade_token("9", {"1": {"value": "a", "grade": "H"}}) == Reading("9", "?", "M")


def test_grade_token_missing_honours_default_grade():
    assert grade_token("9", {}, default_grade="I") == Reading("9", "?", "I")


def test_grade_token_rejects_bad_grade_in_key():
    with pytest.raises(ValueError):
        grade_token("1", {"1": {"value": "a", "grade": "-"}})


def test_grade_token_key_entry_without_grade_takes_default():
    assert grade_token("1", {"1": {"value": "a"}}, default_grade="H") == Reading("1", "a", "H")


def test_apply_key_is_grade_token_over_tokens():
    key = {"1": {"value": "a", "grade": "S"}}
    assert apply_key(["1", "2"], key) == [Reading("1", "a", "S"), Reading("2", "?", "M")]
    assert apply_key(["2"], key, default_grade="I") == [Reading("2", "?", "I")]


def test_summary_line():
    assert summary_line({"H": 1537, "C": 0, "S": 0, "M": 48, "I": 54}) == "1537 H, 0 C, 0 S, 48 M, 54 I"


def test_summary_line_fills_missing_grades_with_zero():
    assert summary_line({"S": 204, "I": 3}) == "0 H, 0 C, 204 S, 0 M, 3 I"
