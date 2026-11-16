import sys
from PIL import Image, ImageDraw
I='/Users/aaymeloglu/.claude-assistant/research/unsolved-ciphers/niccolini-1492/images/'
f,x0,y0,x1,y1,s,out=sys.argv[1:8]; x0,y0,x1,y1=map(int,(x0,y0,x1,y1)); s=float(s)
im=Image.open(I+f).crop((x0,y0,x1,y1)); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
W=60; c=Image.new('RGB',(im.width+2*W,im.height),'white'); c.paste(im,(W,0)); d=ImageDraw.Draw(c)
for y in range((y0//10)*10,y1,10):
    yy=int((y-y0)*s)
    if yy<0: continue
    L=12 if y%50 else 30
    d.line([(W-L,yy),(W,yy)],fill='red'); d.line([(W+im.width,yy),(W+im.width+L,yy)],fill='red')
    if y%50==0: d.text((2,yy-5),str(y),fill='black'); d.text((W+im.width+32,yy-5),str(y),fill='black')
c.save(out)
