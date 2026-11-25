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
T4=[('reread', 'B174r', 7, 'n L 53 z u', 'n L 55 z u'), ('reread', 'B174v', 8, 'b e h b {y/a}', 'b e b {y/a}'), ('reread', 'B174v', 11, 's r e a r', 's r x a r'), ('reread', 'B174v', 13, 'y r 95 p b', 'y r z s p b'), ('reread', 'B174v', 13, 'b t a x', 'b t r a x'), ('reread', 'B174v', 15, 'r 53 q x p', 'r 53 f x p'), ('reread', 'B174v', 16, 'a r f r 24 r', 'a r h 24 r'), ('reread', 'B174v', 16, 'r h r e b', 'r h n e b'), ('reread', 'B174v', 16, 'd h r f g', 'd h f g'), ('reread', 'B174v', 17, '31 f x n', '31 f n'), ('reread', 'B174v', 21, 'a g r e g r', 'a g n d g r'), ('reread', 'B174v', 21, 'g r a r e y n', 'g r n'), ('reread', 'B174v', 21, 'y n', 'y n u e a n'), ('reread', 'B175r', 7, 'x y p b e', 'x y f b e'), ('reread', 'B175r', 20, 'x n 61 f n', 'x n b f n'), ('reread', 'B175r', 22, 'q x e n', 'q x c e n'), ('reread', 'B175r', 22, 'e b z n q', 'e b g n q'), ('reread', 'B175r', 24, '14 n 96 L q', '14 n z b L q'), ('reread', 'B175r', 25, 'n y n 96 3o c', 'n y a z b 3o c'), ('reread', 'B175v', 4, 'y n 96 x a', 'y n z b x a'), ('reread', 'B175v', 4, 'y x z r 22', 'y x 19 r 22'), ('reread', 'B175v', 6, 'x n 5 r 16', 'x n s r 16'), ('reread', 'B175v', 6, 'x f b t', 'x f h h n b t'), ('reread', 'B175v', 6, 'f b t a b', 'f b'), ('reread', 'B175v', 7, '3o c r e', '3o c x'), ('reread', 'B175v', 8, 'n p r f x', 'n p n f x'), ('reread', 'B175v', 8, 'y n o n', 'y n t o n'), ('reread', 'B175v', 9, 'h r a h g', 'h r q h g'), ('reread', 'B175v', 11, 'e r t n h', 'e r f n h'), ('reread', 'B175v', 11, 'x 3o f n 17 r', 'x 3o {f/?} {n/h} 17 r'), ('reread', 'B175v', 12, 'r b a q r', 'r b q r'), ('reread', 'B175v', 14, 'n 3o 4o z u', 'n 3o q b z u'), ('reread', 'B175v', 15, 'r e y n z x', 'r e {y/h} {n/?} z x'), ('reread', 'B175v', 15, 'n L 64 y b', 'n L b q y b'), ('reread', 'B175v', 19, 'n a', 'r n a'), ('reread', 'B175v', 19, 'n a g b', 'n g b'), ('reread', 'B175v', 25, 'b x 61 z u n', 'b x b 19 u n'), ('reread', 'B175v', 26, 'x 3o f b a 25 b', 'x 3o h {n/a} 25 b'), ('control', 'B174r', 5, 'r d h r f g', ''), ('control', 'B175v', 24, 'r a q r e n', ''), ('control', 'B175v', 13, 'p b y z r 22', ''), ('control', 'B174r', 11, 'n 14 n y g e', ''), ('control', 'B175r', 15, '53 c b g r a', ''), ('control', 'B174r', 16, 'b q x p r e', ''), ('control', 'B174r', 23, 'q x q x b L', ''), ('control', 'B174r', 1, 'x f g b c r', ''), ('control', 'B175r', 18, '59 s b e f x', '')]
random.seed(15440109); random.shuffle(T4); key=[]
for idx,(s,p,n,pat,old) in enumerate(T4,101):
    try: i,j=seq(p,n,pat,0)
    except Exception as ex: print('NOFIND',p,n,pat); continue
    im,win,tg=crop(p,n,i,j,ml=2,mr=2); im.save(f'{OUT}/c{idx}.png'); key.append(dict(id=f'c{idx}',set=s,page=p,line=n,i=i,j=j,frag=pat,window=' '.join(win),target=' '.join(tg),old=old))
json.dump(key,open(sys.argv[1],'w'),indent=1); print(len(key))
