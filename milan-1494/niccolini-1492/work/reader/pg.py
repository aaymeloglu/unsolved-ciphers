# Crop a page region and upscale: pg.py <img> x0 y0 x1 y1 scale out
import sys
from PIL import Image, ImageOps
p=sys.argv[1];x0,y0,x1,y1=map(int,sys.argv[2:6]);s=float(sys.argv[6]);out=sys.argv[7]
im=Image.open(p).convert('L').crop((x0,y0,x1,y1))
im=ImageOps.autocontrast(im,cutoff=1)
im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
im.save(out)
