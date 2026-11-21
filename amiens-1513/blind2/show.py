"""Print my decode and the two second-round blind decodes side by side for the 13 re-read lines."""
import re, sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent))
from decode import load_key, load_rows, value, decode_all
KEY = load_key()
NAMES = {"s6": "6", "alpha": "α", "phi": "X", "slash0": "Ø", "T": "r"}
def one(tok):
    m = re.fullmatch(r"([^\^]+)(\^.+)?", tok)
    base, sup = m.group(1), m.group(2) or ""
    base = NAMES.get(base, base)
    if base == "Ø": return "t"
    if base.isdigit() and len(base) > 1: return base
    v = value(base + sup, KEY)
    return v if v else "<" + tok + ">"
def dec(tok):
    if tok.startswith("{"):
        inner, _, suf = tok[1:].partition("}")
        vals = []
        for a in inner.split("/"):
            vals.append(one(a + suf) if a not in ("?", "[del]") else "?")
        return "{" + "/".join(dict.fromkeys(vals)) + "}" if len(set(vals)) > 1 else vals[0]
    if tok in ("?", "[del]"): return "?"
    return one(tok)
mine = {l: " ".join(v for _, v, _ in d if v) for l, d in decode_all()}
A = dict(load_rows("blind2/passA.txt")); B = dict(load_rows("blind2/passB.txt"))
for l in "R04 R05 R06 R10 R12 V01 V04 V05 V08 V09 V10 V15 V16".split():
    print(l, "me:", mine[l]); print("    A:", " ".join(dec(t) for t in A[l])); print("    B:", " ".join(dec(t) for t in B[l])); print()
