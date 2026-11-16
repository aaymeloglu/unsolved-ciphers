import json, collections, re
B='/Users/aaymeloglu/git/unsolved-ciphers/milan-1494/'
KEY=json.load(open(B+'key.json'))['signs']
ALIAS=json.load(open(B+'niccolini-1492/alias.json'))
inv={}
for l in open(B+'niccolini-1492/signs-novalues.md'):
    m=re.match(r'\| (S\d+) \| (.*) \|',l)
    if m: inv[m.group(1)]=m.group(2)
SHAPE={
 'N1':'"#"/"ff": two to four tall slanted strokes crossed by one bar (transcriber N1)',
 'N3':'small 4/t-like or 5-like sign: short stem, arm to the right, short foot, sits on the line (transcriber N3)',
 'N4':'horizontal dash carrying a small e-like loop ("-e-"); same letter as S33 with a lead-in dash (transcriber N4)',
 'N6':'x with a short bar above it (transcriber N6)',
 'N9':'[word sign] NEW: circle with a central dot (⊙), standing alone',
 'N10':'[word sign, not a numeral] NEW: capital H, usually with an extra crossbar (Ħ), standing alone, often followed by 9',
 'N22':'[numeral] 22','N24':'[numeral] 24','N40':'[numeral] 40','N48':'[numeral] 48','N100':'[numeral] 100',
 'N2te':'[numeral] 2 with a raised "te"/"re" (possibly a cursive 24)',
}
NOTE={
 'S12':'÷ with dots not made out; n or c. Where dots are visible: dot above = n (S59), dot below only = c (S47), as on the sheet.',
 'S54':'Transcribers put two Niccolini letters under S54. (1) l: a b- or h-like sign with a looped or closed ascender and a bowl or hook at the foot (meglo, lo on c.176r; alla, catelani, napoli, italia, orsino on c.42r/42v). (2) d: a 5/ʒ-like sign, short flat top stroke, stem, open hook running below the line (da, cardi on 176r; di, cardinale, del, de conti, traditori). In side-by-side zooms the two forms look different, so label l with the loop and d with the flat top if the shape can be made out. At transcriber resolution keep both values.',
 'S51':'6 with the top stroke rising and curving = i. Niccolini\'s p is a σ (S80) whose flat top stroke runs to the right; at 1272 px it is easily taken for a 6 (the c.176r transcriber labelled the p of "potea" S51). Read S51 as i unless the top stroke is flat, then p.',
 'S80':'σ: loop with a flat top stroke running right = p (napoli x2, portico). Easily transcribed as S51.',
 'S69':'Plain b. Only Niccolini case aligned: the p of spirito (176r B6), labelled S69{N2}? by the transcriber. On doc 21 the p-sign is a b with a flag or hook on the ascender (S68, the sheet p): prospero, prefetto, parente, tempora, compagno. So b-for-p is the sheet value S68; plain S69 = p is single-case and may be an S68 whose flag was not seen.',
 'S74':'n-shape. f in fratello and prefetto (sheet value). a once, in naturalmente (176r L21): probably a joined "11" (= a) whose two strokes are linked by an arch.',
 'S37':'9 inside a word = r; 9 closing a word (after the last letter) = null, as the sheet\'s "9 closing a word" (S46).',
 'S33':'e-like sign with a large loop, no lead-in dash = o (sheet: null E9). With a lead-in dash it is N4, also o.',
 'S19':'small o with a flag/tilde = e (sheet). Once read o (nuouo, 42r L16), where the loop may be S33.',
 'S43':'∂ (round bowl, curled top) = g. A d-shape without visible bar stood for ll twice (alla 42r L15, castellano 42v L12); with the bar it is S77 (ll). The c.176r transcriber hesitated S43/S77 on a g.',
 'S14':'### once stood under the b of "buono" (42v L15), once closing "de conti" after 9. Treat as null at word end; b single case.',
 'S15':'double-barred stroke inside a word = ff (affectionato, 176r L21). Sheet: ## null.',
 'S16':'2 (or 2-like with a flat base) once = o (religiosi, 176r L19). Clear-text "2" is Niccolini\'s et/e; sheet 2 = b.',
 'S17':'φ-like group (c-curl, long descender, o) once = ct (affectionato); may be two signs.',
 'S48':'p = u (sheet); once stood for n in "aspirano" (42r L30), which may be a misformed ÷.',
 'N1':'Not glossed in any passage aligned here. On c.176r it ends B4, B8, B11 where the gloss has stopped; on 42r a ### closes "de conti". Treat as a run-final null. The ff inside "affectionato" was written S15, not N1.',
 'N10':'Ħ = Re (9r L6, L22; 9v L1). On 9v L1 a "·H·" has "74" written above it and the gloss "Trotto": probably H corrected to the number 74.',
 'N100':'100 = Re twice with clear gloss (9r L3 "1009", 42v L10); a third gloss on 42r L31 reads "d.l papa" or "dl Re" (unclear). Sheet: 10 = Papa, 11 = Re di Napoli.',
 'S70':'22 = S. Lodovico (gloss \"S. L.o\") 8 times on four letters: doc 6 c.9r, c.9v (x2), doc 59 c.124v, doc 62 c.133v (x2), doc 72 c.147v (x2). On the sheet S. L.o is 15 and 22 is S. di Pesaro, so Niccolini\'s 22 is the sheet\'s 15.',
 'N24':'24 = Ascanio 3 times: c.176r B1 and B5, doc 72 c.147v (\"pregassi 24\"). On 42v L18 a gloss \"Ta.\" (Taverna?) stands next to a 24; that one is unresolved.',
 'N2te':'\"2\" with small raised letters (te/re/n) followed by 9 = Ascanio, glossed \"As.\" 3 times (42v L18, 124v L1, 147v L17). Probably a cursive 24 (the raised letter being a reduced 4), so the transcribers may write it S16 or S16 S32.',
 'N9':'⊙ = papa (42r L16 "del nuouo papa") and papato/pontificato (42r L30 "aspirano al pontificato").',
 'N40':'40 = Duca (9r L5).',
 'N48':'48 with an unreadable gloss (9v L1); 48 occurs several times on doc 6.',
}
rows=[]
for l in open('align.tsv'):
    if l.startswith('#') or not l.strip(): continue
    f=l.rstrip('\n').split('\t'); doc,leaf,line,g,s,v,b=f[:7]
    s=s.split(); v=v.split(); assert len(s)==len(v),f
    rows.append((doc,leaf,line,g,s,v,b))
G=collections.defaultdict(collections.Counter); F=collections.defaultdict(collections.Counter); ex=collections.defaultdict(list)
for doc,leaf,line,g,s,v,b in rows:
    for si,vi in zip(s,v):
        if si=='?' or vi=='?': continue
        val='' if vi=='_' else vi
        (G if b in 'G' else F)[si][val]+=1
        e=f'{doc}/{leaf}/{line}: {g}'+('' if b=='G' else ' (fitted)' if b=='F' else ' (doubtful)')
        if e not in ex[si] and len(ex[si])<8: ex[si].append(e)
# S12 is the n/c union; derive from S12+S59+S47 rows
out={}
def sheetvals(k):
    if k in ALIAS: return KEY[ALIAS[k]].get('sheet')
    return None
for k in sorted(set(G)|set(F)|{'N1'}, key=lambda x:(x[0],int(re.sub(r'\D','',x) or 0),x)):
    g=G[k]; f=F[k]
    vals=[v for v,_ in g.most_common()]+[v for v,_ in f.most_common() if v not in g]
    if k=='N1': vals=['']
    n=sum(g.values())
    clean = n>=2 and len([v for v,c in g.items() if c>=1])<=2
    top=g.most_common(1)[0][1] if g else 0
    grade='C' if top>=2 and k not in ('N1','S14','S17','S16','S48') else 'S'
    sh=sheetvals(k)
    if k=='S37': sh=['r','']
    kv=KEY[ALIAS[k]]['values'] if k in ALIAS else None
    differs=[]
    if sh is None or sh==[]:
        agree=None
    elif not g:
        agree=None
    else:
        main=g.most_common(1)[0][0]
        differs=[v for v,c in g.items() if v not in sh]
        agree = (main in sh) and not any(g[v]>=2 for v in differs)
    if k=='N24': agree=False; sh=['[Ascanio] is 56 on the sheet']
    ent={'values':vals,'count':n,'examples':ex[k],'grade':grade,'agrees_with_sheet':agree,
         'shape':inv.get(k) or SHAPE.get(k,'')}
    if f: ent['fitted_count']=sum(f.values())
    if len(g)>1: ent['value_counts']=dict(g)
    if k in NOTE: ent['note']=NOTE[k]
    if sh is not None: ent['sheet']=sh
    if kv is not None and kv!=sh: ent['key_values']=kv
    if differs: ent['values_not_on_sheet']=differs
    out[k]=ent
json.dump(out,open(B+'niccolini-1492/niccolini-table.json','w'),indent=1,ensure_ascii=False)
print(len(out),'labels;',sum(sum(G[k].values()) for k in G),'gloss-aligned signs;',sum(sum(F[k].values()) for k in F),'fitted')
for k,e in out.items(): print(k,e['values'],e['count'],e['grade'],e['agrees_with_sheet'])
