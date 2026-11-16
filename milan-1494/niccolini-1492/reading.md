# Niccolini 1492: edited reading of the four bare cipher passages

ASF, Mediceo avanti il Principato LXXIV. Angelo Niccolini (Milan court) to Piero di Lorenzo de' Medici.
This is the reading stage, not a blind test. It uses the two blind transcriptions (A, B), the gloss table
`niccolini-table.json` (fallback `../key.json`) and the page images. Doc 97 was not opened for the first draft.
**After the fact:** once the doc 97 test had been scored, its transcription and gloss were tallied as an exemplar
([work/reader/doc97-tally.md](work/reader/doc97-tally.md)); the doc 97 crops and images were not inspected. Notes
marked *after the fact* use that tally. Tiers do not use it: they rest only on the listed values.
The word list with labels, key output, tier and grade is in [reading-words.tsv](reading-words.tsv).
Zoom scripts: `work/reader/cz.py` (line crops) and `work/reader/pg.py` (pages); zooms are in `work/reader/out/`.

Notation: clear text in roman, **cipher in bold**, [editorial letters or name expansions in brackets],
`[...]` = unread. Tiers and grades follow `../README.md` ("How the words are graded"):
- C = value glossed in Niccolini's own letters
- H = sheet value
- S = single case, fitted, a forced choice, or one of two values
- M = lenient, doubt or unread
- I = name number, or a word whose reading supplies the value of an unidentified sign

Tier rule, checked by [verify.py](verify.py) (`python3 milan-1494/niccolini-1492/verify.py`): a word is
**strict** only if every sign has one listed value and no label has an alternative; **forced** only if the listed
values of its signs allow exactly one word; anything that needs a value not listed for its label, a new shape
reading, or a choice between two real words is **lenient**. "Listed" means niccolini-table.json, then key.json via
alias.json, as in decode.py. The S54 hooks were sorted by shape (a crossbar or baseline arm gives the l-form, a ʒ-like
hook below the line gives the d-form). That sorting is not a listed value, so el/ed, di/li, al/ad and da/la are lenient.

## 1. c.90r (doc 42), postscript to the letter dated Pavia, 3 August 1492

> Tenuta adì iij. Et il S.or L.o mi ha conferito come mandano per pigliar el castello del Doria, e mi è parso scriverne ad[...]?
> Item mi ha conferito come **[il Re]** non cessa di stimolar(?) **el Re di Francia che lievi dal governo [22: S. Lodovico], et ch'el Re** risponde volere informarsi sa(?) **[...] se apto al governare lui; per(?) non sendo apto,** vuol esser quello che(?) **ci mantenga [22]**, er(?) dire che(?) manderà q(ualche) primo per veder(e) **[...] se apto** p. Dice po' che(?) **[15]** non è(?) ancora ben resoluto, che(?) mi darà notitia della resolutione.

English: "Item, he [Lodovico] told me that [the King] does not stop urging the King of France to remove
[Lodovico] from the government, and that the King [of France] answers that he wants to find out [...] whether he
[presumably the young Duke Gian Galeazzo] is fit to govern himself; and (since?) he is not fit, [the King of France]
wants to be the one who keeps [Lodovico] in place for us(?); and that he will send someone soon to see [...]
whether he is fit. He then says that [15] has not yet fully made up his mind, and that he will tell me the decision."

Notes.
- B1 is not a null followed by 9. The zoom shows **Ħ9**, the table's word sign for Re (N10, three glosses).
  Both blind passes wrote it N1 S37, so this is a new shape reading: lenient, grade I. On sheet 183 a plain H is
  the word sign for "voi" (row et · che · per · io · tu · voi = λ · B · δ · 2' · E · H); Niccolini's barred H is the Re of
  his own glosses. Which King is meant is not stated. A king
  who presses France to remove Lodovico fits the King of Naples (Gian Galeazzo's wife was Ferrante's granddaughter),
  but that is inference.
- "lievi": the first sign is a 6 with a very tall stem, like the l-form right after "che" on L15. Read as l, it gives
  "che lievi dal governo" (that he remove from the government). If it is the table's 6 (= i), the word does not
  read. The word is lenient. The first sign of L15 (barred ʒ with a dot; A S34, B S49) has the same shape as the d of
  "Domenico" on 200r, so it reads **dal**, not al. d is not a listed value of S34 (null) or S49 (t), so the word is
  lenient. *After the fact:* in doc 97 the same transcriber's S34{S49} stands under a glossed d six times.
- "apto" occurs three times with different signs (11 + barred b + v + π; c + 6 + ʒ + e-loop; 11 + 6 + ʒ + loop + 9).
  The first fixes the barred b (N2) as p. The other two then need 6 = p and ʒ = t (both table values); the 6 in the
  third has a rising top, which the table gives to i, so those two are lenient. *After the fact:* in doc 97 the
  long-tailed 3 (S49{S22}) is glossed e four times, which weakens the second and third "apto".
- "per non sendo apto" (word 20): the δ-like sign is "per" on the sheet. *After the fact:* in doc 97 the transcriber's
  S75 (δ) stands under "ll" three times (della, delle, uolli) and never legibly under "per". "per" is now doubt (M);
  the connective before "non sendo" is unread in substance. S55 = d in "sendo" is confirmed twice in doc 97.
- B4 and B8 have the same construction: an unread group, then **o + e-sign = se**, then **apto**. In B4 the unread
  group is "9 2" after the clear(?) "sa"; in B8 it is "o o— h 2", which may be clear script.
- The sign after the first 22 is a long-tailed 2 (A: N9; B: S26 = et). It has the shape of Ridolfi's person signs,
  but no raised letter is visible.
- The clear group read "et" by the transcribers before the ### (B6) has a looped ascender. The same group stands
  before "15" and before "mi darà". It is probably "che" rather than "et": compare the "et" form in line 1, "et il S.or".
  Marked "che(?)".
- 15 stands free in clear text. On the sheet 15 = S. Lodovico, but Niccolini writes Lodovico as 22, and Lodovico is
  the speaker here. So 15 is someone else; unidentified (I).

| # | labels | key output | reading | tier | grade |
|---|---|---|---|---|---|
| 1 | N10 S46 | [Re] | [il Re] | lenient | I |
| 2 | S28 S54 | e(l/d) | el | lenient | M |
| 3 | S32 S28 | re | Re | strict | C |
| 4 | S54 S51 | (l/d)(i/p) | di | lenient | M |
| 5 | S74 S32 S60 S59 S47 S51 S45 | (f/a)ranc(i/p)a | Francia | lenient | M |
| 6 | S23{S80} | che | che | forced | S |
| 7 | S51 S18 S19 S48 S51 | (i/p)i(e/o)(u/n)(i/p) | lievi | lenient | M |
| 8 | S34{S49} S45 S69 | (∅/t)ap | dal | lenient | M |
| 9 | S43 S11 S63 S28 S32 S59 S11 | (g/ll)ouerno | governo | forced | S |
| 10 | S70 | [S.Lodovico] | [S. Lodovico] | strict | I |
| 11 | N9{S26} | ? / et | et | lenient | M |
| 12 | S23 S72 | chel | ch'el | forced | S |
| 13 | S32 S28 | re | Re | strict | C |
| 14 | S37 S16 | (∅/r)o | - | unread | M |
| 15 | S81 S28 | se | se | strict | C |
| 16 | S60 N2 S50 S11 | a?to | apto | lenient | I |
| 17 | S45 S54 | a(l/d) | al | lenient | M |
| 18 | S43 S11 S48 S28 S32 S59 S60 S32 S28 | (g/ll)o(u/n)ernare | governare | forced | S |
| 19 | S72 S38 S51 | lu(i/p) | lui | forced | S |
| 20 | S75{S43} | per | per | doubt | M |
| 21 | S59 S11 S59{S65} | non | non | forced | S |
| 22 | S81 S28 S59 S55{S61} S11 | sendo | sendo | forced | S |
| 23 | S45 S51 S49{S22} N4 | a(i/p)to | apto | lenient | M |
| 24 | S47 S51 | c(i/p) | ci | forced | S |
| 25 | S62 S60 S59{S65} S50 S28 S59 S43 S27 | manten(g/ll)a | mantenga | forced | M |
| 26 | S70 | [S.Lodovico] | [S. Lodovico] | strict | I |
| 27 | S81 S19 S54 S16 | s(e/o)(l/d)o | - | unread | M |
| 28 | S81 S19 | s(e/o) | se | doubt | M |
| 29 | S60 S51 S49{S22} S76{N4} S37 | a(i/p)tq(∅/r) | apto | lenient | M |
| 30 | N15 | ? | [15] | doubt | I |

Counts: strict 5, forced 9, lenient 11, doubt 3, unread 2 (30 words).

## 2. c.104r (doc 49), Pavia, 20 August 1492

> ...et dicea delle commesse(?) fatte costì in sul papa **m[e]sser G[i]ovan Angelo [...]**. Venendomi a vedere, mi ha domandato come la fate co(n) la S.ria ...

English: "...and he spoke of the commissions (or: bets, *scommesse*?) made there [in Florence] on the Pope, messer Giovan Angelo [...]."
Alexander VI had been elected on 11 August.

Notes.
- The run opens with the ### null.
- "msser" has one sign too many if x and o are read separately. The o is taken as an unflagged e-sign (giving
  "messer") or as part of the sheet's ω-like m; lenient either way.
- The name is spelled Gouanangelo.
- The run ends in 9 (a closing null) and N8 (stem with hook and raised o), followed by a dot. The same N8 closes
  the 177r run. It may be a surname sign, an abbreviation or a run-end mark; left unread.

| # | labels | key output | reading | tier | grade |
|---|---|---|---|---|---|
| 1 | N1 S62 S81 S10 S28 S32 | mssser | m[e]sser | lenient | M |
| 2 | S43 S11 S38 S45 S59 | (g/ll)ouan | G[i]ovan | forced | S |
| 3 | S60 S59 S43 S28 S54 S11 S37{S10} | an(g/ll)e(l/d)o(∅/r) | Angelo | forced | S |
| 4 | N8 | ? | - | unread | M |

Counts: strict 0, forced 2, lenient 1, doubt 0, unread 1 (4 words).

## 3. c.177r (doc 81)

> ...Io ho ritratto la obedientia andrà in lungo, né **[22: S. Lodovico] havervi tanta parte quanta e' dimonstra [...]**. A te(?) mi racomando. Bene vale(?).

English: "I have gathered that the obedience [embassy to the new Pope] will drag on, and that [Lodovico] does not
have as large a part in it as he makes out [...]."

Notes.
- "havervi" depends on "ho ritratto" (accusative and infinitive). Its sixth sign is a short stroke with a hooked top,
  read as ı (= u/v), which was A's alternative. The g of the sheet's long-s gives no word.
- "tanta" uses S74 = a (the table's joined-11 case).
- The barred b in "parte" is again p.
- In "dimonstra" the ### inside the word is a null and the L is s.

| # | labels | key output | reading | tier | grade |
|---|---|---|---|---|---|
| 1 | S70 | [S.Lodovico] | [S. Lodovico] | strict | I |
| 2 | S36 S60 S48 S28 S32 S38 S18 | (h/s)a(u/n)erui | havervi | forced | M |
| 3 | S50 S74 S59 S50 S45 | t(f/a)nta | tanta | forced | S |
| 4 | N2 S45{S19} S32{S37} S49 S19 | ?arte | parte | lenient | I |
| 5 | S76 S38 S45 S59 S50 S45 | quanta | quanta | strict | S |
| 6 | S28 | e | e' | strict | C |
| 7 | S54 S18 S62 N4 S59 S52{S53} N1 S50 S32 S60 S37 | (l/d)imonstra(∅/r) | dimonstra | forced | S |
| 8 | N8{S54} | ? | - | unread | M |

Counts: strict 3, forced 3, lenient 1, doubt 0, unread 1 (8 words).

## 4. c.200r (doc 90), postscript

> Io ti ho narrato el progresso; a me non è possibile far iudicio(?). ... donde e' possa procedere. Io di qua, maravigliandomene, feci tentar da **frate Domenico da Ponzo** el S. L.o, ra[c]cordarmi(?) [...], et benché ne havessi dispiacere, nondimeno ...

English: "...I, wondering at it, had Lord Lodovico sounded out by Fra Domenico da Ponzo [...], and although it displeased me, nevertheless ..."

Notes.
- The run opens with 9 ### (a null group, as after the name numbers on 124v and 147v). The 9 after "frate" is a
  closing null.
- "Domenico" takes B's 3 (= e) for A's ξ.
- "Ponzo": the barred b is p (as in "apto" and "parte"), the plain or flagged b is z (the sheet value), and the last
  sign is a closing 9 (A) or a 7 = i (B).
- Fra Domenico da Ponzo was a Franciscan preacher active in Florence in these years. The identification rests on
  sense, so the word is lenient, and it is grade I because it supplies the value of N2.
- Right after the run, Niccolini writes Lodovico in clear: "el S. L.o".

| # | labels | key output | reading | tier | grade |
|---|---|---|---|---|---|
| 1 | S74 S32 S60 S50 S19 | (f/a)rat(e/o) | frate | lenient | M |
| 2 | S54 S11 S62 S22 S59 S51 S47 N4 | (l/d)omen(i/p)co | Domenico | forced | S |
| 3 | S54 S45 | (l/d)a | da | lenient | M |
| 4 | N2 S11 S59 S69{S68} S11 S37{S18} | ?onpo(∅/r) | Ponzo | lenient | I |

Counts: strict 0, forced 1, lenient 3, doubt 0, unread 0 (4 words).

## Totals

As printed by `verify.py`:

| | strict | forced | lenient | doubt | unread | words | strict / +forced / +lenient |
|---|---|---|---|---|---|---|---|
| 90r | 5 | 9 | 11 | 3 | 2 | 30 | 5 / 14 / 25 |
| 104r | 0 | 2 | 1 | 0 | 1 | 4 | 0 / 2 / 3 |
| 177r | 3 | 3 | 1 | 0 | 1 | 8 | 3 / 6 / 7 |
| 200r | 0 | 1 | 3 | 0 | 0 | 4 | 0 / 1 / 4 |
| **total** | **8** | **15** | **16** | **3** | **4** | **46** | **8 / 23 / 39** |

Grades in total: C 4, S 14, I 8, M 20.

## A vs B: disputed signs and verdicts

| place | A | B | verdict |
|---|---|---|---|
| 90r B1 | N1 S37 | N1 S37 | Ħ9 = [Re] (both missed the H) |
| 90r B2 sign 14 | S23 | S80 | B-shape with two closed bowls: S23 = che |
| 90r B2 sign 17 | N13 | S19 | S19 (e) |
| 90r B3 sign 1 | S34 | S49 | barred ʒ = d-form, as in 200r Domenico (unlisted value; doc 97 d ×6, after the fact) |
| 90r B3 after 22 | N9 | S26 | S26 (et), lenient |
| 90r B3 sign 13 | S23 | S80 | S23 = che (same shape as sign 14 of B2) |
| 90r B4 last two | S45 S54 | N5 S54 | S45 (a) |
| 90r B5 sign 13 | S75 | S75{S43} | δ; sheet per, but ll in doc 97 (after the fact): doubt |
| 90r B5 sign 20 | S55 | S61 | S55 (d), forced by sendo |
| 90r B5 sign 23-24 | S39 S49 | S51 S22 | 6 + ʒ = p t (apto), lenient |
| 90r B7 signs 4-5 | S43 N10(cross) | N10(ɔ) N11 | ∂ = g, cross = + = a |
| 90r B8 | N13 ×2, S49 S76 | S19 ×2, S22 S76{N4} | S19 = e; ʒ = t; final loop = o |
| 104r sign 3 | S81 | S76 | o, taken as an e-sign (lenient) |
| 104r last 9 | S37 | S10 | closing null |
| 177r sign 7 | S61 | N5 | ı = v (havervi) |
| 177r sign 15 | S45 | S19 | S45 (a), parte |
| 177r sign 23 | S54 | S61 | ʒ-form = d (dimonstra) |
| 177r sign 30 | S53 | S52 | S52 (s) |
| 200r sign 7 | N13 | S19 | S19 (e), frate |
| 200r sign 11 | S49 | S22 | S22 (e), Domenico |
| 200r last | S37 | S18 | closing null (A), doubtful |

## Name signs

- **22 (S70)** occurs three times: twice on 90r and once on 177r. Each time the context fits S. Lodovico.
  - 90r: the King of France is urged to remove him "dal governo", and wants to be the one who keeps him.
  - 177r: his part in the obedience embassy is smaller than he makes out.
  - This agrees with the eight glosses "S. L.o" over 22 in Niccolini's other letters (the sheet has 22 = S. di
    Pesaro). On 200r Niccolini writes Lodovico in clear, "el S. L.o".
- **Ħ9 (N10) = [il Re]** on 90r, lenient I (a new shape reading; both passes wrote N1 S37). On sheet 183 plain H = voi. Which King is not stated (Naples is likely).
- **15 (N15)**, in clear text on 90r. It is not Lodovico (the speaker), despite the sheet's 15 = S. L.o. Unidentified.
- **N2 (barred b) = p**. It is unglossed, and the value is fitted from three words (apto, parte, Ponzo).
- **N8 (stem + hook + raised o)** closes two runs (104r, 177r), each time after a closing 9. Unread.
- **N1 (###)** is a null in every place it occurs here: 104r start, inside "dimonstra" on 177r, 200r start, 90r B6.
