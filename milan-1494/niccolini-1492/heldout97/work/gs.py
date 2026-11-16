# gloss strip, stacked: page region deskewed, 3x, cut into 3 segments stacked vertically, crop-x ticks (crop x = 3*(page x-120))
import sys, math
from PIL import Image, ImageFilter, ImageDraw, ImageOps
from lines import LINES
I='/Users/aaymeloglu/.claude-assistant/research/unsolved-ciphers/niccolini-1492/images/'
name=sys.argv[1]; top=int(sys.argv[2]); bot=int(sys.argv[3])
for leaf,lab,f,yl,yr in LINES:
    if f'{leaf}_{lab}'!=name: continue
    im=Image.open(I+f).convert('RGB')
    r=im.rotate(math.degrees(math.atan2(yr-yl,750)),resample=Image.BICUBIC,center=(290,yl))
    c=r.crop((120,yl-top,1250,yl+bot)); c=c.resize((c.width*3,c.height*3),Image.LANCZOS)
    pass
    seg=1150; h=c.height+14; out=Image.new('RGB',(seg+40,3*h),'white'); d=ImageDraw.Draw(out)
    for i in range(3):
        x0=i*1130; p=c.crop((x0,0,min(c.width,x0+seg),c.height)); out.paste(p,(0,i*h+14))
        for X in range(0,p.width,50):
            d.line([(X,i*h+(0 if (x0+X)%100==0 else 7)),(X,i*h+14)],fill='red')
            if (x0+X)%100==0: d.text((X+2,i*h),str(x0+X),fill='black')
    out.save(f'view/s_{name}.png')
