"""Zoom a crop: z.py <crop> <x0> <x1> [scale] [out]. Draws x tick labels every 50px."""
import sys
from PIL import Image, ImageDraw, ImageOps
base = "/Users/aaymeloglu/git/unsolved-ciphers/milan-1494/niccolini-1492/"
src, x0, x1 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
s = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
out = sys.argv[5] if len(sys.argv) > 5 else base + "work/transcriberB/out/z.png"
im = Image.open(base + src).convert("L")
im = ImageOps.autocontrast(im, cutoff=1)
c = im.crop((x0, 0, x1, im.height))
c = c.resize((int(c.width * s), int(c.height * s)), Image.LANCZOS)
pad = 22
canvas = Image.new("L", (c.width, c.height + pad), 255)
canvas.paste(c, (0, pad))
d = ImageDraw.Draw(canvas)
for x in range((x0 // 50 + 1) * 50, x1, 50):
    px = int((x - x0) * s)
    d.line([(px, 0), (px, 10 if x % 100 else 18)], fill=0)
    if x % 100 == 0:
        d.text((px + 2, 0), str(x), fill=0)
canvas.save(out)
print(out, canvas.size)
