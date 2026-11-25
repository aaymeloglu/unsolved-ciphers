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
T2=[('code','A78v',8,'L10',0),('code','B175r',7,'L10',1),('code','B175r',24,'L10',0),('code','B174r',3,'L10',0),('code','B174r',17,'L9',0),('code','B174r',17,'L10',0),
 ('name','A79r',15,'s 27 x e r a k r',0),('name','B174v',11,'s r x a r f',0),('name','A78v',18,'f r x z x',0),('stem','A78r',10,'y x t r a g r',0),('code','B174v',9,'L9',0)]
random.seed(1544); random.shuffle(T2); key=[]
for idx,(s,p,n,pat,k) in enumerate(T2,50):
    try: i,j=seq(p,n,pat,k)
    except Exception as ex: print('NOFIND',p,n,pat); continue
    im,win,tg=crop(p,n,i,j,ml=3,mr=3); im.save(f'{OUT}/c{idx:02d}.png'); key.append(dict(id=f'c{idx:02d}',set=s,page=p,line=n,i=i,j=j,frag=pat,window=' '.join(win),target=' '.join(tg)))
json.dump(key,open(sys.argv[1],'w'),indent=1); print(len(key)); [print(k['id'],k['page'],k['line'],k['target'],'|',k['window']) for k in key]
