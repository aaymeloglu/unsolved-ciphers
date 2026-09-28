# Scoring, evidence and coverage diagnostics

## Check a scorer before optimizing it

An objective can prefer a correct message to shuffled text yet reward small
errors in that message. `perturbation_report` measures this using a supplied key
and the same mapping-to-score interface as `anneal`:

```python
from cipherkit import CharLM
from cipherkit.diagnostics import perturbation_report

tokens = ["A", "B", "A"]
true_key = {"A": "a", "B": "b"}  # a synthetic control's known answer
lm = CharLM.from_text("ababaabababa", order=2)
report = perturbation_report(
    tokens, true_key, "abc",
    lambda key: lm.score("".join(key[g] for g in tokens)),
    singletons_only=True,
)
print(report["tested"], report["improving"], report["tied"])
```

Higher scores must be better. Changes apply to every occurrence of a symbol;
this is a homophonic reassignment experiment, not a bijective key swap. Inputs
and the supplied key are preserved. Duplicate alternatives count once;
nonfinite scores are errors. `local_optimum` is `None` when nothing was tested.
Ties are reported separately and do not establish a unique reading. Examples
are capped by `max_examples`; aggregate counts cover the full experiment.

Train outside the control passages and report the exclusion policy. This
function does not construct that split or run a cold-start search. A false
alternative scoring higher diagnoses a local preference; it does not prove
approximate recovery impossible. Passing this test does not prove a solve.

## Save checkable source rejections

For a proposed source passage, assume each glyph has one fixed nonempty string
value, with homophones permitted and row boundaries preserved. Length and
single-glyph domain contradictions can exclude a candidate under that model:

```python
import json
from pathlib import Path
from cipherkit.evidence import rejection_record, verify_rejection

record = rejection_record([["x", "y"], ["x"]], ["ab", "c"])
assert record["status"] == "rejected"
assert verify_rejection(record)
Path("rejections.jsonl").write_text(json.dumps(record) + "\n")
```

```sh
python -m cipherkit.evidence rejections.jsonl
```

Each record embeds the exact glyph/plaintext rows and their SHA-256, the model,
and a specific witness. Keep source identifiers and normalization policy with
it (additional metadata fields are allowed). The hash binds input to evidence;
it does not authenticate the transcription or source attribution.

`None` means an unknown plaintext row, which cannot supply a contradiction.
Every character in a string, including `#`, is literal. Contradictions in known
rows remain valid when other rows are unknown. This API does not represent
alternative pronunciations, null glyphs or transposition: check those models
separately before making a broader exclusion claim.

The producer uses offset dynamic programming. The verifier independently places
fixed blocks separated by minimum-length gaps, enumerating possible glyph values
in a different order. Edited inputs, malformed records, unsupported models and
inconclusive results fail verification. The CLI also exits nonzero for empty
files. Resource limits (`max_candidates`, `timeout`) return **inconclusive**, as
does finding no contradiction. These checks are not a complete solver and never
certify a compatible key. Passing planted examples remains necessary when adding
a new source-search procedure.

## Measure what a corpus search could actually read

```python
from cipherkit.coverage import coverage_report

report = coverage_report(
    [["le", "soleil"], ["brille"], ["le", "soleil"], ["encore"]],
    {"le": ["lə"], "soleil": ["sɔlɛj"], "encore": ["ɑ̃kɔʁ"]},
    window_size=2,
)
print(report["evaluable_windows"], report["windows"])
print(report["correction_queue"])  # brille is the next lookup to resolve
```

`python -m cipherkit.coverage input.json` accepts the same arguments as JSON.
The caller supplies tokenized rows and a dictionary of pronunciation variants
(or other usable representations). At least one nonempty variant is required.
No normalization or correction is implicit. Empty variant lists are missing;
empty rows are barriers, not silently deleted. A corpus too short for a window
has `window_coverage: null`.

The report separates known tokens, evaluable rows/windows, windows with missing
words, and windows crossing empty rows. Overlapping windows are not independent
passages. The correction queue counts both all windows a missing word blocks and
those where correcting that word alone would recover the window. Repeated words
count once per window. The queue is capped by `max_missing`, with omitted types
reported; coverage totals always include every missing word. Resolve proposed
OCR corrections or pronunciations against the source, then rerun the report.
The queue does not supply guessed corrections.

## Debosnys integration check

The local round-12 investigation supplies a real-data replay for all three APIs:

```sh
python tools/check_debosnys_round12.py /path/to/debosnys --output /tmp/debosnys-replay
python -m cipherkit.evidence /tmp/debosnys-replay/rejections.jsonl
```

The research directory is separate from this repository. It must include the
round-4 controls and training exclusions, round-5 source reader/dictionaries,
round-11 transcription and round-12 downloaded sources/results. The replay
imports those local research readers; run it only on the trusted experiment
directory. It downloads nothing and leaves original results unchanged. This
optional replay is not a portable CI fixture; ordinary tests run without it.

Outputs include scorer reports, source-bound JSONL witnesses, and lookup coverage
with correction priorities. Counts must agree with the saved experiment.
