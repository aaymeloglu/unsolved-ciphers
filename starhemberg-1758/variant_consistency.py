"""Check a source-written syllable's alternatives across separated target words."""
import json
from pathlib import Path

P = Path(__file__).resolve().parent
tokens = [t for t in json.loads((P / 'two-table-parsing.json').read_text())['tokens']
          if t['kind'] != 'null']
audit = json.loads((P / 'target-wide-key-audit.json').read_text())
forms = {(e['table'], e['code']): e.get('interpreted_forms', []) for e in audit['entries']}
results = []
for word, codes, selected, expected_hits in [
    ('nunmehro', ['31078', '31210', '31116', '31428'], ['nun', 'me', 'h', 'ro'], 1),
    ('immer', ['31170', '31210'], ['im', 'mer'], 2),
    ('benehmen', ['31060', '31247', '31210'], ['ben', 'eh', 'men'], 1),
]:
    assert ''.join(selected) == word
    hits = []
    for i in range(len(tokens) - len(codes) + 1):
        seq = tokens[i:i + len(codes)]
        if all(t['table'] == 'A' for t in seq) and [t['code'] for t in seq] == codes:
            for t, value in zip(seq, selected):
                if t['code'] == '31210':
                    assert value in forms[('A', '31210')]
                else:
                    assert value == t['value']
            hits.append({'start': seq[0]['offset'], 'end': seq[-1]['offset'] + len(seq[-1]['code']),
                         'codes': codes, 'selected_roots': selected})
    assert len(hits) == expected_hits, (word, len(hits))
    results.append({'word': word, 'hits': hits})
(P / 'variant-consistency.json').write_text(json.dumps({
    'status': 'Unchanged-digit cross-context check of A31210 me/mer/men',
    'source': 'R1695P7 alphabetical M plus R1698P1 numerical31210; interpreted forms recorded in target-wide-key-audit.json',
    'limitation': 'This checks an explicitly read key alternative; not a global plaintext accuracy score.',
    'words': results}, ensure_ascii=False, indent=2) + '\n')
print('PASS: A31210 alternatives give nunmehro, two immer occurrences, and Benehmen; no digit edits.')
