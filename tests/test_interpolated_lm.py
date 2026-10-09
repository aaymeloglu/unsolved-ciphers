import itertools
import json
import math
import random

import pytest

from cipherkit import InterpolatedCharLM


def test_interpolation_has_known_probabilities():
    model = InterpolatedCharLM.from_text('ababa', alphabet='abc', order=3)
    assert 10 ** model.logp('b') == pytest.approx(3 / 8)
    assert 10 ** model.logp('ab') == pytest.approx(19 / 24)
    assert 10 ** model.logp('aa') == pytest.approx(1 / 6)
    assert 10 ** model.logp('ac') == pytest.approx(1 / 24)
    assert model.logp('cb') == model.logp('b')  # unseen context backs off
    for n in range(3):
        for context in map(''.join, itertools.product('abc', repeat=n)):
            probs = [10 ** model.logp(context + c) for c in 'abc']
            assert min(probs) > 0 and sum(probs) == pytest.approx(1)


def test_terminal_context_counts_only_actual_successors():
    model = InterpolatedCharLM.from_text('aba', alphabet='ab', order=2)
    assert 10 ** model.logp('ab') == pytest.approx((1 + 2 / 5) / 2)
    assert sum(10 ** model.logp('a' + c) for c in 'ab') == pytest.approx(1)


def test_empty_training_and_order_one():
    empty = InterpolatedCharLM.from_text('', alphabet='ab')
    assert empty.logp('abba') == pytest.approx(math.log10(.5))
    unigram = InterpolatedCharLM.from_text('aaa', alphabet='ab', order=1)
    assert unigram.score('ab') == pytest.approx(math.log10(4 / 5) + math.log10(1 / 5))
    assert unigram.score('') == 0


def test_score_start_contexts_and_separate_segments():
    model = InterpolatedCharLM.from_text('ababa', alphabet='ab', order=3)
    assert model.score('abaa') == sum(model.logp(g) for g in ['a', 'ab', 'aba', 'baa'])
    assert model.score('a') + model.score('b') != model.score('ab')
    with pytest.raises(ValueError):
        model.score('a?b')  # cannot silently score across a removed unknown
    with pytest.raises(ValueError):
        model.logp('abab')
    with pytest.raises(ValueError):
        model.logp('')


@pytest.mark.parametrize('params', [dict(alphabet=''), dict(alphabet='aa'),
    dict(alphabet='ab', order=0), dict(alphabet='ab', order=True),
    dict(alphabet='ab', alpha=0), dict(alphabet='ab', alpha=float('nan'))])
def test_invalid_parameters(params):
    with pytest.raises(ValueError):
        InterpolatedCharLM.from_text('ab', **params)


def test_training_never_silently_normalizes():
    with pytest.raises(ValueError):
        InterpolatedCharLM.from_text('a b', alphabet='ab')
    model = InterpolatedCharLM.from_text('a b', alphabet='ab ')
    assert math.isfinite(model.score('a b'))


def test_cache_roundtrip_and_reuse(tmp_path, monkeypatch):
    path = tmp_path / 'model.json'
    model = InterpolatedCharLM.cached_from_text(path, 'ababa', alphabet='abc')
    assert InterpolatedCharLM.load(path).score('abca') == model.score('abca')
    def fail(*args, **kwargs):
        raise AssertionError('matching cache should not rebuild')
    monkeypatch.setattr(InterpolatedCharLM, 'from_text', fail)
    assert InterpolatedCharLM.cached_from_text(path, 'ababa', alphabet='abc').score('abca') == model.score('abca')


@pytest.mark.parametrize('text,params', [
    ('bbb', dict(alphabet='ab')), ('aba', dict(alphabet='abc')),
    ('aba', dict(alphabet='ba')), ('aba', dict(alphabet='ab', order=2)),
    ('aba', dict(alphabet='ab', alpha=2)),
])
def test_cache_invalidates_every_input(tmp_path, text, params):
    path = tmp_path / 'model.json'
    old = InterpolatedCharLM.cached_from_text(path, 'aba', alphabet='ab')
    new = InterpolatedCharLM.cached_from_text(path, text, **params)
    direct = InterpolatedCharLM.from_text(text, **params)
    assert new._stamp() != old._stamp()
    assert new._stamp() == direct._stamp()
    assert new.score('aba') == direct.score('aba')


@pytest.mark.parametrize('damage', ['version', 'broken_json', 'invalid_counts'])
def test_cache_recovers_from_stale_or_malformed_data(tmp_path, damage):
    path = tmp_path / 'model.json'
    old = InterpolatedCharLM.cached_from_text(path, 'aba', alphabet='ab')
    data = json.loads(path.read_text())
    if damage == 'version':
        data['stamp']['version'] = -1
    if damage == 'invalid_counts':
        data['counts']['a'] = -2
    path.write_text('{' if damage == 'broken_json' else json.dumps(data))
    rebuilt = InterpolatedCharLM.cached_from_text(path, 'aba', alphabet='ab')
    assert rebuilt.score('aba') == old.score('aba')


def test_heldout_english_beats_shuffle(english_text, english_tail):
    train = english_text[:int(len(english_text) * .8)].replace(' ', '')
    real = english_tail.replace(' ', '')[:400]
    model = InterpolatedCharLM.from_text(train, alphabet='abcdefghijklmnopqrstuvwxyz')
    shuffled = list(real); random.Random(1).shuffle(shuffled)
    assert model.score(real) > model.score(''.join(shuffled))
