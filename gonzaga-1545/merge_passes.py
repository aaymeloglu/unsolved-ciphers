"""Merge two independent transcription passes of a page into a consensus with open spots.

    uv run python gonzaga-1545/merge_passes.py A79r        # writes transcription/A79r.AB.txt

Tokens both readers wrote alike stay as they are. Where one reader's doubt mark contains the
other's reading, the shared reading is taken. Where they differ the token is `{a/b}` (reader A
first); a token only one reader has is `{x/?}`. The open spots are what the third reader settles.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cipherkit.transcribe import compare, consensus, load_pass  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def main(pages):
    for page in pages:
        a = load_pass(os.path.join(HERE, "transcription", f"{page}.A.txt"))
        b = load_pass(os.path.join(HERE, "transcription", f"{page}.B.txt"))
        rows = consensus(a, b)
        with open(os.path.join(HERE, "transcription", f"{page}.AB.txt"), "w", encoding="utf-8") as f:
            for r in rows:
                f.write(" ".join(r.tokens) + "\n")
        c = compare(a, b)
        n = sum(len(r.tokens) for r in rows)
        opened = sum(1 for r in rows for t in r.tokens if t.startswith("{") or t == "?")
        print(f"{page}: {n} tokens, {opened} open ({opened / n:.1%}); "
              f"passes agree on {c['agreement_rate']:.1%} of paired tokens")


if __name__ == "__main__":
    main(sys.argv[1:])
