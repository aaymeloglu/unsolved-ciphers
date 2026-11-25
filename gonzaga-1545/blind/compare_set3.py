"""Score the blind readers of crop set 3 (letter A places reread after the Vatican collation).

    uv run python gonzaga-1545/blind/compare_set3.py [3|4]

Each reread crop has the edition's signs (`target`) and the signs it replaced (`old`). A reader's
row is `new` if it holds the target sign for sign, `old` if it holds the replaced signs, `both` if
its own {a/b} alternatives allow either, otherwise `new~`/`old~` when only the look-alike pairs of
EDIT.md make it fit one of them, or `neither`. Rule, fixed before the readers reported: a reread is
supported when both readers give new (or both), rejected when both give old, contested otherwise.
"""
import itertools
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from compare_crops import found as found_in  # noqa: E402


SET = sys.argv[1] if len(sys.argv) > 1 else "3"


def expand(text):
    """Every sign sequence a row allows. A reader's alternative may span signs: {h/f r}, {59/s z}."""
    parts = [p[1:-1].split("/") if p.startswith("{") else [p] for p in re.findall(r"\{[^}]*\}|\S+", text)]
    return [" ".join(c).split() for c in itertools.product(*parts)]


def found(target, text, loose):
    return any(found_in(target, seq, loose) for seq in expand(text))


def verdict(row, new, old):
    old = [o.split() for o in (" ".join(c) for c in itertools.product(*[t[1:-1].split("/") if t.startswith("{") else [t] for t in old]))] if old else []
    n, o = found(new, row, False), any(found(x, row, False) for x in old)
    if n and o:
        return "both"
    if n or o:
        return "new" if n else "old"
    n, o = found(new, row, True), any(found(x, row, True) for x in old)
    return "new~" if n and not o else "old~" if o and not n else "either~" if n else "neither"


def main():
    keys = json.load(open(os.path.join(HERE, f"crops-set{SET}.key.json")))
    rows = {r: dict(ln.rstrip("\n").split("\t", 1) for ln in open(os.path.join(HERE, f"{r}.set{SET}.tsv")) if "\t" in ln) for r in ("R1", "R2")}
    tally = {}
    for k in sorted(keys, key=lambda k: (k["set"], k["page"], k["line"])):
        new = [t.rstrip("!") for t in k["target"].split()]
        old = k["old"].split()
        v = [verdict(rows[r].get(k["id"], ""), new, old) for r in ("R1", "R2")]
        if k["set"] == "control":
            res = "ok" if all(x in ("new", "both") for x in v) else "loose" if all(x != "neither" for x in v) else "missed"
        else:
            res = "supported" if all(x in ("new", "both") for x in v) else "rejected" if all(x == "old" for x in v) else "contested"
        tally.setdefault(k["set"], []).append(res)
        print(f"{k['id']} {k['set']:7} {k['page']} L{k['line']:<2} {res:9} R1 {v[0]:8} R2 {v[1]:8} new: {k['target']:26} old: {k['old']}")
        for r in ("R1", "R2"):
            print(f"       {r}: {rows[r].get(k['id'], '')}")
    for s, rs in tally.items():
        print(s + ":", ", ".join(f"{rs.count(x)} {x}" for x in dict.fromkeys(rs)))


if __name__ == "__main__":
    main()
