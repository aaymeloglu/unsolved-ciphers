"""Reproduce manuscript collation and explicitly emended reading.

No source files are rewritten. A complete parse is not proof of every reading.
Run with Python's standard library from any directory.
"""
import hashlib
import csv
from collections import Counter
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GENERATED = ['emendations.json', 'manuscript-tokens.json', 'manuscript-roots.txt',
             'emended-tokens.json', 'emended-roots.txt', 'alignment.tsv', 'verification.json']
checking = '--check' in sys.argv
committed = {name: (HERE / name).read_bytes() for name in GENERATED} if checking else {}
OLD = HERE.parent
sys.path.insert(0, str(OLD))
from cipher_model import parse_units


def read(name):
    return json.loads((HERE / name).read_text())


def write(name, obj):
    (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


old_rows = json.loads((OLD / 'ciphertext-lines.json').read_text())
original = ''.join(c for r in old_rows for c in r if c.isascii() and c.isdigit())
rows = read('manuscript-lines.json')
manuscript = ''.join(c for r in rows for c in r['transcription'] if c.isascii() and c.isdigit())
collation = read('collation.json')
observed = [{'offset': e['old_offset'], 'from': '', 'to': e['insert'],
             'status': 'observed margin digits', 'line': e['line']}
            for e in collation['observed_insertions']]
baseline = json.loads((OLD / 'two-table-parsing.json').read_text())['tokens']
keys = {t: dict(l.split('\t', 1) for l in (OLD / f).read_text().splitlines())
        for t, f in [('A', 'working-prima-v4.tsv'), ('B', 'working-secunda.tsv')]}
keys['A'].update({'31221': 'es'})
keys['B'].update({'50': 'die', '31133': 'l/ll'})

# These are proposed enciphering-error corrections, NOT new photograph readings.
emendations = [
    (115, '31211', '31221', 'es in daß es deroselben; manuscript appears31211'),
    (195, '31168', '31368', 's in Statssecretario; keep31168=u in vergnüglich'),
    (325, '30073', '31073', 'sich in vorsichtig; photographed30073 is malformed'),
    (443, '7', '', 'surplus digit before31197=bi(s)'),
    (449, '3', '', 'surplus digit before31394=zu'),
    (624, '119', '', 'damaged recto/verso join; adjective ending editorial'),
    (1046, '31329', '31326', 'd after un'),
    (1061, '55', '95', 'en in entschließen'),
    (1139, '31389', '31399', 'Engelland before Prussia; adjective expanded'),
    (1216, '55', '95', 'en in setzen, same error as1061'),
    (1414, '31168', '31368', 's in beseres'),
]
emendations = [dict(offset=o, **{'from': a, 'to': b}, reason=r,
                    status='conjectural manuscript emendation')
              for o, a, b, r in emendations]
write('emendations.json', {'offsets': 'zero-based positions in old1721-digit stream',
                         'edits': emendations,
                         'additional_assumptions': [
                             'Unmarked883 at both boundaries is treated as framing.',
                             'Initial854 punctuation is aligned by code boundary; its mark is displaced.',
                             'Four contextual99→g values are separately labelled; no global99 override.',
                             'Code choices and grammatical expansions are distinct from digit repairs.',
                             'Deleting119 is one of two prior three-edit peace-join reconstructions.']})


def transform(edits):
    chars = list(original)
    origins = list(range(len(original)))
    last = len(original) + 1
    for e in sorted(edits, key=lambda e: e['offset'], reverse=True):
        o, a, b = e['offset'], e['from'], e['to']
        assert original[o:o+len(a)] == a
        assert o + len(a) <= last
        chars[o:o+len(a)] = list(b)
        origins[o:o+len(a)] = list(range(o, o+len(a))) if len(a) == len(b) else [None]*len(b)
        last = o
    return ''.join(chars), origins


source_digits, source_origins = transform(observed)
assert source_digits == manuscript, 'Photograph transcription must equal explicit collation'
assert len(manuscript) == 1726
source_locations = []
for row in rows:
    width = sum(c.isascii() and c.isdigit() for c in row['transcription'])
    source_locations.extend((row['line'], i+1) for i in range(width))
old_to_source = {old: pos for pos, old in enumerate(source_origins) if old is not None}
outputs = {}
for label, edits in [('manuscript', observed), ('emended', observed + emendations)]:
    digits, origins = transform(edits)
    inserted_source_positions = iter(i for i, o in enumerate(source_origins) if o is None)
    source_positions = [old_to_source[o] if o is not None else next(inserted_source_positions)
                        for o in origins]
    locations = [source_locations[o] for o in source_positions]
    index = {old: new for new, old in enumerate(origins) if old is not None}
    controls = {index[t['offset']]: (t['code'], 'observed mark, interpreted boundary')
                for t in baseline if t['kind'] in ('control', 'switch')}
    assert digits.startswith('883') and digits.endswith('883')
    controls[0] = ('883', 'hypothesized opening frame')
    controls[len(digits)-3] = ('883', 'hypothesized closing frame')
    tokens = parse_units(digits, controls, keys, locations)
    for t in tokens:
        start = t['offset']
        old_positions = [o for o in origins[start:start+len(t['code'])] if o is not None]
        t['old_positions'] = old_positions
        t['manuscript_digit_positions'] = source_positions[start:start+len(t['code'])]
        old_start = old_positions[0] if old_positions else None
        t['baseline_root'] = t['value']
        if start in (0, len(digits)-3):
            t['kind'] = 'framing_hypothesis'
            t['value'] = '[cipher begins]' if start == 0 else '[cipher ends]'
        if old_start == 719:
            assert t['code'] == '31183'
            t['value'] = 'Farinelli'
            t['reading_basis'] = 'explicit proper-name alternative in alphabetical and numerical keys'
        if old_start in (725, 796, 1369):
            # Source-written longer ge-variant; following n yields gegen.
            assert t['code'] in ('31010', '31126', '31115'), t
            t['value'] = 'gege'
            t['reading_basis'] = 'longer ge-variant, checked against alphabetical/numerical copies'
        if label == 'emended' and old_start in (97, 335, 945, 1608):
            assert t['code'] == '99'
            t['value'] = '[g]'
            t['reading_basis'] = 'contextual emendation; not a universal historical99 mapping'
        # Grade the selected output, rather than inheriting the parser's lookup grade.
        # A choice between clear historical alternatives remains H; uncertain letters are M.
        if '?' in t['value'] or old_start in (725, 796, 1369) or (t['table'], t['code']) in [('B', '31405'), ('A', '31427')]:
            t['grade'], t['basis'] = 'M', t.get('reading_basis', 'uncertain handwriting or selected reading; see key-evidence.json')
        if t['kind'] == 'framing_hypothesis' or old_start == 109:
            t['grade'], t['basis'] = 'I', 'assumed framing or displaced punctuation boundary; see emendations.json'
        if label == 'emended':
            affected = [e for e in emendations if
                        set(old_positions).intersection(range(e['offset'], e['offset'] + len(e['from']))) or
                        (not e['to'] and old_start == e['offset'] + len(e['from']))]
            if affected or old_start in (97, 335, 945, 1608):
                t['grade'], t['basis'] = 'I', t.get('reading_basis', 'proposed digit repair or token boundary after deletion; see emendations.json')
        if t['grade'] == 'H' and t.get('reading_basis'):
            t['basis'] += '; ' + t['reading_basis']
    assert ''.join(t['code'] for t in tokens) == digits
    assert [(t['table'], t['code']) for t in tokens if t['kind'] == 'switch'] == [('A','876'),('B','899')]
    outputs[label] = dict(digit_count=len(digits), token_count=len(tokens),
                          grade_counts=dict(sorted(Counter(t['grade'] for t in tokens).items())),
                          invalid=[t for t in tokens if t['kind']=='invalid'],
                          tokens=tokens)
    write(label+'-tokens.json', outputs[label])
    (HERE/(label+'-roots.txt')).write_text(' / '.join(t['value'] for t in tokens if t['kind']!='null')+'\n')

assert not outputs['emended']['invalid']
assert next(t for t in outputs['emended']['tokens'] if t['old_positions']==[1298,1299])['value']=='er'
with (HERE / 'alignment.tsv').open('w', newline='') as f:
    writer = csv.writer(f, delimiter='\t', lineterminator='\n')
    writer.writerow(['table', 'code', 'root', 'start_line', 'start_digit', 'end_line', 'end_digit', 'grade', 'qualification'])
    for t in outputs['emended']['tokens']:
        writer.writerow([t['table'], t['code'], t['value'], *t['source_start'], *t['source_end'], t['grade'], t['basis']])
write('verification.json', {
    'source_sha256': hashlib.sha256(manuscript.encode()).hexdigest(),
    'old_digits': len(original), 'observed_new_digits': 5,
    'manuscript_digits': len(manuscript),
    'manuscript_tokens': outputs['manuscript']['token_count'],
    'grade_counts': {label: out['grade_counts'] for label, out in outputs.items()},
    'manuscript_invalid_groups': [(t['offset'],t['code']) for t in outputs['manuscript']['invalid']],
    'emended_digits': outputs['emended']['digit_count'],
    'emended_invalid_groups': len(outputs['emended']['invalid']),
    'conjectural_edit_sites': len(emendations),
    'specified_digit_edit_cost': sum(len(e['from']) if not e['to'] else
                                    sum(a != b for a,b in zip(e['from'],e['to']))
                                    for e in emendations),
    'switches': ['A876→B', 'B899→A'],
    'qualification': 'Mechanical consistency and digit accounting; not independent authentication of conjectures.'})
print((HERE/'verification.json').read_text())
if checking:
    stale = [name for name in GENERATED if (HERE / name).read_bytes() != committed[name]]
    for name, data in committed.items():
        (HERE / name).write_bytes(data)
    if stale:
        raise SystemExit('Stale edition artifacts: ' + ', '.join(stale))
