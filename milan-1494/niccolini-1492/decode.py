#!/usr/bin/env python3
"""Decode a neutral-label transcription with Niccolini's table, falling back to key MAP LXXII 183.

usage: decode.py transcription-neutral.tsv [--pass A|B]
Value source per sign, in order: niccolini-table.json (values from his own glossed letters), then key.json via
alias.json (sheet 183 as read in Ridolfi's hand), else '?'. Output per block: the label sequence with values, and a
letter string where a sign with several values shows them as (x/y), nulls as nothing, unknown signs as '?'.
The transcribers' own new labels N9-N13 mean different shapes from the table's N9/N10, so they are renamed
<pass>:N9 etc. before lookup (and come out '?') unless mapped in SHAPE_MAP below.
"""
import csv, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
table = json.load(open(os.path.join(HERE, "niccolini-table.json")))
key = json.load(open(os.path.join(HERE, "..", "key.json")))["signs"]
alias = json.load(open(os.path.join(HERE, "alias.json")))

# transcriber label -> table label, where the shapes are the same (filled in by hand after comparing shape notes)
SHAPE_MAP = {
    "A": {"N22": "S70", "N15": "N15"},
    "B": {"N22": "S70", "N15": "N15", "N9": "S54"},
}
OWN = {"N9", "N10", "N11", "N12", "N13"}


def base(tok):
    return re.sub(r"\{.*?\}", "", tok).rstrip("?")


def value(lab):
    if lab in table:
        return table[lab]["values"], "T"
    k = alias.get(lab)
    if k and k in key:
        return key[k]["values"], "K"
    return ["?"], "-"


def show(vals):
    vals = [v for v in vals]
    if vals == [""]:
        return ""
    if len(vals) == 1:
        return vals[0]
    return "(" + "/".join(v if v else "∅" for v in vals) + ")"


def main():
    path = sys.argv[1]
    p = sys.argv[sys.argv.index("--pass") + 1] if "--pass" in sys.argv else "A"
    rows = csv.DictReader((l for l in open(path) if not l.startswith("#")), delimiter="\t")
    for r in rows:
        if r["kind"] == "clear":
            print(f"{r['block']:9} L{r['line']:>3} [clear] {r['tokens']}")
            continue
        labs, out, src = [], [], []
        for t in r["tokens"].split():
            b = base(t)
            b = SHAPE_MAP.get(p, {}).get(b, (f"{p}:{b}" if b in OWN else b))
            v, s = value(b)
            labs.append(b); out.append(show(v)); src.append(s)
        print(f"{r['block']:9} L{r['line']:>3} {''.join(out)}")
        print(" " * 15 + " ".join(f"{l}={o or '∅'}{'' if s == 'T' else '*'}" for l, o, s in zip(labs, out, src)))


if __name__ == "__main__":
    main()
