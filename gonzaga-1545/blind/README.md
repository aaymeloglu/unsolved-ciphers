# Blind checks

What the checks in the main README rest on. No images are kept here.

- `R1.tsv`, `R2.tsv`: two readers' transcriptions, by shape, of 59 unlabelled crops (`c01`–`c60`,
  no `c53`). They had the crops and a description of the sign shapes, and no text of the letters.
- `crops-set1.key.json`, `crops-set2.key.json`: which page, line and signs each crop was cut from,
  with the edition's signs at the time of cutting. `make_crops_set1.py` and `make_crops_set2.py`
  cut them (`uv run python gonzaga-1545/blind/make_crops_set1.py key.json outdir`; they need the
  page images). Sets: `name` places, persons and numbers; `code` name codes; `stem` the six *ge*
  places and *diligentemente*; `c_h`, `c_tr`, `c_fn` controls for the tall-stemmed signs.
- `compare_crops.py`: scores both readers against the key files.
- `B174r-second-edit/`: an independent edit of B174r made from a checkout with no edition in it.
  `compare_second_edit.py` compares it with `edition/B174r.it.txt` word by word. Before two of its
  readings were adopted the agreement was 317 of 327 words; the Vatican-collated edition agrees on 321 of 328.

## The docket of letter A

A reader given only a crop of the note of receipt on the address leaf, and asked to report what the ink
shows, returned:

    raised above line 1: "le" over "Cav", then the figures "54" over "di"
    line 1: Cav^le. di Mant^a. 4 di
    line 2: Maggio

Day figure 4: high confidence. Raised second figure 4: high. Raised first figure: read as 5,
moderate to high, "a vertical stem with a small flag at its top; from mid-stem a flat bar runs
right, then a diagonal comes back down to the foot of the stem, closing a bowl"; alternatives 6 or
b. The same first figure stands in the raised year on the dockets of cc. 102-105 and 106-110,
whose covering letters are dated July 1544 in clear, so it is taken as 4. That comparison was made
by me with the date in mind, not blind.
