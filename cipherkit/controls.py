"""Matched controls. A negative result means nothing without one.

A matched control is a synthetic ciphertext of the same length, symbol count and cipher
design as the target, enciphered from a real text in the target's language. If the solver
reads the control and not the target, the target is the problem. If the solver reads
neither, the solver is.

Also here: two permutation z-scores with different nulls. `permutation_z` shuffles the
ciphertext tokens and rescores under the found key: is the order of the text informative
under this key? `permutation_z_key` keeps the text and shuffles the key's values among its
symbols: is this key better than a relabelling of the same glyphs? Report which one a number
came from; they answer different questions and are not comparable.
"""
from __future__ import annotations

import collections
import random
import statistics
from collections.abc import Callable, Mapping, Sequence


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


def spaced_control(
    plaintext: str,
    n_homophones: int = 0,
    word_signs: Mapping[str, str] | None = None,
    seed: int = 0,
    symbols: Sequence | None = None,
) -> tuple[list[str], dict]:
    """Homophonic substitution that keeps the word gaps and gives whole words their own sign,
    the design of the period keys in this repo that keep their word gaps (Moray 1568: 23
    letters, four homophones, two word-signs, word spacing).

    `plaintext` is normalized with keep_spaces=True. `word_signs` maps a whole word to the
    single symbol that replaces it (`{"the": "[THE]"}`); those words contribute no letters, so
    the letter alphabet is the letters of the remaining words. The symbol count is therefore
    `len(letters) + n_homophones + len(word_signs)`, where `letters` is taken after the
    word-sign substitution: a letter occurring only inside a signed word gets no symbol.
    `symbols` supplies the letter symbols only and must hold exactly
    `len(letters) + n_homophones` of them; the word-signs bring their own.

    Returns (tokens, key). Tokens are cipher symbols with " " kept as a token between words, so
    `parse`/`segments` see the gaps. The key maps each letter symbol to its letter and each
    word-sign symbol to its word, so decoding the tokens reproduces the plaintext.
    """
    signs = dict(word_signs or {})
    words = plaintext.split()
    letter_stream = "".join(w for w in words if w not in signs)
    alphabet = sorted(set(letter_stream))
    n_letter_symbols = len(alphabet) + n_homophones
    if symbols is None:
        symbols = list(range(n_letter_symbols))
    else:
        symbols = list(symbols)
        if len(symbols) != n_letter_symbols:
            raise ValueError(
                f"need {n_letter_symbols} letter symbols "
                f"({len(alphabet)} letters + {n_homophones} homophones), got {len(symbols)}"
            )
    clash = set(symbols) & set(signs.values())
    if clash:
        raise ValueError(f"word-sign symbols also used for letters: {sorted(map(str, clash))}")
    letter_tokens, key = homophonic_control(
        letter_stream, n_letter_symbols, seed=seed, symbols=symbols
    )
    key.update({sym: word for word, sym in signs.items()})
    it = iter(letter_tokens)
    tokens: list = []
    for i, w in enumerate(words):
        if i:
            tokens.append(" ")
        if w in signs:
            tokens.append(signs[w])
        else:
            tokens.extend(next(it) for _ in w)
    return tokens, key


def _plaintext_for_tokens(
    corpus: str, n_tokens: int, signs: Mapping[str, str], seed: int = 0
) -> str:
    """A spaced plaintext window that enciphers to exactly `n_tokens` non-space tokens under
    `signs` (a signed word is one token, every other word one token per letter). Cuts the last
    word short if a whole word would overshoot."""
    pt = sample_plaintext(corpus, n_tokens * 3 + 10, seed, keep_spaces=True)
    out, total = [], 0
    for w in pt.split():
        cost = 1 if w in signs else len(w)
        if total + cost > n_tokens:
            if w not in signs and total < n_tokens:
                out.append(w[: n_tokens - total])
                total = n_tokens
            break
        out.append(w)
        total += cost
    if total < n_tokens:
        raise ValueError(f"corpus window too short: {total} of {n_tokens} tokens")
    return " ".join(out)


def matched_control(
    corpus: str,
    target_tokens: Sequence,
    design: str = "homophonic",
    seed: int = 0,
    n_symbols: int | None = None,
    word_signs: Mapping[str, str] | None = None,
) -> tuple[list, dict, str]:
    """Control matched to `target_tokens` in length and symbol count, written in the target's
    own symbols so the same parsing and scoring code runs on both. Pass `n_symbols` to
    override the count (the control then uses integer symbols). Returns (tokens, key, plaintext).

    `design="spaced"` (word gaps kept, whole words replaced by a sign) takes `word_signs`
    and matches the target's count of non-space tokens; " " is a token on both sides and is
    not one of the symbols. The word-signs come out of the same symbol budget, so the letters
    get `n_symbols - len(word_signs)` symbols and
    `n_homophones = n_symbols - len(letters) - len(word_signs)`, clamped at 0. When the budget
    is smaller than the sampled plaintext's alphabet the control cannot be matched at all and
    `spaced_control` raises rather than return a control of the wrong shape.
    """
    target_symbols = sorted(set(target_tokens), key=str)
    if n_symbols is None or n_symbols == len(target_symbols):
        symbols = target_symbols
    else:
        symbols = list(range(n_symbols))
    if design == "spaced":
        signs = dict(word_signs or {})
        length = sum(t != " " for t in target_tokens)
        budget = len([s for s in symbols if s != " "])
        pool = [s for s in symbols if s != " " and s not in signs.values()]
        pool = pool[: max(0, budget - len(signs))]
        pt = _plaintext_for_tokens(corpus, length, signs, seed)
        n_letters = len({c for w in pt.split() if w not in signs for c in w})
        tokens, key = spaced_control(
            pt,
            n_homophones=max(0, len(pool) - n_letters),
            word_signs=signs,
            seed=seed,
            symbols=pool,
        )
        return tokens, key, pt
    pt = sample_plaintext(corpus, len(target_tokens), seed)
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


def permutation_z_key(
    score: Callable[[Mapping], float],
    key: Mapping,
    tokens: Sequence,
    n: int = 1000,
    seed: int = 0,
    fixed: Sequence | None = None,
) -> dict:
    """Score `key` against `n` keys that shuffle its plaintext values among its non-fixed
    symbols. Word-signs (any symbol whose value is longer than one character, such as
    "[the]" or a whole word) and every symbol in `fixed` keep their values. `score(m)` decodes
    `tokens` with the key under test and returns the model score; `tokens` is passed through
    so the call site reads like `permutation_z` and the null is over the same text.
    Returns observed, null mean, null sd, z, and the empirical p-value, as `permutation_z`."""
    rnd = random.Random(seed)
    held = set(fixed or ())
    free = [s for s in key if s not in held and len(str(key[s])) == 1]
    observed = score(dict(key))
    pool = [key[s] for s in free]
    null = []
    for _ in range(n):
        rnd.shuffle(pool)
        m = dict(key)
        m.update(zip(free, pool))
        null.append(score(m))
    mean = statistics.fmean(null)
    sd = statistics.pstdev(null) if n > 1 else 0.0
    z = (observed - mean) / sd if sd else float("inf")
    p = (1 + sum(v >= observed for v in null)) / (n + 1)
    return {"observed": observed, "mean": mean, "sd": sd, "z": z, "p": p, "n": n}
