# Catalogue sweep: undeciphered ciphers outside the standard lists

Compiled 18 September 2026 from three catalogues that Tomokiyo's, Schmeh's and Dunin's lists draw
on thinly and that cyphersolver's Gallica sweep did not cover: the DECODE database, the Biblioteca
Nacional de España, and PARES (Simancas, the Archivo Histórico Nacional, the Nobleza archive, the
Corona de Aragón). Everything here was selected from catalogue records and public metadata. **No
leaf has been looked at.** Each entry says what would confirm it is genuinely open.

Scripts and data in [`catalogue/`](catalogue/): `fetch_decode.py` (1,187 record pages), `fetch_pares.py`
`fetch_pares_pages.py` and `fetch_pares_images.py` (1,115 units, 536 description pages and image viewers), the BNE pull inside `rank_bne.py`'s
docstring, and the three `rank_*.py` scripts that produce [decode-ranked.md](catalogue/decode-ranked.md),
[bne-ranked.md](catalogue/bne-ranked.md) and [pares-ranked.md](catalogue/pares-ranked.md). The
JSONL files are the raw pulls. Record ids already on Tomokiyo's list or in cyphersolver are in
`exclude.txt` and `pares-exclude.txt` and were dropped before ranking.

Classes, by what stands between us and a reading:

- **A**: a key is attached to the record or sits in the same archive under a known shelfmark, and the
  images are public. The work is transcription and lookup, as with Ottobon and Starhemberg.
- **B**: a key or a decipherment of a sibling exists somewhere identifiable, but the images need a
  login, a reproduction order, or a visit.
- **C**: described as ciphered, no key known, no images online. A finding aid for later.

## 1. DECODE: 1,187 records marked non-decrypted or partly decrypted

DECODE's own status field is unreliable for our purpose: 124 of the "non-decrypted" or "partially
decrypted" records carry a deciphered text among their attached files, so they are read and are
listed separately at the end of `decode-ranked.md`. Of the 1,038 that remain, the useful signals
are an attached key, public images, inline cleartext, and keys from the same collection and period.
The Vatican material (Barb.lat and Segretario di Stato, 300 records) is where the community has
spent its effort and is scored down.

### Class A: key attached, images public

| Records | Date | Where | What | Confirm before starting |
|---|---|---|---|---|
| R3811–R3815, R4625, R4645, R4734, R4736 (9 letters, 3–38 pp) | Feb 1638 – Apr 1639 | Státní oblastní archiv v Plzni, Rodinný archiv Trauttmansdorffů, inv. 200, kt. 9 | Sigismund Kurtz von Senftenau, writing from Hamburg and Glückstadt, to Maximilian von Trauttmansdorff; one to Ferdinand III, one to Schwarzenberg. German, homophonic with bigrams and nulls, Greek-alphabet symbols, inline cleartext. Key attached to every record; two other Kurtz letters of 1639 in the same fonds (R4685, R4761) are marked decrypted, so the key reads this hand. | That the two decrypted letters are separate documents, not duplicates of these. Mírka, *Západočeské archivy* 2012, pp. 44–72, is the only publication and is a survey, not an edition. |
| R5019–R5024, R5029 (7 letters, 3–8 pp) | 1720–1722 | Same archive, Rodinný archiv Windischgrätzů, inv. 1433 | Charles VI to Leopold Viktorin von Windischgrätz, six letters, and one Windischgrätz family letter (R5029) with its key attached. Nulls and punctuation signs. Four Ernst Friedrich von Windischgrätz letters of 1721 in the same fonds (R5025–R5028) are marked decrypted. | Whether the key on R5029, or the one behind the four decrypted letters, is the one the emperor's chancery used for the six to Leopold Viktorin. |
| R2785, R2786 (3 pp each) | 1615, 1617 | BnF Français 18043 f. 83–84, 18044 f. 109–110 (Gallica) | Nicolas Brulart de Sillery (chancellor) to Brulart de Léon (his son, ambassador). French, numbers with diacritics, nomenclature; key attached, inline plaintext. Status "partially decrypted". | How much the partial reading already covers; whether the Brulart family correspondence in fr. 18043–18044 has been edited. Not in cyphersolver's catalogue. |

### Class B: key attached or in the collection, images behind the DECODE login

| Records | Date | Where | What | Confirm before starting |
|---|---|---|---|---|
| R413 (2 pp) | 1628 | TNA SP 106 box 5 | William Boswell, English and Latin, key attached; eleven SP 106 keys of the period in DECODE. Same correspondent as our closed-negative Boswell 1643. | Whether the attached key is the one Pitt used for the 1643 letters. |
| R8347, R8348 (4 pp each) | Jan 1568, 26 July 1569 | BL Add MS 33531 ff. 73–74, 79–80 | Scottish state letters of the Moray regency, the second addressed to the "Lorde Regent of Scotlande"; a key image is attached to each; ff. 27–30 and 99–104 in the same volume are marked decrypted. **This is the lead for our Moray target (R8345, Add MS 32091 f. 213, dated 1558 in DECODE, which is wrong: it is 13 July 1568).** | Whether the attached keys are the Wood/Cecil cipher whose 35-letter crib we recovered from Add MS 4136 f. 33. If so, Moray reads by lookup. |
| R8465, R8473, R8533, R8559, R8573 (1–4 pp) | 1526–1527 | BL Cotton Vespasian C III–IV | Siblings of the Worcester Latin letters (R8476, R8589, R8613), keys attached, English cleartext. | Almost certainly printed in *State Papers Henry VIII* VI or *L&P* IV like their siblings; check before anything else. |
| R660 (2 pp, Italian) and R931, R595 (English, 1 p each) | 1558, 1645, 1758 | TNA SP 106 box 7 and 10 | Transcription attached, 30–50 SP 106 keys of the period in DECODE. | The 1645 piece is of the Naseby haul; check *The King's Cabinet Opened* (1645). |
| R1325 (4 pp), R1212 (4 pp, Latin) | 1600, 1540 | ÖStA HHStA Staatskanzlei | Transcription attached (R1325) or inline cleartext; 180 and 19 Chiffrenschlüssel of the period in the same fonds, the Starhemberg route. | Which Schlüssel by date and correspondent. |
| R10171 (1 p) | 1435 | Archivo de la Corona de Aragón, Cancillería reg. 3225 f. 59r | Queen María of Castile to Alfonso V. The earliest item in the sweep. DECODE holds an ACA Cancillería key of 1437 (R10183) and one of 1413 (R10182). | Whether R10183 is the queen's cipher; whether the registro is on PARES with images (the Cancillería registers largely are). |
| R10172–R10180 (9 letters, 1–7 pp) | 1495–1498 | Archivo de la Corona de Aragón, Diversos, Sástago 193 | Ferdinand the Catholic's "cartas del Rey en cifra" to his ambassador Juan Ram, the same units PARES lists (section 3). DECODE holds a Sástago 193 key (R10184, dated 1520) and four ACA Reserva keys of the 16th century (R10185–R10188). | Whether R10184 is the 1490s key or a later one; the Gayangos *Alfabetos y cifras* at the BNE covers the Puebla correspondence of the same years. |

### Collections worth a systematic pass

| Records | Collection | Note |
|---|---|---|
| 45 | Brussels, Algemeen Rijksarchief, Secrétairerie d'État et de Guerre inv. 2559 | 1577–1678, Spanish; a transcription is attached to 44 of the 45. The Ferdinand 1635 draft came from the sister fonds (Allemande inv. 540). With the Simancas Estado keys this is the most attackable block after Plzeň: transcribed, one court, one language. |
| 178 | Real Academia de la Historia, signaturas 9/23–9/34 | 1424–1525, Spanish; no transcriptions, no keys in DECODE, images behind the login. The Catholic Monarchs' diplomacy; pair with the Gayangos *Alfabetos y cifras* and the ACA keys. |
| 40 | The Hague, Koninklijk Huisarchief, Prins Willem V inv. 192, 196, 201 | 1751–1804, French; transcriptions attached to 23. Keys of the Stadholder's secretariat may survive at the KHA. |
| 36 | Florence, Archivio di Stato, Dieci di Balia | Early 15th c., Latin cleartext; no transcriptions. |
| 16 | Riksarkivet, Stockholm | 1600–1646, images public; R4332 (1637) carries both a decipherment and a key, so one key of the Oxenstierna circle is at hand for the rest. |
| 24 | Naples, Archivio di Stato, Ministero degli affari esteri 2337 | 1816–1823, Italian; outside our period. |

## 2. Biblioteca Nacional de España: 173 manuscript records mentioning cipher

Pulled through the catalogue's public Primo API with the manuscripts facet. After dropping music
tablature: 58 letters described as ciphered with no decipherment in the note, 41 with the plaintext
noted alongside (interlinear, overwritten, or a "traducción de la cifra" on following leaves), and 2
keys or treatises. Full table in [bne-ranked.md](catalogue/bne-ranked.md). BDH digitisation is not
in the catalogue record and must be checked by shelfmark; the Ottobon volume (Mss/994) was, so the
BNE does put such material online.

### Worth confirming first

| Date | Shelfmark | What | Why |
|---|---|---|---|
| 12 May 1548; 1548–1554 | RES/261/73; MSS/20212/29, MSS/7909/189–192, MSS/20210/15, MSS/20214/61, MSS/7913/127 | Diego Hurtado de Mendoza (ambassador at Rome) to Cardinal Granvelle, one letter "cifrada" and a bundle of six with the first ciphered; Cardinal Carpi to Granvelle, six letters partly ciphered (1548–1550); Cardinal Sigüenza (1554); Jean de Saint-Mauris (1548, French) | The Granvelle correspondence at the BNE (MSS/7900s) is a coherent run of 1544–1555 diplomatic cipher. Van Durme's *Correspondance* and the Besançon Granvelle papers hold keys of exactly this circle. Class B. |
| 1622 | MSS/1868/96, RES/227/122, MSS/1869/17 | Archduke Leopold to Fernández de Córdoba, one letter "cifrada" without the overwritten decipherment its siblings have; Marqués de Mirabel to Carlos Coloma, Lyon, 8 Dec 1622, "carta cifrada"; the "papel cifrado" on the Palatinate war | Thirteen siblings in the same series carry the decipherment written over the cipher, which is a key in all but name. Class A if BDH has the volume. |
| 1628–1629 | MSS/1870/127–151 | Fernández de Córdoba to Philip IV and Olivares from Alessandria and Milan, seven letters "cifrada" or "mayormente cifrada", copies "para enviar a Don Fernando" | Same circle and key family as 1622. Class A/B. |
| 1658; 1664 | MSS/18621/14, 15, 27, 39 | Philip IV to the Marqués de Caracena, two royal letters ciphered, two partly | Habsburg royal cipher of the 1650s; PARES lists ciphered royal letters to Caracena and Albornoz 1648–1651 in AHNOB Osuna and Frías, so keys or decipherments exist across the two holdings. Class B. |
| 1679–1681 | MSS/18632/43–44, RES/261/58, MSS/20210/46 | Leopold I to Charles II, three letters "texto en español y cifrado", one autograph of 14 April 1680 (Prague); Diego Crolope, 12 Jan 1681, "texto cifrado" | Vienna–Madrid family cipher; the ÖStA Chiffrenschlüssel in DECODE cover the 1670s. Class B. |
| 1470–1479 | MSS/20211/56, 98, 123 (the three unread) | Thirteen letters of Ferdinand the Catholic to his father Juan II; ten have "cifra interlineal" (read), three are only "parcialmente cifrada": Dueñas 12 Nov 1470, Bilbao 5 Aug 1476, Córdoba 4 Nov 1478 | The ten read siblings give the key. Class A if digitised. |
| 1508–1512 | MSS/18640/54/1–8 | Ferdinand to Jerónimo de Vich, five letters, each with "traducción de la cifra" on its last leaves | Not targets: read. But they are the key for AHN Estado 8715, where cyphersolver read three of four; the fourth (N.73, 1515) may fall to these. |
| 1612; 18th c.; c. 1861 | MSS.MICRO/12253, MSS/18657/20, Gayangos (not expanded) | Tamayo de Vargas, *Cifra, contracifra, antigua y moderna* (485 ff.); *Reglas para descifrar sin contracifra*; Gayangos, *Alfabetos y cifras* from the Puebla correspondence 1488–1498 | Keys and method, not targets. The Gayangos volume is the key set for the Puebla–Ferdinand letters, of which PARES lists "carta en cifra" units at Simancas PTR 54 (1505). |

## 3. PARES: 1,115 units described as ciphered, 536 before 1800

Text searches for *carta cifrada*, *en cifra*, *cifrada(s)*, *descifrada* and *carta en cifra* across the
whole portal, then every pre-1800 description page. 70 units are transcriptions, decipherments or
drafts by their title or summary; 6 are cyphersolver's (García de Toledo 1565, Adrian of Utrecht
1521, the four AHN Vich letters); 460 remain. Full table with each unit's summary in
[pares-ranked.md](catalogue/pares-ranked.md).

**424 of the 460 have images on PARES, 5,204 page images in all.** The results list flags only three
as "Digitalizado Completamente", but each unit's image viewer reports its page count, and every
Simancas Estado unit has one (the 36 without are mostly Nobleza bundles and the Corona de Aragón
Sástago letters, whose viewer says no images are attached). So the Spanish material is class A or B
on images, and what stands between us and a reading is the key: Simancas keeps the Estado ciphers
as a separate series, and a key found for one Genoa letter of 1581 reads the forty-four beside it.
The archivist's title says "cifrada" and no more; a decipherment may sit in the same legajo
unmentioned, and in the Santa Cruz papers the summaries say so explicitly: several of Philip IV's
ciphered letters to the Marqués de Santa Cruz (1632–1635) are marked *[Sin descifrar]* and one *posible
descifrado*, which is the archivist telling us which ones nobody read.

### Series

| Units | Years | Series | Note |
|---|---|---|---|
| 50 + 45 + 39 + 35 + 25 + 16 + 14 + 14 + 11 × 4 | 1553–1600 | AGS Estado, Génova legajos 1383–1430 | The Genoa embassy: Gómez Suárez de Figueroa, Pedro de Mendoza, Pedro González de Mendoza, Juan Andrea Doria, Sfondrato, to Philip II and Philip III. Dozens of letters per year "cifrada" with their duplicates, every one with images on PARES. Simancas holds the Estado keys; DECODE has 12 AGS records, none of these. The largest homogeneous body of undeciphered-as-catalogued cipher in the sweep, and viewable tonight. |
| 16 | 1520–1521 | AGS PTR 1–3 | Cardinal of Tortosa (Adrian of Utrecht) and the Comuneros war; most units are transcriptions, i.e. the decipherments exist beside the ciphers. Class C for the ciphers, but a key can be rebuilt from the pairs. |
| 22 + 20 + 11 | 1520–1674 | AHNOB Santa Cruz, Osuna, Frías | Philip IV's ciphered letters to the Marqués de Santa Cruz (1632–1635, three bundles marked *[Sin descifrar]* in the summary, 21 of 22 units with images), to Cardinal Albornoz and Oñate at Rome (1648), Infantado (1650), Caracena (1651), Frías (1664) | Same royal ciphers as the BNE Caracena letters; the Santa Cruz units are the ones the archive itself calls unread. |
| 13 + 14 | 1639–1643 | AGS Estado 3594–3598 | Milan and Venice embassies under Philip IV. |
| 6 | 1495–1497 | ACA Diversos, Sástago 193 | Ferdinand the Catholic to his ambassador Juan Ram, "carta del Rey en cifra"; the same letters are DECODE R10172–R10180 (section 1, class B), with a Sástago key of 1520 catalogued as R10184. No images on PARES; DECODE has them behind its login. |

## 4. Leads for targets already on the tracker

- **Moray 1568**: DECODE R8347 and R8348, BL Add MS 33531 ff. 73–74 and 79–80, Moray-regency letters with keys attached, one addressed to the Regent. Check whether the key matches the Wood → Cecil glyph families before any more annealing.
- **Boswell 1643**: R413 (1628) has a Boswell key attached.
- **Ferdinand 1635/1640**: 45 Brussels Secrétairerie d'État et de Guerre records in DECODE for the same court.
- **Vich (cyphersolver's fourth letter)**: the BNE holds five Vich letters with contemporary decipherments.

## 5. What to do first

1. **Trauttmansdorff (Plzeň)**: pull the key image and the shortest letter (R4736, 3 pp) from DECODE's public files, transcribe, look up. If it reads, the other eight follow, then the Windischgrätz set.
2. **Moray key check** (R8347/R8348): one comparison of the attached key against our Wood glyph table.
3. **Brulart de Sillery**: Gallica images, key attached, French; see what "partially decrypted" left.
4. **BNE Fernández de Córdoba 1622/1629**: check BDH for MSS/1869–1870; the overwritten siblings are the key.
5. **AGS Estado Génova**: the images are on PARES. Transcribe one 1581 letter of Pedro de Mendoza (legajo 1414, 45 units in one key year) with `cipherkit.transcribe`, and search the Simancas Estado cipher series for the Genoa key of the 1580s; with 45 letters in one key, a ciphertext-only attack has more text than any target on the tracker.
6. **Santa Cruz 1632–1635**: the units marked *[Sin descifrar]*, with images, in a royal cipher whose siblings to Albornoz, Caracena and Frías survive across three holdings.
