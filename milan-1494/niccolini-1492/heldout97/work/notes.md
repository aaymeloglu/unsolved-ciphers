# heldout97 working notes

## Sources and identification
- Images: ASF MAP filza LXXIV doc. 97, c.222r, 222v, 232r, 232v (1272x1872 JPEGs).
- Writer: Angelo Niccolini. Signature at the foot of c.222v "Angelus Niccolinus U. d. ex or[ator]"; endorsement on
  c.232v "Agnolo Niccolini". Addressee: Piero de' Medici (address on c.232v, "... Florentie").
- Date: c.222v dateline "... die xx Julij 149?" - last digit has the same form as the second digit (4), so 20 July
  1494; the endorsement on c.232v reads "1494 ... a di 22 di luglio" (date of receipt), which agrees.
  Note: 1494, not 1492.
- Cipher: c.222r lines 3 to the foot (24 full cipher lines, plus one short group at the end of the clear line above
  them and one short group inside a clear line between C07 and C08) and the first six lines of c.222v. All carry an
  interlinear gloss in a lighter, browner ink, written in the space ABOVE each cipher line. c.232r/v have no cipher.

## Method
- `lines.py`: one entry per line (leaf, label, image, y of the line centre at page x=290 and x=1040). Fitted from
  local ink-profile peaks (`refine` step, saved in lines_refined.txt), then the lower 222r lines and 222v C04-C06 were
  corrected by hand from tick-marked overviews because the gloss rows pulled the fit.
- `crop_lines.py`: rotate the page about (290, yc) by atan((yR-yL)/750), crop page x 120-1250, y yc-48..yc+26,
  3x LANCZOS -> `crops/unmasked/<leaf>_<label>.png` (3390x222). Crop x = 3*(page x-120).
- `mask.py` (+ `mask_cfg.json`): gloss painted out with local paper colour (80th-percentile filter, smoothed, sd-2
  noise). Not colour-based (gloss and cipher ink measured almost the same colour). Geometry instead:
  top cut = valley of the ink profile between gloss row and cipher row per 300-px segment (smoothed); above it paint
  everything except ink components whose centroid lies below the cut (cipher ascenders); in the 12-px zone under the
  cut keep only components reaching the cipher body or compact marks <=30x30 crop px (dots of the ÷-like sign, raised
  o/c/9); below crop y 186 paint everything except components centred above it (descenders, dots under dashes).
  Per-crop overrides in mask_cfg.json: kill boxes 222r_C01 x1950-1990 y70-122 (gloss descender), 222r_C20
  x2240-2620 y80-102 and 222v_C03 x2380-2950 y80-96 (filler lines); lower top cut on 222r_C23 x1900-2250 (y120)
  and 222v_C05 x1100-1700 (y113) where the gloss sits low. Line centres for 222r_C17 (right end descends) and
  222r_C24 (fit had locked on the gloss) were re-set after the first masked check and those crops re-cut.
- Gloss reading: `gs.py` stacked 3x strips (gloss row + top of cipher), read once line by line, then a targeted
  second look at doubtful spots (5x zooms of C05/C09 "re di francia", C16/C17, the looped abbreviation sign written
  '??' in B17/B24/B26 etc.). The looped sign (a c/6-like loop with a long flourish) recurs but I could not fix its
  expansion (che? et?) without reading from sense, so it stays '?'. Doubtful letters '?'.
  Readings were never checked against the cipher signs (no sign counting, no key/table).
- Views in `work/view/` (s_* gloss strips, mm_* masked checks).

## Block extent
The gloss is a compact running decipherment, not letter-over-sign: smaller script, starts at the left margin, stops
at 45-85% of the width, then a drawn filler line to the margin; sense runs on from line to line. So each block is the
whole cipher run of its line (first to last sign). I could not identify any cipher tail that the gloss leaves out.
This is my reading of "the cipher signs standing under a legible gloss" for this letter; the scorer should know it.
Consequence: gloss-to-sign alignment inside a line is unknown, so name numbers / word signs could not be located;
none were excluded. Name/title words are flagged in blocks-97.md (possible word signs) and kept spelled out in the
reference.

## Reference conventions
- Letters as written (no spelling normalisation). Word spaces kept as in the gloss. Punctuation dropped.
  Struck-through gloss words dropped (B8, B18, B23; the corrections written above them were illegible).
- '?' = one illegible letter; where a run of letters was illegible the number of '?' is my estimate of the letter
  count from the ink width (approximate, +-1-2).
- No expansions were needed/added. Abbreviation marks: B11 "?logna??" and B14/B27 show tildes I could not resolve;
  written as '?'.
- Totals: 1314 gloss characters (no spaces), 902 legible, 412 '?' (69% legible).

## Legibility and masking per block
Touch spots = ink components with >=12% of their ink on each side of the top cut (gloss touching or crossing a
cipher sign, or a tall cipher sign reaching into the gloss row); split at the cut. Coordinates in crop px.

| Block | Crop | legible | ? | % | touch spots (crop x, y) |
|---|---|---|---|---|---|
| B1 | 222r_C01 | 35 | 9 | 80% | x788-812 y65-142 |
| B2 | 222r_L02 | 2 | 1 | 67% | x3019-3042 y66-109; x2389-2406 y83-113; x605-621 y90-138 |
| B3 | 222r_C02 | 32 | 21 | 60% | x2681-2708 y45-117; x2704-2729 y88-133; x1605-1626 y89-143 |
| B4 | 222r_C03 | 22 | 13 | 63% | x274-288 y62-111; x197-216 y74-106; x1785-1800 y100-117 |
| B5 | 222r_C04 | 35 | 13 | 73% | x1978-1999 y111-128 |
| B6 | 222r_C05 | 51 | 3 | 94% | x131-144 y82-117; x1831-1853 y82-111; x655-693 y109-119 |
| B7 | 222r_C06 | 31 | 39 | 44% | x479-506 y80-133; x1782-1817 y86-156; x1516-1535 y102-135 |
| B8 | 222r_C07 | 31 | 12 | 72% | x458-485 y74-154; x1194-1222 y98-127; x77-90 y99-126 |
| B9 | 222r_L08 | 4 | 2 | 67% | x329-360 y60-126; x2282-2406 y76-117; x1584-1608 y96-114 |
| B10 | 222r_C08 | 40 | 5 | 89% | x131-190 y21-128; x877-906 y55-125; x797-817 y72-120; x845-860 y80-129; x1460-1474 y82-123 |
| B11 | 222r_C09 | 30 | 15 | 67% | x82-117 y57-133; x845-888 y79-115; x2951-3041 y86-94; x786-797 y89-138; x193-211 y92-130; x918-947 y93-136; x679-734 y97-149; x2050-2080 y109-148 |
| B12 | 222r_C10 | 21 | 20 | 51% | x1216-1237 y87-117; x1512-1562 y96-134 |
| B13 | 222r_C11 | 35 | 9 | 80% | x2102-2161 y92-99; x173-186 y93-124; x1981-2003 y106-121 |
| B14 | 222r_C12 | 31 | 10 | 76% | x1011-1065 y55-162 |
| B15 | 222r_C13 | 33 | 8 | 80% | x1434-1479 y43-132; x3079-3140 y72-162; x658-693 y79-136; x777-806 y79-154 |
| B16 | 222r_C14 | 39 | 12 | 76% | x1483-1540 y32-132; x1513-1536 y74-106 |
| B17 | 222r_C15 | 31 | 4 | 89% | x432-452 y89-165; x1272-1289 y98-135 |
| B18 | 222r_C16 | 28 | 20 | 58% | x77-100 y73-149; x625-641 y84-113 |
| B19 | 222r_C17 (re-cut) | 37 | 19 | 66% | x971-1017 y96-112; x1560-1577 y96-111; x1042-1054 y98-131 |
| B20 | 222r_C18 | 41 | 7 | 85% | x1883-1896 y102-122; x2176-2196 y102-134 |
| B21 | 222r_C19 | 17 | 15 | 53% | x1796-1825 y70-133; x2072-2092 y80-113 |
| B22 | 222r_C20 | 27 | 16 | 63% | x25-84 y0-100; x671-697 y84-115; x2246-2608 y88-123 |
| B23 | 222r_C21 | 26 | 23 | 53% | x2059-2088 y89-130 |
| B24 | 222r_C22 | 32 | 6 | 84% | x612-634 y68-113; x480-579 y74-133; x1237-1262 y81-121 |
| B25 | 222r_C23 | 34 | 9 | 79% | x176-209 y53-137 |
| B26 | 222r_C24 | 20 | 11 | 65% | - |
| B27 | 222v_C01 | 13 | 15 | 46% | - |
| B28 | 222v_C02 | 26 | 15 | 63% | x1954-1993 y57-142 |
| B29 | 222v_C03 | 21 | 24 | 47% | x156-178 y79-147 |
| B30 | 222v_C04 | 35 | 5 | 88% | x1126-1174 y81-90; x2766-2799 y81-134; x1465-1487 y95-132 |
| B31 | 222v_C05 | 27 | 16 | 63% | x2009-2205 y82-93; x1187-1213 y84-158 |
| B32 | 222v_C06 | 15 | 15 | 50% | x3055-3101 y60-125; x2551-2610 y81-118; x2896-2915 y83-103; x2471-2496 y85-121 |

Masking checks: every masked crop was viewed (Read of the mm_*/fx* stacks) after the final rule; leaks found on the
first pass (222r_C17 and C24 bands mis-centred, C23 and 222v_C05 low gloss) were fixed and re-checked. In the
final set I could not read any gloss letter. Known artefacts:
- Raised marks wider than 30 crop px in the zone just under the cut can be lost (no keep-boxes were set); I saw
  none lost in the checks, but a raised tilde over a cipher sign would be at risk (222r_C15 x~2740-2830 and
  222r_C23 x~2800-2900 have tilde-like marks in the gloss row that I judged to be gloss and removed).
- Tall cipher ascenders that reach into the gloss row are clipped at the cut in places (e.g. 222r_C01 x~590 and
  x~2660, 222r_C05 x~1700, 222r_C13 x~1450, 222r_C14 x~1500). The sign body is intact; the top of the stroke is
  shortened.
- A few flat ink stubs (bottoms of gloss descenders) remain just above the cipher, e.g. 222r_C02 x~1180-1500,
  222r_C08 x~1550-1650, 222r_C06 x~1780-1820 (gloss L merged with a cipher sign). Not letter-shaped.
- Bottom cut at crop y 186 can trim the lowest tip of long descenders; dots under dashes are kept.
- Clear text in the bands (L02, L08, C07 end, C08 start, 222v_C06 end) is left visible, as on c.176r.
