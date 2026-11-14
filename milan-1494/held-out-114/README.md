# Held-out test on Ridolfi doc. 114, and what its gloss taught

14 November 2026. Ridolfi's letter of 22 October 1494 (ASF MAP LXXIV doc. 114, cc. 258v and 259v) is in the same cipher as 112, 113 and 115 and carries a contemporary interlinear decipherment. It was not used in building the readings: its images were downloaded on 13 November with the rest of docs 97 to 115, and the working notes record no use of them. Brice Dudout tested our key on it first ([cyphersolver #589](https://github.com/dbourdeau/cyphersolver/issues/589)); Daniel Bourdeau asked us to run it as our own held-out test. This folder is that test, and then the use of 114's gloss as an exemplar set.

## The measurement

Protocol and hashes: [PREREGISTRATION.md](PREREGISTRATION.md), written before the cipher leaves or the printed text were opened by the session that scored.

- One agent located the cipher lines and painted out the gloss ([blocks.md](blocks.md)). A second agent, given only the masked crops, the label and shape inventory without values, and letters 112, 113, 115 as shape exemplars, transcribed 865 signs in 27 lines ([transcription-frozen.tsv](transcription-frozen.tsv), [its notes](transcription-blind-notes.md)). The file was hashed before the decoder ran.
- Key: `key.json` at commit 46dec7b, unchanged ([key-46dec7b.json](key-46dec7b.json)).
- Reference: the printed text in Desjardins and Canestrini, *Négociations diplomatiques de la France avec la Toscane*, t. I (1859), pp. 585-586 ([reference-desjardins.tsv](reference-desjardins.tsv)), fetched after the freeze.

| | Agreement | Best of 1,000 shuffled keys | Mean shuffle |
|---|---|---|---|
| **Pre-registered: any listed value of a sign counts** | **0.838** | 0.379 | 0.286 |
| First listed value only | 0.775 | | |

The bar was 0.85, so the key output on a blind transcription falls just short of it. Dudout's independent figure on the same letter was 0.774 against 0.397. `python3 score.py transcription-frozen.tsv reference-desjardins.tsv` reproduces [result-desjardins.txt](result-desjardins.txt).

What costs agreement: Desjardins prints a modernised text (*elezione* for the gloss's *electione*, *abbia* for *habbi*, *gli disse* for *li dixe*) and writes out what the cipher abbreviates or gives as one sign (*il Re*, *il duca*, *Sua Maestà*, *prefata*); the first three signs the transcriber took as cipher on c. 259v line 3 are probably the clear abbreviation *ch[e] q[ua]n[do]*; and the transcriber's own errors.

**After the fact, not pre-registered:** against the gloss as read from the leaf ([gloss/](gloss/), [reference-gloss.tsv](reference-gloss.tsv)) the same frozen transcription scores 0.886 (best shuffle 0.378). The gloss letters are 4 to 6 px tall and about a dozen spellings were settled by counting the cipher signs beneath them, so this figure is partly circular and is given only to show how much of the shortfall is the printed text.

## What the gloss gave

From here on 114 is no longer held out.

1. **÷ separates into n and c by its dots.** A third agent sorted every ÷ of 114 by what the ink shows, without values ([shapes/doc114-A.tsv](shapes/doc114-A.tsv)). Joined to the reference afterwards ([aligned-signs.tsv](aligned-signs.tsv)): a tick or dot above the dash is *n* in 32 of 34; a dot below only is *c* in 14 of 21. The mask had painted out much of the space around the signs in 114, so the same sort was repeated on the unmasked letters, by agents who had the labels but not the values: in 112, 113 and 115 a mark above (with or without a dot below) is *n* in 73 of 73 and a dot below only is *c* in 34 of 34, 34 and 20 of them in words where the word alone decides; in Alamanni's letter 12 of 12 and 6 of 6 in such words ([shapes/ridolfi-A.tsv](shapes/ridolfi-A.tsv), [shapes/alamanni-A.tsv](shapes/alamanni-A.tsv)).
2. **Ridolfi's d and l are different signs.** Both are a tall stem ending in an open hook. With a horizontal arm to the right at the baseline it is *l* (32 of 33 in 114; 32 of 32 in the three letters); without the arm, with or without a bar across the stem, it is *d* (38 of 43; 57 of 57).
3. **A sign for ll.** A d-shape with a long bar across its ascender stands in 114 where the gloss has *quella*, *alla*, *quello*, *fanciullo*, *Isabella*, *quelli*. In 112, 113 and 115 the same form gives *castello*, *a lla camera*, *ne lletto*, *della*, *quelli*, *quello*, *quella*, *Isabella*, *non volle*, *cavallaro*, *ne lla città*, *a lla corte*: fourteen uses, all words. In Alamanni's letter it is the sign we could not place in *mante[?]o*, which becomes *mantello*.
4. **bb** (cross with dots): *gioverebbe*, *harebbe*, *passerebbe*, *sarebbe*, 4 of 4.
5. **Person signs.** The long-tailed 2 with a raised c is glossed *Re* five times. The same base with another raised letter is glossed *Duca* twice ([gloss/signs.md](gloss/signs.md)); the raised letter is not clear enough to be sure it is the sign of letter 112, so that one stays inferred, now as [il Duca].

`apply_shapes.py` is the script that relabelled the two published transcriptions from the shape tables. Only signs sorted with high confidence were relabelled; the rest keep the two-valued label and their word keeps its tier.

## Gabbrielli's copy book

Dudout pointed to Gabbrielli's nineteenth-century *Chiavi delle cifre delle lettere ai Dieci di Balìa dal 1424 al 1530*, vol. 1, on Vincent Ilardi's microfilm reel 58 ([Yale Dataverse, doi:10.60600/YU/XKVOWE](https://doi.org/10.60600/YU/XKVOWE)). Read from frames 58-29 and 58-38:

- **No. 25, "Alamannis (de) Petrus", 1492, Dieci filza 39,** is the alphabet of MAP LXXII 183, as far as Gabbrielli recovered it (he has no b, g or z, and one sign for d). His "doppie" are ll (the barred d-shape), nn (the large e-loop), rr (the barred circle) and tt, and the ÷ forms he draws under C and under N look different, though the dots are hard to make out on the film. That corroborates the nn and rr we had only fitted, and it is where the ll sign was first seen. It is a reconstruction made from deciphered letters, three and a half centuries later, so it is corroboration and not a second key sheet.
- **No. 34, "Johannes Batta de Rydolphis", 1495, Dieci filze 40-42,** is a different alphabet, with its own doppie and name numbers. It does not bear on the October 1494 letters.

Not tested here: no. 25 against Alamanni's doc. 96 as a separate key (it is a subset of 183, so it would read what 183 reads), and nos. 13, 26 and 30.

The frames and the ASF images are not redistributed. The shape sorters' cut-outs are image crops and are not in the repository either; the tables give each sign's position.
