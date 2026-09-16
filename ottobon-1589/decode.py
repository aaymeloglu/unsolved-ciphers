"""Literal archival-key lookup for the Ottobon transcription; Python 3 stdlib."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def decode_token(token, mapping):
    if token.startswith('{') and token.endswith('}'):
        return '{' + '/'.join(decode_token(t, mapping)
                              for t in token[1:-1].split('/')) + '}'
    value = mapping.get(token)
    return '[' + token + '?]' if value is None else value or '[null]'


def literal(tokens, mapping):
    return ' | '.join(decode_token(t, mapping) for t in tokens.split())


def render(document, mapping):
    out = ['# Ottobon–Mocenigo: line-by-line transcription', '',
           'Generated from [transcription.json](transcription.json) and '
           '[key.json](key.json). Literal lookup and editorial reading are separate. '
           'See [notation and limitations](README.md#reproduce-the-literal-decoding) '
           'and [manuscript page locations](SOURCES.md#manuscript-page-locations).', '']
    for folio in document['folios']:
        out.extend([f'## f.{folio["folio"]}', ''])
        for row in folio['rows']:
            out.extend([f'### f.{folio["folio"]}, line {row["line"]}', '',
                        '`' + row['tokens'] + '`', '',
                        'Literal: `' + literal(row['tokens'], mapping) + '`', '',
                        'Reading: ' + row['reading'], ''])
        if folio.get('clear_text'):
            out.extend(['Clear handwriting (brackets mark expansions or uncertainty):', ''])
            for label, value in folio['clear_text'].items():
                out.extend([f'**{label}:** {value}', ''])
    return '\n'.join(out).rstrip() + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tokens', help='Decode a supplied sequence')
    parser.add_argument('--folio', help='Select folio, e.g. 35v')
    parser.add_argument('--line', type=int, help='Select cipher-line number')
    parser.add_argument('--check', action='store_true', help='Check literal fields and generated Markdown')
    parser.add_argument('--write', action='store_true', help='Regenerate TRANSCRIPTION.md')
    args = parser.parse_args()
    mapping = json.loads((ROOT / 'key.json').read_text())['mapping']
    document = json.loads((ROOT / 'transcription.json').read_text())
    if args.tokens:
        print(literal(args.tokens, mapping))
        return
    rendered = render(document, mapping)
    if args.write:
        (ROOT / 'TRANSCRIPTION.md').write_text(rendered)
    if args.check:
        errors, count, slots, uncertain = [], 0, 0, 0
        for folio in document['folios']:
            for row in folio['rows']:
                count += 1
                tokens = row['tokens'].split()
                slots += len(tokens)
                uncertain += sum('?' in t or '{' in t for t in tokens)
                if row['literal_decode'] != literal(row['tokens'], mapping):
                    errors.append(f'{folio["folio"]}:{row["line"]}: literal mismatch')
        if (ROOT / 'TRANSCRIPTION.md').read_text() != rendered:
            errors.append('TRANSCRIPTION.md is stale; run --write')
        if errors:
            parser.exit(1, '\n'.join(errors) + '\n')
        print(f'PASS: {count} rows; {slots} provisional token slots; '
              f'{uncertain} explicitly uncertain slots. Markdown matches JSON/key.')
        print('Consistency check only; these counts do not measure handwriting accuracy.')
    elif not args.write:
        found = False
        for folio in document['folios']:
            if args.folio and args.folio != folio['folio']:
                continue
            for row in folio['rows']:
                if args.line is not None and args.line != row['line']:
                    continue
                found = True
                print(f'f.{folio["folio"]}, line {row["line"]}')
                print(row['tokens'])
                print(literal(row['tokens'], mapping))
                print('Reading:', row['reading'], '\n')
        if not found:
            parser.error('No matching folio/line')


if __name__ == '__main__':
    main()
