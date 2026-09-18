# Starhemberg, Paris, 23 May 1758: partial decipherment

**Substantial partial decipherment. The cipher system is identified; a complete, exact plaintext is not yet established.** The 1752 Prima/Secunda key in DECODE R1695/R1698 yields connected German across the letter. Work of 17-18 September 2026. This is a reproducible partial reading, not a claim of a complete or first decipherment.

Square brackets identify material restorations or uncertain readings; ellipses identify omitted unresolved text. Word boundaries, capitalization, spelling, and grammatical expansions of abbreviated key entries are editorial. Unbracketed prose is not a claim that every ending is independently encoded. The unchanged ciphertext and literal roots are available separately.

## Evidence and method

The target is [Cryptiana's transcription of Starhemberg's letter](https://cryptiana.web.fc2.com/code/variable2.htm#Starhemberg), credited there to Alexandre Pillon. We have not inspected the original letter image. The cipher rows, punctuation and marks are preserved in [ciphertext-lines.json](ciphertext-lines.json) and [source-transcription.txt](source-transcription.txt); no proposed digit repair is applied to them.

The existing 1752 Austrian key has two tables, called Prima (A) and Secunda (B). Ordinary units are two digits; a leading 3 introduces a four-digit code, producing a five-digit written unit. A standalone 8 is null. Marked three-digit units supply punctuation, dates or table changes. For this target, 876 switches A to B, 899 switches back, and Secunda897 supplies a period. The initial mark displacement is an explicit hypothesis. There are 1,721 digits in the saved transcription.

| Source | Material used |
|---|---|
| [DECODE R1695](https://de-crypt.org/decrypt-web/RecordsView/1695) | Alphabetical Secunda: I7472 P3 and I7473 P4; alphabetical Prima: I7475 P6 and I7476 P7; numerical copies: I7477 P8 and I7478 P9 |
| [DECODE R1698](https://de-crypt.org/decrypt-web/RecordsView/1698) | Numerical Prima I7484 P1 and Secunda I7486 P3 |
| [DECODE R1696](https://de-crypt.org/decrypt-web/RecordsView/1696), [R1697](https://de-crypt.org/decrypt-web/RecordsView/1697) | Instructions and historical worked example: I7481 P2, collated with I7483 P2 |
| [Antal, Mírka and Kováč, *Development of obfuscation techniques in Vienna during the early modern era*](https://doi.org/10.1080/01611194.2025.2457096) | Appendix C describes the system; Figures 1-2, printed p.193, reproduce a separate 1756 cipher/plaintext pair used here as a limited comparison |

The working keys are our provisional transcriptions of the cited historical tables. Some entries include alternatives or abbreviated roots; lack of a question mark does not certify a reading. Running the code reproduces our parsing and checks, while validating the handwriting requires consulting the sources. The published study documents the system, not a solution of this Starhemberg letter.

## Current readable text

### Opening and memorandum, rows 1–6

> … als ich nun den Innhalt derselben gefunden, so große Hoffnun[g] macht mir … daß … deroselben annoch gelingen werde, die durch das dem Stat[s]secretario Wall behändigte sehr treflich gefasste Memoir so geschickt als vor[sich]ti[g] eingeleitete Handlung nunmehro immer offen zu behalten und den spanischen Hof … zu solchen Resolutionen zu vermögen …

This concerns keeping open the negotiation initiated through the memorandum delivered to Wall. “Wall” is spelled `wa + l` here and again near the end. The name, memorandum, and long closing supply independent, separated support for the key match.

The uninterrupted `an + noch + ge + li + ng + en + werden` now gives **annoch gelingen werde**. Both an31005 and noch31019 were misread in the working key; no target digit repair is needed.

The opening adjective remains unresolved. Removing one surplus 3 permits `so / stat / lich`, but does not establish “stattlich” or “tröstlich.” The court passage needs a separate repair: two deletions yield `bi / zu / solch / resolution`; “bis zu solchen Resolutionen” remains a candidate, not an accepted restoration.

The proposed `31168 → 31368` at offset 195 supplies *s* in *Statssecretario*. The malformed `30073 → 31073` at 325 supplies *sich* in *vorsichtig*. Both still depend on the absent original. The 99 issue is discussed below.

### Peace passage, rows 6–8

> … die entweder dem Krieg eine vergnüglichere, als die dermahlige Gestalt ist, geben oder uns ein[en] erspr[ieß]lich[en] … honorablen Frieden verschaffen könnte, und gibt mir zumahl[en] …

The key corrections **31036 = Krieg**, **31490 = re** recover the first alternative without changing any digits. The literal sequence includes `Gestalt / ist / geben`; the displayed punctuation and inflections are editorial. Approximate sense: give the war a more favorable turn than its present state, or obtain an advantageous and honorable peace. The damaged join before *honorablen* still prevents an exact continuous reading.

**Frieden is now source-supported.** The full alphabetical F entry reads **fried**, with *en* and *same* endings; both numerical copies have the corresponding abbreviated entry. The previous reading *fremd* was wrong, and the target-specific override has been retired. The join before *honorablen* remains separate: inserting31 at624 and changing9→3 at626 yields `en / ho / null / n / or / ab / le / n / fried`. Deleting119 at624 gives a competing three-edit repair, with the preceding adjective ending editorial. Neither repair is authenticated. Once the join is repaired, `ver / [table switch] / schaff / könnte` follows unchanged. The baseline, correctly, still shows the damaged join.

### Contemporary statements and Minorca, rows 9–15

> … Euer Hochgebohrn … französischen Botschafter fast zu gleicher Zeit gemachten, genau gleichförmigen Äusserungen … sehr große Hoffnun[g], daß … Minorca an Spanien überlassen würde, wozu sich Frankreich [bereit?] zeige un[d] wohl leicht [en]tschließen wird, alsdann dieser Hof an dem Krieg mit Theil nehmen und andurch den [engländischen] und preußischen Hof in sehr große Verlegenheit setz[en] würde.

**New source correction:** Secunda 53 reads **mahl**, with s/en alternatives, not the earlier *meist*. The alphabetical entry lies between *mach* and *man* and agrees with the numerical copy. Thus the unchanged `gi / eb / t / mir / zu / mahl` supports **gibt mir zumahlen**. This supplies part of the lead-in; the following `von / den / no / ge / n …` remains unresolved.

The long phrase from *französischen Botschafter* through *Äusserungen* uses **unchanged digits**. Correcting the key readings recovers `fa+st`, `zeit`, `ge+mach`, `genau`, and `gl+ei+ch+fo+r+mi+gen+aus+ser+ung`. The abbreviated endings and first ge/gen reading remain editorial/paleographic choices, recorded in the audit.

The war passage is a reconstruction with specific limitations:

| Reading | Evidence or required restoration |
|---|---|
| Minorca an Spanien überlassen würde | Unchanged codes, grammatical endings expanded |
| bereit | Not established: 31405 reads *berg* in the historical key |
| und wohl leicht entschließen wird | Proposed 31329→31326 at 1046 and 55→95 at 1061 |
| engländischen / English | Proposed 31389→31399 at 1139, then an adjectival expansion of *Engelland* |
| preußischen Hof | Unchanged *Preuss + n + Hof*, ending editorial |
| Verlegenheit | Unchanged `ver / le / ge[n] / heit`; earlier rejection was caused by misread key entries |
| setzen würde | Proposed 55→95 at 1216 supplies *en* |

The repeated **55→95** repair is economical: it supplies *en* in two unrelated words, *entschließen* and *setzen*. It is still a conjecture. The connective before *Minorca* currently gives `daß / scho / n` and remains unresolved. Consequently the passage cannot yet be translated as an unconditional promise of Spanish participation.

### Closing, rows 15–22

> Da ich nun Euer Hochgebohrn durch den Courier Zinner zu erstattenden Berichten mit vielem Ver[langen?] ent[gegen]sehe, so brauche indessen nichts be[s]eres einrathen, als in dem bereits eingeschlagenen Weeg fortzufahren und den Wall so viel nur immer möglich durch dero [g]schicktes Benehmen zu weiteren Vertrauenausserungen zu vermögen.

Approximate English of this reconstructed closing:

> As I await with great eagerness the reports Your Excellency is to send through the courier Zinner, I can advise nothing better in the meantime than to continue along the course already taken and, through your skillful conduct, persuade Wall as far as possible to make further confidential disclosures.

The ending **nur** is explicit in both numerical copies of31218. The W entry31484 has a t alternative, supporting *weit* in *weiteren*; that t requires no inserted ciphertext. Other grammatical expansions remain editorial.

The awaiting/eagerness clause is **less secure** than the courier, reports, and subsequent advice. The key's 31427 has been read *lau* or *lan* with a *g* alternative, making *Verlangen* plausible. At the next row boundary, insertion of **seven digits, `3111531`, at offset 1369** produces `en / t / ge / ge / n / s / eh`. This gives *entgegensehe* with an editorial final e, but the length and content of the missing text are not uniquely established.

**Shorter alternative found on re-audit:** inserting only `31` at 1369 gives `31115 / 95 / 31154 / 31247`. Both numerical key copies and the alphabetical G entry show a longer alternative beside the usual *ge* for 31115, apparently **gege**. If that reading is correct, the sequence is `en / t / gege / n / s / eh`, giving the same *entgegensehe* with **two**, rather than seven, inserted digits. The exact letters of the longer key alternative remain provisional. This is a competing reconstruction, not an additional insertion. The baseline key and source remain unchanged.

The `31168 → 31368` restoration at 1414 supplies the *s* in *beseres*. This is selective: another 31168, at 525 in *vergnüglich*, correctly represents *u*. There is no separately encoded *zu* in *einrathen*; the earlier paraphrase “einzurathen” should not be represented as a literal decoding.

## Independent corroboration and the 99 problem

**Zinner** is `14 zi / 31307 n / 99 er`, following the whole-word code *Courier*. It requires no digit repair. Wille's journal independently records “M. Zinner, courrier impérial” under **5 September 1759**, volume 1, printed p.120. This corroborates the existence of a courier with this name, not conclusively that the two references identify the same person. [Primary source, full text](https://archive.org/stream/mmoiresetjournal01will/mmoiresetjournal01will_djvu.txt).

This also rejects a **global** replacement of 99 by g. Four target occurrences, at 97, 335, 945, and 1608, appear to need *g*, but occurrence 1298 needs the ordinary Secunda *er*. Prima99 is *man* and Secunda99 is *er* in the historical tables. Possible explanations include a target-specific variant or misread manuscript glyphs; none is settled without the target image.

## Mechanical verification

- All **1,721 published digits** remain unchanged in the baseline parser, producing 423 units.
- Marked 876 switches Prima→Secunda at 662; 899 switches back at 1349. Secunda897 at 1220 is a period.
- One explicit mark-placement hypothesis interprets the initial control as 854 at 109 instead of the overlapping published 885 at 108.
- **Thirteen unchanged-digit fragment alignments** pass, including the ambassador statement, courier Zinner, reports, and Verlegenheit.
- The independently transcribed historical worked example has **202 digits and 74 units**. All boundaries and switch818 agree exactly. Its 34 ordinary occurrences include 27 represented in the working key, with compatible roots. This validates mechanics and selected entries, not every target-key reading.
- A separate1756 letter with surviving plaintext supplies a limited **53-digit/13-unit lexical control**, independently aligning *Nachricht*, *glücklichen*, and *Ankunft*. Its plaintext article after *von* is not separately represented in the parsed fragment; this is not an exact full-clause match. See `parallel-control.json`.
- A second, disjoint **48-digit/12-unit** window in that 1756 letter aligns **so den 13 Marti an Euer Excellenz abgefert…**, including date codes 852/839 and table switch 840. The intervening span remains unresolved: these two windows are **not** a continuous 101-digit match. See `parallel-extension.json`.
- The key alternatives **me / mer / men** at Prima 31210 account for **nunmehro**, both **immer** occurrences, and **Benehmen**, with no digit edits. `variant-consistency.json` records all four contexts.
- Eleven explicitly modeled local repair cases reproduce their stated code sequences. Passing these checks proves only that a conjecture parses as claimed.

`repair_diagnostic.py` separately enumerates all minimum structural repairs within four fixed windows: 19, 11, 58, and 2 alternatives. Structure alone does not select the intended plaintext. In particular, deleting the surplus threes to obtain `31126 + 31272` at 793 requires **three**, not two, deletions, and still leaves the surrounding sentence unclear.

## What remains unresolved

The main gaps are the opening adjective; the join after *spanischen Hof*; the recto/verso join before *honorablen*; the sentence leading into the contemporary statements; the connective before *Minorca*; the *bereit* reading; and the beginning of the closing. The terminal 3 is incomplete. A few grammatical endings and the four 99→g occurrences also remain uncertain.

These limitations prevent an exact full-letter edition. They do not undermine the repeated key match or the recovered subject matter. The latest pass inspected all **239 distinct ordinary entries in the baseline target parse** against the numerical key, recording interpreted alternatives for 91 and unresolved notes for 18 in `target-wide-key-audit.json`. This measures inspection coverage, not decipherment accuracy; entries in malformed spans may not be intended codes, and repaired-only entries are outside this239-entry set. Proper-name alternatives irrelevant to this text were not exhaustively transcribed. The pass corrected *mahl* and confirmed *me / mer / men* across separate words. It did not establish *bereit*, the opening adjective, or the damaged central sentence.

## Combined repair assessment

`joint_candidates.py` combines the specified local conjectures into **eight competing full-letter parses**. Every nonterminal unit parses, both table switches survive, and Secunda99 remains *er* in **Zinner**. The terminal 3 is still incomplete. Several resulting phrases remain unreadable: valid segmentation alone does not solve the letter.

The alternatives cost **19 or 24 specified digit edits**, depending on the conditional two-digit or ordinary seven-digit *entgegensehe* reconstruction. Those counts exclude four selective 99→g readings, the initial mark displacement, and editorial root expansions. They are not a global minimum-distance result or a ranking by historical likelihood.

A useful ambiguity remains: at offsets 2, 443, 449, 708, and 793, replacing the presumed surplus digits with null **8s** yields exactly the same non-null code sequence as deleting them, at equal edit cost. Comparison scans contain difficult3/8 forms, but cannot establish the target's digits. Neither explanation wins on parsing alone.

The repeated-code checks also prevent indiscriminate repairs: Prima 31168 must remain *u* in *vergnüglich*, despite the two proposed 31168→31368 corrections elsewhere; the two Secunda 55→95 restorations consistently supply *en*; and the courier occurrence rules out global 99→g. See `joint-candidates.json` for original-offset edits and `joint-candidates.md` for literal roots.

## Original / printed counterpart search

No target scan or matching printed plaintext was located. Cryptiana credits Alexandre Pillon and warns that some digits may be missing at the image's right edge.

A promising counterpart remains [AT-OeStA/HHStA StAbt Frankreich Varia 28-14](https://www.archivinformationssystem.at/detail.aspx?ID=4225949): five German documents from Starhemberg to Franz von Rosenberg, 19 April–12 December 1758, cataloged with Spain, Bernis, Menorca, mediation, and peace plans. **The catalog does not establish that 23 May is included.** No attached scans or item-level children were found. Rosenberg is therefore a likely recipient, not a name decrypted from the ciphertext.

The separate [Spanien Diplomatische Korrespondenz 89-8](https://www.archivinformationssystem.at/detail.aspx?ID=2494474), Kaunitz/Maria Theresa to Rosenberg in 1758, is contextual material, not this letter.

Two public-domain OCR copies of Arneth volume5 were searched for the date, Rosenberg, Wall, and Minorca without a matching letter. A further volume6 check established that pp.362–365, suggested by a Bernis memoir footnote, concern **1762**, not this 1758 letter. This closes that particular lead; Fraktur OCR and non-exhaustive coverage limit the negative search. [Volume5](https://archive.org/details/geschichtemariat05arneuoft), [volume6](https://archive.org/details/geschichtemariat06arneuoft), [Bernis memoir chapter](https://fr.wikisource.org/wiki/M%C3%A9moires_et_lettres_de_Fran%C3%A7ois-Joachim_de_Pierre_de_Bernis/P2/IV).

The cited DECODE facsimiles are not redistributed here.

## Reproduce

Requires Python 3.9 or later and the standard library; no downloads or credentials are needed to reproduce the saved transcriptions. From this directory run:

```sh
python3 run_checks.py
```

This runs the baseline decoder first, followed by all eight verification and diagnostic scripts. The checks reproduce the checked-in JSON/text reports and generate the larger `joint-candidates.json` token report locally. Repeating them should leave Git status unchanged; the generated joint report and Python caches are ignored.

The baseline output conserves the public transcription; repairs are rendered separately in `repair-cases.json`. `key-audit-continuation.json` records source-based key corrections, while `target-hypotheses.json` records target-specific readings and proposed digit edits. The audit ledger retains explicitly superseded readings so corrections can be traced; the TSVs and current reconstruction take precedence over those earlier entries.

## Independent parallel-letter evidence

Figures1–2 of Antal, Mírka and Kováč, [Development of obfuscation techniques in Vienna during the early modern era](https://doi.org/10.1080/01611194.2025.2457096), printed p.193, reproduce a cipher and plaintext headed **Kaunitz, Vienna,17April1756**. The first53digits parse into13Prima units and independently corroborate the corrected an31005, nach73, and the u/uc/uck alternative31453. The paper describes sixteen parallel letters in the Slovak National Archive, Bratislava, Esterházy Čeklís branch, box634. Those letters were absent from the available DECODE catalog snapshot; no public supplement containing the full transcriptions was located. This negative search does not establish that none exists.

## English sense of the recovered text

The letter expresses hope that the recipient can keep open the negotiations initiated through the skillfully drafted memorandum delivered to Wall and induce the Spanish court to take favorable decisions. It discusses improving the course of the war or securing an advantageous, honorable peace. Closely agreeing statements involving the recipient and the French ambassador raise hopes concerning Minorca being ceded to Spain and Spanish participation in the war, which would put the English and Prussian courts in difficulty. The writer awaits reports through courier Zinner and advises continuing the existing approach, using tactful dealings with Wall to encourage further confidential disclosures.

This is a summary of the reconstructed passages. The unresolved connective before Minorca prevents deciding whether Spanish participation is stated conditionally, expected, or promised; the summary must not be quoted as a complete translation.


## Files

| Files | Purpose |
|---|---|
| `ciphertext-lines.json`, `source-transcription.txt` | Unchanged saved cipher rows and source attribution |
| `working-prima-v4.tsv`, `working-secunda.tsv` | Provisional key roots used by the decoder |
| `cipher_model.py`, `decode.py`, `two-table-parsing.json`, `two-table-output.txt` | Baseline parser and literal output; no digit repairs |
| `target-wide-key-audit.json`, `key-variants.json`, `key-audit-continuation.json` | Source readings, alternatives, uncertainty and correction history |
| `verify.py`, `fragment-alignments.json` | Source conservation and 13 unchanged-digit fragment alignments |
| `historical-control.json`, `calibrate.py`, `historical-calibration.json` | Independent historical worked-example transcription and mechanical calibration |
| `parallel_control.py`, `parallel_extension.py`, corresponding JSON reports | Two disjoint windows from the 1756 cipher/plaintext comparison |
| `variant_consistency.py`, `variant-consistency.json` | Alternative syllable readings checked across four target occurrences |
| `target-hypotheses.json`, `repair_cases.py`, `repair-cases.json` | Explicit, unverified local repairs and their consequences |
| `joint_candidates.py`, `joint-candidates.json`, `joint-candidates.md` | Eight competing combinations of proposed repairs |
| `repair_diagnostic.py`, `repair-diagnostic.json` | Minimum structural repairs within four fixed windows; not a plaintext ranking |
| `run_checks.py` | Runs the complete reproduction sequence |

All repair offsets are zero-based positions in the original digit stream. Generated candidate positions are separate. This distinction matters when combining insertions and deletions.
