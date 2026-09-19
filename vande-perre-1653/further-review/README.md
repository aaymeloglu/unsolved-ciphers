# Vande Perre: further source review, 19 September 2026

The core decipherment is convincing. Four additional cipher runs are present on the next
page of the October letter, giving three securely glossed code groups and one additional
recoverable Dutch word. The two original troublesome fragments remain unresolved.

## Additional text on page 523

The letter beginning on p. 522 continues on [p. 523](https://archive.org/details/collectionofstat01thur/page/n552).
Its date is **10 October 1653, New Style**, printed at its conclusion. The page image was
downloaded from `https://archive.org/download/collectionofstat01thur/page/n552.jpg` and read
directly. The OCR is inaccurate here: in particular it gives 100 where the scan prints **109**.

| Run | Printed groups | Reading | Basis |
|---|---|---|---|
| P523.1 | 109 | Major-General Harrison | Printed gloss `M. G. Harrison`; C |
| P523.2 | 3.17.3.43.22.27.12.26.27.7.17 | ana[ba]ptisten | Ten existing letter values; 43 interpreted as 4.3 = ba, I; agrees with gloss `Anabaptists` |
| P523.3 | 76 | Denmark | Printed gloss; C |
| P523.4 | 52 | queen of Sweden | Printed gloss; C |

In context, the letter reports that the influence of Harrison and the Anabaptists is
declining, and that Colonel Wurts, presenting himself as an envoy of Denmark, receives a
yearly pension from the queen of Sweden. These meanings were already supplied by the
historical translators. This is an extension of our inventory and reconstructed code list,
not a first discovery of those meanings.

The inventory consequently contains **at least 20 runs and 322 printed groups**, not 16 and
308. Under the conservative proposed treatment of 43, the expanded grades would be
304 S / 5 C / 13 I. These are token mapping grades, not a percentage of securely understood
meaning. The existing baseline's unresolved fragments remain within its S count.

Do not infer a general homophone 43=b: that gives `anabptisten`. Reading the token as ba
gives `anabaptisten`. Whether 43 is an intentional syllable code or joined printing of 4.3
cannot be settled from this occurrence. This also cautions against confidently calling 77
an intentional ee digraph: 7.7 produces the same letters. The reading ee is useful; the
mechanism needs an original manuscript or another witness.

English labels in braces in the mechanical output identify code meanings. They do not
claim that the underlying Dutch wording or titles have been recovered exactly.

## The open fragments

### P522.2: `diemnicvndament`

The source crop confirms 6.12.7.15.17.12.5.28.17.6.3.15.7.17.27. A conjectural
`die met fvndament` agrees with the English gloss and the context of someone able to speak
with good grounds, but requires **three**, not two, consecutive letter substitutions:

| Position | Printed | Literal | Required |
|---|---|---|---|
| 5 | 17 | n | e (7) |
| 6 | 12 | i | t (27) |
| 7 | 5 | c | f (8) |

The v/u spelling in fvndament is a separate normalization. The passage does not establish
these three changes, nor the exact original wording. No alternative manuscript text was
obtained. Preserve the literal output and label the full phrase conjectural.

### P582.4: `ote`

The scan clearly prints 21.27.7 immediately after the English word `fleet`. One possibility
is a residual Dutch word ending, `[vl]ote` or `[vlo]ote`, duplicated or partly retained during
translation/copying. The same paragraph mixes English translation and Dutch original:
`to look to them` precedes `bewaren`, and English `want of masts` precedes the partly ciphered
`gebreck van masten bevonden`. This gives the hypothesis some contextual motivation.

It does not establish a missing prefix, explain precisely how it was lost, or exclude a
damaged separate word. Neither proposed prefix is encoded by the three surviving numbers.
**Still unresolved.**

### P522.4: `tenprincipaln`

The reading `ten principal en` adds an e; it is not just a word division. An explicit
representation is `ten principal [e]n`. The boundaries are not securely fixed by the loosely
placed English glosses. A different emendation to `ten principale` changes the final n to e;
it should not be adopted merely to improve grammar. No exact original wording recovered.

## Historical and source corrections

The ambassador was **Paulus van de Perre**, not Johan. See the
[NNBW biography](https://www.dbnl.org/tekst/molh003nieu05_01/molh003nieu05_01_0674.php),
which identifies the 1651/52 and 1653 envoy, and the
[Nationaal Archief inventory](https://www.nationaalarchief.nl/onderzoeken/archief/3.01.17).
The NNBW bibliography itself cites the ambassadors' Verbael under a title containing
`J. van de Perre`; distinguish that bibliographic wording from the subject's identification.

The printed source gives manuscript references that can support a focused original-source
check. The [British Library catalogue of Birch's index](https://searcharchives.bl.uk/catalog/040-002109624)
explicitly says these volume/page references point into Bodleian MSS Rawlinson A 1-67.
Accordingly, the following are source-backed location leads, not inspected manuscripts:

| Letter / print | Birch's manuscript reference | Modern volume inferred from the catalogue |
|---|---|---|
| 29 August, p. 431 | Vol. V, p. 226 | MS. Rawl. A. 5, old p. 226 |
| 3 October, p. 500 | Vol. VI, p. 355 | MS. Rawl. A. 6, old p. 355 |
| 10 October, pp. 522-523 | Vol. X, p. 471 | MS. Rawl. A. 10, old p. 471 |
| 4/14 November, pp. 575-576 | Vol. VIII, p. 50 | MS. Rawl. A. 8, old p. 50 |
| 11/21 November, p. 582 | Vol. VIII, p. 102 | MS. Rawl. A. 8, old p. 102 |

**Later catalogue check:** X/471 is genuinely printed, but A.10 is principally Dec 1653–Feb 1654.
A.6 has 10 October letters at pp.463 and 474; A.6 p.471 is an alternative location to investigate,
not a verified correction. See [the expanded audit](../evidence-audit/README.md).

The margin on the retained p. 522 image was checked visually for X/471; p. 582 for VIII/102.
Other references above were collected from the volume OCR and should be checked against
full-page scans before ordering images. Old page numbers may differ from modern foliation.
The referenced witness may be an interception copy or English translation, not the Dutch
autograph; catalogue provenance alone does not establish its language or decipherment state.

## Scope and reproducibility

`python3 verify_review.py` independently checks the baseline inventory/grades, decodes the new
runs, and enumerates the exact repairs needed by the two editorial suggestions. The baseline
files are snapshots of the public repository as read on 19 September 2026. `additions.json`
keeps original groups, glosses, and proposed readings separate. `p523.jpg` is the public-domain
1742 scan, not a DECODE image.

The full Internet Archive volume OCR was searched for Vande Perre headings and adjacent
number runs, including the continuation of each of the five letters. This is a discovery
pass, not an exhaustive page-by-page inventory of every letter in the book. No additional
matching cipher letter beyond these continuation runs was verified.

The subsequent [expanded evidence audit](../evidence-audit/README.md) inspected the Bodleian
catalogues through Aside, screened Colenbrander and First Dutch War V–VI, verified current
Zeeland inventory entries, and found an unprinted cipher letter. The 1725 Verbael remains
incompletely inspected because Google Books downloads/viewer requests met verification and
rate-limit responses. No target manuscript images were obtained and no outreach was sent.

Further statistical searching cannot identify missing or misprinted symbols uniquely in
these tiny fragments. The productive next evidence would be the corresponding manuscript
pages, a Dutch-side copy, or another letter demonstrably using the same key. The p. 523
additions strengthen and enlarge the existing result but do not solve its two residual gaps.
