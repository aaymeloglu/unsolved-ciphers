"""Crop deskewed line bands at 3x.

Each line is defined by two baseline points (xL, yL) and (xR, yR) in original
page pixels. The page is rotated about (xL, yL) so the baseline becomes
horizontal, then the band [yL-up, yL+down] x [X0, X1] is cropped and upscaled
3x with LANCZOS.

Usage: crop_lines.py            -> writes all crops listed in LINES
       crop_lines.py --debug     -> also writes original-res crops to work/dbg/
"""
import math
import os
import sys

from PIL import Image

IMGDIR = "/Users/aaymeloglu/.claude-assistant/research/unsolved-ciphers/niccolini-1492/images"
OUT = "/Users/aaymeloglu/git/unsolved-ciphers/milan-1494/niccolini-1492/crops"
DBG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dbg")
SCALE = 3
X0, X1 = 50, 1250
UP, DOWN = 60, 26

# key: (image file, out subdir, out name, (xL, yL), (xR, yR))
LINES = [
    ("81645_doc81_c176r.jpg", "unmasked", "176r_L17", (110, 1015), (1200, 1047)),
    ("81645_doc81_c176r.jpg", "unmasked", "176r_L19", (110, 1128), (1200, 1170)),
    ("81645_doc81_c176r.jpg", "unmasked", "176r_L20", (110, 1180), (1200, 1220)),
    ("81645_doc81_c176r.jpg", "unmasked", "176r_L21", (110, 1232), (1200, 1276)),
    ("81645_doc81_c176r.jpg", "unmasked", "176r_L22", (110, 1282), (1200, 1325)),
    ("81645_doc81_c176r.jpg", "unmasked", "176r_L23", (110, 1330), (1200, 1372)),
    ("81645_doc81_c176r.jpg", "unmasked", "176r_L27", (110, 1570), (1220, 1620)),
    ("81645_doc81_c176r.jpg", "unmasked", "176r_L28", (110, 1625), (1200, 1662)),
    ("81477_doc42_c90r.jpg", "bare", "090r_L14", (100, 1088), (1200, 1116)),
    ("81477_doc42_c90r.jpg", "bare", "090r_L15", (100, 1132), (1200, 1162)),
    ("81477_doc42_c90r.jpg", "bare", "090r_L16", (100, 1188), (1200, 1215)),
    ("81477_doc42_c90r.jpg", "bare", "090r_L17", (100, 1244), (1200, 1265)),
    ("81477_doc42_c90r.jpg", "bare", "090r_L18", (100, 1294), (1200, 1305)),
    ("81503_doc49_c104r.jpg", "bare", "104r_L15", (100, 868), (1200, 892)),
    ("81651_doc81_c177r.jpg", "bare", "177r_L03", (100, 308), (1200, 308)),
    ("81697_doc90_c200r.jpg", "bare", "200r_L03", (100, 312), (1200, 306)),
]


def paper_colour(im):
    """Median-ish paper colour: the 70th percentile of luminance pixels."""
    small = im.resize((im.width // 8, im.height // 8))
    px = sorted(small.getdata(), key=lambda p: sum(p))
    return px[int(len(px) * 0.7)]


def band(img_path, pL, pR, up=UP, down=DOWN, x0=X0, x1=X1):
    im = Image.open(img_path).convert("RGB")
    (xL, yL), (xR, yR) = pL, pR
    ang = math.degrees(math.atan2(yR - yL, xR - xL))
    fill = paper_colour(im)
    rot = im.rotate(ang, resample=Image.BICUBIC, center=(xL, yL), fillcolor=fill)
    return rot.crop((x0, yL - up, x1, yL + down))


def main():
    debug = "--debug" in sys.argv
    if debug:
        os.makedirs(DBG, exist_ok=True)
    for f, sub, name, pL, pR, *rest in LINES:
        kw = rest[0] if rest else {}
        b = band(os.path.join(IMGDIR, f), pL, pR, **kw)
        if debug:
            b.save(os.path.join(DBG, name + ".png"))
        big = b.resize((b.width * SCALE, b.height * SCALE), Image.LANCZOS)
        os.makedirs(os.path.join(OUT, sub), exist_ok=True)
        big.save(os.path.join(OUT, sub, name + ".png"))
        print(sub, name, big.size)


if __name__ == "__main__":
    main()
