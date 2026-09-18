"""Verify source conservation, control states, and unchanged-digit fragments.

These checks establish alignment and reproducibility, not paleographic accuracy
of every provisional key entry or correctness of editorial inflection choices.
Run decode.py first. No ciphertext repair is applied by this script.
"""
import json
from pathlib import Path

P = Path(__file__).resolve().parent
rows = json.loads((P / 'ciphertext-lines.json').read_text())
source = ''.join(c for row in rows for c in row if c.isascii() and c.isdigit())
tokens = json.loads((P / 'two-table-parsing.json').read_text())['tokens']
assert len(source) == 1721
assert ''.join(t['code'] for t in tokens) == source
for token in tokens:
    start = token['offset']
    assert source[start:start + len(token['code'])] == token['code']
assert [(t['offset'], t['code']) for t in tokens if t['kind'] == 'switch'] == [
    (662, '876'), (1349, '899')]
period = next(t for t in tokens if t['offset'] == 1220)
assert (period['table'], period['code'], period['value']) == ('B', '897', '.')

fragments = [
    ('giebt mir zumahl', 'B', '31384 31042 31238 31325 31466 53'),
    ('annoch gelingen werde', 'A', '31005 31019 31033 31334 31223 31113 31181'),
    ('more favorable form of the war', 'A', '31293 31036 31318 31184 31372 31168 31350 31121 31490 69 01 31106 31208 31228 31115 31075 31359 62 31041 31333'),
    ('honorable peace', 'A', '95 31346 31000 31169 95 31004 31184'),
    ('memoir', 'A', '31149 31438 66 31364 31121 31115 31158 31348 31122 31084 31433 31443 31033 31271 31079 31315 62 69 31287'),
    ('Minorca / Spain', 'B', '31031 31183 31334 31278 44 31345 31208 31361 09'),
    ('consistent statement', 'B', '31218 31299 31286 31006 31334 31031 31126 31075 31225 31291'),
    ('French ambassador and contemporary statements', 'B', '31182 74 31238 31162 31300 31264 31377 31448 31218 31299 02 31014 31010 31403 63 31218 31299 31286 31006 31334 31031 31126 31075 31225 31291'),
    ('Verlegenheit', 'B', '31342 31330 31151 31033'),
    ('courier Zinner', 'B', '31455 14 31307 99'),
    ('reports to be sent', 'B', '31448 31320 31090 31300 31210 31070 94 31457 31222 31342'),
    ('course / Wall', 'A', '31325 31062 62 31154 31112 31115 31271 31127 31342 31058 31391 31406 31314 90 31257 31394 31158 31116 31085 30000 31047 31466 31136'),
    ('confidential disclosures', 'A', '31184 31500 31058 31326 31451 31462 31089 31184 31263'),
]
ordinary = [t for t in tokens if t['kind'] != 'null']
alignments = []
for label, table, codes in fragments:
    wanted = codes.split()
    hits = []
    for i in range(len(ordinary) - len(wanted) + 1):
        segment = ordinary[i:i + len(wanted)]
        if all(t['table'] == table for t in segment) and [t['code'] for t in segment] == wanted:
            hits.append(segment)
    assert len(hits) == 1, (label, len(hits))
    segment = hits[0]
    alignments.append({'label': label, 'table': table,
                       'start': segment[0]['offset'],
                       'end': segment[-1]['offset'] + len(segment[-1]['code']),
                       'literal_roots': ' / '.join(t['value'] for t in segment),
                       'tokens': segment})

# Historical interlinear example, independently read from R1697 P2.
secunda = dict(line.split('\t', 1) for line in
               (P / 'working-secunda.tsv').read_text().splitlines())
control = ['31218', '65', '30000', '31275']
assert ''.join(secunda[c] for c in control) == 'gleichen'

(P / 'fragment-alignments.json').write_text(json.dumps({
    'status': 'alignment checks passed; provisional key accuracy not certified',
    'source_digits': len(source), 'tokens': len(tokens),
    'historical_control': {'codes': control, 'reading': 'gleichen'},
    'fragments': alignments}, ensure_ascii=False, indent=2) + '\n')
print('PASS: 1721 digits conserved; switches and period checked;')
print(f'{len(fragments)} unchanged-digit target alignments and historical gleichen control.')
