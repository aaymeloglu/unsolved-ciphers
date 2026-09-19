import math
import random

import pytest

from cipherkit import Segmenter


def _train(english_text: str) -> Segmenter:
    return Segmenter(english_text[: int(len(english_text) * 0.8)])


def test_segment_recovers_words(english_text):
    seg = _train(english_text)
    assert seg.segment("thekingandthehouse") == ["the", "king", "and", "the", "house"]


def test_real_split_beats_shuffled(english_text, english_tail):
    seg = _train(english_text)
    words = english_tail.split()[:40]
    real = "".join(words)
    rnd = random.Random(0)
    letters = list(real)
    rnd.shuffle(letters)
    assert seg.score(real) > seg.score("".join(letters)) + 20


def test_score_chunks_breaks_on_word_signs(english_text):
    seg = Segmenter(english_text)
    assert seg.score_chunks(["the#lord"]) == seg.score("the") + seg.score("lord")


def test_score_chunks_sums_chunks_and_skips_empty(english_text):
    seg = Segmenter(english_text)
    assert seg.score_chunks(["#the", "king#", ""]) == seg.score("the") + seg.score("king")


def test_word_logp_unseen_falls_back_to_char_model(english_text):
    seg = Segmenter(english_text, oov=-6.0)
    assert seg.word_logp("the") > seg.word_logp("thq")
    # A word absent from the corpus is scored by the character model plus the oov penalty.
    assert seg.word_logp("zzzzq") < -6.0


def test_rare_words_are_not_in_lexicon():
    seg = Segmenter("aa bb bb cc cc cc", order=2, min_count=2)
    assert set(seg.words) == {"bb", "cc"}
    assert seg.words["cc"] > seg.words["bb"]


def test_arithmetic_matches_moray_scorer():
    # Hand-computed on a tiny corpus: words aa x1, bb x2, cc x3 (6 in all); the letters
    # "aabbbbcccccc" give 11 bigrams (bb x3, cc x5, aa/ab/bc x1). This pins the add-0.5
    # gram estimate and the oov fallback of moray-1568/solver.py's Scorer (18 Sept 2026).
    seg = Segmenter("aa bb bb cc cc cc", order=2, min_count=2, oov=-6.0)
    assert seg.word_logp("bb") == pytest.approx(math.log10(2 / 6))
    assert seg.word_logp("cc") == pytest.approx(math.log10(3 / 6))
    assert seg.gram_logp("bb") == pytest.approx(math.log10(3.5 / 11))
    assert seg.word_logp("ab") == pytest.approx(-6.0 + math.log10(1.5 / 11))
    assert seg.word_logp("aa") == pytest.approx(-6.0 + math.log10(1.5 / 11))
    assert seg.score("bbcc") == pytest.approx(math.log10(2 / 6) + math.log10(3 / 6))
    assert seg.segment("bbcc") == ["bb", "cc"]
