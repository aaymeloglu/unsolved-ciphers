"""Paint gloss out of the 3x line bands.
Band: page yc-48..yc+26 -> crop y 0..222, cipher body centred at crop y 144.
Rule per crop:
  * top cut  y_t(x): valley of the ink profile between gloss row and cipher row, found per 300-px segment
    in crop y 80..125 and smoothed; everything above it is replaced by local paper colour, EXCEPT pixels of
    ink components whose centroid lies below the cut (cipher ascenders) and keep-boxes (raised cipher marks).
  * zone cut..cut+12 crop px is also painted, except components reaching below cut+14 (cipher bodies with
    their ascenders) and compact marks <=30x30 crop px (dots of ÷, raised o/c/9).
  * bottom cut y_b(x) (default crop 186 = page yc+14): everything below is painted, except pixels of
    components whose centroid lies above it (cipher descenders, dots under dashes).
  * components with >=12% of their ink on each side of the top cut and >=150 px are reported as
    touching spots (gloss touching cipher); they are split at the cut.
Paper colour: 80th-percentile filter (75x75 crop px) of the band, smoothed, plus sd-2 noise.
Usage: mask.py [name ...]
"""
import sys, json
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from lines import LINES
U='/Users/aaymeloglu/git/unsolved-ciphers/milan-1494/niccolini-1492/heldout97/crops/unmasked/'
M='/Users/aaymeloglu/git/unsolved-ciphers/milan-1494/niccolini-1492/heldout97/crops/masked/'
CFG=json.load(open('mask_cfg.json'))
only=sys.argv[1:]
report={}
for leaf,lab,*_ in LINES:
    name=f'{leaf}_{lab}'
    if only and name not in only: continue
    cfg=CFG.get(name,{})
    im=np.asarray(Image.open(U+name+'.png').convert('RGB')).astype(float)
    H,W,_=im.shape; g=im.mean(2)
    # ink mask (local threshold)
    bgg=ndi.median_filter(g,size=(31,31))
    ink=g<bgg-28
    ink=ndi.binary_opening(ink,iterations=1)|(g<bgg-45)
    # top cut
    if 'top' in cfg and isinstance(cfg['top'],(int,float)):
        yt=np.full(W,float(cfg['top']))
    else:
        lo,hi=cfg.get('search',[78,124])
        xs=[];ys=[]
        for x0 in range(0,W,300):
            p=ink[:,x0:x0+300].sum(1).astype(float); p=ndi.uniform_filter1d(p,9)
            seg=p[lo:hi]; xs.append(x0+150); ys.append(lo+int(np.argmin(seg)))
        yt=np.interp(np.arange(W),xs,ys); yt=ndi.uniform_filter1d(yt,301,mode='nearest')
    for x0,x1,y in cfg.get('top_override',[]):
        yt[x0:x1]=y
    yb=np.full(W,float(cfg.get('bottom',186)))
    for x0,x1,y in cfg.get('bottom_override',[]):
        yb[x0:x1]=y
    Y=np.arange(H)[:,None]
    above=Y<yt[None,:]; below=Y>yb[None,:]
    zone=(Y>=yt[None,:])&(Y<yt[None,:]+12)
    lab_,n=ndi.label(ink,structure=np.ones((3,3)))
    keep=np.zeros_like(ink)
    touch=[]
    if n:
        idx=np.arange(1,n+1)
        cy=np.array(ndi.center_of_mass(ink,lab_,idx))[:,0]
        area=ndi.sum(ink,lab_,idx)
        na=ndi.sum(ink&above,lab_,idx)
        objs=ndi.find_objects(lab_)
        for i in range(n):
            sl=objs[i]; comp=(lab_[sl]==i+1)
            yt_c=yt[sl[1]].mean()
            ybot=sl[0].stop; w=sl[1].stop-sl[1].start; h=sl[0].stop-sl[0].start
            if cy[i]>=yt_c and cy[i]<=yb[sl[1]].mean():
                # zone just under the cut: keep only components that reach the cipher body (below cut+14)
                # or are compact marks (<=30x30 crop px: dots of ÷, raised o/c/9); wide flat bits there are gloss tails / filler lines
                if ybot>=yt_c+14 or (w<=30 and h<=30):
                    keep[sl]|=comp
            if area[i]>=150 and na[i]>=0.12*area[i] and (area[i]-na[i])>=0.12*area[i]:
                bb=(sl[1].start,sl[1].stop,sl[0].start,sl[0].stop)
                touch.append([int(v) for v in bb])
    for x0,y0,x1,y1 in cfg.get('keep',[]):
        keep[y0:y1,x0:x1]|=ink[y0:y1,x0:x1] | (g[y0:y1,x0:x1]<bgg[y0:y1,x0:x1]-15)
    for x0,y0,x1,y1 in cfg.get('kill',[]):   # extra gloss bits to paint even if below cut
        keep[y0:y1,x0:x1]=False; above[y0:y1,x0:x1]=True
    paint=(above|below|zone)&~ndi.binary_dilation(keep,iterations=2)
    # paper colour
    pap=np.empty_like(im)
    for c in range(3):
        pc=ndi.percentile_filter(im[:,:,c][::3,::3],80,size=(25,25))
        pc=ndi.uniform_filter(pc,9)
        pap[:,:,c]=np.asarray(Image.fromarray(pc.astype(np.float32)).resize((W,H),Image.BILINEAR))
    rng=np.random.default_rng(0); noise=rng.normal(0,2.0,(H,W,1))
    out=im.copy(); out[paint]=(pap+noise)[paint]
    Image.fromarray(np.clip(out,0,255).astype(np.uint8)).save(M+name+'.png')
    report[name]={'touch':touch,'top_cut_range':[int(yt.min()),int(yt.max())]}
json.dump(report,open('mask_report.json','w') if not only else open('mask_report_partial.json','w'),indent=1)
print(json.dumps(report))
