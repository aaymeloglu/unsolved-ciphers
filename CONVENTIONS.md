# Conventions

How work in this repo is recorded, so that a reading can be trusted at the level it deserves and
a negative result says something. Adopted 2026-09-18 after comparing our first month against
[dbourdeau/cyphersolver](https://github.com/dbourdeau/cyphersolver), whose per-group grading and
mandatory controls we take over; grades H, C, M, I mean the same thing in both repos.

## 1. Every claimed reading is graded per group

| Grade | Meaning | Examples here |
|---|---|---|
| **H** | Read from a primary key source: the group is looked up in a surviving key or table | Ottobon groups found in Ziffra prima (DECODE R1789); Starhemberg groups found in the 1752 Prima/Secunda tables |
| **C** | Read from known plaintext: a contemporary decipherment, a printed sibling, a minute in clear | Royalist 1646 values fixed from Evelyn's printed decipherments |
| **S** | Determined by cryptanalysis alone, and only claimed alongside a control (section 2) | Forster 1644: 204 of 207 tokens under a key found ciphertext-only, key-shuffle permutation z = 11.2 |
| **M** | Uncertain: alternative readings, unread signs, groups absent from the key | Ottobon `{a84/a94}` and `?` slots; Starhemberg groups the tables do not contain |
| **I** | Inferred or supplied: editorial restorations, emendations, repairs of the ciphertext | Ottobon *sole[va]tione*; Forster's three emended tokens; every Starhemberg digit repair |

Machine-readable outputs carry the grade per token (`decode.py` in each folder); READMEs give the
counts. A reading with no H or C tokens is a cryptanalytic result and its README says so. A
table of grades is not a claim about the handwriting: transcription accuracy is a separate
question, stated separately.

## 2. A negative result is reported only next to a matched control

Before saying a target resists an attack, run the same attack on a synthetic text of the same
length, alphabet, symbol count and cipher design in the target's language
(`cipherkit.controls.matched_control`), and report both numbers. "The annealer reads 5 of 6
matched 134-letter controls but not the target" is a result. "The annealer found nothing" is not.
Permutation z-scores accompany any claimed reading that rests on statistics, and the report
names the null: `permutation_z` shuffles the tokens (is the order informative under this
key?), `permutation_z_key` shuffles the key's values among the glyphs (is this key better than
a relabelling of the same glyphs?). The two are not comparable with each other.

## 3. Check the printed editions before calling anything unsolved

Before a campaign, search the cipher's name, then the sender's standard correspondence edition,
then the comment threads of the list posts. Barney 1863 was the first search result for its
name (solved on Reddit a month earlier); Richelieu 1629 was in Avenel 1858 with the plaintext in
footnotes; Forster 1644 had been read by Lasry and Biermann; Davison 1584 and Worcester 1526 were
in the calendared state papers. None of the source lists had caught up. The order is: the
cipher's name in a search engine, the sender's *Lettres* or *Correspondance* on the Internet
Archive, the calendars and state-paper series, the source list's comment thread, then DECODE
and the archive catalogue.

## 4. Dates are absolute, and status is tracked in one place

[TARGETS.md](TARGETS.md) holds every target touched, with a status from this set:
`solved` · `partial` · `open` · `closed-negative` (controls pass, target does not) ·
`found-solved` (already in print or online; the source list is stale) · `blocked` (needs an
image, a login, or an archive visit). Notes say "18 Sept 2026", never "yesterday" or "recently",
so that "since" claims can be checked against the source lists' last-modified dates.

## 5. What a target folder contains

- `README.md`: sources with links, what is established, what is inferred, the failure log, the
  grade counts, and which corpus the language model was built from (`cipherkit.corpora` id).
- The ciphertext as transcribed, never silently repaired; proposed repairs live in their own file.
- A `decode.py` or `verify.py` that reproduces the reading from the transcription and key with
  the standard library plus `cipherkit`, and exits non-zero if the committed reading is stale.
- Images only where the licence allows. DECODE images are never redistributed.

## 6. Public pages state the current account

Reading pages, summaries, and their tables must stand on their own for a new
reader. State current beliefs and uncertainty directly; do not refer to earlier
versions of the page or narrate the withdrawal or correction of absent claims.
Keep revision history in audit files and Git. Preserve relevant provenance,
competing interpretations, independent prior work, and experimental controls.
See `AGENTS.md` for the site-wide editorial and regeneration rule.
