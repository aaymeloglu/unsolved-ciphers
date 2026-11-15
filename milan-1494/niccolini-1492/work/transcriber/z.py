import sys
from PIL import Image, ImageDraw
# usage: z.py LINE x0 x1 [scale] -> work/transcriber/out/LINE_x0_x1.png with x ticks every 50px
line, x0, x1 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
s = float(sys.argv[4]) if len(sys.argv) > 4 else 1.5
im = Image.open(f"crops/masked/176r_{line}.png").convert("RGB").crop((x0, 0, x1, 258))
im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
d = ImageDraw.Draw(im)
for x in range((x0 // 50 + 1) * 50, x1, 50):
    px = int((x - x0) * s)
    d.line([(px, 0), (px, 8)], fill=(255, 0, 0))
    if x % 100 == 0:
        d.text((px + 2, 0), str(x), fill=(255, 0, 0))
import os
os.makedirs("work/transcriber/out", exist_ok=True)
p = f"work/transcriber/out/{line}_{x0}_{x1}.png"
im.save(p)
print(p)
