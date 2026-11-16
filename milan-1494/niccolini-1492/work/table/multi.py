# usage: multi.py out.png scale < specs   (spec lines: imgid x0 y0 x1 y1 label)
import sys, glob
from PIL import Image, ImageOps, ImageDraw
IMG='/Users/aaymeloglu/.claude-assistant/research/unsolved-ciphers/niccolini-1492/images/'
out=sys.argv[1]; s=float(sys.argv[2])
tiles=[]
for ln in sys.stdin:
    p=ln.split()
    if not p or p[0].startswith('#'): continue
    f=glob.glob(IMG+p[0]+'_*.jpg')[0]; assert 'doc97' not in f
    x0,y0,x1,y1=map(int,p[1:5]); lab=' '.join(p[5:])
    im=Image.open(f).convert('L').crop((x0,y0,x1,y1)); im=ImageOps.autocontrast(im,cutoff=1)
    im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS).convert('RGB')
    d=ImageDraw.Draw(im)
    for x in range((x0//25+1)*25,x1,25):
        X=int((x-x0)*s); d.line([(X,im.height-6),(X,im.height)],fill=(255,0,0),width=2)
        if x%50==0: d.text((X+2,im.height-16),str(x),fill=(255,0,0))
    for y in range((y0//25+1)*25,y1,25):
        Y=int((y-y0)*s); d.line([(0,Y),(6,Y)],fill=(0,160,0),width=2); d.text((8,Y-6),str(y),fill=(0,160,0))
    d.text((40,2),lab+f' y{y0}-{y1}',fill=(0,0,255))
    tiles.append(im)
W=max(t.width for t in tiles)
sheet=Image.new('RGB',(W,sum(t.height+4 for t in tiles)),'white'); y=0
for t in tiles: sheet.paste(t,(0,y)); y+=t.height+4
sheet.save(out); print(out,sheet.size)
