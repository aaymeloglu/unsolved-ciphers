"""Score the blind readers of crop set 3 (letter A places reread after the Vatican collation).

    uv run python gonzaga-1545/blind/compare_set3.py

Each reread crop has the edition's signs (`target`) and the signs it replaced (`old`). A reader's
row is `new` if it holds the target sign for sign, `old` if it holds the replaced signs, `both` if
its own {a/b} alternatives allow either, otherwise `new~`/`old~` when only the look-alike pairs of
EDIT.md make it fit one of them, or `neither`. Rule, fixed before the readers reported: a reread is
supported when both readers give new (or both), rejected when both give old, contested otherwise.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from compare_crops import found  # noqa: E402


def verdict(row, new, old):
    n, o = found(new, row, False), bool(old) and found(old, row, False)
    if n and o:
        return "both"
    if n or o:
        return "new" if n else "old"
    n, o = found(new, row, True), bool(old) and found(old, row, True)
    return "new~" if n and not o else "old~" if o and not n else "either~" if n else "neither"


def main():
    keys = json.load(open(os.path.join(HERE, "crops-set3.key.json")))
    rows = {r: dict(ln.rstrip("\n").split("\t", 1) for ln in open(os.path.join(HERE, r + ".set3.tsv")) if "\t" in ln) for r in ("R1", "R2")}
    tally = {}
    for k in sorted(keys, key=lambda k: (k["set"], k["page"], k["line"])):
        new = [t.rstrip("!") for t in k["target"].split()]
        old = k["old"].split()
        v = [verdict(rows[r].get(k["id"], "").split(), new, old) for r in ("R1", "R2")]
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
