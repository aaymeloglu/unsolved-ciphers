#!/usr/bin/env python3
"""Steepest-ascent hill climbing with random kicks for the Forster cipher."""
import random, sys, json, math
import solver
from solver import parse, score_text, decode, ALPH

def climb(words, syms, rnd, m):
    cur = score_text(decode(words, m))
    improved = True
    while improved:
        improved = False
        best_delta = 0; best_move = None
        for s in syms:
            old = m[s]
            for L in ALPH:
                if L == old: continue
                m[s] = L
                sc = score_text(decode(words, m))
                if sc - cur > best_delta:
                    best_delta = sc - cur; best_move = (s, L)
            m[s] = old
        if best_move:
            m[best_move[0]] = best_move[1]; cur += best_delta; improved = True
    return cur, m

def run(restarts, seed, split, kicks=25):
    words = parse(split)
    syms = sorted(set(s for w in words for s in w))
    rnd = random.Random(seed)
    overall = []
    for r in range(restarts):
        m = {s: rnd.choice(ALPH) for s in syms}
        best, bm = climb(words, syms, rnd, m)
        for k in range(kicks):
            m2 = dict(bm)
            for s in rnd.sample(syms, rnd.randint(2, 5)):
                m2[s] = rnd.choice(ALPH)
            sc, m2 = climb(words, syms, rnd, m2)
            if sc > best:
                best, bm = sc, m2
        overall.append((best, bm))
        print(f"[{r}] {best:.1f} | {' '.join(decode(words, bm))}", flush=True)
    overall.sort(key=lambda x: -x[0])
    b, m = overall[0]
    print("\nBEST", b); print(' '.join(decode(words, m))); print(json.dumps(m, sort_keys=True))

if __name__ == '__main__':
    run(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
