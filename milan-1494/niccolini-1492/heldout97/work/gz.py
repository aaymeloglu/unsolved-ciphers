# gloss zoom: page region, deskew like band, 4x, mild unsharp; split into n parts
import sys, math
from PIL import Image, ImageFilter, ImageDraw
from lines import LINES
I='/Users/aaymeloglu/.claude-assistant/research/unsolved-ciphers/niccolini-1492/images/'
name=sys.argv[1]; top=int(sys.argv[2]); bot=int(sys.argv[3]); n=int(sys.argv[4]); xa=int(sys.argv[5]) if len(sys.argv)>5 else 120; xb=int(sys.argv[6]) if len(sys.argv)>6 else 1250
for leaf,lab,f,yl,yr in LINES:
    if f'{leaf}_{lab}'!=name: continue
    im=Image.open(I+f).convert('RGB')
    ang=math.degrees(math.atan2(yr-yl,750))
    r=im.rotate(ang,resample=Image.BICUBIC,center=(290,yl))
    c=r.crop((xa,yl-top,xb,yl+bot)); S=4
    c=c.resize((c.width*S,c.height*S),Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=4,percent=120,threshold=2))
    step=-(-c.width//n)
    for i in range(n):
        x0=i*step; p=c.crop((x0,0,min(c.width,x0+step+40),c.height))
        cv=Image.new('RGB',(p.width,p.height+14),'white'); cv.paste(p,(0,14)); d=ImageDraw.Draw(cv)
        for X in range(0,p.width,S*10):
            px=(x0+X)//S+xa; cx=3*(px-120)
            if px%25==0: d.line([(X,6),(X,14)],fill='red'); d.text((X+2,0),str(cx),fill='black')
        cv.save(f'view/z_{name}_{i}.png')
