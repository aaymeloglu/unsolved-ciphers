# Unsolved ciphers worth attempting: consolidated shortlist (round 2)

Date: 2026-09-13. Built from five parallel research passes (Schmeh Top 50 status audit, author-created book ciphers, archival diplomatic ciphers via Cryptiana/DECODE, famous modern ciphers, and recent solves + AI-solve landscape). Complements the earlier `README.md`/`dossier.html` in this folder, which recommended Gun Wa and Hutton Part 5. This round disagrees with that ordering; see "Why not Gun Wa or Hutton first" below.

## 1. Premise check: the Fable solve is real

Reticuli's refutation (GitHub, 2026-09-01) tested the wrong book. It used EEBO-TCP A64608, transcribed from the British Library copy of the 1653 *Logopandecteision*. That copy has different Proquiritation text and ordering and ends with no distich leaf. Vals cited the Maitland Club 1834 *Works* (reprinted from the National Library of Scotland copy), which prints "THE CYPHRAL DISTICH" on p. 417 directly after Proquiritation 32.

Reproduced twice today (agent, then me) against the 1834 OCR with the plain rule "i-th number = 1-based word index into Proquiritation i, take first letter":

| Line | Output | Hits |
|---|---|---|
| 1 | OGODUPHOLDKINGCHARLSTHESECONDAND | 32/32 |
| 2 | MAKEHIMTHESUPR**W**M**C**RULEROFTHISLAND | 30/32 |

The two line-2 misses are tokenization artifacts (OCR joins "Parole-breaking" into one token; Latin "hinc inde" counted as one unit per Vals's footnote). No position is infeasible in the 1834 text. 

Nobody in the cipher community (Schmeh, Pelling, Tomokiyo) has published on this either way. One Schneier commenter ("kjfriedo", Sept 10) reached the same conclusion. Open bibliographic question: which 1653 issue carries the expanded Proquiritations plus distich leaf (NLS H.32.a.39 reportedly does). Publishing this reproduction is itself a small, useful contribution.

## 2. What "comparable difficulty" means

The Distich profile: short ciphertext, author-created, key internal to the surrounding material, that material digitized, solution self-evidently right once found, and nobody had actually sat down with it. Vals's own caution: avoid targets that have absorbed thousands of expert-hours (Kryptos K4, Voynich, Zodiac, d'Agapeyeff).

Pattern across every real solve 2015-2026 (Zodiac 340, Mary Queen of Scots, Dickens, Silk Dress, Perwich, Milroy): the break was identifying the system or finding the key/plaintext in an archive, with hill-climbing software to finish. Pure cryptanalysis of the ciphertext alone almost never did it.

## 3. Tier 1: start here

Ranked by (cheap to attempt) x (self-verifying) x (someone would care).

### 1. Gelett Burgess, *The Master of Mysteries* (1912), third hidden message
- **What:** The anonymous preface says three messages are hidden in the book. Message 1 = first letters of chapter bodies ("THE AUTHOR IS GELETT BURGESS"). Message 2 = last letters of chapters ("FALSE TO LIFE AND FALSE TO ART", found by a blog commenter in Aug 2021). Message 3 has never been found.
- **Why it fits:** Exactly the Urquhart shape. Author-built, structural, the key is the book's own layout, the text is on Internet Archive, and the two found messages tell you the author's style.
- **Attack:** Work from a first-edition scan (Bobbs-Merrill 1912), not a reflowed text. Enumerate chapter-level and page-level extractions the found messages don't use: first/last words, second sentences, story-final paragraphs, page-initial letters, Astro's mottos, capitalized words.
- **Sources:** [Schmeh post](https://scienceblogs.de/klausis-krypto-kolumne/the-unsolved-mystery-from-the-master-of-mysteries/), [Internet Archive text](https://archive.org/details/cu31924022342871)

### 2. Richard Forster letter, 13 May 1644 (French) - SOLVED 2026-09-14 (this project; see forster-1644/SOLUTION.md)
- **What:** ~230 tokens over ~35 symbols (letters a-y plus numbers 0-90), commas mark word breaks, French cleartext fragments inside and around it. Forster was treasurer of Henrietta Maria's household; the queen was at Exeter, pregnant, weeks from fleeing to France.
- **Why it fits:** Word boundaries are visible, cleartext frames it, nobody has tried. Solution is readable French, so it verifies itself. Tomokiyo maintains the unsolved list and would record a solve.
- **Attack:** Word-boundary-aware substitution/homophonic solve with a French language model. The repeated 2-token "7. 0." and 4-token "y. s. 30. 20." groups are immediate cribs.
- **Source:** [Cryptiana transcription](https://cryptiana.blogspot.com/2021/09/an-unsolved-letter-of-richard-forster.html)

### 3. Richelieu to M. de Rancé, 1629 (French)
- **What:** ~280 two-digit groups (10-92) interleaved with about 25% cleartext. BnF fr.3829 ff.87, 89 (DECODE R9461/R9462). Tomokiyo: "may not be very difficult for people who can read the cleartext."
- **Attack:** The cleartext fixes syntax around each cipher run ("Mr de 43", "jay parle a 24 19 16 10..."). Homophonic hill-climb with French scoring and a small nomenclator for names.
- **Source:** [Cryptiana transcription](https://cryptiana.web.fc2.com/code/richelieu1629.txt)

### 4. ~~Confederate Navy dictionary code, 19 March 1863~~ SOLVED (Aug 2026, not by us)
- **Correction 2026-09-13:** solved by Reddit user offgramercy on r/codes about mid-August 2026, the first Google result for the cipher's name. Key: Webster's *Primary School Pronouncing Dictionary* (1850), HathiTrust hvd.32044086661170; third number = headword ordinal in the column. I verified all 17 mechanical groups against the scan; verified against the HathiTrust scan. Tomokiyo's list was stale. Lesson: search the cipher's name directly before calling anything untouched.

### 5. Roosevelt cryptogram, April 1935 (Schmeh Top 50 #17)
- **What:** ~120 digits and apostrophes in a letter to FDR. The 20-letter part was solved and is a trivial trick ("DID YOU EVER" on even positions, "BITE A LEMON" reversed on odd). Friedman noted the digit pairs contain each of 10-52 exactly once, which screams positional index or transposition key over text in the letter itself.
- **Attack:** Brute-force the parsing ambiguity (apostrophes as separators, 000000 blocks as spacers), treat the 43-value permutation as a read order over the letter's own text or the solved sentence, score for English. No computational attempt has been reported.
- **Sources:** [Schmeh post](https://scienceblogs.de/klausis-krypto-kolumne/2017/12/08/the-top-50-unsolved-encrypted-messages-17-the-roosevelt-cryptogram/), [NSA Friedman Lectures scan](https://www.nsa.gov/portals/75/documents/news-features/declassified-documents/friedman-documents/publications/ACC15281/41785109082412.pdf)

### 6. Regent Moray to John Wood, 13 July 1568 (English/Scots)
- **What:** ~215 units, letters with numbered variants plus numbers 4-19. BL Add MS 32091 f.213. Written eight weeks after Mary Queen of Scots fled to England, in the run-up to the York conference and the Casket Letters. Tomokiyo: "appears simple but unsolved."
- **Why it fits:** Best history-to-effort ratio on the list. A solve lands in Mary Queen of Scots scholarship.
- **Attack:** Homophonic hill-climb; the numbers 4-19 are almost certainly a name list (Queen, Elizabeth, Cecil, Norfolk, Mary).
- **Source:** [Cryptiana transcription](https://cryptiana.web.fc2.com/code/elizabeth_moray.txt)

### 7. TNA SP53/16 nos. 78 and 79, c.1585 (French)
- **What:** Two letters, same hand and cipher, ~500 and ~620 groups (01-141 with letter suffixes). Anonymous letters to an English priest in Paris and the president of the English College at Rheims, intercepted and endorsed by Thomas Phelippes, never deciphered.
- **Why it fits:** Walsingham's own codebreaker filed it unread. ~1100 pooled groups is plenty for a homophonic solver.
- **Attack:** Pool both texts, homophonic solver with French model, Catholic-exile vocabulary cribs (Rheims, seminaire, la Royne d'Ecosse).
- **Sources:** [no. 78](https://cryptiana.web.fc2.com/code/SP53_16_78.txt), [no. 79](https://cryptiana.web.fc2.com/code/SP53_16_79.txt)

### 8. Fair Game code, 2010 (Schmeh Top 50 #36)
- **What:** 71 letters (one illegible) embedded in the end credits of the film *Fair Game*. Schmeh published full credit screenshots, so the entire surrounding "book" is a few images. A 2014 anonymous commenter claimed the yellow letters mark the letters that follow them.
- **Attack:** Work from screenshots, not the disputed forum transcription. Enumerate marker schemes (next letter, previous letter, first letter of next name, offsets) and check for an English sentence.
- **Risk:** Could be a studio stunt with no answer.
- **Sources:** [screenshots](https://scienceblogs.de/klausis-krypto-kolumne/2017/06/22/the-fair-game-code-here-are-the-complete-screenshots/), [2019 revisit](https://scienceblogs.de/klausis-krypto-kolumne/2019/09/22/revisited-the-fair-game-code/)

## 4. Tier 2: real, open, more friction

- **Hooke's tenth anagram (1676).** Verified in EEBO-TCP A44317: two letter-multisets under "A new invention in Mechanicks of prodigious use." Never expanded by Hooke as far as any agent could find. Cheap constrained Latin anagram over his 1676-78 vocabulary. Weakness: anagrams admit many readings, so a solve is arguable rather than self-evident.
- **Julius Petersen's byline "46, 9, 4-57, 3, 5" (1875).** Page/line/word code into his own cryptography articles in *Nær og Fjern*. Perfect shape; blocked on scans from the Danish Royal Library. $100 prize (Bjarne Toft).
- **Göpel, *Maurerische Chiffren* (1862).** Two partly enciphered specimens in a catalogue that prints its own 19 Masonic alphabets. Match specimens to the book's tables.
- **Grimmelshausen "Urban von Wurmsknick auff Sturmdorff".** 32-letter pseudonym; all his others are anagrams of his name, this one isn't. Anagram search against names in the same volume.
- **Copenhagen cryptogram.** 107 symbols, 25 distinct, mono-sub-looking, language unknown (Danish likely). Agents disagreed on prior effort (one says never formally attacked, one says medium-heavy). Cheap to try with a Danish model.
- **Charles II to Duke of Hamilton, 1650.** ~150 code numbers across four printed letters, weeks before Dunbar. Key may sit in John Wallis's papers (Bodleian). Archival hunt more than cryptanalysis.
- **Catokwacopa (1875).** Two linked agony-column ads. Substantial partial reconstruction already exists (Gaffney, Ernst and others, discussion through Sept 2026), so this is finishing work, not a first break.
- **Furlong 1873 postcard, 1909 cigarette case.** Short personal mono-subs with cribs; cheap; ambiguity risk from length.
- **Moustier altar inscriptions.** Two ~50-glyph liturgical texts; 2022 Trithemius-style hypothesis untested with a Latin corpus; a rule must fit both inscriptions unchanged.
- **Debosnys (1883).** Schmeh's #3; Debosnys plagiarized his plaintext poems, so the encrypted poem may be a crib attack against Thomas Moore. Blocker: no clean transcription.
- **Cyphral Octastich confirmation.** Vals claims 231/275 against EEBO-TCP for *The Jewel*; nine letters open. Needs the Glasgow 1652 copy or the 1983 Jack & Lyall edition. Finishing this is adjacent to the reproduction above.
- **Gun Wa (1889) and Hutton Part 5 (2023).** The earlier dossier's picks. See below.

## 5. Why not Gun Wa or Hutton first

Gun Wa is 77 letters with a period-5 signal that only clears chance at about the 1-7% level depending on the test. At that length a Vigenère "solution" is easy to manufacture and hard to prove, and one reader already suggested the ad may be attention-getting nonsense. Hutton Part 5 is an artificial MysteryTwister challenge with random keys; solving it proves a technique, not a mystery, and nobody outside that site would notice. Both are fine as fallbacks. The Tier 1 items above are as cheap to start, produce readable plaintext that verifies itself, and a solve would be recorded by Tomokiyo or Schmeh.

## 6. Excluded (with the reason)

| Target | Reason |
|---|---|
| Kryptos K4 | Plaintext recovered from Sanborn's archive Sept 2025; Paradigm runs a $1/guess hash verifier since June 2026; method space carpet-bombed for 35 years |
| Voynich, Rohonc, Cicada Liber Primus, Codex Seraphinianus | Too large, too many foundational unknowns, or asemic |
| Zodiac Z13, Z32 | Unfalsifiable at that length; Z340 solved 2020 |
| d'Agapeyeff 1939 | 280+ documented computational runs, likely construction error |
| Dorabella 1897 | Wase 2023 rules out mono-sub in English/Latin; heavily mined |
| Beale 1 and 3 | Hoax per 2024 IACR and 2025 Bayesian analyses |
| Pigeon cryptogram | One-time pad per GCHQ |
| Feynman #2/#3, Bellaso challenges, Thouless, Rilke, Silk Dress, Ferdinand III, Perwich, Milroy | Already solved (2017-2026); several "unsolved" lists are stale |
| Somerton Man code | Not a cipher; man identified 2022; initials of horses per Abbott |
| Scorpion, Blitz, Chinese gold bars, Hampton, Penitentia, McCormick | Hoax risk, no context, or no real system |
| Vigenère "challenge" (f.199) | Vigenère prints the plaintext himself; a reconstruction exercise |
| The Secret (Preiss), Decipher III | Riddles and contest puzzles, not ciphers; verification needs a shovel or lost images |

## 7. Recommended first campaign

Run two in parallel because they exercise different muscles:

1. **Burgess third message** (structural, LLM-shaped): get the 1912 first-edition scan, build a page/chapter model, enumerate extractions, score for English. One evening.
2. **Forster 1644** (statistical, tool-shaped): write a word-boundary-aware homophonic hill-climber with French n-gram scoring, seed with the crib groups, run. If it falls, Richelieu 1629 uses the same tooling next.

Before either, spend twenty minutes writing up the Distich reproduction (script plus the two-issue explanation) as a public gist or a comment on Schmeh's post. It settles a live dispute, costs nothing, and is the first thing a skeptic will ask about if we later claim a solve.

Stopping rule for any target: a compact rule that reproduces the whole ciphertext, applied unchanged, yielding coherent plaintext. A free choice per symbol, or a different exception for each awkward position, is not a solve.

## Sources consulted by the agents (main hubs)

- [Cryptiana unsolved historical ciphers](https://cryptiana.web.fc2.com/code/unsolved.htm) (Tomokiyo; updated 2026-09-06)
- [Schmeh Top 50 index](https://scienceblogs.de/klausis-krypto-kolumne/the-top-50-unsolved-encrypted-messages/) and [klausschmeh.net](https://klausschmeh.net/)
- [Cipher Mysteries](https://ciphermysteries.com/) (Pelling)
- [DECODE database](https://de-crypt.org/)
- [Vals post](https://www.vals.ai/blogs/fable-solves-cyphral-distich), [Reticuli refutation](https://github.com/reticuli-labs/panel-artifacts/blob/main/distich-refutation-2026-09-01/FINDINGS.md), [Schneier thread](https://www.schneier.com/blog/archives/2026/09/claude-fable-solves-a-historical-cipher.html), [HN thread](https://news.ycombinator.com/item?id=49688695)
- [Maitland Club 1834 Works](https://archive.org/details/worksofsirthomas00mait/page/416), [Notes and Queries 1899](https://archive.org/details/s9notesqueries03londuoft/page/128)
- [Matthew Green cipher_benchmark](https://github.com/matthewdgreen/cipher_benchmark) (262-record unsolved collection)

## 8. Status check, 2026-09-13 (after the Barney miss)

Method: each candidate's name searched in Google and Reddit through Andy's browser; r/codes new-post titles read back to 2026-05-27 (300 posts); Cryptiana blog 2025-26 post list, Cipher Mysteries 2026 posts, klausschmeh.net "Unsolved cryptogram" category and "Unsolved Crypto Mysteries" page, and the HistoCrypt 2026 programme read for any of the names.

| Candidate | Result | Verdict |
|---|---|---|
| Burgess third message | Only Schmeh 2021, Ramble House, Black Chamber 2021; nothing newer | open |
| Forster 1644 | Cryptiana "undeciphered"; also treated as unread in Critical Quarterly 55/4 (2013), "Reading between the lines: royalist letters and encryption" (note: Forster was in France, recipient unknown) | open |
| Richelieu 1629 | Cryptiana "undeciphered"; nothing else | open |
| Roosevelt 1935 | Only Schmeh 2017 and the Codebreaking Guide; no computational attempt reported | open |
| Regent Moray 1568 | Only Cryptiana; no cipher discussion anywhere | open |
| SP53/16 nos. 78-79 | Only Cryptiana | open |
| Fair Game code | Schmeh reposted it May 24 and June 8 2026 as unsolved | open |
| Hooke tenth anagram | No search results at all | open, but anagram solutions are arguable |
| Petersen byline | Schmeh 2018 revisit; nothing since | open, needs Danish scans |
| Copenhagen cryptogram | Nothing since Schmeh 2021 | open |
| Moustier | Cipher Foundation page dated 2026 still lists it; on Schmeh's current unsolved page | open |
| Debosnys, Cylob, cigarette case, Furlong, Göpel, Grimmelshausen, Callimahos, Gaines, Charles II-Hamilton | No solve claims found; cigarette case, Furlong, Moustier, Fair Game, Catokwacopa, Pollaky are on Schmeh's current unsolved page | open |
| Catokwacopa | Schmeh Aug 14 2026 post; his Facebook comment: "the cipher mechanism has been solved, but the complete, unique plaintext cannot be mathematically reconstructed" | effectively cracked, remove |
| Decipher III | A "Decipher II and III Puzzles solutions" document circulates on Scribd | drop |
| Confederate Navy 1863 | Solved on r/codes Aug 16 2026 (verified here) | solved |

Not found in r/codes since late May 2026: any other historical-cipher solve. New open items seen on Tomokiyo's blog in 2026: Mirabeau 1787 (41 groups, hopeless alone), Wellington's Peninsular War code (Sept 8 2026 post, worth a look).
