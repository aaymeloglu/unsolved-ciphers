#!/usr/bin/env python3
"""Beam search over lexicon words for a homophonic cipher with known word boundaries.
Constraint: same cipher symbol -> same letter. Different symbols may share a letter.
Usage: python3 dict_solver.py [beam] [skip_penalty] [maxlen_forced]
"""
import re, sys, math, collections, unicodedata, json
BEAM=int(sys.argv[1]) if len(sys.argv)>1 else 3000
SKIP=float(sys.argv[2]) if len(sys.argv)>2 else -25.0
MAXLEN=int(sys.argv[3]) if len(sys.argv)>3 else 7   # words longer than this may be skipped

# ---------- ciphertext ----------
words=[]; cur=[]
for ln in open('ct.txt').read().split('\n'):
    ln=re.sub(r'\[.*?\]','|',ln)
    for num,comma,bar in re.findall(r'(\d+|[a-z])\.?|(,)|(\|)',ln):
        if comma or bar:
            if cur: words.append(cur); cur=[]
        else: cur.append(num)
if cur: words.append(cur)

# ---------- lexicon with 17th-c. variants ----------
def strip(t):
    t=unicodedata.normalize('NFD',t); return ''.join(c for c in t if unicodedata.category(c)!='Mn')
freq=collections.Counter()
raw=collections.Counter()
for f in ['corneille_31628.txt','corneille_34445.txt','corneille_36011.txt','corneille_39739.txt','descartes.txt']:
    s=open(f,encoding='utf-8',errors='ignore').read().lower().replace('œ','oe').replace('’',"'")
    for w in re.findall(r"[a-zàâäéèêëîïôöùûüç]+",s): raw[w]+=1
for w,c in raw.items():
    if re.fullmatch(r'[ivxlc]{2,}',w) and w not in ('il','ci','vil'): continue
    if w in ('var','ibid','op','cit','fol','vol','tom','sc','sq'): continue
    base=strip(w); freq[base]+=c
    # old spellings
    v=set()
    if re.search(r'[êâôîû]',w): v.add(strip(re.sub(r'([êâôîû])',lambda m:strip(m.group(1))+'s',w)))
    if w.endswith('ait'): v.add(base[:-3]+'oit')
    if w.endswith('aient'): v.add(base[:-5]+'oient')
    if w.endswith('ais'): v.add(base[:-3]+'ois')
    if 'j' in base: v.add(base.replace('j','i'))
    if base.endswith('i') and len(base)>2: v.add(base[:-1]+'y')
    if base.endswith('oi'): v.add(base[:-2]+'oy')
    if base.endswith('ui'): v.add(base[:-2]+'uy')
    if base.startswith('v') and len(base)>2 and base[1] in 'aeiouy': v.add('u'+base[1:])   # u/v interchange rarely; skip
    if base.startswith('u'): v.add('v'+base[1:])
    for x in v:
        if x!=base: freq[x]+=max(1,c//3)
for i,line in enumerate(open('fr_50k.txt')):
    p=line.split()
    if len(p)<2: continue
    w=strip(p[0])
    if not re.fullmatch(r'[a-z]+',w) or re.fullmatch(r'[ivxlc]{2,}',w): continue
    if i<25000: freq[w]+=max(1,int(p[1])//200000)
for line in open('lex_old.txt'):
    p=line.split()
    if p[-1]=='50': freq[strip(p[0])]+=30
for w in ['exeter','excester','exester','oxford','oxfort','londres','paris','bristol','bristoll','yorck','yorke','falmouth','plimouth','plymouth','pendennis','essex','waller','digby','iermyn','jermyn','goring','hopton','maurice','rupert','ruprecht','cornouaille','cornwall','devon','somerset','bath','reyne','royne','roy','madame','maiesté','maieste','majeste','monseigneur','mazarin','mazarini','richelieu','louvre','angleterre','escosse','irlande','parlement','armee','armées','armees','cavalerie','infanterie','argent','poudre','munitions','vaisseaux','vaisseau','navire','navires','port','mer','passage','lettres','lettre','chiffre','nouvelles','secours','asseurer','asseure','asseuré','asseurance','tousiours','desia','encores','encor','ceste','cest','cestuy','ceux','celle','celles','iceluy','icelle','laquelle','lequel','lesquels','auquel','duquel','sieur','sr','mr','md','mons','vostre','nostre','sa','maté','mate','majesté','sadite','ledit','ladite','lesdits','susdit','susdite']:
    freq[w]+=40
print("lexicon size",len(freq),file=sys.stderr)
bylen=collections.defaultdict(list)
for w,c in freq.items(): bylen[len(w)].append((w,math.log(c+1)))
for k in bylen: bylen[k].sort(key=lambda x:-x[1])

def consistent(cw,pw,m):
    add={}
    for s,ch in zip(cw,pw):
        v=m.get(s,add.get(s))
        if v is None: add[s]=ch
        elif v!=ch: return None
    return add

# dynamic ordering: prefer short words with many distinct symbols shared
order=[]
remaining=list(range(len(words)))
assigned=set()
while remaining:
    def key(i):
        w=words[i]; L=len(w); shared=len(set(w)&assigned)
        return (-(shared/ L), L if L<=MAXLEN else 100+L)
    i=min(remaining,key=key); order.append(i); remaining.remove(i); assigned|=set(words[i])
print("order",[(i+1,''.join(x+' ' for x in words[i]).strip()) for i in order],file=sys.stderr)

beam=[(0.0,{},[])]
for idx in order:
    cw=words[idx]; L=len(cw)
    cands=bylen.get(L,[])
    newbeam=[]
    for sc,m,hist in beam:
        n=0
        for pw,lc in cands:
            add=consistent(cw,pw,m)
            if add is None: continue
            m2=dict(m); m2.update(add)
            newbeam.append((sc+lc,m2,hist+[(idx,pw)]))
            n+=1
            if n>=400: break
        if n==0 or L>MAXLEN:
            newbeam.append((sc+SKIP,m,hist+[(idx,'?'*L)]))
    newbeam.sort(key=lambda x:-x[0])
    # dedupe by mapping
    seen=set(); pruned=[]
    for st in newbeam:
        k=tuple(sorted(st[1].items()))
        if k in seen: continue
        seen.add(k); pruned.append(st)
        if len(pruned)>=BEAM: break
    beam=pruned
    print(f"word {idx+1} ({' '.join(cw)}): beam {len(beam)} best {beam[0][0]:.1f}",file=sys.stderr)

def render(hist,m):
    d=dict(hist); out=[]
    for i,w in enumerate(words):
        out.append(''.join(m.get(s,'?') for s in w))
    return ' '.join(out)
for sc,m,hist in beam[:15]:
    print(f"{sc:.1f} | {render(hist,m)}")
print(json.dumps(beam[0][1],sort_keys=True))
