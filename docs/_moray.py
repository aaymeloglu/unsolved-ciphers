"""Build docs/moray-reading.html from moray-1568/: the four cipher lines as transcribed, the
mechanical reading, the Scots divided into words and the English, then the key and the open
points, all read from the folder at build time."""
import html
import json
import re


def build(root, docs, page, crumbs, repo):
    folder = root / "moray-1568"
    key = {k: v for k, v in json.loads((folder / "key.json").read_text()).items() if not k.startswith("_")}
    lines = []
    for line in (folder / "transcription.txt").read_text().splitlines():
        if line.startswith("L"):
            tag, body = line.split(":", 1)
            lines.append((tag, [g.split() for g in body.split("|")]))
    reading = [l for l in (folder / "reading.txt").read_text().splitlines() if l.startswith("L")]
    readme = (folder / "README.md").read_text()
    scots = re.search(r"Divided into words:\n\n((?:> .*\n)+)", readme).group(1)
    english = re.search(r"\n\n((?:> The allowing.*\n)(?:> .*\n)*)", readme).group(1)
    q = lambda blk: html.escape(" ".join(l[2:] for l in blk.strip().splitlines()))
    open_pts = readme.split("## Open points")[1].split("## Failure log")[0]
    items = re.findall(r"^- (.*?)(?=^- |\Z)", open_pts, re.S | re.M)

    def md(s):
        s = html.escape(s.strip().replace("\n", " "))
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        return re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)

    rows = "".join(
        f"<tr><th>{tag}</th><td class=\"ct\">{html.escape(' | '.join(' '.join(g) for g in groups))}</td>"
        f"<td>{html.escape(rd.split(':',1)[1].strip())}</td></tr>"
        for (tag, groups), rd in zip(lines, reading))
    keyrows = "".join(
        f"<tr><td><code>{html.escape(k)}</code></td><td>{html.escape(v['value'])}</td><td>{v['grade']}</td><td>{html.escape(v['from'])}</td></tr>"
        for k, v in sorted(key.items(), key=lambda kv: (kv[1]['grade'], kv[0])))
    body = f"""{crumbs.format(f'<a href="{repo}/tree/main/moray-1568">write-up and files</a>')}
<header class="masthead">
  <p class="eyebrow">Substantially read · 18 September 2026</p>
  <h1>Regent Moray to John Wood, 13 July 1568</h1>
  <p class="standfirst">The cipher postscript of a letter from the Regent of Scotland to his secretary at Elizabeth's court, BL Add MS 32091 f. 213v (DECODE R8345), read from the page image. A simple substitution with a few homophones and word-signs, in Scots, with word spacing.</p>
</header>
<section>
  <h2>Cipher and reading</h2>
  <p>Glyph labels as in <code>transcription.txt</code>; <code>|</code> is a gap the scribe left; <code>[..]</code> a word-sign; <code>(..)</code> a glyph graded uncertain.</p>
  <table class="reading"><thead><tr><th></th><th>Transcription</th><th>Mechanical reading</th></tr></thead><tbody>{rows}</tbody></table>
  <blockquote>{q(scots)}</blockquote>
  <blockquote>{q(english)}</blockquote>
  <p>Mary was moved from Carlisle to Bolton on 13–15 July 1568, the date of the letter; Lord Fleming was back in Scotland in arms by 21 August. The two person-signs are read as the Queen from context only.</p>
</section>
<section>
  <h2>Key</h2>
  <p>119 of 134 glyphs S (cryptanalysis; permutation z = 17.3 against 1,000 shuffled keys with cipherkit's Scots corpus), 14 M, 1 I. No key or contemporary decipherment is known. The John Wood → Cecil line on the decipherer's specimen sheet Add MS 4136 f. 33 uses the same glyph repertoire in a different key.</p>
  <table class="key"><thead><tr><th>Glyph</th><th>Value</th><th>Grade</th><th>Fixed by</th></tr></thead><tbody>{keyrows}</tbody></table>
</section>
<section>
  <h2>Open points</h2>
  <ul>{''.join(f'<li>{md(i)}</li>' for i in items)}</ul>
</section>
<section>
  <h2>Sources and files</h2>
  <p>British Library, Add MS 32091 ff. 213–214 (images not public domain, not redistributed). DECODE <a href="https://de-crypt.org/decrypt-web/RecordsView/8345">R8345</a>. Satoshi Tomokiyo, <a href="https://cryptiana.web.fc2.com/code/unsolved.htm">Unsolved Historical Ciphers</a>, "Moray-Wood Cipher (1568)". Joseph Bain, <em>Calendar of the State Papers relating to Scotland and Mary, Queen of Scots</em>, vol. ii (1900), for the Wood → Cecil crib (no. 804) and Fleming's movements (no. 775). This page is generated from <code>transcription.txt</code>, <code>key.json</code>, <code>reading.txt</code> and <code>README.md</code> in the <a href="{repo}/tree/main/moray-1568">repository</a>, where the README has the method, the controls and the failure log.</p>
</section>"""
    (docs / "moray-reading.html").write_text(page(
        "Moray to Wood, 1568",
        "The cipher postscript of Regent Moray's letter to John Wood, 13 July 1568, read from the page image: the Queen's stay at Carlisle and the sending home of Lord Fleming have done great evil.",
        body))
