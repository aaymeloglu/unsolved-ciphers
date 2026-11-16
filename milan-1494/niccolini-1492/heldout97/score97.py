#!/usr/bin/env python3
"""Score the frozen doc. 97 transcription against the gloss, per PREREGISTRATION-97.md (as amended before freeze).

usage: score97.py transcription-neutral.tsv reference-gloss-97.tsv [--shuffles N]

Same as held-out-114/score.py except:
- value sets come from niccolini-table.json, falling back to key.json via alias.json (what decode.py does), and the
  transcription stays in neutral labels; the transcriber's own new labels (N9..N13) are unidentified (wildcard
  that never matches);
- an illegible gloss letter '?' stays in the reference as a free position: it may align with one output character
  or with nothing at no cost, it never counts as a match, and an output character aligned to it is left out of the
  denominator. Per block: matched / max(output chars not aligned to '?', legible reference letters).
"""
import csv, json, os, random, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "..")
table = json.load(open(os.path.join(P, "niccolini-table.json")))
key = json.load(open(os.path.join(P, "..", "key.json")))["signs"]
alias = json.load(open(os.path.join(P, "alias.json")))
OWN = {"N9", "N10", "N11", "N12", "N13"}
MAP = {"N22": "S70"}


def norm(s, keep_q=False):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(ch for ch in s if (ch.isalpha() and not unicodedata.combining(ch)) or (keep_q and ch == "?"))
    return s.replace("j", "i").replace("v", "u")


def label(tok):
    tok = re.sub(r"\{.*?\}", "", tok.lstrip("^")).split("=")[0].rstrip("?") or "?"
    tok = MAP.get(tok, tok)
    return "T:" + tok if tok in OWN else tok


def vals_for(lab):
    if lab in table:
        return table[lab]["values"]
    k = alias.get(lab)
    if k and k in key:
        return key[k]["values"]
    return None


def valsets(labels):
    out = {}
    for lab in labels:
        v = vals_for(lab)
        if v is None or any(x.startswith("[") or x == "?" for x in v):
            out[lab] = "WILD"
        elif all(x == "" for x in v):
            out[lab] = None
        else:
            out[lab] = tuple(norm(x) for x in v if x != "") + (("",) if "" in v else ())
    return out


def expand(labels, vs, first_only=False):
    seq = []
    for lab in labels:
        v = vs.get(lab, "WILD")
        if v is None:
            continue
        if v == "WILD":
            seq.append(frozenset()); continue
        v = tuple(x for x in v if x != "") or ("",)
        if first_only:
            v = v[:1]
        n = max(len(x) for x in v)
        if all(len(x) == n for x in v):
            for i in range(n):
                seq.append(frozenset(x[i] for x in v))
        else:
            for ch in v[0]:
                seq.append(frozenset(ch))
    return seq


def align(seq, ref):
    """-> (matches, output chars aligned to '?'). Min cost; ties: more matches, then more wild-aligned."""
    n, m = len(seq), len(ref)
    prev = [(sum(1 for c in ref[:j] if c != "?"), 0, 0) for j in range(m + 1)]
    for i in range(1, n + 1):
        cur = [(i, 0, 0)] + [None] * m
        for j in range(1, m + 1):
            r = ref[j - 1]
            if r == "?":
                a = (prev[j - 1][0], prev[j - 1][1], prev[j - 1][2] - 1)   # output char on a '?'
                c = (cur[j - 1][0], cur[j - 1][1], cur[j - 1][2])          # '?' left empty
            else:
                hit = r in seq[i - 1]
                a = (prev[j - 1][0] + (0 if hit else 1), prev[j - 1][1] - (1 if hit else 0), prev[j - 1][2])
                c = (cur[j - 1][0] + 1, cur[j - 1][1], cur[j - 1][2])
            b = (prev[j][0] + 1, prev[j][1], prev[j][2])                   # output char unaligned
            cur[j] = min(a, b, c)
        prev = cur
    return -prev[m][1], -prev[m][2]


def agreement(blocks, refs, vs, first_only=False):
    num = den = 0
    for b, labels in blocks.items():
        seq = expand(labels, vs, first_only)
        ref = refs.get(b, "")
        mt, wild = align(seq, ref)
        num += mt
        den += max(len(seq) - wild, sum(1 for c in ref if c != "?"))
    return num / den if den else 0.0


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    n_shuf = 1000
    if "--shuffles" in sys.argv:
        n_shuf = int(sys.argv[sys.argv.index("--shuffles") + 1]); args.remove(str(n_shuf))
    blocks = {}
    for r in csv.DictReader((l for l in open(args[0]) if not l.startswith("#")), delimiter="\t"):
        if r["kind"] != "clear":
            blocks.setdefault(r["block"], []).extend(label(t) for t in r["tokens"].split())
    refs = {r["block"]: norm(r["text"], keep_q=True) for r in csv.DictReader(open(args[1]), delimiter="\t")}
    used = sorted({l for ls in blocks.values() for l in ls})
    vs = valsets(used)
    print("signs:", sum(len(v) for v in blocks.values()), "labels:", len(used),
          "wild:", [l for l in used if vs[l] == "WILD"])
    print("legible reference letters:", sum(sum(1 for c in refs.get(b, "") if c != "?") for b in blocks))
    obs = agreement(blocks, refs, vs)
    print(f"agreement (any-of rule): {obs:.4f}")
    print(f"agreement (first value only): {agreement(blocks, refs, vs, True):.4f}")
    lettered = [l for l in used if isinstance(vs.get(l), tuple)]
    rng = random.Random(1494)
    sh = []
    for _ in range(n_shuf):
        perm = lettered[:]; rng.shuffle(perm)
        vs2 = dict(vs); vs2.update({a: vs[b] for a, b in zip(lettered, perm)})
        sh.append(agreement(blocks, refs, vs2))
    print(f"shuffles: n={n_shuf} best={max(sh):.4f} mean={sum(sh)/len(sh):.4f}")
    for b in blocks:
        seq = expand(blocks[b], vs)
        print(f"\n[{b}] output ({len(seq)}):", "".join(sorted(s)[0] if len(s) == 1 else ("(" + "/".join(sorted(s)) + ")" if s else "?") for s in seq))
        print(f"[{b}] gloss  ({len(refs.get(b, ''))}):", refs.get(b, ""))


if __name__ == "__main__":
    main()
