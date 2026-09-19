"""Dictionary-segmentation scorer for ciphers whose plaintext has word boundaries.

A character model alone reads about half of a homophonic key (see README, "What the control
numbers look like"). Forster 1644 and Moray 1568 were carried instead by scoring each
gap-delimited chunk of letters as the best split into words of a period corpus. `Segmenter`
is that scorer, written once. Its arithmetic is the Moray campaign's `Scorer`
(moray-1568/solver.py, 18 September 2026):

- a word seen at least `min_count` times in the corpus scores log10(count / total words);
- any other string scores `oov` plus an add-0.5 order-n character model over its windows,
  built on the corpus letters with spaces removed;
- a chunk scores the best sum over splits into pieces of at most `max_word` letters.

Scores are log10 probabilities, so a chunk of real prose scores tens of units above the same
letters shuffled (`test_real_split_beats_shuffled`), which is the margin an annealer needs.
"""
from __future__ import annotations

import collections
import math
import re

_WORD = re.compile(r"[a-z]+")


class Segmenter:
    """Best-segmentation scorer: a letter string is scored by the best split into corpus words
    (word unigram log10 probabilities; unseen words fall back to an order-n character model plus
    `oov` penalty). Equivalent to moray-1568/solver.py Scorer (18 Sept 2026)."""

    def __init__(self, text: str, order: int = 4, oov: float = -6.0, min_count: int = 2, max_word: int = 14):
        """`text` is a corpus, ideally already `normalize`d with keep_spaces=True; any run of
        characters outside a-z is a word boundary either way. `oov` is the log10 penalty an
        unseen word pays on top of its character-model score (-6 means a hundred thousand
        times less likely than a word that fills the whole lexicon). `max_word` bounds the
        split length the DP considers."""
        words = _WORD.findall(text.lower())
        counts = collections.Counter(words)
        total = sum(counts.values())
        self.words: dict[str, float] = {
            w: math.log10(c / total) for w, c in counts.items() if c >= min_count
        }
        letters = "".join(words)
        self.order = order
        self.grams = collections.Counter(letters[i : i + order] for i in range(len(letters) - order + 1))
        self.gram_total = sum(self.grams.values())
        self.oov = oov
        self.max_word = max_word
        self.alphabet = frozenset(letters)
        self._gram_cache: dict[str, float] = {}
        self._score_cache: dict[str, float] = {}

    @classmethod
    def from_corpus(cls, lang: str, **kw) -> "Segmenter":
        """Build from `cipherkit.corpora.text(lang)`, normalized with keep_spaces=True."""
        from .corpora import text
        from .normalize import normalize

        return cls(normalize(text(lang), keep_spaces=True), **kw)

    def gram_logp(self, gram: str) -> float:
        """log10 of the add-0.5 estimate of one character window."""
        v = self._gram_cache.get(gram)
        if v is None:
            v = math.log10((self.grams.get(gram, 0) + 0.5) / self.gram_total)
            self._gram_cache[gram] = v
        return v

    def word_logp(self, w: str) -> float:
        """log10 probability of one word: the lexicon entry, or `oov` plus the character model."""
        v = self.words.get(w)
        if v is not None:
            return v
        n = self.order
        return self.oov + sum(self.gram_logp(w[i : i + n]) for i in range(len(w) - n + 1))

    def _table(self, s: str) -> tuple[list[float], list[int]]:
        n = len(s)
        best = [-1e9] * (n + 1)
        back = [0] * (n + 1)
        best[0] = 0.0
        for i in range(1, n + 1):
            for j in range(max(0, i - self.max_word), i):
                if best[j] < -1e8:
                    continue
                v = best[j] + self.word_logp(s[j:i])
                if v > best[i]:
                    best[i] = v
                    back[i] = j
        return best, back

    def score(self, s: str) -> float:
        """Score of the best segmentation of `s` (log10; 0.0 for the empty string). Cached."""
        v = self._score_cache.get(s)
        if v is None:
            v = self._table(s)[0][len(s)]
            self._score_cache[s] = v
        return v

    def segment(self, s: str) -> list[str]:
        """The words of the best segmentation of `s`."""
        _, back = self._table(s)
        out, i = [], len(s)
        while i > 0:
            out.append(s[back[i] : i])
            i = back[i]
        out.reverse()
        return out

    def score_chunks(self, chunks: list[str]) -> float:
        """Sum of `score` over the pieces of each chunk. Any character outside the model's
        alphabet (a word-sign such as "#", an unread "?") ends a piece, so "the#lord" scores as
        "the" plus "lord"; empty pieces score nothing."""
        total = 0.0
        alphabet = self.alphabet
        for chunk in chunks:
            piece = []
            for c in chunk:
                if c in alphabet:
                    piece.append(c)
                elif piece:
                    total += self.score("".join(piece))
                    piece = []
            if piece:
                total += self.score("".join(piece))
        return total
