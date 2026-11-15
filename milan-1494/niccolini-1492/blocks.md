# Niccolini 1492 - cipher blocks (blind-test crop index)

Source images: ASF, Mediceo avanti il Principato, filza LXXIV (1272 px wide JPEGs).
Crops: `crops/unmasked/` and `crops/masked/` (c.176r, gloss present / painted out),
`crops/bare/` (leaves without a gloss). Every crop is one deskewed line band,
3x LANCZOS upscale, 3600 px wide. Crop x = 3 * (page x - 50), approximately
(the band is rotated about its left anchor, so the right end drifts by a few px).
Scripts: `work/crop_lines.py` (bands), `work/mask_176r.py` (gloss masking).

Line numbers count every written line from the top of the page text. On c.90r
the dateline and the two signature lines ("Tuus Angelus" / "Niccolinus") are
counted. On c.200r the short heading above line 1 is not counted.

Boundary words are the clear (plain-script) words on either side of the run.
My readings of the clear words are rough; "?" marks a doubtful reading.
Sign readings are deliberately not given.

A recurring sign looks like two or three tall strokes with a cross-stroke
("ff"/"#"-like). It shows up inside runs (90r B6, 104r B1, 177r B1, 200r B1)
and at the ends of runs on c.176r, where it sometimes has no gloss above it.
I treat it as cipher, but it could be a clear abbreviation. Flagged where it matters.

## c.176r (81645_doc81_c176r.jpg) - with gloss

"Gloss zone" = where the gloss sits in the unmasked crop (crop px x, 3x; and
y). It is the same region that is painted over in the masked crop. Use it to
match gloss to block. The y ranges are in 3x crop px, out of 258.

| Block | Line | Crop | Before | After | Run x (crop px) | Gloss zone (unmasked crop) | Notes |
|---|---|---|---|---|---|---|---|
| B1 | 17 | 176r_L17.png | pugnando | "er"/"et"? (x~1035) | 615-790 | x 630-770, y 0-110 | The run is a 2-sign group struck through by a horizontal line. Next to it (x 795-1005) is a "ff"-like group with a raised o, and no gloss above it: cipher or clear abbreviation? Uncertain. |
| B2 | 19 | 176r_L19.png | e (line start, x~225) | a nim...? (x~675) | 265-615 | x 250-600, y 0-80 | Line-initial "e" could be clear "e" or the first cipher sign. Small "o" above the third sign is kept: ink and position look like the cipher hand, but it could be gloss. |
| B3 | 19 | 176r_L19.png | ...him? | da | 1470-1565 | x 1460-1570, y 60-130 | Uncertain block: a 2-letter gloss sits over this short group. It may be a gloss on a cipher group or a correction of a clear word. |
| B4 | 19 | 176r_L19.png | da | (line end) | 1800-3450 | x 1955-2980, y 45-130; short stroke x 2865-2975 | The gloss stops near x 2980. The last part of the run (x 3000-3450, ending in the "ff"/"#" sign) has no gloss above it. Probably continues into L20 B5. |
| B5 | 20 | 176r_L20.png | (line start) | ma indarno? | 210-510 | x 235-355, y 18-95 (same ink shows at the bottom of 176r_L19.png, x 240-340, y 190-258) | The gloss mark sits only over the first two signs. The 2-sign group after them (x 390-500) could be cipher or a clear abbreviation. |
| B6 | 20 | 176r_L20.png | ma indarno? | ...ine ad? (line end) | 1065-3540 | x 1270-2670, y 36-147 | Real gloss only up to ~x 2670. After that there is just one long thin line in gloss ink, nothing letter-like. The last ~5 signs (x 3300-3540) may be clear text ("...ine ad"?). Uncertain. |
| B7 | 21 | 176r_L21.png | lun? / l'un? | tutte? (x~2415) | 300-2400 | x 455-1705, y 18-123 | Over x 1770-2610 only a long thin gloss-ink line, curving down at x~2300-2370 into a dark sign. Is that hook gloss or cipher? Left alone. |
| B8 | 22 | 176r_L22.png | essendo | (line end) | 1260-3450 | x 1325-2985, y 36-160 | Gloss covers to ~x 2985. Tail x 3000-3450 (ends in the "#" sign) has only a thin gloss-ink line above it. Probably continues into L23 B9. |
| B9 | 23 | 176r_L23.png | (line start) | "er"/"et"? (x~915) | 180-900 | x 210-360, y 24-100 (same ink at the bottom of 176r_L22.png, x 210-355, y 160-252); thin line x 480-900 | Short gloss, over the first signs only. |
| B10 | 27 | 176r_L27.png | no? (x~3120, could be "10" = cipher) | (line end) | 3180-3555 | x 3225-3560, y 30-132 | This is the "gloss above it at the right". The text slopes downward, so this run sits at the right end of L27, not L28. |
| B11 | 28 | 176r_L28.png | (line start; follows B10 at the line break) | da qu...? (x~900) | 225-870 | none readable; one long thin gloss-ink line x 240-720, y 50-90 | The "÷115895..." run. No gloss stands directly above it. The gloss at the right end of L27 (B10) may cover B10+B11 together. The group at x 675-870 is struck/overwritten; its end is uncertain. |

## c.90r (81477_doc42_c90r.jpg) - bare, postscript

| Block | Line | Crop | Before | After | Run x (crop px) | Notes |
|---|---|---|---|---|---|---|
| B1 | 14 | 090r_L14.png | Conte | non cessa | 1350-1430 | 2-sign code after "Conte" (a name?). Cipher or clear siglum? Uncertain. |
| B2 | 14 | 090r_L14.png | cessa di simolar | (line end) | 2265-3540 | Continues into B3. |
| B3 | 15 | 090r_L15.png | (line start, continues B2) | risponde | 300-1545 | |
| B4 | 15 | 090r_L15.png | formarsi (then "sa"?) | (line end) | 2625-3315 | "sa" just before the digits may be clear or cipher. Continues into B5. |
| B5 | 16 | 090r_L16.png | (line start, continues B4) | vuol? esser qllo et | 420-2130 | |
| B6 | 16 | 090r_L16.png | qllo et | (line end) | 2850-3360 | Starts with the "#"-like sign. Continues into B7. |
| B7 | 17 | 090r_L17.png | (line start, continues B6) | er dire | 420-960 | Raised small o over one sign (part of the sign). |
| B8 | 17 | 090r_L17.png | q primo quelaer? | p. | 2730-3300 | The extent is uncertain. The first 3 groups (x 2730-2950) may be clear words; the digits (x 2950-3300) are surely cipher. |
| B9 | 18 | 090r_L18.png | dice po et | non er? ancora | 1035-1125 | 2-digit code. |

## c.104r (81503_doc49_c104r.jpg) - bare

| Block | Line | Crop | Before | After | Run x (crop px) | Notes |
|---|---|---|---|---|---|---|
| B1 | 15 | 104r_L15.png | il sul papa | von domi...? / bon domi...? | 750-2085 | Starts with the "#"-like sign. Ends in a raised o. The task brief said ~14 lines down; by my count it is line 15. |

## c.177r (81651_doc81_c177r.jpg) - bare

| Block | Line | Crop | Before | After | Run x (crop px) | Notes |
|---|---|---|---|---|---|---|
| B1 | 3 | 177r_L03.png | in luogo: ne (end of L2) | are? mi racomando (L4) | 150-3480 (whole line) | Has internal spaces. Some short groups (e.g. at x~1400-1500) could be clear words, but I treat the whole line as one run. Contains the "#"-like sign. Whether the L4-initial "are"/"ase" belongs to the run is uncertain. |

## c.200r (81697_doc90_c200r.jpg) - bare

| Block | Line | Crop | Before | After | Run x (crop px) | Notes |
|---|---|---|---|---|---|---|
| B1 | 3 | 200r_L03.png | tentar da | el S. L. | 690-2415 | Second sign is the "#"-like sign. |

Counts: 176r 11 (B3 uncertain), 90r 9 (B1 uncertain; B2/B3, B4-B7 are line-break continuations), 104r 1, 177r 1, 200r 1.
