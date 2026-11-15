# usage: chunks.py imgid y0 y1 step outprefix [scale]  -> images of 3 chunks each (each chunk = two half-width bands)
import sys, subprocess
img,y0,y1,step,pre=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),sys.argv[5]
s=sys.argv[6] if len(sys.argv)>6 else '2.4'
ys=list(range(y0,y1,step)); n=0
for i in range(0,len(ys),3):
    spec=''
    for y in ys[i:i+3]:
        spec+=f'{img} 30 {y} 650 {y+step+20} y{y}L\n{img} 610 {y} 1250 {y+step+20} y{y}R\n'
    out=f'{pre}_{n}.png'
    subprocess.run(['python','multi.py',out,s],input=spec,text=True,check=True); n+=1
