#!/usr/bin/env python3
"""Rank the undeciphered DECODE cipher records by how attackable they look from the catalogue.

    uv run python catalogue/rank_decode.py catalogue/decode-catalog.csv catalogue/decode-records.jsonl catalogue/exclude.txt > catalogue/decode-ranked.md

Signals, all from public metadata (no image was looked at):
  +3  a Key is attached to the record ("Available Documents: Key") and no deciphered text is
  +2  a transcription is attached
  A record with "Deciphered text" attached is already read in DECODE's own files and goes to a
  separate list at the end, whatever its status field says.
  +2  the paper is public (no login needed for the images)
  +1  inline cleartext (the letter is partly in clear, which gives cribs and syntax)
  +1  four pages or fewer
  +1  the cleartext language is recorded
  +1 per DECODE Key record from the same archive and collection dated within 20 years, up to +3
  -2  the collection is one the community has worked over (Vatican Barb.lat / Segretario di Stato)
`exclude.txt` lists record ids already on Tomokiyo's list or in cyphersolver; those are dropped.
The score is a screen, not a judgement: the leaf has not been seen.
"""
import collections
import csv
import json
import re
import sys

WORKED = ("barb.lat", "segretario di stato", "vatican")


def norm_holder(s: str) -> str:
    s = s.replace("&lsquot;", "'").replace("’", "'").lower()
    parts = [p.strip() for p in re.split(r"[,;]", s) if p.strip()]
    # CSV holders start with the city ("Brussels ,Algemeen Rijksarchief, ..."); record pages do not.
    if parts and len(parts[0].split()) <= 3 and len(parts) > 1 and not re.search(r"archiv|library|biblio|record", parts[0]):
        parts = parts[1:]
    return " / ".join(parts[:2])[:80]


def first_year(s: str):
    m = re.search(r"\b(1[3-9]\d\d)\b", s or "")
    return int(m.group(1)) if m else None


def main(csv_path, jsonl_path, exclude_path):
    rows = list(csv.DictReader(open(csv_path, encoding="utf-8")))
    keys = [(norm_holder(r["c_holder"]), first_year(r["c_cates"])) for r in rows if r["record_type"] == "Key"]
    exclude = set()
    try:
        exclude = {ln.strip() for ln in open(exclude_path, encoding="utf-8") if ln.strip().isdigit()}
    except FileNotFoundError:
        pass
    recs = [json.loads(ln) for ln in open(jsonl_path, encoding="utf-8")]
    ranked, already = [], []
    for r in recs:
        if r["id"] in exclude or "error" in r:
            continue
        holder = norm_holder(r.get("Holder", ""))
        year = first_year(r.get("Start Year", "")) or first_year(r.get("list_dates", ""))
        nearby = sum(1 for h, y in keys if h and h == holder and y and year and abs(y - year) <= 20)
        pages = r.get("No. of Pages", "")
        score = 0
        reasons = []
        docs = r.get("Available Documents", "")
        if "Deciphered text" in docs:
            already.append(r)
            continue
        if "Key" in docs:
            score += 3; reasons.append("key attached")
        if "Transcription" in docs:
            score += 2; reasons.append("transcription attached")
        if r.get("Paper Access Mode", "").startswith("Public"):
            score += 2; reasons.append("images public")
        if r.get("Inline Cleartext") == "Yes":
            score += 1; reasons.append("inline cleartext")
        if pages.isdigit() and int(pages) <= 4:
            score += 1
        if r.get("Cleartext Language", "").strip():
            score += 1
        if nearby:
            score += min(nearby, 3); reasons.append(f"{nearby} keys from the same collection within 20 years")
        if any(w in holder for w in WORKED):
            score -= 2; reasons.append("well-worked collection")
        ranked.append((score, r, holder, year, nearby, reasons))
    ranked.sort(key=lambda t: (-t[0], t[3] or 9999))

    print("# DECODE: undeciphered cipher records ranked by catalogue signals\n")
    print(f"{len(recs)} records fetched, {len(exclude)} excluded as already listed elsewhere, {len(already)} carry a "
          f"deciphered text in DECODE and are listed at the end, {len(ranked)} ranked. "
          "Scoring in `rank_decode.py`; nothing here has been looked at on the image.\n")
    print("| Score | R | Date | Holder (archive / collection) | Sender → Receiver | Lang | pp | Signals |")
    print("|---|---|---|---|---|---|---|---|")
    for score, r, holder, year, nearby, reasons in ranked[:80]:
        who = f"{r.get('Sender','')[:30]} → {r.get('Receiver','')[:30]}".strip(" →")
        print(f"| {score} | [{r['id']}](https://de-crypt.org/decrypt-web/RecordsView/{r['id']}) | {year or r.get('list_dates','')} | "
              f"{r.get('Holder','')[:70]} | {who} | {r.get('Cleartext Language','')[:12]} | {r.get('No. of Pages','')} | {'; '.join(reasons)} |")
    print("\n## By collection\n")
    by = collections.defaultdict(list)
    for t in ranked:
        by[t[2]].append(t)
    print("| Records | Best score | Nearby keys | Collection |")
    print("|---|---|---|---|")
    for holder, ts in sorted(by.items(), key=lambda kv: -len(kv[1]))[:40]:
        print(f"| {len(ts)} | {max(t[0] for t in ts)} | {max(t[4] for t in ts)} | {holder} |")
    print("\n## Already carrying a deciphered text in DECODE (not targets)\n")
    for r in sorted(already, key=lambda r: r.get("Start Year", "")):
        print(f"- R{r['id']} {r.get('Start Year','')} {r.get('Holder','')[:60]}: {r.get('Sender','')[:30]} → {r.get('Receiver','')[:30]} ({r.get('Status','')})")


if __name__ == "__main__":
    main(*sys.argv[1:4])
