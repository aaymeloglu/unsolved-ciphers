#!/usr/bin/env python3
"""Apply the blind shape classes (ridolfi-shapes/, alamanni-shapes/) to the published transcriptions:
relabel ÷ by dot position and the d/l stem signs by form, then re-tier words that no longer hold an ambiguous sign.
usage: apply_shapes.py <milan-1494 dir>"""
import csv, json, re, sys, os
D = sys.argv[1]; F = os.path.dirname(os.path.abspath(__file__))
TOKEN = re.compile(r"^(\^?)([^=\{\?]+|\?)(?:=([^\{\?]*))?(?:\{([^}]*)\})?(\?)?$")
key = json.load(open(os.path.join(D, 'key.json')))['signs']
def load(p): return list(csv.DictReader(open(p), delimiter='\t'))
def new_label(letter, fam, r):
    hi = r['confidence'] == 'high'
    if fam == 'A':
        gen = 'N' if letter == 'ridolfi' else '/'
        if not hi: return None
        if 'above' in r['dots']: return gen + "'"
        if r['dots'] == 'below': return gen + ","
        return None
    c = r['class']
    if letter == 'ridolfi':
        if not hi: return None
        return {'B1': 'Zh', 'B6': 'Zh', 'B2': 'Za', 'B5': 'LL'}.get(c)
    return None
stats = {}
for letter, fn, sd in (('ridolfi', 'ridolfi-transcription.tsv', 'ridolfi-shapes'), ('alamanni', 'alamanni-transcription.tsv', 'alamanni-shapes')):
    rel = {}
    for fam in 'AB':
        for r in load(os.path.join(F, sd, fam + '.tsv')):
            nl = new_label(letter, fam, r)
            if nl: rel[(r['id'], int(r['j']))] = (nl, r)
    lines = open(os.path.join(D, fn)).read().split('\n'); out = []; n_rel = n_strict = 0
    for line in lines:
        f = line.split('\t')
        if line.startswith('#') or line.startswith('id\t') or len(f) < 6 or f[3] != 'word':
            out.append(line); continue
        toks = f[4].split(); changed = False
        for j, t in enumerate(toks):
            if (f[0], j) in rel:
                nl, r = rel[(f[0], j)]
                raised, lab, chosen, alts, low = TOKEN.match(t).groups()
                if lab not in ('N', '/', 'Z', 'Zx', '5'): raise SystemExit(f"{f[0]} {j}: unexpected label {lab}")
                if alts and set(alts.split(',')) <= {'Z', '5'}: alts = None      # both were the same arm/hook form
                toks[j] = raised + nl + ('{' + alts + '}' if alts else '') + (low or ''); changed = True; n_rel += 1
        if letter == 'alamanni':                     # d/l alternatives settled by the arm (B3) / no arm (B1)
            for j, t in enumerate(toks):
                if t == '5{Zd}': toks[j] = '5'; changed = True
                if t == 'Zd{5}': toks[j] = 'Zd'; changed = True
        f[4] = ' '.join(toks)
        if changed and f[5] in ('forced', 'lenient'):
            clean = True
            for t in toks:
                raised, lab, chosen, alts, low = TOKEN.match(t).groups()
                if lab not in key and lab not in ("N'", "N,", "/'", "/,", 'Zh', 'Za', 'LL'): raise SystemExit(lab)
                multi = lab in key and len(key[lab]['values']) > 1
                if multi or alts or low or lab == '?' or (lab in key and key[lab]['grade'] == 'I'): clean = False
            if clean: f[5] = 'strict'; n_strict += 1
        out.append('\t'.join(f))
    open(os.path.join(D, fn), 'w').write('\n'.join(out))
    print(letter, 'signs relabelled', n_rel, 'words moved to strict', n_strict)
