import json
import os

import pytest
from PIL import Image, ImageDraw

from cipherkit.transcribe import (
    Row,
    align,
    compare,
    consensus,
    find_lines,
    ink_profile,
    layout,
    load_pass,
    review,
    save_pass,
    strips,
    tokens_match,
)


def test_tokens_match_and_alternatives():
    assert tokens_match("d53", "d53") == "agree"
    assert tokens_match("d53", "{d83/d53}") == "agree_alt"
    assert tokens_match("{d53/d55}", "{d83/d53}") == "agree_alt"
    assert tokens_match("d53", "d83") is None
    assert tokens_match("?", "?") == "agree"
    assert tokens_match("?", "d53") is None


def test_align_does_not_cascade_after_an_insertion():
    a = ["a1", "b2", "c3", "d4", "e5"]
    b = ["a1", "b2", "xx", "c3", "d4", "e5"]
    pairs = align(a, b)
    assert (None, 2) in pairs
    assert (2, 3) in pairs and (4, 5) in pairs


def test_compare_counts_and_disagreements():
    a = [Row(1, "h51 c20 c56 g12".split()), Row(2, "d53 f66 {g99/g98} ?".split())]
    b = [Row(1, "h51 c26 c56 g12 a1".split()), Row(2, "d53 f66 g98 d55".split())]
    c = compare(a, b, ("ctx", "blind"))
    assert c["agree"] == 5 and c["agree_via_alternative"] == 1 and c["differ"] == 2
    assert c["only_blind"] == 1 and c["only_ctx"] == 0
    assert c["disagreements"][0] == {"line": 1, "token": 2, "token_blind": 2, "ctx": "c20", "blind": "c26"}
    assert c["unpaired"] == [{"line": 1, "reader": "blind", "token": 5, "text": "a1"}]
    assert c["agreement_rate"] == round(6 / 8, 4)


def test_consensus_marks_disagreements_and_singletons():
    a = [Row(1, "h51 c20 {g99/g98} d55".split())]
    b = [Row(1, "h51 c26 g98".split())]
    out = consensus(a, b)
    assert out[0].tokens == ["h51", "{c20/c26}", "g98", "{d55/?}"]


def test_pass_file_roundtrip_and_text_format(tmp_path):
    rows = [Row(1, ["a1", "b2"]), Row(2, ["{c3/c4}", "?"])]
    p = str(tmp_path / "pass.json")
    save_pass(rows, p, status="test")
    assert load_pass(p) == rows
    assert json.load(open(p))["status"] == "test"
    t = tmp_path / "pass.txt"
    t.write_text("# comment\na1 b2\n\n{c3/c4} ?\n")
    assert load_pass(str(t)) == rows


@pytest.fixture
def page(tmp_path):
    im = Image.new("L", (400, 300), 255)
    d = ImageDraw.Draw(im)
    for k in range(5):
        d.text((20, 30 + k * 50), "d53 f66 g99 f61 d55 h41 a32 g98 d10 c56", fill=0)
    path = str(tmp_path / "page.png")
    im.save(path)
    return path


def test_find_lines_on_synthetic_page(page):
    im = Image.open(page)
    bands = find_lines(ink_profile(im), min_height=4)
    assert len(bands) == 5
    # Bands are widened to the valleys, so neighbours may touch; the pitch is what matters.
    for (t1, _), (t2, _) in zip(bands, bands[1:]):
        assert 40 < t2 - t1 < 60
    for k, (t, b) in enumerate(bands):
        assert t <= 30 + k * 50 <= b


def test_layout_strips_and_review(page, tmp_path):
    lay = layout(page, rotate=0.0, min_height=4, label="p1")
    assert len(lay["lines"]) == 5 and len(lay["source_sha256"]) == 64
    out = str(tmp_path / "strips")
    m = strips(lay, out)
    assert len(m["strips"]) == 5 and len(m["boards"]) == 2
    assert all(os.path.exists(os.path.join(out, e["file"])) for e in m["strips"])
    assert m["strips"][0]["source_box"][1] == lay["lines"][0][0]  # no rotate/scale: source coords recorded
    rows = [Row(k, "d53 f66 {g99/g98} ?".split()) for k in range(1, 6)]
    other = [Row(k, "d53 f60 g98 d10".split()) for k in range(1, 6)]
    cmp = compare(rows, other)
    page_html = review(lay, rows, key={"d53": "a", "f66": "u", "g98": "do"}, cmp=cmp, title="t")
    assert page_html.count("<section") == 5
    assert 'class="chip disputed"' in page_html and "data:image/jpeg;base64," in page_html
    assert "<span>a</span>" in page_html and "<span>?</span>" in page_html  # g99 not in key
