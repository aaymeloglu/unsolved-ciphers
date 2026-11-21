"""Check that the committed reading of doc. 192 follows from the transcription, the key and the repairs.

    python3 amiens-1513/verify.py

Exits non-zero if 192-reading.txt, 192-decode.txt or the counts in counts.json are stale. It checks derivation,
not palaeography: whether a sign on the page is the sign in the transcription is a separate question, and the
agreement with the blind passes (blind/) is reported for that.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

import difflib

from decode import decode_all, load_key, load_rows

HERE = Path(__file__).resolve().parent
KEY = load_key()


def key_sources():
    src = {}
    for line in (HERE / "key.tsv").read_text().splitlines():
        if line and not line.startswith("#"):
            kind, sign, _, source, *_ = line.split("\t")
            src[(kind, sign)] = source
    return src


def key_source(token, src):
    """Weakest source among the key rows used to read this token: v6, then 190/191, then 192."""
    if token.startswith("{"):
        inner, _, suffix = token[1:].partition("}")
        token = inner.split("/")[0] + suffix
    if token.strip(".").isdigit():
        n = token.strip(".")
        used = [src.get(("code", n), src.get(("number", n), "192"))]
    elif ("word", token) in src:
        used = [src[("word", token)]]
    elif "^" in token:
        base, sup = token.split("^", 1)
        used = [src.get(("base", base), "192"), src.get(("vowel", sup), "192")]
    else:
        used = [src.get(("bare", token), "192")]
    used = ["v6" if u.startswith("v6") else u for u in used]
    return max(used, key=["v6", "190/191", "192"].index)


def changed_since_first_reading():
    first = dict(load_rows("192-first-reading.txt"))
    now = dict(load_rows("192-transcription.txt"))
    n = 0
    for label, tokens in now.items():
        sm = difflib.SequenceMatcher(a=first[label], b=tokens, autojunk=False)
        n += sum(max(i2 - i1, j2 - j1) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal")
    return n


def read_flags():
    """Per line, one flag per token: True when the reading counts the sign as read."""
    reading = reading_rows()
    flags = {}
    open_run = False
    for label, dec in decode_all():
        text = re.sub(r"\[[^\]]*\]", "", reading[label])
        text = re.sub(r"\.(\d+)\.", r"#\1", text)
        text = re.sub(r"(?<![#\d])(\d+)", r"=\1", text)
        marks = []
        for ch in unicodedata.normalize("NFD", text.casefold()):
            if ch == "‹":
                open_run = True
            elif ch == "›":
                open_run = False
            elif re.match(r"[a-z0-9?#=]", ch):
                marks.append(open_run)
        pos, row = 0, []
        for token, v, status in dec:
            if status == "del" or not v:
                row.append(False)
                continue
            n = len(fold(v))
            row.append(not (any(marks[pos:pos + n]) or status == "open"))
            pos += n
        flags[label] = row
    return flags


def fold(s):
    s = unicodedata.normalize("NFD", s.casefold())
    return re.sub(r"[^a-z0-9?#=]", "", s).replace("v", "u").replace("j", "i")


def reading_rows():
    rows = {}
    for line in (HERE / "192-reading.txt").read_text().splitlines():
        if line and not line.startswith("#"):
            label, text = line.split("\t")
            rows[label] = text
    return rows


def strip_reading(text):
    """Letters the reading claims are in the cipher: drop [..], keep ‹..› contents, codes .N. as #N, figures as =N."""
    text = re.sub(r"\[[^\]]*\]", "", text)
    text = re.sub(r"\.(\d+)\.", r"#\1", text)
    text = re.sub(r"(?<![#\d])(\d+)", r"=\1", text)
    return fold(text)


def main():
    decoded = decode_all()
    labels = [f"R{i:02}" for i in range(1, 23)] + [f"V{i:02}" for i in range(1, 20)]
    if [l for l, _ in decoded] != labels:
        raise SystemExit("expected recto lines 1-22 and verso lines 1-19")
    literal = "".join(f"{l} {' '.join(v for _, v, _ in d if v)}\n" for l, d in decoded)
    if literal != (HERE / "192-decode.txt").read_text():
        raise SystemExit("192-decode.txt is stale: rerun decode.py > 192-decode.txt")
    reading = reading_rows()
    bad = 0
    for label, dec in decoded:
        want = fold("".join(v for _, v, _ in dec))
        got = strip_reading(reading[label])
        if want != got:
            bad += 1
            print(f"MISMATCH {label}\n  decode : {want}\n  reading: {got}")
    if bad:
        raise SystemExit(f"{bad} rows of 192-reading.txt do not follow from the transcription")
    src, flags = key_sources(), read_flags()
    counts = {"tokens": 0, "read": 0, "read_key_dudout": 0, "read_key_pair": 0, "read_key_this_letter": 0, "read_alt": 0,
              "read_repair": 0, "unread": 0, "struck": 0}
    for label, dec in decoded:
        for (token, v, status), ok in zip(dec, flags[label]):
            counts["tokens"] += 1
            if status == "del" or not v:
                counts["struck"] += 1
            elif not ok:
                counts["unread"] += 1
            else:
                counts["read"] += 1
                if status == "key":
                    counts[{"v6": "read_key_dudout", "190/191": "read_key_pair", "192": "read_key_this_letter"}[key_source(token, src)]] += 1
                else:
                    counts["read_" + status] += 1
    counts["changed_since_first_reading"] = changed_since_first_reading()
    signs = counts["tokens"] - counts["struck"]
    counts["read_share"] = round(counts["read"] / signs, 3)
    text = json.dumps(counts, indent=1) + "\n"
    if "--write" in sys.argv:
        (HERE / "counts.json").write_text(text)
    elif text != (HERE / "counts.json").read_text():
        raise SystemExit("counts.json is stale: rerun verify.py --write")
    print(f"doc. 192: {signs} signs, {counts['read']} read ({counts['read_share']:.1%}): "
          f"{counts['read_key_dudout']} by Dudout's values, {counts['read_key_pair']} by values from the 190/191 pair, "
          f"{counts['read_key_this_letter']} by values fixed on this letter, "
          f"{counts['read_alt']} at a doubtful sign, {counts['read_repair']} repaired; {counts['unread']} unread; "
          f"{counts['struck']} struck; {counts['changed_since_first_reading']} signs changed since the first reading")


if __name__ == "__main__":
    main()
