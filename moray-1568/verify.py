#!/usr/bin/env python3
"""Reproduce the Moray 1568 reading from transcription.txt and key.json, check it against the
committed reading.txt, print the grade counts, and, when cipherkit's Scots corpus is present,
the permutation z of the key against shuffled keys (the kit's key-shuffle null,
`cipherkit.controls.permutation_z_key`). Standard library plus cipherkit.

    python3 moray-1568/verify.py            # check (exit 1 if reading.txt is stale)
    python3 moray-1568/verify.py --write    # rewrite reading.txt
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from cipherkit.grades import apply_key, counts  # noqa: E402


def load():
    key = {k: v for k, v in json.load(open(os.path.join(HERE, "key.json"))).items() if not k.startswith("_")}
    lines = []
    for line in open(os.path.join(HERE, "transcription.txt")):
        if line.startswith("L"):
            tag, body = line.split(":", 1)
            lines.append((tag, [grp.split() for grp in body.split("|")]))
    return key, lines


def readings(key, lines):
    """One cipherkit Reading per glyph, in page order. Every glyph must be in key.json: a
    missing one is a transcription or key error, not an M reading."""
    missing = sorted({t for _, groups in lines for grp in groups for t in grp if t not in key})
    if missing:
        raise SystemExit(f"glyphs in transcription.txt but not in key.json: {' '.join(missing)}")
    return [r for _, groups in lines for grp in groups for r in apply_key(grp, key)]


def render(key, lines):
    """The folder's own rendering: word-signs and S values bare, every other glyph in
    parentheses, because square brackets already mean word-sign here."""
    out = []
    for tag, groups in lines:
        words = []
        for grp in groups:
            s = ""
            for r in apply_key(grp, key):
                if r.value.startswith("[") or r.grade == "S":
                    s += r.value
                else:
                    s += f"({r.value})"
            words.append(s)
        out.append(f"{tag}: " + " | ".join(words))
    return "\n".join(out) + "\n"


def grades(key, lines):
    """Grade counts over the 134 glyphs, all five CONVENTIONS grades, zeros included."""
    return counts(readings(key, lines))


def permutation_z(key, lines, n=1000, seed=0):
    """Key-shuffle null (cipherkit.controls.permutation_z_key): the dictionary-segmentation score
    of the reading under the key, against keys that shuffle the letter values among the letter
    glyphs. Word-signs ([the], [and], the person-signs) keep their values and break a chunk."""
    from cipherkit.controls import permutation_z_key
    from cipherkit.segment import Segmenter
    try:
        sc = Segmenter.from_corpus("sco")
    except Exception as e:  # corpus not fetched
        return None, f"no Scots corpus ({e.__class__.__name__}); run: python -m cipherkit.corpora fetch sco"
    values = {k: v["value"] for k, v in key.items()}
    chunks = [grp for _, groups in lines for grp in groups]

    def score(m):
        # Word-signs become "#" and break a chunk; the unread "?" is scored as a q.
        return sc.score_chunks(["".join(m[t] if len(m[t]) == 1 else "#" for t in grp).replace("?", "q") for grp in chunks])

    return permutation_z_key(score, values, chunks, n=n, seed=seed), None


def main():
    key, lines = load()
    text = render(key, lines)
    path = os.path.join(HERE, "reading.txt")
    header = "# Mechanical output of key.json over transcription.txt; \"|\" = gap on the page; [..] = word-sign; (..) = grade M or I.\n"
    if "--write" in sys.argv:
        open(path, "w").write(header + text)
        print("wrote reading.txt")
    committed = open(path).read()
    ok = committed == header + text
    print(text, end="")
    c = grades(key, lines)
    print("grades:", {g: n for g, n in sorted(c.items()) if n}, "of", sum(c.values()), "glyphs")
    if "--z" in sys.argv:
        z, note = permutation_z(key, lines)
        print("permutation z (key shuffle, cipherkit.controls.permutation_z_key):", z if z else note)
    if not ok:
        print("reading.txt is stale; run with --write", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
