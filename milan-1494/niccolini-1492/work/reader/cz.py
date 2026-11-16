# crop a bare crop: cz.py name x0 x1 scale out [y0 y1]
import sys
from PIL import Image, ImageOps
n,x0,x1,s,out=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),float(sys.argv[4]),sys.argv[5]
y0,y1=(int(sys.argv[6]),int(sys.argv[7])) if len(sys.argv)>7 else (0,258)
im=Image.open(f'../../crops/bare/{n}.png').convert('L').crop((x0,y0,x1,y1))
im=ImageOps.autocontrast(im,cutoff=1)
im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS).save(out)
