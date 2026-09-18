"""Period corpora, one per language we keep hitting, fetched from Project Gutenberg.

Files land in corpora/<lang>/<id>.txt (gitignored) with the Gutenberg header and footer
already removed. Rebuild any time with `python -m cipherkit.corpora fetch <lang>`.

    python -m cipherkit.corpora list
    python -m cipherkit.corpora fetch fr de
    python -m cipherkit.corpora fetch all

The texts are chosen for period where Gutenberg has one, not for size: a 16th-century French
letter should be scored by Montaigne and Brantôme, not by Zola. Italian and Dutch are the
weakest fits (Manzoni and Multatuli are 19th century). Add an entry when a target needs a
closer match, and say in the target's README which corpus its model used. Every id was
checked against the Gutenberg title and language line on 2026-09-18; `fetch` prints both
so a wrong id shows up immediately.
"""
from __future__ import annotations

import os
import re
import sys
import urllib.request

from .normalize import strip_gutenberg

RECIPES: dict[str, list[tuple[int, str]]] = {
    "en": [
        (1661, "Doyle, Adventures of Sherlock Holmes"),
        (98, "Dickens, A Tale of Two Cities"),
    ],
    "fr": [
        (48529, "Montaigne, Essais I"),
        (49168, "Montaigne, Essais II"),
        (58801, "Montaigne, Essais III"),
        (58706, "Montaigne, Essais IV"),
        (39220, "Brantôme, Vies des dames galantes"),
        (13846, "Descartes, Discours de la méthode"),
    ],
    "de": [
        (9186, "Lessing, Nathan der Weise"),
        (2229, "Goethe, Faust I"),
        (2403, "Goethe, Die Wahlverwandtschaften"),
        (31216, "Schiller and Goethe, Briefe an A. W. Schlegel"),
    ],
    "it": [
        (56498, "Machiavelli, La mandragola, La Clizia, Belfagor"),
        (45334, "Manzoni, I promessi sposi"),
    ],
    "es": [
        (2000, "Cervantes, Don Quijote"),
        (320, "Lazarillo de Tormes"),
        (61202, "Cervantes, Novelas ejemplares"),
        (61022, "Hurtado de Mendoza, Guerra de Granada"),
    ],
    "la": [
        # Gutenberg's Cicero (47001) and Sallust (7402) are mostly English commentary; skipped.
        (218, "Caesar, De Bello Gallico"),
        (23306, "Descartes, Meditationes"),
    ],
    "nl": [
        (21800, "Vondel, Complete werken I"),
        (11024, "Multatuli, Max Havelaar"),
    ],
}

URL = "https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt"
DEFAULT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "corpora")


def _title_lang(raw: str) -> tuple[str, str]:
    head = raw[:6000]
    t = re.search(r"^Title:\s*(.+)$", head, re.M)
    lang = re.search(r"^Language:\s*(.+)$", head, re.M)
    return (t.group(1).strip() if t else "?", lang.group(1).strip() if lang else "?")


def fetch(lang: str, dest: str = DEFAULT_DIR, force: bool = False) -> list[str]:
    """Download every text in RECIPES[lang]. Prints each Gutenberg title and language so a
    wrong id is visible. Returns the file paths."""
    out_dir = os.path.join(dest, lang)
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for gid, label in RECIPES[lang]:
        path = os.path.join(out_dir, f"{gid}.txt")
        if os.path.exists(path) and not force:
            paths.append(path)
            continue
        req = urllib.request.Request(URL.format(id=gid), headers={"User-Agent": "cipherkit/0.1"})
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read().decode("utf-8", errors="replace")
        title, language = _title_lang(raw)
        print(f"{lang} {gid:>6}  {label:40s}  -> {title} [{language}]", file=sys.stderr)
        with open(path, "w", encoding="utf-8") as f:
            f.write(strip_gutenberg(raw))
        paths.append(path)
    return paths


def text(lang: str, dest: str = DEFAULT_DIR) -> str:
    """Concatenate the fetched texts for `lang` (raw, not normalized)."""
    out_dir = os.path.join(dest, lang)
    if not os.path.isdir(out_dir):
        raise FileNotFoundError(f"no corpus for {lang!r}; run: python -m cipherkit.corpora fetch {lang}")
    parts = []
    for name in sorted(os.listdir(out_dir)):
        if name.endswith(".txt"):
            with open(os.path.join(out_dir, name), encoding="utf-8") as f:
                parts.append(f.read())
    return "\n".join(parts)


def main(argv: list[str]) -> int:
    if not argv or argv[0] == "list":
        for lang, items in RECIPES.items():
            print(lang)
            for gid, label in items:
                print(f"  {gid:>6}  {label}")
        return 0
    if argv[0] == "fetch":
        force = "--force" in argv
        langs = [a for a in argv[1:] if a != "--force"] or ["all"]
        if langs == ["all"]:
            langs = list(RECIPES)
        for lang in langs:
            fetch(lang, force=force)
        return 0
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
