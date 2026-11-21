"""Compare the key-aware transcription of doc. 192 with the two blind passes, by decoded value.

    python3 amiens-1513/blind_compare.py [--write]

A blind reader had the strips and a legend of shape names, and no key. Each blind line is decoded with key.tsv,
aligned to my line, and every sign I count as read is scored: does the blind sign, or one of its alternatives, give
the letters the reading prints at that sign? `strict` uses the blind tokens as written. `aliased` also accepts three consistent differences of naming, where the blind
readers gave another name to a shape the legend described badly: my bare 6 (a sigma-like s) against their d, G, 0
or W; my H (ll) against their t#; my Y (closed-loop y) against their 8 or V. Writes blind/agreement.json.
"""
import json
import re
import sys
from pathlib import Path

from decode import decode_all, load_key, load_rows, value

HERE = Path(__file__).resolve().parent
KEY = load_key()
ALIASES = {"6": {"d", "G", "0", "W", "6"}, "H": {"t#", "H"}, "Y": {"8", "V", "Y"}}


def alts(token):
    token = token.replace("T", "r") if token in ("T",) else token
    m = re.fullmatch(r"\{([^}]*)\}(\^.+)?", token)
    if m:
        return [a + (m.group(2) or "") for a in m.group(1).split("/")]
    return [token]


def values(token):
    out = set()
    for a in alts(token):
        if a.isdigit() and len(a) > 1:
            out.add("#" + a)
        v = value(a, KEY)
        if v:
            out.add(v.lstrip("#="))
            out.add(v)
    return out


def align(a, b, same):
    n, m = len(a), len(b)
    score = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            score[i][j] = max(score[i + 1][j + 1] + (2 if same(a[i], b[j]) else -1), score[i + 1][j] - 1, score[i][j + 1] - 1)
    i = j = 0
    pairs = []
    while i < n and j < m:
        if score[i][j] == score[i + 1][j + 1] + (2 if same(a[i], b[j]) else -1):
            pairs.append((i, j)); i += 1; j += 1
        elif score[i][j] == score[i + 1][j] - 1:
            i += 1
        else:
            j += 1
    return pairs


def main():
    from verify import read_flags
    blind = dict(load_rows("blind/recto-pass.txt") + load_rows("blind/verso-pass.txt"))
    out = {"scored": 0, "strict": 0, "aliased": 0, "no_blind_sign": 0}
    flags = read_flags()
    for label, dec in decode_all():
        mine = [(tok, v, st, fl) for (tok, v, st), fl in zip(dec, flags[label])]
        b = blind[label]

        def strict(x, y):
            sign = alts(x[0])[0]
            return bool({x[1], x[1].lstrip("#=")} & values(y))

        def aliased(x, y):
            base = alts(x[0])[0]
            return strict(x, y) or any(set(alts(y)) & names for mine_name, names in ALIASES.items() if base == mine_name)

        paired = dict(align(mine, b, aliased))
        for i, x in enumerate(mine):
            if not x[3]:
                continue
            out["scored"] += 1
            if i not in paired:
                out["no_blind_sign"] += 1
                continue
            y = b[paired[i]]
            out["strict"] += strict(x, y)
            out["aliased"] += aliased(x, y)
    out["strict_share"] = round(out["strict"] / out["scored"], 3)
    out["aliased_share"] = round(out["aliased"] / out["scored"], 3)
    text = json.dumps(out, indent=1) + "\n"
    path = HERE / "blind" / "agreement.json"
    if "--write" in sys.argv:
        path.write_text(text)
    elif text != path.read_text():
        raise SystemExit("blind/agreement.json is stale: rerun blind_compare.py --write")
    print(f"blind passes: of {out['scored']} signs counted as read, {out['strict']} ({out['strict_share']:.1%}) have the same "
          f"value in the blind pass as written, {out['aliased']} ({out['aliased_share']:.1%}) allowing three naming aliases; "
          f"{out['no_blind_sign']} have no blind counterpart")


if __name__ == "__main__":
    main()
