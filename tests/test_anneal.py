import string

from cipherkit import anneal, climb, frequency_init, homophonic_control, key_recovery, mono_control, restarts, sample_plaintext


def test_anneal_recovers_mono_substitution(english_lm, english_tail):
    pt = sample_plaintext(english_tail.replace(" ", ""), 500, seed=3)
    tokens, key = mono_control(pt, symbols=list(string.ascii_uppercase), seed=3)
    symbols = sorted(set(tokens))
    letters = sorted(set(pt))

    def score(m):
        return english_lm.score("".join(m[t] for t in tokens))

    # Real use: several seeds, keep the best score. One seed alone lands in a local optimum
    # about a quarter of the time at this length.
    runs = restarts(lambda seed: anneal(symbols, letters, score, bijective=True, iters=20000, seed=seed),
                    seeds=range(4), workers=1)
    _, best, _ = runs[0]
    assert key_recovery(best, key) >= 0.9


def test_fixed_symbols_never_move():
    symbols = ["a", "b", "c"]
    values = [1, 2, 3]
    best, _ = anneal(symbols, values, lambda m: -abs(m["b"] - 2), fixed={"a": 3}, iters=200, seed=1)
    assert best["a"] == 3


def test_climb_reaches_local_optimum():
    target = {"x": 1, "y": 2, "z": 3}

    def score(m):
        return sum(m[k] == v for k, v in target.items())

    best, s = climb({"x": 3, "y": 3, "z": 3}, [1, 2, 3], score)
    assert best == target and s == 3


def test_frequency_init_covers_every_symbol_and_e_gets_most(english_text, english_tail):
    pt = sample_plaintext(english_tail.replace(" ", ""), 300, seed=1)
    tokens, _ = homophonic_control(pt, n_symbols=40, seed=1)
    init = frequency_init(tokens, english_text.replace(" ", ""), sorted(set(english_text) - {" "}))
    assert set(init) == set(tokens)
    import collections
    assert collections.Counter(init.values()).most_common(1)[0][0] == "e"
    # Passing it as init is honoured: the very first state is this mapping.
    best, _ = anneal(sorted(set(tokens)), ["e"], lambda m: 0.0, iters=0, init=init)
    assert best == init
