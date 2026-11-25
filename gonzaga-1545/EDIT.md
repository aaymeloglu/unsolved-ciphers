# Editing a page: from the frozen transcription to the Italian text

Three readers transcribed each page by shape, without decoding (`transcription/<page>.A.txt`,
`.B.txt`, and the third reader's `.C.txt`, which is frozen: its SHA-256 is in
`transcription/FROZEN.sha256` and it must not be edited). `decode/<page>.txt` is `.C.txt` put
through the key (`key.tsv`, applied by `decode.py`): letters by the swap, `[word]` for word and
name codes, `<group>` for a group with no value in the key, `{x/y}` where the reader left a doubt.

The decode reads as Italian but is full of single-sign slips, because in this hand some signs
cannot be told apart reliably by shape. You are the editor: you read Italian of the 1540s, you
have the image, and you settle the text.

## What you may change, and how it is recorded

You write `edition/<page>.cipher.txt`: the page's cipher signs, one line per manuscript line, in
the same notation as the passes, as you judge they stand on the page. Start from `.C.txt`. Every
sign you write differently from `.C.txt` is a departure and will be counted by a script, so:

- **Look-alike departures.** You may replace a sign by one of its look-alikes when the word
  requires it AND the shape on the page permits it. The look-alike classes (cipher signs):
  d/y; c/e; a/n; n/r; n/u; a/u; g/z; g/q; q/z; e/y and e/d (the final e with a rising loop);
  the long-stem sign h against `f n` or `f r` (and `f` alone); b/h; b/o; s/5; f/t; r/x; p/q;
  a lone minim + figure against a doubling group (`1 z` = `19`, etc.); a sign one reader has and
  another lacks. Passes A and B often already have the right sign: check them first.
  Look at the place on the image (enlarge to 4x or more) for every departure. If the shape
  permits your reading, make it.
- **Emendations.** If the word requires a sign that the shape on the page does NOT permit (the
  scribe's slip, or a sign outside the classes), do not write it into the cipher line silently:
  write the sign you want followed by `!`, e.g. `g!`. These are counted separately as
  emendations and shown in brackets in the text.
- **Open.** If you cannot tell what a word is, leave the signs as `.C.txt` has them (keep its
  `{a/b}` or `?`). Do not force a word. A hole is better than a guess.
- Do not add, drop or reorder signs except where a reader doubled or dropped one (check the image).
- Codes: use only values in `key.tsv`. A group with no value stays as it is and shows as `<..>`
  in the text. If context makes its meaning plain, say so in your notes with the evidence; do not
  put the guess into the text. If you think a group was misread (e.g. `L9` for `L10`), treat it
  like any other sign: look at the image.

## The Italian text

Write `edition/<page>.it.txt`: one line per manuscript line, the decode of your cipher line
divided into words. Rules, so that a script can check it against the cipher line:

- The letters must be exactly what your cipher line decodes to, in order. Keep the scribe's
  spelling (u for v, no accents, no apostrophes, doubled letters as written). Only add spaces.
- A word broken at the line end ends with `-` and continues on the next line.
- Word and name codes appear as `[che]`, `[Papa]`, exactly as `decode.py` prints them. Groups
  without a value appear as `<L3o>`. Nulls disappear.
- An emended sign's letter is written in square brackets inside the word: `ter[r]e`.
- A sign left in doubt appears as `{x/y}`, an unread sign as `?`, exactly as the decode prints.

Check your work: from the repo root run
`uv run python gonzaga-1545/check_edition.py <page>`; it must report that the Italian matches the
cipher line on every line, and it lists your departures by class.

## Notes

Write `edition/<page>.notes.md`: (1) words or passages you could not read, with line numbers;
(2) every emendation `!` with a phrase of reason; (3) what you think each unvalued code group
means and why (context on this page and on the others: you may read every `decode/*.txt`);
(4) persons, places and events you recognise, briefly; (5) any place where the three passes and
the image left you choosing between two real words.

The first page of a letter may start mid-sentence only if a leaf is missing; pages run on:
letter A is A78r, A78v, A79r; letter B is B174r, B174v, B175r, B175v. Read the end of the
previous page's decode and the start of the next so that words broken across pages come out.
