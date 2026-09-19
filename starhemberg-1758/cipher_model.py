"""Mechanical model shared by the target and independent historical control."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cipherkit.grades import check_grade  # noqa: E402

SWITCHES = {'A': {'810', '818', '840', '855', '876', '890'},
            'B': {'801', '822', '830', '855', '885', '899'}}
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
        # Grade per CONVENTIONS.md, H = looked up in the surviving key material:
        #   ordinary unit in the 1752 Prima/Secunda tables (R1695/R1698)          -> H
        #   standalone 8: the instructions (R1696/R1697) define it as a null     -> H
        #   marked code whose value or switch is in the key's marked-code lists  -> H
        #   unit absent from the working key, malformed, or an unlisted mark     -> M
        # Repairs (I) live in repair-cases.json, never here.
        if kind == 'ordinary':
            grade, basis = ('M', 'absent from the working key') if value.startswith('{') \
                else ('H', '1752 Prima/Secunda tables (R1695/R1698)')
        elif kind == 'null':
            grade, basis = 'H', '1752 instructions (R1696/R1697): standalone 8 is a null'
        elif kind in ('control', 'switch') and not value.startswith('[' + code):
            grade, basis = 'H', '1752 marked codes for punctuation, dates and table changes (R1695/R1698)'
        elif kind == 'invalid':
            grade, basis = 'M', 'malformed unit'
        else:
            grade, basis = 'M', 'marked code not in the key\'s lists'
        tokens.append({'offset': i, 'source_start': locations[i],
                       'source_end': locations[min(i + width - 1, len(digits) - 1)],
                       'table': before, 'code': code, 'kind': kind, 'value': value,
                       'grade': check_grade(grade), 'basis': basis})
        i += width
    assert ''.join(t['code'] for t in tokens) == digits
    return tokens
