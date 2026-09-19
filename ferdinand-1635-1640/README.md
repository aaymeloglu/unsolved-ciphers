# Ferdinand correspondence, 1635 / 1640

**Both letters are now readable, with explicit residual glyph and copying problems.** R1889 (16 November 1635) concerns imperial winter quarters at Trier. R1890 (22 February 1640) concerns recruitment in the Westphalian Circle, Hatzfeld's dispatch to Cologne, and a request for 100,000 florins. The draft/cipher relationship was already cataloged by DECODE; no discovery or first-solve claim is made.

The 1635 reconstruction has 51 mapped labels. The final comparison passage agrees with the draft at **93/95 letter positions**; the remaining signs occur in the securely readable words *civitas* and *iam*. On the image (18 September 2026) both are plain 7 and 6 signs, so the discrepancy is the copy's, not the transcription's. See [the final discrepancy check](FINAL-CHECK-1635.md); the original experiment is retained in the validation notes.

Applied **unchanged** to 1640, that map covers 416 of 779 imported cipher units. A subsequent **60-value supplement**, mostly syllables, makes both pages readable **without changing any earlier assignment**. It covers 779 of 782 units in the separately reviewed transcription; an obscured sign and two occurrences in Hatzfeld's name remain unmapped. Coverage is not accuracy: singleton assignments and several malformed words remain qualified. This supports a shared observed alphabet and cipher system, not identity of every unused historical key entry.

## Read the results

- [1635 Latin, English translation, and apparatus](READING-1635.md)
- [1640 Latin, English translation, and apparatus](READING-1640.md)
- [Frozen-key validation, unchanged transfer, and subsequent supplement](VALIDATION.md)
- [Sources, attachments, scholarship, and novelty limits](SOURCES.md)
- [1634: why it was separate and available evidence](1634-ASSESSMENT.md)
- [Key overview](KEY.md), [1635 occurrence evidence](key-evidence.tsv), and [1640 additional mapping evidence](key-1640-evidence.tsv)
- [Transcription conventions](transcriptions/README.md), [R954 draft](transcriptions/R954-draft.md), [R1889 cipher](transcriptions/R1889-working.txt), [R1890 imported cipher](transcriptions/R1890-working.txt), [R1890 reviewed cipher](transcriptions/R1890-reviewed.txt), and [review amendments](transcriptions/R1890-review.tsv)

## Reproduce

Python 3.12 with `cipherkit` (installed by `uv sync`). Run from the repository root:

```sh
uv run python ferdinand-1635-1640/verify.py
```

This checks the committed artifacts without modifying them. For regeneration: `uv run python ferdinand-1635-1640/verify.py --write`.

These regenerate the frozen-key audit, unchanged-transfer outputs, evidence tables, glyph-review layer and supplemented 1640 outputs. `key-v1.json` is hash-checked. The expanded 1635 map is reconstructed from its alignment tables; the 1640 supplement asserts that no old assignment is overwritten. [Literal outputs](results/) retain unknowns and malformed words. The readable editions explicitly distinguish editorial repairs.

## Remaining gaps

- **1635:** an image check of 18 September 2026 (see READING-1635.md notes 1, 2, 7, 11, 13) settled what was transcription and what was not: *hiberna* (P2.L03) was a transcription slip, `1 11` read as `i u`, and now decodes literally; the four *m*-position `6`s have the same form as the *e*-position `6`s, so the copy itself writes *e* for *m* there; the 7s in *civitas* and *locisque* are plain 7s; *hactenus* lacks its *a* on the page. Still open: the unexplained arc under *civitas*, the marked p sign, the 9/g sign in *provisum*, the doubled *n*, and draft/copy wording differences. Exact deletion/revision order in the draft is incomplete.
- **1640:** one obscured end-of-line sign; value of 14 in *ha…feldius/ii*; a few singleton groups and context-assisted glyph reviews; apparent errors *igitua*, *materi*, *expredse*. There is no independent 1640 plaintext witness. These do not leave a substantive paragraph unread.
- **Prior publication:** no exact earlier target solution was located in the checked sources, but novelty remains unestablished. An archive inventory lists nineteenth-century copies of this correspondence; their contents were not inspected. A matching historical key sheet has not been recovered.

Original DECODE attachments are retained with attribution. Transcriptions are source-assisted, not blind. Manuscripts were accessed with the DECODE project's permission; images are not redistributed. Published 18 September 2026. Manuscript images are not redistributed.

Research completed to the limits of the available evidence, 18 September 2026. Earlier statements that 1640 was unread are superseded.

## Evidence grades

Per the repository [conventions](../CONVENTIONS.md), each cipher unit has a machine-readable grade in `results/R1889-token-grades.tsv` and `results/R1890-token-grades.tsv`:

| Letter | C: draft-derived value | M: uncertain/contextual | I: reviewed source amendment |
|---|---:|---:|---:|
| 1635 | 447 | 16 | 0 |
| 1640, reviewed stream | 416 | 347 | 19 |

C records the origin of the mapping in the 1635 plaintext draft; it is not a claim of an independent 1640 plaintext witness. The 60 context-recovered 1640 values remain conservatively graded M because no matched-control cryptanalytic S claim is made. This includes strongly corroborated syllables as well as provisional singletons. I marks the 19 output units affected by 16 explicit source-review amendments. These grades describe the literal stream; bracketed editorial restorations in the readable Latin are supplied readings, documented separately in the apparatus, and are not counted again as literal cipher units. No H or S grade is claimed. No language-model corpus was used.
