import sys, os
from PIL import Image, ImageDraw
# stack.py NAME x0 x1 rows scale [y0]
name, x0, x1, rows, s = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5])
y0 = int(sys.argv[6]) if len(sys.argv) > 6 else 50
src = Image.open(f"heldout97/crops/masked/{name}.png").convert("RGB")
H = src.height - y0
w = (x1 - x0 + rows - 1) // rows
tiles = []
for r in range(rows):
    a = x0 + r * w; b = min(x1, a + w + 30)
    t = src.crop((a, y0, b, src.height)).resize((int((b - a) * s), int(H * s)), Image.LANCZOS)
    d = ImageDraw.Draw(t)
    for x in range((a // 50 + 1) * 50, b, 50):
        px = int((x - a) * s); d.line([(px, 0), (px, 6)], fill=(255, 0, 0))
        if x % 100 == 0: d.text((px + 2, 0), str(x), fill=(255, 0, 0))
    tiles.append(t)
W = max(t.width for t in tiles)
out = Image.new("RGB", (W, sum(t.height for t in tiles) + 4 * rows), "white")
y = 0
for t in tiles: out.paste(t, (0, y)); y += t.height + 4
os.makedirs("heldout97/work/tr", exist_ok=True)
p = f"heldout97/work/tr/{name}_{x0}_{x1}.png"; out.save(p); print(p, out.size)
