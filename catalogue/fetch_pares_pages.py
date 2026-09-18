#!/usr/bin/env python3
"""Fetch the PARES description page of every remaining pre-1800 unit and record the 'Alcance y
contenido' summary. The `images` field it also records is NOT a digitisation signal: the "Ver
Imágenes" button and the thumbnail link appear on every unit. Use fetch_pares_images.py for that.

    uv run python catalogue/fetch_pares_pages.py catalogue/pares-hits.jsonl catalogue/pares-pages.jsonl
"""
import html, json, os, re, subprocess, sys, time
from rank_pares import DECIPHERED, year
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128 Safari/537.36"
rows = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8")]
todo = [r for r in rows if 0 < year(r) < 1800 and not DECIPHERED.search(r["title"])]
done = set()
if os.path.exists(sys.argv[2]):
    done = {json.loads(l)["id"] for l in open(sys.argv[2], encoding="utf-8")}
out = open(sys.argv[2], "a", encoding="utf-8")
for k, r in enumerate([r for r in todo if r["id"] not in done], 1):
    page = subprocess.run(["curl", "-sL", "-A", UA, "-b", "/tmp/pares-cookies.txt", "-c", "/tmp/pares-cookies.txt", "--max-time", "60", r["url"]], capture_output=True).stdout.decode("utf-8", errors="replace")
    text = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>|<style.*?</style>", "", page, flags=re.S))))
    m = re.search(r"Alcance y [Cc]ontenido:?\s*(.*?)(?:Nivel de [Dd]escripci|Signatura|Fecha|$)", text)
    rec = {"id": r["id"], "images": ("Ver Imágenes" in page) and bool(re.search(r"catalogo/show/\d+", page)),
           "n_images": len(set(re.findall(r"catalogo/show/\d+", page))),
           "alcance": (m.group(1).strip() if m else "")[:500],
           "lengua": (re.search(r"Lengua/[Ee]scritura:?\s*([^|]{0,60}?)\s{2}", text) or [None, ""])[1]}
    out.write(json.dumps(rec, ensure_ascii=False) + "\n"); out.flush()
    if k % 50 == 0: print(k, "/", len(todo), file=sys.stderr)
    time.sleep(0.7)
print("done", file=sys.stderr)
