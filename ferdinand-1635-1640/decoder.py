#!/usr/bin/env python3
"""Exact-unit decoder and reproducible evidence audit. Python standard library only.

No language model, Latin correction, null removal, implicit token splitting,
case folding, or context-dependent key switching occurs in this decoder.
"""
import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PUNCT = {'.', ',', ';', ':', '-', '=', '(', ')'}
ALIGNMENTS = ['training-alignment.tsv', 'extension-alignment.tsv', 'postvalidation-alignment.tsv']

def read_key(path):
    return json.loads(Path(path).read_text())['mappings']

def render_unit(token, key):
    return key.get(token, token if token in PUNCT else f'⟦{token}⟧')

def text_parts(text):
    """Split cleartext islands, including nested superscript braces, exactly."""
    depth, start = 0, 0
    for i, char in enumerate(text):
        if char == '{':
            if depth == 0:
                if i > start:
                    yield False, text[start:i]
                start = i
            depth += 1
        elif char == '}':
            assert depth > 0, 'Unbalanced cleartext closing brace'
            depth -= 1
            if depth == 0:
                yield True, text[start:i+1]
                start = i+1
    assert depth == 0, 'Unclosed cleartext island'
    if start < len(text):
        yield False, text[start:]

def decode_line(line, key):
    """Preserve source row and cleartext; leave every unmapped unit explicit."""
    ident, text = line.split(' ', 1)
    parts = []
    for clear, part in text_parts(text):
        if clear:
            parts.append(part)
        else:
            parts.append(''.join(render_unit(t, key) for t in part.split()))
    return ident + ' ' + ''.join(parts)

def decode_file(path, key):
    return '\n'.join(decode_line(line, key) for line in Path(path).read_text().splitlines()
                     if line and not line.startswith('#')) + '\n'

def units(path):
    for line in Path(path).read_text().splitlines():
        if not line or line.startswith('#'):
            continue
        ident, text = line.split(' ', 1)
        text = ' '.join(part for clear, part in text_parts(text) if not clear)
        pos = 0
        for token in text.split():
            if token not in PUNCT:
                pos += 1
                yield ident, pos, token

def rows(name):
    with (ROOT / 'transcriptions' / name).open() as f:
        return list(csv.DictReader(f, delimiter='\t'))

def normalize_plain(s):
    # Only the declared Latin u/v normalization, never ciphertext normalization.
    return s.replace('v', 'u')

def derive(names):
    key, evidence = {}, {}
    for name in names:
        for row in rows(name):
            cipher, plain = row['cipher'].split(), normalize_plain(row['plain'])
            assert len(cipher) == len(plain), row['id']
            for pos, (symbol, value) in enumerate(zip(cipher, plain), 1):
                assert symbol not in key or key[symbol] == value, (row['id'], symbol, value, key.get(symbol))
                key[symbol] = value
                evidence.setdefault(symbol, []).append(f"{row['id']}:{pos}")
    return key, evidence

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def audit(output):
    output.mkdir(parents=True, exist_ok=True)
    v1_path, expanded_path = ROOT / 'key-v1.json', ROOT / 'key-expanded-1635.json'
    v1, expanded = read_key(v1_path), read_key(expanded_path)
    assert sha(v1_path) == '5803d66e26980adc1e9fd1c0571c86b2a09488d636969a1df74f71f8c846a9e5', 'Frozen key changed'
    assert derive(ALIGNMENTS[:1])[0] == v1
    assert derive(ALIGNMENTS)[0] == expanded
    assert all(not p.startswith(('V', 'F', 'E')) for ev in json.loads(v1_path.read_text())['evidence'].values() for p in ev)
    assert render_unit('NOT_A_SYMBOL', v1) == '⟦NOT_A_SYMBOL⟧'
    assert render_unit('P', v1) == '⟦P⟧', 'Cipher case must not be folded'
    assert render_unit('op', v1) == '⟦op⟧', 'Unknown code must not be split'
    assert decode_line('X {known clear} p UNKNOWN', v1) == 'X {known clear}e⟦UNKNOWN⟧'
    assert decode_line('X {Dil^{oi} Vra} p', v1) == 'X {Dil^{oi} Vra}e'

    counts, detail = Counter(), []
    for row in rows('heldout-1635.tsv'):
        tokens, expected = row['cipher'].split(), normalize_plain(row['plain'])
        assert len(tokens) == len(expected), row['id']
        for pos, (token, target) in enumerate(zip(tokens, expected), 1):
            actual = v1.get(token)
            status = 'unknown' if actual is None else 'match' if actual == target else 'mismatch'
            counts[status] += 1
            detail.append([row['id'], pos, token, actual or '', target, status])
    assert dict(counts) == {'match': 87, 'mismatch': 3, 'unknown': 5}, counts
    with (output / 'heldout-occurrences.tsv').open('w') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n'); w.writerow(['span', 'position', 'symbol', 'literal', 'draft_expected', 'status']); w.writerows(detail)
    holdout = ['# Frozen v1 holdout: raw first-pass transcription, not post-review corrections.']
    for row in rows('heldout-1635.tsv'):
        holdout.append(row['id'] + '\t' + ''.join(render_unit(t, v1) for t in row['cipher'].split()) + '\t' + row['plain'])
    (output / 'heldout-v1.txt').write_text('\n'.join(holdout) + '\n')

    # Current reading of the same passage, with the documented image correction.
    # This reports the final documentary agreement, not a second blind test.
    followup_counts, followup_detail = Counter(), []
    working = (ROOT / 'transcriptions/R1889-working.txt').read_text()
    for row in rows('heldout-1635.tsv'):
        original = row['cipher'].split()
        tokens = original.copy()
        if row['id'] == 'V11':
            assert tokens[:4] == ['20', '0', '0', 'm']
            assert '20 c o m' in working
            assert '1 11 9 p q 32 z' in working  # P2.L03 image re-reading, 18 Sept 2026
            tokens[:4] = ['20', 'c', 'o', 'm']
        expected = normalize_plain(row['plain'])
        for pos, (old, token, target) in enumerate(zip(original, tokens, expected), 1):
            actual = expanded.get(token)
            status = 'unknown' if actual is None else 'match' if actual == target else 'mismatch'
            followup_counts[status] += 1
            followup_detail.append([row['id'], pos, old, token, actual or '', target, status])
    with (output / '1635-current-passage.tsv').open('w') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['span', 'position', 'original_label', 'reviewed_label', 'literal', 'draft_expected', 'status'])
        w.writerows(followup_detail)

    summary = {'key_v1_sha256': sha(v1_path), 'key_expanded_sha256': sha(expanded_path),
               'v1_mapping_count': len(v1), 'expanded_mapping_count': len(expanded),
               'holdout_first_pass': dict(counts), 'holdout_tokens': sum(counts.values()),
               'current_1635_passage': dict(followup_counts),
               'warning': 'Expanded key uses post-validation F evidence. Its coverage is not an independent validation. Symbol 6 is disputed.'}
    for record in ['R1889', 'R1890']:
        src = ROOT / 'transcriptions' / f'{record}-working.txt'
        for version, key in [('v1', v1), ('expanded', expanded)]:
            (output / f'{record}-{version}-literal.txt').write_text(
                '# Cleartext in braces. Unmapped units in double brackets. No editorial repairs.\n' + decode_file(src, key))
            inventory = Counter(t for _, _, t in units(src))
            unknown = {t: n for t, n in sorted(inventory.items()) if t not in key}
            summary[f'{record}_{version}'] = {'tokens': sum(inventory.values()),
                'mapped_tokens': sum(n for t, n in inventory.items() if t in key),
                'unmapped_tokens': sum(unknown.values()), 'unmapped_inventory': unknown}
            # Applying to either record must not mutate the map.
            assert key == read_key(v1_path if version == 'v1' else expanded_path)
    (output / 'audit.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n')

    # Evidence-linked table includes every supporting alignment occurrence.
    ev = derive(ALIGNMENTS)[1]
    with (ROOT / 'key-evidence.tsv').open('w') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n'); w.writerow(['symbol', 'plain', 'status', 'occurrence_evidence'])
        for symbol in sorted(expanded, key=lambda s: (not s.isdigit(), int(s) if s.isdigit() else s)):
            w.writerow([symbol, expanded[symbol], 'disputed: b/6-like; e here, m elsewhere' if symbol == '6' else 'aligned', ';'.join(ev[symbol])])
    print(json.dumps({k: v for k, v in summary.items() if not isinstance(v, dict) or k == 'holdout_first_pass'}, indent=2))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', nargs='?', type=Path)
    parser.add_argument('--key', type=Path, default=ROOT / 'key-expanded-1635.json')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'results')
    args = parser.parse_args()
    if args.check:
        audit(args.output_dir)
    elif args.input:
        print(decode_file(args.input, read_key(args.key)), end='')
    else:
        parser.error('Provide an input file or --check')
