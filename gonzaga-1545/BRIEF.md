# gonzaga-1545 working brief (agents read this first)

Target: Cardinal Ercole Gonzaga (Mantua) to his brother Ferrante Gonzaga, two letters of 1545 almost
wholly in cipher, Biblioteca Estense, Autografoteca Campori (Cyphersolver catalogue 1556).
Images (full resolution, colour, local, not committed) are in `images/`:

| page label | file | what |
|---|---|---|
| | `6b71f191_01.jpg` | letter A, c. 77r: a page in clear in the cardinal's own hand |
| A78r | `6b71f191_03.jpg` | letter A cipher, c. 78r (29 lines) |
| A78v | `6b71f191_04.jpg` | letter A cipher, c. 78v (27 lines) |
| A79r | `6b71f191_05.jpg` | letter A cipher, c. 79r (15 lines) |
| | `6b71f191_06.jpg` | letter A address and docket |
| B174r | `9a179607_01.jpg` | letter B cipher, c. 174r (25 lines) |
| B174v | `9a179607_02.jpg` | letter B cipher, c. 174v (26 lines) |
| B175r | `9a179607_03.jpg` | letter B cipher, c. 175r (26 lines) |
| B175v | `9a179607_04.jpg` | letter B cipher, c. 175v (26 lines) |
| | `8fb56845_07.jpg` | SIBLING c. 96r: cipher of 1544, same system, with its period decipherment |
| | `8fb56845_04.jpg`, `8fb56845_05.jpg` | period decipherment of c. 96 ("Co' lre di Mant.a iiij di luglio. Da Roma a XXV di Giugno ...") |
| | `2c1077f1_*.jpg`, `32883bf0_*.jpg` | more 1544 siblings (cc. 102-105, 106-110) with cipher pages and period decipherments |

Line bands are in `layout/<page>.layout.json` (made by `cipherkit.transcribe layout`). `halves/<page>/<page>-L07a.png`
and `...-L07b.png` are the left and right halves of line 7, overlapping by a few signs, padded so
ascenders and descenders are whole, enlarged 1.5x (made by `make_strips.py`). Parts of the lines above
and below show at the top and bottom edge of each strip: the line to read is the one in the middle.

## The system (established 24 Nov 2026 on c. 96 against its period decipherment)

A reciprocal half-alphabet swap over 22 letters, written in ordinary italic minuscules:

    a<->n  b<->o  c<->p  d<->q  e<->r  f<->s  g<->t  h<->u  i<->x  l<->y  m<->z

(u and v are one letter; plaintext "venetia" is written h x a r g x n, read as uenegia). Besides the
letters there are digit groups and `L` plus superscript number groups (`L43`, `L4`, `L10` ...) that are
codes for names and common words, and special signs for doubled letters (for example a sign like `2o`
for `tt`). Words are run together with occasional spaces.

## The hard part is the glyphs, not the key

The scribe's letter forms are confusable, and one careless transcription character merged several
different signs. Known confusions so far:

- a `9`-shaped sign (closed bowl, descender) is cipher `z` (plain m), not `g`;
- `g` (plain t) and `q` (plain d) both have descenders;
- a looped `d`-like sign is cipher `y` (plain l); a true `d` is plain q;
- an `e` with an accent or hook can be cipher `e` (plain r) where it looks like `i`;
- digits sit inside words as signs, and standalone as codes; `3o` looks like `zo` and `2` like `z`.

## Transcription rules

- Transcribe what is on the page, sign by sign, one output line per manuscript line, numbered.
- Use the cipher letter you see (a b c d e f g h i l m n o p q r s t u x y z), digits as digits,
  `L` codes as `L43`, and keep spaces where the scribe left a clear gap.
- When a sign could be two things, write `{g/z}` (most likely first). Unreadable: `?`.
- Never repair a sign to make Italian.
