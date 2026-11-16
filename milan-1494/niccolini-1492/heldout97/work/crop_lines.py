"""Deskewed line bands, 3x LANCZOS. Crop x = 3*(page x - 120); crop y = 3*(page y - (yc-48)) on the deskewed band."""
import math, sys
from PIL import Image
from lines import LINES
I='/Users/aaymeloglu/.claude-assistant/research/unsolved-ciphers/niccolini-1492/images/'
OUT='/Users/aaymeloglu/git/unsolved-ciphers/milan-1494/niccolini-1492/heldout97/crops/unmasked/'
TOP,BOT=48,26
only=sys.argv[1:]
for leaf,lab,f,yl,yr in LINES:
    name=f'{leaf}_{lab}'
    if only and name not in only: continue
    im=Image.open(I+f).convert('RGB')
    ang=math.degrees(math.atan2(yr-yl,1040-290))
    r=im.rotate(ang,resample=Image.BICUBIC,center=(290,yl),fillcolor=(150,144,110))
    c=r.crop((120,yl-TOP,1250,yl+BOT))
    c=c.resize((c.width*3,c.height*3),Image.LANCZOS)
    c.save(OUT+name+'.png')
print('ok')
