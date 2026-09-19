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
| `segment` | `Segmenter(text, order, oov, min_count, max_word)`: score a letter string by its best split into corpus words, with an order-n character fallback for unseen words. `score`, `segment`, `score_chunks` (any non-letter such as a `#` word-sign breaks a chunk), `from_corpus(lang)`. The Moray scorer; the kit's answer to the wall below. |
| `anneal` | `anneal(symbols, values, score, fixed=, bijective=, iters=, t0=, t1=, seed=, init=)` over a plain dict. `frequency_init` for a ranked homophonic start. `climb` for a greedy finish. `restarts(run, seeds, workers)` for several seeds in parallel. |
| `controls` | `matched_control(corpus, target_tokens, design)` builds a synthetic cipher of the same length and symbol count. `mono_control`, `homophonic_control` (homophones apportioned by letter frequency), `spaced_control` (word gaps kept as tokens, whole words replaced by a sign). `key_recovery(found, true, weights)`. Two permutation tests with different nulls: `permutation_z(score, tokens, n)` shuffles the tokens (is the order informative under this key?); `permutation_z_key(score, key, tokens, n, fixed=)` shuffles the key's values among its glyphs (is this key better than a relabelling of the same glyphs?). |
| `align` | Known plaintext to key. `read_tsv(path)` loads rows of `id`, `cipher` (space-separated units), `plain`, `evidence`; `align_rows(rows, fold=)` pairs one unit with one letter and returns per-symbol `Assignment`s (majority letter, every occurrence as `A01:3`, every disagreement in `conflicts`); `holdout(rows, key, fold=)` scores rows the key never saw; `apply(units, key)`. |
| `tokens` | `parse(text, style)` for the four transcription formats we produce (`groups`, `mixed`, `annotated`, `letters`); `cipher_tokens`, `segments`, `symbol_counts`. |
| `transcribe` | The transcription workflow as commands: `layout` (deskew by ink-profile variance, find line bands), `strips` (one PNG per line, labelled boards, manifest with source SHA-256 and boxes), `compare` (align two passes token by token, alternatives count), `consensus` (third pass with `{a/b}` at disagreements), `review` (self-contained HTML with strip, chips, key values, disputed highlights). |
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

# 3. Is the reading better than chance? Two nulls, two questions; say which one you report.
#    Token shuffle: is the order of the text informative under this key?
print(permutation_z(lambda seq: lm.score("".join(best[t] for t in seq)), toks, n=1000))
#    Key shuffle: is this key better than a relabelling of the same glyphs? (word-signs and
#    `fixed` symbols keep their values)
print(permutation_z_key(lambda m: lm.score("".join(m[t] for t in toks)), best, toks, n=1000))
```

The token shuffle is the right test for a claimed *text*: it asks whether the real order
scores above the same letters in any order, and a homophonic key that maps everything to
common letters still fails it. The key shuffle is the right test for a claimed *key* found by
search: it asks whether this assignment beats the other assignments of the same values to
the same glyphs, which is what an annealer was competing against. A word-divided cipher
scored by `Segmenter.score_chunks` needs the key shuffle, because shuffling the tokens also
destroys the word gaps. The two z values are not comparable with each other.

`workers=1` is needed when `run` is a lambda; give `restarts` a module-level function to use
several processes.

## A known-plaintext solve

When a draft, a printed decipherment or an attached key gives the plaintext (grade C), the work
is alignment, not search. Ferdinand 1635 is this shape: the R954 draft against the R1889 units.

```python
from cipherkit import align_rows, apply, holdout, read_tsv
fold = lambda s: s.replace("v", "u")  # u/v folding is the caller's declared choice, never the cipher's
key = {s: a.plain for s, a in align_rows(read_tsv("training-alignment.tsv"), fold=fold).items()}
print(holdout(read_tsv("heldout-1635.tsv"), key, fold=fold))  # positions, agree, mismatches
print(apply("10 h 8 m c 22 n".split(), key))  # hiberna
```

Keep `conflicts` in the README's evidence table: a symbol that met two letters is a transcription
question or a homophone, and the majority vote is only a default.

## A spaced solve

When the cipher keeps its word gaps (Moray 1568, Forster 1644), score each gap-delimited chunk
by its best segmentation into corpus words instead of by a character model. Word-signs are
substituted in as `#` and end a chunk.

```python
from cipherkit import Segmenter, anneal

seg = Segmenter.from_corpus("sco")
chunks = [["Xs", "M", "N"], ["Z2", "o", "V"]]  # glyphs between gaps, from the transcription
fixed = {"Z2": "#"}  # a word-sign

def score(m):
    return seg.score_chunks(["".join(m[t] for t in c) for c in chunks])

key, best = anneal(sorted({t for c in chunks for t in c}), "abcdefghiklmnopqrstuvwy", score, fixed=fixed)
print(seg.segment("thelordofmurray"))  # ['the', 'lord', 'of', 'murray']
```

Scores are log10; 40 words of unseen Scots prose score about 200 units above the same letters
shuffled (measured 2026-09-19 on the `sco` corpus, five samples: 195 to 229). `moray-1568/verify.py --z`
runs the key-shuffle test (`permutation_z_key`) with this scorer and reports z = 17.1.

## What the control numbers look like

Measured 2026-09-18 on the French corpus (Montaigne, Brantôme, Descartes), quadgram model,
four seeds, 40,000 iterations each:

| Control | Token-weighted key recovery |
|---|---|
| 500 letters, monoalphabetic, 25 symbols (English test fixture) | 1.00 on every seed |
| 360 tokens, homophonic, 45 symbols, random start | 0.47 best, 0.00 worst |
| same, `frequency_init` start | 0.67 best, 0.38 worst |
| same, 5-gram, 120,000 iterations | 0.55 on every seed |
| 134 tokens, spaced, 29 symbols (27 for letters and homophones, two word-signs), Scots, `Segmenter.score_chunks` | 0.98 best, 0.00 worst |
| same four controls, quadgram `CharLM` over the letters with gaps dropped | 0.39 best, 0.05 worst |

At eight tokens per symbol a character model alone reads about half a homophonic key, and
the failure mode is the reading collapsing into e, s, n and t. This is the same wall Forster
hit, where word boundaries and a period lexicon (`WordLM`) carried the solve. Run the control
first so the target's number means something.

The spaced rows are the Moray 1568 shape, measured 19 September 2026 by
`python -m cipherkit.measure_spaced_control`, which fixes every parameter: 134 tokens of Scots
from `sco`, 29 symbols of which two are word-signs for *the* and *and*, the models built from
the first 80% of the corpus (cut at a word boundary) and the four control plaintexts drawn
from the last 20% with `matched_control(design="spaced")`, seeds 0 to 3. The windows hold 20
to 25 distinct letters, so the homophone count moves between two and seven. Both rows anneal
the same four draws from the same `frequency_init` start, homophonic moves, 40,000 iterations,
the kit's default temperatures, recovery token-weighted over the letter symbols. The first row
scores the gap-delimited chunks with `Segmenter.score_chunks` (defaults; word-signs as `#`),
the scorer the Moray solve used: 0.98, 0.46, 0.14, 0.00 over seeds 1, 3, 0, 2, the same
one-in-four-reads pattern as the Moray folder's own controls (0.99, 0.35, 0.09, fragments).
The second row scores the decoded letters with the quadgram `CharLM`, gaps and word-signs
dropped: 0.39, 0.31, 0.05, 0.05 over seeds 3, 0, 1, 2. A spaced control is what a negative on
a word-divided target has to be reported next to: at this length the character model reads
none of the four and the segmenter reads one, so the segmenter is the scorer to run, and its
negative is the one that means something.

```python
target = [...]  # the target's tokens, " " kept where the page has a gap
toks, key, pt = matched_control(corpus, target, design="spaced", n_symbols=29,
                                word_signs={"the": "[the]", "and": "[and]"}, seed=0)
```

## Temperatures

`anneal` temperatures are in the score's units. With a log10 quadgram model over a few hundred
tokens one bad swap costs 10 to 50; the defaults `t0=10, t1=0.1` read a 500-letter monoalphabetic
control on every seed tried, and `t0=2` got stuck three seeds in four. Scale `t0` with the
ciphertext length and always run several seeds.

## Transcription

What we did by hand for Ottobon f38r (hand-typed line bounds, per-line strips, a blind reader,
a token-by-token comparison, a review page) is now five commands:

```bash
uv run python -m cipherkit.transcribe layout ottobon-1589/pages/f38r.jpg -o f38r.layout.json
#  -> 9 lines, rotate -3.25; f38r.layout.preview.png shows the bands. Edit the JSON if a band is wrong.
uv run python -m cipherkit.transcribe strips f38r.layout.json -o strips/
#  -> f38r-L01.png … f38r-L09.png, boards of four, manifest.json with the source hash and every box
#  (give the boards to a reader who has not seen the key; they write one line of tokens per line)
uv run python -m cipherkit.transcribe compare context.json blind.txt --names context,blind -o compare.json
#  -> 114 paired: 77 agree, 10 via alternative, 27 differ; agreement 0.76
uv run python -m cipherkit.transcribe consensus context.json blind.txt -o round2.json
#  -> agreed tokens as they are, {x/y} where the readers differ: the input to the next pass
uv run python -m cipherkit.transcribe review f38r.layout.json context.json --key ottobon-1589/key.json --compare compare.json -o review.html
```

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

`clean_ocr` runs on every file. It first rejoins words the printer broke at the right margin, so
`pre-\nlattis` counts as `prelattis` and not as a spurious `lattis`, and a hyphen before a capital
(`Anglo-\nSaxon`) is left alone. It then drops lines that are mostly non-letters (page furniture,
tables, OCR garbage) and lines whose function words point to another language, which is how the
French half of Frederick's correspondence, the editors' apparatus in every IA edition, and
Montaigne's Latin quotations come out. The marker lists are disjoint across languages (a test
checks this); `describe` prints the marker shares so a bad file shows. Known gaps: Fraktur
editions (Arneth's Maria Theresia) OCR to nothing and are excluded; Dutch has no 17th-century
letter edition online in plain text, so Vondel carries it; Italian is Venetian diplomatic prose,
which is right for Ottobon but not for Tuscan targets.

Every source id was verified by fetching it and reading the title and marker counts. Five of
the first Gutenberg ids tried were wrong editions (a Finnish Nathan der Weise, two English
translations, two Latin texts that were mostly English commentary), so add a source only
through `fetch`, never by editing the table blind.

## Conventions this package assumes

- A negative result is reported next to a matched control the same solver does recover.
- The target's README says which corpus (language and Gutenberg ids) its model was built from.
- Every published reading is graded per group: from a key source, from known plaintext,
  uncertain, or inferred.
