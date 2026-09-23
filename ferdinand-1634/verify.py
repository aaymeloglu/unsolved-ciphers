#!/usr/bin/env python3
"""Verify the public R1887 edition without private images, models or network access.

Checks source-label amendments, occurrence conservation, literal decoding, complete
apparatus coverage and every editorial character edit. --write regenerates grades.
This tests reproducibility, not the truth of a proposed historical reading.
"""
import argparse
import csv
import io
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from cipherkit.grades import Reading, counts


def segments(path):
    output, current = [], []
    for line in path.read_text().splitlines():
        if not line or line.startswith('%'):
            continue
        if line.startswith('['):
            if current:
                output.append(current)
                current = []
        else:
            current.extend(line.split())
    if current:
        output.append(current)
    return output


def value(token, key):
    if token in key['S']:
        return key['S'][token]
    m = re.fullmatch(r'([bcdfghlmnprstx]?)([aeiou])([bcdfghlmnprstx]?)', token)
    if m and (m[1] or m[3]):
        frame = m[1] + '_' + m[3]
        if frame in key['F']:
            consonant, direction = key['F'][frame]
            return consonant + m[2] if direction == 0 else m[2] + consonant
    return None


def load_and_check():
    baseline = segments(HERE / 'transcription-pass2.txt')
    elected = segments(HERE / 'transcription.txt')
    key = json.loads((HERE / 'key.json').read_text())
    obs = json.loads((HERE / 'observations.json').read_text())
    rows = list(csv.DictReader((HERE / 'alignment.tsv').open(), delimiter='\t'))
    expected = []
    for seg, tokens in enumerate(baseline):
        for index, token in enumerate(tokens):
            ident = f's{seg}t{index:03d}'
            correction = obs['corrections'].get(ident, {})
            uncertainty = obs['uncertainties'].get(ident, {})
            expected.append((ident, seg, index, token, correction.get('token', token),
                             'replace' if correction else 'retain',
                             correction.get('certainty', 'uncertain' if uncertainty else 'not_individually_graded'),
                             correction.get('alternatives', uncertainty.get('alternatives', [])),
                             correction.get('reason', uncertainty.get('reason', ''))))
            if ident in obs['insertions']:
                r = obs['insertions'][ident]
                expected.append((r['id'], seg, index, '', r['token'], 'insert', r['certainty'], r['alternatives'], r['reason']))
    assert len(rows) == len(expected) == 474
    assert len({r['id'] for r in rows}) == 474
    fields = ['id','segment','baseline_index','baseline','token','action','certainty','alternatives','observation']
    for row, wanted in zip(rows, expected):
        actual = tuple(int(row[f]) if f in {'segment','baseline_index'} else json.loads(row[f]) if f == 'alternatives' else row[f] for f in fields)
        assert actual == wanted, f'Source amendment mismatch: {row["id"]}'
        decoded = value(row['token'], key)
        assert row['literal'] == ('?' if decoded is None else decoded), f'Decoder mismatch: {row["id"]}'
    for seg in range(4):
        assert elected[seg] == [r['token'] for r in rows if int(r['segment']) == seg]
    assert len(baseline) == len(elected) == 4
    assert sum(map(len, baseline)) == 472
    assert sum(r['action'] == 'insert' for r in rows) == 2
    assert sum(r['action'] == 'replace' for r in rows) == 8
    assert sum(r['literal'] == '?' for r in rows) == 13
    assert sum(r['literal'] == '' for r in rows) == 7
    by_id = {r['id']: r for r in rows}
    for new in obs['conditional_assignments']:
        assert new not in key['S'], f'Conjectural value installed in key: {new}'
    assert by_id['s1t198']['token'] == '10' and by_id['s1t199']['token'] == '8'
    assert by_id['s1t106']['token'] == 'tin'
    assert by_id['s2t044a']['token'] == 'p?' and by_id['s2t044a']['literal'] == '?'
    assert ''.join(by_id[t]['literal'] for t in ['s1t203','s1t204','s1t205','s1t205a','s1t206','s1t207','s1t208']) == 'tendishisce'

    # Verify the complete physical line alignment independently of stored labels.
    line_counts = [2,15,11,2]
    groups = []
    for seg, amount in enumerate(line_counts):
        for line in range(amount):
            if seg == 0:
                label, images = f'P1.C{line+1:02d}', [f'L1-{line+2:02d}.png']
            elif seg == 1 and line < 6:
                label, images = f'P1.C{line+3:02d}', [f'L1-{line+16:02d}.png']
            elif seg == 1:
                label, images = f'P2.C{line-5:02d}', [f'L2-{line-6:02d}{s}.png' for s in 'ab']
            elif seg == 2:
                label, images = f'P2.C{line+10:02d}', [f'L2-{line+10:02d}{s}.png' for s in 'ab']
            else:
                label, images = f'P3.C{line+1:02d}', ['p3-cip.png']
            rr = [r for r in rows if r['physical_line'] == label]
            assert rr and all(int(r['segment']) == seg and json.loads(r['images']) == images for r in rr)
            groups.extend(r['id'] for r in rr)
    assert groups == [r['id'] for r in rows]

    literal = []
    for seg in range(4):
        rr = [r for r in rows if int(r['segment']) == seg]
        literal.extend([f'[passage {seg}; unknown = ?; assigned empty = ∅ in unit line]',
                        ''.join(r['literal'] for r in rr),
                        ' · '.join(r['literal'] or '∅' for r in rr), ''])
    assert (HERE / 'literal.txt').read_text() == '\n'.join(literal)
    apparatus = json.loads((HERE / 'apparatus.json').read_text())
    coverage = []
    for a in apparatus:
        rr = [by_id[i] for i in a['token_ids']]
        assert a['first'] == rr[0]['id'] and a['last'] == rr[-1]['id']
        assert all(int(r['segment']) == a['segment'] for r in rr)
        raw = ''.join(r['literal'] for r in rr)
        assert a['literal'] == raw
        coverage.extend(a['token_ids'])
        if a['proposed'] is None:
            assert a['edits'] == []
        else:
            result = raw
            for e in reversed(a['edits']):
                lo, hi = e['raw_start'], e['raw_end']
                assert raw[lo:hi] == e['before']
                result = result[:lo] + e['after'] + result[hi:]
            assert result == re.sub('[^a-z]', '', a['proposed'].lower())
    assert len(apparatus) == 38 and coverage == [r['id'] for r in rows]
    assert ''.join(r['literal'] for r in rows if r['id'] in {f's3t{j:03d}' for j in range(17)}) == 'promouerehauddedignetur'
    return rows, apparatus


def grade_files(rows, apparatus):
    output = io.StringIO()
    writer = csv.writer(output, delimiter='\t', lineterminator='\n')
    writer.writerow(['id','cipher','literal','grade','basis'])
    readings = []
    for r in rows:
        direct = int(r['segment']) == 3 and int(r['baseline_index']) < 17
        grade = 'C' if direct else 'M'
        basis = ('Directly matched to the following cleartext promovere haud dedignetur' if direct
                 else 'Contextual reconstruction or unresolved sign; source alternatives in alignment.tsv; no S claim')
        readings.append(Reading(r['token'], r['literal'], grade, basis))
        writer.writerow([r['id'],r['token'],r['literal'],grade,basis])
    summary = {'literal_unit_grades':counts(readings), 'tokens':len(rows),
               'unknown':sum(r['literal'] == '?' for r in rows),
               'assigned_empty':sum(r['literal'] == '' for r in rows),
               'editorial_grading':'Literal unit grades are separate from proposed text. Non-orthographic changed/supplied letters in emendation or conjecture spans are I; none is installed in the key.',
               'editorial_I_spans':[a['id'] for a in apparatus if a['status'] in {'emendation','conjecture'}]}
    reading = ['# Reading and apparatus', '',
        'This is a partial decipherment. Literal strings are mechanical output from the elected source labels and published proposed key. Source alternatives remain in alignment.tsv. An assigned value is not a correctness grade.', '',
        '**Conjectures are displayed in brackets.** Emendations explicitly change the deciphered letters. Unresolved strings are retained. Terminal signs are not silently removed.', '']
    for seg in range(4):
        reading += [f'## Passage {seg+1}', '']
        for a in [a for a in apparatus if a['segment'] == seg]:
            text = a['proposed'] or a['literal'] or '[assigned-empty terminal signs]'
            if a['status'] == 'conjecture':
                text = '[' + text + '?]'
            reading += [f"**{a['id']} · {a['first']}–{a['last']} · {a['status']}**", '',
                        f"Literal: `{a['literal'] or '∅'}`  ", f'Reading: {text}', '']
            if a['note']:
                reading += [a['note'], '']
            if a['edits']:
                reading += ['Letter changes (zero-based offsets in literal string): ' + '; '.join(
                    f"{e['raw_start']}:{e['raw_end']} `{e['before'] or '∅'}` → `{e['after'] or '∅'}`" for e in a['edits']) + '.', '']
    return {'token-grades.tsv':output.getvalue(), 'grades.json':json.dumps(summary,indent=2)+'\n',
            'READING.md':'\n'.join(reading)+'\n'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    rows, apparatus = load_and_check()
    for name, content in grade_files(rows, apparatus).items():
        target = HERE / name
        if args.write:
            target.write_text(content)
        else:
            assert target.read_text() == content, f'Stale grades: {name}'
    print('PASS R1887: 474 groups, 30 physical cipher lines, 38 complete spans; source amendments, literal output, editorial edits and conjecture isolation verified.')
    print('Literal grades: 17 C, 457 M. Editorial emendations/conjectures are separately marked I; no H or S claim.')


if __name__ == '__main__':
    main()
