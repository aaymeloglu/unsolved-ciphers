"""Transcription tooling: the steps we did by hand for Ottobon and Debosnys, as commands.

    python -m cipherkit.transcribe layout  page.jpg -o f38r.layout.json [--crop l,t,r,b | --crop auto] [--rotate -3] [--scale 1.5]
    python -m cipherkit.transcribe strips  f38r.layout.json -o strips/
    python -m cipherkit.transcribe gaps    strips/f38r-L03.png [--min-gap 12] [--min-ink 0.02] [--dark 100]
    python -m cipherkit.transcribe compare passA.json passB.json -o compare.json
    python -m cipherkit.transcribe consensus passA.json passB.json -o passC.json
    python -m cipherkit.transcribe review  f38r.layout.json passA.json -o review.html [--key key.json] [--compare compare.json]

layout     finds the text lines of a page by its horizontal ink profile and writes a layout file
           (crop, rotation, scale, one [top, bottom] band per line) plus a preview PNG with the
           bands drawn. Edit the bands by hand where the detector is wrong; the file is the record.
           `--crop auto` first finds the paper inside a dark frame (a photographed page), since the
           frame defeats both the deskew and the line finder; the box chosen is recorded.
strips     cuts one PNG per line and contact-sheet boards of four lines with labels, and writes a
           manifest with the source file's SHA-256 and every box, so a crop can be cited as evidence.
gaps       measures the word gaps in one line strip: the column runs with no ink between the first
           and last inked column, so a "|" in a transcription can be checked against the page.
           Pass `--dark` (0-255 on the contrast-stretched strip) when the page shows through from
           the other side or the strip is nearly blank: the strip's own histogram then puts the
           ink threshold between paper and show-through, and every faint column counts as ink.
compare    aligns two independent passes token by token per line (insertions and deletions do not
           cascade) and counts agreement, agreement through a `{a/b}` alternative, and disagreement.
consensus  writes a third pass: agreed tokens as they are, disagreements as `{a/b}`, tokens only one
           reader has as `{a/?}`. This is the input to the next reading round.
review     builds a self-contained HTML page: per line the strip, a chip per token with its key
           value if a key is given, disputed chips highlighted from a compare file.

Pass files are JSON `{"rows": [{"line": 1, "tokens": "d10 h40 {d53/d83} ?"}, ...]}` (the
Ottobon format) or plain text, one line of tokens per row, `#` for comments. `{a/b}` marks
alternatives, `?` an unread sign.

Never run this on images whose licence forbids
redistribution and then commit the strips; the manifest records where every pixel came from.
"""
from __future__ import annotations

import base64
import hashlib
import html
import io
import json
import os
import sys
from typing import NamedTuple

# ---------------------------------------------------------------- pass files

class Row(NamedTuple):
    line: int
    tokens: list[str]


def load_pass(path: str) -> list[Row]:
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if path.endswith(".json"):
        data = json.loads(text)
        rows = data["rows"] if isinstance(data, dict) else data
        return [Row(int(r["line"]), str(r["tokens"]).split()) for r in rows]
    out = []
    n = 0
    for ln in text.splitlines():
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        n += 1
        out.append(Row(n, s.split()))
    return out


def save_pass(rows: list[Row], path: str, **meta) -> None:
    data = dict(meta)
    data["rows"] = [{"line": r.line, "tokens": " ".join(r.tokens)} for r in rows]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write("\n")


def alternatives(token: str) -> set[str]:
    if token.startswith("{") and token.endswith("}"):
        return set(token[1:-1].split("/"))
    return {token}


def tokens_match(a: str, b: str) -> str | None:
    """'agree' if identical, 'agree_alt' if they share a reading through alternatives, else None."""
    if a == b:
        return "agree"
    if a == "?" or b == "?":
        return None
    if alternatives(a) & alternatives(b):
        return "agree_alt"
    return None


# ---------------------------------------------------------------- alignment

def align(a: list[str], b: list[str]) -> list[tuple[int | None, int | None]]:
    """Needleman-Wunsch over two token lists. Returns index pairs; None marks a gap."""
    n, m = len(a), len(b)
    gap = -1
    score = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        score[i][0] = i * gap
    for j in range(1, m + 1):
        score[0][j] = j * gap
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            kind = tokens_match(a[i - 1], b[j - 1])
            s = 2 if kind == "agree" else 1 if kind == "agree_alt" else -1
            score[i][j] = max(score[i - 1][j - 1] + s, score[i - 1][j] + gap, score[i][j - 1] + gap)
    pairs = []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            kind = tokens_match(a[i - 1], b[j - 1])
            s = 2 if kind == "agree" else 1 if kind == "agree_alt" else -1
            if score[i][j] == score[i - 1][j - 1] + s:
                pairs.append((i - 1, j - 1))
                i, j = i - 1, j - 1
                continue
        if i > 0 and score[i][j] == score[i - 1][j] + gap:
            pairs.append((i - 1, None))
            i -= 1
        else:
            pairs.append((None, j - 1))
            j -= 1
    return pairs[::-1]


def compare(a_rows: list[Row], b_rows: list[Row], names=("a", "b")) -> dict:
    """Per-line alignment of two passes. Counts are over aligned token pairs; a token present
    in only one pass is listed under `unpaired` and counts as a disagreement."""
    b_by_line = {r.line: r for r in b_rows}
    na, nb = names
    counts = {"agree": 0, "agree_alt": 0, "differ": 0, "only_" + na: 0, "only_" + nb: 0}
    disagreements, unpaired = [], []
    lines_only_a = [r.line for r in a_rows if r.line not in b_by_line]
    lines_only_b = [r.line for r in b_rows if r.line not in {x.line for x in a_rows}]
    for ra in a_rows:
        rb = b_by_line.get(ra.line)
        if rb is None:
            continue
        for i, j in align(ra.tokens, rb.tokens):
            if i is None:
                counts["only_" + nb] += 1
                unpaired.append({"line": ra.line, "reader": nb, "token": j + 1, "text": rb.tokens[j]})
            elif j is None:
                counts["only_" + na] += 1
                unpaired.append({"line": ra.line, "reader": na, "token": i + 1, "text": ra.tokens[i]})
            else:
                kind = tokens_match(ra.tokens[i], rb.tokens[j]) or "differ"
                counts[kind] += 1
                if kind == "differ":
                    disagreements.append({"line": ra.line, "token": i + 1, "token_" + nb: j + 1,
                                          na: ra.tokens[i], nb: rb.tokens[j]})
    paired = counts["agree"] + counts["agree_alt"] + counts["differ"]
    return {
        "readers": list(names),
        "paired_tokens": paired,
        "agree": counts["agree"],
        "agree_via_alternative": counts["agree_alt"],
        "differ": counts["differ"],
        "only_" + na: counts["only_" + na],
        "only_" + nb: counts["only_" + nb],
        "agreement_rate": round((counts["agree"] + counts["agree_alt"]) / paired, 4) if paired else None,
        "lines_only_" + na: lines_only_a,
        "lines_only_" + nb: lines_only_b,
        "disagreements": disagreements,
        "unpaired": unpaired,
    }


def consensus(a_rows: list[Row], b_rows: list[Row]) -> list[Row]:
    """Agreed tokens as they are; disagreements as `{a/b}`; a token only one reader has as `{x/?}`."""
    b_by_line = {r.line: r for r in b_rows}
    out = []
    for ra in a_rows:
        rb = b_by_line.get(ra.line)
        if rb is None:
            out.append(ra)
            continue
        toks = []
        for i, j in align(ra.tokens, rb.tokens):
            if i is None:
                toks.append("{" + rb.tokens[j] + "/?}")
            elif j is None:
                toks.append("{" + ra.tokens[i] + "/?}")
            else:
                x, y = ra.tokens[i], rb.tokens[j]
                kind = tokens_match(x, y)
                if kind == "agree":
                    toks.append(x)
                elif kind == "agree_alt":
                    common = sorted(alternatives(x) & alternatives(y))
                    toks.append(common[0] if len(common) == 1 else "{" + "/".join(common) + "}")
                else:
                    alts = []
                    for t in (x, y):
                        for alt in sorted(alternatives(t)):
                            if alt not in alts:
                                alts.append(alt)
                    toks.append("{" + "/".join(alts) + "}")
        out.append(Row(ra.line, toks))
    for rb in b_rows:
        if rb.line not in {r.line for r in a_rows}:
            out.append(rb)
    return sorted(out, key=lambda r: r.line)


# ---------------------------------------------------------------- images

def _pil():
    from PIL import Image, ImageDraw, ImageOps
    return Image, ImageDraw, ImageOps


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def prepare(image, crop=None, rotate=0.0, scale=1.0):
    """Apply the layout's processing chain in a fixed order: crop, rotate, scale."""
    Image, _, _ = _pil()
    im = image
    if crop:
        im = im.crop(tuple(crop))
    if rotate:
        im = im.rotate(rotate, Image.Resampling.BICUBIC, expand=False, fillcolor="white")
    if scale and scale != 1:
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
    return im


def _gray(image):
    """Grayscale, contrast-stretched copy: the form every measurement below works on."""
    _, _, ImageOps = _pil()
    return ImageOps.autocontrast(image.convert("L"))


def _split_level(g) -> int:
    """Threshold between paper and ink: midpoint of the two histogram mass centres, one pass."""
    hist = g.histogram()
    total = sum(hist)
    mean = sum(i * c for i, c in enumerate(hist)) / total
    low = [c for c in hist[: int(mean)]]
    high = hist[int(mean):]
    m_low = sum(i * c for i, c in enumerate(low)) / max(1, sum(low))
    m_high = sum((int(mean) + i) * c for i, c in enumerate(high)) / max(1, sum(high))
    return int((m_low + m_high) / 2)


def ink_profile(image, dark: int | None = None) -> list[float]:
    """Fraction of dark pixels in each pixel row of a grayscale image."""
    g = _gray(image)
    w, h = g.size
    px = g.load()
    if dark is None:
        dark = _split_level(g)
    return [sum(px[x, y] < dark for x in range(w)) / w for y in range(h)]


def _paper_run(means: list[float], bright: float, margin: int) -> tuple[int, int]:
    """[start, end) of the paper along one axis, given the mean brightness of each row (or
    column). Rows brighter than `bright` are paper. A dark run touching an image edge is frame
    when it is at least `margin` thick (thinner is a scan edge). A dark run inside the image is
    frame only when it is at least a tenth of the extent (the gutter of an open book, the frame
    beyond a ruler laid along the edge); thinner interior dark runs are writing or ruled lines.
    The paper is the longest bright run between frames. With no frame the full extent is
    returned."""
    n = len(means)
    dark = [m <= bright for m in means]
    runs, start = [], None
    for i, d in enumerate(dark + [False]):
        if d and start is None:
            start = i
        elif not d and start is not None:
            runs.append((start, i))
            start = None
    frame = [(a, b) for a, b in runs if b - a >= (margin if a == 0 or b == n else max(margin, n // 10))]
    if not frame:
        return 0, n
    best, cursor = (0, 0), 0
    for a, b in frame + [(n, n)]:
        if a - cursor > best[1] - best[0]:
            best = (cursor, a)
        cursor = b
    return best


def _frame_and_paper_levels(g, margin: int) -> tuple[float, float]:
    """(frame, paper) brightness: the median of the outermost `margin` rows and columns, and
    the median of the whole image, which the page dominates."""
    w, h = g.size
    px = g.load()
    m = max(1, min(margin, w // 2, h // 2))
    edge = [px[x, y] for y in range(h) for x in range(w) if x < m or x >= w - m or y < m or y >= h - m]
    edge.sort()
    hist = g.histogram()
    half, acc, paper = sum(hist) / 2, 0, 0
    for v, c in enumerate(hist):
        acc += c
        if acc >= half:
            paper = v
            break
    return edge[len(edge) // 2], paper


def page_bounds(image, margin: int = 8, bright: int | None = None) -> tuple[int, int, int, int]:
    """(left, top, right, bottom) of the paper inside a dark frame, as a PIL crop box (right and
    bottom exclusive): the largest run of columns, then of rows within those columns, whose
    mean brightness exceeds `bright`. The default `bright` is the midpoint between the frame
    level (median of the outermost `margin` rows and columns) and the paper level (median of
    the image, which the page dominates); the ink-profile histogram midpoint is too high for a
    photographed page whose brightness falls off towards one side. A dark border thinner than
    `margin` pixels is a scan edge, not a frame, and a dark band inside the page thinner than a
    tenth of the image is writing, not a frame. Returns the full image when no frame is found:
    no dark run thick enough, or a border no darker than the page (contrast under 32 of 255)."""
    g = _gray(image)
    w, h = g.size
    if bright is None:
        frame, paper = _frame_and_paper_levels(g, margin)
        if paper - frame < 32:
            return 0, 0, w, h
        bright = (frame + paper) / 2
    px = g.load()
    col_means = [sum(px[x, y] for y in range(h)) / h for x in range(w)]
    left, right = _paper_run(col_means, bright, margin)
    row_means = [sum(px[x, y] for x in range(left, right)) / (right - left) for y in range(h)]
    top, bottom = _paper_run(row_means, bright, margin)
    return left, top, right, bottom


def _smooth(values: list[float], win: int) -> list[float]:
    out = []
    for y in range(len(values)):
        lo, hi = max(0, y - win), min(len(values), y + win + 1)
        out.append(sum(values[lo:hi]) / (hi - lo))
    return out


def _percentile(values: list[float], q: float) -> float:
    ranked = sorted(values)
    return ranked[min(len(ranked) - 1, int(q * len(ranked)))]


def _runs_above(values: list[float], cut: float) -> list[list[int]]:
    bands, start = [], None
    for y, v in enumerate(values + [-1.0]):
        if v >= cut and start is None:
            start = y
        elif v < cut and start is not None:
            bands.append([start, y])
            start = None
    return bands


def find_lines(profile: list[float], min_height: int = 8, min_gap: int = 3,
               threshold: float = 0.35, pad: int = 2, border: float = 0.85,
               expand: float = 0.45) -> list[list[int]]:
    """Bands [top, bottom] of text lines, in two stages. Rows darker than `border` (scan
    edges, binding shadow) are ignored. Stage one finds text blocks with heavy smoothing
    against the page's paper level. Stage two splits each block at its own valleys: the cut
    sits `threshold` of the way from the block's paper level (10th percentile) to its ink
    level (90th percentile), with light smoothing. Bands closer than `min_gap` merge; bands
    shorter than `min_height` are dropped. Run `deskew` first: a skew of one degree over a
    thousand pixels smears every valley."""
    if not profile:
        return []
    # Border rows (scan edges, binding shadow) and their neighbourhood: after deskewing, the
    # edge of the page is a ramp of partly dark rows, so mask a margin around every border row.
    margin = max(3, len(profile) // 50)
    prof = list(profile)
    for y, v in enumerate(profile):
        if v >= border:
            for k in range(max(0, y - margin), min(len(prof), y + margin + 1)):
                prof[k] = 0.0
    heavy = _smooth(prof, max(3, len(prof) // 200))
    paper = _percentile(heavy, 0.5)
    ink = _percentile(heavy, 0.95)
    if ink <= paper:
        return []
    blocks = [b for b in _runs_above(heavy, paper + 0.3 * (ink - paper)) if b[1] - b[0] >= min_height]
    light = _smooth(prof, max(1, len(prof) // 600))
    bands = []
    for top, bottom in blocks:
        seg = light[top:bottom]
        lo, hi = _percentile(seg, 0.10), _percentile(seg, 0.90)
        cut = lo + threshold * (hi - lo)
        for a, b in _runs_above(seg, cut):
            bands.append([top + a, top + b])
    merged = []
    for b in bands:
        if merged and b[0] - merged[-1][1] < min_gap:
            merged[-1][1] = b[1]
        else:
            merged.append(b)
    # A text line never touches the scan edge; a band that does is the page border.
    crests = [b for b in merged if b[1] - b[0] >= min_height and b[0] > 0 and b[1] < len(prof)]
    if not crests:
        return []
    # A crest is the dense core of a line. Widen each to the midpoint of the gap on either
    # side (capped at `expand` of the median pitch) so strips keep ascenders, descenders and
    # superscript numbers, which is what a transcriber needs to see.
    pitches = [b[0] - a[0] for a, b in zip(crests, crests[1:])]
    pitch = sorted(pitches)[len(pitches) // 2] if pitches else (crests[0][1] - crests[0][0]) * 2
    cap = int(expand * pitch)
    out = []
    for k, (t, b) in enumerate(crests):
        up = (t - crests[k - 1][1]) // 2 if k else cap
        down = (crests[k + 1][0] - b) // 2 if k + 1 < len(crests) else cap
        out.append([max(0, t - min(cap, up) - pad), min(len(prof), b + min(cap, down) + pad)])
    return out


def deskew(image, limit: float = 4.0, step: float = 0.25) -> float:
    """Rotation (degrees, counter-clockwise positive as PIL uses it) that makes the ink
    profile sharpest: the angle maximising the profile's variance, searched on a copy no
    wider than 600 px. A skewed page smears line valleys into one block."""
    Image, _, _ = _pil()
    g = image.convert("L")
    if g.width > 600:
        g = g.resize((600, round(g.height * 600 / g.width)), Image.Resampling.BILINEAR)
    # Central 70 % only: scan borders and the white corners that rotation brings in would
    # otherwise dominate the variance and push the search to its limit.
    w, h = g.size
    g = g.crop((int(0.15 * w), int(0.15 * h), int(0.85 * w), int(0.85 * h)))
    best, best_var = 0.0, -1.0
    n = int(round(2 * limit / step)) + 1
    for k in range(n):
        ang = -limit + k * step
        prof = ink_profile(prepare(g, None, ang, 1.0))
        prof = [0.0 if v >= 0.85 else v for v in prof]
        mean = sum(prof) / len(prof)
        var = sum((v - mean) ** 2 for v in prof) / len(prof)
        if var > best_var:
            best, best_var = ang, var
    return best


def layout(image_path: str, crop=None, rotate: float | None = None, scale=1.0,
           label: str | None = None, **kw) -> dict:
    """rotate=None means deskew automatically; pass 0.0 to keep the page as it is. crop is a
    box (l, t, r, b), None for the whole image, or "auto" to take page_bounds of the source
    (the paper inside a dark photograph frame); the box used is recorded in processing["crop"]."""
    Image, _, _ = _pil()
    src = Image.open(image_path)
    if crop == "auto":
        crop = list(page_bounds(src))
    if rotate is None:
        rotate = deskew(src.crop(tuple(crop)) if crop else src)
    im = prepare(src, crop, rotate, scale)
    bands = find_lines(ink_profile(im), **kw)
    return {
        "label": label or os.path.splitext(os.path.basename(image_path))[0],
        "source": image_path,
        "source_sha256": sha256_file(image_path),
        "source_size": list(Image.open(image_path).size),
        "processing": {"crop": list(crop) if crop else None, "rotate": rotate, "scale": scale,
                       "order": "crop, rotate about centre, scale"},
        "processed_size": [im.width, im.height],
        "lines": bands,
        "note": "Bands are [top, bottom] in processed coordinates. Edit by hand where the detector is wrong.",
    }


def draw_preview(lay: dict, out_path: str) -> None:
    Image, ImageDraw, _ = _pil()
    im = prepare(Image.open(lay["source"]), lay["processing"]["crop"], lay["processing"]["rotate"],
                 lay["processing"]["scale"]).convert("RGB")
    d = ImageDraw.Draw(im)
    for k, (top, bottom) in enumerate(lay["lines"], 1):
        d.rectangle([0, top, im.width - 1, bottom], outline=(200, 40, 40), width=2)
        d.text((6, top + 2), f"L{k:02d}", fill=(200, 40, 40))
    im.save(out_path)


def strips(lay: dict, out_dir: str, board_rows: int = 4) -> dict:
    Image, ImageDraw, _ = _pil()
    os.makedirs(out_dir, exist_ok=True)
    proc = lay["processing"]
    im = prepare(Image.open(lay["source"]), proc["crop"], proc["rotate"], proc["scale"])
    entries = []
    for k, (top, bottom) in enumerate(lay["lines"], 1):
        name = f"{lay['label']}-L{k:02d}.png"
        strip = im.crop((0, top, im.width, bottom))
        strip.save(os.path.join(out_dir, name))
        entry = {"line": k, "file": name, "processed_box": [0, top, im.width, bottom]}
        if not proc["rotate"] and (proc["scale"] or 1) == 1:
            ox, oy = (proc["crop"] or [0, 0])[:2]
            entry["source_box"] = [ox, oy + top, ox + im.width, oy + bottom]
        entries.append(entry)
    boards = []
    for start in range(0, len(entries), board_rows):
        chunk = entries[start : start + board_rows]
        ims = [Image.open(os.path.join(out_dir, e["file"])) for e in chunk]
        board = Image.new("RGB", (max(i.width for i in ims) + 70, sum(i.height + 20 for i in ims)), "white")
        d = ImageDraw.Draw(board)
        y = 0
        for e, s in zip(chunk, ims):
            d.text((5, y + 10), f"L{e['line']:02d}", fill=(200, 40, 40))
            board.paste(s, (65, y))
            y += s.height + 20
        name = f"{lay['label']}-board{start // board_rows + 1}.png"
        board.save(os.path.join(out_dir, name))
        boards.append(name)
    manifest = {
        "label": lay["label"], "source": lay["source"], "source_sha256": lay["source_sha256"],
        "processing": proc, "strips": entries, "boards": boards,
        "note": "processed_box is in the coordinates of the processed image; source_box, when present, "
                "is in the original file's pixel coordinates.",
    }
    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1)
        f.write("\n")
    return manifest


# ---------------------------------------------------------------- word gaps

def gaps(strip, min_gap: int = 12, min_ink: float = 0.02, dark: int | None = None) -> list[tuple[int, int]]:
    """Column runs with no ink inside a line strip: [(x0, x1), ...] between the first and the
    last inked column. A column is inked when its dark-pixel fraction is >= `min_ink` (`dark`
    is the ink threshold, default as ink_profile). Each gap is half-open, [x0, x1): x0 is the
    first blank column after an inked one, x1 the next inked column, so x1 - x0 is the gap's
    width and strip.crop((x0, 0, x1, h)) is exactly the blank. Runs shorter than `min_gap`
    columns are not gaps. Blank columns before the first or after the last ink are margins,
    not gaps. A strip with no ink returns []."""
    g = _gray(strip)
    w, h = g.size
    px = g.load()
    if dark is None:
        dark = _split_level(g)
    inked = [sum(px[x, y] < dark for y in range(h)) / h >= min_ink for x in range(w)]
    if not any(inked):
        return []
    first = inked.index(True)
    last = w - 1 - inked[::-1].index(True)
    out, start = [], None
    for x in range(first, last + 1):
        if not inked[x] and start is None:
            start = x
        elif inked[x] and start is not None:
            if x - start >= min_gap:
                out.append((start, x))
            start = None
    return out


def _inked_span(strip, min_ink: float = 0.02, dark: int | None = None) -> list[int] | None:
    """[first, last + 1) of the inked columns, or None."""
    g = _gray(strip)
    w, h = g.size
    px = g.load()
    if dark is None:
        dark = _split_level(g)
    inked = [sum(px[x, y] < dark for y in range(h)) / h >= min_ink for x in range(w)]
    if not any(inked):
        return None
    return [inked.index(True), w - inked[::-1].index(True)]


# ---------------------------------------------------------------- review page

def review(lay: dict, rows: list[Row], key: dict | None = None, cmp: dict | None = None,
           title: str | None = None, attribution: str = "") -> str:
    Image, _, _ = _pil()
    proc = lay["processing"]
    im = prepare(Image.open(lay["source"]), proc["crop"], proc["rotate"], proc["scale"])
    disputed = {}
    if cmp:
        for d in cmp["disagreements"]:
            other = cmp["readers"][1]
            disputed[(d["line"], d["token"])] = f"{other}: {d[other]}"
        for u in cmp["unpaired"]:
            if u["reader"] == cmp["readers"][0]:
                disputed[(u["line"], u["token"])] = f"not read by {cmp['readers'][1]}"
    cards = []
    for row in rows:
        band = lay["lines"][row.line - 1] if row.line - 1 < len(lay["lines"]) else None
        img = ""
        if band:
            b = io.BytesIO()
            im.crop((0, band[0], im.width, band[1])).convert("RGB").save(b, format="JPEG", quality=90)
            img = (f'<img alt="line {row.line}" src="data:image/jpeg;base64,'
                   f'{base64.b64encode(b.getvalue()).decode()}">')
        chips = []
        for i, tok in enumerate(row.tokens, 1):
            note = disputed.get((row.line, i), "")
            cls = "chip disputed" if note else "chip"
            if "?" in tok or tok.startswith("{"):
                cls += " uncertain"
            val = ""
            if key is not None:
                v = key.get(tok)
                val = "<span>" + html.escape(v if v else ("∅" if v == "" else "?")) + "</span>"
            chips.append(f'<button class="{cls}" title="{html.escape(note)}"><b>{html.escape(tok)}</b>{val}</button>')
        cards.append(f'<section id="L{row.line}"><h2>Line {row.line}</h2>{img}'
                     f'<div class="chips">{"".join(chips)}</div></section>')
    summary = ""
    if cmp:
        summary = (f'<p>Compared with a second reading: {cmp["agree"]} tokens agree, '
                   f'{cmp["agree_via_alternative"]} agree through an alternative, {cmp["differ"]} differ, '
                   f'{cmp["only_" + cmp["readers"][0]]} + {cmp["only_" + cmp["readers"][1]]} unpaired. '
                   f'Amber chips differ; hover or click for the other reading.</p>')
    title = title or f'{lay["label"]}: transcription review'
    nav = "".join(f'<a href="#L{r.line}">{r.line}</a>' for r in rows)
    return f'''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(title)}</title>
<style>
:root{{--bg:#faf9f5;--fg:#1b2835;--card:#fff;--line:#d8d8d0;--chip:#f2f7fa;--chipb:#bed2dc;--amber:#fff6dc;--amberb:#c58c22;--grey:#eee}}
@media (prefers-color-scheme:dark){{:root:not([data-theme=light]){{--bg:#14181c;--fg:#e6e6e0;--card:#1d2328;--line:#333;--chip:#243039;--chipb:#3d5566;--amber:#4a3a10;--amberb:#d9a441;--grey:#2a2f34}}}}
body{{max-width:1200px;margin:32px auto;padding:0 16px;font:17px/1.55 system-ui;color:var(--fg);background:var(--bg)}}
h1{{font-size:28px;line-height:1.2}}h2{{font-size:19px}}section{{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:16px;margin:20px 0}}
img{{width:100%;height:auto;display:block}}.chips{{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}}
.chip{{font:15px system-ui;color:var(--fg);border:1px solid var(--chipb);border-radius:5px;background:var(--chip);padding:6px 9px;cursor:pointer}}
.chip span{{display:block;font-style:italic;margin-top:3px}}.disputed{{border-color:var(--amberb);background:var(--amber)}}.uncertain b{{text-decoration:underline dotted}}
nav a{{margin-right:12px}}#detail{{position:sticky;bottom:12px;background:#17364a;color:#fff;border-radius:5px;padding:10px;min-height:22px}}small{{opacity:.7}}
</style><h1>{html.escape(title)}</h1>{summary}<nav>{nav}</nav>{"".join(cards)}
<p><small>Source {html.escape(os.path.basename(lay["source"]))}, SHA-256 {lay["source_sha256"]}. {html.escape(attribution)}</small></p>
<div id="detail" aria-live="polite">Select a token.</div>
<script>document.querySelectorAll('.chip').forEach(b=>b.onclick=()=>document.querySelector('#detail').textContent=b.querySelector('b').textContent+(b.title?': '+b.title:''));</script></html>'''


# ---------------------------------------------------------------- CLI

def _box(s: str | None):
    if s == "auto":
        return "auto"
    return [int(x) for x in s.split(",")] if s else None


def main(argv: list[str]) -> int:
    import argparse
    p = argparse.ArgumentParser(prog="cipherkit.transcribe", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("layout"); s.add_argument("image"); s.add_argument("-o", "--out", required=True)
    s.add_argument("--crop", help="l,t,r,b in source pixels, or 'auto' to find the paper inside a dark frame")
    s.add_argument("--rotate", type=float, default=None, help="degrees; default: deskew automatically")
    s.add_argument("--scale", type=float, default=1.0); s.add_argument("--label")
    s.add_argument("--min-height", type=int, default=8); s.add_argument("--threshold", type=float, default=0.35)
    s = sub.add_parser("strips"); s.add_argument("layout"); s.add_argument("-o", "--out", required=True)
    s = sub.add_parser("gaps", help="word gaps in one line strip, as JSON"); s.add_argument("strip")
    s.add_argument("--min-gap", type=int, default=12, help="columns; shorter blank runs are not gaps")
    s.add_argument("--min-ink", type=float, default=0.02, help="dark-pixel fraction that makes a column inked")
    s.add_argument("--dark", type=int, default=None,
                   help="ink threshold 0-255 after contrast stretch; default: the strip's histogram midpoint")
    s = sub.add_parser("compare"); s.add_argument("a"); s.add_argument("b"); s.add_argument("-o", "--out")
    s.add_argument("--names", default="a,b")
    s = sub.add_parser("consensus"); s.add_argument("a"); s.add_argument("b"); s.add_argument("-o", "--out", required=True)
    s = sub.add_parser("review"); s.add_argument("layout"); s.add_argument("pass_file")
    s.add_argument("-o", "--out", required=True); s.add_argument("--key"); s.add_argument("--compare")
    s.add_argument("--title"); s.add_argument("--attribution", default="")
    a = p.parse_args(argv)

    if a.cmd == "layout":
        lay = layout(a.image, _box(a.crop), a.rotate, a.scale, a.label, min_height=a.min_height, threshold=a.threshold)
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(lay, f, indent=1); f.write("\n")
        preview = os.path.splitext(a.out)[0] + ".preview.png"
        draw_preview(lay, preview)
        crop = lay["processing"]["crop"]
        print(f"{len(lay['lines'])} lines, crop {crop or 'none'}, rotate {lay['processing']['rotate']:+.2f} "
              f"-> {a.out}, preview {preview}")
    elif a.cmd == "strips":
        lay = json.load(open(a.layout, encoding="utf-8"))
        m = strips(lay, a.out)
        print(f"{len(m['strips'])} strips, {len(m['boards'])} boards -> {a.out}/manifest.json")
    elif a.cmd == "gaps":
        Image, _, _ = _pil()
        strip = Image.open(a.strip)
        found = gaps(strip, a.min_gap, a.min_ink, a.dark)
        out = {"source": a.strip, "source_sha256": sha256_file(a.strip), "size": [strip.width, strip.height],
               "min_gap": a.min_gap, "min_ink": a.min_ink, "dark": a.dark, "ink_span": _inked_span(strip, a.min_ink, a.dark),
               "gaps": [list(g) for g in found],
               "note": "gaps are [x0, x1) column ranges in the strip; ink_span is [first, last + 1) inked column"}
        print(json.dumps(out, indent=1))
    elif a.cmd == "compare":
        names = tuple(a.names.split(","))
        c = compare(load_pass(a.a), load_pass(a.b), names)
        c["sources"] = {names[0]: a.a, names[1]: a.b}
        text = json.dumps(c, ensure_ascii=False, indent=1) + "\n"
        if a.out:
            open(a.out, "w", encoding="utf-8").write(text)
        print(f"{c['paired_tokens']} paired: {c['agree']} agree, {c['agree_via_alternative']} via alternative, "
              f"{c['differ']} differ; unpaired {c['only_' + names[0]]}/{c['only_' + names[1]]}; "
              f"agreement {c['agreement_rate']}")
    elif a.cmd == "consensus":
        rows = consensus(load_pass(a.a), load_pass(a.b))
        save_pass(rows, a.out, status="consensus of two passes; {x/y} where they differ, {x/?} where one reader has no token",
                  sources=[a.a, a.b])
        n_alt = sum(t.startswith("{") for r in rows for t in r.tokens)
        print(f"{len(rows)} rows, {n_alt} tokens with alternatives -> {a.out}")
    elif a.cmd == "review":
        lay = json.load(open(a.layout, encoding="utf-8"))
        key = None
        if a.key:
            k = json.load(open(a.key, encoding="utf-8"))
            key = k.get("mapping", k)
        cmp = json.load(open(a.compare, encoding="utf-8")) if a.compare else None
        page = review(lay, load_pass(a.pass_file), key, cmp, a.title, a.attribution)
        open(a.out, "w", encoding="utf-8").write(page)
        print(f"-> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
