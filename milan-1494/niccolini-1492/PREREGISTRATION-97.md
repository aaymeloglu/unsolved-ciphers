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
