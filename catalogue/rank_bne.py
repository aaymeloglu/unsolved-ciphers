#!/usr/bin/env python3
"""Classify the BNE manuscript records that mention cipher.

    uv run python catalogue/rank_bne.py catalogue/bne-records.jsonl > catalogue/bne-ranked.md

Input is the expanded Primo records from the sweep (fetched 2026-09-18 with the catalogue's
public pnxs API, manuscripts facet, queries cifra / cifrada / cifrado / descifr / "en cifra").
Three bins from the cataloguer's notes:
  deciphered   the note says the plaintext is there: "cifra sobreescrita", "cifra interlineal",
               "traducción de la cifra", "texto descifrado", "con la transcripción"
  open         "cifrada", "en cifra", "texto cifrado", "mayormente cifrada" with no such note
  key          a cipher key or a treatise on ciphers
Music tablature ("cifra de arpa", "puesto en cifra") is dropped. Nothing has been looked at
on the image; the BDH digitisation status is not in the catalogue record and must be checked
by shelfmark.
"""
import json
import re
import sys

DECIPHERED = re.compile(r"sobreescrita|sobre escrita|interlin|traducci[oó]n|descifrad|con la transcripci|texto en claro|clave de la cifra")
CIPHER = re.compile(r"cifrad|en cifra|texto cifrado|papel cifrado")
KEY = re.compile(r"contracifra|alfabetos y cifras|reglas .*descifrar|cifra, contracifra")
MUSIC = re.compile(r"arpa|vihuela|tecla|tonos|m[uú]sica|laud|órgano|organo|coplas|cuentos en cifra")


def flat(r):
    d = r.get("display", {})
    notes = " ".join(" ".join(v) if isinstance(v, list) else str(v) for k, v in d.items() if k.startswith("lds") or k in ("contents", "description", "publisher"))
    notes = re.sub(r"<[^>]+>|&bull;", " ", notes)
    return re.sub(r"\s+", " ", (r["title"] + " " + r["description"] + " " + notes)).strip()


def shelfmark(r):
    if r.get("callno"):
        return r["callno"]
    m = re.search(r"(Mss?/[\d/]+(?:\s*\(\d+\))?|MSS/[\d/]+|Res/\d+)", flat(r))
    return m.group(1) if m else ""


def main(path):
    recs = [json.loads(ln) for ln in open(path, encoding="utf-8")]
    bins = {"open": [], "deciphered": [], "key": []}
    for r in recs:
        t = flat(r)
        low = t.lower()
        if MUSIC.search(low):
            continue
        if KEY.search(low):
            bins["key"].append((r, t))
        elif CIPHER.search(low):
            bins["deciphered" if DECIPHERED.search(low) else "open"].append((r, t))
    print("# BNE: manuscript letters and keys that mention cipher\n")
    print(f"{len(recs)} records expanded; {len(bins['open'])} ciphered with no decipherment noted, "
          f"{len(bins['deciphered'])} with the plaintext noted alongside, {len(bins['key'])} keys or treatises. "
          "From the cataloguer's notes only; see `rank_bne.py`.\n")
    for name, title in (("open", "Ciphered, no decipherment noted"), ("key", "Keys and treatises"), ("deciphered", "Ciphered, plaintext noted alongside (not targets)")):
        print(f"## {title}\n")
        print("| Date | Shelfmark | Title | Cataloguer's note |")
        print("|---|---|---|---|")
        for r, t in sorted(bins[name], key=lambda x: x[0]["date"]):
            note = re.search(r"([^.;|]*(?:cifra|cifrad|descifr)[^.;|]*)", t, re.I)
            print(f"| {r['date']} | {shelfmark(r)} | [{r['title'][:90]}]({r['link']}) | {(note.group(1).strip() if note else '')[:110]} |")
        print()


if __name__ == "__main__":
    main(sys.argv[1])
