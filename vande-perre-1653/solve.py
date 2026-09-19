#!/usr/bin/env python3
"""Find the Vande Perre key from the printed digits alone, as a check that key.json is what
ciphertext-only search recovers. Bijective simulated annealing then a swap hill-climb (cipherkit.anneal, climb) over
the 22 letter symbols, scored by a 4-gram character model of the kit's Dutch corpus with runs split
at code groups; no glosses, no cribs. Prints each seed's agreement with key.json.

    python3 vande-perre-1653/solve.py [n_seeds]      # default 16
"""
import functools
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from cipherkit.anneal import anneal, climb, restarts  # noqa: E402
from cipherkit.corpora import text  # noqa: E402
from cipherkit.lm import CharLM  # noqa: E402
from cipherkit.normalize import normalize  # noqa: E402

KEY = {k: v for k, v in json.load(open(os.path.join(HERE, "key.json"))).items() if not k.startswith("_")}
LETTERS = [k for k, v in KEY.items() if v["grade"] == "S"]
RUNS = []
for line in open(os.path.join(HERE, "transcription.txt")):
    if line.startswith("P"):
        cur = []
        for t in line.split(":", 1)[1].split():
            if t in LETTERS:
                cur.append(t)
            elif cur:
                RUNS.append(cur)
                cur = []
        if cur:
            RUNS.append(cur)
VALUES = list("abcdefghiklmnopqrstuvwyz")  # y stands for ij, as often in 17th-century Dutch
LM = None


def load_model():
    global LM
    if LM is None:
        LM = CharLM.from_text(normalize(text("nl"), keep_spaces=True), order=4)


def score(m):
    return LM.score_words("".join(m[t] for t in run) for run in RUNS)


def run(seed):
    load_model()
    m, _ = anneal(LETTERS, VALUES, score, bijective=True, iters=200000, t0=10.0, t1=0.1, seed=seed)
    return climb(m, VALUES, score, bijective=True)  # polish: best single swap until none helps


def agreement(m):
    want = {k: ("y" if v["value"] == "ij" else v["value"]) for k, v in KEY.items() if k in LETTERS}
    n = sum(1 for run_ in RUNS for t in run_)
    return sum(m[t] == want[t] for t in want), len(want), sum(m[t] == want[t] for r in RUNS for t in r), n


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    res = restarts(functools.partial(run), range(1, n + 1))
    for seed, m, s in res:
        sym, nsym, tok, ntok = agreement(m)
        print(f"seed {seed}: score {s:.1f}  symbols {sym}/{nsym}  tokens {tok}/{ntok}  "
              + " / ".join("".join(m[t] for t in r) for r in RUNS[:3]))
    load_model()
    want = {k: ("y" if v["value"] == "ij" else v["value"]) for k, v in KEY.items() if k in LETTERS}
    print(f"key.json scores {score(want):.1f}")
