import random

from cipherkit import CharLM, WordLM, cached, normalize


def test_charlm_prefers_english_over_shuffled(english_lm, english_tail):
    real = english_tail.replace(" ", "")[:400]
    letters = list(real)
    random.Random(1).shuffle(letters)
    shuffled = "".join(letters)
    assert english_lm.per_window(real) > english_lm.per_window(shuffled) + 1.0


def test_charlm_unknown_symbol_gets_floor(english_lm):
    assert english_lm.logp("q#zz") == english_lm.floor


def test_charlm_roundtrip(tmp_path, english_lm):
    path = tmp_path / "lm.pkl"
    english_lm.save(str(path))
    again = CharLM.load(str(path))
    assert again.score("the quick brown fox") == english_lm.score("the quick brown fox")


def test_cached_builds_once(tmp_path):
    calls = []

    def build():
        calls.append(1)
        return CharLM.from_text("abcabcabc", order=2)

    path = str(tmp_path / "m.pkl")
    a = cached(path, build, CharLM.load)
    b = cached(path, build, CharLM.load)
    assert calls == [1]
    assert a.score("abc") == b.score("abc")


def test_wordlm_bigram_and_oov(english_text):
    lm = WordLM.from_text(english_text)
    assert lm.in_vocab("the")
    assert lm.logp_bigram("of", "the") > lm.logp_bigram("the", "of")
    # An unseen but English-looking word beats an unseen junk word.
    assert lm.logp_word("sherlockian") > lm.logp_word("xqzvkp")
    # A real sentence beats its reversal.
    words = normalize("it was the best of times", keep_spaces=True).split()
    assert lm.score(words) > lm.score(words[::-1])


def test_wordlm_roundtrip(tmp_path, english_text):
    lm = WordLM.from_text(english_text[:20000])
    path = str(tmp_path / "w.pkl")
    lm.save(path)
    again = WordLM.load(path)
    assert again.score(["the", "man"]) == lm.score(["the", "man"])
