# Masking notes - c.176r

## Method
- `crop_lines.py`: for each cipher line I placed two baseline points by eye. The page is rotated about the left point so the baseline is horizontal. Then a band is cropped (page x 50-1250; 60 px above, 26 px below the baseline for 176r; 56/40 for the bare leaves) and upscaled 3x with LANCZOS. Rotation fill = paper colour (70th-percentile luminance of the page).
- `mask_176r.py`: gloss regions are hand-drawn rectangles/polygons in each band's 1x coordinates. They are mapped back to page coordinates and painted on a copy of the whole page. So gloss that hangs into the neighbouring line's band (L19/L20, L22/L23) is removed in both crops. "Keep" polygons are subtracted from the paint mask to protect cipher strokes.
- Fill = local paper estimate: 11 px max filter (removes dark ink), then a 3 px Gaussian blur. Mask edge softened by 0.8 px. The patches are visibly smoother than the paper, so painted areas can be spotted. That is cosmetic; no gloss letters are left.
- Checked every masked band at 2-6x (red-tint overlays of the painted area plus before/after zooms) and iterated until nothing gloss-like was readable.

## Protected cipher strokes / spots where gloss touched cipher
- L19 x~130-147 (band px): small raised "o" over the 3rd sign of B2. Kept as cipher; the gloss on either side is painted.
- L19 x~886-893: ascender of the sign under the gloss's last letters. Kept. A few px of gloss stroke beside it survive (not readable).
- L19 x~838-850, y 43-50: top of a cipher sign right under the gloss. Kept.
- L20 x~424-441: a long stroke runs from gloss level down into the cipher line (descender of the cipher's 4-like sign). The lower part (y>=43) is kept; the upper part is painted along with the gloss.
- L20 x~553-561, y 48-56: dot above a dash (division-like sign) touching the bottom of a gloss letter. Dot kept. A sliver of the gloss letter's foot may remain merged with the dot.
- L20 x~806-818, y 38-48: top of a cipher sign under the gloss. Kept.
- L21 x~327-339, y 27-39: dot above a dash. Kept.
- L21 x~417-426, y 0-24 and x~434-452, y 39-70: top of an L20 cipher descender and the cipher's dagger-like sign (its top dot sits in the gloss zone). Kept.
- L22 x~503-516, y 0-26: L21 descender. Kept.
- L22 x~779-794, y 48-72: cipher sign whose ascender touches a gloss letter. The gloss letter is painted down to y 49; the ascender stub is kept.
- L22 x~716-727: the gloss's last letter overlaps the ascender of the "b"-like cipher sign. Painted only to x 727. A tiny bit of gloss may remain fused to the ascender.
- L17 x~210-256: gloss mark over the struck 2-sign group. Painted down to y 30 (y 37 in the middle). The cipher sign below starts at y~38 and is untouched.

## Not masked (on purpose)
- Long thin horizontal pen strokes in gloss ink with nothing letter-like: above L20 x~890-1200, L21 x~590-870 (curving into a dark sign at x~765-790, unclear whether gloss or cipher), L22 x~1000-1150, L23 x~160-300, L28 x~80-240. They give no reading, and some cross cipher ascenders, so they were left in place.
- The horizontal strike through the L17 group (B1) is in cipher-line ink and belongs to the original line, so it was not masked.
- 176r_L28 has no gloss of its own. Its masked crop differs from the unmasked one only where the L27 gloss reaches the top edge (right end).

## Files
- `work/176r_masked_page.png` - whole page with gloss painted out. `work/176r_paintmask.png` - binary paint mask.
- `work/dbg/` - 1x bands (unmasked `*.png`, masked `*_m.png`, overlays `ov_*.png`) used for checking. `dbg/*.png` without `_m` show the gloss; don't hand those to the blind reader.
