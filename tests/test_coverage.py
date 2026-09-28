import json
import subprocess
import sys

import pytest

from cipherkit.coverage import coverage_report


def test_missing_words_count_once_per_window_and_rank_by_repair_value():
    rows = [['rare', 'rare'], ['known'], ['rare'], ['common'], ['other', 'common']]
    r = coverage_report(rows, {'known': ['n']}, window_size=2)
    assert r['tokens'] == 7 and r['known_tokens'] == 1
    assert r['windows'] == 4 and r['evaluable_windows'] == 0
    q = {x['word']: x for x in r['correction_queue']}
    assert q['rare'] == dict(word='rare', tokens=3, blocked_windows=3, recoverable_windows=2)
    assert q['common']['recoverable_windows'] == 0
    assert r['correction_queue'][0]['word'] == 'rare'


def test_empty_rows_are_barriers_and_unknown_variants_stay_missing():
    r = coverage_report([['a'], [], ['a'], ['b'], ['c']],
                        {'a': ['x', 'y'], 'b': [''], 'c': []}, window_size=2)
    assert r['windows_with_empty_rows'] == 2
    assert r['windows_with_missing_words'] == 2
    assert r['evaluable_windows'] == 0
    assert r['known_tokens'] == 2 and r['missing_tokens'] == 2
    assert r['windows'] == (r['windows_with_empty_rows'] + r['windows_with_missing_words']
                            + r['evaluable_windows'])


def test_no_windows_is_not_full_coverage_and_queue_truncation_explicit():
    r = coverage_report([['b', 'a']], {}, window_size=4, max_missing=1)
    assert r['window_coverage'] is None
    assert r['omitted_missing_types'] == 1
    assert r['correction_queue'][0]['word'] == 'a'
    assert coverage_report([], {})['token_coverage'] is None


def test_complete_coverage_and_case_are_explicit():
    r = coverage_report([['a'], ['A'], ['a']], {'a': ['x']}, window_size=1)
    assert r['evaluable_windows'] == 2 and r['window_coverage'] == 2 / 3
    assert r['correction_queue'][0]['word'] == 'A'


def test_validation_and_cli(tmp_path):
    with pytest.raises(ValueError):
        coverage_report([['a']], {'a': 'x'})
    with pytest.raises(ValueError):
        coverage_report([], {}, window_size=0)
    data = dict(rows=[['a'], ['b']], lexicon={'a': ['x']}, window_size=1)
    path = tmp_path/'input.json'
    path.write_text(json.dumps(data))
    r = subprocess.run([sys.executable, '-m', 'cipherkit.coverage', str(path)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout) == coverage_report(**data)
