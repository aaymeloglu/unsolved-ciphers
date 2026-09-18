import json,re,math,collections
import mom_parse
from mom_parse import clean,pages,TITLES
stories=json.load(open('wspages/stories.json'))
def norm(t):
    t=t.replace("'''","").replace("''","")
    t=re.sub(r'\bTHE END\b','',t)
    return t
for s in stories:
    s['text']=norm(s['text']); s['paras']=[norm(p) for p in s['paras'] if re.search('[A-Za-z]',norm(p))]
    s['words']=re.findall(r"[A-Za-z][A-Za-z'’-]*",s['text'])
    s['sents']=[x.strip() for x in re.split(r'(?<=[.!?])["”’]?\s+',s['text']) if re.search('[A-Za-z]',x)]
    s['letters']=re.sub('[^A-Za-z]','',s['text']).upper()
    s['pagetexts']=[norm(p['text']) for p in s['pages'] if re.search('[A-Za-z]',norm(p['text']))]
# intro pages 11-13
intro=norm('\n'.join(clean(pages[n] or '') for n in (11,12,13)))
# --- scorer: quadgram from the book's own text (cipherkit.CharLM, add-0.01)
from cipherkit import CharLM
alltxt=re.sub('[^A-Z]','',(intro+''.join(s['text'] for s in stories)).upper())
LM=CharLM.from_text(alltxt,order=4,alpha=0.01)
def qscore(x):
    x=re.sub('[^A-Z]','',x.upper())
    if len(x)<4: return -99
    return LM.per_window(x)
words=set(w.strip().lower() for w in open('/usr/share/dict/words') if len(w.strip())>=4)
def longwords(x,minlen=5):
    x=x.lower(); found=set()
    for i in range(len(x)):
        for j in range(i+minlen,min(len(x),i+12)+1):
            if x[i:j] in words: found.add(x[i:j])
    return sorted(found,key=len,reverse=True)[:6]
FL=lambda w:w[0].upper(); LL=lambda w:re.sub("[^A-Za-z]","",w)[-1].upper()
cands={}
def add(name,units):
    if all(units): cands[name]=''.join(units)
for k in range(12):
    add(f'first letter of word {k+1}',[FL(s['words'][k]) for s in stories])
    add(f'last letter of word {k+1}',[LL(s['words'][k]) for s in stories])
    add(f'first letter of word -{k+1}',[FL(s['words'][-1-k]) for s in stories])
    add(f'last letter of word -{k+1}',[LL(s['words'][-1-k]) for s in stories])
for k in range(8):
    add(f'first letter of sentence {k+1}',[FL(re.search("[A-Za-z]",s['sents'][k]).group()) for s in stories])
    add(f'last letter of sentence {k+1}',[LL(re.findall("[A-Za-z]+",s['sents'][k])[-1]) for s in stories])
    add(f'first letter of sentence -{k+1}',[FL(re.search("[A-Za-z]",s['sents'][-1-k]).group()) for s in stories])
    add(f'last letter of sentence -{k+1}',[LL(re.findall("[A-Za-z]+",s['sents'][-1-k])[-1]) for s in stories])
    add(f'first letter of para {k+1}',[FL(re.search("[A-Za-z]",s['paras'][k]).group()) for s in stories])
    add(f'last letter of para {k+1}',[LL(re.findall("[A-Za-z]+",s['paras'][k])[-1]) for s in stories])
    add(f'first letter of para -{k+1}',[FL(re.search("[A-Za-z]",s['paras'][-1-k]).group()) for s in stories])
    add(f'last letter of para -{k+1}',[LL(re.findall("[A-Za-z]+",s['paras'][-1-k])[-1]) for s in stories])
    add(f'first letter of page {k+1}',[FL(re.search("[A-Za-z]",s['pagetexts'][k]).group()) for s in stories if k<len(s['pagetexts'])] if all(k<len(s['pagetexts']) for s in stories) else [])
    add(f'last letter of page {k+1}',[LL(re.findall("[A-Za-z]+",s['pagetexts'][k])[-1]) for s in stories] if all(k<len(s['pagetexts']) for s in stories) else [])
    add(f'first letter of page -{k+1}',[FL(re.search("[A-Za-z]",s['pagetexts'][-1-k]).group()) for s in stories])
    add(f'last letter of page -{k+1}',[LL(re.findall("[A-Za-z]+",s['pagetexts'][-1-k])[-1]) for s in stories])
for k in range(20):
    add(f'letter {k+1} of story',[s['letters'][k] for s in stories])
    add(f'letter -{k+1} of story',[s['letters'][-1-k] for s in stories])
add('middle letter',[s['letters'][len(s['letters'])//2] for s in stories])
add('middle word first letter',[FL(s['words'][len(s['words'])//2]) for s in stories])
for k in range(5):
    add(f'title word {k+1} first letter',[FL(re.findall("[A-Za-z]+",s['title'])[k]) if k<len(re.findall("[A-Za-z]+",s['title'])) else '' for s in stories])
    add(f'title letter {k+1}',[re.sub('[^A-Za-z]','',s['title'])[k].upper() for s in stories])
    add(f'title letter -{k+1}',[re.sub('[^A-Za-z]','',s['title'])[-1-k].upper() for s in stories])
add('title last word last letter',[LL(re.findall("[A-Za-z]+",s['title'])[-1]) for s in stories])
for s in stories: s['italics']=[i for i in s['italics'] if re.search('[A-Za-z]',i)]
add('first italic first letter',[FL(re.search("[A-Za-z]",s['italics'][0]).group()) if s['italics'] else '' for s in stories])
add('last italic last letter',[LL(re.findall("[A-Za-z]+",s['italics'][-1])[-1]) if s['italics'] else '' for s in stories])
add('first quoted speech first letter',[FL(re.search(r'["“]\s*([A-Za-z])',s['text']).group(1)) for s in stories])
add('first quoted speech last letter',[LL(re.search(r'["“]([^"”]+)["”]',s['text']).group(1).strip().split()[-1]) for s in stories])
add('word count mod 26',[chr(64+((len(s['words'])-1)%26)+1) for s in stories])
add('page count',[chr(64+len(s['pages'])) if len(s['pages'])<=26 else '?' for s in stories])
add('para count mod 26',[chr(64+((len(s['paras'])-1)%26)+1) for s in stories])
add('first word length',[chr(64+len(s['words'][0])) for s in stories])
add('last word length',[chr(64+len(re.sub("[^A-Za-z]","",s['words'][-1]))) for s in stories])
add('first word length -> letter of first word? (nth letter)',[s['letters'][len(s['words'][0])-1] for s in stories])
res=[]
for n,x in cands.items():
    for tag,y in (('',x),(' [rev]',x[::-1])):
        res.append((qscore(y),n+tag,y,longwords(y)))
res.sort(reverse=True)
print("controls: first-of-first",qscore('THEAUTHORISGELETTBURGESS'),"last-of-last",qscore('FALSETOLIFEANDFALSETOART'))
print("median",sorted(r[0] for r in res)[len(res)//2])
for r in res[:45]: print(f"{r[0]:.3f} {r[1]:42s} {r[2]} {r[3]}")
print("--- any with a dictionary word >=6:")
for r in res:
    if any(len(w)>=6 for w in r[3]): print(f"{r[0]:.3f} {r[1]:42s} {r[2]} {r[3]}")
