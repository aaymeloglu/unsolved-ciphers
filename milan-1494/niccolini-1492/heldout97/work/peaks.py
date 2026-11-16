import sys
from PIL import Image
import numpy as np
from scipy.ndimage import uniform_filter1d
from scipy.signal import find_peaks
I='/Users/aaymeloglu/.claude-assistant/research/unsolved-ciphers/niccolini-1492/images/'
f=sys.argv[1]; y0,y1=int(sys.argv[2]),int(sys.argv[3])
g=np.asarray(Image.open(I+f).convert('L')).astype(float)
for (xa,xb) in [(150,450),(500,800),(880,1180)]:
    p=(g[:,xa:xb]<105).sum(1).astype(float); p=uniform_filter1d(p,5)
    pk,pr=find_peaks(p[y0:y1],distance=12,prominence=8)
    print((xa,xb),[ (int(k+y0),int(p[k+y0])) for k in pk])
