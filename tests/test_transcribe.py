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
    gaps,
    ink_profile,
    layout,
    load_pass,
    page_bounds,
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


# ---------------------------------------------------------------- framed photographs

def _framed_page(lines=5, frame=60):
    """A pale page inside a dark frame, as a photographed manuscript comes: paper 480 x 680 at
    (60, 60) in a 600 x 800 image, five heavy bars of ink 400 px wide."""
    im = Image.new("L", (600, 800), 20)
    page = Image.new("L", (600 - 2 * frame, 800 - 2 * frame), 245)
    d = ImageDraw.Draw(page)
    for i in range(lines):
        d.rectangle([40, 80 + i * 90, 440, 80 + i * 90 + 18], fill=0)
    im.paste(page, (frame, frame))
    return im


def test_page_bounds_finds_paper():
    l, t, r, b = page_bounds(_framed_page())
    assert abs(l - 60) <= 4 and abs(t - 60) <= 4 and abs(r - 540) <= 4 and abs(b - 740) <= 4


def test_page_bounds_without_frame_is_full_image():
    im = Image.new("L", (300, 200), 240)
    ImageDraw.Draw(im).rectangle([20, 50, 200, 60], fill=0)
    assert page_bounds(im) == (0, 0, 300, 200)


def test_page_bounds_ignores_ruler_and_uneven_frame():
    """A bright strip along one edge (a ruler) and a thicker bottom frame: the paper is the
    largest bright run, not the run touching the edge."""
    im = Image.new("L", (600, 800), 20)
    page = Image.new("L", (480, 600), 245)
    im.paste(page, (60, 60))
    ImageDraw.Draw(im).rectangle([0, 780, 599, 799], fill=230)   # ruler along the bottom edge
    l, t, r, b = page_bounds(im)
    assert abs(l - 60) <= 4 and abs(t - 60) <= 4 and abs(r - 540) <= 4 and abs(b - 660) <= 4


def test_layout_auto_crop_counts_lines(tmp_path):
    """Without a crop the frame rows and the heavy ink rows are both darker than find_lines'
    border level, so every line is masked as a scan edge and the detector finds nothing."""
    p = tmp_path / "f.png"
    _framed_page().save(p)
    assert len(layout(str(p), crop=None, rotate=0.0)["lines"]) != 5
    lay = layout(str(p), crop="auto", rotate=0.0)
    assert len(lay["lines"]) == 5
    box = lay["processing"]["crop"]
    assert isinstance(box, list) and len(box) == 4 and abs(box[0] - 60) <= 4 and abs(box[1] - 60) <= 4
    assert lay["processed_size"] == [box[2] - box[0], box[3] - box[1]]


def test_layout_auto_crop_then_strips_round_trip(tmp_path):
    p = tmp_path / "f.png"
    _framed_page().save(p)
    lay = layout(str(p), crop="auto", rotate=0.0)
    m = strips(lay, str(tmp_path / "strips"))
    assert len(m["strips"]) == 5
    assert m["strips"][0]["source_box"][0] == lay["processing"]["crop"][0]


def test_gaps_between_words():
    """Gaps are half-open column ranges [x0, x1): x0 is the first blank column after an inked
    one, x1 the next inked column. Bars at 10..50, 80..120, 200..240 (inclusive)."""
    strip = Image.new("L", (300, 30), 245)
    d = ImageDraw.Draw(strip)
    for x0 in (10, 80, 200):
        d.rectangle([x0, 5, x0 + 40, 25], fill=0)
    assert gaps(strip, min_gap=12) == [(51, 80), (121, 200)]
    assert gaps(strip, min_gap=30) == [(121, 200)]
    assert gaps(Image.new("L", (100, 20), 245)) == []


def test_gaps_min_ink_ignores_specks():
    strip = Image.new("L", (300, 40), 245)
    d = ImageDraw.Draw(strip)
    d.rectangle([10, 5, 50, 35], fill=0)
    d.rectangle([200, 5, 240, 35], fill=0)
    d.point((120, 20), fill=0)          # one dark pixel in a 40-row column: 2.5 %
    assert gaps(strip, min_gap=12, min_ink=0.05) == [(51, 200)]
    assert gaps(strip, min_gap=12, min_ink=0.02) == [(51, 120), (121, 200)]


def test_gaps_cli_prints_json(tmp_path, capsys):
    from cipherkit.transcribe import main
    strip = Image.new("L", (300, 30), 245)
    d = ImageDraw.Draw(strip)
    for x0 in (10, 80, 200):
        d.rectangle([x0, 5, x0 + 40, 25], fill=0)
    p = str(tmp_path / "s.png")
    strip.save(p)
    assert main(["gaps", p, "--min-gap", "12"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["gaps"] == [[51, 80], [121, 200]] and out["ink_span"] == [10, 241] and out["dark"] is None


def test_gaps_dark_threshold_ignores_show_through(tmp_path, capsys):
    """Two words of black ink with a broad mid-grey smudge between them (writing showing through
    from the other side of the leaf). The strip's own histogram midpoint counts the smudge as
    ink; an explicit `dark` below its level does not."""
    from cipherkit.transcribe import main
    strip = Image.new("L", (400, 40), 245)
    d = ImageDraw.Draw(strip)
    d.rectangle([10, 5, 60, 35], fill=0)
    d.rectangle([300, 5, 350, 35], fill=0)
    d.rectangle([120, 10, 240, 30], fill=150)
    assert gaps(strip, min_gap=12, min_ink=0.1) == [(61, 120), (241, 300)]
    assert gaps(strip, min_gap=12, min_ink=0.1, dark=100) == [(61, 300)]
    p = str(tmp_path / "s.png")
    strip.save(p)
    assert main(["gaps", p, "--dark", "100"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["gaps"] == [[61, 300]] and out["dark"] == 100
