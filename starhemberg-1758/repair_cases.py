"""Render explicit local conjectures without rewriting the published ciphertext.

Every edit uses ORIGINAL zero-based offsets. Exact proposed code sequences are
checked, but a passing check does not authenticate a conjectural restoration.
"""
import json
from pathlib import Path
from cipher_model import parse_units

P = Path(__file__).resolve().parent
source = ''.join(c for row in json.loads((P / 'ciphertext-lines.json').read_text())
                 for c in row if c.isascii() and c.isdigit())
keys = {table: dict(line.split('\t', 1) for line in (P / filename).read_text().splitlines())
        for table, filename in [('A', 'working-prima-v4.tsv'), ('B', 'working-secunda.tsv')]}
hypotheses = json.loads((P / 'target-hypotheses.json').read_text())
edits_by_offset = {e['offset']: e for e in hypotheses['digit_emendations'] + hypotheses['longer_conjectures']}

cases = [
    dict(label='und wohl leicht entschließen wird', table='B', start=1044, end=1078,
         offsets=[1046, 1061], codes='54 31326 31091 31304 95 31238 31201 31456',
         qualification='Two substitutions. Inflected schließen is a key alternative/editorial expansion; future tense is directly wird.'),
    dict(label='English and Prussian courts', table='B', start=1134, end=1166,
         offsets=[1139], codes='31210 31399 31157 31167 31397 31272 41',
         qualification='One substitution, plus editorial adjectival endings; singular Hof is retained.'),
    dict(label='Verlegenheit setzen würde', table='B', start=1181, end=1220,
         offsets=[1216], codes='31342 31330 31151 31033 31246 31282 31475 95 09',
         qualification='One substitution; Verlegenheit itself needs no digit edit. Ge/gen is an abbreviated key reading.'),
    dict(label='entgegensehe', table='A', start=1362, end=1384,
         offsets=[1369], codes='31113 62 31115 31115 95 31154 31247',
         qualification='Seven inserted digits, with final e editorial. Substantially weaker evidence than the one-digit repairs; not unique.'),
    dict(label='entgegensehe, shorter variant-dependent alternative', table='A', start=1362, end=1384,
         edits=[dict(offset=1369, **{'from':'', 'to':'31'})],
         codes='31113 62 31115 95 31154 31247',
         conditional_key_readings={'31115': 'gege'},
         qualification='Only two inserted digits IF the secondary 31115 reading is gege. Both numerical copies and the alphabetical G entry show a longer alternative; its precise ending remains provisional. Final e editorial. Do not combine this insertion with the seven-digit alternative.'),
    dict(label='opening extra 3', table='A', start=2, end=18,
         offsets=[2], codes='31159 31217 31214',
         qualification='Restores valid so/stat/lich segmentation, but the adjective remains unresolved; NOT proof of stattlich or tröstlich.'),
    dict(label='court, two deletions', table='A', start=443, end=465,
         edits=[dict(offset=443, **{'from':'7', 'to':''}), dict(offset=449, **{'from':'3', 'to':''})],
         codes='31197 31394 31380 31216',
         qualification='Bi/zu/solch/resolution is mechanically possible. Bis zu is a conjecture, not an accepted repair.'),
    dict(label='four threes, three deletions', table='B', start=793, end=806,
         edits=[dict(offset=793, **{'from':'333', 'to':''})], codes='31126 31272',
         qualification='Gives gn/gen+n, but leaves preceding wa and the full syntax unresolved. Not accepted.'),
    dict(label='after zumahl, extra zero', table='B', start=706, end=719,
         edits=[dict(offset=708, **{'from':'0', 'to':''})], codes='53 31400 31460',
         qualification='Gives mahl/von/den but does not resolve following no/ge/n and the sentence. B53 source correction supersedes meist. Not accepted.'),
    dict(label='peace join, restore en before honorablen', table='A', start=624, end=657,
         edits=[dict(offset=624, **{'from':'', 'to':'31'}), dict(offset=626, **{'from':'9', 'to':'3'})],
         codes='31113 31328 8 95 31346 31000 31169 95 31004',
         qualification='Three digit edits: insert31 and substitute9→3. Gives en/ho/n/or/ab/le/n/fried after lich. Frieden itself is now source-supported; the join repair is unverified and nonunique.'),
    dict(label='peace join, remove three digits', table='A', start=624, end=657,
         edits=[dict(offset=624, **{'from':'119', 'to':''})],
         codes='31328 8 95 31346 31000 31169 95 31004',
         qualification='Competing three-edit hypothesis, deleting119 and expanding prior lich inflection editorially. Same honorablenFrieden sequence, different treatment of the join. Do not combine alternatives.'),
]

results = []
for case in cases:
    start, end = case['start'], case['end']
    proposed = case.get('edits', [edits_by_offset[o] for o in case.get('offsets', [])])
    text = source[start:end]
    previous = end + 1
    for edit in sorted(proposed, key=lambda e: e['offset'], reverse=True):
        pos = edit['offset']
        old, new = edit['from'], edit['to']
        assert start <= pos <= end and pos + len(old) <= end
        assert pos + len(old) <= previous, 'Overlapping edits'
        assert source[pos:pos + len(old)] == old
        rel = pos - start
        text = text[:rel] + new + text[rel + len(old):]
        previous = pos
    tokens = parse_units(text, {}, keys, initial_table=case['table'])
    assert [t['code'] for t in tokens] == case['codes'].split(), case['label']
    assert not any(t['kind'] == 'invalid' for t in tokens)
    results.append({**case, 'edits': proposed, 'source_digits': source[start:end],
                    'proposed_digits': text,
                    'literal_roots': ' / '.join(t['value'] for t in tokens),
                    'status': 'CONJECTURE: segmentation checked, original not inspected'})
    if case.get('conditional_key_readings'):
        results[-1]['conditional_roots'] = ' / '.join(
            case['conditional_key_readings'].get(t['code'], t['value']) for t in tokens)
    print(case['label'], '=>', results[-1]['literal_roots'])

(P / 'repair-cases.json').write_text(json.dumps({
    'status': 'Explicit alternatives, never an authenticated corrected ciphertext',
    'source_unchanged': True, 'cases': results}, ensure_ascii=False, indent=2) + '\n')
