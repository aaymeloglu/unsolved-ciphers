# Repository instructions

Read `CONVENTIONS.md` before changing a cipher reading or its evidence.

## Public pages describe current beliefs

Every public page must be self-contained and state the current reading,
evidence, uncertainty, and attribution. Assume the reader has never seen a
previous version. Do not narrate changes to the page or refer to superseded
claims: avoid phrases such as “the earlier argument is withdrawn,” “we
previously read,” “now corrected,” or “the old reading was wrong.” State what
the evidence supports directly, and replace obsolete claims wherever they
appear, including tables, notes, summaries, and generated content.

Preserve provenance and research history in explicitly identified audit files
and Git history. Current alternatives, literal output versus editorial repairs,
source-transcription differences, historical events, independent prior work,
and experimental controls are substantive evidence, not page revision history;
keep them when useful and explain them without assuming an earlier page.

When updating a reading, audit all public pages for this rule. Edit the source
generators (`docs/_build_site.py`, `docs/_moray.py`, `docs/_ferdinand.py`) or the
Ottobon source (`ottobon-1589/reading.html`), then regenerate with
`python3 docs/_build_site.py`. Check generated pages as well as their sources.
Run the checks in `.github/workflows/ci.yml` before publishing.
