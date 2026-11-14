#!/usr/bin/env python3
"""Reproduce the Ridolfi (October 1494) and Alamanni (April 1494) readings from the two
transcriptions and key.json, check them against the committed reading.txt, and print the
read fractions and grade counts. Standard library plus cipherkit.

    python3 milan-1494/verify.py            # check (exit 1 if reading.txt is stale or a rule fails)
    python3 milan-1494/verify.py --write    # rewrite reading.txt

Checks, for every cipher word:
- every label is in key.json, and a label with several values carries the chosen one (`N=c`),
  which must be one of its values;
- a word read as `strict` uses only single-valued labels, with no other shape reading and no
  poorly seen sign;
- the editorial reading, with [bracketed] letters removed, accents and apostrophes dropped and
  v written u, spells exactly what the key gives (person signs and unidentified signs excepted).

Grades (CONVENTIONS.md section 1) are assigned per word: unread or doubtful words M; words
using a person sign or a name number I; words whose reading depends on an unidentified sign I;
other lenient words (the choice among the signs' values was made by sense) M; forced words
(only one choice gives a word) S, or M if a sign in them is poorly seen; strict words take the
weakest provenance of their signs' values: H for a value on the key sheet, C for a value fixed
by a contemporary gloss, S for a value fitted to the text.
"""
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from cipherkit.grades import Reading, check_grade, counts, summary_line  # noqa: E402

LETTERS = [("ridolfi", "ridolfi-transcription.tsv"), ("alamanni", "alamanni-transcription.tsv")]
ORDER = {"H": 0, "C": 1, "S": 2, "M": 3, "I": 4}
TOKEN = re.compile(r"^(\^?)([^=\{\?]+|\?)(?:=([^\{\?]*))?(?:\{([^}]*)\})?(\?)?$")


def load_key():
    return json.load(open(os.path.join(HERE, "key.json")))["signs"]


def load_rows(name):
    rows = []
    for line in open(os.path.join(HERE, name)):
        if line.startswith("#") or line.startswith("id\t") or not line.strip():
            continue
        f = line.rstrip("\n").split("\t")
        f += [""] * (8 - len(f))
        rows.append(dict(zip(["id", "leaf", "line", "kind", "tokens", "tier", "reading", "note"], f)))
    return rows


def parse_token(tok, key, where):
    m = TOKEN.match(tok)
    if not m:
        raise SystemExit(f"{where}: cannot parse token {tok!r}")
    raised, label, chosen, alts, low = m.groups()
    if label not in key:
        raise SystemExit(f"{where}: label {label!r} is not in key.json")
    values = key[label]["values"]
    if len(values) > 1:
        if chosen is None:
            raise SystemExit(f"{where}: {label!r} has values {values}; the transcription must say which (label=value)")
        if chosen not in values:
            raise SystemExit(f"{where}: {chosen!r} is not a value of {label!r} ({values})")
    elif chosen is not None and chosen != values[0]:
        raise SystemExit(f"{where}: {label!r} has the single value {values[0]!r}, not {chosen!r}")
    else:
        chosen = values[0]
    return dict(label=label, value=chosen, alts=alts, low=bool(low), raised=bool(raised),
                multi=len(values) > 1, grade=key[label]["grade"])


def plain(s):
    s = re.sub(r"\[[^\]]*\]", "", s)
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.replace("v", "u").replace("'", "").replace(" ", "")


def grade_word(toks, tier, where):
    if tier == "strict":
        bad = [t["label"] for t in toks if t["multi"] or t["alts"] or t["low"] or t["value"] == "?"]
        if bad:
            raise SystemExit(f"{where}: read as strict but {bad} are ambiguous, have other shape readings or are poorly seen")
    if tier in ("unread", "doubt"):
        return "M"
    if any(t["grade"] == "I" for t in toks):
        return "I"
    if any(t["value"] == "?" for t in toks):
        return "I"
    if tier == "lenient":
        return "M"
    if tier == "forced":
        return "M" if any(t["low"] for t in toks) else "S"
    if tier == "strict":
        return max((t["grade"] for t in toks), key=ORDER.get)
    raise SystemExit(f"{where}: unknown tier {tier!r}")


def build():
    key = load_key()
    out, summary, ok = [], [], True
    for letter, name in LETTERS:
        readings, tiers = [], {}
        out.append(f"## {letter}")
        for r in load_rows(name):
            where = f"{name} {r['id']}"
            if r["kind"] in ("clear", "null"):
                if r["kind"] == "null":
                    for tok in r["tokens"].split():
                        if parse_token(tok, key, where)["value"] != "":
                            raise SystemExit(f"{where}: a null row holds a non-null sign")
                continue
            toks = [parse_token(t, key, where) for t in r["tokens"].split()]
            literal = "".join(t["value"] for t in toks)
            g = check_grade(grade_word(toks, r["tier"], where))
            if r["tier"] != "unread" and g != "I" and plain(r["reading"]) != plain(literal):
                print(f"{where}: reading {r['reading']!r} does not spell the key's {literal!r}", file=sys.stderr)
                ok = False
            readings.append(Reading(r["tokens"], literal, g))
            tiers[r["tier"]] = tiers.get(r["tier"], 0) + 1
            out.append(f"{r['id']}\t{literal}\t{r['reading']}\t{r['tier']}\t{g}")
        n = len(readings)
        s, f, l, d, u = (tiers.get(k, 0) for k in ("strict", "forced", "lenient", "doubt", "unread"))
        line = (f"{letter}: {n} cipher words | strict {s} ({s / n:.1%}) | +forced {s + f} ({(s + f) / n:.1%}) | "
                f"+lenient {s + f + l} ({(s + f + l) / n:.1%}) | doubtful {d} | unread {u} | grades {summary_line(counts(readings))}")
        summary.append(line)
        out.append(line)
    return "\n".join(out) + "\n", summary, ok


def permutation_z(letter, name, n=1000, seed=0):
    """Key-shuffle null (cipherkit.controls.permutation_z_key): the Italian 4-gram score of
    the words read in `letter`, against keys that shuffle the single-letter values among the
    (label, chosen value) symbols actually used. Code signs, person signs, doubled-consonant
    signs and nulls keep their values. Unread words are left out."""
    from cipherkit import corpora
    from cipherkit.controls import permutation_z_key
    from cipherkit.lm import CharLM
    from cipherkit.normalize import EARLY_MODERN_FOLDS, normalize
    try:
        lm = CharLM.from_text(normalize(corpora.text("it"), folds=EARLY_MODERN_FOLDS, keep_spaces=True), order=4)
    except Exception as e:  # corpus not fetched
        return f"no Italian corpus ({e.__class__.__name__}); run: python -m cipherkit.corpora fetch it"
    key = load_key()
    words = []
    for r in load_rows(name):
        if r["kind"] == "word" and r["tier"] != "unread":
            toks = [parse_token(t, key, r["id"]) for t in r["tokens"].split()]
            if all(t["value"] != "?" and not t["value"].startswith("[") for t in toks):
                words.append([(t["label"], t["value"]) for t in toks])
    symkey = {sym: sym[1] for w in words for sym in w}

    def score(m):
        return lm.score_words("".join(m[s] for s in w) for w in words)

    res = permutation_z_key(score, symkey, words, n=n, seed=seed)
    return f"{letter}: observed {res['observed']:.1f}, null mean {res['mean']:.1f} (sd {res['sd']:.1f}), z = {res['z']:.1f}, p = {res['p']}"


def main():
    if "--z" in sys.argv:
        for letter, name in LETTERS:
            print("permutation z (key shuffle):", permutation_z(letter, name))
        return
    text, summary, ok = build()
    path = os.path.join(HERE, "reading.txt")
    header = "# Generated by verify.py: id, key output, editorial reading, tier, grade. Do not edit by hand.\n"
    if "--write" in sys.argv:
        open(path, "w").write(header + text)
        print("wrote reading.txt")
    print("\n".join(summary))
    if not os.path.exists(path) or open(path).read() != header + text:
        print("reading.txt is stale; run with --write", file=sys.stderr)
        ok = False
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
