# Niccolini sign-value table from the interlinear glosses (exemplar work)

Output: `../../niccolini-table.json`, built by `make_table.py` from `align.tsv`, one row per aligned gloss word.
`align.tsv` asserts that each row has as many values as signs. No image of doc. 97 was opened, and nothing in
`crops/bare/` or `transcription-bare-*`.

## Leaves used
- **doc. 21 c.42r** (81379): ll. 12-18, 26-27, 29-31. Most of the clean material comes from here.
- **doc. 21 c.42v** (81380): ll. 9-22.
- **doc. 6 c.9r** (81313): ll. 1, 3-6, 22, plus name numbers. **c.9v** (81314): l. 1-2.
- **doc. 62 c.133v** (81562): two "22"s and one partial word.
- **doc. 59 c.124v** (81548) and **doc. 72 c.147v** (81594): name numbers only (22, 24, 2-with-raised-letters).
- **doc. 81 c.176r** (81645 / `crops/unmasked/176r_L*.png`): B4, B6 (start), B7, B8, B10/B11, plus B1/B5 for 24. This
  was done first, to see how the blind transcriber's labels map onto Niccolini's real letter forms.
- Paged through but not aligned: doc. 21 c.43r, 44r (cipher with gloss, not reached); doc. 32 c.66r (short runs);
  doc. 35 c.78v/79r (dense cipher, but the gloss is faint and crowded at 1272 px; one line tried and dropped); doc. 37
  c.83r, doc. 62 c.133r/134r, doc. 72 c.147r (heavily glossed, worth doing next), doc. 78 c.163v/164r/164v (glossed runs).
  Every contact sheet (`out/contact_00`-`12`) was paged. Contact sheets are
  `out/contact_*.jpg` (`contact.py`). Docs 21, 35, 37 and 62 have the most cipher still to align.

## Method
1. Contact sheets, then 2x quadrant crops (`multi.py`, page-pixel ticks in red for x and green for y), then 3-5x
   crops of single runs. `chunks.py` makes two-line strips. `ucrop.py` crops the 3x deskewed unmasked c.176r bands.
2. Read the gloss word first, then the cipher signs under it. Where the gloss is compressed or shifted left (common:
   it often runs 20-70 px left of the cipher), word order and length decide which signs a word covers.
3. Labels are the neutral S/N labels, assigned the way the blind transcribers would assign them by shape. Where my
   reading of a shape and theirs may differ, the note says so (see S51/S80, S54, S43/S77).
3b. Line numbers in `align.tsv` are approximate counts from the top of the text. Page y for the main
   lines: 42r L12 ~725, L13 ~770, L14 ~810, L15 ~850, L16 ~895, L17 ~955, L18 ~1000, L26 ~1215, L27 ~1255, L29 ~1580,
   L30 ~1625, L31 ~1665; 42v L9 ~320, L10 ~350, L12 ~405, L13 ~450, L15 ~500, L17 ~590, L18 ~640, L19 ~680, L20 ~725,
   L22 ~825; 9r L1 ~205, L3 ~290, L4 ~350, L6 ~435, L22 ~830; 9v L1 ~210, L2 ~260; 133v L28 ~1010, L29 ~1065.
4. Basis: **G** = the gloss word is legible enough to fix the letters. **F** = the gloss is faint or partly
   illegible, and the values were fitted from context and the visible letters. Only G rows count toward `count`,
   `grade` and `agrees_with_sheet`. F rows show up as `fitted_count` and are marked "(fitted)" in `examples`.
   `agrees_with_sheet` is checked against key.json's `sheet` field, not `values`. It is false when the main gloss value
   is not on the sheet, or when some other gloss value off the sheet occurs at least twice. `values_not_on_sheet`
   lists any single-case departures.
5. Grade C = the main value has 2 or more clean gloss cases. S = one case, or fitted, or doubtful.
6. Most of the common letters agree with the sheet. That is still evidence: every G value was read against a gloss
   word, not taken from the key. But for o, n, a, e, r, t the gloss was checked word by word rather than letter by
   letter, so a single-letter misreading inside an otherwise clear word is possible.

## Results: where Niccolini departs from the sheet (MAP LXXII 183)
- **p is σ (S80) or a flagged b (S68). i is 6 (S51).** At 1272 px a σ looks like a 6. The difference is the top
  stroke: flat and running right for p, rising and curving for i. The c.176r transcriber labelled the p of "potea" S51.
  Two G rows (potea, aspirano) keep S51 = p because there the form is close to a 6. S51 is otherwise i, 8 times.
  The b-shaped p on doc 21/6 has a flag or hook on its ascender, which makes it S68, the sheet's p (5 G cases). Plain
  S69 = p only once (spirito on c.176r, where the transcriber wrote `S69{N2}?`).
- **S54 holds two letters (l 12, d 8).** In side-by-side zooms Niccolini's l is a b- or h-like sign with a looped
  ascender, and his d is a 5/ʒ-form: short flat top, stem, open hook below the line. The c.176r transcriber put both
  under S54 ("meglo" and "lo" = l; "da" and "cardi" = d). The table gives S54 both values, with the stroke feature.
  The l of "del" and "al" is a small 5 sitting on the line (S53, 3 cases); N3 in "naturalmente" is probably the same.
- **The e-like loop = o.** N4 (loop with a lead-in dash) has 7 G cases: suo, lo, spirito, affectionato, taranto,
  orsino x2. The sheet makes E9 (S33) a null. S33 alone has only one fitted case (inquieto).
- **S74 (n)** = f in fratello and prefetto (the sheet value), and a in naturalmente. I take the a to be a joined 11
  (two strokes linked by an arch). A transcriber cannot tell these apart, so S74 carries both values.
- **A double-barred stroke inside a word (S15) = ff** (affectionato, 1 case). The sheet's ## is a null. N1, the
  run-end #-sign on c.176r, is never under a gloss here. I treat it as a null (grade S). The ### (S14) closing "de
  conti" and the 9### after name numbers (124v, 147v) are nulls.
- **9 (S37):** r inside a word, null when it closes a word. This matches the sheet's "9 closing a word".
- **∂ / d-shape (S43):** g four times. A d-shape with no visible bar stood twice for ll (alla, castellano). The barred
  d-shape (S77) = ll.
- Single cases: S16 (2) = o in religiosi; S17 (φ group) = ct in affectionato; S48 (p) = n in aspirano; S19 = o in
  nuouo (S19 is otherwise e, 6 cases); S10 = ss in insignorissi.
- **Word and name signs:**
  - N9 ⊙ = papa (twice, 42r).
  - N10 Ħ, usually followed by 9, = Re (3 cases). This is a shape label, not numeral 10. On 9v L1 a "·H·" with "74"
    written over it carries the gloss "Trotto".
  - 100 = Re twice (9r "1009", 42v L10). A third gloss (42r L31) is "d.l papa" or "dl Re"; I cannot tell which.
  - **22 (S70) = S. Lodovico** ("S. L.o"), 8 cases on doc 6 c.9r and 9v (x2), doc 59 c.124v, doc 62 c.133v (x2) and
    doc 72 c.147v (x2). On the sheet S. L.o is 15, and 22 is S. di Pesaro.
  - **15: no glossed 15 anywhere in what I read.** On 147v L12-13 a "5" after "al" sits under what may be a gloss
    "re" (twice). The reading is too faint to count.
  - **24 = Ascanio** 3 times (176r B1 and B5; 147v "pregassi 24"). The sheet has Ascanio = 56. A "2" with small raised
    letters followed by 9 is also glossed "As." 3 times (42v, 124v, 147v); it is probably a cursive 24. On 42v L18 a
    "24" stands by a gloss "Ta." (Taverna?), unresolved.
  - 40 = Duca (9r L5). 48 has an unreadable gloss (9v L1).
  - λ (S26) = et (twice). ∇ (S25) = cc and ψ (S42) = tt, once each.

## Coverage gaps
- No glossed case for h, z or b (the only "b" is a doubtful ### under "buono"). No case for the word signs che (B),
  per (δ) or non (TH). For x, v and the doubled consonants other than ll there are only single cases.
- Labels used in `transcription-176r-neutral.tsv` with no table entry: N5, N7, N8, S27, S29.
  - N8 (stem + hook + raised o) is unglossed on 176r. The "2re/2n" + 9 group above may be what the transcriber saw
    as N8 at L19.
  - S27 (+) and S29 (u) were not met under a gloss.
- Not checked: 42r around x 240-350, y 830-875, a gloss like "abre(z)o" over a short group. It might give b and z.

## Uncertain spots
- 42r L12: the gloss "Ascanio" sits over "÷π÷" plus a following "2re". I recorded "÷π÷" as non (fitted).
- 42r L13 "orsino": the sixth sign is an unclear small loop.
- 42r L18 "catelano": the "o9" before it is not glossed.
- 42r L15 "creatione": I first read the gloss as "ragione" (fitted). L16 "creatione" is clear.
- 9r L1 "(l)apugla": the gloss reads "rapugla" or "la pugla"; the first sign (4-like) is unresolved.
- 42r L17 "Maria in portico": the gloss looks like "M.a in portico". "tico" runs onto L18.
- 176r L28 "nali": the gloss is "cardin?le". I took the plural (S58 = i). If it is singular, S58 = e.
- 176r B8 "non" is fitted: the gloss there is unreadable ("tono?ora").
- I could not align the long glossed runs on 9r L19 ("per dar alimento ... sopportarlo el S. L.o"), 9r L6 ("regno"),
  42r L14 ("rompere porto"), 42r L18 tail ("è più ... inimici?") or 42v L11.

- Rows whose gloss I could only partly read are marked F: inquieto, traditori, buono ecclesiastico, (l)apugla,
  santo Agnolo suo parente, cardinale orsino (42v L9), e non sia ne, the first creatione, non (x2), arcivescovo.

## Aligned passages (cipher labels | gloss values | basis)
Signs are neutral labels; `_` = null; `N24` etc. are numerals (S70 = 22). Generated from align.tsv.

- doc 21 c.42r L12 "riuniti": `S32 S51 S38 S12 S18 S50 S58` = `r i u n i t i` [G]
- doc 21 c.42r L12 "non": `S12 S11 S12` = `n o n` [F] - gloss "no" with tilde; Ascanio gloss sits over this+following 2-sign group, unresolved
- doc 21 c.42r L13 "orsino": `S11 S37 S52 S18 S12 ? S37` = `o r s i n o _` [G] - gloss "orsyno"; 6th sign e-like small loop (unclear), last 9 closing
- doc 21 c.42r L15 "ne": `S12 S28` = `n e` [G]
- doc 21 c.42r L15 "alla": `S45 S43 S60` = `a ll a` [G] - d-shape without visible bar
- doc 21 c.42r L15 "creatione": `S12 S32 S28 S60 S50 S51 S11 S12 S22` = `c r e a t i o n e` [F] - last sign 3/ʒ with long tail; gloss read "ragione"? letters fit creatione
- doc 21 c.42r L16 "alla": `S60 S54 S54 S60` = `a l l a` [G]
- doc 21 c.42r L16 "creatione": `S12 S32 S28 S45 S50 S58 S11 S12 S28` = `c r e a t i o n e` [G]
- doc 21 c.42r L17 "e non sia ne": `S28 S12 S11 S12 S52 S51 S45 S12 S28` = `e n o n s i a n e` [F] - gloss faint; values fit key
- doc 21 c.42r L17 "Napoli": `S12 S60 S80 S11 S54 S18` = `n a p o l i` [G] - p-sign has flat top stroke running right (sigma), not a 6
- doc 21 c.42r L17 "ne": `S12 S28` = `n e` [G]
- doc 21 c.42r L17 "Santa": `S52 S60 S12 S50 S45` = `s a n t a` [G]
- doc 21 c.42r L17 "Maria in portico": `S62 S60 S32 S51 S60 S18 S12 S80 S11 S32 S50 S51 S12 S11` = `m a r i a i n p o r t i c o` [G] - gloss "M.a in portico"; "tico" on L18 (v6÷π); p = sigma (flat top), i = 6 (rising top)
- doc 21 c.42r L18 "catelano": `S12 S60 S50 S60 S54 S45 S12 S11` = `c a t a l a n o` [G] - preceded by unglossed "o9"
- doc 21 c.42r L18 "catelani": `S12 S60 S50 S60 S54 S45 S12 S51 S46` = `c a t a l a n i _` [G] - final 9 closing word
- doc 21 c.42r L18 "Napoli": `S12 S60 S80 S11 S54 S18` = `n a p o l i` [G] - p-sign has flat top stroke running right (sigma), not a 6
- doc 81 c.176r L21 "naturalmente": `S59 S74 S50 S38 S32 S60 N3 S62 S28 S59 S50 S28` = `n a t u r a l m e n t e` [G] - gloss "natural[men]te"; N3 = small 5/t-like (sheet "5" = l)
- doc 81 c.176r L21 "affectionato": `S60 S15 S28 S17 S51 N4 S59 S60 S49 S11` = `a ff e ct i o n a t o` [G] - S17 (c-curl + long descender + o) taken as one sign = ct (could be 2 signs); S15 = ff
- doc 81 c.176r L22 "suo": `S52 S38 N4` = `s u o` [G]
- doc 81 c.176r L22 "fratello": `S74 S32 S60 S50 S28 S77 S11` = `f r a t e ll o` [G]
- doc 81 c.176r L22 "meglo": `N6 S28 S43 S54 S11` = `m e g l o` [G] - gloss "m?glo"; S54 here b-form with looped ascender
- doc 81 c.176r L22 "lo": `S54 N4` = `l o` [G] - S54 h-form, looped
- doc 81 c.176r L22 "potea": `S51 S11 S50 S19 S45` = `p o t e a` [G] - gloss "pot??"; S51 6-like = p
- doc 81 c.176r L22 "non": `S59 N4 S59` = `n o n` [F] - gloss illegible ("tono?ora"); fits n-o-n
- doc 81 c.176r L19 "religiosi": `S32 S28 S54 S18 S43 S58 S16 S52 S58` = `r e l i g i o s i` [G] - gloss "??lygnosi"; S43 = U/∂ with tall right stroke; S16 (2-like) = o, single
- doc 81 c.176r L19 "et": `S26` = `et` [G] - gloss "ce"/"et"
- doc 81 c.176r L19 "da": `S54 S60` = `d a` [G] - S54 here 5-form (flat top, hooked bowl)
- doc 81 c.176r L20 "spirito": `S81 S69 S18 S32 S58 S50 N4` = `s p i r i t o` [G] - gloss "sp????o"; plain b = p
- doc 81 c.176r L20 "inquieto": `S18 S59 S76 S48 S18 S19 S49 S33 S37` = `i n q u i e t o _` [F] - gloss "m?p?o" (badly read; letters fit inquieto); S33 = o single; final 9 closing
- doc 81 c.176r L20 "et": `S26` = `et` [G]
- doc 81 c.176r L27 "cardi(nali)": `S47 S60 S32 S54 S18` = `c a r d i` [G] - S54 5-form = d
- doc 81 c.176r L28 "(cardi)nali": `S59 S60 S54 S58` = `n a l i` [G] - gloss "cardin?le" spans L27-28; S54 = l; S58 = i (or e if singular)
- doc 21 c.42r L16 "del": `S54 S19 S53` = `d e l` [G] - gloss "del nuouo papa"; h-like sign then small o then 5
- doc 21 c.42r L16 "nuouo": `S12 S38 S19 S48 S11` = `n u o u o` [G] - S19 (small o w/ flag) here = o?; gloss legible "nuouo"
- doc 21 c.42r L16 "papa": `N9` = `[papa]` [G] - N9 = circle with central dot (⊙), word sign
- doc 21 c.42r L29 "de conti": `S54 S19 S47 S11 S59 S50 S51 S37 S14` = `d e c o n t i _ _` [G] - gloss "de conti" (Card. de' Conti); ÷ dot below = c, dot above = n; 9 then ### closing
- doc 21 c.42r L30 "aspirano": `S60 S81 S51 S18 S32 S45 S48 S11` = `a s p i r a n o` [G] - p-sign = n (single); S51 = p
- doc 21 c.42r L30 "al": `S60 S53` = `a l` [G] - preceded by unglossed dash+π
- doc 21 c.42r L30 "pontificato": `N9` = `[papa]` [G] - same ⊙ sign
- doc 6 c.9r L4 "traditori": `S49 S32 S45 S54 S51 S50 S11 S32 S51 S37` = `t r a d i t o r i _` [F] - S54 here 5-form = d; gloss partly legible
- doc 6 c.9r L6 "leuare": `S54 S28 S48 S45 S32 S22` = `l e u a r e` [G] - gloss "leuar(e)"; first sign y/h-like looped = l
- doc 6 c.9r L6 "questo": `S76 S38 S19 S81 S50 S11` = `q u e s t o` [G] - S19 small o with flag/tilde = e
- doc 6 c.9r L1 "(l)apugla": `S32 S60 S68 S38 S43 S54 S45` = `? a p u g l a` [F] - gloss "rapugla"/"la pugla"; first sign 4-like unresolved; b = p
- doc 6 c.9r L22 "S. Lo": `S70` = `[S.Lodovico]` [G] - "se 22 hauea", gloss "S. L.o" over 22
- doc 62 c.133v L29 "S. Lo": `S70` = `[S.Lodovico]` [G] - "sospetti di 22", gloss "S. L.o"
- doc 62 c.133v L28 "Il S. Lo": `S70` = `[S.Lodovico]` [G] - "22 no ha ...", gloss "Il S. L.o"
- doc 6 c.9r L22 "Re": `N10 S46` = `[Re] _` [G] - "offeso H9", gloss "Re"; N10 = capital H with crossbar
- doc 6 c.9r L6 "Re": `N10 S46` = `[Re] _` [G] - "il H9", gloss "Re"
- doc 6 c.9r L5 "Duca": `N40` = `[Duca]` [G] - "40" at line start, gloss "Duca"
- doc 62 c.133v L28 "entrare(tail)": `S50 S32 S60 S32 S28` = `t r a r e` [G] - gloss "entrare" over "ag. v4114m"; first part unresolved
- doc 21 c.42r L26 "suo": `S81 S38 S11` = `s u o` [G] - "Giangiò Orsino? suo"
- doc 21 c.42r L27 "prefetto": `S68 S32 S28 S74 S19 S42 S11 S46` = `p r e f e tt o _` [G] - gloss "Pfecto"/"prefetto"; n = f; ψ = tt
- doc 21 c.42r L27 "prospero co(lonna)": `S68 S32 S11 S81 S68 S28 S32 S11 S12 S11` = `p r o s p e r o c o` [G] - gloss "prospero colonna"; rest of Colonna on next line not aligned
- doc 21 c.42v L9 "cardinale orsino": `S12 S60 S32 S54 S18 S12 S60 S54 S28 S11 S37 S52 S18 S12 S11` = `c a r d i n a l e o r s i n o` [F] - gloss "cardinal(e) orsino"; d = 5/h-form, l = looped-b form (both S54 in transcriber usage)
- doc 21 c.42v L10 "Re": `N100` = `[Re]` [G] - "che 100", gloss "Re" over 100
- doc 21 c.42v L10 "tempora(le)": `S50 S28 S62 S68 S11 S32 S60` = `t e m p o r a` [G] - gloss "temporale"; b = p
- doc 21 c.42v L12 "castellano di Castel(lo)": `S12 S60 S81 S50 S19 S43 S60 S12 S11 S54 S18` = `c a s t e ll a n o d i` [G] - gloss "castellano di Castel..."; ∂ = ll here; preceded by o+h (gloss "el"?) not aligned
- doc 21 c.42v L13 "santo Agnolo suo parente": `S81 S60 S12 S50 S11 S45 S43 S12 S11 S54 S11 S81 S38 S11 S68 S60 S32 S28 S12 S50 S28` = `s a n t o a g n o l o s u o p a r e n t e` [F] - gloss "Agnolo suo parente" (santo fitted, gloss compressed)
- doc 21 c.42v L15 "buono ecclesiastico": `S14 S38 S11 S12 S11 S28 S25 S54 S28 S52 S58 S45 S81 S50 S18 S12 N4 S37` = `b u o n o e cc l e s i a s t i c o _` [F] - gloss "buono ecclesiastico" (2nd word cramped); ### under the b of buono (single); ∇ = cc; e-like loop = o; 9 closing
- doc 21 c.42v L17 "arcivescov(o)": `S60 S32 S12 S18 S48 S28 S81 S12 S11 S48` = `a r c i u e s c o u` [F] - gloss cramped; π inserted above line between ÷ and p; tail unresolved
- doc 21 c.42v L17 "di Taranto": `S54 S18 S49 S60 S32 S45 S12 S50 N4 S37` = `d i t a r a n t o _` [G] - gloss "di T(a)ranto"; d is 5-form; ξ = t; dash+e-loop = o
- doc 21 c.42v L18 "As.": `N2te` = `[Ascanio]` [G] - "ad 2" with raised "te"/"re", gloss "As."
- doc 21 c.42v L18 "Ta.?": `N24` = `[Taverna?]` [S] - "24 · R.mo", gloss "Ta." just left of/above 24; conflicts with 176r (24 = As.)
- doc 81 c.176r L17 "As.": `N24` = `[Ascanio]` [G] - B1, struck-through 24, gloss "As."
- doc 81 c.176r L20 "As.": `N24` = `[Ascanio]` [G] - B5, gloss "As."
- doc 6 c.9r L3 "Re": `N100 S46` = `[Re] _` [G] - "uerso 1009", gloss "Re" (et over following λ)
- doc 21 c.42r L31 "del papa?": `S54 S19 S53 N100` = `d e l [papa?]` [S] - gloss read "d.l papa" but could be "dl Re"; c42v and c9r gloss 100 as Re
- doc 21 c.42v L20 "si insignorissi": `S81 S18 S12 S52 S58 S43 S12 S11 S32 S51 S10 S58` = `s i n s i g n o r i ss i` [G] - gloss "s'insignoressi"; S10 (9 with long crossed descender) = ss
- doc 21 c.42v L20 "Re": `N100` = `[Re]` [S] - "a 100", gloss "Re" faint above
- doc 21 c.42v L22 "card(inale) orsino": `S12 S60 S32 S54 N4 S37 S81 S18 S12 N4 S37` = `c a r d o r s i n o _` [G] - gloss "cardinal orsino"; cardinal abbreviated to 4 signs; dash+loop = o
- doc 21 c.42v L19 "di Italia": `S54 S18 S51 S50 S60 S54 S58 S45` = `d i i t a l i a` [G] - gloss "di Italia"; d = 5-form, l = looped b
- doc 6 c.9v L1 "che compagno al Re": `S12 S11 S62 S68 S60 S43 S12 S11 S60 S53 N10` = `c o m p a g n o a l [Re]` [G] - gloss "che compagno al Re"; 7th sign a ÷ blotted with a cross stroke; Ħ = Re
- doc 6 c.9v L1 "S. Lo": `S70` = `[S.Lodovico]` [G] - "al 22", gloss "al S. L.o"
- doc 6 c.9v L2 "S. Lo": `S70 S46` = `[S.Lodovico] _` [G] - "di 22 9", gloss "S. L.o"
- doc 6 c.9v L1 "Trotto": `N10` = `[Trotto?]` [S] - "· H ·" with "74" written above it, gloss "Trotto"; probably H corrected to number 74
- doc 6 c.9v L1 "aym?": `N48` = `[?]` [S] - "a 48", faint gloss "aym'"? unresolved
- doc 59 c.124v L1 "S. Lo": `S70 S46 S14` = `[S.Lodovico] _ _` [G] - "di 22 9###", gloss "S. L.o" (y~205)
- doc 59 c.124v L1 "As.": `N2te S46` = `[Ascanio] _` [G] - "30 x11 2re 9", gloss "As." over the 2 with raised letters (y~205); "Amas(?)" gloss over 30x11 unread
- doc 72 c.147v L17 "As.": `N2te S46 S14` = `[Ascanio] _ _` [G] - "2n 9###", gloss "As." (y~710)
- doc 72 c.147v L18 "As.": `N24` = `[Ascanio]` [G] - "pregassi 24", gloss "As." (y~760)
- doc 72 c.147v L18 "S. Lo": `S70` = `[S.Lodovico]` [G] - "conforemsi 22 all...", gloss "S. L.o" (y~760)
- doc 72 c.147v L17 "S. Lo": `S70` = `[S.Lodovico]` [G] - "...one d. 22" line end, gloss "S. L.o" (y~715)
