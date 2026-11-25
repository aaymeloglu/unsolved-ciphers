# Settling the open spots of a page (third reader)

Two independent readers transcribed each page (`transcription/<page>.A.txt`, `.B.txt`, each with a
`.notes.md`). `transcription/<page>.AB.txt` is their merge: one line per manuscript line, tokens
they agree on as plain tokens, and open spots in braces:

- `{a/b}`: the readers differ (or both doubted): the candidates are listed;
- `{x/?}`: only one reader has a sign here, so either a sign is missing from the other pass or
  one reader split a single sign in two (the commonest causes: `f r` or `f n` against the long
  form of `h`; a lone minim against the 1 of `14 16 18 19`; `s` against `5` in a digit group);
- `?`: unread by both.

Your job is to settle each open spot from the image and nothing else.

1. Read `BRIEF.md` and all of `glyphs.md` (sections 1, 2 and 6) and look at the comparison sheets
   in `glyphs/`. You may read both readers' notes for the page.
2. For each line with open spots, find each spot on the page (read along the half-line strips
   `halves/<page>/` with the merged line beside you; plain tokens are your landmarks), cut an
   enlargement of 4x or more with a few neighbours for scale (via `layout/<page>.layout.json` and
   `cipherkit.transcribe.prepare`, as in TRANSCRIBE.md), and decide by shape, using the rules of
   `glyphs.md`. Compare with a plain instance of each candidate sign from the same line or a
   neighbouring one where you can.
3. **Decide by shape. Do not decode**, and do not open `decode/` or any unsuffixed
   `transcription/<page>.txt`. The candidates are not exhaustive: if the sign is neither, write
   what it is.
4. Where the shape truly does not decide, keep `{a/b}` with the likelier first. Keep `?` only for
   a sign that is blotted or lost. Expect to settle most spots.
5. While you are on a line, if you see that a plain token next to an open spot is wrong, or that
   the token count is off (a sign both readers dropped or doubled), correct it and say so.
6. Output `transcription/<page>.C.txt` (same format as the passes: one line per manuscript line,
   no numbers, no comments) and `transcription/<page>.C.notes.md`: for every open spot, the line,
   approximate x, the candidates, your decision and one phrase of reason; then a list of any
   other corrections; then how many spots stay open. Append to the output as you finish lines.
