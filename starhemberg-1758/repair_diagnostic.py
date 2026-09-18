"""Enumerate minimal local transcription repairs, without changing the source.

Only unmarked ordinary-code windows are considered. Endpoints are assumptions:
they must coincide with independently chosen code boundaries. Structural validity
does not establish a reading. Ranking by known entries favors our incomplete key
and is presented only as a browsing aid, never as evidence of correctness.
"""
import json
from pathlib import Path

P = Path(__file__).resolve().parent
rows = json.loads((P / 'ciphertext-lines.json').read_text())
source = ''.join(c for row in rows for c in row if c.isascii() and c.isdigit())
keys = {table: dict(line.split('\t', 1) for line in (P / filename).read_text().splitlines())
        for table, filename in [('A', 'working-prima-v4.tsv'), ('B', 'working-secunda.tsv')]}


def parse(s):
    codes = []
    i = 0
    while i < len(s):
        width = 5 if s[i] == '3' else 1 if s[i] == '8' else 2
        code = s[i:i + width]
        if len(code) != width:
            return None
        if width == 5 and not (code == '30000' or 31000 <= int(code) <= 31500):
            return None
        codes.append(code)
        i += width
    return codes


def edits(s):
    for i in range(len(s)):
        yield s[:i] + s[i + 1:]
        for digit in '0123456789':
            if digit != s[i]:
                yield s[:i] + digit + s[i + 1:]
    for i in range(len(s) + 1):
        for digit in '0123456789':
            yield s[:i] + digit + s[i:]


windows = [('opening', 'A', 2, 8),
           ('invalid vorsichtig unit', 'A', 325, 330),
           ('Spanish court', 'A', 443, 465),
           ('four consecutive threes', 'B', 793, 806)]
report = []
for label, table, start, end in windows:
    raw = source[start:end]
    assert parse(raw) is None, (label, raw)
    seen = {raw}
    frontier = {raw}
    for distance in (1, 2):
        candidates = set()
        next_frontier = set()
        for previous in frontier:
            for changed in edits(previous):
                if changed in seen:
                    continue
                next_frontier.add(changed)
                if parse(changed) is not None:
                    candidates.add(changed)
        if candidates:
            break
        seen.update(next_frontier)
        frontier = next_frontier

    def describe(changed):
        codes = parse(changed)
        unknown = sum(code != '8' and code not in keys[table] for code in codes)
        return {'digits': changed, 'codes': codes, 'unknown_entries': unknown,
                'provisional_roots': [keys[table].get(c, '' if c == '8' else '?') for c in codes]}

    descriptions = sorted((describe(c) for c in candidates),
                          key=lambda x: (x['unknown_entries'], len(x['codes']), x['digits']))
    report.append({'label': label, 'table': table, 'start': start, 'end': end,
                   'source': raw, 'minimum_edits': distance,
                   'structurally_valid_candidates': len(candidates),
                   'candidates': descriptions})
    print(label, raw, 'minimum edits:', distance, 'alternatives:', len(candidates))
    for result in descriptions[:5]:
        print(' ', result['codes'], result['provisional_roots'])

(P / 'repair-diagnostic.json').write_text(json.dumps({
    'status': 'exhaustive minimum Levenshtein-distance structural alternatives up to two edits; no repairs accepted',
    'limitations': 'Fixed window endpoints; unmarked codes only; incomplete key cannot rank linguistic plausibility reliably.',
    'windows': report}, ensure_ascii=False, indent=2) + '\n')
