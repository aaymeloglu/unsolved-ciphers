import sys
from PIL import Image, ImageDraw
M='/Users/aaymeloglu/git/unsolved-ciphers/milan-1494/niccolini-1492/heldout97/crops/masked/'
name=sys.argv[1]
im=Image.open(M+name+'.png'); seg=1150; h=im.height+14
out=Image.new('RGB',(seg+10,3*h),'white'); d=ImageDraw.Draw(out)
for i in range(3):
    x0=i*1130; out.paste(im.crop((x0,0,min(im.width,x0+seg),im.height)),(0,i*h+14))
    for X in range(0,seg,50):
        d.line([(X,i*h+(0 if (x0+X)%100==0 else 7)),(X,i*h+14)],fill='red')
        if (x0+X)%100==0: d.text((X+2,i*h),str(x0+X),fill='black')
out.save(f'view/m_{name}.png')
