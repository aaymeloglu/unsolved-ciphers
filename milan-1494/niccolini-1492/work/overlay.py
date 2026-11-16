"""overlay.py NAME OUT : original band with painted area tinted red, keep area tinted green."""
import sys
from PIL import Image, ImageChops
import crop_lines as C
import mask_176r as M
name, out = sys.argv[1], sys.argv[2]
pL, pR = M.GEOM[name]
o = C.band(M.PAGE, pL, pR)
pm = C.band("176r_paintmask.png", pL, pR).convert("L")
red = Image.new("RGB", o.size, (255, 0, 0))
t = Image.composite(Image.blend(o, red, 0.35), o, pm.point(lambda v: 255 if v > 128 else 0))
t.save(out)
