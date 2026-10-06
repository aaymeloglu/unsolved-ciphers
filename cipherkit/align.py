"""Known-plaintext alignment: derive a key from cipher units paired letter by letter with plaintext.

This is the shape of a solve that rests on a draft, a printed decipherment or an attached key
(grade C in CONVENTIONS.md). The worked example is Ferdinand 1635, where the R954 draft was
aligned to the R1889 units. Rows are the TSV the Ferdinand folder uses: columns
`id`, `cipher` (space-separated units), `plain` (one letter per unit), `evidence` (free text).
Folding of the plaintext (u/v, i/j) is the caller's job through `fold`; ciphertext is never folded.

    training = read_tsv("transcriptions/training-alignment.tsv")
    key = {s: a.plain for s, a in align_rows(training, fold=lambda s: s.replace("v", "u")).items()}
    print(holdout(read_tsv("transcriptions/heldout.tsv"), key, fold=...)["agree"])
    print(apply("10 h 8 m".split(), key))
"""

from __future__ import annotations

import csv
from collections import Counter
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path

__all__ = ["Assignment", "align_rows", "apply", "holdout", "read_tsv", "literal_crib_scan"]


def literal_crib_scan(units: Sequence[str | None], plaintext: str) -> dict:
    """Check every literal placement under a consistent glyph -> one-letter key.

    Distinct glyphs may be homophones. None is one unknown glyph position and
    imposes no equality constraint; it is NOT a null/deletion or a span of
    unknown length. Scan separate segments to avoid crossing such spans.
    No normalization is performed, even for spaces or punctuation. No word
    codes, nulls, variable expansions or transcription errors are modelled.

    Zero conflicts means a consistent local assignment exists, not that the
    crib is correct. Witness offsets are zero-based absolute token positions.
    Runtime is O(number of windows * crib length), with no optional dependencies.
    """
    units = list(units)
    if not isinstance(plaintext, str) or not plaintext:
        raise ValueError("plaintext must be a nonempty string")
    if any(t is not None and (not isinstance(t, str) or not t) for t in units):
        raise ValueError("units must be nonempty strings or None")
    windows = []
    n = len(plaintext)
    for offset in range(len(units) - n + 1):
        counts = {}
        totals = Counter()
        first = {}
        conflicts = 0
        witness = None
        for j, letter in enumerate(plaintext):
            symbol = units[offset + j]
            if symbol is None:
                continue
            bucket = counts.setdefault(symbol, Counter())
            conflicts += totals[symbol] - bucket[letter]
            if symbol not in first:
                first[symbol] = (offset + j, letter)
            elif witness is None and first[symbol][1] != letter:
                i, earlier = first[symbol]
                witness = dict(symbol=symbol, offsets=[i, offset + j], letters=[earlier, letter])
            bucket[letter] += 1
            totals[symbol] += 1
        windows.append(dict(offset=offset, conflicting_pairs=conflicts, witness=witness))
    return dict(
        model="one_glyph_one_letter", unknown="None consumes one unconstrained position",
        tokens=len(units), crib=plaintext, windows=windows,
        exact_offsets=[w["offset"] for w in windows if w["conflicting_pairs"] == 0],
    )


@dataclass
class Assignment:
    symbol: str
    plain: str
    occurrences: list[str] = field(default_factory=list)  # "A01:3" = row id, 1-based unit index
    conflicts: list[tuple[str, str]] = field(default_factory=list)  # (occurrence, other plain)


def _pairs(row: Mapping[str, str], fold: Callable[[str], str] | None) -> tuple[str, list[str], str]:
    """Row id, cipher units and (folded) plaintext, checked for one unit per letter."""
    row_id = row["id"]
    units = row["cipher"].split()
    plain = fold(row["plain"]) if fold else row["plain"]
    if len(units) != len(plain):
        raise ValueError(f"row {row_id}: {len(units)} cipher units but {len(plain)} plaintext letters")
    return row_id, units, plain


def align_rows(rows: Iterable[Mapping[str, str]], fold: Callable[[str], str] | None = None) -> dict[str, Assignment]:
    """One unit per plaintext letter (rows with len(units) != len(plain) raise ValueError naming the row id).
    Majority letter wins (ties: first seen); every disagreement is kept in `conflicts`."""
    seen: dict[str, list[tuple[str, str]]] = {}
    for row in rows:
        row_id, units, plain = _pairs(row, fold)
        for i, (symbol, letter) in enumerate(zip(units, plain), 1):
            seen.setdefault(symbol, []).append((f"{row_id}:{i}", letter))
    key: dict[str, Assignment] = {}
    for symbol, met in seen.items():
        counts = Counter(letter for _, letter in met)  # insertion-ordered, so max() breaks ties by first seen
        winner = max(counts, key=counts.__getitem__)
        key[symbol] = Assignment(
            symbol=symbol,
            plain=winner,
            occurrences=[occ for occ, _ in met],
            conflicts=[(occ, letter) for occ, letter in met if letter != winner],
        )
    return key


def apply(units: Sequence[str], key: Mapping[str, str], unknown: str = "?") -> str:
    """Read `units` through `key`; a unit the key lacks renders as `unknown`."""
    return "".join(key.get(unit, unknown) for unit in units)


def holdout(rows: Iterable[Mapping[str, str]], key: Mapping[str, str],
            fold: Callable[[str], str] | None = None) -> dict:
    """Score rows not used for the key: {'positions': n, 'agree': k, 'mismatches': [(row_id, i, unit, expected, got)]}.
    A unit the key lacks counts as a position, not an agreement; its `got` is None."""
    positions = agree = 0
    mismatches: list[tuple[str, int, str, str, str | None]] = []
    for row in rows:
        row_id, units, plain = _pairs(row, fold)
        for i, (unit, expected) in enumerate(zip(units, plain), 1):
            positions += 1
            got = key.get(unit)
            if got == expected:
                agree += 1
            else:
                mismatches.append((row_id, i, unit, expected, got))
    return {"positions": positions, "agree": agree, "mismatches": mismatches}


def read_tsv(path) -> list[dict]:
    """Rows of an alignment TSV (`id`, `cipher`, `plain`, `evidence`) as dicts, in file order."""
    with Path(path).open(encoding="utf-8", newline="") as f:
        return [dict(row) for row in csv.DictReader(f, delimiter="\t")]
