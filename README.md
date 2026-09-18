# Unsolved ciphers

**Site: [aaymeloglu.github.io/unsolved-ciphers](https://aaymeloglu.github.io/unsolved-ciphers/)** with side-by-side readings of [Ottobon 1589](https://aaymeloglu.github.io/unsolved-ciphers/ottobon-reading.html) [Forster 1644](https://aaymeloglu.github.io/unsolved-ciphers/forster-reading.html) and, partially deciphered, [Starhemberg 1758](https://aaymeloglu.github.io/unsolved-ciphers/starhemberg-reading.html).

Working repo for attempts on historical ciphers that are short, context-rich, and listed as unsolved. Started September 2026 after Vals AI reported Claude Fable 5.1 reading Thomas Urquhart's Cyphral Distich; the question was whether the same approach (an agent plus a person checking its work) gets anywhere on the rest of the list. Only open items and our own solves go here. Work uses Claude Code and native Codex agents. Scripts reproduce decoding from the transcriptions; handwriting judgments require comparison with the cited images.

## Contents

| Folder | Item | Status |
|---|---|---|
| [`forster-1644/`](forster-1644/) | Sir Richard Forster's ciphered letter, 13 May 1644 (Karen Britland, *Critical Quarterly* 2013; Tomokiyo's unsolved list) | **Read 14 Sept 2026; not the first reading** (George Lasry and Norbert Biermann earlier, Robert Pitt the same day). Mixed letter-and-number homophonic substitution; plaintext is spiritual counsel to preserve one's life. Three symbols in 207 need repair. Independently re-verified. Not yet checked against the manuscript (AD Val-d'Oise 68 H 8). |
| `burgess-1912/` | Gelett Burgess, *The Master of Mysteries*, the third hidden message | Open. Simple acrostic families exhausted; notes list what was tested. |
| `royalist-1646/` | Two intercepted royalist letters in cipher, 13 and 21 May 1646 (BL Add MS 72438 ff. 9-10, Weckherlin's papers; Tomokiyo's unsolved list) | Open, partial. The 13 May letter's cipher is identified as key no. 129 of Digby's captured cabinet ("from the Queen's Court"), also used by the King in June-August 1646; about 45 values fixed from the surviving key page and Evelyn's printed decipherments. Full reading needs the rest of the key or the contemporary decipher. |
| [`ottobon-1589/`](ottobon-1589/) | Venetian dispatch to Giovanni Mocenigo, 27 April 1589, with reply to Gerolamo Gondi dated 24 April (BNE Mss/994 ff.35r–38r) | **Substantially deciphered, 16 Sept 2026.** Surviving key “Ziffra prima” (DECODE R1789) reads both letters; local gaps and apparent encoding errors remain explicit. Italian/English editions, source links, transcription and reproducible decoder. |
| [`starhemberg-1758/`](starhemberg-1758/) | Georg Adam Starhemberg, Paris, 23 May 1758 (Cryptiana transcription) | **Substantial partial decipherment, 18 Sept 2026.** Existing 1752 Prima/Secunda key (DECODE R1695/R1698) yields connected German about Wall, Spain, Minorca and negotiations. Exact full text remains unresolved; proposed repairs are explicit. German reconstruction, qualified English summary, working keys and reproducible checks. |
| `SHORTLIST.md` | Candidates, with per-item status checks | |
| `docs/` | The GitHub Pages site; `python3 docs/_build_site.py` rebuilds it | |

## Conventions and tracker

[CONVENTIONS.md](CONVENTIONS.md): per-group grades (H key source, C known plaintext, S cryptanalytic with a control, M uncertain, I supplied), matched controls before any negative, printed editions before any campaign, absolute dates. [TARGETS.md](TARGETS.md): every target touched, its status, evidence and next step. [CATALOGUE.md](CATALOGUE.md): the 18 Sept 2026 sweep of DECODE, the BNE and PARES for undeciphered letters not on the standard lists, ranked by what stands between us and a reading.

## Method notes

Two things carried the Forster solve, and neither was cryptanalytic cleverness: known word boundaries, and a lexicon with 17th-century spellings (estoit, mesme, roy, luy, ie). Character n-gram hill climbing on 207 tokens over 34 symbols went nowhere. A beam search over dictionary words, constrained only by same-symbol-same-letter, produced most of the key in one run; a dozen symbols were then fixed by hand. Details and the failure log are in `forster-1644/README.md`.

## Sources

- Satoshi Tomokiyo, [Unsolved Historical Ciphers](https://cryptiana.web.fc2.com/code/unsolved.htm)
- Klaus Schmeh, [Top 50 unsolved encrypted messages](https://scienceblogs.de/klausis-krypto-kolumne/the-top-50-unsolved-encrypted-messages/)
- Nick Pelling, [Cipher Mysteries](https://ciphermysteries.com/)

The solvers build their language models from `cipherkit.corpora` (`uv run python -m cipherkit.corpora fetch all`); nothing else is needed.

## cipherkit

Shared solver pieces, so a new target does not start by copy-pasting a quadgram scorer and an
annealing loop from the last one. See [`cipherkit/README.md`](cipherkit/README.md).

```bash
uv sync                                   # Python 3.12 venv with the package, pytest, Pillow
uv run pytest -q                          # 38 tests, about 10 s
uv run python -m cipherkit.corpora fetch fr   # period corpus into corpora/ (gitignored)
uv run python -m cipherkit.transcribe layout page.jpg -o page.layout.json   # line strips, two-pass compare, review page
uv run python some-target/solve.py        # scripts import cipherkit from the venv
```
