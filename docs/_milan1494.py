"""Build the Ridolfi and Alamanni pages (milan-1494/) from the transcriptions, the generated
reading.txt, key.json and the two reading files. Grades and tiers come from verify.py's output,
so the pages cannot drift from the checked reading."""
import html
import json
import re

FILES = "https://github.com/aaymeloglu/unsolved-ciphers/blob/main/milan-1494/"
TIER_MARK = {"strict": "", "forced": "ᶠ", "lenient": "ˡ", "doubt": "⁇", "unread": ""}
LETTERS = {
    "ridolfi": dict(
        page="ridolfi-reading.html",
        tsv="ridolfi-transcription.tsv",
        md="ridolfi-reading.md",
        title="Ridolfi to Piero de' Medici, October 1494",
        short="Ridolfi, Milan, 1494",
        eyebrow="Partial · two groups unread · 14 November 2026",
        standfirst="Three despatches of Giovan Battista Ridolfi, Florentine envoy in Milan, to Piero de' Medici, 16, 21 and 30 October 1494 (ASF, Mediceo avanti il Principato LXXIV docs 112, 113, 115), as Charles VIII came through Lombardy and Gian Galeazzo Sforza died at Pavia. Read with the embassy's key sheet, MAP LXXII 183.",
        desc="Ridolfi's cipher despatches from Milan, October 1494, read in part with the surviving Florentine key sheet: the King at Pavia with Duchess Bona, the death of Gian Galeazzo, and Milanese opinion that Florence cannot resist.",
    ),
    "alamanni": dict(
        page="alamanni-reading.html",
        tsv="alamanni-transcription.tsv",
        md="alamanni-reading.md",
        title="Alamanni to Piero de' Medici, 26 April 1494",
        short="Alamanni, Vigevano, 1494",
        eyebrow="Partial · nine words unread · 14 November 2026",
        standfirst="A letter of Piero Alamanni, Florentine orator at Lodovico Sforza's court, to Piero de' Medici, Vigevano, 26 April 1494 (ASF, Mediceo avanti il Principato LXXIV doc. 96), with cipher passages urging the Neapolitan stroke against Genoa. Read with the same key sheet as Ridolfi's letters, MAP LXXII 183.",
        desc="Alamanni's cipher passages from Vigevano, April 1494, read in part with the surviving Florentine key sheet: the plan to turn Genoa as the one remedy, done in time and under cover.",
    ),
}


def md_inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\[([^\]]+)\]\(((?:https?://|[\w.-]+\.(?:md|json|tsv|txt|py))[^)]*)\)", lambda m: f'<a href="{m.group(2) if m.group(2).startswith("http") else FILES + m.group(2)}">{m.group(1)}</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s, flags=re.S)
    return s


def md_blocks(text):
    out = []
    for block in re.split(r"\n\s*\n", text.strip()):
        block = block.strip()
        if not block:
            continue
        if block.startswith("- "):
            items = re.split(r"\n- ", block[2:])
            out.append("<ul>" + "".join(f"<li>{md_inline(i.replace(chr(10), ' '))}</li>" for i in items) + "</ul>")
        elif block.startswith("#"):
            level = len(block) - len(block.lstrip("#"))
            out.append(f"<h{level + 1}>{md_inline(block.lstrip('#').strip())}</h{level + 1}>")
        else:
            out.append(f"<p>{md_inline(block.replace(chr(10), ' '))}</p>")
    return "\n".join(out)


def load(folder, name):
    rows = []
    for line in (folder / name).read_text().splitlines():
        if line.startswith("#") or line.startswith("id\t") or not line.strip():
            continue
        f = line.split("\t") + [""] * 8
        rows.append(dict(zip(["id", "leaf", "line", "kind", "tokens", "tier", "reading", "note"], f)))
    return rows


def generated(folder):
    """id -> (key output, editorial reading, tier, grade), per letter, from reading.txt."""
    out, letter = {}, None
    for line in (folder / "reading.txt").read_text().splitlines():
        if line.startswith("## "):
            letter = line[3:]
            out[letter] = {}
        elif line.startswith("#") or ": " in line.split("\t")[0]:
            continue
        elif letter and "\t" in line:
            i, lit, rd, tier, g = line.split("\t")
            out[letter][i] = (lit, rd, tier, g)
    return out


def summary(folder, letter):
    for line in (folder / "reading.txt").read_text().splitlines():
        if line.startswith(f"{letter}: "):
            return line
    return ""


def table(rows, gen):
    by = {}
    for r in rows:
        by.setdefault(f"{r['leaf']}:{r['line']}", []).append(r)
    trs = []
    for ln, items in by.items():
        signs, words, notes = [], [], []
        for r in items:
            if r["kind"] == "clear":
                signs.append(f'<span class="clear">[{html.escape(r["reading"])}]</span>')
                words.append(f'<span class="clear">{html.escape(r["reading"])}</span>')
                continue
            signs.append(f"<code>{html.escape(r['tokens'])}</code>")
            if r["kind"] == "null":
                continue
            lit, rd, tier, g = gen[r["id"]]
            if tier == "unread":
                words.append(f'<strong title="unread; key gives {html.escape(lit)}">[?]</strong>')
            else:
                words.append(f'<em title="key gives {html.escape(lit)}; grade {g}">{html.escape(rd)}</em>{TIER_MARK[tier]}<sub>{g}</sub>')
            if r["note"]:
                notes.append(f"<b>{html.escape(rd if tier != 'unread' else lit)}</b>: {html.escape(r['note'])}")
        trs.append(f"<tr><th>{ln}</th><td class=\"ct\">{' · '.join(signs)}</td><td>{' '.join(words)}</td><td>{'; '.join(notes)}</td></tr>")
    return "".join(trs)


def build(root, docs, page, crumbs, repo):
    folder = root / "milan-1494"
    gen = generated(folder)
    key = json.loads((folder / "key.json").read_text())["signs"]
    keyrows = "".join(
        f"<tr><td><code>{html.escape(k)}</code></td><td>{html.escape(v['shape'])}</td>"
        f"<td>{html.escape(' / '.join(x or '∅' for x in v['values']))}</td><td>{v['grade']}</td><td>{html.escape(v['basis'])}</td></tr>"
        for k, v in sorted(key.items(), key=lambda kv: ("HCSMI".index(kv[1]["grade"]), kv[0])))
    for letter, cfg in LETTERS.items():
        rows = load(folder, cfg["tsv"])
        md = (folder / cfg["md"]).read_text()
        intro = md.split("\n## ", 1)[0].split("\n", 1)[1]
        rest = "## " + md.split("\n## ", 1)[1]
        body = f"""{crumbs.format(f'<a href="{repo}/tree/main/milan-1494">write-up and files</a>')}
<header class="masthead">
  <p class="eyebrow">{cfg['eyebrow']}</p>
  <h1>{html.escape(cfg['title'])}</h1>
  <p class="standfirst">{html.escape(cfg['standfirst'])}</p>
</header>
<section>
  {md_blocks(intro)}
  <p class="legend">Counts from <code>verify.py</code>: {html.escape(summary(folder, letter))}.</p>
</section>
<section>
  {md_blocks(rest)}
</section>
<section>
  <h2>Cipher, word by word</h2>
  <p>Sign labels as in <a href="{repo}/blob/main/milan-1494/key.json">key.json</a>; <code>label=value</code> gives the value chosen for an ambiguous sign, <code>{{…}}</code> other shape readings, a trailing <code>?</code> a poorly seen sign, <code>^</code> a raised sign. Clear text in brackets. In the reading, ᶠ marks a forced word (only one choice of values gives a word), ˡ a lenient one (chosen by sense or a language model), ⁇ a doubtful one; the subscript is the grade (H key sheet, C contemporary gloss, S fitted to the text, M uncertain, I inferred). Hover a word for the literal key output.</p>
  <table class="reading"><thead><tr><th></th><th>Transcription</th><th>Reading</th><th>Notes</th></tr></thead><tbody>{table(rows, gen[letter])}</tbody></table>
</section>
<section>
  <h2>The key</h2>
  <p>The Milan embassy key sheet, ASF MAP LXXII 183 (verso endorsed "Cifra con Paulantonio Soderini"), with the signs the letters use beyond it. The grade is the provenance of the value. The <a href="{repo}/blob/main/milan-1494/README.md">write-up</a> gives the controls, the blind calibration and the open points; <a href="{repo}/blob/main/milan-1494/AUDIT.md">AUDIT.md</a> records how the reading was made and independently reviewed.</p>
  <table class="key"><thead><tr><th>Label</th><th>Shape</th><th>Values</th><th>Grade</th><th>Basis</th></tr></thead><tbody>{keyrows}</tbody></table>
</section>
<section>
  <h2>Sources</h2>
  <p>Archivio di Stato di Firenze, Mediceo avanti il Principato, online images (not redistributed here; on 13 November 2026 the server answered only from Italy, on 14 November from the US as well). Daniel Bourdeau, <a href="https://github.com/dbourdeau/cyphersolver">cyphersolver</a>, catalogue entries 2381 and 2382. This page is generated from the transcriptions, <code>reading.txt</code>, <code>key.json</code> and the reading file in the <a href="{repo}/tree/main/milan-1494">repository</a>.</p>
</section>"""
        (docs / cfg["page"]).write_text(page(cfg["short"], cfg["desc"], body))
