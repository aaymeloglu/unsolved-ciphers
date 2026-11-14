> Audit file. Independent review of both readings by Codex, 13 November 2026, written before the corrections were applied. file:line references point to the research folder (R/ = ridolfi-1494/pass2/, A/ = alamanni-1494/pass2/), not to this repository; the crops it links are not redistributed. How each finding was handled is in ../AUDIT.md.

# Independent review of the 1494 Ridolfi and Alamanni readings

## Verdicts

**Ridolfi, docs 112/113/115: publishable as annotated partial readings after modest but material corrections.** The expanded key produces the tabled text remarkably consistently; this is real decoding, not merely an Italian paraphrase. However, **98.6% is proposed-reading coverage, not a demonstrated accuracy or secure-decryption rate**. Preserve the uncertain person signs and both doubtful words in 112; retain the two unread groups in 113; distinguish supplied spelling and abbreviation expansions from cipher letters. Replace the unmarked `uole → volle` change in the connected text. The six doubled-consonant values do not all have equally independent support.

- **112:** publish as partial. Keep `edicto` and `strignerebbe` doubtful; `[il Re]` and especially `[Duca o Lodovico]` remain contextual identifications. Print `Pav[i]a` if expanding cipher `paua`.
- **113:** publish as partial. **`nipote de la pr[efa]ta duchessa [Bona]` is well supported as an interpreted reading**, and substantially better supported than “nipote del Re.” The exact expansion `prefata` is editorial, not six recovered letters. Do not present the proposed personal identification or remembered genealogy as independent verification.
- **115:** publish as a provisional reading with no presently designated gaps, not as an independently verified 100% solution. `bb`, `cc`, and `nn`, abbreviation expansions, and the royal person sign remain material assumptions.

**Alamanni, doc 96: publishable as a partial, with the confidence labels and reproducibility defects corrected first.** Keep “voltare Genova,” “a manifesta vittoria,” and the clause about “la salute del re Alfonso,” subject to the qualifications below. **Do not publish 22 = Lodovico as established or sheet-derived.** A genuine contemporary gloss supports that interpretation in Ridolfi 107; transfer to Alamanni is probable but not proven. Downgrade contextual `rr` readings currently called strict. Retain uncertainty in `[in]dugarlo`, `andassi`, `havessi`, `mantello`, `ferla/farla`, and the trade-route gaps. The stated 80 proposed read words is reconcilable, but the 93-word denominator and strict/lenient split need a word ledger.

## Scope and audit record

No network was used. All review outputs are inside `review-codex-1494/`; source files were not modified. I inspected the key-sheet image, Ridolfi 107's gloss, the relevant 110 glosses, all four Alamanni leaf overviews, and enlarged crops from the original images. The itemized visual sample below comprises **15 cipher words in each of Ridolfi 112, 113, and 115, plus 25 in Alamanni: 70 total**. Ridolfi 113 includes recto and verso; Alamanni includes all three cipher-bearing faces. Its 220r overview contains clear text, so there is no cipher-word sample from that face.

This is a targeted audit, not a blind transcription or a random accuracy estimate. I had read the proposed readings before comparing the crops. Enlargement adds no source detail. “Matches” below means the visible sign sequence is compatible with the stated transcription, not that every ambiguous sign value or resulting word is independently certain. Clear text was checked where needed for the requested claims, not comprehensively collated.

Reproducible artifacts:

- [Exact-substitution audit script](audit_decode.py), [results](mechanical_results.txt), [Ridolfi candidates](ridolfi_exact.tsv), [Alamanni candidates](alamanni_exact.tsv), and [extra Alamanni key values](alamanni_extra_key.tsv). The script does not run either supplied decoder or its language model.
- [Visual sample ledger](visual_samples.tsv), [crop script](crop_review.py), and [crop coordinates](crop_manifest.json). Supplemental detail crops are identified at the relevant findings.
- [Alamanni count reconstruction](alamanni_table_count.tsv). This records the table's displayed grade units, not a proposed replacement count of the manuscript's unknown words.

References below are repository-relative `file:line` references. `R/` means `ridolfi-1494/pass2/`; `A/` means `alamanni-1494/pass2/`. Leaf:line follows the supplied editions, including their local cipher-line numbering for Ridolfi 113.

## 1. Mechanical decoding

### 1.1 Ridolfi: tabled readings mostly pass exact substitution

An independent parser joined continuation words in `R/transcription_final.txt`, verified their token sequences against `R/final_words.json`, and enumerated the alternatives in `R/signs.tsv` without collapsing consonants or adding letters. Among the **283 counted units**:

| Result | Units | Interpretation |
|---|---:|---|
| Stated literal reading is an exact candidate | 273 | Conditional on the expanded working key and the chosen alternatives; includes the two explicitly doubtful readings. |
| Contextual person-sign expansion | 7 | Four RC, three RD; a label in a reconstructed key is not independent evidence of identity. |
| Unknown sign supplied by context | 1 | `apresentarsi`, 113r:4: Y remains `?` in the sign file. |
| Declared unread | 2 | 113r:9 end and 113v:1 start. |

There were **no further exact-string mismatches in the tabled literal words**. This is stronger evidence of internal consistency than the supplied check, which normalizes away doubled letters, some h, and ct, and allows a word containing an unknown sign to pass its compatibility test (`R/finalize.py:29`, `:32`; `R/decode_lattice.py:11`). It does not establish the reconstructed key's correctness.

The eight `TH → non` substitutions and all six doubled-consonant mappings have already been installed in `signs.tsv` before tiering (`R/signs.tsv:39`, `:47`). The script therefore cannot test those hypotheses by showing that the resulting words decode.

### 1.2 Ridolfi: connected prose goes beyond the literal table

These changes need a stated normalization policy or explicit brackets. Most are plausible editorial readings, not reasons to reject the decipherment:

- **112r:4 `S 11 p c → paua`, then “Pavia.”** The absent i is acknowledged in `R/reconcile.md`, but not marked in the connected text (`R/reading.md:30`, `:51`). Use `Pav[i]a` in a diplomatic expansion.
- **112r:8 `gorni → giorni`; 113r:3 `figluolo → figliuolo`; 113r:5 `piglando → pigliando`; 113v:1 and 115r:11 `gouanni → Giovanni`.** Each adds an i not in the literal string (`R/reading.md:34`, `:53`, `:78`, `:80`, `:85`, `:96`, `:98`, `:130`, `:137`). Normalized spelling is legitimate if labeled; these are not additional recovered signs.
- **113r:4 `p P 5 m → uole`, but connected text “non volle.”** This is an unmarked tense/spelling intervention, not just u/v conversion (`R/reading.md:79`, `:96`; [crop](crops/113_L4.png)). Restore `non vuole`/`non uole` or explicitly justify an emendation.
- **`mta`, `prta`, `pierfranco`, `lorzo`** are abbreviated strings, not full names/words. The connected edition usually handles these correctly with `M[aes]tà`, `pr[efa]ta`, `Pierfranc[esc]o`, `Lor[en]zo` (`R/reading.md:77`, `:78`, `:85`, `:96`, `:98`, `:130`, `:137`). Preserve those brackets when quoting the result elsewhere.
- Single-to-double consonant changes such as `castelo → castello`, `quelo → quello`, `isabela → Isabella`, and `glanno → gl'hanno` are also editorial normalization. They must not be used retrospectively to prove that every special sign encodes a double consonant.

### 1.3 Alamanni: the archived transcription does not reproduce all final readings

`A/blind_transcription.tsv` is an earlier-stage artifact. It is not a complete final transcription. I tested all **60 archived runs**, using the working dictionary extracted as data from `A/lattice.py:9`, plus every recorded shape alternative. With the target strings specified in the audit script, 53 are compatible, two remain designated unread runs, and five fail exact substitution. These are run counts, not the edition's word counts. Some compatible targets are only literal fragments; three names are retained as `[22]`, not decoded as Lodovico.

| Place | What the saved signs permit | Additional operation in final reading |
|---|---|---|
| 220v:13, V13.1 (`A/blind_transcription.tsv:20`) | `edugarlo` is among the candidates, starting with cipher `m = e` | Reclassify the initial mark as clear text and interpret it as **in**; `dugarlo → indugiarlo` also supplies an i. The reading marks this conjectural (`A/reading.md:19`). |
| 220v:17, V17.1 (`:23`) | `andar`, `andarb`, `andare`, etc.; not `andassi` | Re-segment `9 2¦3¦E9` as `QX 7`. The final 7 is absent from the saved alternatives (`A/reading.md:21`). |
| 220v:19, V19.2 (`:28`) | `haueo`, `hauero`, etc.; not `hauessi` | Re-segment the pendant as QX and change final P to 7. Final P has no 7 alternative in the saved file (`A/reading.md:24`). |
| 220v:21, V21.4 (`:34`) | `mantelo` or `mantedo`, among other n/c alternatives | `mantello` adds a second l or assumes an unrecorded ll value; the final table instead uses `?` for the disputed sign (`A/reading.md:28`). |
| 221r:10, R10.2 (`:56`) | Includes `larmataua`/`larmataup` etc. | The saved `i = u` is reduced to an uninterpreted stroke in the final table, then the blot is tentatively `[a]` (`A/reading.md:41`). Preserve the unread remainder; do not call the full phrase mechanically complete. |

The re-readings are partly documented in the prose apparatus. The problem is reproducibility and confidence, not necessarily concealment. A final token file and explicit change log would resolve much of it. `A/REPORT.md:55` says post-hoc changes are “all lenient,” yet `sicurtà` is strict in `A/reading.md:37`. Its p→pp change has **no plaintext effect** because both are u. Conversely, the d-choice in `dugarlo` was already present as an alternative in the saved transcription; it is not an out-of-lattice change.

There is also a straightforward display omission: **`A/reading.md:27` omits the leading `/` of Napoli**. `Z 7 / 11 S P 5 7`, treated entirely as cipher tokens, yields `di(n/c)apoli`, with only one n/c sign for the two displayed words. The archived transcription correctly has separate `Z¦5 7` and `/ 11 S P 5 7` (`A/blind_transcription.tsv:31`). The image shows the latter sign.

### 1.4 Alamanni needs more than the two TSV keys

The audit above deliberately uses the richer Alamanni working dictionary. It is not a demonstration that the supplied TSVs alone suffice:

- **X3:** both `ridolfi-1494/key.tsv:40` and `R/signs.tsv:34` give **t**. Alamanni's script gives **tt or t** (`A/lattice.py:12`). The six occurrences producing `tutto`, `vittoria`, `sotto`, `netta`, `mettere`, and `citta` (the last two in one combined run) require this extra tt value. The visible open-cup form resembles Ridolfi's PSI, whose tt value is gloss-supported. Map that shape explicitly to PSI or document the additional value; do not silently call X3→tt a sheet lookup.
- **QX:** must be equated with the gloss-supported ss family (Ridolfi Q). **PHI→rr** is reconstructed, not a value printed on the sheet. Alamanni permits both rr and x, then chooses rr by context.
- **22:** the sheet gives the Signore di Pesaro; the Ridolfi supplementary file uses the token `22` for a **null**. Alamanni uses it as a name code. These are contextual/tokenization distinctions, not a single interchangeable key entry.
- Other labels (`Zo`, `E9`, `6o`) and the r/null distinction of 9 need their own explicit conventions. The sheet's null list is prose, not executable rows. Also, `key.tsv` has duplicate `/` rows (`:11`, `:28`); a naive last-value-wins dictionary loses c. My audit preserves alternatives rather than treating that serialization defect as a failed decipherment.

## 2. Requested historical and sign claims

### 2.1 Name number 22: genuine gloss evidence, insufficient for an unconditional transfer

The [key-sheet crop](crops/key_names.png) shows **15 = S. Lᶜᵒ** and **22 = S. di Pesaro/Pesero**. The [fresh crop of 107 c.241r](crops/107_gloss22.png), source coordinates x=680–1220, y=1430–1570, shows an abbreviated **S. Lᶜᵒ directly over 22**, between clear “dove” and “quattro.” I see no reason to dismiss that association as a misaligned gloss.

That establishes a conflict between the sheet and this contemporary gloss. It supports a Lodovico interpretation **for this occurrence in Ridolfi 107**. It does not prove whether the discrepancy arose from a different working nomenclator, a local substitution, or an error, nor that Alamanni used precisely the same number list. Matching alphabet substitutions do not by themselves establish a matching nomenclator.

Recommended edition: **`[22: probably S. Lodovico; cf. Ridolfi 107 gloss; sheet: S. di Pesaro]`** on first occurrence, and `[22]` or `[Lodovico?]` thereafter. Keep the uncertainty in the English too: `A/reading.md:142` drops it. `A/REPORT.md:13` already says “probably”; the strict labels at `A/reading.md:17`, `:36` and the categorical statement in `A/reconcile.md:66` overstate the same evidence. The claim that the three contexts are “about Lodovico” partly depends on the disputed expansion and is not three independent confirmations. A cancelled generic “questo Signore,” even if read correctly, would not independently distinguish the candidates.

**Grade:** C for the local gloss association; **I, with M confidence, for its transfer to Alamanni**. Not H.

### 2.2 Six doubled-consonant signs: useful reconstructed key, unequal support

| Sign/value | Evidence inspected and assessment | Appropriate provenance |
|---|---|---|
| Q/QX = ss | Crossed/looped-descender family in targets; Ridolfi 107 c.241r glossed `fussi`, `messo` visibly support it ([crop](crops/107_ss.png)). | **C**, with M retained where the individual glyph is doubtful. |
| PSI/open cup = tt | Visibly distinct from closed PHI; `tutto` and `tratto` in 110 c.250r have the corresponding open-cup form ([crop](crops/110_tt.png)). | **C** for Ridolfi PSI; document the cross-hand equivalence for Alamanni X3. |
| PHI/closed circle = rr | Two Ridolfi lexical contexts, `arriuando`, `uorrei`; also Alamanni `guerra`, `serrarci`. Shape family is real; value is fitted to words, not gloss-confirmed. | **S**, not H/C; exact doubling is less independently established than the consonant identity. |
| Large loop = nn | Recurs in `innanzi`, `danno`, `Donnino`, `gouanni`, `glanno`. Strong internal consistency. | **S**. |
| Dotted cross = bb | Clear recurrence in `habbiate`/`habbia`; `strignerebbe` occurrence is materially less secure. The first two are the same lexical stem, not two independent lexical tests. | **S**, with **M** for the third occurrence and caution about the exact doubled value. |
| Triangle = cc | Clearly distinct sign in `bocca` and `faccenda`. Two compatible lexical contexts, no inspected gloss. | **S**. |

`R/REPORT.md:34` calls all six “fixed by at least two independent words.” This is too strong, especially for bb. Exact double versus single consonant is not proved solely by producing conventional Italian spellings in texts that elsewhere use single consonants. Keep these as reconstructed values with their actual provenance; do not remove the useful readings merely because they are reconstructed.

The sheet already has phi-like forms under x. “Not on the sheet” should distinguish **an unattested value** from **a demonstrably different glyph**. Do not generalize “φ means tt”: the working inventories distinguish an open tt form from a closed rr form.

### 2.3 θ/TH = non: supported in usage, not the sheet's label

I read the sheet's word as **noi**, in the sequence io, tu, voi, noi ([crop](crops/key_codes.png)); `key.tsv:52` agrees. `R/signs.tsv:47` instead says the label was read “non,” contradicting `R/REPORT.md:35`.

However, there is better evidence than eight plausible target contexts: **110 c.250r, cipher row around y=600, has the same arch-with-dot family beneath a gloss `no[n]` before `venga`** ([detail](crops/110_non_detail.png), original crop x=140–355, y=570–660). This supports non as a contemporary usage value. Correct the provenance, rather than reverting all eight target occurrences to noi.

**Grade: C for the attested usage; not H as a direct reading of the sheet label.** The eight strict occurrences can remain mechanically unambiguous under a documented working key, but must not count as eight independent validations of its value.

### 2.4 “nipote de la prefata duchessa”: retain with abbreviation brackets

At 113r:3 the sequence is compatible with:

`N 7 pb P v eo` · `Z eo 5 11` · `S 9` with raised `v c` · `Z i B? Q c`, followed by `2 P N 11` at 113r:4.

It gives **nipote · dela · prta · duchessa · bona**, after the recorded n/c, p/l/z, and d/l choices. The [detail crop](crops/113_prta_full.png), x=970–1255, y=1290–1430, confirms the raised signs. The royal RC sign is a different shape, visible elsewhere, and is not present in this sequence. Thus “nipote del Re” should be removed.

Keep **`nipote de la pr[efa]ta duchessa Bona`**. Prefata is a plausible expansion; the cipher encodes prta, not the missing efa. The table's `prta` can be H at the literal-letter level; the expansion is I. The phrase as a whole involves S/C and editorial I, not pure H. “Nephew” is a contextual interpretation of nipote. The specific identification as Louis de Luxembourg and the remembered genealogy (`R/reading.md:116`) have not been independently verified in this offline audit and should not serve as corroboration. `R/REPORT.md:21` calls remembered contextual facts corroboration despite explicitly saying they were not checked; downgrade that argument.

### 2.5 Alamanni's three phrases

- **“voltare Genova,” 220v:8:** retain. The visible `p P b u c 4 m` and `gd m / P p c` support `uoltare genoua` ([crop](crops/A_v8.png); `A/blind_transcription.tsv:13`, `:14`; `A/reading.md:14`). No supplied letters are needed. b=l and /=n require choices among the recorded values, so this is strong key-based lexical resolution, not a unique output of the raw key. Political interpretation as changing Genoa's allegiance goes beyond the letters and should be called interpretation.
- **“a manifesta vittoria,” 220v:18:** retain. `11 x c / 8 n m o u 11` yields `a manifesta` with /=n; `p 7 X3 P 4 7 c` gives `uitoria` with TSV X3=t or `uittoria` with the additional tt value ([crop](crops/A_v18.png); `A/reading.md:22`). The words are well supported, but doubling must be documented. **The preceding `andassi` is a separate, weaker re-reading** and should not inherit the phrase's confidence.
- **“la salute del re Alfonso,” 221r:2:** retain as a probable mixed clear/cipher reading. **`la salute` is clear text**, visible immediately before the cipher; it is not recovered by the key. The saved cipher alternatives include `delrealfonso`, but require several choices (`A/blind_transcription.tsv:43`). In particular, the penultimate sign in Alfonso looks open/u-like in the [detail crop](crops/A_alfonso_detail.png); I cannot certify the recorded o over u on shape alone. The name is a persuasive lexical resolution, deserving a forced/uncertain qualification rather than “every sign secure.” `et n[ost]ra` on the next line expands an abbreviation and chooses an uncertain ET sign (`A/reading.md:34`). The clause's conditional wording matters: it says the action **would be** the salvation, not that salvation occurred.

## 3. Fractions and grading

### 3.1 Ridolfi counts reproduce, but their interpretation needs narrowing

The independent count agrees exactly with the reports:

| Document | Units | Strict | Additional forced | Additional lenient | Doubtful | Unread |
|---|---:|---:|---:|---:|---:|---:|
| 112 | 131 | 44 | 45 | 40 | 2 | 0 |
| 113 | 100 | 41 | 25 | 32 | 0 | 2 |
| 115 | 52 | 19 | 20 | 13 | 0 | 0 |
| Total | 283 | 104 | 90 | 85 | 2 | 2 |

Thus 104/283 = 36.7%, 194/283 = 68.6%, and 279/283 = 98.6% are arithmetically honest **under the stated counting convention** (`R/reading.md:15`). It is good that low strict coverage, calibration errors, and known doubtful words are disclosed.

But 279 includes seven unresolved/contextual person expansions and `apresentarsi` with an unidentified p-sign. “Only four words not settled” (`R/REPORT.md:5`) overstates settlement; those four are only the units assigned the explicit doubtful/unread labels. Three RD instances still have two proposed identities. If the eight I-level units were excluded from “read,” the numerator would be 271/283 = 95.8%, **still not a secure-accuracy estimate**. This sensitivity illustration is not a replacement score.

Of the 104 strict units, **15 depend on reconstructed/non-sheet values**: eight TH, three Q words, one PSI word, two NN words, and one CC word. So no more than 89/283 = 31.4% are even candidates for a purely sheet-based strict tier before further provenance/abbreviation checks. That is an upper bound, not a newly certified H percentage.

“Forced” means one **normalized form present in the chosen finite corpus**, not one possible period-Italian expansion (`R/decode_lattice.py:65`). The corpus is neither a complete historical dictionary nor independent of all target context. The calibration-derived widening of confusable signs is sensible, but evaluating improved performance on that same calibration passage does not supply a fresh held-out accuracy estimate. The report's claim that more viewing cannot change the result is also stronger than a resolution limit warrants (`R/REPORT.md:19`).

### 3.2 Alamanni count is incompletely auditable; some strict labels contradict its policy

`A/reading.md:57` reports 93 units, with 65 strict, 15 additional lenient, 13 unread. Expanding the displayed table grades literally gives **64 S, 16 L, 11 U = 91**. If `el re` at line 13 is split into lenient el and strict re, despite the run's single L label, the read portion becomes **65 S + 15 L = 80**, as reported.

The remaining difference is the largest gap: `A/reading.md:52`–`:54` displays **U + U + U U = four units**, whereas `:60` assigns **six** unread words to 221v:3–4. Word division there is explicitly unknown. Six could be an editorial estimate, but it is not recoverable from the displayed units. Publish a per-word ledger and call the denominator provisional. I would not replace 93 with 91 as an allegedly exact manuscript count either.

More materially:

- `guerra` and `serrarci` are strict although rr is admitted to be **context only** (`A/reading.md:44`, `:55`; `A/REPORT.md:23`). This conflicts directly with the stated rule assigning context-inferred values to lenient (`A/reading.md:3`).
- All three Lodovico expansions are strict despite the cross-document transfer uncertainty. They should be I/M, even though the local Ridolfi gloss is C.
- Several other strict words choose values or earlier shape alternatives by lexical fit. They may be persuasive readings, but the same procedure would often enter Ridolfi's forced tier. **70% versus 36.7% strict is not a like-for-like comparison.**
- The report admits incomplete blindness and target-fitted key values. Its shuffled-key score supports non-random Italian structure and the general alphabet identification; it does not validate particular conjectures or calibrate the 86% coverage as 86% correct (`A/REPORT.md:43`, `:48`).

### 3.3 Recommended mapping to H/C/S/M/I

Here **S means cryptanalysis**, not Alamanni's existing “S = strict.” These labels describe evidence provenance; M additionally records unresolved confidence.

| Existing tier or operation | Appropriate review grade |
|---|---|
| Strict word, clear glyphs, literal values directly attested on the sheet, no lexical selection or expansion | **H** |
| Strict word depending on an inspected contemporary gloss, e.g. ss, PSI=tt, TH=non | **C**, retaining M for a poorly seen occurrence |
| Strict word depending on reconstructed nn, cc, bb, rr | **S**, with M where the inference or glyph remains weak |
| Forced lexical choice among ambiguous signs | **S**; often **S/M** because corpus uniqueness is not historical necessity |
| Lenient LM/sense selection within the admitted alternatives | **M** (a cryptanalytic proposal, not an authenticated lookup) |
| Added letters, abbreviation expansion, contextual name/person identity, transferring a nomenclator value between documents | **I**, with C cited when a gloss motivates the inference; M where unsettled |
| Doubtful/unread | **M/unread**; no recovered-word credit for a conjectural completion |

Retain both a literal transcription/decode and a normalized reading. Publish coverage by explicit evidence class, or retain the present fractions with these qualifications. No percentage from this targeted review measures the number of words actually correct.

## 4. Itemized image spot-checks

The tables record every counted sample and link to the inspected crop. Sign alternatives are shown with `¦` to distinguish them from table separators. Reported tiers are those of the proposed reading, not endorsements by this review. See sections 1–3 for the consequences of ambiguous or inferred values.

### Ridolfi 112: 15 cipher words

| Leaf:line | Proposed word; tier | Signs | Image comparison |
|---|---|---|---|
| 112r:4 | intendo; lenient | `7 N v eo N Z P` | [Crop](crops/112_L4.png). Matches the recorded sign classes; n/c and d/l are unresolved, so the word remains a contextual selection. |
| 112r:4 | arriuando; lenient | `11 PHI 7 p 11 N Z P` | [Crop](crops/112_L4.png). Matches, including a closed circle with vertical stem (PHI); rr is an inferred value, not visible letters. |
| 112r:4 | paua; strict | `S 11 p c` | [Crop](crops/112_L4.png). Matches four signs S 11 p c. There is no i sign. |
| 112r:4 | [il Re]; lenient | `RC` | [Crop](crops/112_L4.png). Long-tailed 2 with raised c is visible. The image supports the sign, not its royal expansion. |
| 112r:5 | duchessa; forced | `Z i B Q? c` | [Crop](crops/112_L5.png). Compatible with Z i B Q c; the long crossed/looped tail is visible, but Q? should retain its question mark. |
| 112r:5 | bona; lenient | `2 P N c` | [Crop](crops/112_L5.png). Matches 2 P N c; the n/c choice is linguistic. |
| 112r:5 | sala; lenient | `L 11 5¦^¦n c` | [Crop](crops/112_L5.png). L 11 [crossed upright] c visible. I cannot establish the third sign as l from shape alone. |
| 112r:8 | gorni; lenient | `gd P 4 N 6` | [Crop](crops/112_L8.png). Matches gd P 4 N 6; no additional i between g and o. |
| 112r:8 | innanzi; forced | `8 NN 11 N 6¦pb 7` | [Crop](crops/112_L8.png). Matches including the large looped NN and uncertain flagged 6/pb. Both the NN value and z choice need interpretation. |
| 112r:8 | edicto; doubt | `m Z 7 N v P` | [Crop](crops/112_L8.png). Matches m Z 7 N v P as classes. d/l and n/c remain open; edicto is not visually forced. |
| 112r:8 | fatto; forced | `n 11? PSI P` | [Crop](crops/112_L8.png). Open cup/descender PSI is visible. The preceding area is overwritten with raised correction marks; 11? is appropriately uncertain. |
| 112r:12 | strignerebbe; doubt | `L v 9 7 gd N m 4 3 BB? eo` | [Crop](crops/112_L12.png). Inserted v is raised above the baseline; a crossed, dotted penultimate sign is visible. BB identity remains doubtful. |
| 112r:17 | uorrei; lenient | `p P PHI m 6` | [Crop](crops/112_L17.png). Matches p P PHI m 6. Same closed PHI family as arriuando; rr and final i depend on interpretation. |
| 112r:20 | saria; lenient | `L c 4 b¦6 c` | [Crop](crops/112_L20.png). Matches L c 4 b/6 c. s/h and i/l/z ambiguity are not resolved by this crop. |
| 112r:20 | danno; forced | `Z c NN P` | [Crop](crops/112_L20.png). Matches Z c NN P; NN is conspicuously larger than the small e/o signs. |

### Ridolfi 113: 15 cipher words

| Leaf:line | Proposed word; tier | Signs | Image comparison |
|---|---|---|---|
| 113r:3 | figluolo; lenient | `n 7 gd Z i P Z P` | [Crop](crops/113_L3.png). Matches n 7 gd Z i P Z P, including two open d/l-family signs. No extra i after l. |
| 113r:3 | conte; lenient | `N P N v eo` | [Crop](crops/113_L3.png). Matches N P N v eo; c/n assignments are contextual. |
| 113r:3 | polo; lenient | `pb P b P` | [Crop](crops/113_L3.png). Compatible with pb P b P; first b is flagged, second plain. p and l chosen from the recorded classes. |
| 113r:3 | nipote; forced | `N 7 pb P v eo` | [Crop](crops/113_L3.png). Matches N 7 pb P v eo; first N is n/c, and pb remains the broader transcription class. |
| 113r:3 | dela; forced | `Z eo 5 11` | [Crop](crops/113_prta_full.png). Matches Z eo 5 11, not a code for the King. |
| 113r:3 | prta; strict | `S 9 ^v ^c` | [Crop](crops/113_prta_full.png). Matches S 9 with raised v c. The letters efa are absent and supplied by abbreviation expansion. |
| 113r:3 | duchessa; forced | `Z i B? Q c` | [Crop](crops/113_prta_full.png). Compatible with Z i B? Q c. The B area is dark/overwritten; retaining its question mark is justified. |
| 113r:4 | isabela; strict | `8 o 11 2 eo 5 11` | [Crop](crops/113_L4.png). Matches 8 o 11 2 eo 5 11: one l-sign only. |
| 113r:4 | uole; strict | `p P 5 m` | [Crop](crops/113_L4.png). Matches p P 5 m: u-o-l-e, not the connected text's volle. |
| 113r:4 | apresentarsi; lenient | `11 Y? 9 m L eo N v 11 9 o 7` | [Crop](crops/113_L4.png). The y-like second sign is visible and distinct from the usual p forms. Its p value is not independently established. |
| 113r:8 | donnino; lenient | `Z P NN 7 N P` | [Crop](crops/113_L8.png). Matches Z P NN 7 N P; large looped NN again visible. d/l and n/c still require choices. |
| 113r:8 | uestito; strict | `p m o v 7 Z°x v P` | [Crop](crops/113_L8.png). Matches p m o v 7 [cancelled sign] v P; the crossed-out insertion is real and should be documented as deletion. |
| 113v:1 | bocca; strict | `2 oo CC c` | [Crop](crops/113v_L1.png). Matches 2 oo CC c. A closed triangle is clearly present; cc is a reconstructed value. |
| 113v:1 | gouanni; strict | `gd P p c NN 8` | [Crop](crops/113v_L1.png). Matches gd P p c NN 8. No i-sign after g. |
| 113v:2 | modona; forced | `x P Z P N c` | [Crop](crops/113v_L2.png). Matches x P Z P N c; d/l and n/c remain choices. |

### Ridolfi 115: 15 cipher words

| Leaf:line | Proposed word; tier | Signs | Image comparison |
|---|---|---|---|
| 115r:5 | opinione; forced | `oo pb 8 N 7 P N 3` | [Crop](crops/115_L5.png). Matches oo pb 8 N 7 P N 3; two n/c signs and flagged b are visible. |
| 115r:5 | habbiate; forced | `^ + BB 8 c v eo` | [Crop](crops/115_L5.png). Matches ^ + BB 8 c v eo. Dotted cross after the plain a-cross is distinct; bb is inferred. |
| 115r:6 | potere; strict | `S oo v 3 4 m` | [Crop](crops/115_L6.png). Matches S oo v 3 4 m. |
| 115r:6 | resistere; forced | `9 eo L 6 o X3 m 9 3` | [Crop](crops/115_L6.png). Matches 9 eo L 6 o X3 m 9 3; s/h and i/z classes remain as recorded. |
| 115r:6 | forze; forced | `n P 9 b m` | [Crop](crops/115_L6.png). Matches n P 9 b m; b is compatible, z chosen linguistically. |
| 115r:7 | citta; forced | `N 8 PSI 11` | [Crop](crops/115_L7.png). Matches N 8 PSI 11; the open tt-family sign is visible. |
| 115r:7 | habbia; forced | `^ 11 BB 7 c` | [Crop](crops/115_L7.png). Matches ^ 11 BB 7 c. Same dotted-cross family as habbiate. |
| 115r:7 | essere; strict | `m Q 3 4 eo` | [Crop](crops/115_L7.png). Matches m Q 3 4 eo; long crossed/looped descender Q is visible. |
| 115r:9 | faccenda; forced | `n 11 CC eo N Zx c` | [Crop](crops/115_L9.png). Matches n 11 CC eo N Zx c; closed triangle distinct from the cup and circle signs. |
| 115r:10 | glanno; strict | `gd 5 11 NN P` | [Crop](crops/115_L10.png). Matches gd 5 11 NN P. There is no h-sign: gl'hanno is editorial normalization. |
| 115r:10 | promesso; forced | `pb 9 P x m Q oo` | [Crop](crops/115_L10.png). Matches pb 9 P x m Q oo, including final underlined o. |
| 115r:10 | faenza; forced | `n c eo N 6¦pb 11` | [Crop](crops/115_L10.png). Matches n c eo at line end and N 6/pb 11 at next line start (also 115_L11). z remains a choice. |
| 115r:11 | lorzo; lenient | `b P 4 ^6¦pb ^P` | [Crop](crops/115_L11.png). Matches b P 4 with raised 6/pb P. en is absent; abbreviation expansion is marked in the reading. |
| 115r:11 | gouanni; lenient | `gd P p 11 NN 6` | [Crop](crops/115_L11.png). Matches gd P p 11 NN 6; no i-sign after g, final i/z choice unresolved visually. |
| 115r:12 | sono; forced | `o P N oo` | [Crop](crops/115_L12.png). Matches o P N oo; N is n/c, final o underlined. |

### Alamanni 96: 25 cipher words

| Leaf:line | Proposed word; tier | Signs | Image comparison |
|---|---|---|---|
| 220v:8 | voltare; strict | `p P b u c 4 m` | [Crop](crops/A_v8.png). Matches. Seven signs, giving uoltare with the l value of b. |
| 220v:8 | Genova; strict | `gd m / P p c` | [Crop](crops/A_v8.png). Matches. The slash-label sign is visible; n rather than c is a word-level choice. |
| 220v:13 | [in]dugarlo; lenient | `m 5¦Z p gd 11¦ii 4 5¦Z P Zo` | [Crop](crops/A_v13.png). Cipher body is compatible with d-u-g-a-r-l-o. The preceding clear/cipher m-like mark does not itself give in. |
| 220v:17 | andassi; lenient | `c / Z c 9 2¦3¦E9` | [Crop](crops/A_v17.png). A crossed-tail 9 family is plausible, but the final sign is hooked/2-like. Final QX 7 is a conjectural resegmentation, not a confirmation of the archived tokens. |
| 220v:18 | manifesta; strict | `x c / 8 n m o u 11` | [Crop](crops/A_v18.png). Matches; the preceding 11 is a separate a. n/c value selected for the slash sign. |
| 220v:18 | vittoria; strict | `p 7 X3 P 4 7 c` | [Crop](crops/A_v18.png). Matches open cup with descender for X3. It resembles Ridolfi PSI; tt is not the t value recorded for X3 in the TSV keys. |
| 220v:19 | havessi; lenient | `^ c p m 9 3¦Z¦Zo P` | [Crop](crops/A_v19.png). Pendant crosses the 9-family sign; QX is plausible. Last mark is pi-like rather than an unequivocal 7. Keep final i uncertain. |
| 220v:21 | sotto; strict | `o P X3 P` | [Crop](crops/A_v21.png). Matches open cup/descender X3. Again tt requires the additional value. |
| 220v:21 | mantello; lenient | `x c / u m Z¦5 P` | [Crop](crops/A_v21.png). Crossed penultimate glyph is real but not securely the ordinary l-form. No separate ll-sign or second l is transcribed. |
| 221r:1 | vedessi; strict | `p m Z¦3 eo¦o QX 7` | [Crop](crops/A_r1.png). Compatible with chosen p m Z eo QX 7, including flagged small o. The alternative classes are recorded in the archived transcription. |
| 221r:1 | ferla; lenient | `n m 4 5 11` | [Crop](crops/A_ferla_detail.png). I do not confirm the claimed three-minim m. The vowel sign looks c-like at this resolution; farla remains viable. Preserve uncertainty. |
| 221r:2 | netta; lenient | `/ m X3¦4 11` | [Crop](crops/A_r2.png). Open cup form favours X3 over 4; n/c remains unresolved, and tt is additional to the TSV key. |
| 221r:2 | Alfonso; strict | `c 5¦/ n P / o¦u P` | [Crop](crops/A_alfonso_detail.png). Broad sequence compatible; penultimate sign is visibly open/u-like. I cannot certify o over u by shape. Alfonso is a plausible lexical resolution, not all-signs-secure. |
| 221r:3 | nra; lenient | `/ 4¦X3 c` | [Crop](crops/A_r3.png). Matches the short group and visible abbreviation stroke; ost is supplied, not enciphered. |
| 221r:17 | volessi; strict | `p P 5¦Z eo¦o QX 7` | [Crop](crops/A_r17.png). Matches chosen l-form, flagged o and crossed-tail QX. |
| 221r:17 | guerra; strict | `gd p m PHI 11 9` | [Crop](crops/A_r17.png). Matches closed circle with vertical stem PHI and terminal 9. rr and null status of final 9 are interpretive. |
| 221r:18 | mettere; strict | `x m X3 m 4¦9 3` | [Crop](crops/A_r18.png). Matches open cup X3, not two written t-signs. |
| 221r:18 | travaglo; strict | `u 4 11 p c gd 5¦Z P` | [Crop](crops/A_r18.png). Matches; no extra i after gl. travaglio is a normalized spelling. |
| 221v:2 | poter; strict | `S P u eo¦o 4` | [Crop](crops/A_w2.png). Compatible with chosen S P u eo 4; small flagged o is distinguishable from the initial p sign. |
| 221v:2 | made (unread); unread | `x c 5¦Z m` | [Crop](crops/A_w2.png). Open/hooked d-family form is compatible. The crop does not license promotion to male. |
| 221v:3 | assai; strict | `c¦o QX 11 7` | [Crop](crops/A_w3.png). Compatible with c QX 11 7; crossed-tail sign visible. |
| 221v:3 | tenuto; strict | `u eo¦o / i u P` | [Crop](crops/A_w3.png). Matches chosen u eo / i u P; slash n/c resolved linguistically. |
| 221v:4 | serrarci; strict | `o eo¦o PHI 11 4 / 7` | [Crop](crops/A_w4.png). Matches closed PHI family; rr is inferred and slash c chosen. This is not sheet-only strict. |
| 221v:4 | la; strict | `5¦Z 11` | [Crop](crops/A_w4.png). Heavy foot on first glyph supports l-form; two strokes support a. |
| 221v:4 | via; strict | `p 7 c` | [Crop](crops/A_w4.png). Matches p 7 c; u/v convention gives via. |

