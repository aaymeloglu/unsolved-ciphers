"""Check an edited page: the Italian must be exactly the decode of the edited cipher line, and
every departure from the frozen third-reader transcription is counted by class.

    uv run python gonzaga-1545/check_edition.py PAGE [PAGE ...]
"""
import difflib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import decode  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
PAIRS = ["d/y", "c/e", "a/n", "n/r", "n/u", "a/u", "g/z", "g/q", "q/z", "e/y", "e/d", "b/h", "b/o",
         "s/5", "f/t", "r/x", "p/q", "f/h"]


def strip_alts(tok):
    return tok[1:-1].split("/")[0] if tok.startswith("{") and tok.endswith("}") else tok


def decode_for_check(line, key):
    out = []
    for tok in line.split():
        em = tok.endswith("!") and len(tok) > 1
        t = tok[:-1] if em else tok
        d = decode.decode_token(t, key).strip()
        out.append(f"[{d}]" if em and not d.startswith("[") else d)
    return "".join(out)


def squash(s):
    return re.sub(r"[\s\-]", "", s)


def classify(old, new):
    o = [strip_alts(t) for t in old]
    n = [t.rstrip("!") if len(t) > 1 else t for t in new]
    if any(t.endswith("!") and len(t) > 1 for t in new):
        return "emendation"
    if len(o) == 1 and len(n) == 1:
        if n[0] in [a for t in old for a in (t[1:-1].split("/") if t.startswith("{") else [])]:
            return "reader-doubt"
        for p in PAIRS:
            if set(p.split("/")) == {o[0], n[0]}:
                return p
        return "other"
    if (o == ["h"] and n in (["f", "n"], ["f", "r"])) or (n == ["h"] and o in (["f", "n"], ["f", "r"])):
        return "h/f+"
    if not o:
        return "sign added"
    if not n:
        return "sign dropped"
    return "regrouped"


def main(pages):
    key = decode.load_key()
    ok = True
    total = {}
    for page in pages:
        cpath = os.path.join(HERE, "edition", f"{page}.cipher.txt")
        ipath = os.path.join(HERE, "edition", f"{page}.it.txt")
        frozen = [ln.split() for ln in open(os.path.join(HERE, "transcription", f"{page}.C.txt")) if ln.strip()]
        cipher = [ln.strip() for ln in open(cpath, encoding="utf-8") if ln.strip()]
        ital = [ln.strip() for ln in open(ipath, encoding="utf-8") if ln.strip()]
        if not (len(frozen) == len(cipher) == len(ital)):
            print(f"{page}: line counts differ: frozen {len(frozen)}, cipher {len(cipher)}, italian {len(ital)}")
            ok = False
            continue
        bad, counts, signs = 0, {}, 0
        for n, (fz, c, it) in enumerate(zip(frozen, cipher, ital), 1):
            want = squash(decode_for_check(c, key))
            got = squash(it)
            if want != got:
                bad += 1
                print(f"{page} L{n:02d} MISMATCH\n   cipher decodes: {want}\n   italian text:   {got}")
            new = c.split()
            signs += len(new)
            sm = difflib.SequenceMatcher(a=[strip_alts(t) for t in fz], b=[strip_alts(t.rstrip('!')) if len(t) > 1 else t for t in new], autojunk=False)
            for op, i1, i2, j1, j2 in sm.get_opcodes():
                if op == "equal":
                    for k in range(i2 - i1):          # a reader's doubt settled for its first reading
                        if fz[i1 + k].startswith("{") and not new[j1 + k].startswith("{"):
                            counts["reader-doubt"] = counts.get("reader-doubt", 0) + 1
                    continue
                if op == "replace" and (i2 - i1) == (j2 - j1):
                    for k in range(i2 - i1):
                        cls = classify([fz[i1 + k]], [new[j1 + k]])
                        counts[cls] = counts.get(cls, 0) + 1
                else:
                    cls = classify(fz[i1:i2], new[j1:j2])
                    counts[cls] = counts.get(cls, 0) + 1
        dep = sum(counts.values())
        print(f"{page}: {len(cipher)} lines, {signs} signs, {bad} lines where text and cipher differ; "
              f"{dep} departures from the frozen transcription ({dep / max(signs, 1):.1%}): "
              + ", ".join(f"{k} {v}" for k, v in sorted(counts.items(), key=lambda kv: -kv[1])))
        ok = ok and bad == 0
        for k, v in counts.items():
            total[k] = total.get(k, 0) + v
    if len(pages) > 1:
        print("all pages:", ", ".join(f"{k} {v}" for k, v in sorted(total.items(), key=lambda kv: -kv[1])))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
