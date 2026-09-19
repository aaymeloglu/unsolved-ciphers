"""Reproduce the spaced-control rows of the kit README (the Moray 1568 shape).

    uv run python -m cipherkit.measure_spaced_control            # the two control rows
    uv run python -m cipherkit.measure_spaced_control --margin   # the "200 units" sentence

Draws four spaced controls matched to moray-1568/transcription.txt and anneals each twice
from the same start, once scored by `Segmenter.score_chunks` over the gap-delimited chunks
and once by a quadgram `CharLM` over the decoded letters with gaps and word-signs dropped, so
the two README rows are measured on the same four samples. Every parameter is fixed here.
`--margin` instead scores five 40-word windows of held-out prose against the same letters
shuffled, the margin the "A spaced solve" section quotes. Standard library plus cipherkit;
needs the `sco` corpus; not run by CI. About 10 s.
"""
from __future__ import annotations

import collections
import json
import os
import random
import sys

from .anneal import anneal, frequency_init
from .controls import key_recovery, matched_control
from .corpora import text
from .lm import CharLM
from .normalize import normalize
from .segment import Segmenter

LANG = "sco"
N_SYMBOLS = 29
WORD_SIGNS = {"the": "[the]", "and": "[and]"}
SEEDS = (0, 1, 2, 3)
ITERS = 40000
TRAIN_SHARE = 0.8  # models from the first 80% (cut at a word boundary), plaintexts from the rest
SEGMENTER = dict(order=4, oov=-6.0, min_count=2, max_word=14)  # Segmenter defaults
CHARLM_ORDER = 4
MARGIN_WORDS, MARGIN_SEEDS = 40, (0, 1, 2, 3, 4)
TARGET = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "moray-1568", "transcription.txt")


def target_tokens(path: str = TARGET) -> list[str]:
    """The Moray glyph labels with " " for each gap on the page."""
    out: list[str] = []
    for line in open(path, encoding="utf-8"):
        if line.startswith("L"):
            for i, grp in enumerate(line.split(":", 1)[1].split("|")):
                if i:
                    out.append(" ")
                out.extend(grp.split())
    return out


def split(lang: str = LANG) -> tuple[str, str]:
    """(train, held): the normalized corpus cut at a word boundary at TRAIN_SHARE."""
    corpus = normalize(text(lang), keep_spaces=True)
    cut = corpus.rfind(" ", 0, int(len(corpus) * TRAIN_SHARE))
    return corpus[:cut], corpus[cut:]


def margin(lang: str = LANG, seeds=MARGIN_SEEDS, n_words: int = MARGIN_WORDS) -> list[dict]:
    """Segmenter score of a held-out window of `n_words` words minus the score of the same
    letters shuffled, one window per seed (the start word and the shuffle share the seed)."""
    train, held = split(lang)
    seg = Segmenter(train, **SEGMENTER)
    words = held.split()
    out = []
    for seed in seeds:
        rnd = random.Random(seed)
        start = rnd.randrange(0, len(words) - n_words)
        real = "".join(words[start : start + n_words])
        letters = list(real)
        rnd.shuffle(letters)
        out.append({"seed": seed, "start_word": start, "real": round(seg.score(real), 1),
                    "shuffled": round(seg.score("".join(letters)), 1),
                    "margin": round(seg.score(real) - seg.score("".join(letters)), 1)})
    return out


def measure(lang: str = LANG, seeds=SEEDS, iters: int = ITERS) -> dict:
    train, held = split(lang)
    seg = Segmenter(train, **SEGMENTER)
    lm = CharLM.from_text(train.replace(" ", ""), order=CHARLM_ORDER)
    letters = sorted(set(train) - {" "})
    target = target_tokens()
    out = {}
    for seed in seeds:
        toks, key, pt = matched_control(held, target, design="spaced", n_symbols=N_SYMBOLS, word_signs=WORD_SIGNS, seed=seed)
        chunks: list[list[str]] = [[]]
        for t in toks:
            if t == " ":
                chunks.append([])
            else:
                chunks[-1].append(t)
        symbols = sorted({t for t in toks if t != " "}, key=str)
        fixed = {s: "#" for s in WORD_SIGNS.values() if s in symbols}
        letter_toks = [t for t in toks if t != " " and t not in fixed]
        init = frequency_init(letter_toks, train, letters)
        true_letters = {s: v for s, v in key.items() if s not in fixed}  # recovery over letter symbols only
        weights = collections.Counter(letter_toks)  # token-weighted

        def seg_score(m):
            return seg.score_chunks(["".join(m[t] for t in c) for c in chunks])

        def lm_score(m):
            return lm.score("".join(m[t] for t in letter_toks))

        row = {"plaintext": pt, "distinct_letters": len({c for w in pt.split() if w not in WORD_SIGNS for c in w})}
        for name, score in (("segmenter", seg_score), ("charlm", lm_score)):
            # Homophonic (not bijective) anneal, kit default temperatures, same start for both scorers.
            found, best = anneal(symbols, letters, score, fixed=fixed, iters=iters, seed=seed, init=dict(init))
            row[name] = {"recovery": round(key_recovery(found, true_letters, weights), 2), "score": round(best, 1),
                         "decoded": " ".join("".join(found[t] for t in c) for c in chunks)}
            print(f"seed {seed} {name:9s} recovery {row[name]['recovery']:.2f}", file=sys.stderr, flush=True)
        out[seed] = row
    return out


if __name__ == "__main__":
    print(json.dumps(margin() if "--margin" in sys.argv else measure(), indent=1))
