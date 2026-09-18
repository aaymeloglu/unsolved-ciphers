#!/usr/bin/env python3
"""Steepest-ascent hill climbing with random kicks for the Forster cipher, on cipherkit.climb.

    uv run python climb.py RESTARTS SEED SPLIT_LINES
"""
import json
import random
import sys

from cipherkit import climb as kit_climb

from solver import ALPH, decode, parse, score_text


def run(n_restarts, seed, split, kicks=25):
    words = parse(split)
    syms = sorted({s for w in words for s in w})
    rnd = random.Random(seed)

    def score(m):
        return score_text(decode(words, m))

    overall = []
    for r in range(n_restarts):
        bm, best = kit_climb({s: rnd.choice(ALPH) for s in syms}, list(ALPH), score)
        for _ in range(kicks):
            m2 = dict(bm)
            for s in rnd.sample(syms, rnd.randint(2, 5)):
                m2[s] = rnd.choice(ALPH)
            m2, sc = kit_climb(m2, list(ALPH), score)
            if sc > best:
                best, bm = sc, m2
        overall.append((best, bm))
        print(f"[{r}] {best:.1f} | {' '.join(decode(words, bm))}", flush=True)
    overall.sort(key=lambda x: -x[0])
    b, m = overall[0]
    print("\nBEST", round(b, 1))
    print(" ".join(decode(words, m)))
    print(json.dumps(m, sort_keys=True))


if __name__ == "__main__":
    run(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
