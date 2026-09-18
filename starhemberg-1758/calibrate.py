"""Check the shared parser against a separately transcribed historical example.

The interlinear roots are independent evidence, not a new inferred target key.
Agreement in segmentation is distinct from agreement in key transcription.
"""
import json
from pathlib import Path
from cipher_model import parse_units

P = Path(__file__).resolve().parent
example = json.loads((P / 'historical-control.json').read_text())
digits = ''.join(c for c in example['raw_transcription'] if c.isdigit())
controls = {int(k): tuple(v) for k, v in example['marked_controls'].items()}
keys = {table: dict(line.split('\t', 1) for line in (P / filename).read_text().splitlines())
        for table, filename in [('A', 'working-prima-v4.tsv'), ('B', 'working-secunda.tsv')]}
tokens = parse_units(digits, controls, keys)
assert [t['code'] for t in tokens] == example['expected_units']
assert not [t for t in tokens if t['kind'] == 'invalid']
assert [t['code'] for t in tokens if t['kind'] == 'switch'] == ['818']
comparisons = []
for t in tokens:
    if t['kind'] != 'ordinary':
        continue
    expected = example['interlinear_readings'][t['table']][t['code']]
    comparisons.append({'table': t['table'], 'code': t['code'],
                        'interlinear': expected, 'working_key': t['value'],
                        'in_working_key': t['code'] in keys[t['table']]})
report = {'status': 'Exact historical code-boundary and table-switch agreement',
          'digits': len(digits), 'units': len(tokens),
          'ordinary_occurrences': len(comparisons),
          'shared_working_key_occurrences': sum(c['in_working_key'] for c in comparisons),
          'comparison': comparisons,
          'limitations': 'Root comparison is for human review, not an automatic paleographic accuracy score; inflections and some control-only entries differ.'}
(P / 'historical-calibration.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(f"PASS: {len(digits)} historical digits, {len(tokens)} units, exact boundaries and switch818.")
print(f"{len(comparisons)} ordinary occurrences; {report['shared_working_key_occurrences']} overlap working key.")
for c in comparisons:
    if not c['in_working_key']:
        print('Control-only entry:', c['table'], c['code'], c['interlinear'])
