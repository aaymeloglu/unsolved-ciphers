# Research report: Distich dispute, solved-cipher exclusion list, AI-assisted solves

Date: 2026-09-13. Author: recent-solves agent. Scratch dir: `<scratch>/`

## Part A. Status of the Cyphral Distich dispute (as of 2026-09-13)

**Bottom line: the Fable decoding is correct against the witness Vals actually used (Maitland Club 1834 text, from the National Library of Scotland copy), and Reticuli's refutation is based on a different state of the 1653 book (British Library copy, as filmed for EEBO). I reproduced this myself; see the "Reproduction" section below.** Nobody in the historical-cryptology community (Schmeh, Pelling, Tomokiyo) has published a response either way. Public consensus is "disputed / unverified" only because nobody has done the reproduction in public yet, except one Schneier commenter.

### A.1 What I did (summary)

1. Downloaded EEBO-TCP A64608 (the transcription Reticuli used; the film is of the British Library copy) from the Text Creation Partnership GitHub mirror and ran the stated rule (position i, number = 1-based word index into Proquiritation i, take the first letter). Result: 4/32 and 2/32 hits, and exactly the same ten "letter begins no word in that section" positions Reticuli lists. Their Finding 2 is reproducible against that text.
2. Downloaded the OCR of the Maitland Club 1834 *Works of Sir Thomas Urquhart* from Internet Archive. Vals's archived post cites this as its source: "Sir Thomas Urquhart, Logopandecteision (London, 1653), in The Works of Sir Thomas Urquhart of Cromarty, Knight (Edinburgh: Maitland Club, 1834), Proquiritations, pp. 412–417; 'The Cyphral Distich,' p. 417" with a footnote "one coordinate depends on treating the Latin expression 'hinc inde' as a single unit; otherwise that position is shifted by one." Ran the same rule.

| Line | Result against 1834 text (1-based, first letter) | Hits |
|---|---|---|
| 1 | OGODUPHOLDKINGCHARLSTHESECONDAND | 32/32 |
| 2 | MAKEHIMTHESUPR**W**M**C**RULEROFTHISLAND | 30/32 |

The two line-2 misses are counting artifacts, not failures:
- Position 15 (number 20 into Proquiritation 15) lands on "word" because the 1834 OCR prints "parolbreaking" as one token where the 1653 has "Parole-breaking". Counting the hyphenated form as two words shifts the index to "every" = E.
- Position 17 (number 35 into Proquiritation 17) lands on "choice". Proquiritation 17 contains the Latin "hinc inde"; treating it as one unit (Vals's footnote) shifts the index to "English" = E.

No position is infeasible in the 1834 text (every needed letter begins at least one word in its section).

3. The two witnesses have **different Proquiritation text and ordering**, not just different pagination:
   - British Library / TCP, Proquiritation 11: "The Authors family being of the greatest antiquity in Scotland, and by an especial providence till this time preserved..." (80 words; confirmed visually from Reticuli's own endleaf-157.jpg).
   - Maitland 1834 / NLS, Proquiritation 11: "Seeing there is none considering the relations and tyes whereunto the Author by nature and duty was bound, can with any shew of reason be accounted more blameless..."
   - Maitland 1834 Proquiritation 15 = BL/TCP Proquiritation 9 ("Seeing the Author hath been still faithful to his trust, never culpable of Parole-breaking...").
   - Per-section word counts: BL/TCP 34, 40, 45, 46, 48, 58, 71, 45, 66, 76, 82, 49, 76, 66, 50, 49, 68, 58, 66, 92, 76, 98, 64, 46, 95, 48, 64, 67, 102, 49, 39, 38. Maitland 1834: 71, 65, 107, 41, 54, 69, 44, 50, 75, 40, 78, 65, 61, 79, 66, 76, 77, 63, 77, 71, 48, 80, 94, 47, 106, 68, 65, 51, 82, 121, 47, 48.
   - The BL copy ends: Proquiritations 31, 32, printer's ornament, "Parva peto" epigraph, FINIS (confirmed by viewing endleaf-162.jpg). No distich leaf.
   - Conclusion: the 1653 *Logopandecteision* exists in at least two states/issues. The distich only makes sense against the expanded one, which is what the NLS copy and the 1834 reprint carry. This needs bibliographic confirmation (ESTC/Wing variant records; NLS H.32.a.39), which I could not do after the search budget ran out.

### A.2 Provenance (Reticuli's Findings 1 and 3 are wrong)

- The 1834 Maitland Club edition, "reprinted from the original editions", digitized from the National Library of Scotland copy, prints "THE CYPHRAL DISTICH" at p. 417 immediately after Proquiritation 32, followed by the verse "Of carping Zoil and despightful Momus... For if upon this Cyphral Distich look / An honest skilful man, he'll therein finde / His own heart's wishes, and the Author's minde", then the "Parva peto" epigraph, then FINIS. [Internet Archive worksofsirthomas00mait, p. 416](https://archive.org/details/worksofsirthomas00mait/page/416). Full OCR: https://archive.org/stream/worksofsirthomas00mait/worksofsirthomas00mait_djvu.txt
- Notes and Queries, 9th series vol. 3 (1899), p. 128: query headed "CIPHER" signed "J. W., Lerwick" (John Willcock, the biographer), giving the numbers and the verse and asking for a solution. [Internet Archive s9notesqueries03londuoft, p. 128](https://archive.org/details/s9notesqueries03londuoft/page/128). So Willcock's 1899 biography is not the sole source; the 1834 reprint predates it by 65 years and itself derives from a 1653 copy.
- Schmeh's posts cite only Willcock: [Top 50 #28 (2017-06-30)](https://scienceblogs.de/klausis-krypto-kolumne/2017/06/30/the-top-50-unsolved-encrypted-messages-28-thomas-urquharts-encrypted-poems/), [Revisited (2019-07-28)](https://scienceblogs.de/klausis-krypto-kolumne/2019/07/28/revisited-thomas-urquharts-encrypted-poems/). No 2026 comments on either post.
- Transcription variant: Schmeh, Vals and Reticuli give line 2 position 24 as 33; both the 1834 edition and N&Q 1899 read 38. In the 1834 text either value yields F ("OF"), so it does not affect the result.
- Ciphertext (Schmeh/Vals reading):
  - L1: 5.3.27.38.32.14.21.8.66.8.70.39.5.9.12.18.2.3.56.5.1.7.3.2.13.19.3.25.9.3.16.6
  - L2: 25.15.13.6.11.20.5.1.2.12.1.20.20.49.20.20.35.33.4.6.8.35.5.33.5.5.18.10.3.11.32.42 (1834/N&Q: position 24 = 38)

### A.3 Who has responded

- **Vals AI:** no update, correction, or addendum on the post as of today. Author: Geby Jaff (Research @ Vals). [Vals post](https://www.vals.ai/blogs/fable-solves-cyphral-distich). X thread: [ValsAI](https://x.com/ValsAI/status/2094851406931095593), [Rayan Krishnan](https://x.com/RayanKrishnan/status/2094851287137554908). Vals says the model was asked open-endedly to find and solve an unsolved cipher and chose this one; 44 minutes, 176k tokens. Internal files (transcription.txt, SOLUTION.md, verify_octastick.py) are referenced but not published.
- **Anthropic:** nothing found.
- **Schmeh, Pelling, Tomokiyo:** nothing found on their sites. Tomokiyo's unsolved-ciphers page was updated 2026-09-06 and does not mention Urquhart. Pelling's Cipher Mysteries has no Urquhart post.
- **Schneier** posted 2026-09-09 without judging validity. [Schneier post](https://www.schneier.com/blog/archives/2026/09/claude-fable-solves-a-historical-cipher.html). Comments:
  - "foo" (Sept 9) linked the Reticuli repo.
  - "KC" (Sept 9) noted the Wikipedia paragraph is poorly sourced and that Vals cites the Maitland 1834 edition rather than the BL copy.
  - "kjfriedo" (Sept 10, 2:57/3:09/3:49 AM) is the only person who has publicly done what I did: states the Distich mechanism "is reproducible against the 1834 Proquiritation ordering", cites NLS copy H.32.a.39 as containing the distich, and reports that Glasgow Sp Coll Bi2-l.17 (1652 *Jewel*) is complete at the end with the octastich leaves. Their octastich spot-checks against the Glasgow copy reproduce Fable's unresolved "CONERTHTO" run at positions 149–157, and positions 159–161 support "THIS USURP'D AUTHORITIE", with one caveat about a line-broken word on p. 158.
- **Hacker News** (471 points, 198 comments, 2026-08-31): mostly source-hunting confusion ("GranPC": "almost sounds like this whole thing is a hallucination"); "fxwin" posted the archive.org links to N&Q 1899 and the Maitland 1834 edition; no reproduction. [HN thread](https://news.ycombinator.com/item?id=49688695)
- **Wikipedia** *Logopandecteision* has one paragraph on the claim, flagged "better source needed", citing only a Chosun Daily article. [Wikipedia](https://en.wikipedia.org/wiki/Logopandecteision)
- **Reticuli:** [FINDINGS.md](https://github.com/reticuli-labs/panel-artifacts/blob/main/distich-refutation-2026-09-01/FINDINGS.md). Folder contains replicate_distich.py, replication_report.json, proquiritations.json, vals_raw.html, endleaf-157.jpg, endleaf-162.jpg, plus OpenTimestamps/TSA files. The GitHub org has no public description; the repo (0 stars, 0 issues) is otherwise "Ainglish comprehension panel" replications. No follow-up on the distich after Sept 1. Their best convention across a 65-convention grid scored 8/64, consistent with my 6/64 on the plain rule against the same text.
- Press (no independent verification): [The Decoder](https://the-decoder.com/claude-fable-5-1-decoded-a-centuries-old-royalist-message-hidden-in-plain-sight-since-1653/), [ForkLog](https://forklog.com/en/anthropics-claude-fable-5-1-deciphers-17th-century-cryptogram/), [SecurityOnline](https://securityonline.info/claude-fable-decrypts-cyphral-distich/).

### A.4 EEBO-TCP

- A64608 = Logopandecteision 1653 (British Library copy, microfilm IA40313007-11, Early English Books 1641–1700 reel U137). [UMich TOC](https://quod.lib.umich.edu/e/eebo/A64608.0001.001?view=toc) (returns 403 to non-browser fetches; the GitHub mirror works: https://raw.githubusercontent.com/textcreationpartnership/A64608/master/A64608.xml). Contains 32 `<div type="part">` Proquiritations, epigraph, FINIS, errata. No distich.
- A95749 = The Jewel / Ekskybalauron 1652. Lacks the final quire where the octastich sits; main text and pagination (284 numbered pages) present.
- BL film on Internet Archive: [bim_early-english-books-1641-1700_logopandecteision-or-an_urquhart-sir-thomas_1653](https://archive.org/details/bim_early-english-books-1641-1700_logopandecteision-or-an_urquhart-sir-thomas_1653) (165 pages, OCR available).

### A.5 Octastich (The Jewel, 1652)

Vals's method: number k (counting through the eight lines plus the "decagram", 285 numbers) = word index into page k of the 284-page book, first letter. Claimed 231/275 exact first-occurrence hits against EEBO-TCP A95749, remaining 44 within 1–3 words for transcription reasons. Claimed plaintext begins "GREAT LORD, MANTAINE THAT REGAL FAMILIE WHEREOF KING CHARLS THE SECOND IS THE HEAD, AND..." (ottava rima, royalist prayer, London March 1652). Nine letters in line 5 (pages 149–157, "CONERTHTO") unreadable. Not independently confirmed; kjfriedo's Glasgow-copy checks are supportive but partial. Confirming needs a physical 1652 copy or the 1983 Jack & Lyall edition.

### A.6 Reproduction: exact commands and scripts

Environment: macOS, python3 stdlib only, run from the scratch dir.

```bash
cd <scratch>/

# 1. EEBO-TCP A64608 (British Library copy)
curl -sL -o A64608.xml "https://raw.githubusercontent.com/textcreationpartnership/A64608/master/A64608.xml"

# 2. Maitland Club 1834 Works (NLS copy), OCR text
curl -sL -o mait.txt "https://archive.org/stream/worksofsirthomas00mait/worksofsirthomas00mait_djvu.txt"

# 3. Notes and Queries 9th ser. vol 3 (1899), OCR text
curl -sL -o nq.txt "https://archive.org/stream/s9notesqueries03londuoft/s9notesqueries03londuoft_djvu.txt"

# 4. Reticuli bundle
for f in FINDINGS.md replication_report.json vals_raw.html endleaf-157.jpg endleaf-162.jpg; do
  curl -sL -o $f "https://raw.githubusercontent.com/reticuli-labs/panel-artifacts/main/distich-refutation-2026-09-01/$f"
done
```

Script 1: decode against EEBO-TCP A64608.

```python
import re, xml.etree.ElementTree as ET
root = ET.parse('A64608.xml').getroot()
NS = '{http://www.tei-c.org/ns/1.0}'
parts = {}
for d in root.iter(NS + 'div'):
    if d.get('type') == 'part' and (d.get('n') or '').isdigit():
        parts[int(d.get('n'))] = d          # last occurrence of each n = the Proquiritations
def text_of(el):
    s = []
    def rec(e):
        if e.tag.endswith('note'): return
        if e.tag.endswith('g') and (e.get('ref') or '').endswith('EOLhyphen'): s.append('\x00')
        if e.text: s.append(e.text)
        for c in e:
            rec(c)
            if c.tail: s.append(c.tail)
    rec(el)
    return re.sub(r'\x00\s*', '', ''.join(s))   # join end-of-line hyphenations
def words(n):
    body = [c for c in parts[n] if not c.tag.endswith('head')]
    return re.findall(r"[A-Za-z][A-Za-z'’]*", ' '.join(text_of(c) for c in body))
L1 = [5,3,27,38,32,14,21,8,66,8,70,39,5,9,12,18,2,3,56,5,1,7,3,2,13,19,3,25,9,3,16,6]
L2 = [25,15,13,6,11,20,5,1,2,12,1,20,20,49,20,20,35,33,4,6,8,35,5,33,5,5,18,10,3,11,32,42]
T1 = "OGODUPHOLDKINGCHARLSTHESECONDAND"; T2 = "MAKEHIMTHESUPREMERULEROFTHISLAND"
for L, T in ((L1, T1), (L2, T2)):
    out = ''.join(words(i)[n-1][0].upper() if n-1 < len(words(i)) else '?' for i, n in enumerate(L, 1))
    print(out, sum(a == b for a, b in zip(out, T)), '/32')
for L, T, nm in ((L1, T1, 'L1'), (L2, T2, 'L2')):
    print(nm, 'infeasible:', [(i, c) for i, c in enumerate(T, 1) if c not in {w[0].upper() for w in words(i)}])
```

Output:

```
NTMTMNDNYOHTISEABRPTTSGSNTAATVTD 4 /32
OSOTHMOSTTTBHPBTHRIPFSWTLVWTABV? 2 /32
L1 infeasible: [(2,'G'),(5,'U'),(9,'L'),(11,'K'),(31,'N')]
L2 infeasible: [(1,'M'),(3,'K'),(4,'E'),(19,'U'),(31,'N')]
```

(Identical to Reticuli's ten infeasible positions.)

Script 2: decode against the Maitland Club 1834 OCR.

```python
import re
t = open('mait.txt', encoding='utf-8', errors='ignore').read()
end = t.find('THE  CYPHRAL  DISTICH')          # OCR uses double spaces
seg = t[end-60000:end]
seg = re.sub(r'(?m)^\s*(\d)\s+(\d)\s*\.', r'\1\2.', seg)   # OCR "3 1 ." -> "31."
marks = [(int(m.group(1)), m.start(), m.end()) for m in re.finditer(r'(?m)^\s*(\d{1,2})\s*\.\s+', seg)]
parts = {}
for k, (n, s, e) in enumerate(marks):
    nxt = marks[k+1][1] if k+1 < len(marks) else len(seg)
    body = re.sub(r'(?m)^.*(PROQUIRITATIONS|LOGOPANDECTEISION).*$', '', seg[e:nxt])  # drop running heads
    body = re.sub(r'-\s*\n\s*', '', body)                                                # join hyphenated line breaks
    parts.setdefault(n, body)     # first occurrence wins: the 1..32 Proquiritations follow the 33..76 "excellences" list
W = {n: re.findall(r"[A-Za-z][A-Za-z'’]*", parts[n]) for n in range(1, 33)}
L1 = [5,3,27,38,32,14,21,8,66,8,70,39,5,9,12,18,2,3,56,5,1,7,3,2,13,19,3,25,9,3,16,6]
L2 = [25,15,13,6,11,20,5,1,2,12,1,20,20,49,20,20,35,33,4,6,8,35,5,38,5,5,18,10,3,11,32,42]  # 1834 reading, pos24=38
T1 = "OGODUPHOLDKINGCHARLSTHESECONDAND"; T2 = "MAKEHIMTHESUPREMERULEROFTHISLAND"
for L, T in ((L1, T1), (L2, T2)):
    out = ''.join(W[i][n-1][0].upper() if n-1 < len(W[i]) else '?' for i, n in enumerate(L, 1))
    print(out, sum(a == b for a, b in zip(out, T)), '/32')
for L, T, nm in ((L1, T1, 'L1'), (L2, T2, 'L2')):
    print(nm, 'infeasible:', [(i, c) for i, c in enumerate(T, 1) if c not in {w[0].upper() for w in W[i]}])
print([(i, w) for i, w in enumerate(W[15], 1)][14:24])   # pos 15 context
print([(i, w) for i, w in enumerate(W[17], 1)][29:38])   # pos 17 context
```

Output:

```
OGODUPHOLDKINGCHARLSTHESECONDAND 32 /32
MAKEHIMTHESUPRWMCRULEROFTHISLAND 30 /32
L1 infeasible: []
L2 infeasible: []
[(15,'but'),(16,'always'),(17,'true'),(18,'in'),(19,'every'),(20,'word'),(21,'and'),(22,'action'),(23,'that'),(24,'the')]
[(30,'any'),(31,'other'),(32,'company'),(33,'with'),(34,'many'),(35,'choice'),(36,'English'),(37,'gentlemen'),(38,'that')]
```

Interpretation of the two misses: section 15's OCR reads "parolbreaking" (one token) where the 1653 print reads "Parole-breaking"; count it as two and index 20 is "every" = E. Section 17 contains "hinc inde"; count it as one unit (Vals's footnote) and index 35 is "English" = E. With those two conventions line 2 is 32/32.

Caveat: `mait.txt` is uncorrected OCR. Anyone re-running this should expect the numeric-marker regex to be fragile; the parts dict must come out with keys 1..32 in order and word counts near 71, 65, 107, 41, 54, 69, 44, 50, 75, 40, 78, 65, 61, 79, 66, 76, 77, 63, 77, 71, 48, 80, 94, 47, 106, 68, 65, 51, 82, 121, 47, 48.

## Part B. Famous ciphers solved 2015–2026 (exclusion list) and what worked

| Cipher | Status | Who / when | Method, tool | Source |
|---|---|---|---|---|
| Zodiac Z340 (1969) | Solved, FBI-confirmed | David Oranchak, Sam Blake, Jarl Van Eycke, Dec 5 2020 | Homophonic substitution plus period-19 diagonal transposition in three segments; AZdecrypt (Van Eycke) hill-climbing over ~650k transposition variants generated in Mathematica | [ABC](https://www.abc.net.au/news/2020-12-12/zodiac-killer-code-cracked-by-australian-mathematician/12977342), [Wolfram blog](https://blog.wolfram.com/2021/03/24/the-solution-of-the-zodiac-killers-340-character-cipher/), [arXiv 2403.17350](https://arxiv.org/pdf/2403.17350) |
| Mary Queen of Scots letters (1578–84) | Solved (57 letters, ~50k words) | George Lasry, Norbert Biermann, Satoshi Tomokiyo, Cryptologia Feb 8 2023 | Homophonic nomenclator; CrypTool 2 hill-climbing GUI, then archival cross-referencing of plaintext copies | [Cryptologia](https://www.tandfonline.com/doi/full/10.1080/01611194.2022.2160677), [NPR](https://www.npr.org/2023/02/10/1155701113/mary-queen-of-scots-ciphers-prison-letters) |
| Dickens Tavistock letter (1859) | Solved (>60% of outlines; sense recovered) | Dickens Code project, Claire Wood (Leicester) and Hugo Bowles (Foggia); competition winner Shane Baggs, Feb 2022 | Gurney's Brachygraphy shorthand, crowdsourced transcription | [Leicester](https://le.ac.uk/news/2022/february/dickens-code-tavistock-letter), [dickenscode.org](https://dickenscode.org/decoding-the-tavistock-letter-or-dickens-and-the-dark-arts-of-victorian-media-management/) |
| Silk Dress cryptogram (1888) | Solved | Wayne Chan (U. Manitoba), Cryptologia 2023 | Identified as US Army Signal Service weather telegraph code; found the 1887 codebook | [Cryptologia](https://www.tandfonline.com/doi/abs/10.1080/01611194.2023.2223562), [CBC](https://www.cbc.ca/news/canada/manitoba/code-silk-dress-cryptogram-1.7056758), [NOAA](https://www.noaa.gov/heritage/stories/cryptogram-in-silk-dress-tells-weather-story) |
| Bellaso challenge ciphers (1555, 1564) | All solved | Tony Gaffney solved 6 of 7 from 1564 (2009) and others; remaining 1555 ones published in Cryptologia 2018 | Attacks on reciprocal alphabets and digram tables, hand plus software | [Cipher Mysteries Bellaso page](https://ciphermysteries.com/other-ciphers/bellaso-ciphers), [Cryptologia 2018](https://www.tandfonline.com/doi/abs/10.1080/01611194.2017.1422050) |
| Rohonc Codex | Claimed, not accepted | Levente Zoltán Király and Gábor Tokai, Cryptologia 2018 | Proposed as a code (not substitution cipher) for a Catholic religious text; no scholarly consensus, still on Schmeh's list at #6 | [Cryptologia](https://www.tandfonline.com/doi/abs/10.1080/01611194.2018.1449147), [Wikipedia](https://en.wikipedia.org/wiki/Rohonc_Codex) |
| Kryptos K4 (1990) | Unsolved publicly | Sept 2025: Jarett Kobek and Richard Byrne found the plaintext on scraps in Sanborn's Smithsonian archive (not released; files sealed to 2075). Nov 20 2025: Sanborn's archive sold at RR Auction for $962,500 to Paradigm. | Paradigm (June 12 2026) runs an HMAC-based verifier, $1 per guess; states "an explosion in AI-assisted attempts, none have succeeded" | [Sanborn open letter Aug 2025](https://www.elonka.com/kryptos/OpenLetterAug2025.html), [RR Auction](https://www.rrauction.com/jim-sanborn-kryptos-k4-solution-auction/), [Paradigm](https://paradigm.xyz/2026/06/kryptos), [WBUR](https://www.wbur.org/news/2025/11/24/kryptos-sculpture-cia-headquarters-decipher-boston-auction) |
| Somerton Man / Tamam Shud (1948) | Man identified as Carl "Charles" Webb (Derek Abbott and Colleen Fitzpatrick, July 2022, forensic genealogy; not officially confirmed by SA authorities). Code unsolved; Abbott suggests it may be a horse-betting list | | [Smithsonian](https://www.smithsonianmag.com/smart-news/have-scholars-finally-identified-the-mysterious-somerton-man-180980540/), [Wikipedia](https://en.wikipedia.org/wiki/Somerton_Man) |
| Ricky McCormick notes (1999) | Unsolved | FBI CRRU still lists as open (Nov 2025) | | [Wikipedia](https://en.wikipedia.org/wiki/Ricky_McCormick's_encrypted_notes) |
| Dorabella (1897) | Unsolved | Viktor Wase 2023: algorithms that solve comparable short ciphers fail on it, so unlikely a monoalphabetic substitution in English or Latin. Zackery Belanger "rose-shaped key / list of plants" proposal Mar 2025, revised Mar 2026, self-rated moderate confidence, unverified. Dan Bartlett self-published "Dorabella Cipher: Solved" book, unverified | | [Cipher Mysteries](https://ciphermysteries.com/other-ciphers/the-dorabella-cipher), [Wikipedia](https://en.wikipedia.org/wiki/Dorabella_Cipher) |
| Debosnys cryptograms (1882) | Unsolved | No developments found | | Schmeh Top 50 #3 |
| Blitz ciphers | Unsolved | Only eight page scans public | | [Cipher Mysteries](https://ciphermysteries.com/other-ciphers/blitz-ciphers) |
| Chinese gold bar ciphers (1933) | Unsolved | Chinese text translated; cryptograms undeciphered | | [IACR page](https://www.iacr.org/misc/china/), [Cipher Foundation](http://cipherfoundation.org/modern-ciphers/chinese-gold-bar-ciphers/) |
| Zodiac Z13 / Z32 | Unsolved | Alex Baber's "Marvin Merrill" claim (Dec 2025; AI-generated name candidates filtered against records) endorsed by some ex-NSA people incl. Ed Giorgio; no cryptographic proof possible at 13 characters; FBI silent | | [SF Chronicle](https://www.sfchronicle.com/bayarea/article/black-dahlia-zodiac-killings-new-theory-21259726.php), [zodiackillerciphers.com](https://zodiackillerciphers.com/) |
| Voynich | Unsolved | Naibbe cipher (Cryptologia 2025; press Jan 2026) is a plausibility model showing a die-and-cards substitution of Latin/Italian reproduces Voynichese statistics; not a decipherment. Pelling Jan 22 2026: f17r marginalia read as Occitan, not a decipherment. Dec 2025 Zenodo "morphemic nomenklator, 99.8%" package is a fringe claim. Manifold gives ~5% for a recognized decipherment by end-2026 | | [Naibbe, Cryptologia](https://www.tandfonline.com/doi/full/10.1080/01611194.2025.2566408), [Pelling](https://ciphermysteries.com/2026/01/22/finally-i-can-read-the-voynich-manuscript), [Manifold](https://manifold.markets/Quintsequence/will-a-decipherment-of-the-voynich) |
| Beale, D'Agapeyeff | Unsolved | No credible AI or human claims found 2025–26 | | [Wikipedia Beale](https://en.wikipedia.org/wiki/Beale_ciphers), [Wikipedia D'Agapeyeff](https://en.wikipedia.org/wiki/D%27Agapeyeff_cipher) |
| "1937 Spanish transposition cipher" (HN mention) | Could not identify the HN item | Probable match: Tomokiyo lists "Telegram from Switzerland, two messages 8 Jan 1937, begins BLUME SALAMANCA, index of coincidence suggests transposition but structure unclear", unsolved. The HN items I could find are older (Lasry's double transposition 2013; Ferdinand's 1500-year-old... i.e. 500-year-old code 2018) | | [Cryptiana unsolved list](http://cryptiana.web.fc2.com/code/unsolved.htm), [HN 2013](https://news.ycombinator.com/item?id=6960168) |

Also worth knowing from Tomokiyo's list (updated 2026-09-06): many archival diplomatic ciphers solved 2020–2026 by Lasry, Biermann, Köpte, Brown and others, mostly 16th–17th c. French/Spanish/Italian nomenclators, all via hill-climbing plus archival key reconstruction.

Pattern across the real solves: the break was almost never pure cryptanalysis of the ciphertext. It was identifying the system (weather code, shorthand, book-as-key, nomenclator) or finding the key or plaintext in an archive, with software (AZdecrypt, CrypTool 2, custom hill-climbers) to finish. Schmeh's Top 50 index page has not been updated since 2020 except to mark Z340 and K4-partial. [Cipherbrain Top 50](https://scienceblogs.de/klausis-krypto-kolumne/the-top-50-unsolved-encrypted-messages/)

## Part C. AI/LLM-assisted cipher solves and benchmarks, 2024–2026

### C.1 Claimed solves

- **Urquhart Cyphral Distich (Claude Fable 5.1, Vals AI, 2026-08-31).** Genuine, in my assessment (Part A). Model was given an open-ended "find and solve an unsolved cipher" task; 44 min, 176k tokens.
- **Urquhart Cyphral Octastich (same run).** Partial: 276 of 285 positions, nine letters in line 5 open; needs physical 1652 *Jewel* to confirm. Same book-as-key idea with pages instead of paragraphs.
- **Milroy Civil War telegrams (1861/62), solved 2026 by Richard Bean "with the help of Claude Opus 5."** Stager route-transposition cipher No. 7; previously unsolved encrypted telegrams to Brig. Gen. Robert H. Milroy in the Indiana State Library digital collections. Write-up first posted on Tomokiyo's Cryptiana on 2026-09-06; it does not separate what the model did from what Bean did, and leaves open historical questions (dating, which Kelley). [Cryptiana Milroy page](http://cryptiana.web.fc2.com/code/civilwar1b_milroy.htm), [Cryptiana unsolved list entry](http://cryptiana.web.fc2.com/code/unsolved.htm)
- **Zodiac Z13 (Alex Baber, Dec 2025).** AI used only to generate candidate names; not an LLM cryptanalysis. Unverifiable.

### C.2 Refuted or empty claims

- Aaron Toponce's gist "No, ChatGPT didn't solve Kryptos 4" (updated Mar 27 2026) collects ChatGPT/Claude/Grok "K4 solutions" (e.g., Thiago Avelar, Dec 2025) and shows each fails Sanborn's published cribs (EAST 22–25, NORTHEAST 26–34, BERLIN 64–69, CLOCK 70–74). [Gist](https://gist.github.com/atoponce/1cd01f40786ab21af011f0d6257fba0c)
- Paradigm (June 2026): many AI-assisted K4 submissions, none verified. [Paradigm](https://paradigm.xyz/2026/06/kryptos)
- Pelling (Jan 2026) says his inbox is "inundated with AI-generated theories" about the Voynich. [Pelling](https://ciphermysteries.com/2026/01/22/finally-i-can-read-the-voynich-manuscript)
- Analogous non-cipher cautionary case: OpenAI's Oct 2025 "GPT-5 solved 10 open Erdős problems" retraction (the model had found existing literature). [TechCrunch](https://techcrunch.com/2025/10/19/openais-embarrassing-math/)
- Content-farm items like "Zodiac Killer 2026: Did AI Just Crack the Final Z13" (gsnsp.com) name no model, no operator, no validation. Ignore.

### C.3 Academic AI in historical cryptology (tools, not famous-cipher solves)

- HistoCrypt 2026 (Amiens, June 22–24). Session "From transcription to decryption: AI in action": Oliveros Blanco et al. (joint transcription+decryption of cipher images), George Lasry ("Location Matters: Accelerating Historical Cipher Transcription with Detection-Based AI"), Lei Kang et al. ("Learning to Decipher from Pixels, a Copiale case study"). Also Richard B. Shapiro, Camille Desenclos, Cécile Pierrot, "A brief guide to the authentication of cryptanalytic claims" (information-theoretic tests for short ciphertexts; directly relevant to judging distich-length claims). [Programme](https://histocrypt.org/program/), [Proceedings](https://dspace.ut.ee/collections/70b1d875-afc3-46a7-819a-cb425b29689d)
- DESCRYPT project (ML for pencil-and-paper archival ciphers), covered by Schneier June 3 2026. [Schneier](https://www.schneier.com/blog/archives/2026/06/ai-used-to-decrypt-medieval-ciphers.html), [descrypt.org](https://descrypt.org/)
- Láng, "From Codes to Contexts: The Maturation of Historical Cryptology", History Compass 2026 (field overview). [Wiley](https://compass.onlinelibrary.wiley.com/doi/full/10.1111/hic3.70034)
- arXiv 2606.05078, "Attention-Augmented LSTMs for Automatic Homophonic Ciphertext Decipherment" (June 2026). [arXiv](https://arxiv.org/pdf/2606.05078)

### C.4 Ready-made candidate lists and benchmarks

- **Matthew D. Green, `cipher_benchmark`** (GitHub, MVP as of April 23 2026): 905 solved records across image-to-transcription, transcription-to-plaintext, and end-to-end tracks (Copiale 101, Borg 397 folios, synthetic 240, Kryptos/Feynman calibration), plus a **262-record unsolved collection** (Voynich 227, Zodiac variants, Scorpion, Kryptos K4, Beale 1/3, D'Agapeyeff, Dorabella, Taman Shud, others) with a "Track D image2hypothesis" mode. `scripts/bench.py`, Python 3.10+, no deps. No published LLM results. Repo says it is currently private-ish/rights vary per record. [GitHub](https://github.com/matthewdgreen/cipher_benchmark)
- **Tomokiyo, "Unsolved Historical Ciphers"** (updated 2026-09-06): ~89 archival items, mostly 16th–18th c. diplomatic nomenclators and 19th–20th c. telegrams, each with a note on why it is stuck (short, no key, no plaintext). Best source of tractable, un-famous targets with scans. [Cryptiana](http://cryptiana.web.fc2.com/code/unsolved.htm)
- **Schmeh Top 50** (static since 2020). [Cipherbrain](https://scienceblogs.de/klausis-krypto-kolumne/the-top-50-unsolved-encrypted-messages/). Schmeh's current site: [klausschmeh.net](https://klausschmeh.net/)
- **Codebreaking Guide unsolved-cryptograms page** (Schmeh and Dunin), which Vals's post links. [codebreaking-guide.com](https://codebreaking-guide.com/links/unsolved-cryptograms/)
- **DECODE database** (DECRYPT project): systematic collection of ciphertexts, keys and related documents; contains many unsolved items. [de-crypt.org](https://de-crypt.org/)
- **CryptanalysisBench** (arXiv 2607.18538, July 2026): 191 tasks on modern primitives, not historical ciphers; five frontier models incl. Mythos 5 break 65–86% of Tier-1 schemes. [arXiv](https://arxiv.org/abs/2607.18538)
- **Epoch AI**: no cipher benchmark; FrontierMath Open Problems is the analogous "unsolved" set for math. [Epoch benchmarks](https://epoch.ai/benchmarks)
- **Vals AI**: no cipher benchmark; the distich was a one-off open-ended task during Fable 5.1 evaluation.

## Caveats

- This session's WebSearch budget (200 calls) ran out near the end. Not done: ESTC/Wing lookup confirming the two-state 1653 issue; fetching X replies to Vals's thread; identifying the exact HN "1937 Spanish" item; checking klausschmeh.net directly for a September 2026 post.
- The 1834 reproduction runs on uncorrected OCR. The result is robust (32/32 on line 1 with zero tuning) but anyone citing it should re-run against a page image of Maitland pp. 412–417 or the NLS 1653 copy.
- Scratch files: `A64608.xml`, `mait.txt`, `nq.txt`, `FINDINGS.md`, `rep.json` (Reticuli replication_report.json), `vals_raw.html`, `endleaf-157.jpg`, `endleaf-162.jpg`, `schmeh28.html`, all in the scratch dir named at the top.
