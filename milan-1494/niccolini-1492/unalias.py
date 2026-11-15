#!/usr/bin/env python3
"""Map a transcription in neutral labels (S10..S81, N1..) to key.json labels, for score.py.

usage: unalias.py transcription-neutral.tsv > transcription-keylabels.tsv
Columns as score.py expects: block, leaf, line, kind, tokens. Neutral labels come from alias.json (fixed before
transcription, see PREREGISTRATION.md). New labels (N1, N2, ...) are left as they are; score.py treats any label
not in key.json as an unidentified sign (one wildcard). Alternatives in braces and '?' marks are kept; score.py
uses the first shape reading.
"""
import csv, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
alias = json.load(open(os.path.join(HERE, "alias.json")))


def map_tok(tok):
    def sub(m):
        return alias.get(m.group(0), m.group(0))
    return re.sub(r"S\d\d", sub, tok)


rows = [l for l in open(sys.argv[1]) if not l.startswith("#")]
r = csv.DictReader(rows, delimiter="\t")
w = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
w.writerow(["block", "leaf", "line", "kind", "tokens"])
for row in r:
    toks = row["tokens"] if row["kind"] == "clear" else " ".join(map_tok(t) for t in row["tokens"].split())
    w.writerow([row["block"], row["leaf"], row["line"], row["kind"], toks])
