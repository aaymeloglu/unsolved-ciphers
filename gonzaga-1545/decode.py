"""Decode the frozen transcriptions with key.tsv.

    uv run python gonzaga-1545/decode.py [page ...]        # prints the decode, writes decode/<page>.txt
    uv run python gonzaga-1545/decode.py --check           # exit 1 if a transcription differs from its frozen hash

Letters go through the reciprocal swap; doubling signs, nulls, word codes and name codes come from
key.tsv. A doubtful sign {a/b} is decoded by its first reading and shown as {x/y}. A sign or code
absent from the key is shown as <sign>. Word and name codes are shown in [brackets]; nulls are dropped.
"""
import csv
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = ["A78r", "A78v", "A79r", "B174r", "B174v", "B175r", "B175v"]


def load_key():
    key = {}
    with open(os.path.join(HERE, "key.tsv"), encoding="utf-8") as f:
        for row in csv.reader((ln for ln in f if not ln.startswith("#")), delimiter="\t"):
            if row:
                key[row[0]] = (row[1], row[2], row[4])
    return key


def join_codes(tokens):
    """`L 43`-style pairs stay separate tokens; nothing to join. Kept as a hook for notation fixes."""
    return tokens


def decode_token(tok, key):
    if tok == "|":
        return " "
    if tok == "?":
        return "?"
    if tok.startswith("{") and tok.endswith("}"):
        alts = [decode_token(t, key) for t in tok[1:-1].split("/")]
        return "{" + "/".join(alts) + "}"
    if tok in key:
        value, kind, _ = key[tok]
        if kind == "null":
            return ""
        if kind in ("word", "name"):
            return f" [{value}] "
        return value
    return f"<{tok}>"


def decode_line(line, key):
    return "".join(decode_token(t, key) for t in join_codes(line.split())).replace("  ", " ").strip()


def frozen():
    path = os.path.join(HERE, "transcription", "FROZEN.sha256")
    out = {}
    if os.path.exists(path):
        for ln in open(path):
            if ln.strip():
                h, name = ln.split()
                out[name] = h
    return out


def main(argv):
    key = load_key()
    fr = frozen()
    if "--check" in argv:
        bad = 0
        for name, h in fr.items():
            got = hashlib.sha256(open(os.path.join(HERE, "transcription", name), "rb").read()).hexdigest()
            if got != h:
                print("CHANGED", name)
                bad = 1
        print("frozen files:", len(fr), "ok" if not bad else "MISMATCH")
        return bad
    os.makedirs(os.path.join(HERE, "decode"), exist_ok=True)
    for page in [a for a in argv if not a.startswith("-")] or PAGES:
        name = f"{page}.txt"
        path = os.path.join(HERE, "transcription", name)
        if not os.path.exists(path):
            print(f"{page}: no transcription yet")
            continue
        if name not in fr:
            print(f"{page}: transcription is not frozen (not in FROZEN.sha256); refusing to decode")
            continue
        lines = [ln.rstrip("\n") for ln in open(path, encoding="utf-8") if ln.strip() and not ln.startswith("#")]
        out = [f"{page} L{n:02d}  {decode_line(ln, key)}" for n, ln in enumerate(lines, 1)]
        open(os.path.join(HERE, "decode", name), "w", encoding="utf-8").write("\n".join(out) + "\n")
        print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
