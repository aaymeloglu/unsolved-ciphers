#!/usr/bin/env python3
"""Fetch the public metadata of every undeciphered or partly deciphered cipher record in DECODE.

    uv run python catalogue/fetch_decode.py decode-catalog.csv catalogue/decode-records.jsonl

The catalogue CSV is the DECODE RecordsList export (RecordsList?recperpage=ALL). Each record
page is fetched once, politely (one request every 0.4 s), and its field table is parsed into
one JSON line. No login is used: the fields, including "Private Ciphertext" and "Available
Documents", are public. Images are never fetched.
"""
import csv
import html
import json
import os
import re
import sys
import time
import urllib.request

URL = "https://de-crypt.org/decrypt-web/RecordsView/{id}"
FIELDS = [
    "Holder", "Author", "Sender", "Receiver", "Region", "Origin City", "Start Year", "Start Month",
    "Start Day", "End Year", "Record Type", "Status", "Symbol Set", "Cipher Type", "Cipher Type (notes)",
    "Symbol Sets (notes)", "No. of Pages", "Inline Cleartext", "Inline Plaintext", "Cleartext Language",
    "Plaintext Language", "Private Ciphertext", "Available Documents", "Paper Access Mode",
    "Creation Date", "Key: encoded plaintext type",
]
_TAG = re.compile(r"<[^>]+>")


def parse(page: str) -> dict:
    text = re.sub(r"<script.*?</script>|<style.*?</style>", "", page, flags=re.S)
    text = html.unescape(re.sub(r"\s+", " ", _TAG.sub(" ", text)))
    text = text.replace("&lsquot;", "'")
    start = text.find("Holder ")
    if start < 0:
        return {}
    text = text[start:]
    out = {}
    for i, f in enumerate(FIELDS):
        a = text.find(f + " ")
        if a < 0:
            continue
        a += len(f) + 1
        ends = [text.find(g + " ", a) for g in FIELDS[i + 1 :]]
        ends = [e for e in ends if e >= 0]
        b = min(ends) if ends else a + 200
        out[f] = text[a:b].strip()
    m = re.search(r"Public Notes?\s+(.*?)(?:Reference|Bibliography|Source|$)", text[:4000])
    if m:
        out["Notes"] = m.group(1).strip()[:600]
    return out


def main(csv_path: str, out_path: str) -> None:
    rows = [r for r in csv.DictReader(open(csv_path, encoding="utf-8"))
            if r["record_type"] == "Cipher" and r["status"] in ("Non-decrypted", "Partially decrypted")]
    done = set()
    if os.path.exists(out_path):
        for ln in open(out_path, encoding="utf-8"):
            done.add(json.loads(ln)["id"])
    todo = [r for r in rows if r["id"] not in done]
    print(f"{len(rows)} records, {len(done)} already fetched, {len(todo)} to go", file=sys.stderr)
    with open(out_path, "a", encoding="utf-8") as out:
        for k, r in enumerate(todo, 1):
            req = urllib.request.Request(URL.format(id=r["id"]), headers={"User-Agent": "cipherkit-catalogue/0.1"})
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    page = resp.read().decode("utf-8", errors="replace")
                rec = parse(page)
            except Exception as e:  # noqa: BLE001
                rec = {"error": str(e)}
            rec["id"] = r["id"]
            rec["list_status"] = r["status"]
            rec["list_dates"] = r["c_cates"]
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            out.flush()
            if k % 50 == 0:
                print(f"{k}/{len(todo)}", file=sys.stderr)
            time.sleep(0.4)
    print("done", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
