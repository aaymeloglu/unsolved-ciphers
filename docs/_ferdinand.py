"""Build docs/ferdinand-reading.html from the published Ferdinand editions.

One page, three letters. The 1634 partial reading is built by _ferdinand1634. Each letter is split into passages; each passage shows the cipher rows
as transcribed (left, sticky), the readable Latin (middle) and the English (right), then the
apparatus notes whose locations fall in that passage, and a fold-out table of cipher row against
literal decoder output. The key, the checks, the grades and the open points follow. Everything is
read from ferdinand-1635-1640/ at build time; nothing on the page is typed in twice.
"""
import html
import json
import re

from _ferdinand1634 import build_section as build_1634

# ---------------------------------------------------------------- markdown helpers

def inline(md):
    """Markdown inline to HTML: code, bold, italic, links; everything else escaped."""
    out, pos = [], 0
    for m in re.finditer(r"`([^`]+)`|\*\*(.+?)\*\*|\*(.+?)\*|\[([^\]]+)\]\(([^)]+)\)", md):
        out.append(html.escape(md[pos:m.start()]))
        if m.group(1) is not None:
            out.append("<code>" + html.escape(m.group(1)) + "</code>")
        elif m.group(2) is not None:
            out.append("<strong>" + html.escape(m.group(2)) + "</strong>")
        elif m.group(3) is not None:
            out.append("<em>" + html.escape(m.group(3)) + "</em>")
        else:
            out.append(f'<a href="{html.escape(m.group(5))}">{html.escape(m.group(4))}</a>')
        pos = m.end()
    out.append(html.escape(md[pos:]))
    return "".join(out)


def quoted(path, heading, end_heading):
    """The blockquote paragraphs between two headings of a reading file, as a list of HTML."""
    text = path.read_text().split(heading, 1)[1].split(end_heading, 1)[0]
    paragraphs, cur = [], []
    for line in text.splitlines() + [""]:
        if line.startswith(">"):
            part = line[1:].strip()
            if part:
                cur.append(part)
                continue
        if cur:
            paragraphs.append(inline(" ".join(cur)))
            cur = []
    assert paragraphs, (path, heading)
    return paragraphs


def table(path, heading):
    """First Markdown table after `heading`, as a list of rows of raw cell strings."""
    text = path.read_text().split(heading, 1)[1]
    rows = []
    for line in text.splitlines():
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in cells):
                continue
            rows.append(cells)
        elif rows:
            break
    return rows[1:]  # drop the header


def rows_of(path):
    out = []
    for line in path.read_text().splitlines():
        if line and not line.startswith("#"):
            label, text = line.split(" ", 1)
            out.append((label, text))
    return out


def line_no(label):
    """P1.L11 -> (1, 11); P2.C03 -> (2, 3)."""
    m = re.match(r"P(\d)\.[LC](\d+)", label)
    assert m, label
    return (int(m.group(1)), int(m.group(2)))


def in_range(label, first, last):
    return line_no(first) <= line_no(label) <= line_no(last)


def note_locations(loc):
    """Line labels named in an apparatus location cell, e.g. 'P1.L12, L19, L23; P2.L02'."""
    out, page = [], 1
    for m in re.finditer(r"(?:P(\d)\.)?([LC])(\d+)(?:[–-](\d+))?", loc):
        if m.group(1):
            page = int(m.group(1))
        out.append(f"P{page}.{m.group(2)}{int(m.group(3)):02d}")
        if m.group(4):
            out.append(f"P{page}.{m.group(2)}{int(m.group(4)):02d}")
    return out


# ---------------------------------------------------------------- page

def build(root, docs, page, crumbs, repo):
    folder = root / "ferdinand-1635-1640"
    grades = json.loads((folder / "results" / "grades.json").read_text())

    letters = [
        dict(
            year="1635", record="R1889", title="Winter quarters at Trier",
            sub="Cardinal-Infante Ferdinand to the future Ferdinand III · Brussels, 16 November 1635 · DECODE R1889, with the Latin draft R954",
            cipher=rows_of(folder / "transcriptions" / "R1889-working.txt"),
            literal=dict(rows_of(folder / "results" / "R1889-expanded-literal.txt")),
            latin=quoted(folder / "READING-1635.md", "## Readable Latin", "## English translation"),
            english=quoted(folder / "READING-1635.md", "## English translation", "## Apparatus"),
            notes=table(folder / "READING-1635.md", "## Apparatus"),
            note_cols=(1, 2, 3),  # location, evidence, treatment
            passages=[
                dict(id="saar", h="The news from the Saar", nav="Saar", first="P1.L01", last="P1.L04", latin=[0, 1], english=[0, 1],
                     hand="In clear"),
                dict(id="hiberna", h="The request for winter quarters", nav="Hiberna", first="P1.L05", last="P1.L11", latin=[2], english=[2],
                     hand="Cipher rows 5–9, clear 9–11"),
                dict(id="trier", h="Why Trier cannot take them", nav="Trier", first="P1.L11", last="P1.L26", latin=[3], english=[3],
                     hand="Cipher rows 11–26"),
                dict(id="close1635", h="The answer, and the date", nav="Close 1635", first="P1.L26", last="P2.L07", latin=[4, 5, 6], english=[4, 5],
                     hand="Cipher rows P2.2–4, clear to the end"),
            ],
            source_note="Rows from <a href='{repo}/blob/main/ferdinand-1635-1640/transcriptions/R1889-working.txt'>R1889-working.txt</a>: XZ's DECODE transcription of January 2021, checked selectively against the images, with one documented correction (row 15). Braces are clear writing, unexpanded; spaces separate cipher units; a caret marks a sign written above the line.",
        ),
        dict(
            year="1640", record="R1890", title="Recruitment in Westphalia and 100,000 florins",
            sub="Ferdinand III to Cardinal-Infante Ferdinand · Vienna, 22 February 1640 · DECODE R1890, no plaintext witness",
            cipher=rows_of(folder / "transcriptions" / "R1890-reviewed.txt"),
            literal=dict(rows_of(folder / "results" / "R1890-supplemented-reviewed-literal.txt")),
            latin=quoted(folder / "READING-1640.md", "## Readable Latin", "## English translation"),
            english=quoted(folder / "READING-1640.md", "## English translation", "## Apparatus"),
            notes=table(folder / "READING-1640.md", "## Apparatus"),
            note_cols=(0, 1, 2),
            passages=[
                dict(id="castagneti", h="What the ambassador will explain", nav="Castañeda", first="P1.C01", last="P1.C09", latin=[0, 1, 2], english=[0, 1, 2],
                     hand="Heading and salutation in clear, then cipher columns 1–9"),
                dict(id="remedy", h="A speedy remedy: counter-recruitment", nav="Remedy", first="P1.C10", last="P1.C24", latin=[3], english=[3],
                     hand="Cipher columns 10–24"),
                dict(id="florins", h="The hundred thousand florins", nav="Florins", first="P1.C24", last="P2.C13", latin=[4], english=[4],
                     hand="Cipher columns 24–P2.13"),
                dict(id="close1640", h="Closing, date and signature", nav="Close 1640", first=None, last=None, latin=[5, 6, 7], english=[5, 6, 7],
                     hand="In clear; not part of the cipher transcription"),
            ],
            source_note="Rows from <a href='{repo}/blob/main/ferdinand-1635-1640/transcriptions/R1890-reviewed.txt'>R1890-reviewed.txt</a>: XZ's DECODE transcription imported unit by unit, then sixteen documented image-review amendments (<a href='{repo}/blob/main/ferdinand-1635-1640/transcriptions/R1890-review.tsv'>R1890-review.tsv</a>). The imported stream is kept unchanged beside it.",
        ),
    ]

    def cipher_block(L, first, last):
        if first is None:
            return "<p class='fn'>The heading, salutation, closing and signature are in clear and are not part of the cipher transcription.</p>"
        ps = []
        for label, text in L["cipher"]:
            if in_range(label, first, last):
                ps.append(f"<p><span class='rn'>{html.escape(label)}</span> {html.escape(text)}</p>")
        return "<div class='rows'>" + "".join(ps) + "</div>"

    def rowtable(L, first, last):
        trs = []
        for label, text in L["cipher"]:
            if first is None or in_range(label, first, last):
                lit = L["literal"].get(label, "")
                lit = html.escape(lit).replace("⟦", "<i>⟦").replace("⟧", "⟧</i>")
                trs.append(f"<tr><td class='ln'>{html.escape(label)}</td><td class='tok'>{html.escape(text)}</td><td class='lit'>{lit}</td></tr>")
        return ("<div class='scroll'><table><thead><tr><th>Row</th><th>Cipher row as transcribed</th>"
                "<th>Literal decoder output, no repairs</th></tr></thead><tbody>" + "".join(trs) + "</tbody></table></div>")

    def notes_for(L, first, last, is_last):
        """Notes whose locations fall in the passage; notes with no parsable location go to the
        letter's last passage."""
        loc_i, ev_i, tr_i = L["note_cols"]
        items = []
        for row in L["notes"]:
            if len(row) <= tr_i:
                continue
            locs = note_locations(row[loc_i])
            if locs:
                hit = first is not None and any(in_range(x, first, last) for x in locs)
            else:
                hit = is_last
            if not hit:
                continue
            num = f"<b>{html.escape(row[0])}</b> " if L["note_cols"][0] == 1 else ""
            items.append(f"<li>{num}<span class='loc'>{inline(row[loc_i])}</span> {inline(row[ev_i])} <span class='treat'>{inline(row[tr_i])}</span></li>")
        return "".join(items)

    def section(L, p):
        latin = "".join(f"<p>{L['latin'][i]}</p>" for i in p["latin"])
        english = "".join(f"<p>{L['english'][i]}</p>" for i in p["english"])
        notes = notes_for(L, p["first"], p["last"], p is L["passages"][-1])
        span = f" (rows {p['first'][3:]}–{p['last'][3:]})" if p["first"] else ""
        return f"""
<section class="folio" id="{p['id']}">
  <header class="folio-head"><h2>{p['h']}</h2><p>{L['record']} · {p['hand']}</p></header>
  <div class="cols">
    <figure class="scan">
      {cipher_block(L, p['first'], p['last'])}
      <figcaption>{L['source_note'].format(repo=repo)}</figcaption>
    </figure>
    <div class="col it"><h3>Latin</h3>{latin}</div>
    <div class="col en"><h3>English</h3>{english}</div>
  </div>
  <div class="apparatus">{'<h4>Apparatus</h4><ul>' + notes + '</ul>' if notes else ''}
  {'' if p['first'] is None else f'<details class="groups"><summary>Cipher rows and literal output, row by row{span}</summary>{rowtable(L, p["first"], p["last"])}<p class="fn">Mechanical output of the published key files with no editorial repair. Braces are clear writing; double brackets mark a unit the key does not cover. From <a href="{repo}/tree/main/ferdinand-1635-1640/results">results/</a>.</p></details>'}
  </div>
</section>"""

    def letter_header(L):
        return f"""
<section class="wide" id="letter-{L['year']}">
  <h2>{L['title']}</h2>
  <p class="legend">{html.escape(L['sub'])}</p>
</section>"""

    # ---- key tables
    key_md = folder / "KEY.md"
    alpha = table(key_md, "# Reconstructed 1635 alphabet")
    alpha_rows = "".join(f"<tr><td class='ln'>{inline(a)}</td><td class='tok'>{inline(b)}</td></tr>" for a, b in alpha)
    fam = table(key_md, "## 1640 supplement")
    fam_rows = "".join(f"<tr><td class='tok'>{inline(a)}</td><td>{inline(b)}</td></tr>" for a, b in fam)

    g35, g40 = grades["R1889"], grades["R1890"]
    section1634 = build_1634(root, repo)
    nav = '<a href="#letter-1634">1634 · Rhine</a>' + "".join(
        f'<a href="#{p["id"]}">{p["nav"]}</a>' for L in letters for p in L["passages"]
    ) + '<a href="#key">Key</a><a href="#checks">Checks</a><a href="#open">Open</a>'

    body = f"""{crumbs.format(f'<a href="{repo}/tree/main/ferdinand-1635-1640">write-up and files</a>')}
<header class="masthead">
  <p class="eyebrow">Brussels, Algemeen Rijksarchief, Secrétairerie d'État Allemande, inv. 540 · DECODE R1887, R954, R1889, R1890 · Latin, homophonic alphabet with a syllabary</p>
  <h1>Rhine, hiberna and florins</h1>
  <p class="standfirst">Three ciphered letters between the Cardinal-Infante Ferdinand, governor of the Spanish Netherlands, and his cousin Ferdinand, King of Hungary and from 1637 Emperor. In October 1634 the King writes about a French Rhine expedition and seeks an armed diversion. In November 1635 the Cardinal-Infante declines to let the imperial army winter in Trier. In February 1640 the Emperor asks him for a hundred thousand florins to raise troops against the Elector of Cologne's levies in Westphalia. The 1634 letter has a separate, partly reconstructed cipher. The later two are read with an alphabet recovered from the surviving 1635 Latin draft and a contextual 1640 syllable supplement.</p>
  <span class="status">1634: substantial reading with gaps · 1635/1640: readable throughout, with local uncertainties</span>
</header>

<div class="lede">
  <div>
    <h3>What the letters say</h3>
    <p>The 1634 letter, from Stuttgart, concerns French preparations to cross the Rhine, the restoration of protected princes, and military action in the interests of the House of Austria. The names Württemberg and Durlach and several connected phrases are readable. Gaps in the construction and the request remain, so its English column summarizes recognizable content rather than offering a complete translation.</p>
    <p>The 1635 letter answers one of 14 October in which the King had asked for winter quarters for the imperial army, then advancing on the Saar, in the archbishopric and city of Trier. The Cardinal-Infante would gladly oblige, but Trier has stood under the King of Spain's protection for two hundred years and has been garrisoned by his troops whenever necessary, as when the French seized it; the garrison and the Elector, whose upkeep has hitherto come from the Spanish treasury, need the city and its surroundings. Imperial troops can only with difficulty be quartered there, and he trusts the King will take that in good part.</p>
    <p>The 1640 letter, from Vienna, says the Spanish ambassador, the Marquis of Castañeda, will explain the new levies begun in the Westphalian Circle by the Elector of Cologne and the estates, and the harm the Emperor fears from them. The only remedy is to raise a larger force there at once, so that the Circle does not fall under another's control; Count Hatzfeld has been ordered to Cologne. Lacking the money, the Emperor asks again, most urgently, that the hundred thousand florins previously requested be paid to his commissioners at Cologne, to be spent only on his express order or on Hatzfeld's assignment.</p>
    <h3>How they were read</h3>
    <p>The 1634 reading uses repeated phrases, vowel-preserving syllable families and the surrounding clear Latin. Its ending repeats in clear immediately after the cipher, giving a direct check. No external key or corresponding draft was used. Source alternatives, literal output and editorial proposals are separated in the <a href="{repo}/tree/main/ferdinand-1634">1634 edition</a>, reviewed on 23 September 2026.</p>
    <p>DECODE catalogues R954, a partly ciphered draft of the 1635 letter with its Latin in clear, beside R1889, the cipher copy. Aligning the two gave a 42-symbol alphabet from the first cipher paragraph; the next paragraph, held out, then read at 87 of 95 letter positions, while the fully assessed key and transcription give 93 of 95 in the comparison passage. The frozen-key holdout is the independent check; the 93-of-95 result includes evidence from that passage. Applied unchanged to the 1640 letter, that alphabet covers 416 of 779 units. The rest fell to a syllabary found in the 1640 text itself: sixty values in regular families (<code>pla ple pli plo plu</code> for <em>ta te ti to tu</em>, <code>41–54</code> for <em>le li lo lu na ne ni no nu ra re ri ro ru</em>), with all fifty-one assignments of the 1635 alphabet retained. Work of 18 September 2026 by a native Codex agent; everything is reproducible from the <a href="{repo}/tree/main/ferdinand-1635-1640">published files</a> with <code>python3 verify.py</code>.</p>
  </div>
  <div>
    <div class="callout">
      <h3>What is not settled</h3>
      <p>In 1634, several key values and source signs remain uncertain. Thirteen occurrences are unmapped, seven have inherited empty values, and even mapped strings sometimes require editorial changes. The 474-group inventory includes one partly clipped group. Coverage is not verified accuracy; the three proposed gap readings remain bracketed conjectures.</p>
      <p>In 1635, one sign yields <em>e</em> where four words need <em>m</em>, and a 7 yields <em>c</em> where <em>civitas</em> needs <em>a</em>. On the photograph, checked on 18 September 2026, the four <em>m</em>-position signs have the same form as the <em>e</em>-position signs and the 7s are plain 7s, so these are the copy's own inconsistencies, not two glyphs conflated in transcription; the reading marks every such place rather than switching the key. The photographed signs in <em>hiberna</em> read <code>1 11</code>; the word decodes without repair. The draft and the copy differ in wording at several points. In 1640 there is no plaintext witness at all: the reading rests on the alphabet carrying over and on the syllabary making sustained Latin sense across both pages. One sign at an obscured line end and the symbol <code>14</code> in Hatzfeld's name are unmapped; <em>igitua</em>, <em>materi</em> and <em>expredse</em> are apparent copying errors.</p>
      <p>The draft-and-copy relationship is recorded in the DECODE catalogue, and no earlier reading of either letter was found in the sources checked, but novelty is not established: the Belgian archive lists nineteenth-century copies of this correspondence that were not inspected. No historical key sheet has been recovered.</p>
    </div>
    <h3>Reading the columns</h3>
    <p class="legend">Left: the cipher rows as transcribed, braces for clear writing. Middle: the Latin, with the editor's word division, capitals and punctuation; square brackets mark a reading supplied or repaired with the draft's help, superscript numbers point to the apparatus. Right: an English translation of that Latin, restorations included. The fold-out under each passage gives the literal decoder output row by row, which is the authority for what the key actually produces. Grades per cipher unit (<a href="{repo}/blob/main/CONVENTIONS.md">C draft-derived, M contextual, I amended on review</a>) are in the checks below.</p>
  </div>
</div>

<nav class="folios" aria-label="Passages">{nav}</nav>
{section1634}
{letter_header(letters[0])}
{"".join(section(letters[0], p) for p in letters[0]["passages"])}
{letter_header(letters[1])}
{"".join(section(letters[1], p) for p in letters[1]["passages"])}

<section class="wide" id="key">
  <h2>The 1635/1640 key as reconstructed</h2>
  <div class="two">
    <div>
      <p>Transliterated glyph labels, not a facsimile of a historical key. The 1635 alphabet has two to five signs per letter; forty-two assignments were frozen from the first paragraph and nine added from the held-out and final passages with their evidence recorded. Plaintext <em>u</em> and <em>v</em> are one letter. The 1640 supplement keeps all fifty-one and adds sixty syllable values; <code>b</code> is <em>m</em> there, which bears on the 1635 <em>e</em>/<em>m</em> problem without settling it.</p>
      <div class="scroll"><table class="checks"><thead><tr><th>Plain</th><th>Cipher signs (1635)</th></tr></thead><tbody>{alpha_rows}</tbody></table></div>
    </div>
    <div>
      <p>The 1640 syllabary, by family. Unused grid cells are omitted; the four singletons in the last row are provisional.</p>
      <div class="scroll"><table class="checks"><thead><tr><th>Cipher family</th><th>Plaintext values</th></tr></thead><tbody>{fam_rows}</tbody></table></div>
      <p class="fn">From <a href="{repo}/blob/main/ferdinand-1635-1640/KEY.md">KEY.md</a>; occurrence-level evidence in <a href="{repo}/blob/main/ferdinand-1635-1640/key-evidence.tsv">key-evidence.tsv</a> and <a href="{repo}/blob/main/ferdinand-1635-1640/key-1640-evidence.tsv">key-1640-evidence.tsv</a>.</p>
    </div>
  </div>
</section>

<section class="wide" id="checks">
  <h2>Checks and grades for 1635/1640</h2>
  <div class="two">
    <div>
      <div class="scroll"><table class="checks"><thead><tr><th>Check</th><th>Result</th></tr></thead><tbody>
<tr><td>Frozen key, 1635</td><td>42 assignments from cipher rows 5–9 aligned to the draft; file hash recorded</td></tr>
<tr><td>Held-out paragraph, 1635</td><td>87 of 95 letter positions agree with the draft; 5 positions unknown, 3 mismatch (the <em>civitas</em>, <em>iam</em> and <em>praesidio</em> signs)</td></tr>
<tr><td>Final comparison passage, 1635</td><td>93 of 95 with the image-checked transcription and <code>o</code>=<em>a</em>; this uses evidence from the comparison passage, whose two remaining signs sit in securely readable words</td></tr>
<tr><td>Unchanged transfer to 1640</td><td>416 of 779 imported units read with the 1635 alphabet alone</td></tr>
<tr><td>1640 supplement</td><td>60 syllable values supplement the unchanged 1635 alphabet; 779 of 782 reviewed units covered. Coverage, not verified accuracy</td></tr>
<tr><td>Grades, 1635 (R1889)</td><td>{g35.get('C',0)} C · {g35.get('M',0)} M · {g35.get('I',0)} I</td></tr>
<tr><td>Grades, 1640 (R1890, reviewed stream)</td><td>{g40.get('C',0)} C · {g40.get('M',0)} M · {g40.get('I',0)} I</td></tr>
</tbody></table></div>
    </div>
    <div>
      <p>C means the value came from the 1635 draft alignment; it is not a claim of an independent 1640 witness. The sixty contextual 1640 values are graded M throughout, including the well-corroborated syllable families, because no matched-control cryptanalytic claim is made for them. I marks the nineteen 1640 units affected by the sixteen review amendments. Grades attach to literal units, not to the editorial restorations in the Latin.</p>
      <p>There is no matched control here in the sense of the repository's conventions: the 1635 reading is a documentary alignment, checked on held-out text, and the 1640 reading is contextual. The per-unit grade files are <a href="{repo}/blob/main/ferdinand-1635-1640/results/R1889-token-grades.tsv">R1889-token-grades.tsv</a> and <a href="{repo}/blob/main/ferdinand-1635-1640/results/R1890-token-grades.tsv">R1890-token-grades.tsv</a>; the full audit is in <a href="{repo}/blob/main/ferdinand-1635-1640/VALIDATION.md">VALIDATION.md</a>.</p>
    </div>
  </div>
</section>

<section class="wide" id="open">
  <h2>What remains open</h2>
  <div class="two">
    <div>
      <h3>1635</h3>
      <ul>
        <li>Four places where the copy writes the <em>e</em> sign for <em>m</em>, and two where it writes 7 for <em>a</em> or <em>u</em>: checked on the image, these are in the copy, not the transcription. The arc under <em>civitas</em> is unexplained.</li>
        <li>A marked <code>p</code> sign in <em>circumiacentibus</em>, apparent omissions and a doubled <em>n</em>.</li>
        <li>Wording differences between draft and copy (<em>circumvicinatibus</em> against <em>circumiacentibus</em>, <em>sumat</em> against <em>sumet</em>), and the order of the draft's late revisions.</li>
      </ul>
    </div>
    <div>
      <h3>1640, and the correspondence</h3>
      <ul>
        <li>One obscured end-of-line sign; the value of <code>14</code> in Hatzfeld's name; a few singleton syllable values; the copying errors <em>igitua</em>, <em>materi</em>, <em>expredse</em>.</li>
        <li>No independent 1640 plaintext; the countersignatures read provisionally <em>Furstenberg</em> and <em>Jo: Georgius Pucher[g?]</em>.</li>
        <li>Prior publication is unestablished. Manuscrits Divers 1151 contains nineteenth-century copies of the correspondence, catalogued as Spanish; inclusion of this Latin letter is unknown. No matching historical key sheet was found. The separate 1634 cipher has unresolved signs and syntax. A matching key or another witness could test these readings; further progress is not ruled out. See the <a href="{repo}/blob/main/ferdinand-1634/SOURCES.md">1634 source search and its limits</a>.</li>
      </ul>
    </div>
  </div>
</section>

<footer class="colophon">
  <div>
    <h3>Sources</h3>
    <p>DECODE <a href="https://de-crypt.org/decrypt-web/RecordsView/1887">R1887</a> (28 October 1634), <a href="https://de-crypt.org/decrypt-web/RecordsView/954">R954</a> (draft, 16 November 1635), <a href="https://de-crypt.org/decrypt-web/RecordsView/1889">R1889</a> (cipher copy) and <a href="https://de-crypt.org/decrypt-web/RecordsView/1890">R1890</a> (22 February 1640), Brussels, Algemeen Rijksarchief, Secrétairerie d'État Allemande inv. 540. The 1634 transcription is our own LLM-assisted collation, reviewed on 23 September 2026; source hashes and review scope are in <a href="{repo}/blob/main/ferdinand-1634/sources.json">sources.json</a>. The 1635/1640 ciphertext transcriptions are by XZ, January 2021, on the DECODE records; our working layers record normalisation and review amendments. Manuscript images were accessed with the DECODE project's permission and are not redistributed, which is why this page has no scans. <a href="{repo}/blob/main/ferdinand-1635-1640/SOURCES.md">Source and prior-publication audit</a>.</p>
  </div>
  <div>
    <h3>Files and status</h3>
    <p>The published folder <a href="{repo}/tree/main/ferdinand-1635-1640">ferdinand-1635-1640</a> holds the transcriptions, the frozen and expanded keys with their evidence, the decoder, the literal outputs, the per-unit grades, the two readings with their apparatus, and a one-command verifier. The separate <a href="{repo}/tree/main/ferdinand-1634">ferdinand-1634</a> folder holds its transcription, key, literal output, source observations, complete apparatus and portable verifier. This page is generated from both editions.</p>
    <p>The 1635/1640 bodies are read in substance, with marked restorations translated into English. The 1634 reading remains partial, with conjectures and an explicitly limited English summary. Work dated 18 September 2026 (1635/1640) and 23 September 2026 (1634).</p>
  </div>
</footer>"""
    (docs / "ferdinand-reading.html").write_text(page(
        "Rhine, hiberna and florins",
        "Three ciphered Latin letters between the Cardinal-Infante Ferdinand and Ferdinand III, 1634, 1635 and 1640: cipher rows, Latin, English, the reconstructed key, checks, grades and what remains open.",
        body))
