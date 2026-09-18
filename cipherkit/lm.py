"""Language models for scoring candidate plaintexts.

CharLM  order-n character model, add-alpha smoothed, log10. This is the `lp()` that was
        copy-pasted into a dozen solvers, with a cache and a stable per-window scale.
WordLM  unigram + bigram over words with a character backoff for out-of-vocabulary words.
        Homophonic solves with known word boundaries (Forster) needed this and the char
        model alone went nowhere.

Both pickle to a cache file so a target directory builds its model once.
"""
from __future__ import annotations

import collections
import math
import os
import pickle
from collections.abc import Iterable


class CharLM:
    def __init__(self, counts: collections.Counter, order: int, alpha: float = 0.5):
        self.counts = counts
        self.order = order
        self.alpha = alpha
        self.total = sum(counts.values())
        self._cache: dict[str, float] = {}
        # Score for a window that never occurs. Windows with unknown symbols get this too.
        self.floor = math.log10(alpha / (self.total + alpha))

    @classmethod
    def from_text(cls, text: str, order: int = 4, alpha: float = 0.5) -> "CharLM":
        """`text` should already be normalized. Spaces, if present, are modelled like any character."""
        counts = collections.Counter(text[i : i + order] for i in range(len(text) - order + 1))
        return cls(counts, order, alpha)

    def logp(self, gram: str) -> float:
        v = self._cache.get(gram)
        if v is None:
            v = math.log10((self.counts.get(gram, 0) + self.alpha) / (self.total + self.alpha))
            self._cache[gram] = v
        return v

    def score(self, text: str) -> float:
        n = self.order
        lp = self.logp
        return sum(lp(text[i : i + n]) for i in range(len(text) - n + 1))

    def score_words(self, words: Iterable[str], pad: str = " ") -> float:
        """Score words independently, each padded so boundaries count. Use when the model
        was built with keep_spaces=True and the cipher gives word boundaries."""
        total = 0.0
        for w in words:
            total += self.score(pad + w + pad)
        return total

    def per_window(self, text: str) -> float:
        k = len(text) - self.order + 1
        return self.score(text) / k if k > 0 else self.floor

    def save(self, path: str) -> None:
        with open(path, "wb") as f:
            pickle.dump((self.counts, self.order, self.alpha), f, protocol=4)

    @classmethod
    def load(cls, path: str) -> "CharLM":
        with open(path, "rb") as f:
            counts, order, alpha = pickle.load(f)
        return cls(counts, order, alpha)


class BackoffCharLM:
    """Character model with stupid backoff: at each position use the longest context seen at
    least `min_count` times, paying a fixed penalty per backoff step. Unlike CharLM this gives
    a sane per-character probability to words the training text never contained, so it is
    the right model for scoring an unseen word rather than a whole text."""

    def __init__(self, counts: collections.Counter, order: int, min_count: int = 3, backoff: float = 0.4):
        self.counts = counts  # every n-gram of every order 1..order
        self.order = order
        self.min_count = min_count
        self.log_backoff = math.log10(backoff)
        self.unigrams = sum(c for g, c in counts.items() if len(g) == 1)
        self.vocab = sum(1 for g in counts if len(g) == 1)
        self._cache: dict[str, float] = {}

    @classmethod
    def from_text(cls, text: str, order: int = 6, **kw) -> "BackoffCharLM":
        counts = collections.Counter()
        for n in range(1, order + 1):
            counts.update(text[i : i + n] for i in range(len(text) - n + 1))
        return cls(counts, order, **kw)

    def score(self, text: str) -> float:
        v = self._cache.get(text)
        if v is not None:
            return v
        total = 0.0
        get = self.counts.get
        for i in range(len(text)):
            lp = None
            penalty = 0.0
            for n in range(min(self.order, i + 1), 1, -1):
                ctx = text[i - n + 1 : i]
                cc = get(ctx, 0)
                if cc >= self.min_count:
                    cf = get(text[i - n + 1 : i + 1], 0)
                    if cf:
                        lp = math.log10(cf / cc) + penalty
                        break
                    penalty += self.log_backoff
            if lp is None:
                lp = math.log10((get(text[i], 0) + 1) / (self.unigrams + self.vocab + 1)) + penalty
            total += lp
        self._cache[text] = total
        return total


class WordLM:
    """Word unigram/bigram with interpolation, plus a backoff character model for unseen words."""

    def __init__(
        self,
        uni: collections.Counter,
        bi: collections.Counter,
        chars: BackoffCharLM,
        lam: float = 0.72,
        alpha: float = 0.05,
    ):
        self.uni = uni
        self.bi = bi
        self.chars = chars
        self.lam = lam
        self.alpha = alpha
        self.N = sum(uni.values())
        self.V = len(uni)
        self.ctx = collections.Counter()
        for (a, _), c in bi.items():
            self.ctx[a] += c
        self._oov: dict[str, float] = {}

    @classmethod
    def from_text(cls, text: str, char_order: int = 6, max_word: int = 24, **kw) -> "WordLM":
        """`text` should be normalized with keep_spaces=True."""
        words = [w for w in text.split() if len(w) <= max_word]
        uni = collections.Counter(words)
        bi = collections.Counter(zip(words, words[1:]))
        padded = "".join("^" + w + "$" for w in words)
        chars = BackoffCharLM.from_text(padded, order=char_order)
        return cls(uni, bi, chars, **kw)

    def logp_word(self, w: str) -> float:
        c = self.uni.get(w, 0)
        if c:
            return math.log10((c + self.alpha) / (self.N + self.alpha * self.V))
        v = self._oov.get(w)
        if v is None:
            # Unseen word: character model, then the share of mass the unigram gives to unseen words.
            v = self.chars.score("^" + w + "$") + math.log10(self.alpha / (self.N + self.alpha * self.V))
            self._oov[w] = v
        return v

    def logp_bigram(self, w1: str, w2: str) -> float:
        c12 = self.bi.get((w1, w2), 0)
        c1 = self.ctx.get(w1, 0)
        pu = 10 ** self.logp_word(w2)
        p = (self.lam * c12 / c1 if c1 else 0.0) + (1 - self.lam) * pu
        return math.log10(max(p, 1e-15))

    def score(self, words: list[str]) -> float:
        if not words:
            return 0.0
        total = self.logp_word(words[0])
        for a, b in zip(words, words[1:]):
            total += self.logp_bigram(a, b)
        return total

    def in_vocab(self, w: str) -> bool:
        return w in self.uni

    def save(self, path: str) -> None:
        with open(path, "wb") as f:
            pickle.dump(
                (self.uni, self.bi, self.chars.counts, self.chars.order, self.chars.min_count,
                 self.chars.log_backoff, self.lam, self.alpha),
                f, protocol=4,
            )

    @classmethod
    def load(cls, path: str) -> "WordLM":
        with open(path, "rb") as f:
            uni, bi, ccounts, corder, min_count, log_backoff, lam, alpha = pickle.load(f)
        return cls(uni, bi, BackoffCharLM(ccounts, corder, min_count, 10 ** log_backoff), lam, alpha)


def cached(path: str, build, loader, rebuild: bool = False):
    """Load a pickled model from `path`, or build it with `build()` and save it."""
    if not rebuild and os.path.exists(path):
        return loader(path)
    model = build()
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    model.save(path)
    return model
