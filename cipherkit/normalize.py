"""Text normalization so a language model and a decipherment live in the same alphabet.

Every solver in this repo used to carry its own copy of this. The rules that matter:
folds run before accent stripping (so ä -> ae, not a), and the alphabet filter runs last.
"""
from __future__ import annotations

import re
import unicodedata

LATIN = "abcdefghijklmnopqrstuvwxyz"

# Folds applied before NFKD accent stripping.
BASE_FOLDS = {"ß": "ss", "œ": "oe", "æ": "ae"}
GERMAN_FOLDS = {**BASE_FOLDS, "ä": "ae", "ö": "oe", "ü": "ue"}
# Early modern hands and printed keys usually do not distinguish i/j and u/v.
EARLY_MODERN_FOLDS = {"j": "i", "v": "u"}

_GUT_START = re.compile(r"\*\*\* ?START OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*", re.S)
_GUT_END = re.compile(r"\*\*\* ?END OF (THE|THIS) PROJECT GUTENBERG EBOOK", re.S)


def strip_accents(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c))


def normalize(
    text: str,
    *,
    alphabet: str = LATIN,
    folds: dict[str, str] | None = None,
    keep_spaces: bool = False,
    lower: bool = True,
) -> str:
    """Lowercase, apply folds, strip accents, drop everything outside `alphabet`.

    With keep_spaces=True, any run of non-alphabet characters becomes one space and
    the result is stripped, so word boundaries survive for word-level models.
    """
    if lower:
        text = text.lower()
    folds = BASE_FOLDS if folds is None else folds
    for src, dst in folds.items():
        text = text.replace(src, dst)
    text = strip_accents(text)
    allowed = set(alphabet)
    if keep_spaces:
        out = []
        in_gap = False
        for c in text:
            if c in allowed:
                out.append(c)
                in_gap = False
            elif not in_gap:
                out.append(" ")
                in_gap = True
        return "".join(out).strip()
    return "".join(c for c in text if c in allowed)


def strip_gutenberg(text: str) -> str:
    """Cut a Project Gutenberg text down to its body. Returns the input unchanged if no markers."""
    m = _GUT_START.search(text)
    start = m.end() if m else 0
    m = _GUT_END.search(text, start)
    end = m.start() if m else len(text)
    return text[start:end]
