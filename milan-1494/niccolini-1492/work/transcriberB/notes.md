# Bare-leaf blind transcription, transcriber B (neutral labels)

Inputs: crops/bare (8 crops), hand learned from crops/masked/176r_L17-L28 with transcription-176r-neutral.tsv and work/transcriber/notes-176r.md. Zooms: work/transcriberB/z.py (autocontrast, x ticks every 50 crop px), output in work/transcriberB/out/. All x below are crop px (3x).

Conventions follow notes-176r.md: `Sxx{Syy}?` = best, then alternative; `+` joins a multi-sign alternative. ÷ with dot above and below = `S59{S12}?`; dash with dot above only = `S59`; dash with dot below only = `S47{S67}?`; "11" = S60; 9 with a long straight/curved descender = `S37{S10}?` (`S10{S37}?` when the descender loops back right). Free-standing two-digit numbers = N22, N15 (flagged). A single baseline dot after a sign (punctuation-like) is not recorded.

Total: 176 cipher tokens in 12 word rows, plus one clear row.

## Labels reused from 176r
- N1 "#"/"ff": 2-3 slanted strokes on one long bar (090r B1, B6; 104r start; 177r; 200r 2nd sign). Same as 176r.
- N2 b with a horizontal bar across the ascender: clear examples here, not a stray stroke (090r L15 x~3050; 177r x~1370-1430; 200r x~1960-2080). Since 176r had only one doubtful case, this confirms N2 as a real sign in this hand.
- N4 dash with an e/a-like loop in it ("-e-"): 090r L16 end of B5 (x~2020-2100), 177r x~2580-2670, 200r x~1760-1830 (faint).
- N5 short r/Γ-like stroke: 090r L15 x~3255-3285 (alt c), 177r x~835-860 (short stem with a blob/hook at top right, alt ı).
- N8 kinked stem + raised o: 104r last sign (x~2130-2195, a baseline dot after it not recorded). 177r last sign: kinked stem clear, the raised o only a faint smear at x~3460-3520, so `N8{S54}?`.
- S54 covers all the tall hooked/kinked stems, as in A's 176r calls. I checked this on an equal-scale contact sheet (work/transcriberB/sheet.py, out/sheet.png) against A's S54 at 176r L19 x~1990 and ~2650, L20 ~2440, L23 ~590, L27 ~3420 and L28 ~430. A's set already includes (a) the barless zigzag-through-baseline form (L19 ~2650, L27) and (b) the form with an arm to the right at the baseline and a short tail (L20, L23). So I write S54 and keep my sub-form in braces: `S54{N9}?` for the zigzag form (090r L14 x~2530-2580, L15 x~3295-3335, 200r x~1870-1935) and `S54{S72}?` for the baseline-arm form (090r L15 x~1400-1440, L16 x~990-1040, L17 x~2745-2785). Plain S54 = with a crossbar (090r L14 x~2340-2400, 104r x~1900-1950).
- S80 (o with a long flat top stroke): a bold closed bowl with a flat or peaked top stroke over it, 090r L14 x~3040-3090, L15 x~1330-1390. Alt S23 (B-like). Same shape both times.
- S19 o with a flag/dash to the right: 090r L14 x~3200-3250, L17 x~2640-2690 and 2930-2990, 177r x~1700-1820 (long thin tail ending in an upturned tick, alt o + S65), 200r x~1160-1240.

## New labels
- **N9** (used only as an alternative in braces): the barless S54 sub-form. A tall slanted stroke from above x-height to below the baseline, with an angular zigzag where it crosses the baseline. N8 is this body plus a raised o.
- **N10**: reversed c "ɔ", an arc open to the left, top end curling in. 090r L17 x~660-700. Alt S43 with no visible ascender.
- **N11**: cross/dagger. Heavy slanted stem from above x-height to below the line, horizontal bar at mid-height, small raised c/o at upper right. 090r L17 x~740-810. The stem is blotted (possible correction). Written `N11{S27}?`; could also be N8-like.
- **N22, N15**: free-standing numbers (flag): 090r L17 "22" (x~860-960, spaces on both sides, between N11 and clear "er"); 177r line-initial "22" followed by a dot (x~250-340); 090r L18 "15" (see B9).

## Per block
**090r-B1 (L14)** - high. "#" with two strokes and two bars (N1), then 9 with a long descender curving left under the N1. Cipher vs siglum: same N1 shape as inside runs.

**090r-B2 (L14)** - high. Sign 2 (x~2340-2400) tall stem + crossbar + foot hook = S54, same as 176r L19 x~1990. Sign 5 = S54, zigzag form (`S54{N9}?`). Signs 10-11: first ÷ has dots above and below; second has only the dot below. Sign 13 small c right after the 6 (could be part of the 6). Line is blank after x~3330.

**090r-B3 (L15)** - medium-high. Sign 1 (x~450-530): ʒ/ξ body with a horizontal bar across a short ascender, and a dot at its left (x~455), S49 alt S34 (dot not recorded separately). Sign 6: p whose descender is crossed by a long underline that also runs under the π = S63. Sign 9: dash with dot above only. "22" (x~1110-1200) sits inside the run with normal sign spacing, so S70 here, written `S70{N22}?` (or two S16). Sign 13 = S80.

**090r-B4 (L15)** - "sa" (x~2600-2700, accent-like stroke above it) is in the same letterforms as clear "formarsi" just before it, so I give it a clear row; if cipher: S55 S76. Cipher starts with 9 (x~2740). Sign 6 = N2 (bar clearly crosses the ascender). Last two signs N5 + S54 (zigzag form) run to x~3335.

**090r-B5 (L16)** - medium-high. Sign 1 ∂ with top hook (S43); sign 13 (x~1190-1260) bowl with the stem arching over to the right and down, unlike the S43 at sign 1, so S75 alt S43. Sign 16 (x~1420-1480) dash whose right end turns up with a dot above = S65 alt S59; sign 19 dash with dot above its right part (S59 alt S65). Sign 20 tall wavy long-s (S61 alt S55). Sign 24: 3 with a long tail, flat top joined to the preceding 6. Sign 25 N4. Clear "vuol" from ~2220.

**090r-B6 (L16)** - high. Clear "et" at x~2830-2900. N1 has three strokes. The run goes on past the listed end (3360): x, 11, then a dash with upturned right end and dot above (x~3400-3460, S65 alt S59).

**090r-B7 (L17)** - medium. v m; dash with dot above its right end; N10; N11; then free-standing "22" (N22). Clear "er" from ~1020.

**090r-B8 (L17)** - medium for signs, LOW for extent. Clear "q primo per vedere?" ends ~2580. I start the run at x~2605 with "o" + S19, one group earlier than listed (2730), because that group has the same o-with-flag shape as the S19 at x~2930. It could also be clear "o". Then S54 (baseline-arm form), 2, o, S19, 11, 6, 3 with long tail, a/N4-like loop joined to a 9 with long descender. The "ꝑ." after (x~3330) is clear.

**090r-B9 (L18)** - medium. Free-standing "15" (1 + 5 with top bar and descending tail) at x~935-1000, between clear "et" (x~800-860) and "nō" (x~1040-1150). NOTE: blocks.md gives 1035-1125, but that position holds clear "nō" (non). I take the listed "2-digit code" to be this "15" (the listed x seems off by ~100 px). Written `N15{S38+S54}?`.

**104r-B1 (L15)** - high. N1 on a long bar (x~775-945). Sign 3 a/o (S76 alt S81). Both 9s have descenders that loop back right, so S10 alt S37. Sign 16 S54 (stem + crossbar + foot hook). Last sign N8 (kinked stem + raised o), then a baseline dot (not recorded).

**177r-B1 (L3)** - medium overall. Sign 1 = N22 ("22." at line start). Sign 2 ⊥ with a flag at top-left of the stem (S36). Sign 10 (x~1080-1130) n vs u not clear (S74 alt S29). Sign 13 c, maybe an unclosed o. Sign 15 (x~1450-1500) is a solid ink blob with a short flag at upper right, blotted c/o, S19 alt S45. Signs 19-21 "a ı c" (x~1850-1960) have plain letterforms but I keep them as cipher. Sign 30 (x~2790-2830) L with a base stroke, separate from the next N1's bar (S52 alt S53; it could be the first stroke of the N1). Last sign N8{S54}? (see N8 above). Ink fades toward the right end (x>3150).

**200r-B1 (L3)** - medium; ink faint in places. Clear "tentar da" before it. Sign 9 (x~1330-1380): stem with a long bar across the top, lower part an open 5-like hook rather than a closed b bowl, so S54 alt N2. Sign 15 dash with dot below. Sign 16 N4 (faint). Sign 17 S54 (zigzag form): the stroke is a separate sign, not the descender of the "ſ" in L2 above, which ends higher up. Sign 19 N2 (closed bowl, bar across the ascender). Sign 22 (x~2220-2270) b whose ascender loops right at the top (S68 alt S69). Last sign 7 with a long descender curving left (S18). Clear "el" from ~2440.

## Main doubts
1. Run extents: 090r-B8 start (clear "o"?); 090r-B9 x-position mismatch with blocks.md; 090r-B6 runs past the listed end; "sa" before 090r-B4.
2. The S54 family (crossbar / zigzag / baseline-arm forms, N8 = with a raised o) is written as one label, S54, with the sub-form in braces. If these forms turn out to be different signs, the braces keep that information.
3. S80 vs S23 for the bold closed sign; S19 vs S81+dash.
4. Dots on ÷ variants are mostly clear on these bare leaves; 200r is the faintest.
