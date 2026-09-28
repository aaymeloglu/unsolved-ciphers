import math

import pytest

from cipherkit.diagnostics import perturbation_report


def test_report_detects_wrong_preference_and_preserves_key():
    tokens = ['x', 'y', 'x']
    key = {'x': 'a', 'y': 'b'}
    seen = []

    def score(m):
        seen.append(dict(m))
        return ''.join(m[t] for t in tokens).count('a')

    r = perturbation_report(tokens, key, ['a', 'b', 'b'], score)
    assert key == {'x': 'a', 'y': 'b'}
    assert r['tested'] == 2
    assert r['improving'] == 1 and r['worse'] == 1
    assert r['local_optimum'] is False
    assert r['examples'][0]['symbol'] == 'y'
    assert r['by_frequency']['1']['improving'] == 1
    assert len(seen) == 3


def test_repeated_symbol_changes_every_occurrence():
    r = perturbation_report(['a', 'a', 'b'], {'a': 'x', 'b': 'y'}, 'xyz',
                            lambda m: 2 * (m['a'] == 'z') + (m['b'] == 'z'))
    assert r['tested'] == 4 and r['improving'] == 2
    assert r['examples'][0]['occurrences'] == 2
    assert r['examples'][0]['delta'] == 2


def test_ties_tolerance_and_no_alternatives_are_distinct():
    r = perturbation_report(['a'], {'a': 'x'}, 'xy', lambda m: 1e-10 * (m['a'] == 'y'))
    assert r['tied'] == 1 and r['improving'] == 0 and r['local_optimum'] is True
    r = perturbation_report(['a', 'a'], {'a': 'x'}, 'xy', lambda _: 0, singletons_only=True)
    assert r['tested'] == 0 and r['local_optimum'] is None


def test_singleton_mode_and_bounded_examples():
    r = perturbation_report(['a', 'b', 'c', 'c'], dict(a='x', b='x', c='x'), 'xyz',
                            lambda m: sum(v != 'x' for v in m.values()),
                            singletons_only=True, max_examples=1)
    assert r['tested_symbols'] == 2 and r['tested'] == 4
    assert r['improving_symbols'] == 2 and len(r['examples']) == 1
    assert r['examples'][0]['symbol'] == 'a'


@pytest.mark.parametrize('score', [lambda _: math.nan, lambda _: math.inf,
                                 lambda m: 0 if m['a'] == 'x' else -math.inf])
def test_nonfinite_scores_rejected(score):
    with pytest.raises(ValueError):
        perturbation_report(['a'], {'a': 'x'}, 'xy', score)


def test_bad_key_and_empty_experiment_rejected():
    for tokens, key in [([], {}), (['a'], {}), (['a'], {'a': 'q'})]:
        with pytest.raises(ValueError):
            perturbation_report(tokens, key, 'xy', lambda _: 0)
