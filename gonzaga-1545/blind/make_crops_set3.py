import json, os, random, re, sys, difflib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from PIL import Image
from cipherkit.transcribe import prepare
H=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT=sys.argv[2]
SW=dict(zip('abcdefghilm','nopqrstuxyz')); SW.update({v:k for k,v in SW.items()})
enc=lambda w:[SW[c] for c in w]
def toks(path,n):
    L=[l for l in open(path).read().split('\n') if l.strip()]
    t=L[n-1].split(); 
    if re.match(r'^(L?\d+[.:]?|\w+\s*L\d+)$',t[0]) and False: t=t[1:]
    return [x for x in t if x!='|']
norm=lambda t:t.rstrip('!')
_im={}
def page(p):
    if p not in _im:
        lay=json.load(open(f'{H}/layout/{p}.layout.json')); pr=lay['processing']
        im=prepare(Image.open(os.path.join(H,'..',lay['source'])),crop=pr['crop'],rotate=pr['rotate'],scale=pr['scale'])
        _im[p]=(im,lay['lines'])
    return _im[p]
def extent(p,n):
    im,lines=page(p); top,bot=lines[n-1]; g=im.convert('L').crop((0,top+15,im.width,bot-15)); px=g.load()
    cols=[x for x in range(g.width) if 0.03< sum(1 for y in range(0,g.height,2) if px[x,y]<120)/(g.height/2) <0.6]
    # drop isolated edge columns
    cols=[x for x in cols if 60<x<im.width-60]
    return min(cols),max(cols)
w=lambda t:1.7 if re.fullmatch(r'\d[\do]',norm(t)) else (2.4 if t.startswith('{') else 1.0)
def crop(p,n,i,j,ml=4,mr=4):
    T=toks(f'{H}/edition/{p}.cipher.txt',n); W=[w(t) for t in T]; tot=sum(W)
    a=max(0,i-ml); b=min(len(T),j+mr)
    x0,x1=extent(p,n); f0=sum(W[:a])/tot; f1=sum(W[:b])/tot
    im,lines=page(p); top,bot=lines[n-1]
    c=im.crop((max(0,int(x0+f0*(x1-x0))-130),top-40,min(im.width,int(x0+f1*(x1-x0))+130),bot+50))
    return c.resize((c.width*3,c.height*3),Image.Resampling.LANCZOS), T[a:b], T[i:j]
def find(p,n,frag,k=0):
    T=[norm(t) for t in toks(f'{H}/edition/{p}.cipher.txt',n)]; e=enc(frag)
    hits=[i for i in range(len(T)-len(e)+1) if T[i:i+len(e)]==e]
    if not hits: print('NOFIND',p,n,frag,' '.join(T)); return None
    return hits[k],hits[k]+len(e)

def seq(p,n,pat,k=0):
    T=[norm(t) for t in toks(f'{H}/edition/{p}.cipher.txt',n)]; e=pat.split()
    hits=[i for i in range(len(T)-len(e)+1) if T[i:i+len(e)]==e]; return hits[k],hits[k]+len(e)
T3=[('reread','A78r',3,'p b a y x','p b n y x'),('reread','A78r',4,'b x y c x r z b a g r','b x e b c x {h/t} 19 b a g r'),
 ('reread','A78r',12,'f x g e b h n','t g e b h n'),('reread','A78r',16,'f r z b','h g b'),('reread','A78r',16,'b o t y x t n g x','b o t y x r n g x'),
 ('reread','A78r',17,'q x b t e n g x n','q x b h n g x n'),('reread','A78r',19,'y n 61 c h b','y n b {1/i} c h b'),
 ('reread','A78v',3,'z x b a x c b g r','z x b n x c b g r'),('reread','A78v',8,'L9','L10'),('reread','A78v',24,'c r e 59 r t y x','c r c s z r t y x'),
 ('reread','A78v',27,'p b f r q x g b f p n a n','p b h q x g b h n a n'),('reread','A79r',1,'c x f n L','c x h L'),
 ('reread','A79r',1,'q n y x h b e a b','q n a b x h b e a b'),('reread','A79r',6,'x a y n L','x n y n L'),('reread','A79r',7,'e n d h n L','e n y h n L'),
 ('reread','A79r',11,'f x f n q','f x h {r/n} q'),
 ('control','A79r',7,'q x 59 x a g',''),('control','A78v',6,'x y 61 c r e b',''),('control','A79r',1,'f x h g x h a b',''),
 ('control','A78v',27,'h x f b a b h r a h g x',''),('control','A79r',2,'d h r 14 r c n e g x',''),('control','A78r',12,'s b e k n 25 n o n f g n',''),
 ('control','A79r',8,'c n e b a b p b a g e n e x','')]
random.seed(15440504); random.shuffle(T3); key=[]
for idx,(s,p,n,pat,old) in enumerate(T3,61):
    try: i,j=seq(p,n,pat,0)
    except Exception as ex: print('NOFIND',p,n,pat); continue
    im,win,tg=crop(p,n,i,j,ml=3,mr=3); im.save(f'{OUT}/c{idx:02d}.png'); key.append(dict(id=f'c{idx:02d}',set=s,page=p,line=n,i=i,j=j,frag=pat,window=' '.join(win),target=' '.join(tg),old=old))
json.dump(key,open(sys.argv[1],'w'),indent=1); print(len(key)); [print(k['id'],k['set'],k['page'],k['line'],k['target'],'|',k['window']) for k in key]
# c66 (A78v 8, the name code after "al"): the line is indented, so the proportional cut falls in the margin. Recut by position.
for k in key:
    if k['frag']=='L9':
        im,lines=page(k['page']); top,bot=lines[k['line']-1]; x0,_=extent(k['page'],k['line'])
        T=toks(f"{H}/edition/{k['page']}.cipher.txt",k['line']); W=[w(t) for t in T]
        a=int(x0+sum(W[:k['i']])/sum(W)*(extent(k['page'],k['line'])[1]-x0))
        c=im.crop((a+250,top-40,a+1000,bot+50)); c.resize((c.width*3,c.height*3),Image.Resampling.LANCZOS).save(f"{OUT}/{k['id']}.png")
