"""Paint out the interlinear gloss on c.176r and write masked line crops.

Gloss regions are drawn as polygons in the 1x coordinates of a deskewed line
band (see crop_lines.py: band x = page x - X0 after rotation, band y = 0 at
baseline-UP).  They are mapped back to page coordinates and painted on a copy
of the whole page, so gloss that intrudes into a neighbouring line's band is
removed there as well.  "keep" polygons are subtracted from the paint mask to
protect cipher strokes (tall ascenders, dots of division-sign signs, etc.).

Fill = local paper estimate: max-filter (removes ink strokes) + blur
(no texture added).

Usage: mask_176r.py [--debug]
"""
import math
import os

import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter

import crop_lines as C

PAGE = os.path.join(C.IMGDIR, "81645_doc81_c176r.jpg")
WORK = os.path.dirname(os.path.abspath(__file__))

GEOM = {name: (pL, pR) for f, sub, name, pL, pR, *r in C.LINES if f == os.path.basename(PAGE)}


def R(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


# polygons in band coordinates of the named line
MASK = {
    "176r_L17": [R(210, 0, 256, 30), R(230, 24, 250, 37)],
    "176r_L19": [
        [(84, 0), (200, 0), (200, 27), (147, 27), (147, 21), (130, 21), (130, 27), (84, 27)],
        R(80, 64, 113, 86),
        R(487, 20, 523, 43),
        R(652, 15, 802, 41), R(728, 41, 752, 44),
        R(806, 15, 940, 30), R(811, 30, 940, 44),
        R(955, 28, 992, 38),
    ],
    "176r_L20": [
        R(78, 6, 118, 31),
        R(424, 12, 441, 42), R(441, 12, 510, 44),
        R(528, 22, 605, 49),
        R(625, 22, 890, 43),
    ],
    "176r_L21": [
        R(152, 6, 325, 33),
        R(338, 9, 400, 41), R(400, 16, 568, 41),
    ],
    "176r_L22": [
        R(442, 12, 597, 44),
        R(636, 26, 716, 54), R(716, 26, 727, 40),
        R(745, 14, 860, 49),
        R(862, 18, 995, 47),
        R(70, 53, 118, 84),
    ],
    "176r_L23": [R(70, 8, 120, 34)],
    "176r_L27": [R(1075, 10, 1186, 44)],
}
KEEP = {
    "176r_L19": [R(130, 21, 147, 40), R(886, 20, 893, 50), R(838, 43, 850, 50)],
    "176r_L20": [R(553, 48, 561, 56), R(806, 38, 818, 48), R(424, 43, 441, 70)],
    "176r_L21": [R(327, 27, 339, 39), R(417, 0, 426, 24), R(434, 39, 452, 70)],
    "176r_L22": [R(503, 0, 516, 26), R(779, 48, 794, 72)],
}


def to_page(name, pts):
    (xL, yL), (xR, yR) = GEOM[name]
    th = math.atan2(yR - yL, xR - xL)
    c, s = math.cos(th), math.sin(th)
    out = []
    for cx, cy in pts:
        u, v = cx + C.X0, cy + yL - C.UP
        dx, dy = u - xL, v - yL
        out.append((xL + c * dx - s * dy, yL + s * dx + c * dy))
    return out


def build_masked_page():
    im = Image.open(PAGE).convert("RGB")
    paint = Image.new("L", im.size, 0)
    keep = Image.new("L", im.size, 0)
    dp, dk = ImageDraw.Draw(paint), ImageDraw.Draw(keep)
    for name, polys in MASK.items():
        for p in polys:
            dp.polygon(to_page(name, p), fill=255)
    for name, polys in KEEP.items():
        for p in polys:
            dk.polygon(to_page(name, p), fill=255)
    m = ImageChops.subtract(paint, keep)
    # background estimate: remove ink with a max filter, then smooth
    bg = im.filter(ImageFilter.MaxFilter(11)).filter(ImageFilter.GaussianBlur(3))
    # soften mask edge by ~1px
    m_soft = m.filter(ImageFilter.GaussianBlur(0.8))
    out = Image.composite(bg, im, m_soft)
    return out, m


def main():
    page, m = build_masked_page()
    page.save(os.path.join(WORK, "176r_masked_page.png"))
    m.save(os.path.join(WORK, "176r_paintmask.png"))
    os.makedirs(os.path.join(C.OUT, "masked"), exist_ok=True)
    tmp = os.path.join(WORK, "_tmp_page.png")
    page.save(tmp)
    for name, (pL, pR) in GEOM.items():
        b = C.band(tmp, pL, pR)
        if "--debug" in sys.argv:
            os.makedirs(C.DBG, exist_ok=True)
            b.save(os.path.join(C.DBG, name + "_m.png"))
        big = b.resize((b.width * C.SCALE, b.height * C.SCALE), Image.LANCZOS)
        big.save(os.path.join(C.OUT, "masked", name + ".png"))
        print("masked", name)
    os.remove(tmp)


if __name__ == "__main__":
    main()
