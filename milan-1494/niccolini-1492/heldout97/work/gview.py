import sys
from PIL import Image, ImageOps, ImageDraw
src,out=sys.argv[1],sys.argv[2]; parts=int(sys.argv[3]); r0,r1=int(sys.argv[4]),int(sys.argv[5]); s=float(sys.argv[6])
im=Image.open(src).crop((0,r0,3390,r1)); im=ImageOps.autocontrast(im,cutoff=1)
W=im.width; step=-(-W//parts)
for i in range(parts):
    x0=i*step; x1=min(W,x0+step+40)
    c=im.crop((x0,0,x1,im.height)); c=c.resize((int(c.width*s),int(c.height*s)),Image.LANCZOS)
    cv=Image.new('RGB',(c.width,c.height+14),'white'); cv.paste(c,(0,14)); d=ImageDraw.Draw(cv)
    for x in range((x0//50)*50,x1,50):
        xx=int((x-x0)*s)
        if xx<0: continue
        d.line([(xx,8 if x%100 else 0),(xx,14)],fill='red')
        if x%100==0: d.text((xx+2,0),str(x),fill='black')
    cv.save(f'{out}_{i}.png')
