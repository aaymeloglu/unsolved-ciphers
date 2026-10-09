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
import hashlib
import json
import re
from collections.abc import Iterable, Sequence
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


def segments(tokens: list[Token], *, gaps: Iterable[str] = ()) -> list[list[str]]:
    """Split at separators, clear text, and explicitly named illegible signs.

    Gap labels remain in the parsed source; only the scoring segments omit them.
    No gap spelling, symbol merger or punctuation stripping is implicit.
    """
    gaps = frozenset(gaps)
    out, cur = [], []
    for t in tokens:
        if t.kind == "cipher" and t.text not in gaps:
            cur.append(t.text)
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def transformation_report(source: Sequence[str], transformed: Sequence[str]) -> dict:
    """Audit a position-preserving relabelling without modifying either input.

    Records every changed position and many-to-one merger, including collisions
    with unchanged labels. Different lengths and empty labels are rejected:
    insertions/deletions need a separate alignment, not an implicit zip/truncate.
    Hashes bind the ordered labels, not the manuscript or correctness of a merger.
    """
    source, transformed = list(source), list(transformed)
    if len(source) != len(transformed):
        raise ValueError("source and transformed lengths must agree")
    if any(not isinstance(t, str) or not t for t in source + transformed):
        raise ValueError("labels must be nonempty strings")
    origins = collections.defaultdict(set)
    changes = []
    for i, (old, new) in enumerate(zip(source, transformed)):
        origins[new].add(old)
        if old != new:
            changes.append(dict(offset=i, source=old, transformed=new))

    def digest(labels):
        data = json.dumps(labels, ensure_ascii=False, separators=(",", ":"))
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    return dict(
        schema_version=1, positions=len(source), changed_positions=len(changes),
        source_types=len(set(source)), transformed_types=len(set(transformed)),
        source_sha256=digest(source), transformed_sha256=digest(transformed),
        changes=changes,
        mergers={new: sorted(old) for new, old in sorted(origins.items()) if len(old) > 1},
    )
