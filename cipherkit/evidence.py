"""Reproducible rejection witnesses for fixed nonempty glyph-to-string models.

These are necessary-condition checks, not a full constraint solver. An
inconclusive result is never a compatible key or an exclusion. None denotes an
unknown plaintext row; every character of a string, including '#', is literal.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections import Counter
from collections.abc import Sequence
from pathlib import Path

MODEL = 'fixed_nonempty_strings'


def _inputs(rows, plaintext):
    rows = [list(row) for row in rows]
    plaintext = list(plaintext)
    if len(rows) != len(plaintext):
        raise ValueError('cipher and plaintext row counts must agree')
    if any(not isinstance(g, str) or not g for row in rows for g in row):
        raise ValueError('glyph identifiers must be nonempty strings')
    if any(v is not None and not isinstance(v, str) for v in plaintext):
        raise ValueError('plaintext rows must be strings or None')
    return dict(cipher_rows=rows, plaintext_rows=plaintext)


def _digest(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=False,
                                    separators=(',', ':')).encode()).hexdigest()


def _fits(row, text, glyph, value):
    """Producer: dynamic programming over reachable plaintext offsets."""
    positions = {0}
    for g in row:
        if not positions:
            return False
        if g == glyph:
            positions = {p + len(value) for p in positions if text.startswith(value, p)}
        else:
            positions = set(range(min(positions) + 1, len(text) + 1))
    return len(text) in positions


def _fits_blocks(row, text, glyph, value):
    """Verifier: greedily place fixed blocks separated by minimum-length gaps.

    Consecutive fixed glyphs form one block. An earlier placement leaves at
    least as much room for every subsequent block; a final block without a
    trailing gap must be anchored at the end. Does not use the producer's DP.
    """
    blocks = []
    gap = 0
    i = 0
    while i < len(row):
        if row[i] != glyph:
            gap += 1
            i += 1
            continue
        j = i
        while j < len(row) and row[j] == glyph:
            j += 1
        blocks.append((gap, value * (j - i)))
        gap = 0
        i = j
    pos = 0
    for index, (before, block) in enumerate(blocks):
        if index == len(blocks) - 1 and gap == 0:
            start = len(text) - len(block)
            if start < pos + before or (before == 0 and start != pos):
                return False
            if not text.startswith(block, start):
                return False
        elif before == 0:
            start = pos
            if not text.startswith(block, start):
                return False
        else:
            start = text.find(block, pos + before)
            if start < 0:
                return False
        pos = start + len(block)
    return len(text) - pos >= gap if gap else len(text) == pos


def rejection_record(
    cipher_rows: Sequence[Sequence[str]],
    plaintext_rows: Sequence[str | None],
    *,
    max_candidates: int = 100_000,
    timeout: float = 10.0,
) -> dict:
    """Return a JSON-safe input-bound rejection or an explicit inconclusive record.

    Tests row lengths, then asks whether each repeated glyph individually has
    any constant nonempty value compatible with all known rows. Other glyphs
    are free nonempty gaps, even across repeated occurrences. A contradiction
    in this relaxed model excludes the full model. No contradiction proves
    nothing. Enumeration exhaustion and missing data are explicitly labeled.
    """
    import math

    if not isinstance(max_candidates, int) or max_candidates < 0:
        raise ValueError('max_candidates must be a nonnegative integer')
    if not math.isfinite(timeout) or timeout < 0:
        raise ValueError('timeout must be finite and nonnegative')
    data = _inputs(cipher_rows, plaintext_rows)
    record = dict(schema_version=1, model=MODEL, inputs=data, input_sha256=_digest(data))
    known = [(i, r, v) for i, (r, v) in enumerate(zip(data['cipher_rows'], data['plaintext_rows']))
             if v is not None]
    for i, row, text in known:
        if len(row) > len(text) or (not row and text):
            return dict(record, status='rejected', witness=dict(kind='row_length', row=i))
    if not known:
        return dict(record, status='inconclusive', reason='no_known_rows')
    freq = Counter(g for _, row, _ in known for g in row)
    deadline = time.monotonic() + timeout
    tested = 0
    for glyph in sorted(g for g in freq if freq[g] > 1):
        affected = [(r, v) for _, r, v in known if glyph in r]
        text = min((v for _, v in affected), key=len)
        # Every assignment must be a substring of each affected row. Test all
        # distinct substrings of the shortest row until one works or a limit hits.
        seen = set()
        found = False
        for start in range(len(text)):
            for end in range(start + 1, len(text) + 1):
                if time.monotonic() >= deadline:
                    return dict(record, status='inconclusive', reason='timeout', tested_candidates=tested)
                value = text[start:end]
                if value in seen:
                    continue
                if tested >= max_candidates:
                    return dict(record, status='inconclusive', reason='candidate_limit', tested_candidates=tested)
                seen.add(value)
                tested += 1
                if all(_fits(r, v, glyph, value) for r, v in affected):
                    found = True
                    break
            if found:
                break
        if not found:
            return dict(record, status='rejected', witness=dict(kind='empty_glyph_domain', glyph=glyph))
    return dict(record, status='inconclusive', reason='no_contradiction', tested_candidates=tested)


def verify_rejection(record: dict) -> bool:
    """Independently verify a saved witness against the embedded input and hash.

    Returns False for malformed, altered, unsupported or inconclusive records.
    A hash binds the evidence to its input; it does not authenticate the source.
    """
    try:
        if (record['schema_version'] != 1 or record['model'] != MODEL
                or record['status'] != 'rejected'):
            return False
        data = _inputs(
            record['inputs']['cipher_rows'], record['inputs']['plaintext_rows'])
        if _digest(data) != record['input_sha256']:
            return False
        rows, plains = data['cipher_rows'], data['plaintext_rows']
        witness = record['witness']
        if witness['kind'] == 'row_length':
            i = witness['row']
            if not isinstance(i, int) or not 0 <= i < len(rows) or plains[i] is None:
                return False
            return bool(len(rows[i]) > len(plains[i]) or (not rows[i] and plains[i]))
        if witness['kind'] != 'empty_glyph_domain':
            return False
        glyph = witness['glyph']
        affected = [(r, v) for r, v in zip(rows, plains) if v is not None and glyph in r]
        if sum(r.count(glyph) for r, _ in affected) < 2:
            return False
        # Independent enumeration by length (the producer enumerates by start).
        text = min((v for _, v in affected), key=len)
        for length in range(1, len(text) + 1):
            for start in range(len(text) - length + 1):
                value = text[start:start + length]
                if all(_fits_blocks(r, v, glyph, value) for r, v in affected):
                    return False
        return True
    except (KeyError, TypeError, ValueError):
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('records', type=Path, help='JSONL rejection records')
    args = parser.parse_args()
    checked = 0
    for line in args.records.read_text().splitlines():
        if not line.strip():
            continue
        try:
            valid = verify_rejection(json.loads(line))
        except json.JSONDecodeError:
            valid = False
        if not valid:
            parser.exit(1, f'Unverified record {checked + 1}\n')
        checked += 1
    if not checked:
        parser.exit(1, 'No records supplied\n')
    print(json.dumps(dict(verified_rejections=checked)))


if __name__ == '__main__':
    main()
