# Burgess, The Master of Mysteries (1912): third hidden message, first crack (2026-09-13)

Source: Wikisource page-level transcription of the 1912 Bobbs-Merrill first edition
("Index:The Master of Mysteries (1912).djvu", 552 djvu pages, all fetched to wspages/pages.json).
Parsed into 24 stories with pages, paragraphs, sentences, italics (mom_parse.py).

## Verified
- First letter of first word of each story: THE AUTHOR IS GELETT BURGESS
- Last letter of last word of each story: FALSE TO LIFE AND FALSE TO ART
Both known long before 2021 (Ramble House edition; Lillian de la Torre letter, pre-1993: "still chewing over the third cipher (if any)").

## Status check for a published third-message solve (none found)
Schmeh 2021 post + comments, klausschmeh.net, Cipher Mysteries, Codebreaking Guide unsolved list,
Ramble House pages, Black Chamber blog Dec 2021, Brave/Bing/Marginalia/HN Algolia/GitHub. Unchecked:
Klinger's 2023 LOC Crime Classics edition notes (no preview online; not on IA), ACA Facebook/The Cryptogram.

## Tested and negative (scorer = quadgram model built from the book, `cipherkit.CharLM` since 18 Sept 2026; the two known messages still rank #1 and #2)
- Per-story, 24 units: first/last letter of word k and word -k (k=1..12); sentence k / -k (1..8);
  paragraph k / -k (1..8); page k / -k (1..8); letter k / -k of story (1..20); middle letter/word;
  title letters/words; first/last italic; first quoted speech; word/para/page counts as letters;
  first-word length as index. All also reversed.
- Diagonal acrostics: unit k of story k (words, letters, sentences, paragraphs, from start and end, offsets 0..3).
- Contents page numbers (1,23,44,...,465) as word/letter/paragraph/sentence indices into each story and into the book.
- Every n-th word (50..1000) and every n-th letter (500..5000) of the whole book.
- Book-wide: first/last letters of every page, every paragraph (per story), every sentence (per story), every italic span.
- OCR line-initial and line-final letters over the whole Cornell scan (15.5k lines): no words > 7 letters.
- 25 plate captions: first letters / last letters.
- Introduction: paragraph first/last words.

## Untested ideas
- Baconian biliteral or Donnelly-style word counts (the Introduction opens on Donnelly's Great Cryptogram; story 2 is about a Shakespeare folio). Needs page images and a hypothesis for the counting rule.
- In-story cipher rules reused on the frame: the Lorsson Elopement Bible chapter:verse code; Dalrymple phonetic French.
- Word-level acrostics (first words of paragraphs forming a sentence) not scored automatically; only letter-level scanned.
- Reading a different unit: lines on the printed page (Wikisource drops line breaks; OCR line breaks used instead but OCR is noisy).
- Possibility there is no third message: the Introduction says only "Possibly".
