"""Check the reading table in README.md against edition/*.it.txt, and count what is read.

    uv run python gonzaga-1545/check_readme.py [-v]

The Italian column must be the edition's letters in order. It may differ only in word division,
capitals, punctuation and apostrophes; code words lose their brackets. An ellipsis, a bracketed
gloss ending in a question mark, and a bare code such as [L30] or [63] stand for a run of the
edition that is not read. Everything in the edition that falls in such a run is counted as unread.
The coverage table counts each multiword code as one unit. An expansion inferred from context
stays in the doubtful column. Exit 1 on a text mismatch or a stale coverage table.
"""
import os
import re
import sys

from decode import load_key

HERE = os.path.dirname(os.path.abspath(__file__))
LETTERS = {"A": ["A78r", "A78v", "A79r"], "B": ["B174r", "B174v", "B175r", "B175v"]}


def edition_words(pages):
    text = " ".join(open(os.path.join(HERE, "edition", f"{p}.it.txt"), encoding="utf-8").read().replace("\n", " ") for p in pages)
    text = re.sub(r"-\s+", "", text)
    # A single code may expand to a title with spaces, including inside an alternative.
    # Count it once in both the numerator and denominator.
    return re.findall(r"(?:\{[^}]*\}|\[[^\]]*\]|[^\s{\[])+", text)


def letters(s):
    return re.sub(r"[^a-z]", "", s.lower())


def table_cells(readme, heading):
    part = readme.split(heading, 1)[1]
    part = re.split(r"\n#{2,3} ", part, maxsplit=1)[0]
    return [ln.split("|")[2].strip() for ln in part.splitlines() if ln.startswith("| ") and not ln.startswith("| Page") and not ln.startswith("|---")]


def main(verbose):
    readme = open(os.path.join(HERE, "README.md"), encoding="utf-8").read()
    inferred = {f"[{value}]" for value, _, confidence in load_key().values() if confidence == "inferred"}
    ok, totals = True, []
    for name, pages in LETTERS.items():
        words = edition_words(pages)
        stream, owner = "", []                      # edition letters, and the word each belongs to
        for i, w in enumerate(words):
            body = re.sub(r"\{[^}]*\}|<[^>]*>|\?", "#", w.lower())   # a doubt, an unvalued group, an unread sign
            body = re.sub(r"[^a-z#]", "", body)
            stream += body
            owner += [i] * len(body)
        italian = " ".join(table_cells(readme, f"### Letter {name}"))
        gap = r"…|\[[^\]]*\?\]|\[L\d+\]|\[\d+\]"
        segments = [letters(s) for s in re.split(gap, italian)]
        pos, hit = 0, [False] * len(stream)
        for seg in segments:
            if not seg:
                continue
            at = stream.find(seg, pos)
            if at < 0:
                ok = False
                print(f"letter {name}: not in the edition: {seg[:90]!r}\n   edition from here: {stream[pos:pos + 90]!r}")
                continue
            hit[at:at + len(seg)] = [True] * len(seg)
            pos = at + len(seg)
        status = []
        for i, w in enumerate(words):
            mine = [k for k, o in enumerate(owner) if o == i]
            covered = all(hit[k] for k in mine if stream[k] != "#")
            if not covered:
                status.append("unread")
            elif w in inferred or any(stream[k] == "#" for k in mine):
                status.append("doubt")
            elif re.search(r"\w\[\w+\]|\[\w+\]\w", w):
                status.append("supplied")
            else:
                status.append("read")
        count = {k: status.count(k) for k in ("read", "supplied", "doubt", "unread")}
        totals.append(count | {"words": len(words)})
        print(f"letter {name}: {len(words)} words: {count['read']} read as written, {count['supplied']} with a supplied letter, "
              f"{count['doubt']} with a doubtful sign or inferred code, {count['unread']} not read")
        if verbose:
            for k in ("unread", "doubt", "supplied"):
                print(f"   {k}:", " ".join(w for w, st in zip(words, status) if st == k))
    n = sum(t["words"] for t in totals)
    parts = {k: sum(t[k] for t in totals) for k in ("read", "supplied", "doubt", "unread")}
    print(f"both: {n} words: " + ", ".join(f"{v} {k} ({v / n:.1%})" for k, v in parts.items()))
    # Compare the displayed totals as well as the reading. Rounding alone can put a
    # document on the wrong side of a per-document threshold.
    for label, tally in zip(("A, 4 May", "B, 9 January", "Both"), [*totals, parts | {"words": n}]):
        values = [f"{tally['read']:,} ({tally['read'] / tally['words']:.2%})",
                  *(f"{tally[k]:,}" for k in ("supplied", "doubt", "unread", "words"))]
        row = "| " + " | ".join([label, *values]) + " |"
        if row not in readme.splitlines():
            ok = False
            print(f"coverage table differs for {label}: expected {row}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main("-v" in sys.argv))
