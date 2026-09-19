#!/usr/bin/env python3
"""Reproduce the Vande Perre 1653 reading from transcription.txt, key.json and repairs.json,
check it against the committed reading.txt, and print the grade counts. With --z, also the
permutation z of the key against shuffled keys (cipherkit.controls.permutation_z_key) under the
kit's Dutch corpus. Standard library plus cipherkit.

    python3 vande-perre-1653/verify.py            # check (exit 1 if reading.txt is stale)
    python3 vande-perre-1653/verify.py --write    # rewrite reading.txt
    python3 vande-perre-1653/verify.py --z        # add the key-shuffle control
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from cipherkit.grades import Reading, apply_key, counts, render, summary_line  # noqa: E402


def load():
    key = {k: v for k, v in json.load(open(os.path.join(HERE, "key.json"))).items() if not k.startswith("_")}
    lines = []
    for line in open(os.path.join(HERE, "transcription.txt")):
        if line.startswith("P"):
            tag, body = line.split(":", 1)
            lines.append((tag, body.split()))
    repairs = json.load(open(os.path.join(HERE, "repairs.json")))["repairs"]
    return key, lines, repairs


def literal(key, lines):
    """The key alone over the printed digits. Every printed symbol must be in key.json."""
    missing = sorted({t for _, toks in lines for t in toks if t not in key})
    if missing:
        raise SystemExit(f"symbols in transcription.txt but not in key.json: {' '.join(missing)}")
    return {tag: apply_key(toks, key) for tag, toks in lines}


def edited(key, lines, repairs):
    """The literal reading with each repair applied at its position, graded I."""
    out = literal(key, lines)
    toks = dict(lines)
    for r in repairs:
        i = r["pos"] - 1
        if toks[r["line"]][i] != r["printed"]:
            raise SystemExit(f"repairs.json: {r['line']} position {r['pos']} is {toks[r['line']][i]}, not {r['printed']}")
        out[r["line"]][i] = Reading(r["printed"], r["value"], "I", r["why"])
    return out


def main():
    key, lines, repairs = load()
    lit = literal(key, lines)
    ed = edited(key, lines, repairs)
    text = "".join(
        f"{tag}\n  printed: {''.join(r.value for r in lit[tag])}\n  edited:  {render(ed[tag])}\n"
        for tag, _ in lines)
    header = ("# Mechanical output of verify.py. printed: key.json over the printed digits, '?' unread.\n"
              "# edited: with repairs.json applied; (..) = M, [..] = I (a repair).\n")
    path = os.path.join(HERE, "reading.txt")
    if "--write" in sys.argv:
        open(path, "w").write(header + text)
        print("wrote reading.txt")
    print(text, end="")
    c = counts(r for rs in ed.values() for r in rs)
    print("grades (edited):", summary_line(c), "of", sum(c.values()), "symbols")
    if "--z" in sys.argv:
        from cipherkit.controls import permutation_z_key
        from cipherkit.segment import Segmenter
        sg = Segmenter.from_corpus("nl")
        values = {k: v["value"] for k, v in key.items()}
        chunks = [toks for _, toks in lines]

        def score(m):
            # Code groups and misset symbols ("?") break a chunk; "ij" is spelled out.
            return sg.score_chunks(["".join(m[t] if m[t] != "?" else "#" for t in c) for c in chunks])

        z = permutation_z_key(score, values, chunks, n=1000, seed=0)
        print("permutation z (key shuffle, printed digits, kit Dutch corpus): "
              f"z = {z['z']:.1f}, observed {z['observed']:.1f}, null mean {z['mean']:.1f} sd {z['sd']:.1f}, p = {z['p']:.4f}, n = {z['n']}")
    if not os.path.exists(path) or open(path).read() != header + text:
        print("reading.txt is stale; run with --write", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
