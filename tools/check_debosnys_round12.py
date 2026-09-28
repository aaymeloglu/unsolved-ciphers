"""Replay real Debosnys round-12 results through the shared diagnostics.

Usage: python tools/check_debosnys_round12.py /path/to/debosnys --output /tmp/replay

The research directory supplies the four round-4 controls, source corpus,
Lexique/CMU dictionaries, round-12 sources and saved results. None are downloaded
or modified. Source parsing uses that experiment's saved round-5 reader so the
representations are identical; the new library checks them independently.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cipherkit import Segmenter, normalize, strip_gutenberg
from cipherkit.coverage import coverage_report
from cipherkit.diagnostics import perturbation_report
from cipherkit.evidence import rejection_record, verify_rejection


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('research', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    root = args.research.resolve()
    output = args.output.resolve()
    if output == root or root in output.parents:
        parser.error('output must be outside the research directory')
    output.mkdir(parents=True, exist_ok=True)
    controls = json.loads((root/'round4/controls/known.json').read_text())
    provenance = json.loads((root/'round4/provenance.json').read_text())
    expected = {r['control']: r for r in json.loads((root/'round12/scorer-gate.json').read_text())['results']}
    reports = []
    for corpus in provenance['corpus']:
        path = root/'sources'/corpus['source']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == corpus['source_sha256']
        words = normalize(strip_gutenberg(path.read_text()), keep_spaces=True).split()
        groups, last = [], 0
        for a, b in corpus['excluded_word_intervals']:
            groups.append(words[last:a]); last = b
        groups.append(words[last:])
        assert sum(map(len, groups)) == corpus['training_words']
        for ctl in controls:
            if ctl['language'] != corpus['language']:
                continue
            assert all(ctl['plaintext'] not in ''.join(g) for g in groups)
            model = Segmenter(' '.join(' '.join(g) for g in groups))
            lines = (root/'round4/controls'/f"{ctl['stem']}.txt").read_text().splitlines()
            chunks = [part.split() for line in lines for part in line.split('#') if part.strip()]
            tokens = sum(chunks, [])
            assert ''.join(ctl['key'][g] for g in tokens) == ctl['plaintext']
            def score(key):
                return model.score_chunks([''.join(key[g] for g in row) for row in chunks])
            r = perturbation_report(tokens, ctl['key'], 'abcdefghijklmnopqrstuvwxyz', score,
                                    singletons_only=True)
            old = expected[ctl['stem']]
            assert r['tested'] == old['tested_alternatives']
            assert r['improving'] == old['improving_alternatives']
            assert r['improving_symbols'] == old['affected_singletons']
            assert abs(r['baseline_score']-old['true_score']) < 1e-8
            reports.append(dict(control=ctl['stem'], **r))
            print(ctl['stem'], r['tested'], r['improving'], flush=True)

    # This intentionally uses the historical reader, not a newly normalized or
    # silently repaired source. Only the diagnostic operations are replaced.
    sys.path.insert(0, str(root/'round5'))
    sys.path.insert(0, str(root/'round12'))
    from search import corpus_rows, DICTS, words as tokenize
    from source_scan import furniture

    target = [r['glyphs'] for r in json.loads((root/'round11/transcription-v1.3.json').read_text())
              if r['document'] == 'poem']
    cache = {}
    records = []
    for old in json.loads((root/'round12/source-alignments.json').read_text()):
        key = (old['source'], old['mode'], old['view'])
        if key not in cache:
            rows, _ = corpus_rows(root/'round12/sources'/old['source'], 'fr', old['mode'])
            if old['view'] == 'furniture_removed':
                rows = [r for r in rows if not furniture(r['text'])]
            cache[key] = rows
        rows = cache[key]
        start = next(i for i, r in enumerate(rows) if r['line'] == old['source_line'])
        window = rows[start:start+20]
        assert [r['text'] for r in window] == old['lines']
        plains = [None if '#' in r['value'] else r['value'] for r in window]
        r = rejection_record(target, plains)
        assert r['status'] == 'rejected' and verify_rejection(r), old
        r['source'] = dict(file=old['source'], line=old['source_line'], mode=old['mode'], view=old['view'])
        records.append(r)

    coverage = []
    lexicon = {word: [''.join(v) for v in variants] for word, variants in DICTS['fr'].items()}
    saved = json.loads((root/'round12/source-summary.json').read_text())
    for old in saved:
        if old['mode'] != 'dictionary':
            continue
        key = (old['source'], old['mode'], old['view'])
        if key not in cache:
            rows, _ = corpus_rows(root/'round12/sources'/old['source'], 'fr', 'dictionary')
            cache[key] = rows if old['view'] == 'raw' else [r for r in rows if not furniture(r['text'])]
        r = coverage_report([tokenize(row['text'], 'fr') for row in cache[key]], lexicon)
        assert r['evaluable_windows'] == old['counts']['four_evaluable']
        assert r['windows_with_missing_words'] == old['counts'].get('four_oov', 0)
        coverage.append(dict(source=old['source'], view=old['view'], **r))

    (output/'scorers.json').write_text(json.dumps(reports, indent=2)+'\n')
    (output/'rejections.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False)+'\n' for r in records))
    (output/'coverage.json').write_text(json.dumps(coverage, indent=2, ensure_ascii=False)+'\n')
    summary = dict(controls=len(reports), substitutions=sum(r['tested'] for r in reports),
                   verified_rejections=len(records), coverage_reports=len(coverage),
                   all_historical_counts_reproduced=True)
    (output/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary))


if __name__ == '__main__':
    # Source parsing is intentionally inherited from the experiment being replayed.
    # The main function resolves the supplied path before importing its modules.
    main()
