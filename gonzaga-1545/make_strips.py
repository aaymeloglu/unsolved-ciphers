"""Cut padded half-line strips from the layout files, for transcription.

cipherkit's `strips` cuts each line at its ink band, which clips this hand's long ascenders and
descenders (g, q, z, p, the looped y). This cuts the same bands with padding, in two overlapping
halves per line, enlarged, so every sign is whole. Output goes to halves/<page>/.

    uv run python gonzaga-1545/make_strips.py
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PIL import Image  # noqa: E402

from cipherkit.transcribe import prepare  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
PAD_TOP, PAD_BOTTOM, ZOOM, OVERLAP = 45, 55, 1.5, 90


def text_columns(im, lines):
    """Leftmost and rightmost column carrying writing. A column of the scanner's black frame is
    dark almost from top to bottom, a column of writing only where a stroke crosses it."""
    g = im.convert("L")
    band = g.crop((0, min(b[0] for b in lines), im.width, max(b[1] for b in lines)))
    px = band.load()
    rows = range(0, band.height, 2)
    share = [sum(1 for y in rows if px[x, y] < 110) / len(rows) for x in range(band.width)]
    cols = [x for x, s in enumerate(share) if 0.02 < s < 0.5]
    return max(0, min(cols) - 40), min(im.width, max(cols) + 40)


def main():
    for path in sorted(glob.glob(os.path.join(HERE, "layout", "*.layout.json"))):
        lay = json.load(open(path))
        p = lay["processing"]
        src = os.path.join(HERE, "..", lay["source"])
        im = prepare(Image.open(src), crop=p["crop"], rotate=p["rotate"], scale=p["scale"])
        out = os.path.join(HERE, "halves", lay["label"])
        os.makedirs(out, exist_ok=True)
        left, right = text_columns(im, lay["lines"])
        mid = (left + right) // 2
        for n, (top, bottom) in enumerate(lay["lines"], 1):
            for half, (a, b) in zip("ab", [(left, mid + OVERLAP), (mid - OVERLAP, right)]):
                c = im.crop((a, max(0, top - PAD_TOP), b, min(im.height, bottom + PAD_BOTTOM)))
                c = c.resize((int(c.width * ZOOM), int(c.height * ZOOM)), Image.Resampling.LANCZOS)
                c.save(os.path.join(out, f"{lay['label']}-L{n:02d}{half}.png"))
        print(lay["label"], len(lay["lines"]), "lines, text columns", (left, right))


if __name__ == "__main__":
    main()
