"""Mechanical model shared by the target and independent historical control."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cipherkit.grades import GRADES  # noqa: E402

SWITCHES = {'A': {'810', '818', '840', '855', '876', '890'},
            'B': {'801', '822', '830', '855', '885', '899'}}
# Where each grade H comes from, as read on the DECODE images (page = DECODE image id).
TABLE_SOURCE = {'A': '1752 Clavis Prima, numeric (R1698 I7484 P1)',
                'B': '1752 Clavis Secunda, numeric (R1698 I7486 P3)'}
NULL_SOURCE = '1752 Nota, items 2 and 4 (R1696 I7480 P1): 8 is the errans (null) among two-digit numbers'
MARK_NAMES = {',': 'coma', '.': 'punctum'}
CONTROLS = {'A': {'832': '26', '852': '13', '839': 'Marti',
                  '854': ',', '891': ',', '878': '.'},
            'B': {'870': ',', '841': ',', '897': '.', '900': ','}}


def parse_units(digits, controls, keys, locations=None, initial_table='A'):
    locations = locations or [(1, i + 1) for i in range(len(digits))]
    assert initial_table in ('A', 'B')
    state = initial_table
    i = 0
    tokens = []
    while i < len(digits):
        before = state
        if i in controls:
            code, mark = controls[i]
            width = 3
            assert digits[i:i + width] == code
            kind = 'control'
            value = CONTROLS.get(state, {}).get(code, '[' + code + ']')
            if code in SWITCHES[state]:
                state = 'B' if state == 'A' else 'A'
                kind = 'switch'
                value = '[' + before + '→' + state + ']'
        else:
            width = 5 if digits[i] == '3' else 1 if digits[i] == '8' else 2
            next_mark = min((p for p in controls if p > i), default=len(digits))
            width = min(width, next_mark - i)
            code = digits[i:i + width]
            kind = 'null' if code == '8' else 'ordinary'
            value = '' if code == '8' else keys[state].get(code, '{' + code + '}')
            if digits[i] == '3' and (len(code) != 5 or not
                    (code == '30000' or 31000 <= int(code) <= 31500)):
                kind = 'invalid'
        # Grade per CONVENTIONS.md, H = looked up in the surviving key material, all read on
        # the DECODE images (private-source-manifest.json in the research folder; not
        # redistributed):
        #   ordinary unit in the 1752 Prima/Secunda tables (R1698 I7484 P1, I7486 P3)   -> H
        #   standalone 8: the Nota of 3 Sept 1752 (R1696 I7480 P1, items 2 and 4) makes
        #     it the "errans", and both numeric tables head their 800 column
        #     "8 errans cum duobus numeris tantum"                                        -> H
        #   marked three-digit code listed in the table's 800 column (854 coma and
        #     876 indic. Clav. Secundam on P1; 841 Coma, 870 Coma, 897 punctum and
        #     899 indic. clav. Primam on P3)                                              -> H
        #   unit absent from the working key, malformed, or a mark not in that column   -> M
        # Repairs (I) live in repair-cases.json, never here.
        if kind == 'ordinary':
            grade, basis = ('M', 'absent from the working key') if value.startswith('{') \
                else ('H', TABLE_SOURCE[before])
        elif kind == 'null':
            grade, basis = 'H', NULL_SOURCE
        elif kind == 'switch':
            grade, basis = 'H', f'{TABLE_SOURCE[before]}, 800 column: {code} indic. Clav. {"Secundam" if state == "B" else "Primam"}'
        elif kind == 'control' and value != '[' + code + ']':
            grade, basis = 'H', f'{TABLE_SOURCE[before]}, 800 column: {code} {MARK_NAMES.get(value, value)}'
        elif kind == 'invalid':
            grade, basis = 'M', 'malformed unit'
        else:
            grade, basis = 'M', "marked code not in the table's 800 column"
        tokens.append({'offset': i, 'source_start': locations[i],
                       'source_end': locations[min(i + width - 1, len(digits) - 1)],
                       'table': before, 'code': code, 'kind': kind, 'value': value,
                       'grade': grade, 'basis': basis})
        i += width
    assert ''.join(t['code'] for t in tokens) == digits
    assert all(t['grade'] in GRADES for t in tokens)
    return tokens
