"""Auditable two-table parser. Incomplete key; never claims a full decipherment.

The first mark is displaced one digit from the boundary implied by the ordinary
parser. This is a named hypothesis, not a change to the source transcription.
Unrecognized digit groups are retained; no silent digit repair occurs.
"""
import json
from pathlib import Path
P=Path(__file__).resolve().parent
rows=json.loads((P/'ciphertext-lines.json').read_text())
digits=[]; loc=[]; marks=[]
for row,line in enumerate(rows,1):
 for col,c in enumerate(line,1):
  if c.isascii() and c.isdigit():digits.append(c);loc.append((row,col))
  elif c=='^':marks.append((len(digits),line[col:col+1]))
s=''.join(digits)
controls={n-2:(s[n-2:n+1],mark) for n,mark in marks}
# 885 at offset 108 intersects ordinary 31268. Keep this exception visible.
controls.pop(108)
controls[109]=('854','"')
key={}
for state,name in [('A','working-prima-v4.tsv'),('B','working-secunda.tsv')]:
 f=P/name
 key[state]=dict(l.split('\t',1) for l in f.read_text().splitlines()) if f.exists() else {}
from cipher_model import parse_units
out = parse_units(s, controls, key, loc)
report={'status':'partial; provisional key and unresolved source errors','hypotheses':['first mark interpreted at code 854, offset 109, rather than overlapping 885 at offset 108'],'tokens':out}
(P/'two-table-parsing.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
lines=[]
for row in range(1,len(rows)+1):
 ts=[t for t in out if t['source_start'][0]==row]
 lines.append(f'ROW {row}: '+' '.join("{}:{}={}".format(t["table"],t["code"],t["value"]) for t in ts if t['kind']!='null'))
 lines.append(''.join(t['value'] for t in ts))
(P/'two-table-output.txt').write_text('\n'.join(lines)+'\n')
print('tokens',len(out),'switches',[(t['offset'],t['code'],t['value']) for t in out if t['kind']=='switch'])
print('invalid',[(t['offset'],t['code']) for t in out if t['kind']=='invalid'])
grades={g:sum(t['grade']==g for t in out) for g in 'HM-'}
report['grades']={'H':grades['H'],'M':grades['M'],'not_graded':grades['-'],'note':'H = in the 1752 tables, M = absent or malformed; repairs are I and stay in repair-cases.json'}
(P/'two-table-parsing.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('grades',grades)
