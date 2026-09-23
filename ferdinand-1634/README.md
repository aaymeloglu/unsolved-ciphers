# Ferdinand to the Cardinal-Infante, 28 October 1634

**Partial decipherment.** This Latin letter from Stuttgart discusses French preparations to cross the Rhine, princes under French protection, and a requested armed diversion in the interests of the House of Austria. Connected stretches are readable, but several passages and parts of the sentence structure remain uncertain. No complete English translation is claimed.

The letter is [DECODE R1887](https://de-crypt.org/decrypt-web/RecordsView/1887), Brussels, Algemeen Rijksarchief, Secrétairerie d'État Allemande, inv. 540. The sender was then King of Hungary and Bohemia, later Emperor Ferdinand III; the recipient was his cousin, Cardinal-Infante Ferdinand. The public [Ferdinand correspondence page](https://aaymeloglu.github.io/unsolved-ciphers/ferdinand-reading.html#letter-1634) presents this alongside their 1635 and 1640 letters.

## Evidence and limits

The proposed key uses vowel-preserving syllable families, numerical groups and graphic homophones. For example, `for ub id #` yields `co·mu·ni·s`, and `xar/xer/xir/xur` yield `ta/te/ti/tu`. Repeated phrases and surrounding clear Latin constrain the reconstruction. The final cipher phrase produces `promouerehauddedignetur`, directly matching the following clear words, *promovere haud dedignetur*. Three additional terminal signs remain outside that match.

The 1634 repertoire is separate from the alphabet reconstructed from the 1635 draft and transferred to 1640. No historical key sheet or corresponding plaintext draft was used for 1634. This is a context-assisted reconstruction, not a blind decipherment. No first-solve claim is made.

The elected transcription has **474 groups**, including a partly clipped group provisionally counted as one. All 30 physical lines containing cipher were collated against private manuscript images. Eight baseline labels have revised readings; five revisions remain probable with alternatives retained. Two additions record a visible `#=s` before *hisce* and a clipped p-initial group after `fir`. The latter is **p?**, not a silently restored *pin*.

The literal output has **13 unmapped occurrences and seven assigned empty values**. An assigned letter may still be wrong, and the editorial Latin changes several assigned letters. These counts are inventory and coverage, not verified accuracy. The [apparatus](READING.md) accounts for every group and every editorial character change; [alignment.tsv](alignment.tsv) preserves source alternatives independently of proposed wording.

| Candidate | Literal output | Evidence still needed |
|---|---|---|
| *intermissurum* | `intermisurim` | The probable ib reading supplies mi; tin still has to become tun, and s is doubled editorially. Earlier noun and relative clause remain unresolved. |
| *subvertendis* | `suutuertendis` | A probable tus reading and visible final s help. Reading `10 8` as `108=b` is unverified; the digits are visibly separated and there is no independent occurrence. |
| *facilius mihi* | `?aci?usmihi` | Assign the distinct flat oval f, complete the clipped p? to pin=li, and accept the probable ib/G rereadings. |

These are conjectures. Their required new assignments are listed separately in `observations.json` and are **not** added to `key.json`. The request paragraph and the final comparison remain incomplete, and a polished translation would conceal that uncertainty.

## Grades and verification

Literal-unit grades: **17 C, 457 M; 0 H, 0 S, 0 I**. C is reserved for the closing phrase matched directly to cleartext. M includes contextual assignments, unresolved signs and source ambiguities; it does not mean that every phrase is equally doubtful. Editorial changes in the proposed text are a separate layer: non-orthographic changed or supplied letters in emendation/conjecture spans are **I**, with the exact differences recorded in `apparatus.json`. Normalization of spelling is also recorded explicitly. No editorial repair is passed off as literal key output.

No matched-control S claim is made for this publication. Exploratory work used the `cipherkit` Latin corpus plus Grotius letters and fixed-key shuffle diagnostics; those optimized-key comparisons were not adjusted for the search and manual selection. The public verifier does not depend on a corpus, model pickle, private image or network access, and does not purport to validate individual readings statistically.

```sh
uv run python ferdinand-1634/verify.py
```

This checks occurrence conservation, source-label changes, all literal assignments, the four passages, all 38 apparatus spans, every editorial character edit, the direct closing match, grades, and exclusion of conjectural values from the key. It verifies reproducibility, not paleographic or historical certainty.

## Sources, attribution and files

Manuscript photographs DECODE I9345–I9348 were consulted with permission. **Images and derived crops are not redistributed.** Strip filenames in the alignment identify local evidence, not public image links. `sources.json` records the holding, source hashes and review scope. The transcription and interpretation are LLM-assisted work, reviewed 23 September 2026. A second-model review independently reproduced all 474 literal assignments and all 38 spans, checked the source additions and revised forms, and retained the three gap readings as conjectures.

The [AP transcription of R953](../ferdinand-1635-1640/sources/R953-DECODE-rejected-comparison.txt) was checked as a candidate key. Its numerical and syllabic values conflict with established assignments here. R945's public metadata was inspected, but no matching key was established and its images were not checked. Targeted searches did not locate another witness or settle publication priority. This is not an exhaustive image-level survey of the SEA keys or printed correspondence.

`transcription-pass2.txt` preserves the baseline; `transcription.txt` is the elected transcription with stable line labels. `observations.json` records each amendment, alternative and unadopted hypothesis. `alignment.tsv`, `key.json` and `literal.txt` define the literal reading. `apparatus.json` and `READING.md` distinguish normalization, emendation, conjecture and unresolved material. `token-grades.tsv` and `grades.json` give the evidence grades.

A matching key or another letter with the same repertoire would be the strongest next evidence for the rare signs and disputed numerical grouping.
