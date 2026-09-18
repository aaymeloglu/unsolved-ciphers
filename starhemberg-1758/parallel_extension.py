"""Extend the independent1756 comparison without forcing a full transcription.

Local windows have explicit starts; damaged/uncertain intervening digits are not
silently repaired. Only the date/address window is used as an additional check.
"""
import json
from pathlib import Path
from cipher_model import parse_units

P = Path(__file__).resolve().parent
keys = {t: dict(line.split('\t', 1) for line in (P / f).read_text().splitlines())
        for t, f in [('A', 'working-prima-v4.tsv'), ('B', 'working-secunda.tsv')]}
raw = '31.44.33104.785.28.398.404.4310.650.53.101.03.105.131.22.831.282'
digits = ''.join(c for c in raw if c.isdigit())
controls = {10: ('852', 'day boundary'), 13: ('839', 'month boundary'),
            16: ('840', 'marked switch')}
tokens = parse_units(digits, controls, keys)
expected = '31443 31047 852 839 840 44 31065 05 31010 31051 31228 31282'.split()
assert len(digits) == 48
assert [t['code'] for t in tokens] == expected
assert [(t['table'], t['code']) for t in tokens if t['kind'] == 'switch'] == [('A', '840')]
assert [t['value'] for t in tokens[2:4]] == ['13', 'Marti']
assert all(t['table'] == 'B' for t in tokens[5:])
report = {
    'status': 'Additional local comparison; not an exact complete1756 edition',
    'source': 'Antal/Mírka/Kováč, DOI10.1080/01611194.2025.2457096, Figures1–2, printedp193',
    'location': 'Cipher row2 tail across row3 first half; independent of first53digit fragment',
    'raw_transcription': raw, 'digits': digits, 'digit_count': len(digits),
    'literal_roots': ' / '.join(t['value'] for t in tokens),
    'tokens': tokens,
    'comparison_reading': 'so den13Marti an EuerExcellenz abgefert…',
    'qualification': [
        'End of word abgefertigt lies outside this checked window.',
        'Control boundaries use visible marks together with source-key day/month entries; precise pen-mark placement is not mechanically measured.',
        'The key table reads A852=13, A839=Marti, A840=switch; B31065=EuerExcellenz.',
        'As in the first fragment, spelling, grammatical endings, and ge/gn/gen expansion require editorial reading.',
    ],
    'additional_observations_not_counted_as_passed_control': [
        {'reading': 'von der Vollziehung der damahligen …',
         'evidence': 'Surviving plaintext, plus partial cipher/key matches; the exact digit transcript includes unresolved3/8 and2/3 readings.',
         'effect_on_target': 'Prompted independent alphabetical/numerical rereading of B53 as mahl with s/en endings, superseding meist.'},
        {'reading': 'B900 is a comma', 'evidence': 'R1698I7486P3 bottom control row; candidate boundary in1756 row3.'},
        {'reading': 'Title/Expresse span between original53digits and newwindow',
         'status': 'Not fully aligned; ambiguous digits and abbreviated roots. No claim of a continuous101digit match.'},
        {'reading': 'Remaining lower portion of cipher illustration',
         'status': 'Inspected; several digit and mark ambiguities remain. Not included in calibration.'},
    ],
}
(P / 'parallel-extension.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print('PASS: additional48digit/12unit window, 13Marti, switch840, address and abgefert…')
