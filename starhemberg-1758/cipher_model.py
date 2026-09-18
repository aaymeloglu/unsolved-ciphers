"""Mechanical model shared by the target and independent historical control."""
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
        # Grade per CONVENTIONS.md: H = found in the 1752 tables, M = not in the working
        # key or malformed, '-' = null, control or switch. Repairs (I) live in repair-cases.json.
        if kind == 'ordinary':
            grade = 'M' if value.startswith('{') else 'H'
        elif kind == 'invalid':
            grade = 'M'
        else:
            grade = '-'
        tokens.append({'offset': i, 'source_start': locations[i],
                       'source_end': locations[min(i + width - 1, len(digits) - 1)],
                       'table': before, 'code': code, 'kind': kind, 'value': value,
                       'grade': grade})
        i += width
    assert ''.join(t['code'] for t in tokens) == digits
    return tokens
