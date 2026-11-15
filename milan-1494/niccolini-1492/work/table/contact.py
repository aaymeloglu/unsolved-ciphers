import sys, glob, os
from PIL import Image, ImageDraw
IMG='/Users/aaymeloglu/.claude-assistant/research/unsolved-ciphers/niccolini-1492/images/'
docs=sys.argv[1].split(',')
files=[]
for d in docs:
    files+=sorted(f for f in glob.glob(IMG+f'*_doc{d}_c*.jpg') if 'doc97' not in f)
out=sys.argv[2]
n=0
for i in range(0,len(files),4):
    grp=files[i:i+4]
    W=640; tiles=[]
    for f in grp:
        im=Image.open(f).convert('RGB'); s=W/im.width; im=im.resize((W,int(im.height*s)))
        ImageDraw.Draw(im).text((10,10),os.path.basename(f),fill=(255,0,0))
        tiles.append(im)
    H=max(t.height for t in tiles)
    sheet=Image.new('RGB',(W*2,H*((len(tiles)+1)//2)),'white')
    for j,t in enumerate(tiles): sheet.paste(t,((j%2)*W,(j//2)*H))
    sheet.save(f'{out}/contact_{n:02d}.jpg',quality=80); print(f'{out}/contact_{n:02d}.jpg',[os.path.basename(g) for g in grp]); n+=1
