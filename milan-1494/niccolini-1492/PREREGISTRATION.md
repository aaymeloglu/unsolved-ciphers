# Held-out test of key MAP LXXII 183 on Niccolini, MAP LXXIV doc. 81, c. 176r (21 Dec 1492)

Written 15 November 2026, before any transcription of c. 176r was made and before its gloss was read.

How blind the session that writes this file and scores is: it has seen c. 176r once at page size (1272 px), gloss
included, without reading the gloss, and it knows the key values. It does not transcribe, read the gloss or set the
sign divisions. Those are done by separate agents as below, and the scoring is mechanical.

## Fixed inputs
- Key: `milan-1494/key.json` at commit 26378c7, sha256
  abf087fb7f1176113e58cceea3c0731686b7cbcc5e6b81a17ffc4c16004cc89a. No value is added or changed for this test.
- Scorer: `milan-1494/held-out-114/score.py`, unchanged, sha256
  439bd0eae873ee9038f70e1f5d6f1a125533595d583970ed205d667a03bc5401.
- Locating and masking: an agent finds the cipher runs of c. 176r, paints out the interlinear gloss, and records the
  clear words that bound each run (`blocks.md`). It sees the gloss and sets the block boundaries; it does not
  transcribe and does not see the key.
- Transcription: an agent that sees only the gloss-masked crops and a value-free inventory of the family's signs
  under neutral labels (S10-S81, assigned at random; `signs-novalues.md`). It does not see the gloss, the key, the
  readings of 1494, issue #589 or this repository. New sign forms get new labels with a shape description. The
  transcription is frozen and its sha256 appended below before the decoder is run. No re-transcription after
  scoring. The neutral labels are mapped back to key.json labels by a table fixed before the transcription
  (`alias.json`); new labels map to an unidentified sign (wildcard).
- Reference: Niccolini's (or his secretary's) interlinear gloss over the cipher runs, read by a third agent that
  sees the unmasked crops but not the key or the transcription, and is told to read the gloss letters as written
  and not to count cipher signs to settle a spelling.

## One measurement
Character agreement between key output and the gloss, over all cipher blocks of c. 176r together, computed by
score.py exactly as in `held-out-114/PREREGISTRATION.md`: normalisation (lower case, letters only, accents stripped,
j = i, v = u); multi-valued signs match on any listed value; person signs, name numbers and unidentified signs give
one wildcard that never matches; global alignment per block, agreement = matched / max(output, reference) summed over
blocks; 1,000 shuffles of the value sets among the labels used; best and mean shuffle reported.

Bar: 0.85, the same bar as the doc. 114 test. Reported whatever it is.

Secondary, descriptive only: agreement with first listed values only; words exact.

## Then
c. 176r stops being held out. The four bare passages (doc. 42 c. 90r, doc. 49 c. 104r, doc. 81 c. 177r, doc. 90
c. 200r) are transcribed by the same blind procedure and decoded with the key, with or without changes justified by
the c. 176r gloss (each change recorded with its ground).

## Frozen transcription
(appended at freeze)
- alias.json sha256 4ccbfc7b7a6acd9c3eca4415394f56d66ab9bcf393c06256299383bafda937d6 (neutral label -> key.json label), fixed before transcription.
- transcription-176r-neutral.tsv sha256 db553e65df590eb2fe02b3477655dd34e7f13fdc1b20ba64cd2883e9e1b1fbd5 (144 cipher signs, 15 Nov 2026), frozen before the decoder was run.
- reference-gloss-176r.tsv sha256 e1a8afaf623b5aa8e16c284e8addfcbc0fb6036dd0f4bdf36b586085492ab77b, read by the gloss agent before scoring; illegible gloss letters are '?', which the normalisation drops.

## Result (15 Nov 2026)
- Pre-registered agreement 0.358 (first value only 0.351); best of 1,000 shuffles 0.247, mean 0.173. Bar 0.85: **failed**. Output and reference per block in result-gloss-176r.txt. Anything after this line is after the fact.
- transcription-bare-A-neutral.tsv sha256 ff3d4a0886e609d1b267223cac2d0021f866bfd3595380f6c202da532e506c3e and transcription-bare-B-neutral.tsv sha256 4bd4a682225e8d4e2436f3f8195fdb5252042c3005c773bce927f935c6c4fbee (176 signs each, two blind passes, 148/176 labels agree), committed before any decoding of the bare passages.
