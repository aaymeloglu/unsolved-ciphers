#!/usr/bin/env python3
"""Homophone solver for the spelled-letter tokens of the 1646 'Queen's Court' cipher letter (f.10),
on cipherkit. Symbols below 100 are letters (unknown except the anchors fixed in the key file);
codes 100 and above are words (rendered from the key file when known, otherwise a word boundary).

    uv run python solve.py key129.txt f10_ct.txt RESTARTS SEED [--control]

The language model is a character 5-gram over `cipherkit.corpora` en, whose 17th-century half is
Bruce's Charles I in 1646, Evelyn's correspondence and the Nicholas Papers (the sources the 2026-09
run used, now fetched by the kit). --control runs the same solver on a synthetic text with the same
letter-run lengths and symbol count and reports key recovery.

Result on f.10 (2026-09-16): degenerate, vowel soup. 218 letter tokens over 61 symbols, mostly
suffixes and short fragments between word codes, is too thin for an n-gram solve even with 12
anchors fixed. The control says whether that is the text or the solver.
"""
import json
import random
import re
import sys

from cipherkit import CharLM, anneal, cached, homophonic_control, key_recovery, normalize, restarts, sample_plaintext
from cipherkit.corpora import text

ALPH = "abcdefghiklmnopqrstuvwxyz"  # no j


def load_key(path):
    key = {}
    for ln in open(path, encoding="utf-8"):
        ln = ln.split("#")[0].strip()
        if ln:
            n, t = ln.split(None, 1)
            key[n] = t.strip().lower()
    return key


def parse(path, key):
    """Items: ('L', sym) letter symbol, ('W', text) known word, ('B',) boundary."""
    seq = []
    for ln in open(path, encoding="utf-8"):
        if ln.startswith("#"):
            continue
        for tok in re.findall(r"\[[^\]]*\]|\S+", ln):
            if tok.startswith("["):
                seq.append(("W", re.sub(r"[^a-z ]", "", tok.lower())))
                continue
            t = tok.rstrip("?")
            if not t.isdigit():
                seq.append(("B",))
                continue
            if int(t) < 100 and t not in key:
                seq.append(("L", t))
            elif t in key:
                seq.append(("W", key[t].replace("-", " ")))
            else:
                seq.append(("B",))
        seq.append(("B",))
    return seq


def render(seq, m):
    out, cur = [], []
    for x in seq:
        if x[0] == "L":
            cur.append(m[x[1]])
        else:
            if cur:
                out.append("".join(cur))
                cur = []
            out.append(x[1] if x[0] == "W" else "|")
    if cur:
        out.append("".join(cur))
    return out


def make_control(seq, corpus, n_symbols, seed):
    """Same letter-run lengths and boundaries, letters from the corpus, a fresh homophonic key."""
    rnd = random.Random(seed)
    runs, n = [], 0
    for x in seq:
        if x[0] == "L":
            n += 1
        elif n:
            runs.append(n)
            n = 0
    if n:
        runs.append(n)
    plain = sample_plaintext(corpus.replace(" ", ""), sum(runs), seed)
    _, key = homophonic_control(plain, n_symbols, seed=seed)
    homophones = {}
    for s, c in key.items():
        homophones.setdefault(c, []).append(s)
    out, pos = [], 0
    for r in runs:
        for c in plain[pos : pos + r]:
            out.append(("L", rnd.choice(homophones[c])))
        out.append(("B",))
        pos += r
    return out, key


def main(argv):
    key = load_key(argv[1])
    seq = parse(argv[2], key)
    n_restarts, seed = int(argv[3]), int(argv[4])
    corpus = normalize(text("en"), alphabet=ALPH, keep_spaces=True)
    lm = cached("lm_en5.pkl", lambda: CharLM.from_text(" " + corpus + " ", order=5), CharLM.load)
    fixed = {s: key[s] for s in key if s.isdigit() and int(s) < 100}
    true_key = None
    if "--control" in argv:
        n_symbols = len({x[1] for x in seq if x[0] == "L"})
        seq, true_key = make_control(seq, corpus, n_symbols, seed)
        fixed = {}
    syms = sorted({x[1] for x in seq if x[0] == "L"}, key=str)
    print("letter tokens", sum(1 for x in seq if x[0] == "L"), "symbols", len(syms), "fixed", len(fixed), file=sys.stderr)

    def score(m):
        s = " ".join(p for p in render(seq, m) if p != "|")
        return lm.score(" " + re.sub(r" +", " ", s) + " ")

    def run(k):
        m, sc = anneal(syms, list(ALPH), score, fixed=fixed, iters=60000, t0=2.0, t1=0.05, seed=seed * 100 + k, swap_prob=0.2)
        print(f"[{k}] {sc:.1f}", file=sys.stderr)
        return m, sc

    results = restarts(run, range(n_restarts), workers=1)
    for _, m, sc in results[:3]:
        print("SCORE", round(sc, 1))
        print(" ".join(render(seq, m)))
        print(json.dumps(m, sort_keys=True))
        print()
    if true_key is not None:
        weights = {}
        for x in seq:
            if x[0] == "L":
                weights[x[1]] = weights.get(x[1], 0) + 1
        print(f"CONTROL key recovery (token-weighted): {key_recovery(results[0][1], true_key, weights):.2f}")


if __name__ == "__main__":
    main(sys.argv)
