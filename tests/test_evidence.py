import copy
import itertools
import json
import random
import subprocess
import sys

import pytest

from cipherkit.evidence import rejection_record, verify_rejection, _fits, _fits_blocks


def test_length_rejection_in_known_rows_despite_missing_row():
    r = rejection_record([['x', 'y'], ['z']], ['a', None])
    assert r['status'] == 'rejected' and r['witness']['kind'] == 'row_length'
    assert verify_rejection(json.loads(json.dumps(r)))
    assert verify_rejection(rejection_record([[]], ['a']))
    assert not verify_rejection(rejection_record([[]], ['']))


def test_repeated_glyph_polygrams_and_homophones():
    r = rejection_record([['x'], ['x']], ['ab', 'ac'])
    assert r['witness'] == dict(kind='empty_glyph_domain', glyph='x')
    assert verify_rejection(r)
    for rows, plains in [([['x', 'y', 'x']], ['abQab']),
                         ([['x', 'x', 'y', 'y']], ['aaaa']),
                         ([['x', 'x']], ['####'])]:
        assert rejection_record(rows, plains)['status'] == 'inconclusive'


def test_limits_and_absence_of_evidence_never_become_rejections():
    for kwargs, reason in [({'max_candidates': 0}, 'candidate_limit'), ({'timeout': 0}, 'timeout')]:
        r = rejection_record([['x', 'x']], ['ab'], **kwargs)
        assert r['status'] == 'inconclusive' and r['reason'] == reason
        assert not verify_rejection(r)
    assert rejection_record([['x']], [None])['reason'] == 'no_known_rows'
    assert rejection_record([['x']], ['abc'])['reason'] == 'no_contradiction'
    with pytest.raises(ValueError):
        rejection_record([['x']], [])


def test_stale_forged_and_malformed_records_fail_verification():
    r = rejection_record([['x'], ['x']], ['ab', 'ac'])
    changed = copy.deepcopy(r)
    changed['inputs']['plaintext_rows'][1] = 'ab'
    assert not verify_rejection(changed)
    forged = rejection_record([['x'], ['x']], ['ab', 'ab'])
    forged.update(status='rejected', witness=dict(kind='empty_glyph_domain', glyph='x'))
    assert not verify_rejection(forged)
    for witness in [dict(kind='row_length', row=-1), dict(kind='other'),
                    dict(kind='empty_glyph_domain', glyph='missing')]:
        forged['witness'] = witness
        assert not verify_rejection(forged)
    assert not verify_rejection({})


def test_independent_matchers_agree_with_bruteforce_on_small_cases():
    rng = random.Random(927)
    for _ in range(250):
        row = [rng.choice('xy') for _ in range(rng.randint(0,4))]
        text = ''.join(rng.choice('ab') for _ in range(rng.randint(0,7)))
        value = rng.choice(['a', 'b', 'ab', 'aa'])
        # Independent enumeration of lengths for free occurrences, then exact
        # substrings. Other y occurrences may have different values in this relaxation.
        expected = False
        for lengths in itertools.product(range(1,len(text)+1), repeat=row.count('y')):
            it = iter(lengths); pos = 0; good = True
            for g in row:
                if g == 'x':
                    good &= text.startswith(value, pos); pos += len(value)
                else:
                    pos += next(it)
            if good and pos == len(text): expected = True; break
        assert _fits(row,text,'x',value) == expected
        assert _fits_blocks(row,text,'x',value) == expected


def test_no_false_rejections_of_random_planted_keys():
    rng = random.Random(28)
    for _ in range(100):
        key = {g: rng.choice(['a','b','ab','ba','aab']) for g in 'xyz'}
        rows = [[rng.choice('xyz') for _ in range(rng.randint(1,6))] for _ in range(3)]
        plain = [''.join(key[g] for g in row) for row in rows]
        assert rejection_record(rows,plain)['status'] == 'inconclusive'


def test_cli_fails_closed_on_empty_invalid_and_unverified_records(tmp_path):
    path = tmp_path/'evidence.jsonl'
    good = rejection_record([['x', 'x']], ['ab'])
    path.write_text(json.dumps(good)+'\n')
    def run():
        return subprocess.run([sys.executable,'-m','cipherkit.evidence',str(path)],
                              capture_output=True,text=True)
    result = run()
    assert result.returncode == 0 and json.loads(result.stdout)['verified_rejections'] == 1
    for text in ['', '{bad json', json.dumps(rejection_record([['x']], ['a']))]:
        path.write_text(text)
        assert run().returncode == 1
