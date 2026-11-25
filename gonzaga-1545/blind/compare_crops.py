"""Compare the two blind crop readings with the edition's signs for the same stretch.

    uv run python gonzaga-1545/blind/compare_crops.py

For every crop, the signs the edition has for the target (crops-set*.key.json, written when the
crops were cut) are looked for in each reader's row: `exact` if the row has them sign for sign,
`look-alike` if it has them once the look-alike pairs of EDIT.md are allowed (a reader's own {a/b}
alternatives count as exact), otherwise `differs`.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import check_edition as ce  # noqa: E402

ALIKE = {frozenset(p.split("/")) for p in ce.PAIRS} | {frozenset(p) for p in (("18", "19"), ("t", "h"))}


def options(tok):
    return tok[1:-1].split("/") if tok.startswith("{") else [tok]


def same(want, got, loose):
    if want in options(got):
        return True
    return loose and any(frozenset((want, g)) in ALIKE for g in options(got))


def found(target, row, loose):
    row = [t for t in row if t != "|"]
    for start in range(len(row) - len(target) + 1):
        if all(same(w, g, loose) for w, g in zip(target, row[start:start + len(target)])):
            return True
    return False


def main():
    keys = []
    for name in ("crops-set1.key.json", "crops-set2.key.json"):
        keys += json.load(open(os.path.join(HERE, name)))
    rows = {r: dict(ln.rstrip("\n").split("\t", 1) for ln in open(os.path.join(HERE, r + ".tsv")) if "\t" in ln) for r in ("R1", "R2")}
    tally = {}
    for k in sorted(keys, key=lambda k: (k["set"], k["id"])):
        target = [t.rstrip("!") for t in k["target"].split()]
        res = []
        for r in ("R1", "R2"):
            row = rows[r].get(k["id"], "").split()
            res.append("exact" if found(target, row, False) else "look-alike" if found(target, row, True) else "differs")
        tally.setdefault(k["set"], []).append(res)
        print(f"{k['id']} {k['set']:5} {k['page']} L{k['line']:<2} {k['target']:28} R1 {res[0]:10} R2 {res[1]:10} {k.get('frag', '')}")
    for s, rs in tally.items():
        both = sum(1 for a, b in rs if a != "differs" and b != "differs")
        one = sum(1 for a, b in rs if (a != "differs") != (b != "differs"))
        print(f"{s}: {len(rs)} crops; both readers agree with the edition on {both}, one of the two on {one}, neither on {len(rs) - both - one}")


if __name__ == "__main__":
    main()
