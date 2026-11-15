"""Stack a band image (any scale) in N horizontal pieces with crop-px grid (in 1x crop units)."""
import sys
from PIL import Image, ImageDraw
src, out = sys.argv[1], sys.argv[2]
unit = int(sys.argv[3]) if len(sys.argv) > 3 else 1   # px per crop-unit in src (3 for 3x crops)
n = int(sys.argv[4]) if len(sys.argv) > 4 else 2
im = Image.open(src).convert("RGB")
# normalise to 2 display px per crop unit
s = 2.0 / unit
im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
w = im.width // n
pieces = []
for i in range(n):
    p = im.crop((i * w, 0, (i + 1) * w, im.height)).copy()
    d = ImageDraw.Draw(p)
    for cx in range(0, w // 2 + 1, 10):
        X = cx * 2
        gx = i * w // 2 + cx
        d.line([(X, 0), (X, 6 if gx % 50 else 12)], fill=(255, 0, 0))
        if gx % 50 == 0:
            d.text((X + 2, 0), str(gx), fill=(255, 0, 0))
    for cy in range(0, im.height // 2, 10):
        d.line([(0, cy * 2), (6, cy * 2)], fill=(0, 0, 255))
        d.text((8, cy * 2 - 5), str(cy), fill=(0, 0, 255))
    pieces.append(p)
H = sum(p.height for p in pieces) + 6 * n
canvas = Image.new("RGB", (w, H), (255, 255, 255))
y = 0
for p in pieces:
    canvas.paste(p, (0, y)); y += p.height + 6
canvas.save(out)
