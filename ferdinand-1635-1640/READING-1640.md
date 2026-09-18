# R1890, Vienna, 22 February 1640: Latin and English

**The encrypted body is now recovered in substance.** The alphabet reconstructed from 1635 was first applied unchanged. A subsequent, explicitly separate 1640 supplement adds 60 values, mostly syllables, without changing any of the 51 earlier assignments. The [literal output](results/R1890-supplemented-reviewed-literal.txt), [mapping evidence](key-1640-evidence.tsv), and [glyph-review log](transcriptions/R1890-review.tsv) allow the reading to be checked. This supersedes the earlier incomplete transfer report.

This is a contextual decipherment, not a collation with an independently preserved 1640 plaintext. The two pages make sustained sense with the same alphabet and a regular syllabary. Some singleton assignments, the precise spelling of a name, and apparent copying errors remain qualified below. No complete historical key sheet has been found.

## Readable Latin

Word spaces, capitalization, punctuation, u/v and expansions of cleartext abbreviations are editorial. Square brackets mark restorations or uncertain name completion, **not** literal decipherments. *Comunicabit*, *Catolici*, *Castagneti*, and *quatinus* retain the recovered spellings. The heading, salutation and closing are clear in the manuscript; the intervening body is enciphered.

> Ferdinandus Tertius, divina favente clementia electus Romanorum Imperator, semper Augustus, etc.
>
> Reverendissime ac Serenissime Princeps, frater et consobrine charissime.
>
> Comunicabit Dilectioni Vestrae orato[r] Serenissimi Regis Catolici, marchio Castagneti, ea quae circa novum apparatum militis in circulo Westphalico ab electore Coloniae et statibus illius circuli inceptum, ac quae inde in praeiudicium boni publici et etiam domus nostrae vereamur incommoda, secum fusius contulimus.
>
> Cum [igitur] illud negotium celeri remedio indigeat neque alius pro eo occurrat modus quam ut et nos festinanter collectionem militis, qui in potentiorem numerum quam dictus apparatus se extendat, in illis partibus instituamus, si alias liberam dispositionem ibidem servare et praecavere velimus ne ille circulus alieno arbitrio subiiciatur, ordinavimus ea propter quatinus comes [Hatzfeldius] se confestim Coloniam transferre atque huic operi, qua maiore potest celeritate, manum admovere debeat.
>
> Deficientibus vero nobis pro eo sumptibus necessariis, petimus a Dilectione Vestra denuo perinstanter quatenus iis quae sibi praedictus orator in [materia] distinctius expositurus est omnimodam fidem habere et, considerata rei gravitate, desideratos hactenus centum mille florenos Coloniam custodiae nostrorum ibidem existentium commissariorum (quibus [expresse] iniungimus ne quidquam ex illis praeter expressum mandatum nostrum aut comitis [Hatzfeldii] assignationem expendant) consignari curare velit.
>
> De caetero eidem Dilectioni Vestrae a Deo praepotente omnia ad votum prospera ac felicia desideramus. Dabantur in civitate nostra Viennensi die vigesima secunda mensis Februarii, anni salutis millesimi sexcentesimi quadragesimi, regnorum nostrorum Romani quarto, Hungarici decimo quinto et Boemici decimo tertio.
>
> Eiusdem Dilectionis Vestrae benevolus consobrinus et frater,
>
> Ferdinandus.

## English translation

“Your Affection,” the formal address *Dilectio Vestra*, is rendered as “you.” Bracketed repairs in the Latin are incorporated in the translation; the identification of Hatzfeld is probable, not a decoded value for the disputed symbol 14.

> Ferdinand III, by the favour of divine clemency elected Roman Emperor, ever august, etc.
>
> Most reverend and most serene prince, dearest brother and cousin,
>
> The ambassador of the Most Serene Catholic King, the Marquis of Castagneti, will inform you of the matters we have discussed with him at greater length concerning the new preparations for raising troops in the Westphalian Circle, begun by the Elector of Cologne and the estates of that Circle, and of the harm which we fear may result to the public good and also to our own house.
>
> Since this affair therefore requires a speedy remedy, and no other course presents itself than for us also to undertake promptly the raising of troops in those parts, in greater numbers than the said preparations envisage, if we are to retain freedom of action there and prevent that Circle from being subjected to another's control, we have accordingly ordered Count [Hatzfeld] to proceed immediately to Cologne and take this work in hand with all possible speed.
>
> As we lack the funds necessary for this, we again ask you most urgently to place full confidence in what the aforesaid ambassador will explain to you more distinctly on this subject and, considering the gravity of the matter, to arrange for the hundred thousand florins previously requested to be delivered to Cologne into the custody of our commissioners residing there. We expressly instruct them to spend none of those funds except under our express command or Count [Hatzfeld]'s authorization.
>
> For the rest, we wish you, from Almighty God, every prosperity and happiness according to your wishes. Given at our city of Vienna on 22 February 1640, the fourth year of our Roman reign, the fifteenth of our Hungarian reign, and the thirteenth of our Bohemian reign.
>
> Your affectionate cousin and brother,
>
> Ferdinand.

## Apparatus and limits

| Location | Literal evidence | Editorial treatment |
|---|---|---|
| P1.C01 | `op fu 47 ap tis 34` → `comunicabit`; `fu` occurs only here. | Single m retained. `fu=mu` is provisional; `mmu` would also fit classical spelling. No extra m inserted into decoder output. |
| P1.C01 end | `... f 50 plo ?` → `orato⟦?⟧`; right edge is obscured. | Supply `[r]`. No value assigned to `?`. |
| P1.C02–03 | `ap 31 pla / 16 46 pli` → `castagneti`. | Retain this Latin title spelling, without replacing it by a modern Spanish spelling. The ambassador is plausibly the Marquis of Castañeda; that historical identification was not needed to select the syllabary. |
| P1.C10 | `12 17 24 plu t` → `igitua`. | `[igitur]`. Final `t` produces a, unlike expected r. No t/r key switch. |
| P1.C20 | XZ's `ple/i?`, visually closer to `pli`, yields `quatinus`. | Retain variant *quatinus*. Review is logged and context-assisted. |
| P1.C21; P2.C11 | `ga 14 me 19 hi 35 31` / `ga 14 me 18 hi 12` → `ha⟦14⟧feldius/ii`. | `[Hatzfeldius/ii]`, probable name identification. 14 remains unassigned: z versus tz, a spelling variant, or another glyph requires better evidence. Two occurrences of the same name are not independent lexical evidence. |
| P2.C02–03 | `... ca ple 52 / hi...` → `materi / di...`. | `[materia]` supplies absent final a; no invisible token inserted. |
| P2.C08–09 | `p 39 g 51 3 / en` → `expred/se`. Last sign is at dark right edge. | `[expresse]`; final visible 3 may conceal a following 1, which would yield 31=s. Retain source 3 until that reading is established. |
| P1.C12; P2.C07 | `lx=oc` in *occurrat*, `li=xi` in *existentium*. | Contextual singleton group values, provisional. Source labels preserved; these are not claims that both glyph labels are palaeographically final. |
| Various | 16 documented review amendments; notably looped `l/z?`→`z`, joined `c/1?o/0?`→`co`. | Original imported token stream remains unchanged. The reviewed stream and its literal output are separate. Some choices use plaintext context and must not be counted as independent validation. |

The cipher has no demonstrated nulls in this reading. The 41–54 sequence gives *le li lo lu na ne ni no nu ra re ri ro ru*; the unused presumed 40 cell is not assigned. Families such as `pla/ple/pli/plo/plu`→*ta/te/ti/to/tu* and `ap/ep/ip/op/up`→*ca/ce/ci/co/cu* explain repeated groups without splitting them into alphabetic symbols.

The expanded map covers 779 of 782 reviewed units. The three unmapped occurrences are `?` and two `14`s. **That is coverage, not 99.6% verified accuracy**: known mappings still produce the malformed words shown above, and several singleton values are contextual. All 51 pre-existing 1635 assignments remain unchanged in the supplemented key; this strongly supports a shared alphabet/key system for the observed material, while identity of every unused historical key entry remains untestable.

Cleartext countersignatures provisionally read *Furstenberg* and *Jo: Georgius Pucher[g?]*. They were not used as cryptanalytic cribs. Prior plaintext publication and global novelty remain unestablished; see [sources](SOURCES.md).
