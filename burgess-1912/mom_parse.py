import json,re,html
pages=json.load(open('wspages/pages.json'))
pages={int(k):v for k,v in pages.items()}
TITLES=["Missing John Hudson","The Stolen Shakespeare","The MacDougal Street Affair","The Fanshawe Ghost","The Denton Boudoir Mystery","The Lorsson Elopement","The Calendon Kidnaping Case","Miss Dalrymple's Locket","Number Thirteen","The Trouble With Tulliver","Why Mrs. Burbank Ran Away","Mrs. Selwyn's Emerald","The Assassins' Club","The Luck of the Merringtons","The Count's Comedy","Priscilla's Presents","The Heir to Soothoid","The Two Miss Mannings","Van Asten's Visitor","The Middlebury Murder","Vengeance of the Pi Rho Nu","The Lady in Taupe","Mrs. Stellery's Letters","Black Light"]
def clean(wt):
    # strip noinclude header/footer
    wt=re.sub(r'<noinclude>.*?</noinclude>','',wt,flags=re.S)
    wt=re.sub(r'<section (begin|end)="[^"]*" ?/>','',wt)
    wt=re.sub(r'\{\{di\|([^}|]*)[^}]*\}\}',r'\1',wt)
    wt=re.sub(r'\{\{dropinitial\|([^}|]*)[^}]*\}\}',r'\1',wt)
    wt=re.sub(r'\{\{SIC\|([^}|]*)\|?[^}]*\}\}',r'\1',wt)
    wt=re.sub(r'\{\{hws\|[^}|]*\|([^}|]*)\}\}',r'\1',wt)   # keep whole word at page end
    wt=re.sub(r'\{\{hwe\|[^}|]*\|[^}|]*\}\}','',wt)         # drop continuation at page start
    wt=re.sub(r'\{\{(c|center)\|(.*?)\}\}',r'\2',wt,flags=re.S)
    wt=re.sub(r'\{\{(x+-larger|larger|smaller|sc|uc)\|(.*?)\}\}',r'\2',wt,flags=re.S)
    wt=re.sub(r'\{\{nop\}\}|\{\{dhr[^}]*\}\}|\{\{rule[^}]*\}\}|\{\{[^{}]*\}\}','',wt)
    wt=re.sub(r'<br\s*/?>','\n',wt)
    wt=re.sub(r'<[^>]+>','',wt)
    wt=html.unescape(wt)
    return wt
# build story structure
stories=[]; cur=None
for n in range(17,545):
    raw=pages.get(n) or ''
    secs=re.findall(r'<section begin="([^"]*)" ?/>',raw)
    txt=clean(raw)
    # detect story start: a line that equals a title in uppercase
    up=txt.upper()
    started=None
    for t in TITLES:
        T=t.upper().replace("’","'")
        m=re.search(r'(?m)^\s*'+re.escape(T)+r'\s*$',up)
        if m: started=(t,m.end()); break
    if started:
        t,pos=started
        pre=txt[:pos]; body=txt[pos:]
        cur={'title':t,'pages':[],'text':''}
        stories.append(cur)
        txt=body
    if cur is None: continue
    cur['pages'].append({'n':n,'text':txt})
    cur['text']+=txt+'\n'
if __name__=="__main__": print(len(stories),"stories")
for s in stories:
    s['paras']=[p.strip() for p in re.split(r'\n\s*\n',s['text']) if p.strip()]
    s['words']=re.findall(r"[A-Za-z][A-Za-z'’-]*",s['text'])
    s['italics']=re.findall(r"''(.+?)''",s['text'])
    if __name__=='__main__': print(f"{s['title'][:26]:26s} pages {s['pages'][0]['n']}-{s['pages'][-1]['n']} paras {len(s['paras']):3d} words {len(s['words']):5d} italics {len(s['italics']):3d} first={s['words'][0]} last={s['words'][-1]}")
json.dump(stories,open('wspages/stories.json','w'))
