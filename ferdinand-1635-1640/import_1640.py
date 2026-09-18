#!/usr/bin/env python3
"""Import XZ's explicit DECODE units; never split unknown groups to improve Latin."""
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parent

def main():
    page = row = 0
    out = ['# Source-row identifiers Cnn exclude clear-only lines; source rows are retained.',
           '# XZ uses double spaces between units and single spaces within units.',
           '# Internal unit spaces are removed; cleartext is enclosed in braces.',
           '# Unknown and ambiguous units are preserved, including source segmentation anomalies.']
    for line in (ROOT / 'sources/R1890-DECODE.txt').read_text().splitlines():
        if line.startswith('#IMAGE NAME: 9352.png'):
            page, row = 1, 0
        elif line.startswith('#IMAGE NAME: 9353.png'):
            page, row = 2, 0
        if not line or line.startswith(('#', '<')):
            continue
        row += 1
        parts = []
        for part in re.split(r'(<CLEARTEXT LA .*?>)', line):
            if part.startswith('<CLEARTEXT LA '):
                # Source cleartext is not silently corrected here.
                parts.append('{' + part[len('<CLEARTEXT LA '):-1] + '}')
            else:
                units = [''.join(u.split()) for u in re.split(r' {2,}', part.strip()) if u.strip()]
                # Sole punctuation split: attached terminal full stop is not a new code.
                units = [v for u in units for v in ([u[:-1], '.'] if u.endswith('.') and u[:-1].isdigit() else [u])]
                parts.extend(units)
        out.append(f'P{page}.C{row:02d} ' + ' '.join(parts))
    (ROOT / 'transcriptions/R1890-working.txt').write_text('\n'.join(out) + '\n')

if __name__ == '__main__':
    main()
