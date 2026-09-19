#!/usr/bin/env python3
"""Check saved review evidence; optionally rescan original corpora. No key fitting.

python3 moray-1568/fresh_review.py [--write] [--corpus-dir PATH]
The default checks the published snapshot, not corpus completeness or handwriting.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent


def corpus_snapshot(folder, sources, words):
    counts, hits = Counter(), []
    for source in sources:
        path = folder / source['file']
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != source['sha256']:
            raise ValueError(f'Corpus source hash mismatch: {source["file"]}')
        text = data.decode(errors='replace').replace('\r\n', '\n').replace('\r', '\n')
        counts.update(re.findall(r'[a-z]+', text.lower()))
        for match in re.finditer(r'\blattis\b', text, re.I):
            before = text[max(0, match.start()-60):match.start()]
            hits.append(dict(file=path.name, line=text.count('\n', 0, match.start())+1,
                             broken_prelattis=bool(re.search(r'pr[eco]-\s*$', before, re.I)),
                             context=text[max(0, match.start()-65):match.end()+90]))
    return hits, {word: counts[word] for word in words}


def partitions(text, counts):
    found = []
    for mask in range(1 << (len(text)-1)):
        words, start = [], 0
        for i in range(1, len(text)):
            if mask & (1 << (i-1)):
                words.append(text[start:i])
                start = i
        words.append(text[start:])
        if all(counts[word] and (len(word)>1 or word in {'a', 'i', 'o'}) for word in words):
            found.append(words)
    return found


def result(evidence):
    key = json.loads((HERE / 'key.json').read_text())
    lines = {}
    for row in (HERE / 'transcription.txt').read_text().splitlines():
        if re.match(r'L[1-4]:', row):
            tag, body = row.split(':', 1)
            lines[tag] = body.replace('|', '').split()
    if [len(v) for v in lines.values()] != [46, 43, 38, 7]:
        raise ValueError('Token positions changed; review must be repeated')
    if lines['L4'] != ['Zz', 'x3', 'A', 'Xs', 'Z2', 'N', 'Zh']:
        raise ValueError('Last-line transcription changed; review must be repeated')
    hits = evidence['lattis_hits']
    for hit in hits:
        matches = list(re.finditer(r'\blattis\b', hit['context'], re.I))
        if len(matches) != 1:
            raise ValueError('Expected one lattis token per saved context')
        broken = bool(re.search(r'pr[eco]-\s*$', hit['context'][:matches[0].start()], re.I))
        if broken != hit['broken_prelattis']:
            raise ValueError('Saved OCR classification disagrees with context')

    def ending(z, singleton='?', fifth='?'):
        values = {k: v['value'] for k, v in key.items() if not k.startswith('_')}
        values.update(Zz=z, x3='n', Xs='u', t=singleton)
        row3 = ''.join(values[g] for g in lines['L3'])
        row4 = ''.join(fifth if i == 5 else values[g] for i, g in enumerate(lines['L4'], 1))
        return [row3, row4]

    strict = {z: ending(z, fifth=key['Z2']['value'])[1] for z in ['k', 't']}
    return dict(
        status='Unsolved; proposed readings remain hypotheses',
        source='moray-1568/transcription.txt',
        token_counts={k:len(v) for k,v in lines.items()},
        lattis_counts=dict(total=len(hits), broken_prelattis=sum(h['broken_prelattis'] for h in hits)),
        strict_final_with_visual_n_u=strict,
        boundary_patterns_per_reading=64,
        corpus_supported_partitions={s:partitions(s, evidence['boundary_word_counts']) for s in strict.values()},
        alternatives={
            'unknown_long_stroked_fifth':ending('k'),
            'es_and_omit_fifth':ending('k', 's', ''),
            'haille_and_word_sign_as_and_omit_fifth':ending('k', '[as]', ''),
        },
        caveat='OCR counts do not establish historical word forms. No null, deletion, or compound W sign is established.'
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--corpus-dir', type=Path)
    args = parser.parse_args()
    evidence = json.loads((HERE / 'review-evidence.json').read_text())
    if args.corpus_dir:
        hits, counts = corpus_snapshot(args.corpus_dir, evidence['sources'], evidence['boundary_word_counts'])
        if hits != evidence['lattis_hits'] or counts != evidence['boundary_word_counts']:
            raise ValueError('Full corpus rescan differs from saved evidence')
        print('Full corpus hashes and rescan match saved evidence.')
    expected = json.dumps(result(evidence), indent=2) + '\n'
    path = HERE / 'fresh-review-results.json'
    if args.write:
        path.write_text(expected)
    if not path.exists() or path.read_text() != expected:
        print('fresh-review-results.json is stale; run with --write', file=sys.stderr)
        return 1
    # The README must reproduce the frozen mechanical output exactly.
    reading = '\n'.join(row for row in (HERE / 'reading.txt').read_text().splitlines() if row.startswith('L'))
    if f'```\n{reading}\n```' not in (HERE / 'README.md').read_text():
        print('README baseline differs from reading.txt', file=sys.stderr)
        return 1
    print('Review snapshot and conditional readings verified; ending remains unresolved.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
