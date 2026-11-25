# Transcribing a page (pass instructions)

You are one of several independent readers. Your pass is compared sign by sign with another
reader's, so do not look at any other file in `transcription/`.

1. Read `BRIEF.md`, then `glyphs.md` sections 1 and 2 (shapes and code groups), and look at the
   comparison sheets `glyphs/compare_dy.png`, `compare_qgzt.png`, `compare_ce.png`, `compare_L.png`
   and a few exemplars of each sign you are unsure of.
2. Work from `halves/<page>/<page>-LNNa.png` and `...b.png` (left and right half of line NN, a few
   signs of overlap; the line to read is the one in the middle of the strip). Where a sign is
   doubtful, cut your own enlargement (3-4x) from the page image through the layout file
   (`layout/<page>.layout.json`: rotate the source by `processing.rotate` with
   `cipherkit.transcribe.prepare`, bands are [top, bottom]) and look again. Put scratch crops in
   your scratch directory, not in the repo.
3. **Transcribe by shape. Do not decode.** You know the key, and it is tempting to read ahead in
   Italian and write the sign the word needs. Do not: the transcription is frozen before anyone
   decodes it, and its value is that it is a record of the page. If a sign's shape is between two
   signs, write `{a/b}` with the likelier shape first. Unreadable: `?`. Struck-out signs: leave
   them out and say so in the notes. Signs written above the line as an insertion: put them where
   the caret points and say so in the notes.
4. Output `transcription/<page>.<pass>.txt`: exactly one line of text per manuscript line, in
   order, no line numbers, no blank lines, no comments. Signs separated by single spaces. Letters
   as the cipher letter you see; digit groups as written (`27`, `3o`, `2o`, `14` ...); `L` codes
   as `L43` when the number is small and raised against the L, or `L 43` when a full-size L is
   followed by full-size digits; a bare `L` alone as `L`. Mark a gap clearly wider than letter
   spacing with `|` as its own token.
5. Output `transcription/<page>.<pass>.notes.md`: per line, anything a later reader needs (which
   signs you enlarged and why, insertions, deletions, damage, show-through), any sign or code
   group that is not in `glyphs.md` (describe its shape and give line and x position), and your
   own estimate of how many signs on the page are doubtful.

The line count for each page is in `BRIEF.md`. If you find the layout has merged or split a line,
keep one output line per real manuscript line and say so at the top of the notes.
