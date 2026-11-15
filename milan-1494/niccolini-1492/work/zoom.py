"""zoom.py BAND x0 x1 OUT [scale]  -> crop band columns x0..x1 (full height), upscale, 5px grid."""
import sys
from PIL import Image, ImageDraw
src, x0, x1, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
s = int(sys.argv[5]) if len(sys.argv) > 5 else 4
im = Image.open(src).convert("RGB")
im = im.crop((x0, 0, x1, im.height))
im = im.resize((im.width * s, im.height * s), Image.LANCZOS)
d = ImageDraw.Draw(im)
for x in range(x0 - x0 % 5, x1, 5):
    X = (x - x0) * s
    L = 14 if x % 10 == 0 else 6
    d.line([(X, 0), (X, L)], fill=(255, 0, 0))
    d.line([(X, im.height - L), (X, im.height)], fill=(255, 0, 0))
    if x % 20 == 0:
        d.text((X + 2, 14), str(x), fill=(255, 0, 0))
for y in range(0, im.height // s, 5):
    Y = y * s
    L = 14 if y % 10 == 0 else 6
    d.line([(0, Y), (L, Y)], fill=(0, 0, 255))
    d.line([(im.width - L, Y), (im.width, Y)], fill=(0, 0, 255))
    if y % 10 == 0:
        d.text((16, Y - 5), str(y), fill=(0, 0, 255))
im.save(out)
