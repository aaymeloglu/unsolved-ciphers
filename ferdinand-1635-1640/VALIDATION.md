# Key selection, validation, and transfer

## What was frozen

`key-v1.json` was selected exclusively from the first cipher paragraph, R1889 P1.L05–09, aligned to R954 D1.09–15. Its 42 assignments are supported by the A-series occurrence references in `transcriptions/training-alignment.tsv`. Its immutable SHA256 is:

```text
5803d66e26980adc1e9fd1c0571c86b2a09488d636969a1df74f71f8c846a9e5
```

Only plaintext u/v is normalized to `u`. Cipher case, digits, and word-like groups are never normalized by the decoder. Training word breaks are alignment aids, not a claim that the manuscript encodes spaces.

## Held-out 1635 test

The next cipher paragraph, after clear “Verum cum”, was not used to assign the initial mappings. Test spans V01–V12 run from *civitas* to *munita*, omitting intervening cleartext. Their first-pass ciphertext, draft expectation, and source locations are in `transcriptions/heldout-1635.tsv`. The frozen key gives:

- **87 matches / 95 positions (91.6%).**
- **5 unknown positions:** symbols `30`, `9`, `e`, `19`, `2`.
- **3 mismatches:** the 7-like mark in *civitas*, the 6-like mark in *iam*, and the first-pass second symbol in *praesidio*.

This is connected-text support for most of the alphabet, not complete error-free validation. Of 90 mapped positions, 87 agree (96.7%). Individual matches are not statistically independent; these percentages are an audit of this documentary alignment, not a cryptographic confidence probability.

```text
V01 ciuitcs              expected civitas
V02 treuirensis          expected trevirensis
V03 iaeindeaducentis      expected iam inde a ducentis
V04 annis
V05 sub
V06 stetprotectione
V07 at⟦30⟧ue
V08 a⟦9⟧eius
V09 ⟦e⟧i⟦19⟧ite
V10 ⟦2⟧uerit
V11 paaesidio
V12 munita
```

The apparent error in V11 was checked against the image: XZ's `20 0 0 m` should read `20 c o m`. This was corrected **only in the reviewed working transcription**, retaining the first-pass holdout unchanged. The symbol `o` was then assigned `a` using the draft; that assignment is explicitly post-validation. The other two mismatches have not been silently repaired. In particular, `6=e` works in the initial training but is not safe at every similar-looking mark in the rest of the letter. Distinguishing b-like from six-like shapes was checked on the photograph on 18 September 2026: the four *m*-position signs and the *e*-position signs have one form, so the difficulty is in the copy, not in the transcription (READING-1635.md note 2). A second transcription correction of the same kind as V11 was made at P2.L03 (`i u` → `1 11`, *hiberna*), outside the held-out spans.

The V-series draft expected strings were read/collated after selecting the initial alphabet. No V/F occurrence appears in the v1 evidence lists. The overall manuscript transcription was source-assisted, not blind: XZ's attached ciphertext was inspected and used, with selective scan checks. This limits claims of independent paleographic verification, not the separation of key-selection and holdout passages.

## Later expansion

`key-v1-extended.json` adds five assignments using E-series evidence outside the holdout (47 total). `key-expanded-1635.json` then adds four more using F-series evidence (51 total). F-series evidence includes the heldout paragraph after the original test. **The expanded key is not independently validated by re-decoding the same passage.** It uses no 1640-derived assignments.

The expanded map covers 461 of 463 cipher units in the reviewed R1889 working transcription. This is **lookup coverage**, not textual accuracy: it includes disputed 6-like occurrences and values which produce malformed words. `p^` and `u` remain unmapped. The Latin reading explicitly marks the required restorations. No nulls, syllables or nomenclature entries were inferred for R1889.

## Unchanged transfer to R1890

Both v1 and the expanded 1635 key were run unchanged on the **whole supplied 1640 ciphertext transcription**, 779 units across two pages. Unknown multi-letter units, for example `op`, `pli`, `tis`, `up`, are kept intact. Splitting them into known single-letter symbols would change the hypothesis and is not done.

| Key | Mapped units | Unknown units |
|---|---:|---:|
| Frozen v1, 42 assignments | 366 | 413 |
| Expanded from 1635 only, 51 assignments | 416 | 363 |

The expanded transfer contains recognisable fragments such as `acquaein` (P1.C06), `prae` (P1.C18), `atquehuic` (within P1.C22), and `quid…quamex` (P2.C09). These offer **partial alphabet compatibility**, but they do not produce a sustained reading sufficient to validate a full shared key. Unit coverage alone cannot establish that the same values are correct in 1640.

Example, P1.C06, with the expanded key:

```text
cipher: 42 23 31 ip c? up 42 15 22 ep 20 plu_. d n x 33 23 n p 24 22
literal: ⟦42⟧us⟦ip⟧⟦c?⟧⟦up⟧⟦42⟧in⟦ep⟧p⟦plu_.⟧macquaein
```

`c?`, `plu_.`, and other marked groups are retained from the attachment; the import is deliberately conservative. Several source units such as `l/z?p` combine apparent adjacency/ambiguity and need manual review. An unknown is not automatically a distinct historical symbol. Source-row identifiers Cnn preserve the attachment's ciphertext rows; they are not claimed to count all physical manuscript lines.

**Initial transfer conclusion:** The unchanged map alone gave only partial alphabet compatibility. That was the state before the separate supplement below; it is preserved as the actual transfer test, not retrospectively promoted to a full decipherment.

## Post-transfer 1640 reconstruction

The productive step was treating `pla/ple/pli/plo/plu` as vowel-indexed syllables, then recognizing `41–54` as *le li lo lu na ne ni no nu ra re ri ro ru*. The `ap/ep/ip/op/up` family supplies *ca ce ci co cu*, not five strings of alphabetic cipher letters. Repeated contexts such as *electore*, *circulo*, *collectionem*, *dilectione*, *quatenus*, *commissariorum* and *consignari curare velit* support one coherent map through both pages.

`key-1640-supplemented.json` adds **60 assignments** to the 51-entry 1635 map, changing **none** of its values. Every addition has selection context and occurrence references in `key-1640-evidence.tsv`. Singleton values are marked provisional. The unobserved presumed number 40 is not inferred into the key. Symbol 14 remains unassigned rather than selecting a convenient spelling of Hatzfeld.

Image review makes 16 documented amendments in a separate `R1890-reviewed.txt`, with the imported stream unchanged. Three composite source units are split into visibly adjacent signs; therefore the reviewed stream has **782 units**, compared with 779 imported units. The supplemental map covers **779/782**, with `?` and two `14` occurrences unknown. It also produces apparent errors *igitua*, *materi*, *expredse*, which remain in literal output. See the Latin apparatus for visible editorial repairs.

This full reading strongly supports continuity of the observed alphabet and cipher system between the letters. It does **not** prove that the unobserved syllabary was present in 1635, or that every entry of the complete historical keys was identical. The 1640 additions were selected using this very letter; no independent 1640 plaintext or blind second validation passage is claimed. Same-letter repetitions are corroboration, not a second holdout experiment.

### Accounting correction

The earlier report said 780 imported 1640 units, with 364 unmapped under the expanded key. A decoder bug ended a cleartext island at the inner brace in `{De catero eidem Dil^{oi} Vra}` and counted `Vra}` as a cipher unit. The balanced-brace parser now correctly reports **779 / 363**. Mapped totals, ciphertext bytes, key hashes, and the entire 1635 holdout result are unchanged. This correction concerns the parser, not the cipher.


## Reproduction

From the repository root, with Python 3.12 and `cipherkit` (installed by `uv sync`):

```sh
uv run python ferdinand-1635-1640/import_1640.py
uv run python ferdinand-1635-1640/decoder.py --check
uv run python ferdinand-1635-1640/extend_1640.py
uv run python ferdinand-1635-1640/decoder.py ferdinand-1635-1640/transcriptions/R1889-working.txt --key ferdinand-1635-1640/key-v1.json
uv run python ferdinand-1635-1640/decoder.py ferdinand-1635-1640/transcriptions/R1890-working.txt --key ferdinand-1635-1640/key-expanded-1635.json
```

The audit regenerates literal files, per-occurrence holdout results, lookup coverage, and `key-evidence.tsv`. It checks the frozen hash, reproduces every key assignment from its alignment table, checks the holdout totals, and verifies that unknown groups and case distinctions survive unchanged. Expected totals are assertions against this saved research checkpoint, not a replacement for source inspection.

The separate supplement script checks that no old mapping is overwritten, verifies that every new label actually occurs, logs all review edits, and regenerates both imported and reviewed supplemented literal outputs.

Of the 51 inherited labels, 46 actually occur in the reviewed 1640 stream; `0`, `1`, `2`, `h`, and `i` do not. Retaining those five values in the supplemented JSON is not a 1640 validation of them.

## Final reading check

The current expanded map plus the documented *praesidio* image correction gives **93 matches / 95 positions**, with only V01:6 (*civitas*) and V03:3 (*iam*) disagreeing. `decoder.py --check` regenerates `results/1635-current-passage.tsv` separately from the original test. [The final check](FINAL-CHECK-1635.md) records the evidence for all six resolved positions and the two remaining glyph issues.
