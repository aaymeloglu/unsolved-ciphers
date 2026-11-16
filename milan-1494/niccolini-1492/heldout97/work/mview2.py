import sys
from PIL import Image, ImageDraw
M='/Users/aaymeloglu/git/unsolved-ciphers/milan-1494/niccolini-1492/heldout97/crops/masked/'
names=sys.argv[2:]; seg=1150; ims=[Image.open(M+n+'.png') for n in names]; h=ims[0].height+14
out=Image.new('RGB',(seg+10,3*h*len(names)+10*len(names)),'white'); d=ImageDraw.Draw(out)
for k,im in enumerate(ims):
  base=k*(3*h+10)
  for i in range(3):
    x0=i*1130; out.paste(im.crop((x0,0,min(im.width,x0+seg),im.height)),(0,base+i*h+14))
    for X in range(0,seg,50):
        d.line([(X,base+i*h+(0 if (x0+X)%100==0 else 7)),(X,base+i*h+14)],fill='red')
        if (x0+X)%100==0: d.text((X+2,base+i*h),str(x0+X) if i or X else names[k],fill='black')
out.save(sys.argv[1])
