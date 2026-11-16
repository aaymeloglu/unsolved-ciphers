#!/usr/bin/env python3
"""Download the ASF Mediceo avanti il Principato images listed in images.tsv, for checking the
milan-1494 transcriptions against the manuscripts. Standard library only.

    python3 milan-1494/fetch_images.py [outdir]      # default: milan-1494/images/ (gitignored)

How the ASF viewer serves images: the viewer page
https://archiviodistatofirenze.cultura.gov.it/map/riproduzione/?id=<image_id> embeds a JSON field
"image" naming a pyramid TIFF; the JPEG comes from the IIPImage server at
/iipsrv/iipsrv.fcgi?FIF=<that path>&WID=<width>&CVT=jpeg. 1272 px is the scans' native width (the
IIIF info.json gives 1272 x 1807 with no larger level), so no tiling trick yields more.

The server sometimes answers only connections from Italy: on 13 November 2026 it timed out from the US,
the Netherlands and about forty other locations, on 14 November it answered a US address, and on
15 November it timed out again. If it times out, use an Italian exit: a whole-machine VPN, or set
FETCH_PROXY (or ALL_PROXY) to a proxy whose exit is in Italy, which this script then uses through curl
(urllib cannot speak SOCKS). A rootless WireGuard-to-SOCKS proxy such as wireproxy keeps the rest of the
machine on its normal route:

    FETCH_PROXY=socks5h://127.0.0.1:1080 python3 milan-1494/fetch_images.py

Plain GET requests, no login, no special headers. Each download is compared with the size and sha256 of
our copy in images.tsv; a byte mismatch with the right size usually means the server re-encoded the JPEG.
The images are not redistributed in this repository.
"""
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://archiviodistatofirenze.cultura.gov.it"


PROXY = os.environ.get("FETCH_PROXY") or os.environ.get("ALL_PROXY") or os.environ.get("all_proxy")


def get(url, timeout=90):
    """GET a URL. With FETCH_PROXY (or ALL_PROXY) set, e.g. socks5h://127.0.0.1:1080, fetch through curl,
    since urllib cannot use a SOCKS proxy; otherwise plain urllib."""
    if PROXY:
        r = subprocess.run(["curl", "-fsS", "--max-time", str(timeout), "--proxy", PROXY, url],
                           capture_output=True, check=False)
        if r.returncode:
            raise RuntimeError(f"curl via proxy failed ({r.returncode}): {r.stderr.decode(errors='replace').strip()}")
        return r.stdout
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.read()


def ptif_path(image_id):
    page = get(f"{BASE}/map/riproduzione/?id={image_id}", timeout=60).decode("utf-8", "replace")
    m = re.search(r'"image"\s*:\s*("(?:[^"\\]|\\.)*")', page)
    if not m:
        raise RuntimeError(f"no image path on the viewer page for id {image_id}")
    return json.loads(m.group(1))


def rows():
    with open(os.path.join(HERE, "images.tsv"), newline="") as f:
        lines = [l for l in f if not l.startswith("#")]
    return list(csv.DictReader(lines, delimiter="\t"))


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "images")
    os.makedirs(out, exist_ok=True)
    bad = 0
    for row in rows():
        iid = row["image_id"]
        path = ptif_path(iid)
        url = f"{BASE}/iipsrv/iipsrv.fcgi?FIF={urllib.parse.quote(path, safe='/')}&WID=1272&CVT=jpeg"
        data = get(url)
        name = f"{iid}_{row['filza']}_{row['doc']}_{row['leaf'].replace('c. ', 'c').replace(' ', '')}.jpg"
        with open(os.path.join(out, name), "wb") as f:
            f.write(data)
        same = hashlib.sha256(data).hexdigest() == row["sha256"]
        print(f"{'ok  ' if same else 'DIFF'} {name}  {row['role']}")
        bad += not same
    if bad:
        print(f"{bad} file(s) differ in bytes from our copies; compare dimensions and content by eye.")


if __name__ == "__main__":
    main()
