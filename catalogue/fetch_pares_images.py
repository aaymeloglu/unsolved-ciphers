#!/usr/bin/env python3
"""For every remaining pre-1800 PARES unit, open the image viewer page (catalogo/show/ID) and record
the image count it reports ("N imgs"). This is the reliable digitisation signal: the description
page's "Ver Imágenes" button and thumbnail link are present on every unit.

    uv run python catalogue/fetch_pares_images.py catalogue/pares-hits.jsonl catalogue/pares-images.jsonl
"""
import html, json, os, re, subprocess, sys, time
from rank_pares import DECIPHERED, year
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128 Safari/537.36"
rows = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8")]
todo = [r for r in rows if 0 < year(r) < 1800]
done = {json.loads(l)["id"] for l in open(sys.argv[2], encoding="utf-8")} if os.path.exists(sys.argv[2]) else set()
out = open(sys.argv[2], "a", encoding="utf-8")
for k, r in enumerate([r for r in todo if r["id"] not in done], 1):
    url = f"https://pares.cultura.gob.es/ParesBusquedas20/catalogo/show/{r['id']}"
    page = subprocess.run(["curl", "-sL", "-A", UA, "-b", "/tmp/pares-cookies.txt", "-c", "/tmp/pares-cookies.txt", "--max-time", "60", url], capture_output=True).stdout.decode("utf-8", errors="replace")
    text = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", "", page, flags=re.S))))
    m = re.search(r"(\d+)\s*imgs", text)
    out.write(json.dumps({"id": r["id"], "n_images": int(m.group(1)) if m else None, "bytes": len(page)}) + "\n"); out.flush()
    if k % 50 == 0: print(k, "/", len(todo), file=sys.stderr)
    time.sleep(0.6)
print("done", file=sys.stderr)
