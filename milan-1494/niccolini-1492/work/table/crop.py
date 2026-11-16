# usage: crop.py <imgid-or-path> x0 y0 x1 y1 [scale] [outname]
import sys, glob
from PIL import Image, ImageOps, ImageEnhance
IMG='/Users/aaymeloglu/.claude-assistant/research/unsolved-ciphers/niccolini-1492/images/'
a=sys.argv
f=a[1] if '/' in a[1] else glob.glob(IMG+a[1]+'_*.jpg')[0]
assert 'doc97' not in f
x0,y0,x1,y1=map(int,a[2:6]); s=float(a[6]) if len(a)>6 else 3
out=a[7] if len(a)>7 else 'out/c.png'
im=Image.open(f).convert('L').crop((x0,y0,x1,y1))
im=ImageOps.autocontrast(im,cutoff=1)
im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
im.save(out); print(out, im.size)
