# cipherkit

The pieces every solver in this repo needs, written once. Before this package the research
folder held 140 scripts with the same add-0.5 quadgram scorer copied 13 times and the same
annealing loop 7 times, and matched controls were run on about half the targets.

Python 3.12, managed by uv; Pillow is the one dependency.

## Modules

| Module | What it gives you |
|---|---|
| `normalize` | `normalize(text, alphabet, folds, keep_spaces)` so the model and the decipherment share one alphabet. Folds run before accent stripping (ä to ae, not a). `GERMAN_FOLDS`, `EARLY_MODERN_FOLDS` (j to i, v to u). `strip_gutenberg`. |
| `lm` | `CharLM` (order-n, add-alpha, log10, cached; `score`, `score_words`, `per_window`). `WordLM` (unigram + bigram, character backoff for unseen words). `BackoffCharLM` (stupid backoff, for scoring a single unseen word). `cached(path, build, loader)` to build once per target. |
| `anneal` | `anneal(symbols, values, score, fixed=, bijective=, iters=, t0=, t1=, seed=, init=)` over a plain dict. `frequency_init` for a ranked homophonic start. `climb` for a greedy finish. `restarts(run, seeds, workers)` for several seeds in parallel. |
| `controls` | `matched_control(corpus, target_tokens, design)` builds a synthetic cipher of the same length and symbol count. `mono_control`, `homophonic_control` (homophones apportioned by letter frequency). `key_recovery(found, true, weights)`. `permutation_z(score, tokens, n)` for the shuffle test. |
| `tokens` | `parse(text, style)` for the four transcription formats we produce (`groups`, `mixed`, `annotated`, `letters`); `cipher_tokens`, `segments`, `symbol_counts`. |
| `transcribe` | The transcription workflow as commands: `layout` (deskew by ink-profile variance, find line bands; `--crop auto` finds the paper inside a dark photograph frame, `--flatten` removes its illumination gradient, `--slabs N` deskews a curled sheet in N pieces), `strips` (one PNG per line, labelled boards, manifest with source SHA-256 and boxes), `gaps` (word gaps in one line strip as column ranges), `compare` (align two passes token by token, alternatives count), `consensus` (third pass with `{a/b}` at disagreements), `review` (self-contained HTML with strip, chips, key values, disputed highlights). |
| `corpora` | `RECIPES` of Gutenberg and Internet Archive sources per language (en, fr, it, de, es, la, sco, nl), `fetch(lang)`, `text(lang)`, `describe(lang)`, `clean_ocr`. See "Period corpora" below. |

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

## Transcription

What we did by hand for Ottobon f38r (hand-typed line bounds, per-line strips, a blind reader,
a token-by-token comparison, a review page) is now six commands:

```bash
uv run python -m cipherkit.transcribe layout ottobon-1589/pages/f38r.jpg -o f38r.layout.json
#  -> 9 lines, rotate -3.25; f38r.layout.preview.png shows the bands. Edit the JSON if a band is wrong.
uv run python -m cipherkit.transcribe strips f38r.layout.json -o strips/
#  -> f38r-L01.png … f38r-L09.png, boards of four, manifest.json with the source hash and every box
#  (give the boards to a reader who has not seen the key; they write one line of tokens per line)
uv run python -m cipherkit.transcribe gaps strips/f38r-L03.png --min-gap 12
#  -> JSON with the blank column runs [x0, x1) between the first and last ink, to check a "|" in a transcription
#  (Moray 1568 at 35 px/mm: --dark 100 --min-ink 0.1 --min-gap 30 found all 12 gaps the transcription marks;
#  the leaf shows through, so without --dark a nearly blank line is all noise gaps; unmarked letter spaces
#  are 30-44 px and marked gaps 37-80 px, so expect extra gaps to filter by eye, and the trailing margin)
uv run python -m cipherkit.transcribe compare context.json blind.txt --names context,blind -o compare.json
#  -> 114 paired: 77 agree, 10 via alternative, 27 differ; agreement 0.76
uv run python -m cipherkit.transcribe consensus context.json blind.txt -o round2.json
#  -> agreed tokens as they are, {x/y} where the readers differ: the input to the next pass
uv run python -m cipherkit.transcribe review f38r.layout.json context.json --key ottobon-1589/key.json --compare compare.json -o review.html
```

`layout --crop auto` takes the paper as the largest bright run of rows and of columns inside a dark
frame, which is what a DECODE photograph of a page needs before the deskew and line finder can work.
`--flatten` subtracts the blurred background so a page that darkens towards one side gets one ink
threshold; `--slabs 4` deskews four horizontal pieces on their own when the sheet curls in the
photograph (the Ferdinand 1635 photographs are level at the top and three degrees off at the foot),
and `strips` cuts each line with its own residual angle from `line_rotate`.

The numbers above are the real f38r run against the blind reading from September 2026; the
hand-made comparison in the research folder recorded 84 agreements and 30 disagreements on a
slightly earlier context pass, so the tool reproduces the process. The line finder deskews by
maximising the variance of the horizontal ink profile (the page is 3.25 degrees off), masks scan
borders, finds text blocks, splits each block at its own valleys, and widens each line to the
midpoint of the gap so superscript numbers stay in the strip. Alignment is Needleman-Wunsch over
tokens, so an extra or missing token does not shift every later comparison. Layout files and
manifests are the evidence record: a crop can be cited by file hash and box.

## Period corpora

`python -m cipherkit.corpora fetch all` (about 40 s, 20 MB, gitignored) builds one corpus per
language from sources chosen for period and register, not size. Documentary editions on the
Internet Archive supply the diplomatic register the targets are written in; Gutenberg supplies
clean literary prose of roughly the right century. Word counts after cleaning, 2026-09-18:

| Lang | Words | Documentary sources (IA OCR) | Literary sources (Gutenberg) | Targets it serves |
|---|---|---|---|---|
| fr | 2.31 M | Henri IV lettres missives t.1 (Xivrey), Richelieu papiers d'Etat t.1 (Avenel) | Montaigne, Brantôme, Descartes | Forster 1644, Richelieu 1629, Cocquet 1616, Boreel 1653 |
| it | 0.35 M | Dispacci veneti alla corte di Francia 1589, Albèri Relazioni s.1 v.1 | Machiavelli | Ottobon 1589 |
| de | 0.34 M | Politische Correspondenz Friedrichs des Grossen v.22 (German half) | Lessing, Schiller/Goethe letters, Goethe | Starhemberg 1758, Ferdinand 1635 |
| es | 0.84 M | CODOIN t.8 | Lazarillo, Hurtado de Mendoza, Cervantes | SP 53/22 f.52 |
| la | 0.43 M | Petrarca Epistolae, Nadal Epistolae 1546-1577 | Caesar, Descartes | Worcester 1526, Ferdinand 1635 |
| sco | 0.37 M | Diurnal of Occurrents 1513-1575, Knox Works v.1 | | Moray 1568, Davison 1584 |
| nl | 0.13 M | | Vondel, Multatuli | Vande Perre 1653 |
| en | 0.70 M | Bruce, Charles I in 1646; Evelyn correspondence v.4; Nicholas Papers v.1–2 | Doyle, Dickens | Royalist 1646, Boswell 1643, Burgess 1912 |

`clean_ocr` runs on every file. It drops lines that are mostly non-letters (page furniture,
tables, OCR garbage) and lines whose function words point to another language, which is how
the French half of Frederick's correspondence, the editors' apparatus in every IA edition, and
Montaigne's Latin quotations come out. The marker lists are disjoint across languages (a test
checks this); `describe` prints the marker shares so a bad file shows. Known gaps: Fraktur
editions (Arneth's Maria Theresia) OCR to nothing and are excluded; Dutch has no 17th-century
letter edition online in plain text, so Vondel carries it; Italian is Venetian diplomatic
prose, which is right for Ottobon but not for Tuscan targets.

Every source id was verified by fetching it and reading the title and marker counts. Five of
the first Gutenberg ids tried were wrong editions (a Finnish Nathan der Weise, two English
translations, two Latin texts that were mostly English commentary), so add a source only
through `fetch`, never by editing the table blind.

## Conventions this package assumes

- A negative result is reported next to a matched control the same solver does recover.
- The target's README says which corpus (language and Gutenberg ids) its model was built from.
- Every published reading is graded per group: from a key source, from known plaintext,
  uncertain, or inferred.
