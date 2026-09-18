#!/usr/bin/env python3
"""Sort the PARES sweep into series and flag what the descriptions already say.

    uv run python catalogue/rank_pares.py catalogue/pares-hits.jsonl catalogue/pares-exclude.txt catalogue/pares-pages.jsonl catalogue/pares-images.jsonl > catalogue/pares-ranked.md

Units dated 1800 or later are dropped. A unit whose title says "transcripción", "descifrada",
"versión descifrada" or "minuta" is a decipherment or a draft, not a target, and is counted
separately. The rest are grouped by series (archive + the signatura up to the legajo), which is
how a key found for one letter reads its neighbours. The results list marks almost nothing
"Digitalizado Completamente", but the image viewer of each unit reports its page count, and
that is the digitisation signal used here (fetch_pares_images.py).
"""
import collections
import json
import re
import sys

DECIPHERED = re.compile(r"transcripci|descifrad|versi[oó]n descifrada|minuta|traducci", re.I)
CIPHER = re.compile(r"cifrad|en cifra|cifra ", re.I)


def year(r):
    m = re.search(r"(1[3-9]\d\d)", r["dates"])
    return int(m.group(1)) if m else 0


def series(r):
    sig = r["signatura"]
    m = re.match(r"([A-ZÑ]+),(?:LEG,)?(\d+)", sig)
    return f"{r['archive']} · {m.group(1)},{m.group(2)}" if m else f"{r['archive']} · {sig.split(',')[0]}"


def main(path, exclude_path, pages_path=None, images_path=None):
    rows = [json.loads(ln) for ln in open(path, encoding="utf-8")]
    pages, images = {}, {}
    if pages_path:
        try:
            pages = {p["id"]: p for p in (json.loads(ln) for ln in open(pages_path, encoding="utf-8"))}
        except FileNotFoundError:
            pass
    if images_path:
        try:
            images = {p["id"]: p for p in (json.loads(ln) for ln in open(images_path, encoding="utf-8"))}
        except FileNotFoundError:
            pass
    for r in rows:
        pg = pages.get(r["id"])
        if pg:
            r["alcance"] = pg["alcance"]
            if DECIPHERED.search(pg["alcance"] or ""):
                r["decipher_note"] = True
        im = images.get(r["id"])
        if im and im.get("n_images") is not None:
            # The viewer's own count; the description page's "Ver Imágenes" button is on every unit.
            r["images"] = im["n_images"] > 0
            r["n_images"] = im["n_images"]
    exclude = set()
    try:
        exclude = {ln.strip() for ln in open(exclude_path, encoding="utf-8") if ln.strip() and not ln.startswith("#")}
    except FileNotFoundError:
        pass
    early = [r for r in rows if year(r) and year(r) < 1800]
    targets, deciphered = [], []
    for r in early:
        (deciphered if DECIPHERED.search(r["title"]) or r.get("decipher_note") else targets).append(r)
    known = [r for r in targets if any(x in r["signatura"] for x in exclude)]
    targets = [r for r in targets if r not in known]
    print("# PARES: units described as ciphered, before 1800\n")
    with_pages = [r for r in targets if "images" in r]
    n_img = sum(r.get("n_images", 0) for r in with_pages if r["images"])
    print(f"{len(rows)} distinct units from the text searches; {len(early)} dated before 1800; "
          f"{len(deciphered)} are transcriptions, decipherments or drafts (by title or by the description's "
          f"summary); {len(known)} already worked elsewhere (cyphersolver); {len(targets)} remain. "
          f"Image viewers checked for {len(with_pages)}: {sum(1 for r in with_pages if r['images'])} report images "
          f"({n_img:,} page images in all), against {sum(r['digitized'] for r in targets)} the results list flagged as "
          "fully digitised. No image was looked at.\n")
    print("## Series with three or more ciphered units\n")
    print("| Units | Years | Series | With images | Example |")
    print("|---|---|---|---|---|")
    by = collections.defaultdict(list)
    for r in targets:
        by[series(r)].append(r)
    for s, rs in sorted(by.items(), key=lambda kv: -len(kv[1])):
        if len(rs) < 3:
            continue
        ys = sorted(year(r) for r in rs)
        ex = min(rs, key=year)
        print(f"| {len(rs)} | {ys[0]}–{ys[-1]} | {s} | {sum(1 for r in rs if r.get('images'))} | [{ex['title'][:70]}]({ex['url']}) |")
    print("\n## Every remaining unit, by date\n")
    print("| Date | Images | Archive | Signatura | Title | Summary |")
    print("|---|---|---|---|---|---|")
    for r in sorted(targets, key=lambda r: (year(r), r["dates"])):
        img = f"{r['n_images']}" if r.get("images") else ("" if "images" in r else "?")
        print(f"| {r['dates'][:10]} | {img} | {r['archive'].replace('Archivo ', '')[:24]} | {r['signatura'][:34]} | [{r['title'][:95]}]({r['url']}) | {(r.get('alcance') or '')[:120]} |")
    print("\n## Already worked elsewhere\n")
    for r in known:
        print(f"- {r['dates'][:10]} {r['signatura']}: {r['title'][:90]}")


if __name__ == "__main__":
    main(*sys.argv[1:5])
