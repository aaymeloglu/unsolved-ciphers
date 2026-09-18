"""Check a separately read fragment with a surviving plaintext witness.

This is a limited lexical control, not a full decipherment of the 1756 letter.
The ciphertext was read from Figure 1 independently of the target transcription;
Figure 2 supplies the comparison words. The article after von is not represented
in this parsed fragment, and endings are not a letter-for-letter match.
"""
import json
from pathlib import Path
from cipher_model import parse_units

P = Path(__file__).resolve().parent
key = dict(line.split('\t', 1) for line in
           (P / 'working-prima-v4.tsv').read_text().splitlines())
punctuated = ('3107.83.111.86.3017.331.22.031.28.131.35.03.145.33.121.431.00.'
              '57.23.11.09')
digits = ''.join(c for c in punctuated if c.isdigit())
expected = '31078 31118 63 01 73 31220 31281 31350 31453 31214 31005 72 31109'.split()
tokens = parse_units(digits, {}, {'A': key})
assert len(digits) == 53
assert [t['code'] for t in tokens] == expected
assert not any(t['kind'] == 'invalid' for t in tokens)
words = []
for label, codes, selected in [
    ('Nachricht', ['73', '31220'], ['nach', 'richt']),
    ('glücklichen', ['31350', '31453', '31214'], ['gl', 'uck', 'lich']),
    ('Ankunft', ['31005', '72'], ['an', 'kunft']),
]:
    for code, root in zip(codes, selected):
        assert root in key[code].split('/'), (code, root, key[code])
    words.append({'plaintext_word': label, 'codes': codes,
                  'selected_roots': selected,
                  'qualification': 'Spelling and endings expanded editorially.'})
report = {
    'status': 'Limited independent lexical control; not exact whole-clause alignment',
    'letter': 'Kaunitz, Vienna, 17 April 1756',
    'source': 'Antal, Mírka and Kováč, Development of obfuscation techniques in Vienna during the early modern era, printed p.193, Figures 1–2 (PDF page 4)',
    'doi': '10.1080/01611194.2025.2457096',
    'ciphertext_transcription': punctuated,
    'digits': digits,
    'ordinary_units': len(tokens),
    'literal_roots': ' / '.join(t['value'] for t in tokens),
    'comparison_words': words,
    'limitations': [
        'The surviving plaintext includes an article after von which this fragment does not encode separately.',
        'No control mark occurs within these first53digits; the next marked unit is excluded.',
        'This checks mechanics and selected roots, not all target entries or proposed repairs.',
        'The paper reports sixteen parallel letters, but they were not present in the available DECODE catalog snapshot.',
    ],
    'tokens': tokens,
}
(P / 'parallel-control.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print('PASS: separate1756 witness, 53digits/13units; Nachricht, glücklichen, Ankunft aligned.')
