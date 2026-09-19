# R1889, Brussels, 16 November 1635: reading and translation

**Substantial recovery, with unresolved glyphs and draft/copy variants.** This is a draft-assisted reading of an already cataloged pair, not a claim that the letter's contents have never previously been known. The [literal decoder output](results/R1889-expanded-literal.txt) remains the authority for what the selected cipher units actually produce. The expanded alphabet has 51 assignments, one disputed; it is not a recovered complete historical key sheet.

The final checked passage agrees with the draft at **93 of 95 letter positions**. The two remaining signs lie in the securely restored words *civitas* and *iam*; they leave no uncertainty about that passage's meaning. See [the final discrepancy check](FINAL-CHECK-1635.md). The original key-selection experiment remains in [the audit](VALIDATION.md).

## Readable Latin

Capitalization, punctuation, word division, u/v, and common title abbreviations are editorial. Square brackets identify a reading supplied or repaired with help from the draft; they are not literal cipher output. Superscript-style labels link to the apparatus below. Words outside brackets may still have spelling or draft/copy qualifications noted there. The salutation and all cleartext are distinguished from cipher text in the line-by-line literal file.

> Serenissime Rex, Domine Consobrine charissime,
>
> Litterae Regiae Dignitatis ac Dilectionis Vestrae, decima quarta proxime elapsi mensis Octobris datae, mihi fuerunt gratissimae, ob laeta quae ex iis de ulteriori exercitus Caesarei ad Saram fluvium facto felici progressu percepi nuntia.
>
> Ad hiberna vero quod attinet, quae Regia Dignitas ac Dilectio Vestra pro iam dicto exercitu Caesareo in archiepiscopatu ac civitate Trevirensi fieri desiderat: desuper Regiam Dignitatem ac Dilectionem Vestram celare nequeo, quod, uti nihil mihi optabilius quam eidem in omnibus gratificare, sic et in hac re lubenter vellem.
>
> Verum cum [civitas]¹ Trevirensis [iam]² inde a ducentis annis sub Regiae Suae Catholicae Maiestatis stet protectione, atque eo nomine ab eius milite semper, quando id necessitas postulavit, fuerit praesidio³ munita, uti etiam fuit cum Gallus vexilla regia superans eandem occuparet;⁴ conveniens esse arbitror, ut [praesidium]² hoc [regium]⁵ in dicta [civitate],⁶ [locisque]⁷ [circumiacentibus]⁸ conservetur, ex quibus sumet⁹ alimenta necessaria, tum ad sui ipsius, uti convenit, [tum]² [principis]¹⁰ electoris (cui [hactenus]¹¹ ex aerario Regiae Suae Catholicae Maiestatis [provisum]¹² fuit) sustentationem.
>
> Quibus aliisque bene perpensis rationibus ac circumstantiis, nullatenus dubito Regiam Dignitatem ac Dilectionem Vestram, quod [militi]² Caesareo in dictis locis difficulter hiberna¹³ concedi possint, aeque bonique laturam; cui de caetero diuturnam incolumitatem et optatos apprecor rerum omnium successus.
>
> Datae Bruxellis XVI mensis Novembris, anno MDCXXXV.
>
> Regiae Dignitatis ac Dilectionis Vestrae [subscription not completed in this copy].

In note 8, **circumiacentibus** means “surrounding.” Its `p^` glyph is deliberately unresolved in the literal transcript.

## English translation

This translates the intended reading above, including its marked restorations. “Your Royal Dignity and Affection” is the formal title rendered more naturally below as “Your Majesty”; the addressee was being addressed as a king in 1635. “His Catholic Majesty” is a different sovereign. The Latin's historical assertion about two centuries of protection is reported as written, not independently endorsed.

> Most serene King, my lord and dearest cousin,
>
> Your letter dated the fourteenth of last October was most welcome to me, for the good news it brought of the imperial army's further successful advance to the River Saar.
>
> As for the winter quarters that you wish to have established for the aforesaid imperial army in the archbishopric and city of Trier, I cannot conceal from you that, just as nothing would please me more than to oblige you in everything, I would gladly do so in this matter too.
>
> But since the city of Trier has stood under His Catholic Majesty's protection for two hundred years, and on that account has always been fortified with a garrison of his troops whenever necessity required it, as was also the case when the French, overcoming the royal forces, occupied it, I think it appropriate that this royal garrison should be maintained in the said city and the surrounding places. From these it will obtain the necessary supplies, both for its own support and, as is fitting, for the support of the prince-elector, for whom provision has hitherto been made from His Catholic Majesty's treasury.
>
> Having duly weighed these and the other reasons and circumstances, I have no doubt that you will take it in good part that winter quarters can only with difficulty be granted to the imperial troops in these places. I pray for your lasting well-being and for the desired success of all your affairs.
>
> Given at Brussels, 16 November 1635.

The passage beginning “as was also the case when the French…” is recovered substantially from the ciphertext and the draft's cipher margin; the main draft column there is heavily revised. *Vexilla regia* literally means “royal standards,” here translated metonymically as royal forces. The parenthetical support of the elector and the refusal to allocate winter quarters are clear in broad sense even though several individual encipherments remain uncertain.

## Apparatus: literal output, not hidden repairs

| Note | Location | Literal / evidence | Treatment in reading |
|---|---|---|---|
| 1 | P1.L11 | `x 12 y 15 37 7 31` → `ciuitcs`; arc below final signs also noted by XZ. Draft main column *ciuitas*. **Image, 18 Sept 2026:** the sign is a plain 7 of the same form as the 7s that read *c* elsewhere, not a *z* (this hand's *z* has a long tail) and not a *y*; the arc sits under `7 31` and is unexplained. | `[civitas]`; the sign is an inherited enciphering mistake or a correction the arc marks, not a transcription ambiguity. |
| 2 | P1.L12, L19, L23; P2.L02 | The sign transcribed `6` yields *e* in training *Caesareo/Trevirensi*, but *m* would be required in *iam, praesidium, tum, militi*. **Image, 18 Sept 2026:** at 3× the four *m*-position signs (L12 *iam*, L19, L23, P2.L02) have the same form as the *e*-position signs (L07, L08, L12 *Trevirensis*, L14): a tall stroke to the upper right on a closed bowl. XZ's 1635 transcription never uses the label `b`, but no second glyph is there to be conflated. | Mark restorations. The b/6 hypothesis is not supported on this copy: the copy writes the *e* sign where *m* is meant, four times. Main decoder retains the frozen e-value. |
| 3 | P1.L15–16 | The image reads `20 c o m`, as does the draft margin; the sequence gives `praesidio`. XZ transcribes `20 0 0 m`. | The transcription follows the image. The `o=a` assignment uses comparison-passage evidence (F04), so it is excluded from the frozen-key holdout score. |
| 4 | P1.L16–18 | `gallus uexilla regia superans eandem occuparet`. | Retained. Not replaced with the draft's cancelled *cum Gallo* construction. *Gallus* is collective “the Frenchman/French.” |
| 5 | P1.L19 | `regiue`, final `m` gives *e* under the otherwise stable key. Draft *regium*. | `[regium]`. Cannot be repaired by the separate b/6 hypothesis. |
| 6 | P1.L19–20 | `ciua/te` → `civate`, not *civitate*. | `[civitate]`, supplying *it* from the draft/grammar. The draft additionally specifies *Trevirensi* here; the cipher does **not**. |
| 7 | P1.L20 | `locisqce`, with 7-like sign producing *c*. Draft *locisq*. **Image, 18 Sept 2026:** both 7s in `30 7 p . 7 15` are plain 7s of the same form; neither is a *y*. | `[locisque]`; an inherited *c* for *u*, or the 7 doing duty for the *-que* abbreviation stroke, which it resembles. Not a transcription ambiguity. |
| 8 | P1.L20–21 | `circumiac⟦p^⟧ntibus`; target uses a p-like sign with a mark. | Reading *circumiacentibus* is likely. Draft main column instead has *circumuicinatibus*. The mark is retained; no null is invented. |
| 9 | P1.L21 | `sumet` vs draft main-column *sumat*. | Preserve target's *sumet* (“will obtain”), a plausible wording difference. |
| 10 | P1.L23 | `prinncipis`, extra n (`22 32`). Draft *Principis*. | `[principis]`, one n omitted editorially, not removed from cipher data. |
| 11 | P1.L24 | `cuihctenus`, lacks a letter for *a*. Draft has inserted *hactenus*. **Image, 18 Sept 2026:** `x y 15 10 7 34` with nothing between `10` and `7`; the omission is the encipherer's. | `[hactenus]`, supplied *a*. No invisible cipher symbol added. |
| 12 | P1.L25 | Working reading begins `9 q f...` → `brouisum`, but initial sign could be `g` (p). Draft margin appears `g q f...`; main draft *provisum*. | `[provisum]`. Target working 9 retained pending an independent glyph adjudication. |
| 13 | P2.L03 | XZ: `i u 9 p q 32 z` → `r⟦u⟧berna`. Draft *hiberna*. **Image evidence, 18 Sept 2026:** the first sign carries the top-left flag of this hand's digit 1 and has no i-dot (compare `1` in L07 and the dotted `i` in L12); the u-shape is two flagged strokes joined at the foot, the digit 11 written without lifting the pen (compare the separate `11` in P2.L02). The image supports `1 11 9 p q 32 z`; XZ's transcription is documented in the file header. | *hiberna* is literal output under the key (`1`=h, `11`=i). Both units are graded C from the draft alignment. |

Other limits: the abbreviated titles and punctuation are expanded/regularized in this edition; the exact crossed-out text and order of the draft's late revisions remain incomplete. A polished reading is not evidence that every cipher glyph has been resolved.

Later comparative evidence: the 1640 reading supports distinct labels `b=m` and `6=e` in that witness. On the 1635 photograph (checked 18 Sept 2026) the four *m*-position signs and the *e*-position signs are one form, so the 1635 copy itself uses the *e* sign for *m* in those four places; the 1640 distinction does not transfer. The original frozen key and first-pass holdout remain unchanged.
