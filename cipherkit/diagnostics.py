"""Known-key scoring diagnostics, independent of the search optimizer."""
from __future__ import annotations

import math
from collections import Counter
from collections.abc import Callable, Mapping, Sequence


def perturbation_report(
    tokens: Sequence[str],
    true_key: Mapping[str, str],
    values: Sequence[str],
    score: Callable[[dict[str, str]], float],
    *,
    singletons_only: bool = False,
    tolerance: float = 1e-9,
    max_examples: int = 10,
) -> dict:
    """Score every single-symbol reassignment from a supplied correct key.

    Higher scores must mean better text. This is a homophonic diagnostic: a
    reassignment need not preserve a bijection. Tokens have no implicit gaps;
    the caller's score function handles boundaries and normalization. The key
    and values must contain nonempty strings. Extra key entries are left fixed.

    No optimization, corpus training, or holdout selection occurs here. A false
    alternative outscoring the truth establishes a local preference, not failure
    to recover substantial text. A local optimum does not establish uniqueness
    or cold-start recovery. With no tested alternatives its value is None.
    """
    tokens = list(tokens)
    key = dict(true_key)
    values = list(dict.fromkeys(values))
    if not tokens or any(not isinstance(t, str) or not t for t in tokens):
        raise ValueError('tokens must contain nonempty symbol strings')
    if not values or any(not isinstance(v, str) or not v for v in values):
        raise ValueError('values must contain nonempty strings')
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError('tolerance must be finite and nonnegative')
    if not isinstance(max_examples, int) or max_examples < 0:
        raise ValueError('max_examples must be a nonnegative integer')
    freq = Counter(tokens)
    if any(g not in key or key[g] not in values for g in freq):
        raise ValueError('every observed symbol needs a true value in the domain')

    def checked(mapping):
        value = float(score(dict(mapping)))
        if not math.isfinite(value):
            raise ValueError('score must return finite numbers')
        return value

    baseline = checked(key)
    symbols = sorted(g for g, n in freq.items() if not singletons_only or n == 1)
    totals = Counter(tested=0, improving=0, tied=0, worse=0)
    improved = set()
    examples = []
    by_frequency = {}
    for glyph in symbols:
        bucket = by_frequency.setdefault(str(freq[glyph]), dict(tested=0, improving=0, tied=0, worse=0))
        for value in values:
            if value == key[glyph]:
                continue
            trial = dict(key)
            trial[glyph] = value
            alternative = checked(trial)
            delta = alternative - baseline
            outcome = 'improving' if delta > tolerance else 'worse' if delta < -tolerance else 'tied'
            totals['tested'] += 1
            totals[outcome] += 1
            bucket['tested'] += 1
            bucket[outcome] += 1
            if outcome == 'improving':
                improved.add(glyph)
                if max_examples:
                    examples.append(dict(symbol=glyph, old=key[glyph], new=value,
                                         occurrences=freq[glyph], score=alternative, delta=delta))
                    examples.sort(key=lambda x: (-x['delta'], x['symbol'], x['new']))
                    del examples[max_examples:]
    return dict(schema_version=1, method='single_symbol_reassignment',
                baseline_score=baseline, tokens=len(tokens), symbols=len(freq),
                tested_symbols=len(symbols), singletons_only=singletons_only,
                tolerance=tolerance, **totals, improving_symbols=len(improved),
                local_optimum=(totals['improving'] == 0) if totals['tested'] else None,
                by_frequency=by_frequency, examples=examples)
