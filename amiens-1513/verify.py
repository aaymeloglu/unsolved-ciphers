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

from decode import decode_all, load_key

HERE = Path(__file__).resolve().parent
KEY = load_key()


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
    open_run = False
    counts = {"tokens": 0, "read": 0, "read_key": 0, "read_alt": 0, "read_repair": 0, "unread": 0, "struck": 0}
    for label, dec in decoded:
        want = fold("".join(v for _, v, _ in dec))
        got = strip_reading(reading[label])
        if want != got:
            bad += 1
            print(f"MISMATCH {label}\n  decode : {want}\n  reading: {got}")
            continue
        # Walk the reading and the tokens together to mark which tokens fall inside ‹..›.
        text = re.sub(r"\[[^\]]*\]", "", reading[label])
        text = re.sub(r"\.(\d+)\.", r"#\1", text)
        text = re.sub(r"(?<![#\d])(\d+)", r"=\1", text)
        flags = []
        for ch in unicodedata.normalize("NFD", text.casefold()):
            if ch == "‹":
                open_run = True
            elif ch == "›":
                open_run = False
            elif re.match(r"[a-z0-9?#=]", ch):
                flags.append(open_run)
        pos = 0
        for token, v, status in dec:
            counts["tokens"] += 1
            if status == "del" or not v:
                counts["struck"] += 1
                continue
            n = len(fold(v))
            unread = any(flags[pos:pos + n]) or status == "open"
            pos += n
            if unread:
                counts["unread"] += 1
            else:
                counts["read"] += 1
                counts["read_" + {"key": "key", "alt": "alt", "repair": "repair"}[status]] += 1
    if bad:
        raise SystemExit(f"{bad} rows of 192-reading.txt do not follow from the transcription")
    signs = counts["tokens"] - counts["struck"]
    counts["read_share"] = round(counts["read"] / signs, 3)
    text = json.dumps(counts, indent=1) + "\n"
    if "--write" in sys.argv:
        (HERE / "counts.json").write_text(text)
    elif text != (HERE / "counts.json").read_text():
        raise SystemExit("counts.json is stale: rerun verify.py --write")
    print(f"doc. 192: {signs} signs, {counts['read']} read ({counts['read_share']:.1%}): "
          f"{counts['read_key']} by the key as transcribed, {counts['read_alt']} at a doubtful sign, "
          f"{counts['read_repair']} repaired; {counts['unread']} unread; {counts['struck']} struck")


if __name__ == "__main__":
    main()
