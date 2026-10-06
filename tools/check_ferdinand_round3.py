"""Replay Ferdinand diagnostics against separately stored, TRUSTED local research.

Usage: python tools/check_ferdinand_round3.py RESEARCH --training-text NORMALIZED --output REPORT

NORMALIZED must be the exact normalized training text used in round 3. The
research directory supplies saved JSON results and local Python model pickles;
only use trusted files (pickle can execute code). No data is fetched or modified.
No source images or research data are required by the public CI tests.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import json
import math
from pathlib import Path
import pickle
import random
import sys
import unicodedata

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cipherkit import InterpolatedCharLM, literal_crib_scan, transformation_report
from cipherkit.diagnostics import perturbation_report

ALPHABET = 'abcdefghilmnopqrstuxz'


def read_tokens(path):
    return [t for line in path.read_text().splitlines() if not line.startswith('%')
            for t in line.split()]


def fold_crib(text):
    text = unicodedata.normalize('NFD', text.lower()).translate(str.maketrans('jvy', 'iui'))
    return ''.join(c for c in text if 'a' <= c <= 'z')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('research', type=Path)
    parser.add_argument('--training-text', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    root = args.research.resolve()
    output = args.output.resolve()
    if output == root or root in output.parents or output == args.training_text.resolve():
        parser.error('output must be outside the research inputs')
    r3 = root / 'solve/round3'
    pinned = json.loads((r3 / 'manifest.json').read_text())['files']
    inputs = ['transcription/pass1.txt', 'transcription/f121-122v.txt',
              'solve/round3/f121r-audited.txt', 'solve/hsolve_model.pkl',
              'solve/round3/backoff-model.pkl']
    for name in inputs:
        assert hashlib.sha256((root / name).read_bytes()).hexdigest() == pinned[name], name
    old, backoff = [pickle.loads((root / name).read_bytes()) for name in inputs[-2:]]
    training = args.training_text.read_text()
    model = InterpolatedCharLM.from_text(training, alphabet=ALPHABET)
    quads = [model.logp(''.join(g)) for g in itertools.product(ALPHABET, repeat=4)]
    error = max(abs(a - b) for a, b in zip(quads, backoff[0]))
    assert len(quads) == len(backoff[0]) and error < 1e-12, 'training/model mismatch'
    assert max(abs(model.logp(c) - p) for c, p in zip(ALPHABET, backoff[1])) < 1e-12
    report = dict(training_sha256=model.training_sha256, conditional_table_max_error=error)

    # Audit the saved relabellings; no manuscript interpretation is implied.
    audit = json.loads((root / 'solve/round2/normalization-audit.json').read_text())
    source = [t for name in inputs[:2] for t in read_tokens(root / name) if t != '[gap]']
    replacements = {c['raw']: c['old'] for c in audit['changes']}
    assert len(replacements) == len(audit['changes'])
    changed = [replacements.get(t, t) for t in source]
    ledger = transformation_report(source, changed)
    assert ledger['changed_positions'] == audit['changed_tokens'] == 537
    assert ledger['positions'] == audit['total_tokens'] == 3136
    report['transformation'] = {k: ledger[k] for k in ['positions', 'changed_positions', 'source_types', 'transformed_types']}

    expected = json.loads((root / 'documentary/followthrough/literal-crib-results.json').read_text())
    report['cribs'] = {}
    for name, doc in expected['documents'].items():
        units = [None if t in ('[gap]', 'Blot') else t for t in read_tokens(root / doc['source'])]
        report['cribs'][name] = {}
        for label, crib in expected['cribs'].items():
            scan = literal_crib_scan(units, fold_crib(crib))
            previous = doc['results'][label]
            assert scan['exact_offsets'] == previous['exact_placements']
            assert len(scan['windows']) == previous['windows']
            best = sorted(scan['windows'], key=lambda w: (w['conflicting_pairs'], w['offset']))[:5]
            assert [(w['offset'], w['conflicting_pairs']) for w in best] == [
                (w['offset0'], w['conflicting_equal_pairs']) for w in previous['best']]
            report['cribs'][name][label] = dict(windows=len(scan['windows']),
                exact=len(scan['exact_offsets']), minimum_conflicting_pairs=best[0]['conflicting_pairs'])

    control = json.loads((r3 / 'control.json').read_text())
    lengths = control['segments']; n = sum(lengths)
    assert old[2] == backoff[2]
    held = old[2]; start = held.index('copia dires a los uenecianos') + len('copia ')
    plain = ''.join(c for c in held[start:] if c in ALPHABET)[:n]
    rng = random.Random(1849)
    tokens = [f'{c}{rng.randrange(3)}' for c in plain]
    truth = {t: t[0] for t in tokens}
    index = {c: i for i, c in enumerate(ALPHABET)}; A = len(ALPHABET)
    report['models'] = {}
    for name, table, uni, filename in [
        ('original', old[0], old[1], 'control.json'),
        ('interpolated', quads, [model.logp(c) for c in ALPHABET], 'backoff-control.json'),
    ]:
        def score(key):
            values = [index[key[t]] for t in tokens]
            total = 0.; off = 0
            for size in lengths:
                for j in range(off + 3, off + size):
                    a, b, c, d = values[j-3:j+1]
                    total += table[((a*A+b)*A+c)*A+d]
                off += size
            freq = Counter(values)
            return total - .5 * sum(count * (math.log10(count/n) - uni[c]) for c, count in freq.items())
        saved = json.loads((r3 / filename).read_text())['answers']
        score_error = max(abs(score(row['key']) - row['score']) for row in saved)
        assert score_error < .001  # original C input rounds unigrams to six decimals
        for row in saved:
            assert abs(sum(row['key'][t] == c for t, c in zip(tokens, plain))/n - row['accuracy']) < 1e-12
        diagnostic = perturbation_report(tokens, truth, list(ALPHABET), score)
        assert diagnostic['tested'] == 1180
        assert diagnostic['improving'] == (21 if name == 'original' else 20)
        report['models'][name] = dict(tokens=n, saved_accuracy=[r['accuracy'] for r in saved],
            max_saved_score_error=score_error, **{k: diagnostic[k] for k in ['tested', 'improving', 'improving_symbols']})
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
