import sys
from PIL import Image, ImageDraw
src,out=sys.argv[1],sys.argv[2]; parts=int(sys.argv[3]) if len(sys.argv)>3 else 2
im=Image.open(src); W=im.width; step=W//parts+1
for i in range(parts):
    x0=i*step; x1=min(W,x0+step+60)
    c=im.crop((x0,0,x1,im.height)); cv=Image.new('RGB',(c.width,c.height+16),'white'); cv.paste(c,(0,16)); d=ImageDraw.Draw(cv)
    for x in range((x0//50)*50,x1,50):
        xx=x-x0
        if xx<0: continue
        d.line([(xx,10 if x%100 else 0),(xx,16)],fill='red')
        if x%100==0: d.text((xx+2,0),str(x),fill='black')
    cv.save(f'{out}_{i}.png')
