"""Build the Moray page from the transcription, current manuscript assessment,
Scots/English reading and evidence notes. Experimental key artifacts stay separate."""
from collections import Counter
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
    # Present the manuscript assessment, keeping every uncertain value graded M.
    # key.json/reading.txt remain reproducible experimental artifacts, not the
    # authority for the current uncertain readings. See FRESH-MANUSCRIPT-REVIEW.md.
    for label, value, evidence in [
        ("Zz", "?", "k or t; lakkis and lattis are both attested; doubled in L3 and opens L4"),
        ("t", "?", "singleton after haill e; s (es = as) or a word-sign [as] are conjectures"),
        ("x3", "n", "curved x visually favours the n-sign; uncertain allograph"),
        ("Xs", "u", "crossed x visually favours the u-sign; uncertain allograph"),
    ]:
        key[label] = dict(value=value, grade="M", **{"from": evidence})
    key["Z2"]["from"] = "to, of; the long-stroked sign at L4.5 is not securely identified with this glyph"
    key["L4.5"] = dict(value="?", grade="M", **{"from": "long-stroked z-like sign; value and relationship to Z2 unresolved"})
    assessed_lines = []
    counts = Counter()
    for tag, groups in lines:
        position, rendered = 0, []
        for group in groups:
            letters = []
            for glyph in group:
                position += 1
                item = key["L4.5"] if (tag, position) == ("L4", 5) else key[glyph]
                value = item["value"]
                counts[item["grade"]] += 1
                letters.append(value if item["grade"] == "S" or value.startswith("[") else f"({value})")
            rendered.append("".join(letters))
        assessed_lines.append(" | ".join(rendered))
    readme = (folder / "README.md").read_text()
    scots = re.search(r"Divided into words:\n\n((?:> .*\n)+)", readme).group(1)
    english = re.search(r"\n\n((?:> The allowing.*\n)(?:> .*\n)*)", readme).group(1)
    q = lambda blk: html.escape(" ".join(l[2:] for l in blk.strip().splitlines()))
    conjecture = readme.split("## The proposed ending\n", 1)[1].split("## The cipher", 1)[0]
    proposed_quotes = re.findall(r"^> (.+)$", conjecture, re.M)
    open_pts = readme.split("## Open points")[1].split("## Failure log")[0]
    items = re.findall(r"^- (.*?)(?=^- |\Z)", open_pts, re.S | re.M)

    def md(s):
        s = html.escape(s.strip().replace("\n", " "))
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        return re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)

    rows = "".join(
        f"<tr><th>{tag}</th><td class=\"ct\">{html.escape(' | '.join(' '.join(g) for g in groups))}</td>"
        f"<td>{html.escape(rd)}</td></tr>"
        for (tag, groups), rd in zip(lines, assessed_lines))
    keyrows = "".join(
        f"<tr><td><code>{html.escape(k)}</code></td><td>{html.escape(v['value'])}</td><td>{v['grade']}</td><td>{html.escape(v['from'])}</td></tr>"
        for k, v in sorted(key.items(), key=lambda kv: (kv[1]['grade'], kv[0])))
    body = f"""{crumbs.format(f'<a href="{repo}/tree/main/moray-1568">write-up and files</a>')}
<header class="masthead">
  <p class="eyebrow">Partial · ending unresolved · 18 September 2026</p>
  <h1>Regent Moray to John Wood, 13 July 1568</h1>
  <p class="standfirst">The cipher postscript of a letter from the Regent of Scotland to his secretary at Elizabeth's court, BL Add MS 32091 f. 213v (DECODE R8345), read from the page image. A simple substitution with a few homophones and word-signs, in Scots, with word spacing.</p>
</header>
<section>
  <h2>Cipher and partial reading</h2>
  <p>The reading shows the current manuscript assessment, with unresolved signs left as question marks. At L4.5 the transcribed Z2 label is uncertain and its value is left open. Glyph labels as in <code>transcription.txt</code>; <code>|</code> is a gap the scribe left; <code>[..]</code> a word-sign; <code>(..)</code> a glyph graded uncertain.</p>
  <table class="reading"><thead><tr><th></th><th>Transcription</th><th>Reading with uncertain values marked</th></tr></thead><tbody>{rows}</tbody></table>
  <blockquote>{q(scots)}</blockquote>
  <blockquote>{q(english)}</blockquote>
  <p>Mary was moved from Carlisle to Bolton on 13–15 July 1568, the date of the letter; Lord Fleming was back in Scotland in arms by 21 August. The two person-signs are read as the Queen from context only.</p>
</section>
<section>
  <h2>A proposed ending, still unproved</h2>
  <blockquote>{html.escape(proposed_quotes[0])}</blockquote>
  <blockquote>{html.escape(proposed_quotes[1])}</blockquote>
  <p>Visual comparison favours <code>?nau?is</code>. With contextual k and o assigned to the fifth sign, the literal result is <strong>knauois</strong>, not <em>knauis</em> (knows). The fifth sign differs from ordinary o-signs, but reading <em>knauis</em> requires omitting it without a demonstrated cancellation or null. Reading <em>es</em> (as) also requires an unproved value for the preceding singleton.</p>
  <p>The corpus has two genuine verb uses of <em>lattis</em>; six other hits are fragments of <em>prelattis</em> (prelates) split across lines. DOST attests both <a href="https://dsl.ac.uk/entry/dost/lat_v_2">lattis</a> and <a href="https://dsl.ac.uk/entry/dost/lak_v">lakkis</a>, as well as <a href="https://dsl.ac.uk/entry/dost/as_adv_conj">es</a> and <a href="https://dsl.ac.uk/entry/dost21033">knauis</a>; these establish possible words, not this reading.</p>
  <p>The <a href="{repo}/blob/main/moray-1568/FRESH-MANUSCRIPT-REVIEW.md">full manuscript review</a> records the glyph comparisons and alternatives, with <a href="{repo}/blob/main/moray-1568/review-evidence.json">saved OCR evidence</a> and <a href="{repo}/blob/main/moray-1568/fresh-review-results.json">reproducible conditional readings</a>. The <a href="{repo}/blob/main/moray-1568/ONLINE-SOURCES.md">archive search</a> found no matching key or additional same-key ciphertext. NRAS217 Box 45 is a specific location lead whose relevance remains unproved.</p>
</section>
<section>
  <h2>Glyph values and uncertainties</h2>
  <p>The displayed reading has {counts['S']} of 134 glyphs S (cryptanalytic assignments), {counts['M']} M (uncertain), and {counts['I']} I (inferred). L4.5 is graded uncertain because its identity as an o-sign is unproved. Statistical controls for the cryptanalytic reconstruction are documented in the <a href="{repo}/blob/main/moray-1568/README.md#method-and-what-the-controls-say">method notes</a>; they do not resolve the handwriting or establish the conjectural ending. No matching key or contemporary decipherment has been identified. The John Wood → Cecil line on the decipherer's specimen sheet Add MS 4136 f. 33 uses the same glyph repertoire in a different key.</p>
  <table class="key"><thead><tr><th>Glyph</th><th>Value</th><th>Grade</th><th>Evidence and qualifications</th></tr></thead><tbody>{keyrows}</tbody></table>
</section>
<section>
  <h2>Open points</h2>
  <ul>{''.join(f'<li>{md(i)}</li>' for i in items)}</ul>
</section>
<section>
  <h2>Sources and files</h2>
  <p>British Library, Add MS 32091 ff. 213–214 (images not public domain, not redistributed). DECODE <a href="https://de-crypt.org/decrypt-web/RecordsView/8345">R8345</a>. Satoshi Tomokiyo, <a href="https://cryptiana.web.fc2.com/code/unsolved.htm">Unsolved Historical Ciphers</a>, "Moray-Wood Cipher (1568)". Joseph Bain, <em>Calendar of the State Papers relating to Scotland and Mary, Queen of Scots</em>, vol. ii (1900), for the Wood → Cecil crib (no. 804) and Fleming's movements (no. 775). This page is generated from <code>transcription.txt</code>, <code>key.json</code>, <code>README.md</code> and the manuscript assessment in <code>FRESH-MANUSCRIPT-REVIEW.md</code> in the <a href="{repo}/tree/main/moray-1568">repository</a>, where the README has the method, the controls and the failure log.</p>
</section>"""
    (docs / "moray-reading.html").write_text(page(
        "Moray to Wood, 1568",
        "The cipher postscript of Regent Moray's letter to John Wood, 13 July 1568, read from the page image: the Queen's stay at Carlisle and the sending home of Lord Fleming have done great evil.",
        body))
