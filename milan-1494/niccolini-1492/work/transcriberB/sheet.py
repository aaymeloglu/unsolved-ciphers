"""Contact sheet of hooked-stem signs at equal scale."""
from PIL import Image, ImageDraw, ImageOps
base = "/Users/aaymeloglu/git/unsolved-ciphers/milan-1494/niccolini-1492/"
items = [
 ("A S54 L19a", "crops/masked/176r_L19.png", 1975, 2065),
 ("A S54 L19b", "crops/masked/176r_L19.png", 2635, 2705),
 ("A S54 L20", "crops/masked/176r_L20.png", 2425, 2505),
 ("A S54 L23", "crops/masked/176r_L23.png", 575, 655),
 ("A S54 L27", "crops/masked/176r_L27.png", 3390, 3470),
 ("A S54 L28", "crops/masked/176r_L28.png", 400, 470),
 ("A N8 L28", "crops/masked/176r_L28.png", 605, 700),
 ("B N9 14", "crops/bare/090r_L14.png", 2515, 2595),
 ("B N9 15", "crops/bare/090r_L15.png", 3280, 3350),
 ("B N9 177", "crops/bare/177r_L03.png", 3365, 3440),
 ("B N9 200", "crops/bare/200r_L03.png", 1855, 1945),
 ("B S72 15", "crops/bare/090r_L15.png", 1385, 1455),
 ("B S72 16", "crops/bare/090r_L16.png", 975, 1055),
 ("B S72 17", "crops/bare/090r_L17.png", 2730, 2800),
 ("B S54 14", "crops/bare/090r_L14.png", 2330, 2410),
 ("B N8 104", "crops/bare/104r_L15.png", 2115, 2200),
]
s = 2
tiles = []
for lab, f, x0, x1 in items:
    im = ImageOps.autocontrast(Image.open(base + f).convert("L"), cutoff=1).crop((x0, 30, x1, 250))
    im = im.resize((im.width * s, im.height * s))
    t = Image.new("L", (200, im.height + 20), 255)
    t.paste(im, (0, 20))
    ImageDraw.Draw(t).text((2, 2), lab, fill=0)
    tiles.append(t)
cols = 8
h = max(t.height for t in tiles)
sheet = Image.new("L", (200 * cols, h * 2), 255)
for i, t in enumerate(tiles):
    sheet.paste(t, ((i % cols) * 200, (i // cols) * h))
sheet.save(base + "work/transcriberB/out/sheet.png")
