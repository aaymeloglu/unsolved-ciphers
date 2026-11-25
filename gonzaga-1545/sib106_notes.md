# Sibling cc. 106-110 (record 32883bf0): notes

Ercole Gonzaga to Ferrante, Mantua 10 July 1544, forwarding news "Di Venetia alli vj di luglio".

## Which image is which

The task note's file numbers are off by two. As found:

| file | what |
|---|---|
| `_01` | c. 106r, covering letter in the cardinal's own hand, with a short cipher run inside it (block C) |
| `_03`, `_04` | cc. 107r-v, period decipherment, headed "sgifrato di mant.a colle lre dil x. Julio del 44" (25 + 10 lines) |
| `_07` | c. 109r, cipher, 28 lines (block A) |
| `_08` | c. 109v, cipher, 5 lines (block B) |
| `_02`, `_05`, `_09` | blank versos (show-through only) |
| `_06` | verso with a sideways docket |
| `_10` | address |

Check: A01 decodes by the swap to "[27] da [L25] alli sei di luglio [24] e ueto che il strozzi e uenuto", the clear's first line.

## Coverage

The clear covers the whole cipher, A01 to B05, with nothing left over. The cipher ends "...da inuestire 24 27" and the clear ends "da inuestir." The run on `_01` (block C) has no period decipherment; it decodes by the swap as
"[24] l'ambasciator Agnello che [in clear: è uenuto qui m'ha] detto hauerli da gen(ge an) gentil homo di Vinegia [25]" (the middle has what looks like a false start; unverified).

## How the transcription was made

Digit groups and L groups: by shape. Every single-occurrence group, and at least one occurrence of every other group, was checked at 3x (all of page B, and all of 5, 11, 12, 16, 17, 18, 6o, 67, 68, 78, L2, L10, L25). Letter runs: at about 1.5x, after the clear had been read, so g/z/q and c/e were often settled by sense. Treat the letters as a guided reading, the codes as an independent one. `/private/tmp/claude-501/-Users-aaymeloglu--claude-assistant/ec467959-a5f2-464e-aef6-4186a124175c/scratchpad/codes-106/decode.py` (scratch, will not survive cleanup) applies the swap and the code table to `sib106_transcription.txt`; the counts in the TSV come from it.

## New against glyphs.md

- **More doubling signs, all confirmed by spelled-out neighbours:** 11 = ff, 12 = dd, 17 = pp, and bare **5 = cc** (5 times). With 14 ll, 16 nn, 18 rr, 19 ss, 2o tt the series runs 11-19 in rough alphabetical order of the consonant (f, d, ?, l, ?, n, p, r, s), so 13 and 15 are probably doubles too (gg, mm?). The bare `8` of c. 96 ("de8a") fits a single-digit double like 5: bb is likely.
- **Plain z** is written with a z-shaped sign identical to the 2 of 2o/24/25 (transcribed `22` in "strozzi", 6 times). The swap's cipher m for plain z does not occur.
- **Word codes:** 6o qualche, 31 io, 35 V. Ex., 39 questo, 57 cosa, 58 quando, 59 quanto, 67 pur, 68 come, 73 ancora, 74 Italia, 75 Italiani, 78 Franza.
  - 39 and 73 settle c. 96 line 12: "39 ho 73 inteso" = "questo ho ancora inteso".
  - The tens seem grouped: 3x pronouns (31 io, 35 V. Ex., 39 questo), 5x/6x particles (53 non, 57 cosa, 58 quando, 59 quanto, 64 perche, 67 pur, 68 come, 69 cosi), 7x includes places (74 Italia, 75 Italiani, 78 Franza) but also 73 ancora.
- **L codes:** L25 = Venetia; L2 (or L7) = Re di Franza. L10 = Papa confirmed 3 times.
- **A third null:** bare 25, beside 24 and 27. 27 opens the text, "24 27" closes it; 24 is strewn inside sentences (11 times), once between "non ha" and "hauuto"; 27 once stands inside a sentence ("sa-|ra 27 auisata"). Every null on these pages stands at a word boundary, never inside a word.

## Confirmed from glyphs.md

14 ll, 16 nn, 18 rr, 19 ss, 2o tt, 3o che, 4o quello, 53 non, 64 perche, bare L = et, L10 = Papa, 24 and 27 null. No contradiction.

Not on these pages: L43, `L 43`, L14, 45, 69, bare 8. So the L43 / `L 43` size rule could not be tested. All three L groups here have a small raised number; bare 14 (ll, 10 times) and bare 25 (null) are full size on the baseline, which supports keeping L14 apart from 14 and L25 apart from 25.

## Misfits

- **"r h r g b" twice (A01, A05) where the clear has "È vero".** The fourth sign is a g with a closed lower loop both times; by the swap this is "ueto". Either the scribe has an e form with a looped descender, or the same slip twice. Elsewhere "uera" (A24) has an ordinary e.
- **A19 "e b 22 n" = "rozza" where the clear has "rotta"** (2o would be expected). Same sign pair as in "strozzi" three signs earlier; probably the encipherer's slip, read by sense by the decipherer.
- A05 end: second digit of a 6x group is under an ink blot; the clear ("Cosa come") and A28 point to 68.
- A09: a blotted sign after "q r a n e" (denaro); A26: a struck sign after "corre".
- **Bare 5 (cc) and short s (plain f) have the same shape.** Side by side at 4x (5 in tocca, uecchi, accelerar, eccetto; s in far, fin, frontiere) I cannot separate them; only sense does. On an undeciphered page a 5-shape between vowels may be either cc or f.
- **L2:** the raised sign has the z-like form of the 2 in 27 and L25 with a short foot stroke, so 2 is likelier than 7, but it is small and stands alone.
- A20: the two signs I give as `{u/n} {n/u}` in "hauera" are an a-like sign plus minims; read by sense.
- A03: one sign unread inside "logo" (y b . t ? ), and "regionando" rather than "ragionando" as I read it.

## Cipher wording vs clear

The decipherer normalises freely:

- A02 "sodisfatto" / "satisfatto"; "risolutione", "nouo", "denari", "po", "homo" / "resolutione", "nuouo", "dinari", "può", "huomo".
- A04 "potesse tale che ui cadesse" / "potessi tal [che] ui cade[sse]".
- A06 "sborsar se non": the clear adds "dinari".
- A07 "dell aiuto" / "dl'ayuto".
- A10 "a lui" with one l / "allui"; "contanti" has its second a added above the line.
- A13 "ancora" (code 73) / "anchor"; A14 "fin che" / "sin che"; A15 "mila" / "miglia".
- A17 "il [L2]" / "Il Re di franza". In the clear "Italiani" is written above a struck word, so code 75 was first read as something else.
- A19 "il strozzi" / "piero strozzi" (no "piero" in the cipher); "otto mila" / "otto m."; A20 "uenti" / "xx".
- A21 "di san secondo" spelled out / "di sans.do".
- A25 "di [Papa] paulo" / "del Papa paulo".
- A27 "et per tal causa le prouisioni" / "Et per questo le prouisioni".
- A28 "munire", "inuestire" / "munir", "inuestir".
- B01 "uescouo di pauia" spelled out; this fixed my reading of the clear's "ves.o di Pauia".
- B04 "la da uiuere" / "[qui?] da Viuer"; B05 "quattro mila scudi" / "quattro m. V".
- Numbers are spelled out in the cipher (sei, dodeci mila, uenti, otto mila, quattro mila); no digit group stands for a number.

Names spelled out, so no code seen for them: Strozzi, Conte della Mirandola, Pitigliano, Scotia, Polino, Turco, Piemonte, San Secondo, Roma, Paulo, Pauia, re (twice), Francia (once, B03), Agnello, Vinegia (block C).

## Autograph forms (block C)

In the cardinal's own hand the y sign is a large looped figure like an 8 with a crossing stroke, and q and g are both g-shaped. The X-like mark before "zifra" in the clear line above is a different sign, not part of the cipher.
