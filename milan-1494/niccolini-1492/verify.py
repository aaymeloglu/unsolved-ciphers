#!/usr/bin/env python3
"""Check the tiers in reading-words.tsv against the listed sign values, and print the tier counts.

usage: python3 milan-1494/niccolini-1492/verify.py   (standard library only; runs from any directory)

A sign's values are looked up as in decode.py: niccolini-table.json first, then key.json via alias.json.
In the labels column, a label's alternatives in braces ({...}) and a trailing '?' are ignored for the lookup,
but a strict word may not contain them.

Rules checked:
- strict: every sign has exactly one listed value, no label has an alternative, and the reading equals that string.
- forced: no sign is unknown, and the reading equals one of the strings the listed values allow.
- lenient, doubt, unread: no check (the reading needs an unlisted value, a new shape reading, or a choice by sense).
Comparison ignores [bracketed] text (editorial letters and name expansions), case, accents, apostrophes,
spaces and dots, and treats u/v and i/j as the same letter. Exits 1 on any violation.
"""
import csv, itertools, json, os, re, sys, unicodedata
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
table = json.load(open(os.path.join(HERE, "niccolini-table.json")))
key = json.load(open(os.path.join(HERE, "..", "key.json")))["signs"]
alias = json.load(open(os.path.join(HERE, "alias.json")))
TIERS = ["strict", "forced", "lenient", "doubt", "unread"]


def values(lab):
    if lab in table:
        return table[lab]["values"]
    k = alias.get(lab)
    if k and k in key:
        return key[k]["values"]
    return None


def norm(s):
    s = re.sub(r"\[[^\]]*\]", "", s)
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[\s'’.\-]", "", s.lower())
    return s.replace("v", "u").replace("j", "i")


def main():
    rows = list(csv.DictReader(open(os.path.join(HERE, "reading-words.tsv")), delimiter="\t"))
    errors, counts = [], defaultdict(Counter)
    for r in rows:
        tag = f"{r['passage']} {r['word_no']} {r['reading']!r}"
        tier = r["tier"]
        if tier not in TIERS:
            errors.append(f"{tag}: unknown tier {tier}")
            continue
        counts[r["passage"]][tier] += 1
        counts["total"][tier] += 1
        if tier not in ("strict", "forced"):
            continue
        toks = r["labels"].split()
        vals, alt = [], False
        for t in toks:
            if "{" in t or t.endswith("?"):
                alt = True
            v = values(re.sub(r"\{.*?\}", "", t).rstrip("?"))
            if v is None or v == ["?"]:
                errors.append(f"{tag}: {t} has no listed value")
                vals = None
                break
            vals.append(sorted({norm(x) for x in v}))
        if vals is None:
            continue
        allowed = {"".join(p) for p in itertools.product(*vals)}
        rd = norm(r["reading"])
        if tier == "strict":
            if alt:
                errors.append(f"{tag}: strict word with a second shape reading")
            if any(len(v) > 1 for v in vals):
                errors.append(f"{tag}: strict word with a multi-valued sign")
        if rd not in allowed:
            shown = sorted(allowed)[:8]
            errors.append(f"{tag}: reading {rd!r} not among allowed {shown}{' ...' if len(allowed) > 8 else ''}")

    order = [p for p in dict.fromkeys(r["passage"] for r in rows)] + ["total"]
    print(f"{'passage':8} " + " ".join(f"{t:>8}" for t in TIERS) + f" {'words':>6}  strict / +forced / +lenient")
    for p in order:
        c = counts[p]
        n = sum(c.values())
        cum = [c["strict"], c["strict"] + c["forced"], c["strict"] + c["forced"] + c["lenient"]]
        print(f"{p:8} " + " ".join(f"{c[t]:>8}" for t in TIERS) + f" {n:>6}  {cum[0]} / {cum[1]} / {cum[2]}")
    for e in errors:
        print("VIOLATION:", e)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
