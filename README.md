# Unsolved ciphers

Working repo for attempts on historical ciphers that are short, context-rich, and listed as unsolved. Started September 2026 after Vals AI reported Claude Fable 5.1 reading Thomas Urquhart's Cyphral Distich; the question was whether the same approach (an agent plus a person checking its work) gets anywhere on the rest of the list. Tooling is mostly Claude Code, with Codex used for independent re-verification. Everything here is reproducible from the scripts and the cited sources.

## Contents

| Folder | Item | Status |
|---|---|---|
| `forster-1644/` | Sir Richard Forster's ciphered letter, 13 May 1644 (Karen Britland, *Critical Quarterly* 2013; Tomokiyo's unsolved list) | **Solved 14 Sept 2026.** Mixed letter-and-number homophonic substitution; plaintext is spiritual counsel to preserve one's life. Three symbols in 207 need repair. Independently re-verified. Not yet checked against the manuscript (AD Val-d'Oise 68 H 8). |
| `urquhart-1653/` | The Cyphral Distich (Vals AI / Fable 5.1 solve, disputed by a GitHub refutation) | Reproduction: the Vals decoding is correct against the Maitland Club 1834 text; the refutation tested the British Library copy, a different state of the book. |
| `barney-1863/` | Confederate Navy dictionary code, Barney to Mallory, 19 March 1863 | Solved on r/codes in August 2026 by another party; all 17 mechanical groups re-verified here against the 1850 Webster's Primary School Dictionary on HathiTrust. |
| `burgess-1912/` | Gelett Burgess, *The Master of Mysteries*, the third hidden message | Open. Simple acrostic families exhausted; notes list what was tested. |
| `SHORTLIST.md` | Candidates, with per-item status checks | |

## Method notes

Two things carried the Forster solve, and neither was cryptanalytic cleverness: known word boundaries, and a lexicon with 17th-century spellings (estoit, mesme, roy, luy, ie). Character n-gram hill climbing on 207 tokens over 34 symbols went nowhere. A beam search over dictionary words, constrained only by same-symbol-same-letter, produced most of the key in one run; a dozen symbols were then fixed by hand. Details and the failure log are in `forster-1644/SOLUTION.md`.

## Sources

- Satoshi Tomokiyo, [Unsolved Historical Ciphers](https://cryptiana.web.fc2.com/code/unsolved.htm)
- Klaus Schmeh, [Top 50 unsolved encrypted messages](https://scienceblogs.de/klausis-krypto-kolumne/the-top-50-unsolved-encrypted-messages/)
- Nick Pelling, [Cipher Mysteries](https://ciphermysteries.com/)

Corpora used by the solvers (Corneille and Descartes from Project Gutenberg, a French frequency list) are not committed; the scripts say where to fetch them.
