import random

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
    # A word below min_count is unseen: its score carries the oov penalty.
    assert seg.word_logp("zzzzq") < -6.0


def test_rare_words_are_not_in_lexicon():
    seg = Segmenter("aa bb bb cc cc cc", order=2, min_count=2)
    assert set(seg.words) == {"bb", "cc"}
    assert seg.words["cc"] > seg.words["bb"]
