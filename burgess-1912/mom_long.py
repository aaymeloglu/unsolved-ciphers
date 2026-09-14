import json,re,math,collections
from mom_parse import clean,pages
stories=json.load(open('wspages/stories.json'))
def norm(t): return re.sub(r'\bTHE END\b','',t.replace("'''","").replace("''",""))
alltxt=''
for s in stories: s['text']=norm(s['text']); alltxt+=s['text']
A=re.sub('[^A-Z]','',alltxt.upper())
Q=collections.Counter(A[i:i+4] for i in range(len(A)-3)); N=sum(Q.values())
def q(x): return sum(math.log10((Q.get(x[i:i+4],0)+0.01)/N) for i in range(len(x)-3))/max(1,len(x)-3)
words=set(w.strip().lower() for w in open('/usr/share/dict/words') if len(w.strip())>=6)
def longwords(x):
    x=x.lower(); f=set()
    for i in range(len(x)):
        for j in range(i+6,min(len(x),i+14)+1):
            if x[i:j] in words: f.add(x[i:j])
    return sorted(f,key=len,reverse=True)
def scan(name,x,win=24):
    x=x.upper()
    best=sorted(((q(x[i:i+win]),i) for i in range(0,max(1,len(x)-win))),reverse=True)[:3]
    print(f"{name}: len {len(x)} | words: {longwords(x)[:12]}")
    for sc,i in best: print(f"   {sc:.3f} @{i}: {x[i:i+win]}")
FL=lambda t:re.search('[A-Za-z]',t).group().upper()
LL=lambda t:re.findall('[A-Za-z]',t)[-1].upper()
# per story paragraph initials/finals
for s in stories:
    paras=[norm(p) for p in s['paras'] if re.search('[A-Za-z]',norm(p))]
    scan(s['title'][:22]+' para-first',''.join(FL(p) for p in paras))
    scan(s['title'][:22]+' para-last',''.join(LL(p) for p in paras))
# book-wide page initials/finals
pg=[norm(p['text']) for s in stories for p in s['pages'] if re.search('[A-Za-z]',norm(p['text']))]
scan('ALL pages first',''.join(FL(p) for p in pg)); scan('ALL pages last',''.join(LL(p) for p in pg))
# first letter of first FULL word per page? and last word
# sentence initials per story
for s in stories:
    sents=[x for x in re.split(r'(?<=[.!?])["”’]?\s+',s['text']) if re.search('[A-Za-z]',x)]
    scan(s['title'][:22]+' sent-first',''.join(FL(x) for x in sents))
# italics across book
it=[i for s in stories for i in re.findall(r"''(.+?)''",''.join(p['text'] for p in s['pages'])) if re.search('[A-Za-z]',i)]
print("ITALIC SPANS",len(it)); scan('italic first',''.join(FL(i) for i in it)); scan('italic last',''.join(LL(i) for i in it))
print("sample italics:",it[:60])
