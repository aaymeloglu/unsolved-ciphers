**Richard Forster’s 1644 cipher letter: independent review**

The proposed decipherment is highly convincing. A single fixed substitution reads essentially the entire encrypted passage as coherent French spiritual counsel. Exactly three positions disagree with a minimally emended reading, and the same key works across long, interconnected phrases. This is strong evidence of a successful decipherment of the published transcription, although it is not yet a manuscript-verified critical edition.

The public record also supports treating the letter as previously unsolved: Cryptiana’s live catalogue, last modified on September 6, 2026, still calls it undeciphered. No earlier published solution was found in the sources searched through September 14, 2026. “No known published solution” is the defensible claim. “Nobody has ever solved it” would exceed what a literature search can establish.[^1]

Several claims in the original write-up need qualification. Henrietta Maria is a plausible recipient, but the deciphered words do not identify her. The ending translated as “sigh” is disputed between two published representations of the cleartext. The key’s regularity is accurately counted but incompletely described, and some modernization has been presented as literal decipherment.

| Claim | Assessment |
|---|---|
| The letter was publicly treated as unsolved | Supported by the original scholarly discussion and current specialist catalogue |
| This key recovers the encrypted message | Very high confidence, conditional on the published transcription |
| Three defective encrypted positions | Confirmed for a reading retaining historical/nonstandard spelling |
| The defects are transcription mistakes | Possible; unverified without the manuscript |
| The subject is spiritual counsel about preserving life for continued service to God | Strongly supported by the recovered text |
| The recipient is almost certainly Henrietta Maria | Too strong; plausible and contextually attractive |
| The closing word means “sigh” | Unresolved; another published reading is “soubir” |
| The system consists of two complete substitution alphabets | Not established; the observed key is a mixed letter-and-number homophonic substitution |

The earliest identified scholarly discussion is Karen Britland’s “Reading between the lines: royalist letters and encryption in the English civil wars,” *Critical Quarterly* 55(4), pp. 15–26. The issue is dated December 2013; Wiley records first online publication on January 21, 2014. Its first note locates the document at Archives départementales du Val-d’Oise, MS 68.H.8, troisième liasse, among Richard Forster’s papers.[^2]

The article’s abstract, reproduced on ResearchGate, explicitly describes an unknown correspondent and a missing key, and reports that attempts using computers had not recovered the meaning. It places Forster in France and proposes a connection to the queen’s request for asylum. This is an explicit contemporary-to-publication statement of failure, rather than an inference from an absence of a translation.[^3]

Satoshi Tomokiyo published the ciphertext on September 21, 2021, under an unsolved-letter title. The live post still has no comments, and its encrypted tokens match the local `ct.txt` token for token. His current catalogue also retains the unsolved description; nearby entries explicitly mark other ciphers as solved. The catalogue’s recent modification date shows maintenance, although it does not establish a fresh investigation of every individual entry.[^1][^4]

Searches included the author’s name, date, article title and DOI, English and French decipherment terms, references citing Britland, and specialist historical-cryptology material. One apparently relevant later decipherment concerns different royalist letters: Macadam and Roy’s work on two June 1644 dispatches to Prince Rupert. It does not solve this May letter.[^5] A full-text search of the 2023 HistoCrypt proceedings found no occurrence of Forster; its Britland references concern invisible ink.[^6]

There are access limits to this conclusion. Britland’s full article and the manuscript image were not obtained. The accessible abstract and publisher notes were inspected, rather than the entire article. Her 2025 book, *Women Writing in a Time of War, 1642–1689*, was identified, but its relevant chapter and index could not be fully inspected. The publicly accessible metadata supplies no solution, which is not proof that the inaccessible text contains none.[^7] Unindexed publications, private communications, and archival decipherments remain possible. Neither Britland nor Tomokiyo has been contacted as part of this review.

The independent mechanical audit used `ct.txt` and `mapping.json`, without a dictionary, language model, or search algorithm. It excluded the two bracketed cleartext stretches and the date, retained commas as group boundaries, and treated line breaks as wrapping. It counted **207 encrypted tokens, 34 distinct symbols, and 37 cipher groups**. The ciphertext was separately extracted from a fresh download of Tomokiyo’s post; all 207 encrypted tokens matched the local file.[^4]

The key has 20 distinct plaintext values when u/v and i/j are represented by u and i. All 16 alphabetic cipher symbols have different plaintext values. The 18 numeric symbols have 16 plaintext values, with e and t each represented twice. Those counts agree with the earlier write-up.

The stronger generalization that every plaintext letter has a letter-symbol is false for the observed key. Plaintext e is represented only by numeric `0` and `2`; q, u/v, and z also have only numeric representatives. Conversely b, m, o, and y have only alphabetic representatives. Twelve plaintext values have representatives in both classes. There may have been a larger original key, but this short message cannot recover its unused entries.

| Plaintext | Alphabetic cipher symbols | Numeric cipher symbols |
|---|---|---|
| a | p | 4 |
| b | f | - |
| c | q | 12 |
| d | a | 7 |
| e | - | 0, 2 |
| f | n | 70 |
| g | e | 5 |
| i/j | d | 16 |
| l | c | 80 |
| m | u | - |
| n | t | 19 |
| o | s | - |
| p | y | 90 |
| q | - | 88 |
| r | l | 20 |
| s | x | 40 |
| t | b | 8, 50 |
| u/v | - | 30 |
| y | g | - |
| z | - | 14 |

The right description is a **homophonic substitution using alphabetic and numeric symbols**. It needs no changing alphabets, positional rules, rearrangement, or deletion of arbitrary symbols. The observation that the alphabetic symbols have distinct values is useful supporting evidence, but not the strongest evidence: that is the sustained French syntax and meaning produced by the same key throughout the message. No statistical probability of accidental success has been calculated.

The three proposed letter repairs are explicit and localized:

| Cipher group | Encrypted token position | Raw decoded form | Proposed reading | Conflict |
|---|---:|---|---|---|
| 13 | 70 | prenezsdulement | prenez seulement | a maps to d, but this position requires e |
| 16 | 97 | piur | pour | 16 maps to i, but this position requires o |
| 27 | 151 | sacrifiye | sacrifice | g maps to y, but this position requires c |

The corresponding replacements could be an e-symbol (`0` or `2`), the o-symbol (`s`), and a c-symbol (`q` or `12`). Which glyph, if any, was actually misread cannot be settled from this table. Explanations involving similar handwriting are hypotheses, not observations of this manuscript.

These are real local inconsistencies under the proposed reading, rather than opportunities to change the whole key. Elsewhere, `a` is required for d in *dieu*, *prudence*, and *des*; `16` is required for i in *subiet*, *perfection*, *dieu*, *sacrifice*, and *multiplication*; and `g` is required for y in *ny* and *voyes*. Changing any of those symbols globally damages other readings.

With those three repairs, **204 of 207 positions match before correction**, or 98.55%. This percentage measures agreement with the proposed text, not a probability that the decipherment is correct. It retains `conceruer` and `des uos`, rather than silently converting the whole passage to modern French.

The apparent anomaly `conceruer`, rendered `concerver` when u/v is modernized, has external support. An official Creuse archival inventory reproduces a phrase from a proceeding dated May 24, 1623 using “concerver leurs bleds.” This is an independent historical transcription attesting the spelling, though not an image of that original handwriting. Retaining it in a diplomatic reading is therefore reasonable; modernization to *conserver* should be labeled.[^8]

Several additional editorial distinctions matter. Group 18 is `30 s 50 20 2`, which decodes to **uotre**, hence **votre**; it has no encrypted s for *vostre*. Group 30 is **des**, so *des vos services* is the literal phrase, while *de vos services* is a grammatical modernization. In `conce(r)ver`, the parenthetical r does not mark the problematic character: r is already explicitly encoded by `l`; modern *conserver* would change the fourth plaintext character, c, to s. The supplied chat passage also leaves the necessary c-repair in *sacrifice* unmarked, although the local solution document marks it.

The strongest check against fitting isolated words is that many phrases are determined by symbol values supported elsewhere. As an additional consistency exercise, each cipher group was withheld in turn, and symbol values were inferred by majority vote from the proposed readings of the other 36 groups. This recovered 195 of 207 target letters, left nine positions unresolved through missing evidence or ties, and reproduced exactly the three defective positions. Entire groups such as *descrupule*, *perfection*, *prudence*, *enfaire*, *seruices*, and *freres* were predicted from the other groups. This is not a blind holdout experiment: the candidate reading had already been developed using the whole text. It does show extensive cross-group constraint rather than independent guessing of every word.

The discovery process was also checked. The saved `dict_solver.py` was rerun with parameters `2000 -25 7` against the original corpus files recovered from the earlier working directory. The program does not read `mapping.json`. Its consistency function enforces one plaintext value per ciphertext symbol while permitting different symbols to share a value. It does not enforce the observed one-to-one structure within the alphabetic symbols.

The best state scored −166.6 and substantially reproduced the reported intermediate output. It was recognizably close to the final message but less clean than the condensed chat description suggests. For example, it produced `perle?toon`, `sa?rofiee`, and `mu?toplica?ooc` where manual completion yields *perfection*, *sacrifice*, and *multiplication*. Thirteen key entries differed from, or were absent relative to, the final key. This supports the claim of a dictionary search followed by substantial manual completion. The fact that the particular hill climbers failed does not prove that 207 tokens are inherently insufficient for n-gram methods.

A minimally emended reading follows. Brackets identify the already-cleartext runs; angle brackets identify the three replacement plaintext letters. Spaces within cipher groups have been supplied for readability. The cipher’s u/v convention is retained, and the final cleartext reading is left as in Tomokiyo’s transcription:

> il ny a aucun subiet de scrupule de manquer a dieu [ie vous en responds et mesmes dans] les reigles de perfection prenez s⟨e⟩ulement les uoyes de prudence p⟨o⟩ur conceruer uotre uie pour en faire a dieu un plus grand sacrifi⟨c⟩e par la multiplication des uos seruices pour le salut de uos freres [et mesurer a cela sil est meilleur d’agir, ou de soupir] 13 de may 1644

The unresolved ending requires particular care. Tomokiyo prints **soupir**, while the article abstract on ResearchGate prints **soubir**. The latter suggests *subir*, “undergo,” “endure,” or “suffer”; it would make an intelligible opposition to *agir*, “act.” *Soupir* normally supplies the noun “sigh,” whereas the expected modern infinitive is *soupirer*. Expanding it to *soupir(er)* is therefore an editorial proposal, not a cipher result. Both the source disagreement and the grammatical issue must remain visible.[^3][^4][^9]

The manuscript might resolve this immediately, but neither a disputed letter nor a missing ending should be asserted from the transcription alone. A cautious translation is:

> There is no reason for scruple about failing God; I assure you of this, even according to the rules of perfection. Only take prudent measures to preserve your life, so that you may make of it a greater sacrifice to God through multiplying your services for the salvation of your brethren; and judge by that whether it is better to act or to [endure/sigh: the final word remains uncertain].

The text’s central advice is clear despite that final uncertainty: preserving life can support a greater offering to God through future service. The earlier English version broadly captures this, but “fears she would be failing God” is an interpretation of the situation, and “she” is supplied by the recipient hypothesis. Nothing in *vous*, *votre vie*, or *vos frères* establishes the recipient’s sex, office, or identity.

The queen hypothesis fits the chronology. A National Maritime Museum Cornwall account places Henrietta Maria in Exeter by May 1, 1644, seriously ill and pregnant. She gave birth on June 16 and sailed from Falmouth for France on July 14. Her departure from Exeter itself was earlier, around the end of June. These details make counsel about preserving life historically plausible, but they do not identify the letter’s recipient.[^10]

The plaintext mentions no queen, pregnancy, Exeter, France, voyage, military commander, or specific danger. Spiritual counsel of this sort could be given to other endangered Catholics. Nor does handwriting establish composition: a document in Forster’s hand could contain advice he composed, copied, or transmitted. The decipherment strengthens the broad contextual plausibility of Britland’s earlier conjecture without converting it into a demonstrated attribution.

The next evidentiary step is narrowly defined: obtain the May 13 letter in Val-d’Oise MS 68.H.8, troisième liasse, and compare the manuscript with the three defective encrypted positions, `conceruer`, `uotre`, `des uos`, and the closing cleartext. Any address, endorsement, adjacent letter, or surviving key should be checked for the recipient and transmission history. Confirmation from Britland and Tomokiyo would also strengthen the claim of an unpublished solution. Until then, the suitable description is: **a highly convincing decipherment of a letter still publicly catalogued as unsolved, with three proposed local corrections and unresolved manuscript and attribution details**.

The accompanying `verify_solution.py` and `verification.json` supply all 37 raw group decodings, every symbol frequency, the exact repairs, and the leave-one-group-out results. `review-sources/` preserves the retrieved catalogue and blog pages, the beam-search rerun output and log, and hashes identifying its inputs. The original `SOLUTION.md`, ciphertext, and key have been preserved.

**Sources**

[^1]: Satoshi Tomokiyo, [“Unsolved Historical Ciphers”](https://cryptiana.web.fc2.com/code/unsolved.htm), entry “Letter of Richard Forster, possibly to Henrietta-Maria (1644).” First posted January 11, 2015; page last modified September 6, 2026; live HTML retrieved September 14, 2026. Local snapshot: `review-sources/cryptiana-unsolved-2026-09-14.html`.
[^2]: Karen Britland, [“Reading between the lines: royalist letters and encryption in the English civil wars”](https://onlinelibrary.wiley.com/doi/abs/10.1111/criq.12072), *Critical Quarterly* 55(4), December 2013, 15–26; first online January 21, 2014. DOI: 10.1111/criq.12072. Publisher metadata and notes accessible; full article not obtained. Archival reference is note 1.
[^3]: Britland, [article abstract reproduced on ResearchGate](https://www.researchgate.net/publication/260410273_Reading_between_the_lines_Royalist_letters_and_encryption_in_the_English_civil_wars), accessed September 14, 2026. Used for the article’s explicit unsolved status, unknown recipient, contextual hypothesis, and spelling `soubir`. This is an abstract-level representation, not an independent transcription of the manuscript.
[^4]: Satoshi Tomokiyo, [“An Unsolved Letter of Richard Forster in the household of Henrietta-Maria (1644)”](https://cryptiana.blogspot.com/2021/09/an-unsolved-letter-of-richard-forster.html), September 21, 2021; retrieved September 14, 2026. Local snapshot: `review-sources/cryptiana-forster-2026-09-14.html`. All encrypted tokens checked against the supplied local transcription; closing cleartext is `soupir`.
[^5]: Joyce Macadam and Ian Roy, [“‘Wilmot’s blots’ and Cavalier plots, June 1644: fresh evidence from captured correspondence”](https://www.tandfonline.com/doi/abs/10.1080/0268117X.2020.1792337), *The Seventeenth Century* 36(4), 2021, published online in 2020. Abstract and notes distinguish the two Rupert letters from this document.
[^6]: [*Proceedings of HistoCrypt 2023*](https://ecp.ep.liu.se/index.php/histocrypt/issue/download/77/80), Linköping University Electronic Press, 2023. Downloaded and text-searched; Britland references concern invisible ink, and “Forster” was absent from the extracted text. This is a bounded check, not an exhaustive survey of all historical-cryptology proceedings.
[^7]: Karen Britland, [*Women Writing in a Time of War, 1642–1689*](https://academic.oup.com/book/60426), Oxford University Press, 2025. Publication information and contents accessible; chapter “Sympathetic Letters: Reading Between the Lines” and index not fully inspected. Listed to disclose a remaining literature-access limitation.
[^8]: Archives départementales de la Creuse, [*Abbaye de Bonlieu, H 284–521: Répertoire numérique*](https://archives.creuse.fr/fichier/287520/25424), revised 2012, PDF pp. 130–131 (zero-based pages 129–130), discussion of the May 24, 1623 proceeding. Its archival transcription includes `concerver leurs bleds`. Text inspected; original 1623 handwriting not inspected.
[^9]: ATILF/CNRTL, [“Subir”](https://www.cnrtl.fr/definition/subir), *Trésor de la langue française informatisé*. Supports the meaning of *subir* and its historical existence; does not itself authenticate the spelling `soubir` in this letter.
[^10]: Linda Batchelor, [“Royal Escape from Falmouth”](https://www.maritimeviews.co.uk/focus-on-falmouth/royal-escape-from-falmouth/), National Maritime Museum Cornwall, undated; accessed September 14, 2026. Historical narrative citing the queen’s letters and contemporary correspondence. Used for Exeter arrival, illness, childbirth, late-June departure toward Falmouth, and July 14 sailing.
