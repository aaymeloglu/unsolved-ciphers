#!/usr/bin/env python3
"""Homophonic substitution solver for the Forster 1644 letter.
Symbols -> letters; word boundaries known (commas) or uncertain (line breaks).
Score = char 5-gram log-prob over words (with spaces) + lexicon bonus.
Simulated annealing with restarts. Usage: python3 solver.py [restarts] [seed] [split_lines 0/1]
"""
import re, math, random, sys, collections, json

# ---------- ciphertext ----------
CT = open('ct.txt').read().split('\n')
def parse(split_lines):
    words=[]; cur=[]
    for ln in CT:
        ln=re.sub(r'\[.*?\]','|',ln)
        for num,comma,bar in re.findall(r'(\d+|[a-z])\.?|(,)|(\|)',ln):
            if comma or bar:
                if cur: words.append(cur); cur=[]
            else: cur.append(num)
        if split_lines and cur: words.append(cur); cur=[]
    if cur: words.append(cur)
    return words

# ---------- language model ----------
N=4
def build_lm(path='corpus_clean.txt'):
    txt=open(path).read()
    txt=' '+re.sub(r'\s+',' ',txt)+' '
    counts=collections.Counter(txt[i:i+N] for i in range(len(txt)-N+1))
    ctx=collections.Counter(txt[i:i+N-1] for i in range(len(txt)-N+2))
    V=27
    lp={}
    total=sum(counts.values())
    return counts,ctx,V
COUNTS,CTX,V=build_lm()
NTOT=sum(COUNTS.values())
LMCACHE={}
def lp(g):
    v=LMCACHE.get(g)
    if v is None:
        c=COUNTS.get(g,0)
        v=math.log10((c+0.5)/NTOT)
        LMCACHE[g]=v
    return v
LEX=set(open('lexicon.txt').read().split())
for line in open('fr_50k.txt'):
    p=line.split()
    if len(p)>=2 and len(LEX)<80000: LEX.add(p[0])

def score_text(words_txt):
    s=' '+' '.join(words_txt)+' '
    sc=sum(lp(s[i:i+N]) for i in range(len(s)-N+1))
    lexb=sum(len(w) for w in words_txt if len(w)>=2 and w in LEX)
    return sc+1.0*lexb

ALPH='abcdefghijklmnopqrstuvxyz'  # no w
def decode(words,m): return [''.join(m[s] for s in w) for w in words]

def anneal(words,syms,seed,iters=120000,T0=3.0,T1=0.05,init=None):
    rnd=random.Random(seed)
    m=dict(init) if init else {s:rnd.choice(ALPH) for s in syms}
    cur=score_text(decode(words,m)); best=cur; bestm=dict(m)
    for it in range(iters):
        T=T0*(T1/T0)**(it/iters)
        s=rnd.choice(syms); old=m[s]
        if rnd.random()<0.15:
            s2=rnd.choice(syms); m[s],m[s2]=m[s2],m[s]; old2=old; old=(s2,)
        else:
            m[s]=rnd.choice(ALPH)
        new=score_text(decode(words,m))
        if new>=cur or rnd.random()<math.exp((new-cur)/T):
            cur=new
            if cur>best: best=cur; bestm=dict(m)
        else:
            if isinstance(old,tuple): m[s],m[old[0]]=m[old[0]],m[s]
            else: m[s]=old
    return best,bestm

if __name__=='__main__':
    restarts=int(sys.argv[1]) if len(sys.argv)>1 else 8
    seed=int(sys.argv[2]) if len(sys.argv)>2 else 1
    split=int(sys.argv[3]) if len(sys.argv)>3 else 1
    words=parse(split)
    syms=sorted(set(s for w in words for s in w))
    # initial prior: numbers -> vowels, letters -> consonants
    results=[]
    for r in range(restarts):
        rnd=random.Random(seed*100+r)
        init={s:(rnd.choice('aeiou') if s.isdigit() else rnd.choice('bcdfglmnpqrstvxz')) for s in syms}
        if r%2: init=None
        b,m=anneal(words,syms,seed*100+r,init=init)
        results.append((b,m))
        print(f"[{r}] {b:.1f} | {' '.join(decode(words,m))}", flush=True)
    results.sort(key=lambda x:-x[0])
    b,m=results[0]
    print("\nBEST",b); print(' '.join(decode(words,m)))
    print(json.dumps(m,sort_keys=True))
