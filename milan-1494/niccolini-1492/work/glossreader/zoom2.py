import sys
from PIL import Image, ImageOps
base="/Users/aaymeloglu/git/unsolved-ciphers/milan-1494/niccolini-1492/crops/unmasked/176r_%s.png"
L,x0,x1,y0,y1,s,out=sys.argv[1],*map(int,sys.argv[2:7]),sys.argv[7]
im=Image.open(base%L).convert("RGB").crop((x0,y0,x1,y1))
im=im.resize((int(im.width*s/10),int(im.height*s/10)),Image.BICUBIC)
im.save(out)
