#!/usr/bin/env python3
"""Permutation tests for the Forster 1644 key, both nulls, from ct.txt and mapping.json.

    uv run python forster-1644/permutation.py          # prints JSON

Score: a character 4-gram `CharLM` over `cipherkit.corpora` fr (Xivrey, Avenel, Montaigne,
Brantôme, Descartes) normalized with EARLY_MODERN_FOLDS (j to i, v to u), applied to the 207
decoded letters run together; the bracketed clear stretches and the date are left out, and
the word breaks are not scored. n = 1000 shuffles, seed 0, for each null:

- token shuffle (`cipherkit.controls.permutation_z`): the 207 tokens in random order, decoded
  with the key. Asks whether the order of the text is informative under this key.
- key shuffle (`cipherkit.controls.permutation_z_key`): the text as written, decoded with keys
  that shuffle the 34 plaintext values among the symbols. Asks whether this key beats a
  relabelling of the same symbols.

The two z values answer different questions and are not comparable. Needs the fr corpus
(`uv run python -m cipherkit.corpora fetch fr`); without it the script says so and exits 0,
so CI does not depend on the corpus.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from cipherkit import CharLM, EARLY_MODERN_FOLDS, normalize, permutation_z, permutation_z_key  # noqa: E402
from cipherkit.corpora import text  # noqa: E402

N, SEED, ORDER = 1000, 0, 4


def tokens():
    raw = open(os.path.join(HERE, "ct.txt"), encoding="utf-8").read()
    cipher = re.sub(r"\[.*?\]", "|", raw, flags=re.S)
    return [t for part in re.split(r"[,|]", cipher) for t in re.findall(r"\d+|[a-z]", part)]


def main():
    try:
        corpus = normalize(text("fr"), folds=EARLY_MODERN_FOLDS)
    except FileNotFoundError as e:
        print(f"skipped: {e}")
        return 0
    lm = CharLM.from_text(corpus, order=ORDER)
    key = json.load(open(os.path.join(HERE, "mapping.json")))
    toks = tokens()
    assert len(toks) == 207 and len(set(toks)) == 34 == len(key)
    token_shuffle = permutation_z(lambda seq: lm.score("".join(key[t] for t in seq)), toks, n=N, seed=SEED)
    key_shuffle = permutation_z_key(lambda m: lm.score("".join(m[t] for t in toks)), key, toks, n=N, seed=SEED)
    print(json.dumps({
        "tokens": len(toks), "symbols": len(key), "model": f"CharLM order {ORDER}, corpus fr, EARLY_MODERN_FOLDS",
        "token_shuffle": token_shuffle, "key_shuffle": key_shuffle,
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
