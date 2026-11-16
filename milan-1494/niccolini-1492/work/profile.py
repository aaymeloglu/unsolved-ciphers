import sys
from PIL import Image
import statistics
img=sys.argv[1]; x0,x1=int(sys.argv[2]),int(sys.argv[3])
im=Image.open(img).convert('L')
w,h=im.size
px=im.load()
rows=[]
for y in range(h):
    vals=[px[x,y] for x in range(x0,x1,2)]
    med=statistics.median(vals)
    rows.append(sum(1 for v in vals if v<med-45))
# smooth
k=6
sm=[sum(rows[max(0,y-k):y+k+1])/(2*k+1) for y in range(h)]
peaks=[y for y in range(1,h-1) if sm[y]>=sm[y-1] and sm[y]>sm[y+1] and sm[y]>8]
# merge peaks closer than 18
out=[]
for p in peaks:
    if out and p-out[-1]<18:
        if sm[p]>sm[out[-1]]: out[-1]=p
    else: out.append(p)
for p in out: print(p, round(sm[p],1))
