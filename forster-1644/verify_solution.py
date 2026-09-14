#!/usr/bin/env python3
"""Audit the supplied Forster key without a lexicon or search algorithm.

Run from any directory. Outputs JSON to stdout; leaves source files untouched.
Expected text retains u/v convention, conceruer and des uos. Exactly three
proposed letter emendations are tested, explicitly rather than silently applied.
"""
import collections
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
raw = ROOT.joinpath('ct.txt').read_text()
key = json.loads(ROOT.joinpath('mapping.json').read_text())
cipher = re.sub(r'\[.*?\]', '|', raw, flags=re.S)
groups = [re.findall(r'\d+|[a-z]', part) for part in re.split(r'[,|]', cipher)]
groups = [group for group in groups if group]
expected = (
    'il ny a aucun subiet descrupule de manquera dieu lesreigles de '
    'perfection prenezseulement lesuoyesde prudence pour conceruer uotre '
    'uie pour enfaire a dieu un plus grand sacrifice parla multiplication '
    'des uos seruices pour lesalut de uos freres'
).split()
assert len(groups) == len(expected) == 37
rows, mismatches, observations = [], [], []
offset = 0
for index, (group, proposed) in enumerate(zip(groups, expected), 1):
    assert len(group) == len(proposed), (index, group, proposed)
    literal = ''.join(key[symbol] for symbol in group)
    rows.append({'group': index, 'cipher': ' '.join(group), 'literal': literal,
                 'proposed': proposed})
    for position, (symbol, letter) in enumerate(zip(group, proposed), 1):
        observations.append((index, symbol, letter))
        if key[symbol] != letter:
            mismatches.append({'group': index, 'position_in_group': position,
                               'token_position': offset + position,
                               'symbol': symbol, 'key_value': key[symbol],
                               'proposed_value': letter})
    offset += len(group)

# Withhold each entire group, infer symbol values by majority from all other
# proposed groups, and predict the withheld group. This is a consistency audit,
# not a blind validation: the proposed reading was developed using all groups.
predictions = []
for index, group in enumerate(groups, 1):
    votes = collections.defaultdict(collections.Counter)
    for other, symbol, letter in observations:
        if other != index:
            votes[symbol][letter] += 1
    predicted = ''
    for symbol in group:
        ranking = votes[symbol].most_common()
        predicted += (ranking[0][0] if ranking and
                      (len(ranking) == 1 or ranking[0][1] > ranking[1][1]) else '?')
    predictions.append({'group': index, 'predicted': predicted})

counts = collections.Counter(s for group in groups for s in group)
classes = {}
for label, predicate in [('letter_symbols', str.isalpha), ('number_symbols', str.isdigit)]:
    subset = {s: key[s] for s in counts if predicate(s)}
    classes[label] = {'symbols': len(subset), 'distinct_values': len(set(subset.values())),
                      'mapping': subset}
result = {
    'cipher_sha256': hashlib.sha256(raw.encode()).hexdigest(),
    'tokens': offset, 'symbols': len(counts), 'groups': len(groups),
    'plaintext_values': len(set(key.values())),
    'matches_to_minimally_emended_reading': offset - len(mismatches),
    'mismatches': mismatches, 'symbol_classes': classes,
    'frequencies': dict(counts), 'group_decodings': rows,
    'leave_one_group_out_consistency': predictions,
}
assert offset == 207 and len(counts) == 34
assert [(m['group'], m['position_in_group']) for m in mismatches] == [(13, 8), (16, 2), (27, 8)]
print(json.dumps(result, ensure_ascii=False, indent=2))
