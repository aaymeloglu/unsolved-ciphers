# Repository instructions

The work here was done by LLM agents (Claude Code and Codex) with a person checking it. Every
reading in this repo came from finding something outside the ciphertext: a surviving key, a draft
in clear, a contemporary gloss, a printed edition, or word boundaries plus a period lexicon. Blind
cryptanalysis of a short nomenclator read nothing on its own. Most of the time lost went to three
things: attacking items that were already solved in print, waiting on image access, and running
solvers whose negative results meant nothing because no control had been run.

Read these before touching a target:

- `CONVENTIONS.md`: the evidence standard (grades H/C/S/M/I, matched controls, printed editions
  first, absolute dates).
- `TARGETS.md`: every target touched, its status and next step. `CATALOGUE.md` section 5 is the
  queue of new leads from the DECODE, BNE and PARES sweep.
- `cipherkit/README.md`: the shared solver package. New scripts import it rather than copying a
  scorer from another folder.

This file covers what has to be available for any of that to work.

## Capabilities to have before you start

**1. Reading images.** Nearly every target starts with a transcription made by looking at the
manuscript: Moray from the DECODE page image, Ferdinand from photographs of the cipher and its
draft, Starhemberg by collating photographs against a published digit transcription. Other
people's transcriptions are a starting point, not ground truth; the Moray list transcription
conflated two glyphs, and one Tomokiyo file used his own symbol IDs where we assumed ciphertext
numbers. A model that cannot view a local JPEG can still run the solvers on an existing
transcription, but it cannot make or check one.

**2. A shell, Python 3.12, and uv.**

    uv sync --frozen
    uv run pytest -q
    uv run python -m cipherkit.corpora fetch fr     # period corpus into corpora/ (gitignored)

Pillow is the only runtime dependency. Corpora are fetched from Gutenberg and Internet Archive
OCR and cleaned at fetch time; after any change to the cleaner, refetch with `--force` (a cache
stamp enforces this).

**3. Plain outbound HTTP.** Most sources answer a GET: archive.org `_djvu.txt` full text for the
printed editions, Gutenberg, DECODE record metadata (public without login), Gallica IIIF, the
Biblioteca Digital Hispánica, PARES. The printed-edition check in `CONVENTIONS.md` section 3 is
almost entirely archive.org text search, and it is the step that caught Richelieu 1629 (Avenel
1858) and Worcester 1526 (State Papers VI) before a solver was wasted on them.

**4. A DECODE account.** This is the one credential worth setting up in advance. Register at
[de-crypt.org](https://de-crypt.org/). A basic account sees metadata and thumbnails; full-size
images for many holdings (British Library, The National Archives) need permission from the DECODE
team, which was granted here on request to the project PI, Beata Megyesi (Stockholm University);
the `decode@` address on older pages bounces. After permission changes, log out and back in or
the old session keeps the old rights. Images obtained this way may not be redistributed.

Once logged in, curl works and is faster than a browser: `ImagesList?showmaster=records&fk_id=<record>`
lists the image files and `/decrypt-custom/filesrv/?file=<name>` serves them at full resolution;
`DocumentsList` does the same for attached keys and transcriptions. Many attachments labelled
"Key" are Tomokiyo's reconstructed alphabets for a different letter, and a few are modern
worksheets. Check what an attachment actually is before testing it as a key.

**5. A browser, for what HTTP will not do.** British History Online and HathiTrust refuse curl
(CAPTCHA and 403) but work in a browser; so do some publisher PDFs behind a cloud challenge. We
used the Aside CLI; Playwright or a Chrome extension driver does the same job. Use it to fetch,
not to think: transcription and analysis happen locally on the downloaded files.

Never point a browser or scraper at books.google.com page views; a burst captcha-walls the network
for hours. If you need Google Books, use the Books API with a key and read the passage in an
archive.org copy of the same scan.

**6. Parallel subagents, if the harness has them.** They earn their keep in two places.
Independent transcription passes: Ottobon was read by three separate agents from the public BNE
scans and their outputs compared, and the Debosnys audit used a fresh-context reviewer given
anonymous crops and no prior labels. `cipherkit.transcribe compare` and `consensus` merge the
passes. And source audits: one agent per printed edition or archive catalogue, since they are
independent.

**7. A second model for review.** Overclaiming is the characteristic failure here, and the model
that wrote a reading does not catch it in its own work. The forms it takes: word-like output from
an annealer presented as plaintext (shuffled Gun Wa ciphertext also yields convincing fragments),
a conjecture promoted into the key because it completes a sentence, a partial gloss written up as
a complete solve, or "nothing found" written up as "unsolvable". Ottobon was deciphered by Codex
and reviewed by Claude, which disputed several readings and found the title-page note on who
broke it in 1589. Have the other model check every claimed reading against the image and the key
before anything is published.

## What you do not need

No paid databases, no archive visits, no OCR or image-processing libraries beyond Pillow (the
model reads the page; `cipherkit.transcribe` cuts it into line strips), and no email access until
there is a result to report.

## Before you attack a target

1. **Check it is still open.** Search the cipher's name, then the sender's standard printed
   correspondence on archive.org, then the calendars, then the source list's comment threads and
   r/codes. Two other projects sweep the same lists:
   [dbourdeau/cyphersolver](https://github.com/dbourdeau/cyphersolver) and Robert Pitt's
   repositories. Check both. Six targets on the tracker turned out to be `found-solved`.
2. **Look for a key or a crib.** DECODE key records for the same correspondents and years, drafts
   in clear (Ferdinand's came from DECODE R954), contemporary glosses in the printed edition
   (Vande Perre), printed decipherments of other letters in the same key (Royalist 1646 via
   Evelyn). This is where the readings came from.
3. **Transcribe from the image**, with `{a/b}` at every doubtful sign. Never silently repair the
   ciphertext; repairs live in their own file and are graded I.
4. **Then solve**, running a matched control first (`cipherkit.controls.matched_control`). If the
   solver cannot read a synthetic text of the target's length and symbol density, it will not read
   the target, and more restarts will not change that. Homophonic nomenclators under about five
   tokens per symbol did not fall to statistics anywhere here (Boreel, Boswell, SP 53/16); Debosnys
   took eleven rounds to establish that its controls fail. Go find more text or a key instead.

## Network quirks that cost a run

| Symptom | What is happening |
|---|---|
| DECODE image list empty or forbidden while logged in | Your account lacks permission for that holding. Request it, then log out and in again. |
| DECODE "Key" attachment does not fit | Often a modern reconstruction for a different letter. Moray's R8347/R8348 were Tomokiyo's alphabets for other correspondents. |
| British History Online CAPTCHA | Blocks curl and WebFetch. Use a browser. |
| HathiTrust 403 | Same; a browser gets the page. |
| PARES TLS error | Incomplete certificate chain; curl gets through. The "Ver Imágenes" flag in results lists is unreliable; count pages in the viewer instead. |
| archive.org `_djvu.txt` 404 on a filename with spaces | The space has to be double-encoded as `%2520`. |
| A period corpus is garbage | Fraktur OCR (Arneth) is unusable. `clean_ocr` drops lines by language markers; check `describe(lang)` before trusting a model. |
| `transcribe layout` finds no lines | Photographs with a dark frame or a curled sheet. Try `--crop auto --flatten --slabs 4`; Ferdinand's R1889 needed all three. |

## Quick start

    uv sync --frozen
    uv run python -m cipherkit.corpora fetch all
    uv run python -m cipherkit.transcribe layout page.jpg -o page.layout.json
    uv run python -m cipherkit.transcribe strips page.layout.json -o strips/
    # read the strips, transcribe with {a/b} alternatives, then solve with a control first

Pick the next target from `TARGETS.md` ("What to do next") or `CATALOGUE.md` section 5. A target
folder gets a `README.md`, the transcription as read, the key, and a `decode.py` or `verify.py`
that reproduces the reading and exits non-zero if it is stale (`CONVENTIONS.md` section 5). Add
the verifier to `.github/workflows/ci.yml`, update the row in `TARGETS.md` and the root
`README.md`, and record the attempt whatever the outcome, so negatives stay visible.

    uv run pytest -q && uv run python docs/_build_site.py

## House rules

Do not commit images from DECODE or the British Library, or any image whose licence does not
allow it. Our own transcriptions made from those images may be published with a provenance note
saying the image is not redistributed.

Do not email archives, libraries or list maintainers from a research run. Reporting is a separate,
deliberate step.

Say what was checked and what was not. A README distinguishes what a search excluded, what
returned nothing, and what could not be reached. A negative result appears next to its matched
control. Dates are absolute ("18 Sept 2026", never "yesterday").

### Public pages describe current beliefs

Every public page must be self-contained and state the current reading, evidence, uncertainty,
and attribution. Assume the reader has never seen a previous version. Do not narrate changes to
the page or refer to superseded claims: avoid phrases such as "the earlier argument is
withdrawn", "we previously read", "now corrected", or "the old reading was wrong". State what the
evidence supports directly, and replace obsolete claims wherever they appear, including tables,
notes, summaries, and generated content.

Preserve provenance and research history in explicitly identified audit files and Git history.
Current alternatives, literal output versus editorial repairs, source-transcription differences,
historical events, independent prior work, and experimental controls are substantive evidence,
not page revision history; keep them when useful and explain them without assuming an earlier
page.

When updating a reading, audit all public pages for this rule. Edit the source generators
(`docs/_build_site.py` and the per-target `docs/_*.py` modules) or the Ottobon source
(`ottobon-1589/reading.html`), then regenerate with `python3 docs/_build_site.py`. Check generated
pages as well as their sources. Run the checks in `.github/workflows/ci.yml` before publishing.
