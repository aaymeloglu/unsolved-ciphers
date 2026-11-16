# usage: band.py <imgid> yc [h=80] [scale=2.6] [x0=40] [x1=1250] out
# crops band centered on baseline yc (gloss above), splits into two halves stacked, with x tick marks every 50px (page coords)
import sys, glob
from PIL import Image, ImageOps, ImageDraw
IMG='/Users/aaymeloglu/.claude-assistant/research/unsolved-ciphers/niccolini-1492/images/'
a=sys.argv
f=glob.glob(IMG+a[1]+'_*.jpg')[0]; assert 'doc97' not in f
yc=int(a[2]); h=int(a[3]); s=float(a[4]); x0=int(a[5]); x1=int(a[6]); out=a[7]
im=Image.open(f).convert('L'); im=ImageOps.autocontrast(im,cutoff=1)
y0=yc-int(h*0.68); y1=yc+int(h*0.32)
xm=(x0+x1)//2
parts=[]
for (p0,p1) in [(x0,xm+20),(xm-20,x1)]:
    c=im.crop((p0,y0,p1,y1)).resize((int((p1-p0)*s),int(h*s)),Image.LANCZOS).convert('RGB')
    d=ImageDraw.Draw(c)
    for x in range((p0//50+1)*50,p1,50):
        X=int((x-p0)*s); d.line([(X,0),(X,8)],fill=(255,0,0),width=2); d.text((X+2,0),str(x),fill=(255,0,0))
    parts.append(c)
W=max(p.width for p in parts)
sheet=Image.new('RGB',(W,sum(p.height for p in parts)+6),'white')
y=0
for p in parts: sheet.paste(p,(0,y)); y+=p.height+6
sheet.save(out); print(out,sheet.size)
