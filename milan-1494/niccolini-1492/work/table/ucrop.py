# usage: ucrop.py <unmasked crop name e.g. 176r_L22> x0 x1 out [scale]
import sys
from PIL import Image, ImageOps, ImageDraw
a=sys.argv
im=Image.open(f'/Users/aaymeloglu/git/unsolved-ciphers/milan-1494/niccolini-1492/crops/unmasked/{a[1]}.png').convert('L')
x0,x1=int(a[2]),int(a[3]); s=float(a[5]) if len(a)>5 else 1.0
c=ImageOps.autocontrast(im.crop((x0,0,x1,im.height)),cutoff=1)
c=c.resize((int(c.width*s),int(c.height*s)),Image.LANCZOS).convert('RGB')
d=ImageDraw.Draw(c)
for x in range((x0//50+1)*50,x1,50):
    X=int((x-x0)*s); d.line([(X,c.height-8),(X,c.height)],fill=(255,0,0),width=2)
    if x%100==0: d.text((X+2,c.height-20),str(x),fill=(255,0,0))
c.save(a[4]); print(a[4],c.size)
