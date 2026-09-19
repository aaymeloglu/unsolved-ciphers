#!/usr/bin/env python3
"""Reproduce the Moray 1568 reading from transcription.txt and key.json, check it against the
committed reading.txt, print the grade counts, and, when cipherkit's Scots corpus is present,
the permutation z of the key against shuffled keys. Standard library plus cipherkit.

    python3 moray-1568/verify.py            # check (exit 1 if reading.txt is stale)
    python3 moray-1568/verify.py --write    # rewrite reading.txt
"""
import json
import os
import random
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)


def load():
    key = {k: v for k, v in json.load(open(os.path.join(HERE, "key.json"))).items() if not k.startswith("_")}
    lines = []
    for line in open(os.path.join(HERE, "transcription.txt")):
        if line.startswith("L"):
            tag, body = line.split(":", 1)
            lines.append((tag, [grp.split() for grp in body.split("|")]))
    return key, lines


def render(key, lines):
    out = []
    for tag, groups in lines:
        words = []
        for grp in groups:
            s = ""
            for t in grp:
                v, g = key[t]["value"], key[t]["grade"]
                if v.startswith("["):
                    s += v
                elif g == "S":
                    s += v
                else:
                    s += f"({v})"
            words.append(s)
        out.append(f"{tag}: " + " | ".join(words))
    return "\n".join(out) + "\n"


def grades(key, lines):
    from collections import Counter
    c = Counter()
    for _, groups in lines:
        for grp in groups:
            for t in grp:
                c[key[t]["grade"]] += 1
    return c


def permutation_z(key, lines, n=1000, seed=0):
    """Dictionary-segmentation score of the reading under the key, against the same score under
    keys that shuffle the letter values among the letter glyphs (word-signs fixed)."""
    try:
        from cipherkit import corpora
        raw = corpora.text("sco")
    except Exception as e:  # corpus not fetched
        return None, f"no Scots corpus ({e.__class__.__name__}); run: python -m cipherkit.corpora fetch sco"
    from solver import Scorer
    sc = Scorer(raw)
    letters = {k: v["value"] for k, v in key.items() if not v["value"].startswith("[")}
    glyphs = list(letters)
    chunks = [grp for _, groups in lines for grp in groups]

    def score(m):
        tot = 0.0
        for grp in chunks:
            s = "".join(m.get(t, "#") for t in grp)
            for piece in s.split("#"):
                if piece:
                    tot += sc.segscore(piece.replace("?", "q"))
        return tot

    obs = score(letters)
    rnd = random.Random(seed)
    null = []
    vals = [letters[g] for g in glyphs]
    for _ in range(n):
        v = vals[:]
        rnd.shuffle(v)
        null.append(score(dict(zip(glyphs, v))))
    mu, sd = statistics.mean(null), statistics.pstdev(null)
    return {"observed": obs, "null_mean": mu, "null_sd": sd, "z": (obs - mu) / sd,
            "p": sum(x >= obs for x in null) / n, "n": n}, None


def main():
    key, lines = load()
    text = render(key, lines)
    path = os.path.join(HERE, "reading.txt")
    header = "# Mechanical output of key.json over transcription.txt; \"|\" = gap on the page; [..] = word-sign; (..) = grade M or I.\n"
    if "--write" in sys.argv:
        open(path, "w").write(header + text)
        print("wrote reading.txt")
    committed = open(path).read()
    ok = committed == header + text
    print(text, end="")
    n = sum(grades(key, lines).values())
    print("grades:", dict(sorted(grades(key, lines).items())), "of", n, "glyphs")
    if "--z" in sys.argv:
        z, note = permutation_z(key, lines)
        print("permutation z:", z if z else note)
    if not ok:
        print("reading.txt is stale; run with --write", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
