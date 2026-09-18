# Transcription layers

Manuscript images were accessed with the DECODE project's permission; images are not redistributed. XZ/AP source attributions and attachment provenance are documented in [sources](../sources/README.md).

- `../sources/R1889-DECODE.txt` and `R1890-DECODE.txt` preserve XZ's attachments verbatim, including uncertainties, malformed cleartext and swapped metadata labels.
- `R954-draft.md` is a manual working reading of the main draft, plus selected cipher-margin excerpts. Cancelled/revised passages and untranscribed gaps are explicit.
- `R1889-working.txt` is a **source-assisted, selectively image-checked** transcription, not an independent blind transcript. It preserves cipher rows, punctuation, uncertainties and clear/cipher boundaries. `{...}` indicates cleartext. Source superscripts are simplified in cleartext; the attachment/facsimile preserves the originals.
- `R1890-working.txt` is a conservative, reproducibly normalized import of XZ's unit spacing, not a full new paleographic edition. Both manuscript pages were viewed. Multi-letter code groups and uncertainties survive. `import_1640.py` reconstructs this file from the attachment.
- A-series alignments selected v1. V-series spans were withheld. E-series expands from other passages; F-series expands after validation. Occurrence references such as `A12:4` mean the fourth token in that row, not a manuscript word number. The row's evidence field locates the image and phrase.

## R1889 decisions relative to XZ

These changes are visible in the working layer only. The source attachment and first-pass holdout have not been overwritten.

| Place | Decision | Basis / limit |
|---|---|---|
| Cipher throughout | Convert spaces inside a numeral such as `3 4` to token `34`; split alphabetic runs into individual cipher letters where required by the established 1635 alphabet. | Explicit one-letter homophonic model, tested by repeated mappings. Does not apply to the syllabic groups in 1640. |
| L05 opening | `0 4`, not a single `04` code; `33 23 l 3`; consistent token boundaries through *attinet*. | Draft *ad ... quod attinet*, visible glyph order, and repeated digit-letter correspondences. This is model-based segmentation, not proof that every glyph was originally space-separated. |
| L07 archiepiscopatu | `n c 7 1 h ...` rather than an invented `71` code. | Draft alignment; 7=c elsewhere. The new 1=h is training evidence with less independent confirmation than frequent symbols. |
| L07 end | `z 7`, not numerical 27. | Draft *ac*; z=a and 7=c corroborated elsewhere. |
| L11 *civitas* | Keep `...37 7 31` and record arc beneath final signs. | Do not substitute n/z/0/t (a-symbols) just to make Latin. |
| L15 | `20 c o m`, replacing XZ's `2 0 0 0 m`. | Enlarged target and draft-margin comparison show c and o, not two zeros. First-pass V11 remains unchanged for the audit. |
| L20 | `p^` retains the source's superscript mark as a distinct, unmapped unit. | A p-like e-symbol is likely, but the mark's function was not established. |
| L24 end | `39`, not separate 3 and 9. | XZ's visual/unit spacing is inconsistent here; target shows 39, and *ex* agrees with the draft. |
| L26 / P2.L02 final | `25`, removing XZ's tentative question mark. | Target signs have the same 25-form as other examples. Output *sustentationem* and *dictis* corroborates, not substitutes for, the image reading. |
| P2.L03 *difficulter* | `5 2`, not a single 52. | Two glyphs are visible; draft and established 5=f give ff, with new 2=f confirmed by *fuerit* after validation. |
| P2.L03 end | `7 f 22`, replacing source's `7 f 2?`. | Source image and draft margin show two 2-forms; continuation *con-cedi*. |
| P2.L03 *hiberna* | Retain source `i u 9 p q 32 z`. | Initial i/1 and u/11-like glyphs unresolved. No invented mapping u=i. |
| All 6-like signs | Keep baseline label `6` and baseline e-value, with warnings. | b/6 distinction or encipherment error unresolved. Reading edition supplies m only with visible editorial brackets. |
| P1.L25 *provisum* | Keep `9` in target working text; record g alternative. | Draft margin appears g; target shape is not securely resolved. |
| Cleartext | Correct obvious XZ readings such as *Puibus* → *Quibus*, *Cœsasci* → *Caesarei*, *Cui de essi*** → *Cui de caetero*; regularize ae/ligatures and abbreviation typography. | Scan check, draft comparison. This is a reading transcription of cleartext, not a letter-form facsimile. Original attachment remains available. |

A shared apparent error in draft margin and target is not an independent second decipherment. The margin may be the source of the fair copy. More complete independent glyph checking could revise the token inventory and coverage totals.

## R1890 post-transfer review

`R1890-working.txt` remains the exact conservative import. `extend_1640.py` creates a separate `R1890-reviewed.txt` and a per-occurrence `R1890-review.tsv` (16 amendments). Both pages were compared with I9352/I9353. The log records changes and confidence; these are context-assisted, not blind readings. Unknown `14` and the obscured first-row ending remain intact.

The 1640 added-value evidence uses positions in the **reviewed** row, counting cipher units and excluding punctuation/cleartext, e.g. `P1.C05:2`. The review log instead uses the **source** row's whitespace-unit position, before any split; its column explicitly says `source_position`. This difference matters after splitting `l/z?p` or `l/z?6`.

Cleartext islands may contain nested superscript braces. The decoder now handles those correctly; an earlier off-by-one 1640 coverage count came from counting `Vra}` as ciphertext. No source text was changed to fix this parser bug.
