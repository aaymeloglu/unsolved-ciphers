# Audit: how the 1494 readings were made and checked

This file is the research history behind [README.md](README.md). All dates are 13 November 2026.

## Sequence

1. **Access.** The ASF MAP image server answered only from Italy; the images (1272 px, the server maximum) were fetched over an Italian VPN exit with plain HTTP.
2. **Key identification.** While building a key from Ridolfi's glossed letters (LXXIV 101-110, 114), the transcriber compared the glossed pairs in 107 and 110 with the key sheets in MAP LXXII and found that LXXII 183 reproduces them (44 of 44 letters on eight words). The same sheet then read Alamanni's letter LXXIV 96. Alamanni's own Naples key sheet, LXXII 178, was saved but not formally tested once 183 read the letter.
3. **First working readings.** One agent per letter made a working transcription and reading. They read roughly half to three quarters of the cipher words; the main obstacles were signs merged in transcription and unrecognised doubled-consonant signs.
4. **Fresh transcriptions (a different model, Claude Fable 5.2).** For each letter a new agent transcribed every cipher run from the images with the key in hand but without opening the working transcription or reading, recorded alternative shape readings for every doubtful sign, and froze and hashed that file before comparing. It then reconciled each disagreement on shape evidence ([audit/ridolfi-reconcile.md](audit/ridolfi-reconcile.md), [audit/alamanni-reconcile.md](audit/alamanni-reconcile.md)), decoded the alternatives as a lattice under a language model, and marked every place where the model or the sense chose. Both transcribers ran a calibration on a glossed sibling (README, "Controls and calibration").
5. **Independent review (Codex).** A second model, given the images, the key and the readings but not the transcribers' reasoning, spot-checked 70 cipher words against enlarged crops, re-decoded every word by exact substitution, and examined the disputed claims ([audit/codex-review.md](audit/codex-review.md)).
6. **This folder.** The review's corrections were applied when the readings were moved here: a final token transcription for each letter that reproduces the reading, grades assigned by rule, and `verify.py` to enforce the rules.

## The review's findings and how they were handled

| Finding | Handling here |
|---|---|
| Ridolfi's 98.6% is coverage, not accuracy | Stated in README and in both reading files; calibration figures given beside it |
| Ridolfi connected text adds letters the cipher lacks (Pavia, giorni, figliuolo, pigliando, Giovanni) and changes *uole* to *volle* | Added letters bracketed: *Pav[i]a*, *g[i]orni*, *figl[i]uolo*, *pigl[i]ando*, *G[i]ovanni*; *non vuole* restored; the normalization policy for u/v and doubled consonants stated |
| *edicto*, *strignerebbe*, the two unread groups of 113 and the person signs must stay uncertain | Kept: doubtful and unread words graded M, person signs graded I, RD left as Duke or Lodovico |
| *nipote de la pr[efa]ta duchessa* is well supported; the genealogy is unverified | Reading kept with the expansion bracketed; the Saint-Pol identification marked as not checked against a reference work |
| The dotted Λ is labelled "noi" on the sheet; "non" comes from usage and the gloss in LXXIV 110 c.250r | key.json gives the sheet label and the gloss; the sign is graded C |
| The six doubled-consonant signs have unequal support; "fixed by two independent words" overstates bb | key.json and README grade ss and tt C (glosses), rr, nn, bb, cc S, with the words that fit them; bb's habbiate/habbia counted as one stem; the third bb doubtful |
| *apresentarsi* depends on an unidentified sign | Rendered *a[p]resentarsi*, graded I |
| Alamanni's earlier transcription file does not reproduce the final reading (andassi, havessi, mantello, the blotted sign, the Napoli display) | A final token transcription written for this folder; `verify.py` checks that each reading spells the key output. *andassi* and *havessi* are lenient with their re-segmentation noted; *mante[?]o* keeps the unidentified sign; the blot is an unread unit; *di* and *Napoli* are separate units with the ÷ sign in *Napoli* |
| Alamanni's open cup is given tt although key.tsv gives that label t; QX must be equated with Q; φ = rr is reconstructed | The open cup carries Ridolfi's label PSI (tt, C) and the crossed-tail 9 carries Q (ss, C); rr is S |
| 22 = Lodovico rests on one gloss in another letter and is not sheet-derived | Rendered "[22: probably S. Lodovico; cf. Ridolfi 107 gloss; sheet: S. di Pesaro]" at first occurrence and [22] after, in Italian and English; graded I |
| *guerra* and *serrarci* were called strict although rr is context only; Alamanni's strict tier was not like-for-like with Ridolfi's | One rule for both letters: a strict word may contain no ambiguous sign (÷, the d/l class) and no recorded alternative. 24 of Alamanni's words move from strict to forced; words with rr are graded S |
| Alamanni's 93-word count is not recoverable from the displayed units | The count is the units in alamanni-transcription.tsv (91), called provisional; the unread second threat on 221v counts as the four units its letters fall into, word division unknown |
| *la salute* is clear text; *Alfonso*'s penultimate sign could be u | Stated in the reading file; *Alfonso* is lenient with the alternative recorded |
| *ferla*, *netta*, *mantello*, *[in]dugarlo* overstated | All lenient (grade M); *ferla* records the c alternative, *netta* the 4 alternative |
| `key.tsv` serialized ÷ as two rows | key.json has one entry per label with a list of values (÷ = n or c) |

Not applied: the review's suggestion to publish a separate diplomatic expansion for every word. The literal key output of every word is in reading.txt and the editorial form beside it, which covers the same need.
