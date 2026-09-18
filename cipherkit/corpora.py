"""Period corpora, one per language we keep hitting.

Files land in corpora/<lang>/<id>.txt (gitignored), cleaned, ready for `normalize`.

    python -m cipherkit.corpora list
    python -m cipherkit.corpora fetch fr de
    python -m cipherkit.corpora fetch all
    python -m cipherkit.corpora describe fr      # words, marker shares, what got dropped

Two kinds of source. Project Gutenberg texts are clean but mostly literary and rarely
older than the 18th century. Internet Archive OCR of 19th-century documentary editions
(Xivrey's Henri IV letters, Albèri's Venetian relazioni, CODOIN, Avenel's Richelieu) is
the right period and register for a diplomatic cipher, but the OCR is noisy and the
editors' apparatus is in a modern language, so every fetched text goes through
`clean_ocr`: lines whose marker words point to another language are dropped, and so are
lines that are mostly not letters (page furniture, tables, garbage). `describe` shows what
survived. Fraktur editions (Arneth's Maria Theresia) OCR to nothing usable and are not listed.

Every id here was checked on 2026-09-18 by fetching a slice and counting marker words;
`fetch` prints the same check so a wrong id or a bad OCR shows up at once.
"""
from __future__ import annotations

import collections
import os
import re
import sys
import urllib.request
from typing import NamedTuple

from .normalize import strip_accents, strip_gutenberg


class Source(NamedTuple):
    kind: str  # "gutenberg" or "ia"
    id: str
    label: str  # author, title, and the period of the *text* (not the edition)


G, IA = "gutenberg", "ia"

RECIPES: dict[str, list[Source]] = {
    "en": [
        Source(IA, "charlesiin1646le00chariala", "Bruce, Charles I in 1646: letters to Queen Henrietta Maria (1646)"),
        Source(IA, "diarycorresponde41evel", "Evelyn, Diary and Correspondence v.4 (17th c. letters)"),
        Source(IA, "nicholaspapersc00nichgoog", "Nicholas Papers v.1 (1641-1652)"),
        Source(IA, "thenicholaspaper02camduoft", "Nicholas Papers v.2 (1653-1655)"),
        Source(G, "1661", "Doyle, Adventures of Sherlock Holmes (1892)"),
        Source(G, "98", "Dickens, A Tale of Two Cities (1859)"),
    ],
    "fr": [
        Source(IA, "recueildeslettre01henr", "Henri IV, Lettres missives t.1, ed. Xivrey (letters 1562-1584)"),
        Source(IA, "lettresinstruct00avengoog", "Richelieu, Lettres et papiers d'Etat t.1, ed. Avenel (1608-1624)"),
        Source(G, "48529", "Montaigne, Essais I (1580)"),
        Source(G, "49168", "Montaigne, Essais II (1580)"),
        Source(G, "58801", "Montaigne, Essais III (1588)"),
        Source(G, "58706", "Montaigne, Essais IV (1588)"),
        Source(G, "39220", "Brantôme, Vies des dames galantes (c. 1600)"),
        Source(G, "13846", "Descartes, Discours de la méthode (1637)"),
    ],
    "it": [
        Source(IA, "idispaccidegliam01kovauoft", "Dispacci degli ambasciatori veneti alla corte di Francia (1589)"),
        Source(IA, "relazionideglia01albgoog", "Albèri, Relazioni degli ambasciatori veneti, s.1 v.1 (16th c.)"),
        Source(G, "56498", "Machiavelli, Mandragola, Clizia, Belfagor (c. 1518)"),
    ],
    "de": [
        Source(IA, "politischecorres22freduoft", "Politische Correspondenz Friedrichs des Grossen v.22 (1763), German half"),
        Source(G, "9186", "Lessing, Nathan der Weise (1779)"),
        Source(G, "31216", "Schiller and Goethe, Briefe an A. W. Schlegel (1790s)"),
        Source(G, "2229", "Goethe, Faust I (1808)"),
        Source(G, "2403", "Goethe, Die Wahlverwandtschaften (1809)"),
    ],
    "es": [
        Source(IA, "colecciondedocum08tick", "Colección de documentos inéditos para la historia de España t.8 (16th c.)"),
        Source(G, "320", "Lazarillo de Tormes (1554)"),
        Source(G, "61022", "Hurtado de Mendoza, Guerra de Granada (1570s)"),
        Source(G, "2000", "Cervantes, Don Quijote (1605)"),
        Source(G, "61202", "Cervantes, Novelas ejemplares (1613)"),
    ],
    "la": [
        Source(IA, "franciscipetrar01fracgoog", "Petrarca, Epistolae de rebus familiaribus v.1 (14th c.)"),
        Source(IA, "epistolaephieron11nada", "Nadal, Epistolae 1546-1577 (Jesuit correspondence)"),
        Source(G, "218", "Caesar, De Bello Gallico"),
        Source(G, "23306", "Descartes, Meditationes (1641)"),
    ],
    "sco": [
        Source(IA, "diurnalofremarka00thom", "Diurnal of Remarkable Occurrents (Scots, 1513-1575)"),
        Source(IA, "worksofjohnknox01knox", "Knox, History of the Reformation, Works v.1 (Scots, 1560s)"),
    ],
    "nl": [
        Source(G, "21800", "Vondel, Complete werken I (17th c.)"),
        Source(G, "11024", "Multatuli, Max Havelaar (1860)"),
    ],
}

# Function words that separate the languages we handle. The lists are disjoint (a test
# checks this): no `la` for French because Spanish and Italian use it, no `et` or `est` for
# Latin because French does, no `die` for German because Dutch does. The Scots list is the
# spellings a modern English editor never uses.
MARKERS: dict[str, tuple[str, ...]] = {
    "fr": ("les", "vous", "nous", "pour", "dans", "avec", "mais", "cette", "sont", "aussi"),
    "it": ("che", "della", "delle", "di", "sono", "questo", "anche", "essere", "gli", "perche"),
    "de": ("und", "der", "das", "nicht", "ich", "ist", "sich", "auch", "mit", "wird"),
    "es": ("los", "las", "por", "para", "como", "muy", "sus", "pero", "tambien", "hay"),
    "la": ("quod", "ut", "cum", "sed", "esse", "atque", "enim", "quae", "autem", "etiam"),
    "en": ("the", "and", "of", "that", "with", "which", "this", "from", "have", "his"),
    "sco": ("quhilk", "thair", "ane", "thame", "quha", "quhen", "sic", "thir", "haif", "oure"),
    "nl": ("het", "een", "van", "niet", "zijn", "ook", "maar", "dat", "zij", "hebben"),
}

GUTENBERG_URL = "https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt"
IA_URL = "https://archive.org/download/{id}/{id}_djvu.txt"
DEFAULT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "corpora")

_WORD = re.compile(r"[^\W\d_]+")


def _fold(w: str) -> str:
    return strip_accents(w.lower())


def marker_counts(text: str) -> dict[str, int]:
    words = collections.Counter(_fold(w) for w in _WORD.findall(text))
    return {lang: sum(words[m] for m in ms) for lang, ms in MARKERS.items()}


def _line_lang(words: list[str], lang: str) -> tuple[str | None, int, int]:
    """(best language, its hit count, hits for `lang`) for one line. Scots counts English
    hits toward itself, since Scots prose is full of English function words too."""
    lower = [_fold(w) for w in words]
    hits = {lg: sum(w in ms for w in lower) for lg, ms in MARKERS.items() if ms}
    if lang == "sco":
        hits["sco"] += hits.pop("en", 0)
    best = max(hits, key=lambda lg: hits[lg])
    return (best if hits[best] else None), hits[best], hits[lang]


def clean_ocr(text: str, lang: str, min_letters: float = 0.6, min_hits: int = 2, long_line: int = 8) -> str:
    """Drop lines that are not `lang` prose. A line goes when (a) fewer than `min_letters`
    of its characters are letters or spaces, (b) another language wins at least `min_hits`
    marker hits, or (c) the line has `long_line` or more words, no marker of `lang` at all,
    and at least one marker of another language. Short lines without markers are kept."""
    out = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            out.append("")
            continue
        letters = sum(c.isalpha() or c == " " for c in s)
        if letters / len(s) < min_letters:
            continue
        words = _WORD.findall(s)
        best, hits, own = _line_lang(words, lang)
        if best != lang and (hits >= min_hits or (own == 0 and hits >= 1 and len(words) >= long_line)):
            continue
        out.append(s)
    return "\n".join(out)


def _download(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "cipherkit/0.1"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read().decode("utf-8", errors="replace")


def _gutenberg_title(raw: str) -> str:
    head = raw[:6000]
    t = re.search(r"^Title:\s*(.+)$", head, re.M)
    lg = re.search(r"^Language:\s*(.+)$", head, re.M)
    return f"{t.group(1).strip() if t else '?'} [{lg.group(1).strip() if lg else '?'}]"


def fetch(lang: str, dest: str = DEFAULT_DIR, force: bool = False, log=sys.stderr) -> list[str]:
    """Download and clean every source for `lang`. Prints, per file, the Gutenberg title
    line or the IA identifier, the word count kept, and the top marker languages after
    cleaning. Returns the file paths."""
    out_dir = os.path.join(dest, lang)
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for src in RECIPES[lang]:
        path = os.path.join(out_dir, f"{src.id}.txt")
        if os.path.exists(path) and not force:
            paths.append(path)
            continue
        if src.kind == G:
            raw = _download(GUTENBERG_URL.format(id=src.id))
            title = _gutenberg_title(raw)
            body = strip_gutenberg(raw)
        elif src.kind == IA:
            raw = _download(IA_URL.format(id=src.id))
            title = f"archive.org/details/{src.id}"
            body = raw
        else:
            raise ValueError(f"unknown source kind {src.kind!r}")
        cleaned = clean_ocr(body, lang)
        with open(path, "w", encoding="utf-8") as f:
            f.write(cleaned)
        print(f"{lang} {src.id:28s} {src.label[:52]:52s} -> {title}", file=log)
        print(f"   {_summary(body, cleaned)}", file=log)
        paths.append(path)
    return paths


def _summary(raw: str, cleaned: str) -> str:
    n_raw = len(_WORD.findall(raw))
    n_clean = len(_WORD.findall(cleaned))
    mc = marker_counts(cleaned)
    top = ", ".join(f"{k}={v}" for k, v in sorted(mc.items(), key=lambda kv: -kv[1])[:3])
    pct = 100 * n_clean / n_raw if n_raw else 0
    return f"kept {n_clean:,} of {n_raw:,} words ({pct:.0f}%); markers {top}"


def text(lang: str, dest: str = DEFAULT_DIR) -> str:
    """Concatenate the fetched, cleaned texts for `lang` (not yet normalized)."""
    out_dir = os.path.join(dest, lang)
    if not os.path.isdir(out_dir):
        raise FileNotFoundError(f"no corpus for {lang!r}; run: python -m cipherkit.corpora fetch {lang}")
    parts = []
    for name in sorted(os.listdir(out_dir)):
        if name.endswith(".txt"):
            with open(os.path.join(out_dir, name), encoding="utf-8") as f:
                parts.append(f.read())
    return "\n".join(parts)


def describe(lang: str, dest: str = DEFAULT_DIR, out=sys.stdout) -> None:
    out_dir = os.path.join(dest, lang)
    total = 0
    for src in RECIPES[lang]:
        path = os.path.join(out_dir, f"{src.id}.txt")
        if not os.path.exists(path):
            print(f"  {src.id:28s} (not fetched)", file=out)
            continue
        with open(path, encoding="utf-8") as f:
            t = f.read()
        n = len(_WORD.findall(t))
        total += n
        mc = marker_counts(t)
        top = ", ".join(f"{k}={v}" for k, v in sorted(mc.items(), key=lambda kv: -kv[1])[:3])
        print(f"  {src.id:28s} {n:>9,} words  {top}   {src.label[:48]}", file=out)
    print(f"  {'total':28s} {total:>9,} words", file=out)


def main(argv: list[str]) -> int:
    force = "--force" in argv
    argv = [a for a in argv if a != "--force"]
    if not argv or argv[0] == "list":
        for lang, items in RECIPES.items():
            print(lang)
            for src in items:
                print(f"  {src.kind:9s} {src.id:28s} {src.label}")
        return 0
    langs = argv[1:] or ["all"]
    if langs == ["all"]:
        langs = list(RECIPES)
    if argv[0] == "fetch":
        for lang in langs:
            fetch(lang, force=force)
        return 0
    if argv[0] == "describe":
        for lang in langs:
            print(lang)
            describe(lang)
        return 0
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
