# Angelo Niccolini, Milan and Pavia, 1492-93: four bare cipher passages

**Status: partial, 15 November 2026.** Four short cipher passages in letters of Angelo Niccolini, Florentine envoy at the Milanese court, to Piero di Lorenzo de' Medici (ASF, Mediceo avanti il Principato LXXIV). They are in the same embassy cipher as the Ridolfi and Alamanni letters in [../](../README.md), but Niccolini's sign values and his list of name numbers differ in places from the key sheet MAP LXXII 183. Neither of two pre-registered held-out tests met its bar. The readings below are proposals at the stated grade.

| Passage | Archive | Cipher words | strict / +forced / +lenient | Unread |
|---|---|---|---|---|
| Pavia, 3 Aug 1492, postscript | LXXIV doc. 42, c. 90r | 30 | 5 / 14 / 25 | 2, plus 3 doubtful |
| Pavia, 20 Aug 1492 | doc. 49, c. 104r | 4 | 0 / 2 / 3 | 1 |
| Vigevano, 21 Dec 1492 | doc. 81, c. 177r | 8 | 3 / 6 / 7 | 1 |
| [Jan 1493], postscript sheet | doc. 90, c. 200r | 4 | 0 / 1 / 4 | 0 |
| **Total** | | **46** | **8 / 23 / 39** | **4, plus 3 doubtful** |

Reading, translation and word table: [reading.md](reading.md), [reading-words.tsv](reading-words.tsv); tiers and counts checked by `python3 milan-1494/niccolini-1492/verify.py`. The read fractions are coverage, not accuracy.

## What the passages say

- **c. 90r.** Lodovico tells Niccolini that [the King] keeps urging "el Re di Francia che lievi dal governo [Lodovico]", and that the King of France answers that he wants to find out whether "he" (presumably the young Duke) is fit to govern, and ("per(?) non sendo apto", the *per* doubtful) wants to be the one who keeps [Lodovico] in place. A name number 15, not Lodovico, "non è ancora ben resoluto".
- **c. 104r.** Talk of commissions (or bets) made in Florence "in sul papa" (Alexander VI was elected on 11 August), "messer Giovan Angelo [...]".
- **c. 177r.** The obedience embassy will drag on, "né [Lodovico] havervi tanta parte quanta e' dimonstra".
- **c. 200r.** Niccolini had Lodovico (named in clear) sounded out by "frate Domenico da Ponzo".

## Name number 22 = Lodovico

Niccolini's own glossed letters gloss **22** as "S. L.o" eight times (docs 6, 59, 62 and 72; [work/table/align.tsv](work/table/align.tsv)) and **24** as "As." (Ascanio) three times. On sheet 183, 15 is S. Lodovico, 22 is S. di Pesaro and Ascanio is 56. Ridolfi's letter LXXIV 107 has the same gloss ("S. Lco") over a 22, so Niccolini and Ridolfi used a name list that is not the sheet's; in Alamanni's letter 22 fits Lodovico by context only. That list's 15 is not glossed anywhere we looked.

## Tests

Both are recorded as they came out; protocols and hashes are in the pre-registration files.

| Test | Key or table | Reference | Agreement | Best of 1,000 shuffles | Bar | |
|---|---|---|---|---|---|---|
| c. 176r (doc. 81, 21 Dec 1492), [PREREGISTRATION.md](PREREGISTRATION.md) | key.json at 26378c7, unchanged | the gloss on the leaf | 0.358 | 0.247 | 0.85 | failed |
| doc. 97 (20 Jul 1494), [PREREGISTRATION-97.md](PREREGISTRATION-97.md) | Niccolini's table, frozen at 0f87f37, key fallback | the gloss, 69% legible | 0.527 | 0.306 | 0.80 | failed |

- **c. 176r.** The gloss agent could read only parts of the gloss at 1272 px, and its reference has 105 letters against 147 output characters. Where both are legible, output and gloss agree on "fratello" (B8) and "cardi" (B10), and partly on "nftura?mente" against "natural??te" (B7). The misses come from signs whose value differs in Niccolini's hand (the ff and o signs, which the key makes nulls), from name number 24 scored as letters (B1, B5, glossed "As."), and from unglossed signs scored as cipher (B9, B11). After this test c. 176r became an exemplar.
- **Doc. 97.** The rule written first could not reach its bar because only 69% of the gloss is legible. It was amended before any transcription existed (illegible letters became free positions; see the amendment). Doc. 97 turned out to be of July 1494, not 1492-93. Where both are legible, output and gloss agree on phrases such as "trovar[e] l[o] arcivescovo" (B17, B20), "principe di Sal[erno]" (B30), "numero a[p]punto" (B24) and "prime" (B10). The misses are systematic: the transcriber's merged l/d and i/p classes; a sign labelled δ (*per*) that stands where the gloss has *ll* in "della" and "delle" (B10), with ∂, the table's ll, as the transcriber's own alternative; and the transcriber's tailed o (N13), which the frozen scorer counts as unidentified and the gloss shows as e.

Both scores are far above the shuffled keys, so the system is the right one. Neither reaches the bar, so the table does not yet read Niccolini at the standard of a secure reading.

## Method

1. A masking agent cropped the cipher lines and painted out the gloss on the test leaves ([blocks.md](blocks.md), [heldout97/blocks-97.md](heldout97/blocks-97.md)).
2. Transcribers worked from crops only, with a value-free sign inventory under random neutral labels ([signs-novalues.md](signs-novalues.md); [alias.json](alias.json) maps them back, fixed before transcription). The four bare passages were transcribed twice, independently: 148 of 176 labels agree, and every block has the same sign count in both passes.
3. A table agent built [niccolini-table.json](niccolini-table.json) from 319 sign-gloss alignments in docs 6, 21, 59, 62, 72 and 81 c.176r, without doc. 97 ([work/table/NOTES.md](work/table/NOTES.md)). Values glossed twice or more are grade C; single cases are S.
   How blind this was: the transcribers were told not to open key.json, alias.json or the readings, and said they did not, but those files sat in folders they could reach. Pass B was given pass A's c. 176r label sequences as exemplars, so the two passes share A's conventions for this hand and their agreement is not fully independent. The session that wrote the protocols and scored had seen c. 176r, gloss included, at page size and knew the key.
4. A reader agent reconciled the two passes sign by sign against the crops, decoded with [decode.py](decode.py) (table first, then key.json), and graded each word by the rules in [../README.md](../README.md).

Where the table departs from the sheet: Niccolini's i is the 6 and his p a σ (they look alike at this resolution); the ʒ/b-like hook class holds both l and d; the e-like loop and the dash-with-loop are o, not nulls; ## inside a word is ff; a barred b is p (fitted in apto, parte, Ponzo); a circle with a dot is *papa*; H with a bar, followed by 9, is *Re*.

## Open points

- c. 90r: *lievi* (lenient), the two unread groups before "se apto", the second and third *apto*, and whether the transcribers' clear "et" groups are *che*.
- The closing sign N8 (stem with a raised o) at the end of the c. 104r and c. 177r runs; the surname after "Giovan Angelo".
- 15 on c. 90r is unidentified.
- The table has no glossed case for h, z, b, *che*, *per* or *non*. Docs 72 c.147r, 37 c.83r, 62 c.133r/134r, 78 c.163v-164v and 21 c.43r-44r carry gloss not yet aligned.
- A third held-out test should first split the l/d and i/p shape classes in the transcribers' labels.
- Images are 1272 px, the most the ASF server gives. They are listed with hashes in [images.tsv](images.tsv) and not redistributed.
