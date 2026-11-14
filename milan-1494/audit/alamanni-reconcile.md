> Audit file. Reconciliation log written by the transcriber of Alamanni's letter on 13 November 2026, after a fresh sign-by-sign transcription (hashed before the earlier working transcription was opened) was compared with that earlier transcription. Working labels: X3 here is the open cup that this repository labels PSI, QX is Q. File names refer to the research folder, not this repository; crops and images are not redistributed.

# Phase B - reconciliation of pass2 blind transcription with pass 1 (transcription_v2.tsv)

Phase A files were saved and hashed before any pass-1 file was opened (hashes in phaseA.sha256):
- blind_transcription.tsv da2003a6b56ed881a7fbb3369a1647c488460a1b04f89925d7058a8f951c8442
- clear_text.md 6bc7b47530545ac0ea3d4bdcfa01435212bf7b0fba50fb56cf15754191edbdf6

Caveats on blindness: I had key.tsv and the key sheet while transcribing, so plaintext suggested itself as I went.
"Blind" here means blind to pass 1's sign readings. Section B was re-examined on a contact sheet after opening pass 1; sections A and C rest on the Phase A crops
(pass2/crops/, 3x-5x) and were not all re-cut - where that matters it is said.
The scans are 1272 px wide; a sign is about 20-25 px tall, so some distinctions (5/Z family) are at the limit of the image.

## A. The ~10 post-key re-reads "o -> sigma(=e)" of pass 1
Pass 1 used one label (s6) for two different shapes. I see two glyphs:
- **S**: closed bowl with a flag rising to the right at the TOP (like a 6 / Greek sigma). Napoli (x3), tempo, schoprire, poter. Sheet value p.
- **eo**: small o with a short horizontal dash leaving it at mid height to the right ("o-"). Sheet value e (third e-sign).
In every place where pass 1 changed v1 "o" to s6=e (Genova 220v.24, 221r.11, 221v.2; vedessi 221r.1; del 221r.2; volessi 221r.17;
poter, tenuto, serrarci on 221v) my blind reading had "o with a dash" = eo, with plain o as the alternative. The dash is
visible in the crops (v220_24, r221_02, r221_17, w3b, w4b). Verdict: the re-reads stand on shape; they are the sheet's
e-sign, not plain o (= s). They are not sigma (= p) either; pass 1's "sigma also e in this hand" should be replaced by "two glyphs".

## B. The d / l split (pass 1: hd vs hl; mine: Z vs 5)
Done after opening pass 1, on a contact sheet (crops/contact_dl.png, crops/contact2.png; 5x-6x). Reference signs where the other
value gives a non-word: l from male, farlo, volessi; d from andassi, fidi, vedessi, grande. Two forms separate cleanly:
- **l-form**: upright stroke with a horizontal foot leaving to the RIGHT at the base (a 5 with a long flat bar).
- **d-form**: S-curved h-like stroke with a hook, no foot; a variant has a crossbar at the top (grande, del).
Disputed signs against the references:
| sign | pass 1 | Phase A first choice | contact sheet | decision |
|---|---|---|---|---|
| 220v.6 "? ### c" | hd | Z (note said "5-like", wrongly) | d-form, no foot | **da** |
| 220v.7 "m ? 4 m 9" | hd? | 5 | upright with bar to the right joining the 4: l-form, but the join makes it less clean | **el re**, kept lenient |
| 220v.13 first sign | hd | 5 | d-form | **d** (pass 1 right, my Phase A first choice wrong) |
| 220v.13 last-but-one | hl | 5 | l-form | l: "dugarlo" |
| 220v.21 "mante?o" | d-sign (g) | Z/5 | neither form: a d-like bowl with crossed ascender | not separable; "mantello" by sense, lenient |
| 221v.2 "x c ? m" | hd | 5 | d-form, no foot | **d: literal "made"**; my Phase A "male" withdrawn, word now unread |
| 221v.4 "? 11 p 7 c" | hd | 5/Z | l-form (heavy foot) | **la via** (pass 1 "da via" rejected) |
| 221r.17 "? 11 gd..." | hl | 5 | l-form | la |
Also checked and agreeing with both passes: di (220v.21, 221r.1, 221v.4), da (221v.2), del (221r.6), Napoli (220v.21), ferla.
Not individually checked: 221r.2 "del", 221r.10 "l'armata", 221r.18 "la citta", 221v.2 "di".
The crops for 221r "ferla" (m vs c) and "la guerra" (second sign) were not re-cut at higher zoom; those two stay lenient on the
Phase A view. The last sign of "havessi" was re-cut (contact2.png): crossed pendant under the 9 = ss sign, then a pi-like or
"stroke + 7" sign; still lenient.

## C. Other differences
| run | pass 1 | pass 2 | decision |
|---|---|---|---|
| 220v.17 end | not seen as cipher ("che si e seq[uito]") | c / Z c + 9-with-crossed-tail + 7-like | **new run: "andassi"** |
| 220v.18-19 "p m g 7" | g 7 (hauegi) | 9 + 3-like below + P | sign is the crossed-tail 9 (= ss, see D); last sign 7 (pass 1) or P (me): **"havessi"**, lenient |
| 221r.1 | "pm" taken as clear; hd s6 q 7 | p m Z eo QX 7 | **cipher "vedessi"**; the first two signs are cipher p, m |
| 221r.1 "di f?rla" | c (farla) | m (ferla) | 3 minims visible: **m, "ferla"** (= farla); lenient |
| 221r.3 "? / ? c" | lam D phi c (qnxa) | ET / 4 c | first sign = sheet's "et" sign (a with tail), third = 4: **"et n[ost]ra"**; lenient |
| 221r.4 | "L 22 9" | clear "del" + 22 9 | the L is the clear-text "del" abbreviation |
| 221r.6 "sic?rta" | phi | p with bar (sheet's third u) | **u: "sicurta"** |
| 221r.8 | nul | 6 with ring | **"grandeza"** if 6 = z, "grande a" if ring-sign null; lenient |
| 221v.2 | (same) | - | after the contact sheet: "x c Z m" literal "made", unread |
| 221r.10 | "non l'armata" | / P / + ... | n/c homophone: **"con l'armata"** by sense (se e' piglia piede con l'armata ... Genova) |
| 221r.17 | hl i d p m phi 11 9 | 5 11|u gd p m PHI 11 9 | second sign: two strokes seen; **"la guerra"**; lenient |
| 221r.18 | lam x m 4 m 4 z3 | D x m X3 m 4 3 | first = "per" code, 4th = tt-sign: **"per mettere"** |
| 221v.4 end | s6 | E9 (e with large loop) | undecided (null "e9" of the sheet, or e/p) |

## D. Signs not on the sheet, fixed by the Ridolfi gloss (calibration)
- 9/q with crossed flourish below (QX) = **ss**: Ridolfi 107 c.241r "n p QX 7" glossed "fussi", "x m QX P" glossed "messo".
  Here: vedessi, volessi, andassi, havessi, assai.
- phi-like sign (PHI) = **rr** here by two contexts (gue-rr-a, se-rr-arci); the sheet lists it under x. Not gloss-confirmed.
- X3 (y-like with dot) = t, used in all 7 cases for doubled t (tutto, vittoria, sotto, citta, mettere, netta; Ridolfi "lettere").
- **Name number 22 = "S. L[odovi]co"**: Ridolfi 107 c.241r "dove 22 quattro di fa" has the contemporary gloss "S. Lco" over 22
  (pass2/calib/c107_22b.png). The sheet LXXII 183 lists 22 as "S. di Pesero" and 15 as "S. Lco"; the correspondents evidently
  used 22 for Lodovico. In this letter the cancelled clear words before the first 22 (220v.11) look like "q[ue]sto S" with a raised o
  (heavily struck; reading not secure) - if so Alamanni began "questo Signore" in clear, struck it and wrote 22.
  One gloss instance; call it gloss-supported, not established. Alamanni's older sheet LXXII 178 uses 12-22 for doubled letters and is no help.
