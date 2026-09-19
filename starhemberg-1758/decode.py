"""Auditable two-table parser. Incomplete key; never claims a full decipherment.

The first mark is displaced one digit from the boundary implied by the ordinary
parser. This is a named hypothesis, not a change to the source transcription.
Unrecognized digit groups are retained; no silent digit repair occurs.
"""
import json
from pathlib import Path
import sys
P=Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent))
from cipherkit.grades import Reading, counts
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
grades=counts(Reading(t['code'],t['value'],t['grade'],t['basis']) for t in out)
h_by_source={'tables':sum(t['grade']=='H' and t['kind']=='ordinary' for t in out),
             'instructions_and_marked_codes':sum(t['grade']=='H' and t['kind']!='ordinary' for t in out)}
report['grades']={**grades,'H_by_source':h_by_source,'note':'H = ordinary unit in the 1752 tables, or a null, punctuation mark or table switch defined by the 1752 instructions and marked-code lists (see each token\'s basis); M = absent from the working key or malformed; repairs are I and stay in repair-cases.json'}
(P/'two-table-parsing.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('grades',grades,'H by source',h_by_source)
