#!/usr/bin/env python3
"""Homophone solver for the spelled-letter tokens of the 1646 'Queen's Court' cipher letter (f.10).
Symbols below 100 are letters (unknown except anchors fixed in the key file); codes 100 and above are
words (rendered from the key file when known, otherwise treated as a word boundary).

Usage: python3 solve.py key129.txt f10_ct.txt RESTARTS SEED
Needs corpus.txt in the working directory: lower-cased 17th-century English, letters and spaces only.
We built ours from the archive.org djvu text of Bruce, Charles I in 1646 (charlesiin1646le00chariala),
Evelyn, Diary and Correspondence vol. 4 (diarycorresponde41evel), and the Nicholas Papers vols 1-2
(nicholaspapersc00nichgoog, thenicholaspaper02camduoft).

Result on f.10: degenerate (vowel soup). 218 letter tokens over 61 symbols, mostly suffixes and short
fragments between word codes, is too thin for an n-gram solve even with 12 anchors fixed.
"""
import re,sys,math,random,collections,json
KEY={}
for ln in open(sys.argv[1]):
    ln=ln.split('#')[0].strip()
    if not ln: continue
    n,t=ln.split(None,1); KEY[n]=t.strip().lower()
CT=sys.argv[2]; RESTARTS=int(sys.argv[3]); SEED=int(sys.argv[4])
# ---- parse ----
seq=[]  # items: ('L',sym) ('W',text) ('B',) boundary
for ln in open(CT):
    if ln.startswith('#'): continue
    for tok in re.findall(r'\[[^\]]*\]|\S+',ln):
        if tok.startswith('['):
            seq.append(('W',re.sub(r'[^a-z ]','',tok.lower()))); continue
        t=tok.rstrip('?')
        if not t.isdigit(): seq.append(('B',)); continue
        n=int(t)
        if n<100 and t not in KEY: seq.append(('L',t))
        elif t in KEY: seq.append(('W',KEY[t].replace('-',' ')))
        else: seq.append(('B',))
    seq.append(('B',))
syms=sorted(set(s for k,s in [x for x in seq if x[0]=='L']),key=int)
FIX={s:KEY[s] for s in KEY if s.isdigit() and int(s)<100}
print('letter tokens',sum(1 for x in seq if x[0]=='L'),'symbols',len(syms),'fixed',len(FIX),file=sys.stderr)
# ---- LM ----
N=5
txt=' '+re.sub(r'\s+',' ',open('corpus.txt').read())+' '
C=collections.Counter(txt[i:i+N] for i in range(len(txt)-N+1))
C4=collections.Counter(txt[i:i+N-1] for i in range(len(txt)-N+2))
V=27
def lp(g):
    return math.log((C.get(g,0)+0.1)/(C4.get(g[:-1],0)+0.1*V))
LP={}
def score_str(s):
    s=' '+s+' '
    tot=0.0
    for i in range(len(s)-N+1):
        g=s[i:i+N]; v=LP.get(g)
        if v is None: v=lp(g); LP[g]=v
        tot+=v
    return tot
ALPH='abcdefghiklmnopqrstuvwxyz'
def render(m):
    out=[]; cur=[]
    for x in seq:
        if x[0]=='L': cur.append(m[x[1]])
        else:
            if cur: out.append(''.join(cur)); cur=[]
            if x[0]=='W': out.append(x[1])
            else: out.append('|')
    if cur: out.append(''.join(cur))
    return out
def score(m):
    parts=render(m)
    s=' '.join(p for p in parts if p!='|')
    s=re.sub(r' +',' ',s)
    return score_str(s)
def anneal(seed,iters=60000):
    rnd=random.Random(seed)
    m={s:FIX.get(s,rnd.choice(ALPH)) for s in syms}
    free=[s for s in syms if s not in FIX]
    cur=score(m); best=cur; bm=dict(m)
    T0,T1=2.0,0.05
    for it in range(iters):
        T=T0*(T1/T0)**(it/iters)
        s=rnd.choice(free); old=m[s]
        if rnd.random()<0.2:
            s2=rnd.choice(free); m[s],m[s2]=m[s2],m[s]; new=score(m)
            if new>=cur or rnd.random()<math.exp((new-cur)/T): cur=new
            else: m[s],m[s2]=m[s2],m[s]
        else:
            m[s]=rnd.choice(ALPH); new=score(m)
            if new>=cur or rnd.random()<math.exp((new-cur)/T): cur=new
            else: m[s]=old
        if cur>best: best=cur; bm=dict(m)
    return best,bm
res=[]
for r in range(RESTARTS):
    b,m=anneal(SEED*100+r); res.append((b,m))
    print(f'[{r}] {b:.1f}',file=sys.stderr)
res.sort(key=lambda x:-x[0])
for b,m in res[:3]:
    print('SCORE',round(b,1)); print(' '.join(render(m))); print(json.dumps(m,sort_keys=True)); print()
