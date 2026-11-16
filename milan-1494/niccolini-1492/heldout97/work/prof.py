import sys
from PIL import Image
import numpy as np
I='/Users/aaymeloglu/.claude-assistant/research/unsolved-ciphers/niccolini-1492/images/'
f=sys.argv[1]
im=np.asarray(Image.open(I+f).convert('RGB')).astype(float)
g=im.mean(2)
best=None
for ang in np.arange(-2,2.01,0.1):
    r=Image.fromarray(g.astype(np.uint8)).rotate(ang,resample=Image.BILINEAR,fillcolor=200)
    a=np.asarray(r).astype(float)[:,150:1200]
    p=(a<110).sum(1)
    v=p.var()
    if best is None or v>best[0]: best=(v,ang,p)
print('angle',best[1])
p=best[2]
for y in range(150,1850,6): print(y, '#'*(int(p[y:y+6].sum()/60)))
