#!/usr/bin/env python3
"""Sweep PARES (Portal de Archivos Españoles) for units described as ciphered letters.

    uv run python catalogue/fetch_pares.py catalogue/pares-hits.jsonl

Runs the catalogue text search for several phrases, follows the displaytag pagination, and
records one JSON line per unit: id, title, archive, dates, signatura, whether PARES marks it
"Digitalizado Completamente", and the query that found it. Throttled to one page a second.
The text search matches unit descriptions, so a hit means the archivist wrote "cifrada" or
similar somewhere in the description; whether a decipherment accompanies the letter is a
question for the description page, which this script does not fetch.
"""
import html
import json
import re
import subprocess
import sys
import time
import urllib.parse

BASE = "https://pares.cultura.gob.es/ParesBusquedas20/catalogo/"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128 Safari/537.36"
QUERIES = ['"carta cifrada"', '"cartas cifradas"', '"en cifra"', "cifrada", "cifradas", "descifrada", '"papel cifrado"', '"carta en cifra"']
ROW = re.compile(r'<tr class="(?:odd|even)">(.*?)</tr>', re.S)


def get(url: str, jar: dict) -> str:
    """Through curl: pares.cultura.gob.es serves an incomplete certificate chain that Python's
    ssl rejects and macOS curl completes from the Keychain."""
    cookies = jar.setdefault("file", "/tmp/pares-cookies.txt")
    out = subprocess.run(["curl", "-sL", "-A", UA, "-b", cookies, "-c", cookies, "--max-time", "60", url],
                         capture_output=True, check=True)
    return out.stdout.decode("utf-8", errors="replace")


def parse_rows(page: str):
    for row in ROW.findall(page):
        m = re.search(r'description/(\d+)\?nm">(.*?)</a>', row, re.S)
        if not m:
            continue
        rid, title = m.group(1), html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(2)))).strip()
        field = lambda cls: (re.search(r'class="%s">.*?</em>(.*?)</p>' % cls, row, re.S) or [None, ""])[1]
        yield {
            "id": rid, "title": title,
            "archive": html.unescape(re.sub(r"<[^>]+>", "", field("tipo_archivo"))).strip(),
            "dates": html.unescape(re.sub(r"<[^>]+>", "", field("fecha"))).strip(),
            "signatura": html.unescape(re.sub(r"<[^>]+>", "", field("signatura"))).strip(),
            "digitized": "Digitalizado Completamente" in row,
            "url": "https://pares.cultura.gob.es/ParesBusquedas20/catalogo/description/" + rid,
        }


def main(out_path: str) -> None:
    jar = {}
    seen = set()
    out = open(out_path, "w", encoding="utf-8")
    for q in QUERIES:
        url = BASE + "find?nm=&texto=" + urllib.parse.quote(q)
        page = get(url, jar)
        banner = re.search(r'class="pagebanner nResul">(.*?)</div>', page, re.S)
        total = re.search(r"de\s+([\d.]+)", re.sub(r"<[^>]+>", "", banner.group(1))) if banner else None
        total = int(total.group(1).replace(".", "")) if total else 0
        tag = re.search(r"d-(\d+)-p=2", page)
        n_pages = max(1, -(-total // 25))
        print(f"{q}: {total} results, {n_pages} pages", file=sys.stderr)
        for p in range(1, n_pages + 1):
            if p > 1:
                if not tag:
                    break
                page = get(BASE + "SearchController.do?texto=" + urllib.parse.quote(q) + f"&d-{tag.group(1)}-p={p}&nm=", jar)
                time.sleep(1.0)
            for rec in parse_rows(page):
                if rec["id"] in seen:
                    continue
                seen.add(rec["id"])
                rec["query"] = q
                out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            out.flush()
        time.sleep(1.0)
    print(f"{len(seen)} distinct units", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1])
