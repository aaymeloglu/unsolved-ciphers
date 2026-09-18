# cipherkit

The pieces every solver in this repo needs, written once. Before this package the research
folder held 140 scripts with the same add-0.5 quadgram scorer copied 13 times and the same
annealing loop 7 times, and matched controls were run on about half the targets.

No dependencies beyond the standard library. Python 3.12, managed by uv.

## Modules

| Module | What it gives you |
|---|---|
| `normalize` | `normalize(text, alphabet, folds, keep_spaces)` so the model and the decipherment share one alphabet. Folds run before accent stripping (ä to ae, not a). `GERMAN_FOLDS`, `EARLY_MODERN_FOLDS` (j to i, v to u). `strip_gutenberg`. |
| `lm` | `CharLM` (order-n, add-alpha, log10, cached; `score`, `score_words`, `per_window`). `WordLM` (unigram + bigram, character backoff for unseen words). `BackoffCharLM` (stupid backoff, for scoring a single unseen word). `cached(path, build, loader)` to build once per target. |
| `anneal` | `anneal(symbols, values, score, fixed=, bijective=, iters=, t0=, t1=, seed=, init=)` over a plain dict. `frequency_init` for a ranked homophonic start. `climb` for a greedy finish. `restarts(run, seeds, workers)` for several seeds in parallel. |
| `controls` | `matched_control(corpus, target_tokens, design)` builds a synthetic cipher of the same length and symbol count. `mono_control`, `homophonic_control` (homophones apportioned by letter frequency). `key_recovery(found, true, weights)`. `permutation_z(score, tokens, n)` for the shuffle test. |
| `tokens` | `parse(text, style)` for the four transcription formats we produce (`groups`, `mixed`, `annotated`, `letters`); `cipher_tokens`, `segments`, `symbol_counts`. |
| `corpora` | `RECIPES` of Gutenberg ids per language (en, fr, de, it, es, la, nl), `fetch(lang)`, `text(lang)`. Every fetch prints the Gutenberg title and language line, because five of the first ids tried were the wrong edition. |

## A homophonic solve, end to end

```python
from cipherkit import *
from cipherkit.corpora import text

corpus = normalize(text("fr"), folds=EARLY_MODERN_FOLDS)
lm = cached("lm_fr.pkl", lambda: CharLM.from_text(corpus, order=4), CharLM.load)

toks = cipher_tokens(parse(open("ciphertext.txt").read()))
symbols = sorted(set(toks))
letters = sorted(set(corpus))

def score(m):
    return lm.score("".join(m[t] for t in toks))

# 1. Can the solver read a control of this shape at all? If not, stop here.
ctl, ctl_key, _ = matched_control(corpus, toks, design="homophonic", seed=0)
def ctl_score(m):
    return lm.score("".join(m[t] for t in ctl))
init = frequency_init(ctl, corpus, letters)
runs = restarts(lambda s: anneal(sorted(set(ctl)), letters, ctl_score, iters=40000, seed=s, init=init),
                range(4), workers=1)
print("control recovery", key_recovery(runs[0][1], ctl_key, symbol_counts(parse(" ".join(ctl)))))

# 2. The target, with whatever the archive already fixed.
fixed = {"31214": "b"}  # a crib, or entries from a surviving key
init = frequency_init(toks, corpus, letters)
runs = restarts(lambda s: anneal(symbols, letters, score, fixed=fixed, iters=40000, seed=s, init=init),
                range(8), workers=1)
best = runs[0][1]

# 3. Is the reading better than chance under this key?
print(permutation_z(lambda seq: lm.score("".join(best[t] for t in seq)), toks, n=1000))
```

`workers=1` is needed when `run` is a lambda; give `restarts` a module-level function to use
several processes.

## What the control numbers look like

Measured 2026-09-18 on the French corpus (Montaigne, Brantôme, Descartes), quadgram model,
four seeds, 40,000 iterations each:

| Control | Token-weighted key recovery |
|---|---|
| 500 letters, monoalphabetic, 25 symbols (English test fixture) | 1.00 on every seed |
| 360 tokens, homophonic, 45 symbols, random start | 0.47 best, 0.00 worst |
| same, `frequency_init` start | 0.67 best, 0.38 worst |
| same, 5-gram, 120,000 iterations | 0.55 on every seed |

At eight tokens per symbol a character model alone reads about half a homophonic key, and
the failure mode is the reading collapsing into e, s, n and t. This is the same wall Forster
hit, where word boundaries and a period lexicon (`WordLM`) carried the solve. Run the control
first so the target's number means something.

## Temperatures

`anneal` temperatures are in the score's units. With a log10 quadgram model over a few hundred
tokens one bad swap costs 10 to 50; the defaults `t0=10, t1=0.1` read a 500-letter monoalphabetic
control on every seed tried, and `t0=2` got stuck three seeds in four. Scale `t0` with the
ciphertext length and always run several seeds.

## Conventions this package assumes

- A negative result is reported next to a matched control the same solver does recover.
- The target's README says which corpus (language and Gutenberg ids) its model was built from.
- Every published reading is graded per group: from a key source, from known plaintext,
  uncertain, or inferred.
