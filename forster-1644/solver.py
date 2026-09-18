#!/usr/bin/env python3
"""Homophonic substitution solver for the Forster 1644 letter, on cipherkit.

Symbols -> letters; word boundaries known (commas) or uncertain (line breaks).
Score = character 4-gram log-prob over the words with spaces, plus a lexicon bonus for
every word the period French lexicon knows. Simulated annealing with restarts.

    uv run python solver.py [restarts] [seed] [split_lines 0/1] [--control]

The language model and lexicon come from `cipherkit.corpora` fr (Xivrey's Henri IV letters,
Avenel's Richelieu, Montaigne, Brantôme, Descartes); run `python -m cipherkit.corpora fetch fr`
once. --control runs the same solver on a synthetic letter of the same shape (same word
lengths, same symbol count) enciphered from the corpus, and reports key recovery, so the
target's number means something. As the README records, the character model alone did not
carry this target; dict_solver.py did.
"""
import json
import random
import re
import sys

from cipherkit import BASE_FOLDS, CharLM, WordLM, anneal, cached, homophonic_control, key_recovery, normalize, restarts
from cipherkit.corpora import text

ALPH = "abcdefghiklmnopqrstuxyz"  # the letter writes i for j and u for v, and has no w
FOLDS = {**BASE_FOLDS, "j": "i", "v": "u"}  # so the corpus is folded to the same convention
CT = open("ct.txt", encoding="utf-8").read().split("\n")


def parse(split_lines):
    words, cur = [], []
    for ln in CT:
        ln = re.sub(r"\[.*?\]", "|", ln)
        for num, comma, bar in re.findall(r"(\d+|[a-z])\.?|(,)|(\|)", ln):
            if comma or bar:
                if cur:
                    words.append(cur)
                    cur = []
            else:
                cur.append(num)
        if split_lines and cur:
            words.append(cur)
            cur = []
    if cur:
        words.append(cur)
    return words


def models(holdout=False):
    """holdout=True trains on the first 90 % of the corpus and keeps the last 10 % for the
    control's plaintext, so the control is not scored by a model that has seen its words."""
    corpus = normalize(text("fr"), alphabet=ALPH, folds=FOLDS, keep_spaces=True)
    if holdout:
        cut = corpus.rfind(" ", 0, int(len(corpus) * 0.9))
        train, held = corpus[:cut], corpus[cut:]
        return held, CharLM.from_text(" " + train + " ", order=4), WordLM.from_text(train)
    lm = cached("lm_fr4_iu.pkl", lambda: CharLM.from_text(" " + corpus + " ", order=4), CharLM.load)
    lex = cached("lex_fr_iu.pkl", lambda: WordLM.from_text(corpus), WordLM.load)
    return corpus, lm, lex


CORPUS, LM, LEX = models(holdout="--control" in sys.argv)


def score_text(words_txt):
    s = " " + " ".join(words_txt) + " "
    bonus = sum(len(w) for w in words_txt if len(w) >= 2 and LEX.in_vocab(w))
    return LM.score(s) + 1.0 * bonus


def decode(words, m):
    return ["".join(m[s] for s in w) for w in words]


def solve(words, syms, seed, iters=120000, init=None):
    def score(m):
        return score_text(decode(words, m))
    best, sc = anneal(syms, list(ALPH), score, iters=iters, t0=3.0, t1=0.05, seed=seed, init=init, swap_prob=0.15)
    return sc, best


def prior(syms, rnd):
    """Numbers -> vowels, letters -> consonants: the starting guess used in 2026-09."""
    return {s: (rnd.choice("aeiou") if s.isdigit() else rnd.choice("bcdfglmnpqrstxz")) for s in syms}


def control(words, seed):
    """A synthetic letter with the same word lengths and symbol count, enciphered from the
    held-out tenth of the corpus (see models)."""
    rnd = random.Random(seed)
    lengths = [len(w) for w in words]
    corpus_words = [w for w in CORPUS.split() if 1 <= len(w) <= 12]
    by_len = {}
    for w in corpus_words:
        by_len.setdefault(len(w), []).append(w)
    plain = [rnd.choice(by_len[n]) if n in by_len else "".join(rnd.choice(ALPH) for _ in range(n)) for n in lengths]
    symbols = sorted({s for w in words for s in w})  # the target's own symbols, so priors still apply
    _, key = homophonic_control("".join(plain), len(symbols), seed=seed, symbols=symbols)
    homophones = {}
    for sym, letter in key.items():
        homophones.setdefault(letter, []).append(sym)
    ct_words = []
    for w in plain:
        ct_words.append([rnd.choice(homophones[c]) if c in homophones else rnd.choice(list(key)) for c in w])
    return ct_words, key, plain


def main(argv):
    n_restarts = int(argv[1]) if len(argv) > 1 else 8
    seed = int(argv[2]) if len(argv) > 2 else 1
    split = int(argv[3]) if len(argv) > 3 else 1
    words = parse(split)
    key = None
    if "--control" in argv:
        words, key, plain = control(words, seed)
        print("CONTROL plaintext:", " ".join(plain))
    syms = sorted({s for w in words for s in w})

    def run(k):
        rnd = random.Random(seed * 100 + k)
        init = prior(syms, rnd) if k % 2 == 0 else None
        sc, m = solve(words, syms, seed * 100 + k, init=init)
        return m, sc

    results = restarts(run, range(n_restarts), workers=1)
    for k, m, sc in results:
        print(f"[{k}] {sc:.1f} | {' '.join(decode(words, m))}", flush=True)
    _, m, sc = results[0]
    print("\nBEST", round(sc, 1))
    print(" ".join(decode(words, m)))
    print(json.dumps(m, sort_keys=True))
    if key is not None:
        weights = {}
        for w in words:
            for s in w:
                weights[s] = weights.get(s, 0) + 1
        print(f"CONTROL key recovery (token-weighted): {key_recovery(m, key, weights):.2f}")


if __name__ == "__main__":
    main(sys.argv)
