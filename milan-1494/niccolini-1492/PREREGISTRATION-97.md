# Second held-out test: Niccolini's table on MAP LXXIV doc. 97 (c. 222r-v, 232r-v)

Written 15 November 2026, before any image of doc. 97 has been opened by anyone in this work (the table agent was
told not to open it; the images were downloaded on 15 Nov with the rest of the filza and not viewed).

## Fixed inputs
- Table: niccolini-table.json at commit 699dce6, sha256 dc1268aa8f7552f05e9e898e9e951c3bebd873c251c34f8240dbedf6717bd39c, built from docs 6, 21, 59, 62, 72 and 81 c.176r only.
  Fallback for labels not in the table: key.json at 26378c7 via alias.json, as decode.py does (sha256 c276fa180d56c2abc6901660876d52323465e1c6dbc0154036a63e7524a83008).
- Locating, masking and gloss reading: one agent (it sees the gloss; it does not see the key, the table or any
  transcription). Block extent = the cipher signs that stand under a legible gloss, so unglossed tails are not
  scored. Name numbers and word signs are excluded on both sides (the agent marks them; the scorer drops them).
  Illegible gloss letters are written '?' and the block's gloss is scored only on its legible letters: a '?' is
  dropped from the reference AND the reference length used in the denominator is the legible length.
- Transcription: the same blind transcriber as c.176r and the bare passages (no key, no table, no gloss; masked
  crops only), its labels as before. Frozen (sha256 below) before decoding.

## One measurement
Character agreement, score.py rules (any listed value matches; global alignment per block; matched /
max(output length, legible reference length), summed over blocks), with the table+fallback value sets in place of
key.json. 1,000 shuffles of the value sets among the labels used. Bar 0.80 (lower than 0.85 because the
reference is a gloss read at 1272 px, not a printed text; set before the data). Reported whatever it is.

## Frozen inputs
(appended at freeze)

## Amendment (15 Nov 2026, before any transcription of doc. 97 exists and before anything was scored)
Found when the gloss was read: the gloss is a running decipherment over each whole cipher line, not letter over
sign, and only 902 of 1,314 gloss letters are legible (69%). Under the rule above (a '?' dropped from the reference
while the output keeps its full length) a perfect table could not score above about 0.69, under the 0.80 bar. So:
- Blocks are whole cipher lines (32 blocks: 26 on c.222r, 6 on c.222v); the gloss agent found no unglossed tail and
  could not tie name or word signs to positions, so nothing is excluded on either side.
- Scorer: heldout97/score97.py (sha256 d5412bce551976db4fa704237fb35dd31f224310ffd3f454f1b97c37d23cd579). An illegible letter '?'
  stays in the reference as a free position: it may take one output character or none at no cost, never counts as
  a match, and an output character on it leaves the denominator. Per block: matched / max(output characters not on
  a '?', legible reference letters). Otherwise as score.py. Value sets from niccolini-table.json with key fallback.
- Bar unchanged: 0.80. The writer is Niccolini, but the letter is of 20 July 1494 (dateline "die xx Julij 1494",
  endorsement "a di 22 di luglio"), not 1492-93: it also tests whether his table holds two years later.
- reference-gloss-97.tsv sha256 814b74f9b59a7190f4809b5ee1d8cd727e530c7887cdb91f2912f5d3d37a36f5, fixed now.
- heldout97/transcription-97-neutral.tsv sha256 fc6d1afcd46d1f41f5fe4287dc039869141d62eeb5f88b917ac9483e4ef458a9 (1,246 signs, 32 blocks), frozen before scoring.

## Result (15 Nov 2026)
- Agreement 0.527 (first value only 0.482); best of 1,000 shuffles 0.306, mean 0.236. Bar 0.80: **failed**. Per block in heldout97/result-97.txt. Anything after this line is after the fact.

## Note on commit ids (15 Nov 2026)
Before the branch was first pushed, image crops were removed from its history, which changed the commit ids. The table commit cited above as 699dce6 is now 0f87f37; the file sha256s above are unchanged and are what identifies the inputs.
