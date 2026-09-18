# Sources and prior-solution audit

Checked 18 September 2026. This is a bounded source review, **not proof of global novelty**.

## Manuscripts and attachments

All three records are from Brussels, Algemeen Rijksarchief, Secrétairerie d'État Allemande, inventory 540. The six previously downloaded images were used; their names, sizes and hashes are in [manifest.json](sources/manifest.json). No manuscript images or authenticated HTML have been placed in this folder.

| Record | Witness and current catalog status | Attachment inspection |
|---|---|---|
| [R954](https://de-crypt.org/decrypt-web/RecordsView/954) | Partly encrypted draft, 16 November 1635; *Decrypted*. The main Latin text and margin cipher survive. | Record page showed no attached transcription/document link. The images are the primary evidence. |
| [R1889](https://de-crypt.org/decrypt-web/RecordsView/1889) | Cipher copy, Cardinal-Infante Ferdinand to the future Ferdinand III, 16 November 1635; *Non-decrypted*. Catalog itself cross-references the draft. | [D3605](https://de-crypt.org/decrypt-custom/filesrv/?file=DOC_R1889_D3605_3605.txt), XZ, January 11, 2021. Ciphertext plus cleartext, not a decipherment or key. Saved verbatim in sources/R1889-DECODE.txt. |
| [R1890](https://de-crypt.org/decrypt-web/RecordsView/1890) | Ferdinand III to Cardinal-Infante Ferdinand, 22 February 1640; *Non-decrypted*. | [D3604](https://de-crypt.org/decrypt-custom/filesrv/?file=DOC_R1890_D3604_3604.txt), XZ, January 14, 2021. Ciphertext plus cleartext, not a decipherment or key. Saved verbatim. |

The attachment metadata swaps duration/date field labels (e.g. “DATE OF TRANSCRIPTION: 2h” and “TRANSCRIPTION TIME: January 11, 2021”); the originals are retained. Their letter and digit spacing is meaningful but imperfect. They are source transcriptions to audit, not infallible manuscript readings.

R954's recipient field erroneously mixes “Ferdinand II” with Ferdinand III's life dates. The 1635 salutation addresses a king. Do not propagate the catalog's title errors as contemporary titulature. The draft/copy relationship was already cataloged: **no discovery claim is made here**. R1887 (1634) is a separate graphical/three-letter cipher, not used in the experiment.

## Current public status

- [Cryptiana, Unsolved Historical Ciphers](https://cryptiana.web.fc2.com/code/unsolved.htm): target section still lists the 1635 and 1640 letters without solved labels. The downloaded page is byte-identical to the handoff's September 18 fetch: SHA256 `089f9dcc9eff8ad7dea4a8165499e8991dbb509854f44b1efb39b2a814b55cfc`. This is a list observation, not a global negative result.
- [Tomokiyo's discussion post](https://cryptiana.blogspot.com/2025/09/correspondence-between-emperor.html), September 20, 2025: displayed no comments.
- [Daniel Bourdeau's public index](https://dbourdeau.github.io/cyphersolver/): no matching R1889/R1890 or 1635/1640 entry found. Other Ferdinand entries concern Ferdinand the Catholic in 1511–1512 and Lucca to Ferdinand III in 1644. Page SHA256 `1d3f394ffd179990a3818f0492c0be103eec9f147eb170778b5aabd47caf5ad3`. Repository-wide audit not performed.
- Searches combining the exact dates/record IDs, correspondents, cipher/decipherment terms, and the distinctive Trier phrases found no published reading of these exact two targets. Search results about Thomas Ernst's 2017 solution concern Ferdinand III–Leopold Wilhelm correspondence, including **20 July 1640**, not the **22 February** target. [Discussion containing Ernst's own reading](https://scienceblogs.de/klausis-krypto-kolumne/2017/10/07/top-50-crypto-mystery-solved-thomas-ernst-deciphers-fredinand-iiis-encrypted-letters/).

## Scholarship and uninspected older copies

[Joseph Lefèvre, *La Secrétairerie d'État et de Guerre sous le régime espagnol (1594–1711)*, Brussels, 1934](https://academieroyale.be/academie/documents/ML8XXXVI1934LEFEVRE23014.pdf), digitized by the Académie royale de Belgique, was downloaded and text-searched. Pages 224–225 discuss letter, syllable and whole-word substitutions and print an example from **15 May 1651**. Those example assignments differ from this reconstruction. The inspected discussion is not a key or edition of the Ferdinand targets. Searches in its extracted text for the exact target dates did not locate them; this is an OCR/text-search limitation, not proof of absence from all scholarship.

The official Belgian archive inventory identifies a potentially relevant older-copy collection: **Collection des Manuscrits Divers / Handschriftenverzameling, no. 1151**, nineteenth-century copies of correspondence between Archduke Ferdinand and the Cardinal-Infante, dated 7 October 1633–19 May 1640. The Dutch catalog labels it Spanish. Thus it might concern other letters rather than these Latin targets. The finding aid does **not** establish inclusion of either exact date or readable cipher passages. [Official Dutch inventory, item 1151](https://agatha.arch.be/nl/data/ead/BE-A0510_000766_803289/); [French inventory PDF, printed p. 140](https://agatha.arch.be/data/ead/BE-A0510_000766_803290/annexes/BE-A0510_000766_803290_fre.ead.pdf).

The inventory page states that no digitized items exist for that inventory. No copies were ordered and no archive contact was made. A standard printed edition containing these exact letters was **not identified or exhaustively checked**. This leaves a substantive prior-publication/prior-reading gap. The existence of a cataloged readable draft already rules out presenting the 1635 content as an entirely unknown text.

## One targeted comparison key, rejected

After the unchanged 1640 test, [R953](https://de-crypt.org/decrypt-web/RecordsView/953), SEA inv. 1 key 17, was inspected because it is the nearby Latin-bearing key entry and its description mentions pronounceable two-/three-letter groups. Its [AP transcription, D2706](https://de-crypt.org/decrypt-custom/filesrv/?file=DOC_R953_D2706_2706.txt), dated May 9, 2020, is saved as a comparison source.

It is **not a matching alphabet**: its numerical section has `12/14=A`, `22=L`, `38=T`; R1889's aligned values are `12=i`, `22=n`, `38=u`. Its word-code table does not supply the recurring `pla/ple/pli/plo/plu` family of R1890. No R953 values or null rules were imported, and no cipher passages were repaired to fit it. Its handwritten key image was not acquired: rejection here is based on the attached transcription. This is one rejected candidate, not an exclusion of the other SEA keys.

## What is new in this workspace

An auditable alignment, frozen partial alphabet, independent-passage test, literal decoder, qualified readings/translations of both letters, an unchanged-key 1640 test, and a separately documented 60-value 1640 supplement. Correctness of those artifacts and historical novelty are separate questions. No first-solve or previously-unread claim is warranted by this audit.

## Follow-up checks after the 1640 reading

A bounded metadata check of neighboring SEA key records R937–R952 was made before the syllable breakthrough. Their catalog descriptions alone did not identify a matching key. No image-level exclusion of those keys is claimed and no values from them were used. The rejected R953 attachment remains the only key comparison actually collated at assignment level.

[Johann Christian Lünig, *Literae procerum Europae*, 1712, CAMENA transcription, part 1](https://mateo.uni-mannheim.de/cera/luenig1/bd1/Luenig_literae_procerum_1.html) was also checked through its indexed text for the distinctive target vocabulary; no matching target was identified. This is one printed collection and a bounded text search, not an exhaustive edition audit.

The probable name identification has independent contextual support: [Grotius to Willem de Groot, 21 July 1640, DBNL edition, letter 4743](https://www.dbnl.org/tekst/groo001brie11_01/groo001brie11_01_0294.php) uses *Hatzfeldius*, identified by its editors as Melchior von Hatzfeldt. A [letter from Charles Marini, 5 April 1640, no. 4586](https://www.dbnl.org/onzekinderboeken/tekst/groo001brie11_01/groo001brie11_01_0137.php) uses the variant *Hazfeld*. These are **different letters**, not plaintext witnesses for R1890. Their variation is a reason not to assign `14=tz` merely to make the modern name.

For the ambassador's possible identification, [Tibor Monostori, JANUS 8 (2019), pp. 172–198](https://dialnet.unirioja.es/descarga/articulo/6952962.pdf) discusses Castañeda's replacement in 1640 and cites the Cardinal-Infante correspondence. This supports historical plausibility, not an equation proved by the cipher. The literal title here remains *marchio Castagneti*.
