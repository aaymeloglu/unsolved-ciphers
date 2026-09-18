#!/usr/bin/env python3
"""Verify committed research artifacts without modifying them; --write regenerates.

Standard library only. Grades follow ../CONVENTIONS.md. C denotes a value from
1635 known-plaintext alignment, not independent paleographic certainty in 1640.
Context-only 1640 additions remain M: no matched-control S claim is made.
"""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def grade_outputs(root):
    sys.path.insert(0, str(root))
    import decoder
    import extend_1640
    keys = {'R1889': decoder.read_key(root/'key-expanded-1635.json'),
            'R1890': decoder.read_key(root/'key-1640-supplemented.json')}
    changed = set()
    for line in (root/'transcriptions/R1890-working.txt').read_text().splitlines():
        if not line or line.startswith('#'): continue
        ident, body = line.split(' ', 1)
        pos = 0
        for token in body.split():
            if token.startswith('{'): break
            replacement = extend_1640.REVIEW.get(token, (token, ''))[0].split()
            for new in replacement:
                if new not in decoder.PUNCT:
                    pos += 1
                    if token in extend_1640.REVIEW: changed.add((ident, pos))
    doubtful35 = {('P1.L11',6), ('P1.L20',7), ('P1.L25',8), ('P2.L03',17)}
    summary = {}
    for record, suffix in [('R1889','working'), ('R1890','reviewed')]:
        counts = Counter()
        with (root/f'results/{record}-token-grades.tsv').open('w') as f:
            w = csv.writer(f, delimiter='\t', lineterminator='\n')
            w.writerow(['row','cipher_position','symbol','literal','grade','basis'])
            for row,pos,token in decoder.units(root/f'transcriptions/{record}-{suffix}.txt'):
                value = keys[record].get(token)
                if value is None:
                    grade,basis = 'M','Unmapped source sign'
                elif record == 'R1890' and (row,pos) in changed:
                    grade,basis = 'I','Image/context-assisted source-label amendment; see R1890-review.tsv'
                elif record == 'R1890' and token in extend_1640.SUPPLEMENT:
                    grade,basis = 'M','Contextual 1640 supplement; no matched-control S claim; see key-1640-evidence.tsv'
                elif record == 'R1889' and (token == '6' or (row,pos) in doubtful35):
                    grade,basis = 'M','Disputed source glyph; literal value retained, see READING-1635.md'
                else:
                    grade,basis = 'C','Value from R954/R1889 known-plaintext alignment; see key-evidence.tsv'
                counts[grade] += 1
                w.writerow([row,pos,token,value or '',grade,basis])
        summary[record] = dict(sorted(counts.items()))
    (root/'results/grades.json').write_text(json.dumps(summary,indent=2)+'\n')
    return summary


def generate(root):
    manifest=json.loads((root/'sources/manifest.json').read_text())
    for source in manifest['attachments']:
        actual=hashlib.sha256((root/source['saved']).read_bytes()).hexdigest()
        if actual != source['sha256']:
            raise SystemExit('Source attachment changed: '+source['saved'])
    for script,args in [('import_1640.py',[]),('decoder.py',['--check']),('extend_1640.py',[])]:
        subprocess.run([sys.executable,str(root/script),*args],check=True,stdout=subprocess.DEVNULL)
    return grade_outputs(root)


def generated_paths(root):
    yield from (root/'results').glob('*')
    for name in ['key-evidence.tsv','key-1640-evidence.tsv','key-1640-supplemented.json',
                 'transcriptions/R1890-working.txt','transcriptions/R1890-reviewed.txt','transcriptions/R1890-review.tsv']:
        yield root/name


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    if args.write:
        counts=generate(ROOT)
    else:
        with tempfile.TemporaryDirectory(prefix='ferdinand-verify-') as temp:
            work=Path(temp)/'research'
            shutil.copytree(ROOT,work,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
            counts=generate(work)
            stale=[]
            for f in generated_paths(work):
                target=ROOT/f.relative_to(work)
                if not target.exists() or f.read_bytes()!=target.read_bytes():stale.append(str(f.relative_to(work)))
            if stale:raise SystemExit('Stale artifacts; run verify.py --write: '+', '.join(stale))
    print('PASS: key hashes, alignment evidence, current readings, reviews, grades and committed outputs reproduced.')
    print(json.dumps(counts,indent=2))

if __name__=='__main__':main()
