"""Pronunciation/lexicon coverage and a prioritized correction queue.

Rows and words are supplied by the caller. Nothing is silently normalized,
deleted, pronounced, or corrected. Overlapping windows are counted as windows,
not independent passages or probabilities.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path


def coverage_report(
    rows: Sequence[Sequence[str]],
    lexicon: Mapping[str, Sequence[str]],
    *,
    window_size: int = 4,
    max_missing: int = 30,
) -> dict:
    """Report coverage and missing words ranked by recoverable windows.

    Each dictionary value is a sequence of pronunciation strings (or other
    usable representations). At least one nonempty variant is required. Empty
    rows are barriers: windows crossing them are not evaluable. A missing word's
    `recoverable_windows` counts windows where it is the only unknown word type;
    correcting it alone would make those windows evaluable. `blocked_windows`
    counts all windows it occurs in, once per window, excluding empty-row windows.
    """
    if not isinstance(window_size, int) or window_size < 1:
        raise ValueError('window_size must be a positive integer')
    if not isinstance(max_missing, int) or max_missing < 0:
        raise ValueError('max_missing must be a nonnegative integer')
    rows = [list(row) for row in rows]
    if any(not isinstance(w, str) or not w for row in rows for w in row):
        raise ValueError('words must be nonempty strings')
    known = set()
    for word, variants in lexicon.items():
        if isinstance(variants, str):
            raise ValueError('lexicon values must be sequences of variants, not strings')
        if any(not isinstance(v, str) for v in variants):
            raise ValueError('pronunciation variants must be strings')
        if any(variants):
            known.add(word)
    missing = Counter(w for row in rows for w in row if w not in known)
    row_missing = [{w for w in row if w not in known} for row in rows]
    blocked, recoverable = Counter(), Counter()
    windows = max(0, len(rows) - window_size + 1)
    evaluated = empty_windows = missing_windows = 0
    for start in range(windows):
        if any(not row for row in rows[start:start + window_size]):
            empty_windows += 1
            continue
        unknown = set().union(*row_missing[start:start + window_size])
        if not unknown:
            evaluated += 1
        else:
            missing_windows += 1
            blocked.update(unknown)
            if len(unknown) == 1:
                recoverable.update(unknown)
    ranked = sorted(missing, key=lambda w: (-recoverable[w], -blocked[w], -missing[w], w))
    tokens = sum(map(len, rows))
    return dict(schema_version=1, window_size=window_size, tokens=tokens,
                known_tokens=tokens - sum(missing.values()), missing_tokens=sum(missing.values()),
                token_coverage=(tokens - sum(missing.values())) / tokens if tokens else None,
                rows=len(rows), empty_rows=sum(not row for row in rows),
                evaluable_rows=sum(bool(row) and not unknown for row, unknown in zip(rows, row_missing)),
                windows=windows, evaluable_windows=evaluated,
                windows_with_empty_rows=empty_windows, windows_with_missing_words=missing_windows,
                window_coverage=evaluated / windows if windows else None,
                missing_types=len(missing), omitted_missing_types=max(0, len(missing)-max_missing),
                correction_queue=[dict(word=w, tokens=missing[w],
                                       blocked_windows=blocked[w], recoverable_windows=recoverable[w])
                                  for w in ranked[:max_missing]])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path, help='JSON with rows, lexicon, optional window_size')
    args = parser.parse_args()
    data = json.loads(args.input.read_text())
    print(json.dumps(coverage_report(**data), indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
