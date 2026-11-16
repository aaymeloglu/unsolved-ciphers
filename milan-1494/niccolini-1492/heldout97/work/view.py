import sys
from PIL import Image
I='/Users/aaymeloglu/.claude-assistant/research/unsolved-ciphers/niccolini-1492/images/'
f,x0,y0,x1,y1,s,out=sys.argv[1:8]
im=Image.open(I+f).crop((int(x0),int(y0),int(x1),int(y1)))
s=float(s); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS); im.save(out)
