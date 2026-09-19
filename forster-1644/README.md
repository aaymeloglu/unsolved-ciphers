# Sir Richard Forster's ciphered letter, 13 May 1644: decipherment (2026-09-14)

**Grades** ([CONVENTIONS.md](../CONVENTIONS.md)): 204 of 207 tokens S (read under a key found ciphertext-only; key-shuffle permutation z = 11.2, token-shuffle z = 15.3, see "Permutation tests" below), 3 tokens I (the explicit emendations); no H or C, since no key source or contemporary decipherment is known. `python3 verify_solution.py` prints the counts; `uv run python permutation.py` reproduces the z values.

**Side-by-side reading:** [ciphertext, French and English](https://aaymeloglu.github.io/unsolved-ciphers/forster-reading.html).

**Earlier decipherments:** this was not the first reading. Karen Britland told Robert Pitt that George Lasry supplied a decipherment after her 2013 article and that Norbert Biermann reached the same solution independently; Pitt reports this in his [forster-cipher](https://github.com/robertpitt/forster-cipher) repository, published a few hours before this one on 14 September 2026. His key and ours were reached separately and are identical. The earlier reading Britland passed on differs in a few words (*aucune voie*, *preveu seulement*, *soupir*). No priority is claimed here.

**Status before:** listed as undeciphered on Satoshi Tomokiyo's Cryptiana ("Unsolved Historical Ciphers", updated 2026-09-06; transcription in his 2021-09 blog post). Described but not read in Karen Britland, "Reading between the lines: royalist letters and encryption in the English civil wars", *Critical Quarterly* 55/4 (2013). Letter is in Forster's hand, among his papers; Forster was treasurer of Henrietta Maria's household.

**Ciphertext (Tomokiyo's transcription; commas = word breaks, line breaks = wrapping):** see `ct.txt`.

## Key

Mixed letter-and-number homophonic substitution. The 16 letter-symbols map to 16 distinct plaintext letters; the 18 number-symbols cover 16 letters (e = 0 or 2, t = 50 or 8). Some letters have only a number (e, q, z), some only a letter (b, m, o, y), and eleven have one of each.

| plain | cipher | plain | cipher | plain | cipher |
|---|---|---|---|---|---|
| a | p, 4 | g | e, 5 | p | y, 90 |
| b | f | i | d, 16 | q | 88 |
| c | q, 12 | l | c, 80 | r | l, 20 |
| d | a, 7 | m | u | s | x, 40 |
| e | 0, 2 | n | t, 19 | t | b, 50, 8 |
| f | n, 70 | o | s | u/v | 30 |
| | | | | y | g |
| | | | | z | 14 |

All 16 letter-symbols map to 16 distinct plaintext letters; the 18 number-symbols map to 16 distinct letters (e and t doubled). That regularity is the main evidence the solution is real rather than fitted.

## Plaintext (cipher words decoded, cleartext in brackets)

il ny a aucun subiet de scrupule de manquer a dieu [ie vous en responds et mesmes dans] les reigles de perfection prenez s(e)ulement les voyes de prudence p(o)ur conce(r)ver votre vie pour en faire a dieu un plus grand sacrifi(c)e par la multiplication des vos services pour le salut de vos freres [et mesurer a cela sil est meilleur d'agir, ou de soubir] 13 de may 1644

The final cleartext word is "soupir" in Tomokiyo's transcription but "soubir" in Britland's abstract, i.e. *subir*, to endure. "To act or to endure" is the better reading; "sigh" was my error from the transcription. The literal decode of `30 s 50 20 2` is *votre* (modern spelling), not *vostre*.

Modernised: « Il n'y a aucun sujet de scrupule de manquer à Dieu, je vous en réponds, et même dans les règles de perfection. Prenez seulement les voies de prudence pour conserver votre vie, pour en faire à Dieu un plus grand sacrifice par la multiplication de vos services pour le salut de vos frères ; et mesurer à cela s'il est meilleur d'agir ou de subir. »

English: "There is no cause for scruple about failing God, I answer to you for it, even by the rules of perfection. Only take the ways of prudence to preserve your life, so as to make of it a greater sacrifice to God through the multiplication of your services for the salvation of your brethren; and measure by that whether it is better to act or to endure."

Spiritual counsel to someone whose life is in danger and who fears that saving it would be a failing before God. The plaintext names no person, place or title, so the addressee is inferred, not established. Britland's abstract says Forster was in France when he wrote it and that Henrietta Maria (at Exeter, ill, pregnant, deciding whether to flee to France) made a related request a few days later, which makes her a plausible addressee, not a certain one. Whether Forster composed the counsel or relayed a confessor's is open.

## Anomalies (3 symbols in 207)

- w13 `prenez s[a]ulement`: cipher **a** (=d) where **2** (=e) is needed. Handwritten 2 and a are easily confused; likely a transcription or enciphering slip.
- w16 `p[16]ur` for pour: **16** (=i) where **s** (=o) is needed.
- w27 `sacrifi[g]e`: **g** (=y) where **q** (=c) is needed; g/q confusable in hand.
- w17 `conceruer`: q = c gives "concerver", attested in period documents (e.g. a 1623 proceeding in the Archives de la Creuse inventory, noted by Codex's review).
- Unmarked word joins inside cipher "words": descrupule, manquera (manquer a), lesreigles, prenezseulement, lesvoyesde, enfaire, parla, lesalut.

## Method

1. Tomokiyo's transcription parsed into 37 comma-delimited words (the repeated word `y s 30 20` occurs once intact and once split by a line break, proving line breaks are wrapping only).
2. n-gram hill climbing (solver.py, climb.py) failed: 207 tokens over 34 symbols is too thin. Re-run 18 Sept 2026 on `cipherkit` (character 4-gram plus lexicon bonus over `cipherkit.corpora` fr, folded to the letter's i-for-j and u-for-v): the target still comes out degenerate ("rs si e ietes semees ceses euese de risseete"), while `solver.py --control`, a synthetic letter of the same word lengths and symbol count from a held-out tenth of the corpus, reads at 0.91 to 0.96 token-weighted key recovery on two seeds of four and sticks at 0.23 to 0.25 on the other two. The target is harder than its matched control, not merely unlucky.
3. Beam search over a lexicon (dict_solver.py): originally 42k French words from Corneille/Descartes (Gutenberg) plus a modern frequency list, with generated 17th-c. variants (-oit, ie for je, y for i, s for circumflex, u/v). Constraint: same symbol = same letter; different symbols may share a letter. Words longer than 7 symbols allowed to be skipped. Beam 2000. The top state read "il ne a aucu? su?oet des?rupule ie manquera dieu lesrei?les ie perle?toon ... prudence pour ?onceruer uotre uie pour eclaire a doeu un plus traci sa?rofiee parla mu?toplica?ooc des uos serui?es pour ?esalut ie uos freres". Ported 18 Sept 2026 to a lexicon from `cipherkit.corpora` fr (Xivrey, Avenel, Montaigne, Brantôme, Descartes; words seen three or more times, folded to i/u, plus lex_old.txt and the same name list); the same run now reads "il ne a aucuc su?oet descrupule ee manquera dieu lesrei?les ee perlectoon ... prudence pour conceruer uotre uie pour eclaire a doeu un plus grace sacrofiee parla mu?toplica?ooc des uos seruices pour ?esalut ee uos freres". The corpus files of the original run were not kept; the ported scripts are the reproducible ones.

Run: `uv run python dict_solver.py 2000 -25 7` in this directory after `uv run python -m cipherkit.corpora fetch fr`.

## Permutation tests

`permutation.py` scores the 207 decoded letters with a character 4-gram model built from
`cipherkit.corpora` fr (Xivrey, Avenel, Montaigne, Brantôme, Descartes; j folded to i, v to u)
and compares that score with 1,000 shuffles under each of the kit's two nulls (seed 0):

| Null | Question | z | p |
|---|---|---|---|
| key shuffle (`permutation_z_key`): the 34 plaintext values shuffled among the symbols | is this key better than a relabelling of the same symbols? | 11.2 | < 0.001 |
| token shuffle (`permutation_z`): the 207 tokens in random order under the key | is the order of the text informative under this key? | 15.3 | < 0.001 |

The two answer different questions and are not comparable with each other, or with the
Moray key-shuffle z, which uses a dictionary-segmentation score. The z = 8.8 that the 14
September 2026 write-up quoted from the independent review was not reproducible from this
folder: no script here computed it, and the review file does not record its null or model.

## Independent check (Codex, 2026-09-14)

Codex re-applied the key mechanically to all 207 tokens from the live transcription and reproduced the reading with the same three local repairs, and substantially reproduced the beam-search intermediate from the same inputs (see INDEPENDENT-REVIEW.md and verify_solution.py in this folder). Its corrections, adopted above: ending reads *soubir*/subir per Britland; addressee plausible not certain; literal *votre*; key described as mixed, not symmetric. Not yet confirmed: the manuscript image (so whether the three defects are Forster's or the transcriber's). Our search at the time (Cryptiana, Britland 2013, Google, Reddit) found no prior solution; there were earlier ones, see the note at the top.

## Manuscript location (checked 2026-09-14)

- Britland 2013, note 1 (from Wiley's snippet): "Archives départementales (Val-d'Oise), France: MS 68.H.8, troisième liasse (papiers de Richard Forster, trésorier de la Reine d'Angleterre)." Her first page (britland-2013-p1.png) prints the full transcription with the same line breaks Tomokiyo copied, says the document is one page, one side, "a mix of ciphered numbers and letters", and reads the last clear word as "soupir" (the "soubir" is only in her abstract).
- 68 H = fonds of the English Benedictine nuns of Pontoise (68 H 1-23, 1635-1790), whose first abbess Anne Christine Forster was Forster's daughter and whom he funded. Finding aid: archives.valdoise.fr/ark:/18127/1117467 (Lemoine 1944 inventory, encoded 2020). FranceArchives lists 68 H 8 (dated 1667-1763 at bundle level) under "non-digitized". Ruellet, "Down and out in Paris and London?", in *Noblesses en exil* (PUR 2021), used the Forster papers and says the bundle is unnumbered and was labelled "papiers inutils".
- Other Forster material, not this letter: Lambeth Palace Library MS 883 (his accounts as Charles II's treasurer in France); BL Add MS 9354 (English Benedictines, cited by Foster 1977).
- No image online. Routes: reproduction request via the archive's contact form (archives.valdoise.fr/wform/wform/fill/contact_general/n:415; reading room Wed-Fri, 3 avenue de la Palette, Pontoise); or ask Karen Britland (Wisconsin) or Tomokiyo whether they hold a photograph.
