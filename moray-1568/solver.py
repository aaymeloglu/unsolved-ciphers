#!/usr/bin/env python3
"""Dictionary-segmentation annealer used on the Moray postscript (18 September 2026).

Scores a glyph->letter map by the best segmentation of each gap-delimited chunk into corpus
words (word unigram log-probabilities; unknown words fall back to a character 4-gram with a
penalty), with a penalty for two glyphs sharing a letter. Moves: reassign one glyph, or swap
two. Word-signs are fixed to "#" and act as breaks. The scorer is `cipherkit.segment.Segmenter`.

    uv run python moray-1568/solver.py TRANSCRIPTION CORPUS RESTARTS SEED DUP_PENALTY [FIX]

FIX is "glyph=letter,glyph=#,..." for values to hold. The corpus used
in the campaign was a 1.3M-word text of CSP Scotland vol. 2 (Bain 1900), Haynes 1740,
Stevenson 1837 and HMC Salisbury i; cipherkit's `sco` corpus (Diurnal of Occurrents, Knox)
gives the same behaviour and is what verify.py uses. Standard library plus cipherkit.
"""
import json
import math
import random
import sys

from cipherkit.segment import Segmenter

LET = "abcdefghiklmnopqrstuvwy"


def read_chunks(path):
    chunks = []
    for line in open(path):
        if line.startswith("L"):
            for grp in line.split(":", 1)[1].split("|"):
                t = grp.split()
                if t:
                    chunks.append(t)
    return chunks


def main():
    tpath, cpath, nrest, seed, pen = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5])
    fix = dict(kv.split("=") for kv in sys.argv[6].split(",")) if len(sys.argv) > 6 and sys.argv[6] else {}
    chunks = read_chunks(tpath)
    syms = sorted({t for c in chunks for t in c})
    free = [s for s in syms if s not in fix]
    sc = Segmenter(open(cpath).read())

    def render(m, c):
        return "".join(m[t] for t in c)

    def score(m):
        tot = sc.score_chunks([render(m, c) for c in chunks])
        vals = [v for v in m.values() if v != "#"]
        return tot - pen * (len(vals) - len(set(vals)))

    def anneal(sd, iters=40000):
        rnd = random.Random(sd)
        m = {s: rnd.choice(LET) for s in syms}
        m.update(fix)
        cur = score(m)
        best, bm = cur, dict(m)
        for it in range(iters):
            T = 2.5 * (0.05 / 2.5) ** (it / iters)
            if rnd.random() < 0.5 or len(free) < 2:
                a = rnd.choice(free)
                old = m[a]
                m[a] = rnd.choice(LET)
                undo = ("r", a, old)
            else:
                a, b = rnd.sample(free, 2)
                m[a], m[b] = m[b], m[a]
                undo = ("s", a, b)
            new = score(m)
            if new >= cur or rnd.random() < math.exp((new - cur) / T):
                cur = new
                if cur > best:
                    best, bm = cur, dict(m)
            elif undo[0] == "r":
                m[a] = undo[2]
            else:
                m[a], m[b] = m[b], m[a]
        return best, bm

    def show(m):
        return " | ".join(" ".join(sc.segment(p)) if "#" not in p else p for c in chunks for p in [render(m, c)])

    res = []
    for r in range(nrest):
        b, bm = anneal(seed * 100 + r)
        res.append((b, bm))
        print(f"[{r}] {b:.1f} | {show(bm)}", flush=True)
    res.sort(key=lambda x: -x[0])
    print("BEST", res[0][0])
    print(show(res[0][1]))
    print(json.dumps({k: v for k, v in res[0][1].items() if k not in fix}, sort_keys=True))


if __name__ == "__main__":
    main()
