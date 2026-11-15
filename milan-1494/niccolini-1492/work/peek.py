"""Inspection helper: crop a region, upscale, draw a coordinate grid (original px).
usage: peek.py IMG x0 y0 x1 y1 scale OUT [gridstep]
"""
import sys
from PIL import Image, ImageDraw

img, x0, y0, x1, y1, s, out = sys.argv[1:8]
step = int(sys.argv[8]) if len(sys.argv) > 8 else 20
x0, y0, x1, y1 = map(int, (x0, y0, x1, y1))
s = float(s)
im = Image.open(img).convert("RGB").crop((x0, y0, x1, y1))
im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
d = ImageDraw.Draw(im)
for y in range((y0 // step + 1) * step, y1, step):
    yy = (y - y0) * s
    d.line([(0, yy), (12, yy)], fill=(0, 0, 255))
    d.text((14, yy - 6), str(y), fill=(0, 0, 255))
for x in range((x0 // step + 1) * step, x1, step):
    xx = (x - x0) * s
    d.line([(xx, 0), (xx, 10)], fill=(255, 0, 0))
    if x % (step * 2) == 0:
        d.text((xx + 1, 10), str(x), fill=(255, 0, 0))
im.save(out)
