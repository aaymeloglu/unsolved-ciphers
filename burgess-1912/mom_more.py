import json,re,math,collections
import mom_parse
from mom_parse import clean,pages
stories=json.load(open('wspages/stories.json'))
def norm(t): return re.sub(r'\bTHE END\b','',t.replace("'''","").replace("''",""))
for s in stories:
    s['text']=norm(s['text']); s['paras']=[norm(p) for p in s['paras'] if re.search('[A-Za-z]',norm(p))]
    s['words']=re.findall(r"[A-Za-z][A-Za-z'’-]*",s['text'])
    s['sents']=[x for x in re.split(r'(?<=[.!?])["”’]?\s+',s['text']) if re.search('[A-Za-z]',x)]
    s['letters']=re.sub('[^A-Za-z]','',s['text']).upper()
A=''.join(s['letters'] for s in stories)
Q=collections.Counter(A[i:i+4] for i in range(len(A)-3)); N=sum(Q.values())
def q(x): 
    x=re.sub('[^A-Z]','',x.upper()); return sum(math.log10((Q.get(x[i:i+4],0)+0.01)/N) for i in range(len(x)-3))/max(1,len(x)-3)
words=set(w.strip().lower() for w in open('/usr/share/dict/words') if len(w.strip())>=5)
def lw(x):
    x=x.lower(); f=set()
    for i in range(len(x)):
        for j in range(i+5,min(len(x),i+14)+1):
            if x[i:j] in words: f.add(x[i:j])
    return sorted(f,key=len,reverse=True)[:6]
FL=lambda w:re.search('[A-Za-z]',w).group().upper()
LL=lambda w:re.findall('[A-Za-z]',w)[-1].upper()
print("== diagonal acrostics (unit k of story k) ==")
for off in range(0,4):
  for name,fn in [('word first',lambda s,k:FL(s['words'][k])),('word last',lambda s,k:LL(s['words'][k])),('word -k first',lambda s,k:FL(s['words'][-1-k])),('word -k last',lambda s,k:LL(s['words'][-1-k])),('letter k',lambda s,k:s['letters'][k]),('letter -k',lambda s,k:s['letters'][-1-k]),('sent k first',lambda s,k:FL(s['sents'][k])),('sent k last',lambda s,k:LL(s['sents'][k])),('para k first',lambda s,k:FL(s['paras'][k])),('para k last',lambda s,k:LL(s['paras'][k])),('para -k first',lambda s,k:FL(s['paras'][-1-k])),('para -k last',lambda s,k:LL(s['paras'][-1-k]))]:
    x=''.join(fn(s,i+off) for i,s in enumerate(stories))
    print(f"{q(x):.3f} {name} off{off}: {x} {lw(x)}")
print("== contents page numbers as indices ==")
cont=[1,23,44,65,83,103,128,148,165,186,203,225]
# get full contents list from page 9
c9=pages[9]; nums=[int(n) for n in re.findall(r'\{\{ts\|ar\}\} \| (\d+)',c9)]; print("contents pages:",nums)
for name,fn in [('word n first',lambda s,n:FL(s['words'][n-1])),('word n last',lambda s,n:LL(s['words'][n-1])),('letter n',lambda s,n:s['letters'][n-1]),('para n first',lambda s,n:FL(s['paras'][n-1]) if n-1<len(s['paras']) else '?'),('sent n first',lambda s,n:FL(s['sents'][n-1]) if n-1<len(s['sents']) else '?'),('n mod 26',lambda s,n:chr(64+((n-1)%26)+1))]:
    x=''.join(fn(s,n) for s,n in zip(stories,nums)); print(f"{q(x):.3f} {name}: {x} {lw(x)}")
# page numbers -> word index into the WHOLE book? and into the intro
allwords=re.findall(r"[A-Za-z][A-Za-z'’-]*",''.join(s['text'] for s in stories))
print("book word n first:",''.join(FL(allwords[n-1]) for n in nums))
intro=norm('\n'.join(clean(pages[n] or '') for n in (11,12,13))); iw=re.findall(r"[A-Za-z][A-Za-z'’-]*",intro)
print("intro words",len(iw)); 
print("== every nth word/letter of whole book ==")
for n in (50,100,150,200,250,300,365,400,500,1000):
    x=''.join(FL(w) for w in allwords[::n]); print(f"every {n}th word first: len {len(x)} {q(x):.3f} {x[:60]} {lw(x)}")
for n in (500,1000,1912,2000,5000):
    x=A[::n]; print(f"every {n}th letter: len {len(x)} {q(x):.3f} {x[:60]} {lw(x)}")
print("== word lists to eyeball ==")
def show(name,fn): print(name+':',' | '.join(fn(s) for s in stories))
show('word2',lambda s:s['words'][1]); show('word3',lambda s:s['words'][2]); show('last2',lambda s:s['words'][-2]); show('last3',lambda s:s['words'][-3])
show('first word of last para',lambda s:re.findall(r"[A-Za-z][A-Za-z'’-]*",s['paras'][-1])[0])
show('last word of first para',lambda s:re.findall(r"[A-Za-z][A-Za-z'’-]*",s['paras'][0])[-1])
show('first word para2',lambda s:re.findall(r"[A-Za-z][A-Za-z'’-]*",s['paras'][1])[0])
show('first word sent2',lambda s:re.findall(r"[A-Za-z][A-Za-z'’-]*",s['sents'][1])[0])
show('last word of last sent-1',lambda s:re.findall(r"[A-Za-z][A-Za-z'’-]*",s['sents'][-2])[-1])
show('first word of last sent',lambda s:re.findall(r"[A-Za-z][A-Za-z'’-]*",s['sents'][-1])[0])
show('middle word',lambda s:s['words'][len(s['words'])//2])
show('word 24',lambda s:s['words'][23]); show('word 12',lambda s:s['words'][11])
print("intro para first words:",[re.findall(r"[A-Za-z]+",p)[0] for p in re.split(r'\n\s*\n',intro) if re.search('[A-Za-z]',p)])
print("intro para last words:",[re.findall(r"[A-Za-z]+",p)[-1] for p in re.split(r'\n\s*\n',intro) if re.search('[A-Za-z]',p)])
