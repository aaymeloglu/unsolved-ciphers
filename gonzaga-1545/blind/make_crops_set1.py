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
targets=[ # set, page, line, cipher-frag (plaintext given), occurrence, extra right
 ('stem','A78r',10,'genti',0,0),('stem','A78v',26,'genti',0,0),('stem','B175r',5,'unti',0,0),
 ('stem','B174r',2,'gentia',0,0),('stem','B174r',6,'gentia',0,0),('stem','A78r',9,'enti',0,0),
 ('name','A78r',1,'casale',0,0),('name','A78r',3,'duami',0,3),('name','A78r',14,'ladriano',0,0),('name','A78r',13,'abbadino',0,0) if False else ('name','A78r',13,'adino',0,0),
 ('name','A78r',23,'monfe',0,5),('name','A78v',9,'mirandola',0,0),('name','A78v',10,'fe',0,6),('name','A78v',11,'bondeno',0,0),
 ('name','A78v',15,'dominich',0,4),('name','A78v',17,'pietro',0,6),('name','A78v',18,'sei',0,5),('name','A78v',20,'uinesia',0,0),
 ('name','A79r',15,'firen',0,2),('name','B174r',20,'dieta',0,0),('name','B174r',22,'luterani',0,0),('name','B174r',25,'bu',0,6),
 ('name','B174v',1,'tra',0,2),('name','B174v',2,'luterani',0,0),('name','B175r',1,'parpignano',0,0),('name','B175r',1,'fiandra',0,0),
 ('name','B175r',2,'turchesca',0,0),('name','B175r',8,'farnese',0,0),('name','B175r',11,'milano',0,0),('name','B175r',12,'toscana',0,0),
 ('name','B175r',19,'pierluigi',0,0),('name','B175r',22,'inghi',0,0),('name','B175v',7,'saluiati',0,0),('name','B175v',9,'sauoia',0,0),
 ('name','A78r',19,'cami',0,4),
]
random.seed(1545)
# controls: agreed h+vowel, agreed t r, agreed f n, across pages
ctrl=[]
for p in ['A78r','A78v','A79r','B174r','B174v','B175r','B175v']:
    nl=len(page(p)[1])
    for n in range(1,nl+1):
        E=[norm(t) for t in toks(f'{H}/edition/{p}.cipher.txt',n)]
        ok=[True]*len(E)
        for ps in 'CA':
            O=toks(f'{H}/transcription/{p}.{ps}.txt',n)
            m=[False]*len(E)
            for tag,i1,i2,j1,j2 in difflib.SequenceMatcher(None,E,O,autojunk=False).get_opcodes():
                if tag=='equal':
                    for i in range(i1,i2): m[i]=True
            ok=[a and b for a,b in zip(ok,m)]
        for i in range(2,len(E)-3):
            if not all(ok[i-1:i+3]): continue
            if E[i]=='h' and E[i+1] in 'nrxb': ctrl.append(('c_h',p,n,i,i+1))
            if E[i]=='t': ctrl.append(('c_tr',p,n,i,i+2))
            if E[i]=='f' and E[i+1]=='n': ctrl.append(('c_fn',p,n,i,i+2))
pick=[]
for k in ('c_h','c_tr','c_fn'):
    c=[x for x in ctrl if x[0]==k]; random.shuffle(c); pick+=c[:5]; print(k,len(c))
items=[]
for s,p,n,frag,k,er in targets:
    r=find(p,n,frag,k)
    if r: items.append((s,p,n,r[0],r[1]+er,frag))
for s,p,n,i,j in pick: items.append((s,p,n,i,j,''))
random.shuffle(items)
key=[]
for idx,(s,p,n,i,j,frag) in enumerate(items,1):
    im,win,tg=crop(p,n,i,j,ml=3,mr=3) if s!='name' else crop(p,n,i,j,ml=2,mr=2)
    im.save(f'{OUT}/c{idx:02d}.png'); key.append(dict(id=f'c{idx:02d}',set=s,page=p,line=n,i=i,j=j,frag=frag,window=' '.join(win),target=' '.join(tg)))
json.dump(key,open(sys.argv[1],'w'),indent=1); print(len(key))
