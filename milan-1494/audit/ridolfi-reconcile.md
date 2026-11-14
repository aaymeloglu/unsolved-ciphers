> Audit file. Reconciliation log written by the transcriber of Ridolfi's letters on 13 November 2026, after a fresh sign-by-sign transcription (frozen and hashed before the earlier working transcription was opened) was compared with that earlier transcription. File names refer to the research folder, not this repository; crops and images are not redistributed.

# Phase B: reconciliation with the previous pass

Inputs: my frozen Phase A transcription (`frozen/blind_transcription.txt`, hashes in `frozen/SHA256SUMS`) against `../transcription_112r.txt` (doc 112 lines 4-18 only; the previous file stops at line 18) and `../reading.md`. Docs 113 and 115 had no earlier sign-by-sign transcription, so mine is the first; for those I compared readings only.

What "blind" covered: I had not opened the previous transcription, reading or README. I had seen `key.tsv`, `decode.py` and `validate.py` (so I knew the sheet values and eight glossed word pairs from docs 107/110), and I read for sense while transcribing, as anyone holding the key does. Sign choices in Phase A are therefore not independent of the Italian. Where I could not separate two signs by shape I wrote both (`a|b`) instead of picking one.

Shape rules I fixed before comparing (from the key sheet, the doc 110 gloss strips in `exemplars/`, and recurring words in the targets):

| pair | rule |
|---|---|
| e-sign vs o-sign vs p-sign | `eo` = small o with a flag leaving the top right (e); `oo` = small e/o sitting on a long underline (o); `S` = σ with a long flat top bar (p). The previous pass merged these as "S (e, sometimes p)" and "e (= o)". |
| d vs l | `5` = closed round bowl with crossed, left-leaning ascender (l). `Z` = open, h-like crossed form: used for d and also, often, for l. I could not find a reliable feature, so `Z` stays d\|l. |
| h vs s | `^` = stem rising from the middle of a base stroke that extends to its left (h); `L` = stem at the left end (s). |
| p vs z vs l | `pb` = b with a hooked flag (p); a 6 with a looped top (z) is close to it; plain `b`/`6` = l, i or z. |
| geminates | five or six signs not on the sheet stand for doubled consonants (see `signs.tsv`). |

## Disagreements in doc 112 and decisions

Re-cropped at 4-5x in Phase B: lines 5, 6, 8, 10, 11 (code signs), 8-9 (edicto, ricomperare), 12 (end of strignere…), 19 (chi havessi). The rest were decided on the Phase A crops (3x), which are in `crops/`.

| line | previous | mine | decision and shape reason |
|---|---|---|---|
| 4, 6, 10, 11 | `IO` (= io) | `RC`, `RD` | Two different signs: a long-tailed 2 with a raised c (line 4) and with a raised ђ (lines 6, 10, 11). The sheet's io sign has a tick, not a raised letter. Kept mine. Values come from context, not shape. |
| 4 | `Sp 11 p c` | `S 11 p c` | Same signs. Both passes see no i-sign: the group is p-a-u-a, i.e. "Pav[i]a" short one letter. |
| 5 | `Z S Z P 5 c 5 7 o 9 c IO P / c` | `X3 eo 5 P · Z¦5 c · Z i B Q c · 2 P N c` | First sign is a tall ξ at the line start, continuing `N 11 o` of line 4 (castelo). The fourth group has a clear B (che) after ı, then the looped-descender 9. The sign before `P N c` is a plain 2 (b), no tail. Kept mine: "la duchessa Bona". |
| 5 | clear text "si h… mi vostro" | "si li fece incontro" | Clear hand; mine. |
| 5 | `L 11 5 c` | `L 11 5¦^¦n c` | Third sign is a crossed stem whose bowl I cannot see; kept three alternatives. |
| 5 | `6 9 7` | `S 9 7` | σ with flat top bar, not 6. Kept mine (pri-). |
| 6 | `AL` (come) | `ET` | Same bold λ sign as in "Lorenzo et Giovanni" (113v, 115r). Kept ET. |
| 6 | `c Z 11` | `c · 5 11` | Closed bowl: 5. |
| 6 | `x m 4 c` | `x m 9 c` | 9 and 4 both = r; no effect. |
| 6 | `IO 9 1 c Z p` as cipher | `RD 9n` then clear "che pur" | The last three marks match the clear-hand abbreviation for "che" used in lines 1-3. Kept mine, medium confidence. |
| 7 | `/ m d S phi P` | `N m · 5 eo PSI P` | Third sign has a crossbar on the ascender, so it is the l-sign, not ∂ (g). Kept mine: "ne letto". |
| 8 | `8 S 11 / 6 7` | `8 NN 11 N 6¦pb 7` | Second sign is the large looped e-form, larger than the e/o signs; it recurs in Donnino, Giovanni, danno. Kept NN. |
| 8 | `11 6 S p 7 c` | `11 · pb c p 7 c` | Flagged b, then c. Kept mine (a Pavia); the previous reading agrees on the words. |
| 8 | `6 P m gf 7 / v P` | `b P · m Z 7 N v P` | Fourth sign is the crossed h-form, not long-s. Kept mine. Reading of the word (edicto) remains doubtful. |
| 8 | "sendo io" (clear) | "sendo ito" | Clear hand; mine. |
| 9 | `x 6 S 9 11 4 3` | `x S eo 9 11 4 3` | σ then flagged o: -mpe-. Kept mine (ricomperare). |
| 9 | `7 5 Z c 6 7 P Z S Z 11` | `7 Z · Z c 6¦pb 7 P · Z¦X3 eo 5 11` | Same signs, different classes; the d/l signs here are open forms, so `Z`. |
| 10 | `L 8 4 6 S v 4 7` | `L 8 4 6 o v 4 7` | Fifth sign is a plain o (s). Kept mine. |
| 10, 13, 15 | `e` | `oo` | Same sign, renamed. |
| 11 | `4 7 S 5 P S Z` | `4 7 o pb P o 3` | Plain o twice (s), flagged b (p), final 3. Kept mine (rispose). |
| 12 | `ET? [qn] A Z 11 b 11 d ^ c 9 7 / P` | `[che quando] TH 5¦Z 11 pb 11 gd ^ c 9¦Q 7 N P` | The line opens with clear "che q[ua]n[do]". Flagged b (p), not plain b. Kept mine. Whether the r/ss sign has the looped descender here is unclear: 9¦Q. |
| 12 | `L 4 7 d / m 4 3 7 o` | `L v 9 7 gd N m 4 3 BB? eo` | A small v is written above the line with a caret after L (insertion). The penultimate sign is a crossed 7 with a dot; Phase A had it as `X3¦7?`, Phase B re-crop reads it as the bb sign by likeness to 115r. Changed, and the word is marked doubtful. |
| 12, 13, 17, 18 | `9` | `Q` | The 9 with a long looped descender is a separate sign (ss). Kept Q. |
| 13 | `B A 6 c f` | `B TH S c gf` | σ (p). Kept mine. |
| 14 | `[pò] ET Z S 5 P` | `[però che] Z eo pb P` | The "ET" is the clear abbreviation for "che". Kept mine. |
| 14 | "disposto sia" (clear) | "di questo sia" | Clear hand; mine. |
| 17 | `a i c 5 / L p / P` | `a i c Z¦5 N ^ p N P` | The sixth sign is ⊥ (h), not L. Kept mine (qualchuno). |
| 17 | `5 7 d 5 i 9 7` | `pb 7 gd Z¦5 11 Q 7` | Two strokes (a), then looped 9. Kept mine (pigliassi). |
| 18 | `S v 9 P` | `o v 4 P` | Plain o. Kept mine (sinistro). |
| 19 | (reading "haverì") | Phase A `L 11 p m Q 7`, now `^ 11 p m Q 7` | **Changed against my own Phase A.** Re-crop shows the base stroke extending left of the stem, the same form as the h in "chi" two signs earlier. The previous pass had h here; the calibration test showed I confuse these two. |

## Docs 113 and 115: readings compared

No earlier transcription existed. Differences in reading that matter:

- 113r l.3: previous "nipote del Re"; mine "nipote de la pr[efa]ta duchessa [Bona]". The group after "nipote" is `Z eo 5 11` (d-e-l-a), then σ 9 with a raised v c, then the same five-sign group as "duchessa" in lines 2 and 4.
- 113r l.1 and passim: previous "io"; mine [il Re] (same sign as 112 l.4).
- 113r l.7: previous took "et io comprendiamo" as clear; I read the clear words as "che è Camprianino(?)" (the courier's name) and the cipher as "dice che in camino tra Parma".
- 115r l.9: previous "fatte(?) … dieci(?) luoghi"; mine "darvi faccenda di più luoghi" (σ 6 ı = p-i-u).
- 115r l.10-11: previous "promesso fa… ciar"; mine "promesso Fae|nza".
- 115r l.11: previous "Por…"; mine `b P 4` with raised `6 P` = Lor[en]zo.

## After calibration

The calibration test (REPORT.md) showed two confusions in my own eye: L for ⊥ (s for h) and plain b for flagged b (l/z for p), four confident errors in 38 words. I did not re-crop every such sign in the targets. Instead `signs.tsv` now gives each of these signs the other's value as an alternative, so the decoder treats them as ambiguous everywhere and no word containing them is counted strict. With that change the lexicon corrects both kinds of calibration error on its own ("havere", "pro"). In the targets it changed no reading except to open one alternative: 112r l.20 "saria suo danno" could be "haria suo danno".

The person-sign check against the glossed letters: the group in doc 110 c.250r that looks like the long-tailed 2 is a plain 2 (b) followed by raised cipher letters and glossed "B[ernar]do"; it is an abbreviated name in letters, not the same sign. I found no gloss for the long-tailed sign, so its values stay contextual.
