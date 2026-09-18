import collections

from cipherkit import homophonic_control, key_recovery, matched_control, permutation_z, sample_plaintext


def test_sample_plaintext_length_and_boundary(english_text):
    s = sample_plaintext(english_text, 100, seed=5)
    assert len(s) == 100
    with_spaces = sample_plaintext(english_text, 100, seed=5, keep_spaces=True)
    assert with_spaces.replace(" ", "") == s
    assert not with_spaces.startswith(" ")


def test_homophonic_control_shape_and_decode(english_tail):
    pt = sample_plaintext(english_tail, 300, seed=2)
    tokens, key = homophonic_control(pt, n_symbols=60, seed=2)
    assert len(tokens) == 300
    assert len(key) == 60
    assert "".join(key[t] for t in tokens) == pt
    # Frequent letters get more homophones than rare ones.
    per_letter = collections.Counter(key.values())
    assert per_letter["e"] > per_letter["z"] if "z" in per_letter else per_letter["e"] > 1


def test_matched_control_matches_target(english_text):
    target = [f"s{i}" for i in range(40)] * 5
    tokens, key, pt = matched_control(english_text, target, design="homophonic", seed=0)
    assert len(tokens) == len(target)
    assert len(set(tokens)) == len(key) == len(set(target))
    assert set(tokens) <= set(target)
    assert len(pt) == len(target)


def test_key_recovery_weighted():
    true = {"x": "a", "y": "b", "z": "c"}
    found = {"x": "a", "y": "b", "z": "q"}
    assert key_recovery(found, true) == 2 / 3
    weights = collections.Counter({"x": 10, "y": 10, "z": 80})
    assert key_recovery(found, true, weights) == 0.2


def test_permutation_z_separates_true_key(english_lm, english_tail):
    pt = sample_plaintext(english_tail.replace(" ", ""), 300, seed=7)
    tokens, key = homophonic_control(pt, n_symbols=40, seed=7)

    def score(seq):
        return english_lm.score("".join(key[t] for t in seq))

    r = permutation_z(score, tokens, n=200, seed=0)
    assert r["z"] > 5
    assert r["p"] < 0.01
