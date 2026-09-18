"""Parsers for the ciphertext transcription formats this repo keeps producing.

groups     `c77 g72 c78 | d10 h40`      whitespace-separated symbols; `|` or `/` as a separator
mixed      `the 113 10 26 of 222 31`    numbers are cipher, words are clear (Boswell, Cocquet)
annotated  `31214=bis 69=ld 8=∅`        symbol=reading pairs (Starhemberg working files)
letters    `QKDF LSUR`                  one symbol per character, whitespace dropped

Lines starting with `#` are comments. A Token is (kind, text, reading) with kind one of
cipher, clear, sep. `reading` is only set by the annotated format.
"""
from __future__ import annotations

import collections
import re
from typing import NamedTuple


class Token(NamedTuple):
    kind: str
    text: str
    reading: str | None = None


_SEPS = {"|", "/", "‖"}


def _lines(text: str):
    for ln in text.splitlines():
        ln = ln.strip()
        if ln and not ln.startswith("#"):
            yield ln


def parse_groups(text: str) -> list[Token]:
    out = []
    for ln in _lines(text):
        for t in ln.split():
            out.append(Token("sep", t) if t in _SEPS else Token("cipher", t))
    return out


def parse_mixed(text: str, cipher: str = r"\d+", clear: str = r"[^\W\d_]+") -> list[Token]:
    pat = re.compile(f"({cipher})|({clear})|([|/])")
    out = []
    for ln in _lines(text):
        for m in pat.finditer(ln):
            if m.group(1):
                out.append(Token("cipher", m.group(1)))
            elif m.group(2):
                out.append(Token("clear", m.group(2)))
            else:
                out.append(Token("sep", m.group(3)))
    return out


def parse_annotated(text: str) -> list[Token]:
    out = []
    for ln in _lines(text):
        for t in ln.split():
            if t in _SEPS:
                out.append(Token("sep", t))
            elif "=" in t:
                sym, reading = t.split("=", 1)
                out.append(Token("cipher", sym, reading))
            else:
                out.append(Token("cipher", t))
    return out


def parse_letters(text: str) -> list[Token]:
    return [Token("cipher", c) for ln in _lines(text) for c in ln if not c.isspace()]


PARSERS = {
    "groups": parse_groups,
    "mixed": parse_mixed,
    "annotated": parse_annotated,
    "letters": parse_letters,
}


def parse(text: str, style: str = "auto") -> list[Token]:
    if style == "auto":
        body = "\n".join(_lines(text))
        if "=" in body:
            style = "annotated"
        elif re.search(r"[^\W\d_]{2,}", body) and re.search(r"\d", body):
            style = "mixed"
        elif " " in body:
            style = "groups"
        else:
            style = "letters"
    return PARSERS[style](text)


def cipher_tokens(tokens: list[Token]) -> list[str]:
    return [t.text for t in tokens if t.kind == "cipher"]


def symbol_counts(tokens: list[Token]) -> collections.Counter:
    return collections.Counter(cipher_tokens(tokens))


def segments(tokens: list[Token]) -> list[list[str]]:
    """Cipher tokens split at separators and clear text (the units a word-level solver scores)."""
    out, cur = [], []
    for t in tokens:
        if t.kind == "cipher":
            cur.append(t.text)
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out
