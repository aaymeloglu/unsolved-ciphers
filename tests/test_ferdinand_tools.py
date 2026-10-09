"""Public synthetic regressions for source handling and literal crib placement."""
import itertools

import pytest

from cipherkit import literal_crib_scan, parse, segments, transformation_report


def test_group_labels_survive_and_gaps_break_scoring():
    text = 'ax a^y B^v Bo B: .T. [gap] ax\na^y Blot B:'
    parsed = parse(text, style='groups')
    original = [t.text for t in parsed]
    assert original == text.split()
    assert segments(parsed, gaps={'[gap]', 'Blot'}) == [
        ['ax', 'a^y', 'B^v', 'Bo', 'B:', '.T.'], ['ax', 'a^y'], ['B:']]
    assert [t.text for t in parsed] == original
    assert segments(parsed) == [original]  # no implicit gap names


def test_adjacent_and_terminal_gaps_do_not_create_empty_segments():
    assert segments(parse('[gap] a [gap] [gap] b [gap]', style='groups'),
                    gaps=['[gap]']) == [['a'], ['b']]
    assert segments(parse('[gap] [gap]', style='groups'), gaps=['[gap]']) == []


def test_transformation_reports_collision_with_unchanged_label():
    source = ['ax', 'a^y', 'a^y', 'B^v', 'Bo']
    changed = ['ax', 'ax', 'ax', 'Bo', 'Bo']
    report = transformation_report(source, changed)
    assert report['changed_positions'] == 3
    assert report['source_types'] == 4 and report['transformed_types'] == 2
    assert report['mergers'] == {'ax': ['a^y', 'ax'], 'Bo': ['B^v', 'Bo']}
    assert [x['offset'] for x in report['changes']] == [1, 2, 3]
    assert source == ['ax', 'a^y', 'a^y', 'B^v', 'Bo']
    assert report['source_sha256'] != report['transformed_sha256']
    assert transformation_report(source, source)['changes'] == []
    assert transformation_report(list(reversed(source)), changed)['source_sha256'] != report['source_sha256']


@pytest.mark.parametrize('a,b', [(['a'], []), (['a'], ['']), ([None], ['a'])])
def test_transformation_rejects_silent_loss(a, b):
    with pytest.raises(ValueError):
        transformation_report(a, b)


def test_literal_crib_allows_homophones_and_reports_absolute_witness():
    assert literal_crib_scan(['A', 'B'], 'aa')['exact_offsets'] == [0]
    scan = literal_crib_scan(['X', 'A', 'A'], 'ab')
    assert scan['exact_offsets'] == [0]
    assert scan['windows'][1] == dict(offset=1, conflicting_pairs=1,
                                     witness=dict(symbol='A', offsets=[1, 2], letters=['a', 'b']))


def test_literal_unknown_is_one_position_and_never_collides_with_labels():
    assert literal_crib_scan(['A', None, 'A'], 'aba')['exact_offsets'] == [0]
    assert literal_crib_scan(['A', None, 'A'], 'abc')['exact_offsets'] == []
    assert literal_crib_scan(['GAP_1', None, 'GAP_1'], 'abc')['exact_offsets'] == []
    assert literal_crib_scan([None, None], 'ab')['exact_offsets'] == [0]
    # Spelling and punctuation are literal: no automatic u/v folding or stripping.
    assert literal_crib_scan(['A', 'A'], 'uv')['exact_offsets'] == []
    assert literal_crib_scan(['A', 'B', 'A'], 'a a')['exact_offsets'] == [0]


def test_literal_empty_and_short_inputs():
    assert literal_crib_scan([], 'a')['windows'] == []
    assert literal_crib_scan(['A'], 'ab')['windows'] == []
    with pytest.raises(ValueError):
        literal_crib_scan(['A'], '')
    with pytest.raises(ValueError):
        literal_crib_scan([''], 'a')


def test_literal_counts_and_witnesses_against_exhaustive_pair_oracle():
    for symbols in itertools.product(['A', 'B', None], repeat=4):
        for letters in itertools.product('ab', repeat=3):
            crib = ''.join(letters)
            scan = literal_crib_scan(symbols, crib)
            for row in scan['windows']:
                offset = row['offset']
                window = symbols[offset:offset + len(crib)]
                expected = sum(window[i] is not None and window[i] == window[j]
                               and crib[i] != crib[j]
                               for i in range(len(crib)) for j in range(i + 1, len(crib)))
                assert row['conflicting_pairs'] == expected
                assert (row['witness'] is None) == (expected == 0)
                if expected:
                    w = row['witness']; i, j = w['offsets']
                    assert symbols[i] == symbols[j] == w['symbol']
                    assert w['letters'] == [crib[i - offset], crib[j - offset]]
                    assert w['letters'][0] != w['letters'][1]
