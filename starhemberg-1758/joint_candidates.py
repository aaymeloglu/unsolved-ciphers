"""Combine local conjectures and test letter-wide consistency, preserving sources.

No candidate is an authenticated corrected ciphertext. This demonstrates both
compatibility and nonuniqueness; grammatical plausibility is not a proof.
"""
import itertools
import json
from pathlib import Path
from cipher_model import parse_units

P = Path(__file__).resolve().parent
rows = json.loads((P / 'ciphertext-lines.json').read_text())
source = ''.join(c for row in rows for c in row if c.isascii() and c.isdigit())
baseline = json.loads((P / 'two-table-parsing.json').read_text())['tokens']
keys = {t: dict(line.split('\t', 1) for line in (P / f).read_text().splitlines())
        for t, f in [('A', 'working-prima-v4.tsv'), ('B', 'working-secunda.tsv')]}
hypotheses = json.loads((P / 'target-hypotheses.json').read_text())


def distance(a, b):
    row = list(range(len(b) + 1))
    for i, ac in enumerate(a, 1):
        new = [i]
        for j, bc in enumerate(b, 1):
            new.append(min(new[-1] + 1, row[j] + 1, row[j - 1] + (ac != bc)))
        row = new
    return row[-1]


def edit(offset, old, new):
    return {'offset': offset, 'from': old, 'to': new}


results = []
for separators, peace, closing in itertools.product(
        ['delete', 'null8'], ['restore_en', 'delete119'], ['two_digits', 'seven_digits']):
    edits = [dict(e) for e in hypotheses['digit_emendations']]
    if separators == 'null8':
        next(e for e in edits if e['offset'] == 2)['to'] = '8'
    for offset, old in [(443, '7'), (449, '3'), (708, '0'), (793, '333')]:
        edits.append(edit(offset, old, '' if separators == 'delete' else '8' * len(old)))
    if peace == 'restore_en':
        edits += [edit(624, '', '31'), edit(626, '9', '3')]
    else:
        edits.append(edit(624, '119', ''))
    edits.append(edit(1369, '', '31' if closing == 'two_digits' else '3111531'))
    chars = list(source)
    origins = list(range(len(source)))
    previous = len(source) + 1
    for e in sorted(edits, key=lambda x: x['offset'], reverse=True):
        pos, old, new = e['offset'], e['from'], e['to']
        assert source[pos:pos + len(old)] == old, e
        assert pos + len(old) <= previous, 'Overlapping conjectures'
        chars[pos:pos + len(old)] = list(new)
        # Substituted digits retain their original positions; insertions have none.
        origins[pos:pos + len(old)] = ([pos + i for i in range(len(new))]
                                     if len(old) == len(new) else [None] * len(new))
        previous = pos
    proposed = ''.join(chars)
    index = {old: new for new, old in enumerate(origins) if old is not None}
    controls = {index[t['offset']]: (t['code'], 'baseline explicit mark hypothesis')
                for t in baseline if t['kind'] in ('control', 'switch')}
    tokens = parse_units(proposed, controls, keys)
    for t in tokens:
        start = t['offset']
        t['original_digit_positions'] = origins[start:start + len(t['code'])]
        t['baseline_key_value'] = t['value']
        old_start = next((n for n in t['original_digit_positions'] if n is not None), None)
        if old_start in [97, 335, 945, 1608]:
            assert t['code'] == '99'
            t['value'] = '[g?]'
            t['hypothesis'] = 'Selective99→g; not a historical-key correction'
        if (closing == 'two_digits' and t['table'] == 'A' and t['code'] == '31115'
                and 1369 in t['original_digit_positions']):
            t['value'] = '[gege?]'
            t['hypothesis'] = 'Conditional reading of longer key alternative'
    invalid = [t for t in tokens if t['kind'] == 'invalid']
    assert len(invalid) == 1 and invalid[0]['original_digit_positions'] == [1720]
    assert [(t['table'], t['code']) for t in tokens if t['kind'] == 'switch'] == [('A', '876'), ('B', '899')]
    zinner = next(t for t in tokens if t['original_digit_positions'] == [1298, 1299])
    assert zinner['value'] == 'er'
    assert ''.join(t['code'] for t in tokens) == proposed
    results.append({
        'label': f'{separators}; peace={peace}; closing={closing}',
        'digit_edit_cost': sum(distance(e['from'], e['to']) for e in edits),
        'candidate_digit_count': len(proposed), 'edits': sorted(edits, key=lambda x: x['offset']),
        'qualifications': [
            'These are combinations of specified conjectures, not an exhaustive search or minimum-distance proof.',
            'Four selective99→g readings and the initial mark displacement are additional assumptions.',
            'Two-digit closing uses a provisional gege alternative; seven-digit closing does not.',
            'Every nonterminal unit parses, but several resulting words and sentence joins remain unresolved.',
        ],
        'literal_roots': ' / '.join(t['value'] for t in tokens if t['kind'] != 'null'),
        'tokens': tokens,
    })

# Paired deletion/null candidates must preserve every non-null code and state.
for deleted in results[:4]:
    nulled = next(r for r in results if r['label'] == deleted['label'].replace('delete;', 'null8;', 1))
    ordinary = lambda r: [(t['table'], t['code'], t['kind']) for t in r['tokens'] if t['kind'] != 'null']
    assert ordinary(deleted) == ordinary(nulled)

consistency = []
for table, code, selected, alternate, caution in [
    ('A', '31168', [195, 1414], 's via31368', 'The occurrence525 must retain u in vergnüglich; no global key replacement.'),
    ('B', '55', [1061, 1216], 'en via95', 'Both target occurrences support the same repair; historical55 remains hand/handlung.'),
    ('A', '99', [97, 335, 1608], 'g', 'All three Prima target occurrences invite g, but historical99=man.'),
    ('B', '99', [945], 'g', 'Occurrence1298 must retain er for Zinner; global99→g is contradicted.'),
]:
    hits = [t for t in baseline if t['table'] == table and t['code'] == code]
    consistency.append({'table': table, 'code': code,
                        'all_offsets': [t['offset'] for t in hits],
                        'candidate_repair_offsets': selected, 'candidate': alternate,
                        'qualification': caution})

report = {'status': 'Eight internally consistent but unverified competing full-letter reconstructions',
          'source_digit_count': len(source), 'source_unchanged': True,
          'null_hypothesis': 'Replacing presumed surplus digits with null8 gives the same ordinary-code sequence as deleting them. Existing scans show difficult3/8 forms; this does not establish what the missing Starhemberg image contains.',
          'repeated_code_consistency': consistency, 'candidates': results}
(P / 'joint-candidates.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
lines = ['# Joint candidate diagnostics', '',
         'These are unverified reconstructions. A complete valid parse is not a complete solution.', '']
for r in results:
    lines += [f"## {r['label']}", '', f"Digit edits: {r['digit_edit_cost']}; candidate digits: {r['candidate_digit_count']}.", '', r['literal_roots'], '']
(P / 'joint-candidates.md').write_text('\n'.join(lines))
print('PASS:', len(results), 'joint candidates; digit-edit costs', sorted({r['digit_edit_cost'] for r in results}))
print('All conserve their explicit edits, retain both switches and Zinner; terminal3 remains invalid.')
