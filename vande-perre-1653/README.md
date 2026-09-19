# Vande Perre to de Bruyne, 1653: the Dutch cipher in Thurloe

**Status: solved, 14 September 2026; four letters read, three code groups and two short
fragments open.** A 22-letter monoalphabetic substitution with a few code groups, in Dutch, with
Dutch words as ciphertext runs inside English translations of the letters. Of 291 printed
symbols, 277 are S (key found by cryptanalysis, with a control), 3 M (unread code groups), 11 I
(repairs of evident misprints). No H or C tokens: this is a cryptanalytic result. Birch's
English glosses over some runs were not used to find the key, and they agree with it.

## The documents

Johan van de Perre, one of the Dutch ambassadors in London during the peace talks of 1653, to
Johan de Bruyne, raadpensionaris of Zeeland, in Birch's *A Collection of the State Papers of
John Thurloe*, vol. 1 (1742). Thurloe's office intercepted the letters and made English
translations, in which the ciphered words were left as numbers. Birch printed the translations
with the numbers. Page images are from the Internet Archive scan
[collectionofstat01thur](https://archive.org/details/collectionofstat01thur); British History
Online omits the cipher passages ("see page image").

| Run | Page (IA leaf) | Letter |
|---|---|---|
| P500.1–3 | [p. 500](https://archive.org/details/collectionofstat01thur/page/n529) | Westminster, 3 October 1653 NS |
| P522.1–5 | [p. 522](https://archive.org/details/collectionofstat01thur/page/n551) | October 1653, "my last was the 3d of this month" |
| P576.1 | [p. 576](https://archive.org/details/collectionofstat01thur/page/n605) | London, 4/14 November 1653 (begins p. 575) |
| P582.1–6 | [p. 582](https://archive.org/details/collectionofstat01thur/page/n611) | Westminster, 11/21 November 1653 |

Satoshi Tomokiyo's [unsolved list](https://cryptiana.web.fc2.com/code/unsolved.htm) says Thurloe
"include[s] some undeciphered Dutch letters", naming Beverning and Vande Perre to Boreel,
1 September 1653 (p. 435) as the example. That letter uses a different cipher and remains open
(see Failure log). Bourdeau's [cyphersolver](https://github.com/dbourdeau/cyphersolver/tree/main/thurloe)
works on the Boreel letter and three 1656 intercepts, not these. DECODE has no record for any of
them (searched 19 September 2026 for Perre, Bruyne, Bruijne, Beverning, Nieupoort, Zeeland,
Thurloe). The English glosses show that Thurloe's office read at least parts of the cipher in
1653. We have found no published Dutch text or key.

## The reading

Mechanical output of [`verify.py`](verify.py) ([`reading.txt`](reading.txt)): the key over the
printed digits, then with [`repairs.json`](repairs.json) applied. `(..)` is an unread code group,
`[..]` a repair. Clear text from Birch's translation in quotes, for context. [`pages/`](pages/) has a
crop of each run as printed (public-domain 1742 edition, from the Internet Archive scan); the
[reading page](https://aaymeloglu.github.io/unsolved-ciphers/vandeperre-reading.html) shows them
next to the decoded text.

| Run | Context | Edited reading | Dutch | English |
|---|---|---|---|---|
| P500.1 | "keep me at present out of harm's way." | `in(?)nviandichland` | in [57] n viandich land | in [?] hostile country |
| P500.2 | "that at present here" | `eenredelijckedisposi[t]ietothandelingewertgespe[u]rtdieweldiendewaergenomen` | een redelijcke dispositie tot handelinge wert gespeurt, die wel diende waergenomen | a reasonable disposition to negotiate is noticed, which ought to be taken up |
| P500.3 | "We hear that many of" | `regeringemetimpatientieopnaderordrevano[n]sverwac` | regeringe met impatientie op nader ordre van ons verwac[hten] | the government await further orders from us with impatience |
| P522.1 | "which we very much long for." | `(?)goededisposi[t]ie` | [617] goede dispositie | [617] good disposition |
| P522.2 | "a person" | `diemnicvndament` | unresolved | Birch: "who upon good grounds" |
| P522.3 | "in case" | `wijgeq[u]alifi[c][ee]rteenigenaderepropositi[e]doen` | wij gequalificeert eenige nadere propositie doen | we [were] authorised to make some further proposal |
| P522.4 | "the work" | `tenprincipaln` | ten principal[e]n | chiefly |
| P522.5 | "within" | `[14]daghen` | 14 daghen | fourteen days |
| P576.1 | "The said change is" | `onstotvoordeelgerekent` | ons tot voordeel gerekent | reckoned to our advantage |
| P582.1 | "the men of" | `thien[s]chepen` | thien schepen | ten ships |
| P582.2 | "to" | `(?)geloope[n]` | [115] geloopen | run [115] |
| P582.3 | "to look to them" | `bewaren` | bewaren | to guard |
| P582.4 | "the fleet" | `ote` | unresolved | |
| P582.5–6 | "want of masts." | `gebreck` van `masten` | gebreck van masten bevonden | want of masts found |

Birch's glosses, all consistent with the key: "the good dispositions do" (P522.1), "who upon good
grounds" (P522.2), "we were qualified with some farther propositions that would do" (P522.3),
"chiefly" (P522.4), "fourteen days" (P522.5), "ten ships at Yarmouth" (P582.1), "were run away"
and "left" (P582.2). The key reads *wij* ("we"), *gequalificeert* ("qualified"), *nadere
propositie* ("farther propositions"), *principalen* ("chiefly"), *thien schepen* ("ten ships")
and *geloopen* ("run") under the glosses without using them. P576.1 has no gloss.

## Key

[`key.json`](key.json). Values run in alphabetical order with gaps, the usual shape of a
mid-century Dutch diplomatic alphabet:

| 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | frac | 12 | 13 | 14 | 15 | 17 | 21 | 22 | 23 | 24 | 26 | 27 | 28 | 29 |
|---|---|---|---|---|---|---|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| a | b | c | d | e | f | g | h | ij | i | k | l | m | n | o | p | q | r | s | t | v | w |

`frac` is the sort Birch sets for 11: a small 1 over 1 beside a small 2 over 2. It reads *ij*
in *redelijcke* and *wij*. Numbers 1, 2, 16, 18–20 and 25 do not occur as letters. The three
code groups 57, 617 and 115 occur once each and stay unread; Birch's glosses suggest 617 is an
article or *de* and 115 is *wech* ("away"), but one occurrence cannot settle either.

## Repairs (grade I)

Every change to the printed digits is in [`repairs.json`](repairs.json) with its reason; the
transcription is not altered.

- *dispositie* is enciphered with 14 (l) for its *t* in both letters that use the word
  (P500.2, P522.1), while 27 is *t* everywhere else (*tot*, *met*, *wert*, *masten*). A slip in
  the writer's key or the decipherer's copy for this word; the text needs *t*.
- *gespeurt* and *gequalificeert* need *u* where the print has 17 (n). Either *u* was written
  with the n-symbol or the print confuses 16 and 17 (16 is never printed).
- Birch's "12. 15. 77." in *gequalificeert* is 12. 5. 7. 7. with the full stops misplaced;
  "71" in *propositie* is "7." with a stray 1.
- 27 (t) for 17 (n) in *ons* (P500.3) and for 26 (s) in *schepen* (P582.1).
- "1" at a line end in P582.2 is 17 with the 7 dropped (*geloopen*).
- In P522.5 the first "14" is the numeral fourteen in clear, as Birch's gloss says; as the
  l-symbol it gives no word.

## Method and what the controls say

The key was found on 14 September 2026 by bijective simulated annealing over a 4-gram model
built from Hooft's *Nederlandsche Historien* (1642, DBNL text `hoof001nede01`, not in this repo):
four of eight restarts converged on the same key, and the few remaining values were read by hand.
The glosses were not used as cribs.

Reproducible here, with the kit's Dutch corpus (`cipherkit.corpora` id `nl`: Vondel, *Complete
werken* I, and Multatuli, *Max Havelaar*):

- `python3 vande-perre-1653/verify.py --z`: key-shuffle permutation (the kit's
  `permutation_z_key`, dictionary segmentation, printed digits without repairs, 1000 shuffles):
  **z = 4.2, p = 0.001**. No shuffled key scores as well as the key. The z is modest because the
  text is 285 letters in short runs.
- `python3 vande-perre-1653/solve.py`: ciphertext-only search with the kit's annealer and
  hill-climb over 16 seeds. The best seeds recover 16–19 of the 22 values (about 90 percent of
  the letters), confusing v/w and c/k/z. Under the same model `key.json` scores −1288.6, better
  than every search result (best −1297.0), so the shortfall is in the search, not a competing key
  the model prefers. The 17th-century prose corpus used for the original search did better than
  the kit's mix of verse and 1860 prose.

## Open points

- The three code groups 57, 617, 115. In P500.1, *in [57] nviandich land*: if 57 stood for *ee*
  the run would read *in een viandich land* ("in a hostile country"), a conjecture only.
- P522.2 `diemnicvndament`, glossed "who upon good grounds": *die m…* and *…fundament* look
  right, but the letters between do not divide into Dutch as printed.
- P582.4 `ote`, "the fleet [ote] will not go out": unresolved; possibly a misprint.
- An earlier Vande Perre letter in the same volume, a few pages before p. 435, has a short run after
  "a character to open a lockt chest", `12. 5. 13. 26. 7. 9. 9. 10. 7.` (*ick segghe*, "I say",
  under this key) followed by symbols the OCR garbles. Not yet checked against the page image.

## Failure log

- Beverning and Vande Perre to Boreel, 1 September 1653 (p. 435): a different system (letters
  6–33, codes 113–527); 128 letters, calibrated Dutch band −614 to −554, attacks top out at −650.
  Closed-negative 14 September 2026; needs more ciphertext in the same key or a Dutch-side crib.

## Files

- `transcription.txt`: every run as printed, with the clear text before it and Birch's glosses.
- `key.json`, `repairs.json`: the key and the proposed misprint repairs, graded.
- `verify.py`: reproduces `reading.txt`, prints grade counts, `--z` for the control. Run in CI.
- `solve.py`: the ciphertext-only search.
- `pages/`: a crop of each run from Birch's page, used by the reading page.
