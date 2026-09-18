"""Simulated annealing and hill climbing over a symbol -> value mapping.

The mapping is a plain dict. `score(mapping)` is whatever the target needs: usually
decode the ciphertext through the mapping and hand the result to a CharLM or WordLM,
minus any penalties (duplicate assignments, nulls, disagreement with a fixed crib).

bijective=True   values are a permutation of symbols (monoalphabetic); moves swap two symbols.
bijective=False  any symbol may take any value (homophonic); moves reassign one symbol,
                 with occasional swaps so two symbols can trade letters.
fixed            symbols whose value never moves (cribs, key entries already known).
"""
from __future__ import annotations

import collections
import concurrent.futures
import math
import random
from collections.abc import Callable, Sequence

Mapping = dict


def frequency_init(tokens: Sequence, corpus: str, letters: Sequence[str]) -> Mapping:
    """Starting mapping for a homophonic anneal: symbols ranked by count get letters ranked by
    corpus frequency, each letter taking a share of symbols proportional to its frequency
    (so `e` starts with several). Beats a random start by 10 to 20 points of key recovery
    on matched controls; pass the result as `init=`."""
    counts = collections.Counter(tokens)
    syms = sorted(counts, key=lambda s: (-counts[s], str(s)))
    cf = collections.Counter(corpus)
    order = sorted(letters, key=lambda c: -cf[c])
    total = sum(cf[c] for c in letters) or 1
    n = len(syms)
    quota = {c: max(1, round(n * cf[c] / total)) for c in order}
    mapping, i = {}, 0
    for c in order:
        for _ in range(quota[c]):
            if i < n:
                mapping[syms[i]] = c
                i += 1
    for s in syms[i:]:
        mapping[s] = order[0]
    return mapping


def anneal(
    symbols: Sequence,
    values: Sequence,
    score: Callable[[Mapping], float],
    *,
    fixed: Mapping | None = None,
    bijective: bool = False,
    iters: int = 20000,
    t0: float = 10.0,
    t1: float = 0.1,
    seed: int = 0,
    init: Mapping | None = None,
    swap_prob: float = 0.3,
) -> tuple[Mapping, float]:
    """Return (best_mapping, best_score). Geometric cooling from t0 to t1.

    Temperatures are in the score's units. With a log10 quadgram CharLM over a few hundred
    tokens one bad swap costs 10 to 50, and t0=10, t1=0.1 reads a 500-letter monoalphabetic
    control on every seed; t0=2 gets stuck in local optima three seeds out of four. Scale
    t0 with the ciphertext length, and run several seeds through `restarts`.
    """
    rnd = random.Random(seed)
    fixed = dict(fixed or {})
    free = [s for s in symbols if s not in fixed]
    if not free:
        m = dict(fixed)
        return m, score(m)
    if init is not None:
        cur = dict(init)
    elif bijective:
        vals = [v for v in values if v not in fixed.values()]
        rnd.shuffle(vals)
        cur = dict(zip(free, vals))
    else:
        cur = {s: rnd.choice(values) for s in free}
    cur.update(fixed)
    cur_score = score(cur)
    best, best_score = dict(cur), cur_score
    ratio = (t1 / t0) ** (1.0 / max(iters - 1, 1))
    temp = t0
    for _ in range(iters):
        a = rnd.choice(free)
        if bijective or (len(free) > 1 and rnd.random() < swap_prob):
            b = rnd.choice(free)
            if a == b:
                temp *= ratio
                continue
            old_a, old_b = cur[a], cur[b]
            cur[a], cur[b] = old_b, old_a
            undo = ((a, old_a), (b, old_b))
        else:
            old_a = cur[a]
            cur[a] = rnd.choice(values)
            if cur[a] == old_a:
                temp *= ratio
                continue
            undo = ((a, old_a),)
        new_score = score(cur)
        delta = new_score - cur_score
        if delta >= 0 or rnd.random() < math.exp(delta / temp):
            cur_score = new_score
            if cur_score > best_score:
                best, best_score = dict(cur), cur_score
        else:
            for s, v in undo:
                cur[s] = v
        temp *= ratio
    return best, best_score


def climb(
    mapping: Mapping,
    values: Sequence,
    score: Callable[[Mapping], float],
    *,
    fixed: Mapping | None = None,
    bijective: bool = False,
) -> tuple[Mapping, float]:
    """Best-improvement hill climb from `mapping` until no single move helps."""
    fixed = fixed or {}
    cur = dict(mapping)
    cur_score = score(cur)
    free = [s for s in cur if s not in fixed]
    improved = True
    while improved:
        improved = False
        best_move, best_gain = None, 0.0
        if bijective:
            for i, a in enumerate(free):
                for b in free[i + 1 :]:
                    cur[a], cur[b] = cur[b], cur[a]
                    gain = score(cur) - cur_score
                    cur[a], cur[b] = cur[b], cur[a]
                    if gain > best_gain:
                        best_move, best_gain = ("swap", a, b), gain
        else:
            for a in free:
                old = cur[a]
                for v in values:
                    if v == old:
                        continue
                    cur[a] = v
                    gain = score(cur) - cur_score
                    if gain > best_gain:
                        best_move, best_gain = ("set", a, v), gain
                cur[a] = old
        if best_move:
            improved = True
            if best_move[0] == "swap":
                _, a, b = best_move
                cur[a], cur[b] = cur[b], cur[a]
            else:
                _, a, v = best_move
                cur[a] = v
            cur_score += best_gain
    return cur, cur_score


def restarts(
    run: Callable[[int], tuple[Mapping, float]],
    seeds: Sequence[int],
    workers: int | None = None,
) -> list[tuple[int, Mapping, float]]:
    """Run `run(seed)` for each seed, in processes when workers != 1. `run` must be picklable
    (a module-level function or functools.partial of one). Returns results sorted best first."""
    if workers == 1:
        out = [(s, *run(s)) for s in seeds]
    else:
        with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as ex:
            out = [(s, *r) for s, r in zip(seeds, ex.map(run, seeds))]
    return sorted(out, key=lambda t: -t[2])
