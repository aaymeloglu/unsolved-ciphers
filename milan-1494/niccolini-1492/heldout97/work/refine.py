from PIL import Image
import numpy as np
from scipy.ndimage import uniform_filter1d
from lines import LINES
I='/Users/aaymeloglu/.claude-assistant/research/unsolved-ciphers/niccolini-1492/images/'
cache={}
out=[]
for leaf,lab,f,yl,yr in LINES:
    if f not in cache: cache[f]=np.asarray(Image.open(I+f).convert('L')).astype(float)
    g=cache[f]; res=[]
    for xc,ye in [(290,yl),(1040,yr)]:
        p=(g[:,xc-140:xc+140]<110).sum(1).astype(float); p=uniform_filter1d(p,7)
        w=p[ye-9:ye+10]; res.append(int(ye-9+np.argmax(w)))
    print(leaf,lab,yl,yr,'->',res)
