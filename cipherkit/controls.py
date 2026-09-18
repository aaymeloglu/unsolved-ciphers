"""Matched controls. A negative result means nothing without one.

A matched control is a synthetic ciphertext of the same length, symbol count and cipher
design as the target, enciphered from a real text in the target's language. If the solver
reads the control and not the target, the target is the problem. If the solver reads
neither, the solver is.

Also here: the permutation z-score we used on Forster and Boswell (shuffle the ciphertext
tokens, rescore under the found key, see how far the real order stands from the null).
"""
from __future__ import annotations

import collections
import random
import statistics
from collections.abc import Callable, Sequence


def sample_plaintext(text: str, length: int, seed: int = 0, keep_spaces: bool = False) -> str:
    """A contiguous window of `length` letters from `text`, starting at a word boundary
    when the text has spaces. `text` should already be normalized."""
    rnd = random.Random(seed)
    if " " in text:
        starts = [i + 1 for i, c in enumerate(text) if c == " "]
        start = rnd.choice(starts[: max(1, len(starts) - 1)])
        out, n = [], 0
        for c in text[start:]:
            if n >= length:
                break
            out.append(c)
            if c != " ":
                n += 1
        s = "".join(out).strip()
        return s if keep_spaces else s.replace(" ", "")
    start = rnd.randrange(0, max(1, len(text) - length))
    return text[start : start + length]


def mono_control(
    plaintext: str, symbols: Sequence | None = None, seed: int = 0
) -> tuple[list, dict]:
    """Monoalphabetic substitution. Returns (ciphertext tokens, key symbol->letter)."""
    rnd = random.Random(seed)
    letters = sorted(set(plaintext) - {" "})
    symbols = list(symbols) if symbols is not None else list(range(len(letters)))
    if len(symbols) < len(letters):
        raise ValueError(f"need at least {len(letters)} symbols, got {len(symbols)}")
    rnd.shuffle(symbols)
    enc = dict(zip(letters, symbols))
    tokens = [enc[c] for c in plaintext if c != " "]
    return tokens, {s: c for c, s in enc.items()}


def homophonic_control(
    plaintext: str,
    n_symbols: int,
    seed: int = 0,
    symbols: Sequence | None = None,
    proportional: bool = True,
) -> tuple[list, dict]:
    """Homophonic substitution with `n_symbols` symbols. Each letter gets at least one
    symbol; extra symbols go to letters in proportion to their frequency (as real keys
    did) unless proportional=False. Returns (ciphertext tokens, key symbol->letter)."""
    rnd = random.Random(seed)
    letters = [c for c in plaintext if c != " "]
    freq = collections.Counter(letters)
    alphabet = sorted(freq)
    if n_symbols < len(alphabet):
        raise ValueError(f"need at least {len(alphabet)} symbols for {len(alphabet)} letters")
    symbols = list(symbols) if symbols is not None else list(range(n_symbols))
    if len(symbols) != n_symbols:
        raise ValueError("len(symbols) must equal n_symbols")
    rnd.shuffle(symbols)
    alloc = {c: 1 for c in alphabet}
    extra = n_symbols - len(alphabet)
    if proportional:
        total = sum(freq.values())
        # Largest-remainder apportionment of the extra symbols by letter frequency.
        quota = {c: extra * freq[c] / total for c in alphabet}
        for c in alphabet:
            alloc[c] += int(quota[c])
        left = extra - sum(int(quota[c]) for c in alphabet)
        for c in sorted(alphabet, key=lambda c: -(quota[c] - int(quota[c])))[:left]:
            alloc[c] += 1
    else:
        for c in rnd.sample(alphabet * (extra // len(alphabet) + 1), extra):
            alloc[c] += 1
    key = {}
    homophones = {}
    it = iter(symbols)
    for c in alphabet:
        homophones[c] = [next(it) for _ in range(alloc[c])]
        for s in homophones[c]:
            key[s] = c
    tokens = [rnd.choice(homophones[c]) for c in letters]
    return tokens, key


def matched_control(
    corpus: str,
    target_tokens: Sequence,
    design: str = "homophonic",
    seed: int = 0,
    n_symbols: int | None = None,
) -> tuple[list, dict, str]:
    """Control matched to `target_tokens` in length and symbol count, written in the target's
    own symbols so the same parsing and scoring code runs on both. Pass `n_symbols` to
    override the count (the control then uses integer symbols). Returns (tokens, key, plaintext)."""
    length = len(target_tokens)
    target_symbols = sorted(set(target_tokens), key=str)
    if n_symbols is None or n_symbols == len(target_symbols):
        symbols = target_symbols
    else:
        symbols = list(range(n_symbols))
    pt = sample_plaintext(corpus, length, seed)
    if design == "mono":
        tokens, key = mono_control(pt, symbols=symbols, seed=seed)
    elif design == "homophonic":
        tokens, key = homophonic_control(pt, len(symbols), seed=seed, symbols=symbols)
    else:
        raise ValueError(f"unknown design {design!r}")
    return tokens, key, pt


def key_recovery(found: dict, true: dict, weights: collections.Counter | None = None) -> float:
    """Fraction of the true key's symbols the found key gets right, weighted by token
    frequency if `weights` (symbol -> count) is given."""
    if not true:
        return 0.0
    if weights:
        tot = sum(weights.get(s, 0) for s in true)
        hit = sum(weights.get(s, 0) for s, v in true.items() if found.get(s) == v)
        return hit / tot if tot else 0.0
    return sum(found.get(s) == v for s, v in true.items()) / len(true)


def permutation_z(
    score: Callable[[Sequence], float],
    tokens: Sequence,
    n: int = 1000,
    seed: int = 0,
) -> dict:
    """Score the tokens in their real order against `n` random shufflings of the same tokens.
    `score` takes a token sequence (decode inside it with the key under test).
    Returns observed, null mean, null sd, z, and the empirical p-value."""
    rnd = random.Random(seed)
    observed = score(tokens)
    pool = list(tokens)
    null = []
    for _ in range(n):
        rnd.shuffle(pool)
        null.append(score(pool))
    mean = statistics.fmean(null)
    sd = statistics.pstdev(null) if n > 1 else 0.0
    z = (observed - mean) / sd if sd else float("inf")
    p = (1 + sum(v >= observed for v in null)) / (n + 1)
    return {"observed": observed, "mean": mean, "sd": sd, "z": z, "p": p, "n": n}
