"""Resolve look-alike signs in a frozen transcription with an Italian character model.

    uv run python gonzaga-1545/resolve.py PAGE [PAGE ...]     # writes resolved/<page>.txt and .changes.tsv
    uv run python gonzaga-1545/resolve.py --file sib102_transcription.txt --name sib102

The transcriptions are made by shape, and in this hand a few pairs of signs cannot be told apart
reliably by shape (glyphs.md): d/y, c/e, a/n, g/z/q, the long-stem h against f + n or f + r, and a
few rarer ones. This script does not touch the frozen transcription. It builds, for each sign, the
set {sign as transcribed} + {its look-alikes}, charges a fixed penalty for every departure from the
transcription, and takes the path through the page that an order-5 Italian character model scores
best (beam search over the decoded letters). Readers' own doubt marks `{a/b}` are alternatives at a
small penalty. Every departure is written to the changes file with its class, so the count of
signs settled by sense, not by shape, is exact and can be reproduced.

The model is cipherkit's `it` corpus (Venetian relazioni and despatches of the 16th century).
"""
import csv
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cipherkit import corpora  # noqa: E402
from cipherkit.lm import CharLM, cached  # noqa: E402
from cipherkit.normalize import normalize  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ALPHABET = "abcdefghilmnopqrstuxyz"   # u and v are one letter in the cipher, so v is folded to u
ORDER = 5
BEAM = 400

# look-alike classes: sign -> [(alternative token sequence, class name, penalty in log10 units)]
PEN = 1.0
PEN_RARE = 1.6
PEN_DOUBT = 0.3      # the second reading of a reader's own {a/b}
CLASSES = {
    "y": [(("d",), "d/y", PEN), (("e",), "e/y", PEN_RARE), (("a",), "a/y", PEN_RARE)],
    "d": [(("y",), "d/y", PEN), (("e",), "e/d", PEN_RARE)],
    "c": [(("e",), "c/e", PEN)],
    "e": [(("c",), "c/e", PEN), (("y",), "e/y", PEN_RARE), (("d",), "e/d", PEN_RARE)],
    "a": [(("n",), "a/n", PEN), (("u",), "a/u", PEN_RARE)],
    "n": [(("a",), "a/n", PEN), (("r",), "n/r", PEN), (("u",), "n/u", PEN_RARE)],
    "r": [(("n",), "n/r", PEN), (("x",), "r/x", PEN_RARE)],
    "g": [(("z",), "g/z", PEN), (("q",), "g/q", PEN)],
    "z": [(("g",), "g/z", PEN), (("q",), "q/z", PEN_RARE)],
    "q": [(("g",), "g/q", PEN), (("z",), "q/z", PEN_RARE), (("p",), "p/q", PEN_RARE)],
    "p": [(("q",), "p/q", PEN_RARE), (("f",), "f/p", PEN_RARE)],
    "h": [(("f", "n"), "h/fn", PEN), (("f", "r"), "h/fr", PEN), (("b",), "b/h", PEN_RARE),
          (("f",), "f/h", PEN_RARE)],
    "b": [(("h",), "b/h", PEN_RARE), (("o",), "b/o", PEN_RARE)],
    "o": [(("b",), "b/o", PEN_RARE)],
    "f": [(("t",), "f/t", PEN_RARE), (("h",), "f/h", PEN_RARE), (("s",), "f/s", PEN_RARE)],
    "t": [(("f",), "f/t", PEN_RARE), (("g",), "g/t", PEN_RARE)],
    "s": [(("5",), "s/5", PEN), (("f",), "f/s", PEN_RARE)],
    "5": [(("s",), "s/5", PEN)],
    "u": [(("n",), "n/u", PEN_RARE), (("a",), "a/u", PEN_RARE)],
    "x": [(("r",), "r/x", PEN_RARE)],
    "k": [],
}
# two transcribed signs that may be one: f n / f r -> h
MERGES = {("f", "n"): (("h",), "h/fn", PEN), ("f", "r"): (("h",), "h/fr", PEN)}


def load_key():
    key = {}
    with open(os.path.join(HERE, "key.tsv"), encoding="utf-8") as f:
        for row in csv.reader((ln for ln in f if not ln.startswith("#")), delimiter="\t"):
            if row:
                key[row[0]] = (row[1], row[2])
    return key


def emit(tok, key):
    """Letters a token contributes to the letter stream, or None for a break in it (a name, a
    title, an unknown group, an unread sign)."""
    if tok in ("|",):
        return ""
    if tok not in key:
        return None
    value, kind = key[tok]
    if kind == "null":
        return ""
    if kind in ("letter", "double"):
        return value
    letters = "".join(c for c in value.lower() if c in ALPHABET)
    if kind == "word" and letters == value.lower():
        return letters
    return None


def models():
    def build(order):
        return lambda: CharLM.from_text(normalize(corpora.text("it"), alphabet=ALPHABET, folds={"v": "u", "j": "i"}), order)
    path = os.path.join(HERE, "..", "corpora", "gonzaga-it-uv-char{}.pkl")
    return (cached(path.format(ORDER), build(ORDER), CharLM.load),
            cached(path.format(ORDER - 1), build(ORDER - 1), CharLM.load))


def cond_scorer(hi, lo):
    """log10 P(letter | previous four letters), from the order-5 and order-4 counts. A context the
    corpus never shows gets the floor, so an unseen string is never preferred to a seen one."""
    cache = {}
    floor, k = -3.5, len(ALPHABET)

    def score(ctx, ch):
        key = (ctx, ch)
        v = cache.get(key)
        if v is None:
            g = (ctx + ch)[-ORDER:]
            if len(g) < ORDER:
                v = -1.3
            else:
                seen = lo.counts.get(g[:-1], 0)
                if seen == 0:
                    v = floor
                else:
                    v = max(floor, math.log10((hi.counts.get(g, 0) + 0.05) / (seen + 0.05 * k)))
            cache[key] = v
        return v
    return score


def options(tokens, i):
    """[(n tokens consumed, replacement tokens, class or None, penalty)] at position i."""
    tok = tokens[i]
    out = []
    if tok.startswith("{") and tok.endswith("}"):
        alts = [a for a in tok[1:-1].split("/") if a]
        for k, a in enumerate(alts):
            if a == "?":
                continue
            out.append((1, tuple(a.split("+")), None if k == 0 else "reader-doubt", 0.0 if k == 0 else PEN_DOUBT))
            for seq, cls, pen in CLASSES.get(a, []):
                out.append((1, seq, cls, pen + (0.0 if k == 0 else PEN_DOUBT)))
        if not out:
            out.append((1, ("?",), None, 0.0))
        return out
    out.append((1, (tok,), None, 0.0))
    for seq, cls, pen in CLASSES.get(tok, []):
        out.append((1, seq, cls, pen))
    if i + 1 < len(tokens) and (tok, tokens[i + 1]) in MERGES:
        seq, cls, pen = MERGES[(tok, tokens[i + 1])]
        out.append((2, seq, cls, pen))
    return out


def resolve(tokens, key, score):
    """Beam search. A beam entry is (total, context, back-pointer)."""
    n = len(tokens)
    beams = [dict() for _ in range(n + 1)]
    beams[0][""] = (0.0, None)
    for i in range(n):
        if not beams[i]:
            continue
        cur = sorted(beams[i].items(), key=lambda kv: -kv[1][0])[:BEAM]
        opts = options(tokens, i)
        for ctx, (tot, _) in cur:
            for used, seq, cls, pen in opts:
                s, c = tot - pen, ctx
                for t in seq:
                    e = emit(t, key)
                    if e is None:
                        c = ""
                    else:
                        for ch in e:
                            s += score(c, ch)
                            c = (c + ch)[-(ORDER - 1):]
                j = i + used
                old = beams[j].get(c)
                if old is None or s > old[0]:
                    beams[j][c] = (s, (i, ctx, used, seq, cls))
    ctx = max(beams[n], key=lambda c: beams[n][c][0])
    path, i = [], n
    while i > 0:
        _, (pi, pctx, used, seq, cls) = beams[i][ctx]
        path.append((pi, used, seq, cls))
        i, ctx = pi, pctx
    return list(reversed(path))


def run(name, lines, key, score, out_dir):
    tokens, where = [], []
    for ln_no, ln in enumerate(lines, 1):
        for k, t in enumerate(ln.split(), 1):
            tokens.append(t)
            where.append((ln_no, k))
    path = resolve(tokens, key, score)
    os.makedirs(out_dir, exist_ok=True)
    out_lines = [[] for _ in lines]
    changes = []
    for i, used, seq, cls in path:
        ln_no, k = where[i]
        orig = " ".join(tokens[i:i + used])
        out_lines[ln_no - 1].extend(seq)
        if cls is not None:
            changes.append((name, ln_no, k, orig, " ".join(seq), cls))
    with open(os.path.join(out_dir, f"{name}.txt"), "w", encoding="utf-8") as f:
        for toks in out_lines:
            f.write(" ".join(toks) + "\n")
    with open(os.path.join(out_dir, f"{name}.changes.tsv"), "w", encoding="utf-8") as f:
        f.write("page\tline\ttoken\ttranscribed\tresolved\tclass\n")
        for c in changes:
            f.write("\t".join(str(x) for x in c) + "\n")
    by = {}
    for c in changes:
        by[c[5]] = by.get(c[5], 0) + 1
    print(f"{name}: {len(tokens)} tokens, {len(changes)} resolved by the model "
          f"({len(changes) / len(tokens):.1%}): " + ", ".join(f"{k} {v}" for k, v in sorted(by.items(), key=lambda kv: -kv[1])))
    return out_lines


def main(argv):
    key = load_key()
    score = cond_scorer(*models())
    out_dir = os.path.join(HERE, "resolved")
    if "--file" in argv:
        path = argv[argv.index("--file") + 1]
        name = argv[argv.index("--name") + 1]
        lines = [ln.strip() for ln in open(os.path.join(HERE, path), encoding="utf-8")
                 if ln.strip() and not ln.startswith("#")]
        lines = [" ".join(ln.split()[1:]) if ln.split()[0].isdigit() and len(ln.split()[0]) == 2 and False else ln
                 for ln in lines]
        run(name, lines, key, score, out_dir)
        return 0
    for page in argv:
        path = os.path.join(HERE, "transcription", f"{page}.C.txt")
        lines = [ln.strip() for ln in open(path, encoding="utf-8") if ln.strip()]
        run(page, lines, key, score, out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
