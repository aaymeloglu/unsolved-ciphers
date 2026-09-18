#!/usr/bin/env python3
"""Build the GitHub Pages site in docs/.

Python 3, standard library only. From the repo root:

    python3 docs/_build_site.py

Writes five pages, all sharing the stylesheet of ottobon-1589/reading.html:

    index.html            the readings, with links to everything else in the repo
    ottobon-reading.html  ottobon-1589/reading.html, images pointed at the repo's raw files
    forster-reading.html  generated from forster-1644/ct.txt, mapping.json and verification.json
    starhemberg-reading.html  generated from starhemberg-1758/source-transcription.txt and two-table-output.txt
"""
import html
import json
import re
from pathlib import Path

from _ferdinand import build as build_ferdinand

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
REPO = "https://github.com/aaymeloglu/unsolved-ciphers"
RAW = "https://raw.githubusercontent.com/aaymeloglu/unsolved-ciphers/main"

OTTOBON = (ROOT / "ottobon-1589" / "reading.html").read_text()
HEAD_LINKS = re.search(r'(<link rel="preconnect".*?)<style>', OTTOBON, re.S).group(1)
STYLE = re.search(r"<style>(.*?)</style>", OTTOBON, re.S).group(1)

EXTRA_STYLE = """
.crumbs { max-width:1400px; margin:0 auto; padding-top:16px; font-size:14px; color:var(--muted); }
.cipher p { font-family:var(--mono); font-size:13.5px; line-height:1.75; margin:0 0 14px; word-spacing:.15em; }
.cipher p.clear { font-family:var(--serif); font-size:18px; font-style:italic; line-height:1.45; word-spacing:normal; }
.cipher mark, td.tok mark { background:none; color:var(--accent); font-weight:500; border-bottom:1px solid var(--accent); }
.col.it p.clear { font-style:italic; color:var(--muted); }
.keytable { min-width:0; width:100%; }
.entries { max-width:1400px; margin:0 auto; display:grid; grid-template-columns:repeat(3,1fr); gap:32px; padding-block:32px; border-bottom:1px solid var(--rule); }
.entry h2 { font-size:30px; font-style:italic; color:var(--accent); margin-bottom:4px; }
.entry .where { color:var(--muted); font-size:14px; margin:0 0 12px; }
.entry p { margin:0 0 12px; max-width:62ch; }
.entry .go { font-family:var(--serif); font-size:20px; }
.more { max-width:1400px; margin:0 auto; padding-block:28px; border-bottom:1px solid var(--rule); }
.more h3 { font-size:20px; margin-bottom:8px; }
.more ul { margin:0; padding-left:18px; max-width:90ch; }
.more li { margin-bottom:6px; }
.entry .status { display:inline-block; margin:0 0 10px; font-size:11.5px; letter-spacing:.08em; text-transform:uppercase; border:1px solid var(--accent); color:var(--accent); padding:3px 8px; border-radius:3px; }
.masthead .status { display:inline-block; margin-top:16px; font-size:12px; letter-spacing:.08em; text-transform:uppercase; border:1px solid var(--accent); color:var(--accent); padding:4px 10px; border-radius:3px; }
.rows { border:1px solid var(--rule); background:var(--surface); border-radius:2px; padding:12px 14px; font-family:var(--mono); font-size:12.5px; line-height:1.5; color:var(--ink); }
.rows p { margin:0 0 6px; word-break:break-word; }
.rows p:last-child { margin-bottom:0; }
.rows .rn { display:inline-block; min-width:2.2em; color:var(--muted); font-variant-numeric:tabular-nums; }
td.lit b { color:var(--accent); font-weight:500; }
td.lit i { color:var(--accent); }
.wide { max-width:1400px; margin:0 auto; padding-block:40px; border-bottom:1px solid var(--rule); scroll-margin-top:56px; }
.wide h2 { font-size:30px; color:var(--accent); font-style:italic; margin-bottom:18px; }
.wide .two { display:grid; grid-template-columns:1fr 1fr; gap:32px; align-items:start; }
.wide p { margin:0 0 12px; max-width:68ch; }
.wide h3 { font-size:13px; font-family:var(--sans); font-weight:600; letter-spacing:.08em; text-transform:uppercase; color:var(--muted); margin-bottom:10px; }
.wide ul { margin:0 0 14px; padding-left:18px; max-width:70ch; font-size:14.5px; }
.wide li { margin-bottom:6px; }
.checks { width:100%; font-size:14px; min-width:0; }
.checks td:first-child { white-space:nowrap; font-variant-numeric:tabular-nums; }
.checks td.ok { color:#3d6b3a; font-weight:500; white-space:nowrap; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) .checks td.ok { color:#8fc48a; } }
.repairs td.tok { white-space:nowrap; }
.wide .scroll table { min-width:0; width:100%; }
footer.colophon ul { margin:0 0 10px; padding-left:18px; }
footer.colophon li { margin-bottom:4px; }
@media screen and (max-width: 1000px) { .entries { grid-template-columns:1fr 1fr; } }
@media screen and (max-width: 680px) { .entries, .wide .two { grid-template-columns:1fr; } }
@media print { .wide { page-break-before:always; padding-block:0 12px; border-bottom:0; } .wide h2 { font-size:22px; } .rows { font-size:8.5px; } }
"""


def page(title, desc, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{HEAD_LINKS}<style>{STYLE}{EXTRA_STYLE}</style>
</head>
<body>
{body}
</body>
</html>
"""


CRUMBS = '<p class="crumbs screen-only"><a href="index.html">Unsolved ciphers</a> / {}</p>'


# ---------------------------------------------------------------- Ottobon

def ottobon_reading():
    src = OTTOBON.replace('src="pages/', f'src="{RAW}/ottobon-1589/pages/')
    src = src.replace("</style>", EXTRA_STYLE + "</style>", 1)
    crumbs = CRUMBS.format(f'<a href="{REPO}/tree/main/ottobon-1589">write-up and files</a>')
    src = src.replace('<header class="masthead">', crumbs + '\n<header class="masthead">', 1)
    (DOCS / "ottobon-reading.html").write_text(src)


# ---------------------------------------------------------------- Forster

F_FRENCH = [
    ("", "Il ny a aucun subiet de scrupule de manquer a Dieu,"),
    ("clear", "ie vous en responds et mesmes dans"),
    ("", "les reigles de perfection. Prenez s[e]ulement les voyes de prudence p[o]ur concerver votre vie, pour en faire "
         "a Dieu un plus grand sacrifi[c]e par la multiplication des vos services pour le salut de vos freres;"),
    ("clear", "et mesurer a cela sil est meilleur d'agir, ou de soubir. 13 de may 1644"),
]
F_MODERN = ("Il n'y a aucun sujet de scrupule de manquer à Dieu, je vous en réponds, et même dans les règles de perfection. "
            "Prenez seulement les voies de prudence pour conserver votre vie, pour en faire à Dieu un plus grand sacrifice par "
            "la multiplication de vos services pour le salut de vos frères ; et mesurer à cela s'il est meilleur d'agir ou de subir.")
F_ENGLISH = [
    "There is no cause for scruple about failing God, I answer to you for it, even by the rules of perfection.",
    "Only take the ways of prudence to preserve your life, so as to make of it a greater sacrifice to God through the "
    "multiplication of your services for the salvation of your brethren; and measure by that whether it is better to act or to endure.",
    "13 May 1644",
]


def forster_groups(ct):
    """Comma-delimited cipher groups, in order, with clear passages removed. Line breaks are wrapping only."""
    body = re.sub(r"\[[^\]]*\]", " ", ct)
    groups = [re.findall(r"[a-z]+|\d+", g) for g in body.replace("\n", " ").split(",")]
    return [g for g in groups if g]


def forster_reading():
    folder = ROOT / "forster-1644"
    ct = (folder / "ct.txt").read_text().strip()
    key = json.loads((folder / "mapping.json").read_text())
    ver = json.loads((folder / "verification.json").read_text())
    groups = forster_groups(ct)
    assert len(groups) == ver["groups"] and sum(map(len, groups)) == ver["tokens"], "tokenisation drifted from verification.json"
    repairs = {(m["group"], m["position_in_group"]): m for m in ver["mismatches"]}

    # Left column: the transcription as printed, clear passages set apart, repaired symbols marked.
    flagged = {m["token_position"] for m in ver["mismatches"]}
    n = 0
    left = []
    for part in re.split(r"(\[[^\]]*\])", ct):
        if not part.strip():
            continue
        if part.startswith("["):
            left.append(f'<p class="clear">{html.escape(part[1:-1])}</p>')
            continue
        out = []
        for tok in re.findall(r"[a-z]+|\d+|,|\n", part):
            if tok == "\n":
                continue
            elif tok == ",":
                out.append('<span aria-hidden="true">,</span>')
            else:
                n += 1
                out.append(f"<mark>{tok}</mark>" if n in flagged else tok)
        left.append("<p>" + " ".join(out).replace(" <span", "<span") + "</p>")
    assert n == ver["tokens"]

    rows = []
    for gi, g in enumerate(groups, 1):
        toks, lit, rd = [], [], []
        for pi, t in enumerate(g, 1):
            r = repairs.get((gi, pi))
            toks.append(f"<mark>{t}</mark>" if r else t)
            lit.append(key[t])
            rd.append(f'[{r["proposed_value"]}]' if r else key[t])
        rows.append(f'<tr><td class="ln">{gi}</td><td class="tok">{" ".join(toks)}</td>'
                    f'<td class="lit">{"".join(lit)}</td><td class="rd">{"".join(rd)}</td></tr>')

    by_plain = {}
    for sym, p in key.items():
        by_plain.setdefault(p, []).append(sym)
    keyrows = "".join(
        f'<tr><td class="rd">{"u / v" if p == "u" else p}</td><td class="tok">'
        f'{", ".join(sorted(s, key=lambda x: (x.isdigit(), int(x) if x.isdigit() else 0, x)))}</td></tr>'
        for p, s in sorted(by_plain.items()))

    french = "".join(f'<p class="{k}">{html.escape(t)}</p>' if k else f"<p>{html.escape(t)}</p>" for k, t in F_FRENCH)
    english = "".join(f"<p>{html.escape(t)}</p>" for t in F_ENGLISH)

    body = f"""{CRUMBS.format(f'<a href="{REPO}/tree/main/forster-1644">write-up and files</a>')}
<header class="masthead">
  <p class="eyebrow">Archives départementales du Val-d'Oise, 68 H 8 · France, 13 May 1644</p>
  <h1>Les voyes de prudence</h1>
  <p class="standfirst">A ciphered passage in a letter in the hand of Sir Richard Forster, treasurer of Henrietta Maria's household: spiritual counsel to someone in danger, that preserving one's life is no failing before God.</p>
</header>

<div class="lede">
  <div>
    <h3>What the passage says</h3>
    <p>Forster wrote from France in May 1644. The plaintext names no person, place or title, so the addressee is inferred, not established. Karen Britland's abstract says Henrietta Maria, at Exeter, ill, pregnant, and deciding whether to flee to France, made a related request a few days later, which makes her a plausible addressee, not a certain one. Whether Forster composed the counsel or relayed a confessor's is open.</p>
    <h3>How it was read</h3>
    <p>The cipher is a mixed letter-and-number homophonic substitution: 34 symbols over 207 tokens, in 37 comma-separated words. Character n-gram hill climbing went nowhere at that length. A beam search over a French lexicon with 17th-century spellings, constrained only by same-symbol-same-letter, produced most of the key in one run; a dozen symbols were then fixed by hand. The 16 letter-symbols map to 16 distinct plaintext letters, and the 18 number-symbols to 16. A Codex agent re-applied the key mechanically and reproduced the reading. Everything is reproducible from the <a href="{REPO}/tree/main/forster-1644">published files</a>.</p>
  </div>
  <div>
    <div class="callout">
      <h3>Not the first reading</h3>
      <p>Satoshi Tomokiyo's list still carried this passage as undeciphered when we read it on 14 September 2026, and we found no published solution. There were earlier ones. Britland has since told Robert Pitt that George Lasry supplied a decipherment after her 2013 article and that Norbert Biermann reached the same solution independently. Pitt published <a href="https://github.com/robertpitt/forster-cipher">his own key</a> a few hours before ours on the same day. Pitt's key and ours were reached separately and are identical; the earlier reading Britland passed on differs in a few words. No priority is claimed here.</p>
    </div>
    <h3>Reading the columns</h3>
    <p class="legend">Left: the ciphertext in Tomokiyo's transcription of Britland's printed text; commas are word breaks, and the two passages Forster left in clear are in italic. Middle: the key's output in the letter's own spelling, then modernised. Right: an English translation. Square brackets mark the three places where the key's output needs repair; the symbols concerned are marked in the ciphertext. No image of the manuscript is online, so whether those slips are Forster's or a transcriber's is not known.</p>
  </div>
</div>

<section class="folio" id="passage">
  <header class="folio-head"><h2>The passage</h2><p>One page, one side; cipher with two clear passages and the date</p></header>
  <div class="cols">
    <div class="col cipher"><h3>Ciphertext</h3>{"".join(left)}</div>
    <div class="col it"><h3>French</h3>{french}<p class="hand">Modernised</p><p>{html.escape(F_MODERN)}</p></div>
    <div class="col en"><h3>English</h3>{english}</div>
  </div>
  <div class="apparatus">
    <h4>Notes</h4>
    <ul>
      <li>Word 13, <code>prenez s[e]ulement</code>: cipher <code>a</code> (d) where <code>2</code> (e) is needed. A handwritten 2 and a are easily confused.</li>
      <li>Word 16, <code>p[o]ur</code>: <code>16</code> (i) where <code>s</code> (o) is needed.</li>
      <li>Word 27, <code>sacrifi[c]e</code>: <code>g</code> (y) where <code>q</code> (c) is needed; g and q are confusable in hand.</li>
      <li>Word 17, <code>conceruer</code>: the key gives <em>concerver</em>, a spelling attested in period documents, so it is not repaired.</li>
      <li>The last clear word is <em>soupir</em> in Tomokiyo's transcription and in Britland's printed text, but <em>soubir</em> in her abstract, that is <em>subir</em>, to endure. “To act or to endure” is the better reading.</li>
      <li>Word breaks inside cipher words are unmarked: <em>descrupule</em>, <em>manquera</em> (manquer a), <em>lesreigles</em>, <em>prenezseulement</em>, <em>lesvoyesde</em>, <em>enfaire</em>, <em>parla</em>, <em>lesalut</em>.</li>
    </ul>
    <details class="groups" open><summary>The 37 cipher words with the key's raw output</summary>
      <div class="scroll"><table><thead><tr><th>Word</th><th>Cipher symbols</th><th>Key output</th><th>Reading</th></tr></thead>
      <tbody>{"".join(rows)}</tbody></table></div>
    </details>
    <details class="groups"><summary>The key, by plaintext letter</summary>
      <div class="scroll"><table class="keytable"><thead><tr><th>Plain</th><th>Cipher symbols</th></tr></thead><tbody>{keyrows}</tbody></table></div>
      <p class="fn">Some letters have only a number (e, q, z), some only a letter-symbol (b, m, o, y); e and t have two numbers each.</p>
    </details>
  </div>
</section>

<footer class="colophon">
  <div>
    <h3>Sources</h3>
    <p>Karen Britland, “Reading between the lines: royalist letters and encryption in the English civil wars”, <em>Critical Quarterly</em> 55/4 (2013), which prints the passage. Satoshi Tomokiyo, <a href="https://cryptiana.web.fc2.com/code/unsolved.htm">Unsolved Historical Ciphers</a>, and his 2021 transcription. Robert Pitt, <a href="https://github.com/robertpitt/forster-cipher">forster-cipher</a>, which reports Britland's account of the Lasry and Biermann decipherments.</p>
    <p>The manuscript is in the fonds of the English Benedictine nuns of Pontoise, whose first abbess was Forster's daughter. It is not digitised and has not been checked.</p>
  </div>
  <div>
    <h3>About this page</h3>
    <p>Read 14 September 2026 with Claude Code; independently checked by a Codex agent the same day. This page is generated from <code>ct.txt</code>, <code>mapping.json</code> and <code>verification.json</code> in the <a href="{REPO}/tree/main/forster-1644">repository</a>, where the README has the method, the failure log and the manuscript location.</p>
  </div>
</footer>"""
    (DOCS / "forster-reading.html").write_text(page(
        "Les voyes de prudence",
        "Sir Richard Forster's ciphered passage of 13 May 1644: ciphertext, French and English side by side, with the key.",
        body))


# ---------------------------------------------------------------- Starhemberg

S_PASSAGES = [
    dict(id="opening", rows=(1, 6), h="Rows 1–6", sub="Opening and the memorandum to Wall · Prima table",
         hand="Cipher, rows 1–6 · Prima",
         de="… als ich nun den Innhalt derselben gefunden, so große Hoffnun[g] macht mir … daß … deroselben annoch gelingen werde, die durch das dem Stat[s]secretario Wall behändigte sehr treflich gefasste Memoir so geschickt als vor[sich]ti[g] eingeleitete Handlung nunmehro immer offen zu behalten und den spanischen Hof … zu solchen Resolutionen zu vermögen …",
         en="… now that I have seen the contents of the same, it gives me such great hope … that … Your Excellency will yet succeed in keeping open, from now on, the negotiation so skilfully and so cautiously begun through the very well drafted memorandum handed to Secretary of State Wall, and in bringing the Spanish court … to such resolutions …",
         notes=[
             "The row-1 adjective before <em>als ich</em> is unresolved. Removing one surplus 3 permits <em>so / stat / lich</em>, which establishes neither <em>stattlich</em> nor <em>tröstlich</em>.",
             "<em>Annoch gelingen werde</em> comes from the uninterrupted <code>an / noch / ge / li / ng / en / werden</code>. Both <em>an</em> (31005) and <em>noch</em> (31019) had been misread in the working key; no target digit is changed.",
             "<em>Wall</em> is spelled <code>wa + l</code> here and again in row 19. With the memorandum and the long closing, it supplies three separated anchors for the key match.",
             "<em>Stat[s]secretario</em> needs 31168→31368 at offset 195; <em>vor[sich]tig</em> needs the invalid 30073 read as 31073. Both wait on the original.",
             "The court passage (row 6) is a damaged join: two deletions yield <em>bi / zu / solch / resolution</em>. <em>Bis zu solchen Resolutionen</em> is a candidate, not an accepted restoration. The baseline output there (<em>nach französisch religion mittelst armee ganz</em>) is what an unrepaired parse produces and is not read as text.",
         ]),
    dict(id="peace", rows=(7, 8), h="Rows 7–8", sub="War or an honourable peace · Prima, switching to Secunda at 876",
         hand="Cipher, rows 6–8 · Prima → Secunda",
         de="… die entweder dem Krieg eine vergnüglichere, als die dermahlige Gestalt ist, geben oder uns ein[en] erspr[ieß]lich[en] … honorablen Frieden verschaffen könnte, und gibt mir zumahl[en] …",
         en="… which could either give the war a more agreeable shape than its present one, or procure us a profitable … and honourable peace; and this gives me, moreover, …",
         notes=[
             "Two key corrections, <strong>31036 = Krieg</strong> and <strong>31490 = re</strong>, recover the first alternative with no digit changes. The literal run is <code>dem / Krieg / ein / ver / gn / u / gl / ich / re / als / die / der / mahl / ig / ge / st / al / t / ist / geben</code>.",
             "<strong>Frieden is source-supported.</strong> The alphabetical F entry reads <em>fried</em> with <em>en</em> and <em>same</em> endings; both numerical copies agree. The earlier reading <em>fremd</em> was wrong and its override has been retired.",
             "The join before <em>honorablen</em> sits at the recto/verso boundary. Inserting 31 at 624 and changing 9→3 at 626 gives <code>en / ho / null / n / or / ab / le / n / fried</code>; deleting 119 at 624 is a competing three-edit repair. Neither is authenticated.",
             "After the join, <code>ver / [A→B] / schaff / könnte</code> follows unchanged: the table switch 876 falls inside <em>verschaffen</em>.",
             "Secunda 53 is <strong>mahl</strong> (with <em>s</em>/<em>en</em> alternatives), not the earlier <em>meist</em>: the alphabetical entry sits between <em>mach</em> and <em>man</em>. So <code>gi / eb / t / mir / zu / mahl</code> reads <em>gibt mir zumahlen</em>. What follows, <code>von / den / no / ge / n …</code>, is unresolved.",
         ]),
    dict(id="minorca", rows=(9, 15), h="Rows 9–15", sub="The matching statements, Minorca, and Spain's entry · Secunda",
         hand="Cipher, rows 9–15 · Secunda",
         de="… Euer Hochgebohrn … französischen Botschafter fast zu gleicher Zeit gemachten, genau gleichförmigen Äusserungen … sehr große Hoffnun[g], daß … Minorca an Spanien überlassen würde, wozu sich Frankreich [bereit?] zeige un[d] wohl leicht [en]tschließen wird, alsdann dieser Hof an dem Krieg mit Theil nehmen und andurch den [engländischen] und preußischen Hof in sehr große Verlegenheit setz[en] würde.",
         en="… the exactly matching statements made almost at the same time by Your Excellency … [and] the French ambassador … [give] very great hope that … Minorca would be ceded to Spain, to which France shows itself [ready?] and will surely readily resolve; whereupon this court would take part in the war and thereby put the [English] and Prussian courts in very great embarrassment.",
         notes=[
             "The phrase from <em>französischen Botschafter</em> through <em>Äusserungen</em> uses <strong>unchanged digits</strong>. Correcting the key readings recovers <code>fa+st</code>, <code>zeit</code>, <code>ge+mach</code>, <code>genau</code> and <code>gl+ei+ch+fo+r+mi+gen+aus+ser+ung</code>. The abbreviated endings are editorial.",
             "<em>Minorca an Spanien überlassen würde</em> is unchanged code with grammatical endings expanded. <em>Preuss + n + Hof</em> and <code>ver / le / ge[n] / heit</code> are likewise unchanged.",
             "<em>[bereit?]</em> is <strong>not established</strong>: 31405 reads <em>berg</em> in the historical key.",
             "<em>Und wohl leicht entschließen wird</em> needs 31329→31326 at 1046 and 55→95 at 1061. <em>Setzen würde</em> needs the same 55→95 at 1216. One repair supplying <em>en</em> in two unrelated words is economical, and still a conjecture.",
             "<em>[Engländischen]</em> needs 31389→31399 at 1139 (<em>Engelland</em>), then an adjectival expansion.",
             "The connective before <em>Minorca</em> reads <code>daß / scho / n</code> and is unresolved. Until it is, the passage cannot be read as an unconditional promise of Spanish participation.",
             "Row 15 ends with Secunda 897, the period; the closing begins on the same row with <em>Da ich nun</em>.",
         ]),
    dict(id="closing", rows=(16, 22), h="Rows 16–22", sub="Courier Zinner and the advice to continue · Secunda, back to Prima at 899",
         hand="Cipher, rows 15–22 · Secunda → Prima",
         de="Da ich nun Euer Hochgebohrn durch den Courier Zinner zu erstattenden Berichten mit vielem Ver[langen?] ent[gegen]sehe, so brauche indessen nichts be[s]eres einrathen, als in dem bereits eingeschlagenen Weeg fortzufahren und den Wall so viel nur immer möglich durch dero [g]schicktes Benehmen zu weiteren Vertrauenausserungen zu vermögen.",
         en="As I await with great eagerness the reports Your Excellency is to send through the courier Zinner, I can advise nothing better in the meantime than to continue along the course already taken and, through your skilful conduct, persuade Wall as far as possible to make further confidential disclosures.",
         notes=[
             "<strong>Zinner</strong> is <code>14 zi / 31307 n / 99 er</code> after the whole-word code <em>Courier</em>, with no digit repair. Wille's journal independently records “M. Zinner, courrier impérial” under 5 September 1759 (vol. 1, p. 120). That corroborates a courier of this name, not that the two are the same man.",
             "The Zinner occurrence is also what kills a <strong>global</strong> 99→g: Secunda 99 must stay <em>er</em> at 1298, while four other occurrences (97, 335, 945, 1608) still appear to need <em>g</em>. A target-specific variant or a misread glyph are both possible; nothing settles it without the image.",
             "The awaiting clause is the least secure part. 31427 reads <em>lau</em> or <em>lan</em> with a <em>g</em> alternative, so <em>Verlangen</em> is plausible. <em>Ent[gegen]sehe</em> needs an insertion at the row boundary (offset 1369): seven digits <code>3111531</code>, or only <code>31</code> if the longer key alternative for 31115, apparently <em>gege</em>, is right. The two are competing reconstructions.",
             "<em>Be[s]eres</em> needs 31168→31368 at 1414. The same code at 525 correctly gives <em>u</em> in <em>vergnüglich</em>, so this repair is selective by design.",
             "<em>Nur</em> is explicit in both numerical copies of 31218; <em>weiteren</em> rests on a <em>t</em> alternative in the W entry 31484 that needs no inserted digit. There is no separately encoded <em>zu</em> in <em>einrathen</em>.",
             "The final unit is a lone 3 and is incomplete under the recovered rule.",
         ]),
]


def starhemberg_reading():
    folder = ROOT / "starhemberg-1758"
    src_lines = (folder / "source-transcription.txt").read_text().splitlines()
    rows = [l for l in src_lines[9:] if l.strip()]
    assert len(rows) == 22, len(rows)
    out = (folder / "two-table-output.txt").read_text().splitlines()
    parsed = {}
    for i in range(0, len(out), 2):
        m = re.match(r"ROW (\d+): (.*)", out[i])
        assert m
        toks = []
        for u in m.group(2).split(" "):
            tbl, rest = u.split(":", 1)
            code, root = rest.split("=", 1)
            toks.append((tbl, code, root))
        parsed[int(m.group(1))] = toks
    # 390 units printed; the decoder omits the standalone-8 nulls from this listing (423 tokens in two-table-parsing.json).
    assert len(parsed) == 22 and sum(len(t) for t in parsed.values()) == 390, "baseline parse drifted"

    def lit(toks):
        parts = []
        for tbl, code, root in toks:
            if code in ("876", "899"):
                parts.append(f"<b>{html.escape(root)}</b>")
            elif root.startswith("{"):
                parts.append(f"<i>{html.escape(root)}</i>")
            else:
                parts.append(html.escape(root))
        return " | ".join(parts)

    def table_of(toks):
        t = [x[0] for x in toks]
        if t[0] != t[-1]:
            return "A→B" if t[0] == "A" else "B→A"
        return "Prima" if t[0] == "A" else "Secunda"

    def rowtable(r0, r1):
        trs = "".join(
            f"<tr><td class='ln'>{n}</td><td class='ln'>{table_of(parsed[n])}</td>"
            f"<td class='tok'>{html.escape(rows[n-1])}</td><td class='lit'>{lit(parsed[n])}</td></tr>"
            for n in range(r0, r1 + 1))
        return ("<div class='scroll'><table><thead><tr><th>Row</th><th>Table</th>"
                "<th>Cipher row as transcribed</th><th>Baseline key output, no digit repairs</th></tr></thead><tbody>"
                + trs + "</tbody></table></div>")

    def section(p):
        r0, r1 = p["rows"]
        cipher = "".join(f"<p><span class='rn'>{n}</span>{html.escape(rows[n-1])}</p>" for n in range(r0, r1 + 1))
        notes = "".join(f"<li>{n}</li>" for n in p["notes"])
        return f"""
<section class="folio" id="{p['id']}">
  <header class="folio-head"><h2>{p['h']}</h2><p>{p['sub']}</p></header>
  <div class="cols">
    <figure class="scan">
      <div class="rows">{cipher}</div>
      <figcaption>Rows {r0}–{r1} of the saved Cryptiana transcription, unchanged. Grouping and punctuation are the transcriber's; a caret marks a digit written above the line.</figcaption>
    </figure>
    <div class="col it"><h3>German</h3><p class="hand">{p['hand']}</p><p>{p['de']}</p></div>
    <div class="col en"><h3>English</h3><p class="hand">Translation</p><p>{p['en']}</p></div>
  </div>
  <div class="apparatus"><h4>Notes</h4><ul>{notes}</ul><details class="groups"><summary>Cipher rows and baseline key output, row by row (rows {r0}–{r1})</summary>
{rowtable(r0, r1)}
<p class="fn">Mechanical output of the working Prima/Secunda keys with no digit repairs. Braces mark units that do not parse; a slash separates key alternatives; bold marks a table switch. From <a href="{REPO}/blob/main/starhemberg-1758/two-table-output.txt">two-table-output.txt</a>.</p></details></div>
</section>"""

    body = f"""{CRUMBS.format(f'<a href="{REPO}/tree/main/starhemberg-1758">write-up and files</a>')}
<header class="masthead">
  <p class="eyebrow">Starhemberg, Paris, 23 May 1758 · Cryptiana transcription, 22 rows, 1,721 digits · Read with the 1752 Austrian Prima/Secunda key</p>
  <h1>Chiffre aus Paris</h1>
  <p class="standfirst">A ciphered letter from Prince Starhemberg, Austria's ambassador at Versailles, to a colleague at the Spanish court, in the spring of 1758: on the memorandum handed to Ricardo Wall, on Minorca as the price of Spain's entry into the war, and on the courier who is to carry the next reports. Read with the two-table numerical key the Vienna chancellery issued in 1752.</p>
  <span class="status">Partial decipherment · system identified · exact full text open</span>
</header>

<div class="lede">
  <div>
    <h3>What the letter says</h3>
    <p>Two years into the Seven Years' War, Austria and France wanted Spain in. Starhemberg writes that the memorandum handed to Wall, the Spanish first secretary, was very well drafted and that the negotiation it opened must be kept alive until the Spanish court comes to a decision. That could either give the war a better shape than it now has or bring an honourable peace. Closely matching statements by the recipient and the French ambassador raise hopes that Minorca, which France had taken from Britain in 1756, would be ceded to Spain, and that Spain would then enter the war and embarrass the English and Prussian courts. He is waiting for reports by the courier Zinner, and meanwhile advises staying on the course already taken and coaxing further confidences out of Wall.</p>
    <p>The recipient's name is not in the recovered text. The Vienna archive catalogues five 1758 letters from Starhemberg to Franz von Rosenberg, the Austrian envoy in Madrid, on exactly these subjects, so Rosenberg is the likely addressee, but the catalogue does not show that 23 May is among them.</p>
    <h3>How it was read</h3>
    <p>The cipher is numerical. Ordinary units are two digits; a leading 3 opens a four-digit code, so most written units are five digits. A standalone 8 is a null. Marked three-digit units supply punctuation, dates and table changes: here 876 switches from the Prima table to the Secunda at digit 662, 899 switches back at 1349, and Secunda 897 is a period. The tables are the 1752 key in <a href="https://de-crypt.org/decrypt-web/RecordsView/1695">DECODE R1695</a> and <a href="https://de-crypt.org/decrypt-web/RecordsView/1698">R1698</a>, with the chancellery's own instructions and worked example in R1696 and R1697. The system, though not this letter, is described in Antal, Mírka and Kováč's 2025 study of Viennese obfuscation techniques. Work of 17 and 18 September 2026 by native Codex agents; everything is reproducible from the <a href="{REPO}/tree/main/starhemberg-1758">published files</a>.</p>
  </div>
  <div>
    <div class="callout">
      <h3>Why it is not finished</h3>
      <p>Nobody on this side has seen the original. The only source is Alexandre Pillon's transcription on Cryptiana, which warns that digits may be missing at the right edge of the image, and several runs of the text do not parse as written. Every place where the reading needs a changed digit is listed below as a proposed repair, never applied to the transcription. The key itself is a provisional reading of eighteenth-century handwriting; where the tables give alternatives, both are kept.</p>
      <p>What is established is the system, the two table switches, and long runs of connected German on unchanged digits: the memorandum, the war-or-peace sentence, the matching statements, Minorca, Verlegenheit, Zinner, and the closing advice. What is not established is the opening adjective, four sentence joins, the word before <em>zeige</em>, and the four places where 99 seems to mean <em>g</em>.</p>
    </div>
    <h3>Reading the columns</h3>
    <p class="legend">Left: the cipher rows exactly as transcribed. Middle: the German reconstruction, with the editor's word boundaries, spelling and expanded endings. Right: an English translation. Square brackets mark a letter or word supplied by a proposed repair or expansion, with <code>?</code> where the supply is doubtful; ellipses are unresolved text. Each passage's notes say which readings rest on unchanged digits and which need a repair, and a fold-out table gives the baseline key output row by row.</p>
  </div>
</div>

<nav class="folios" aria-label="Passages"><a href="#opening">Rows 1–6</a><a href="#peace">Rows 7–8</a><a href="#minorca">Rows 9–15</a><a href="#closing">Rows 16–22</a><a href="#repairs">Repairs</a><a href="#checks">Checks</a><a href="#open">Open</a></nav>
{"".join(section(p) for p in S_PASSAGES)}

<section class="wide" id="repairs">
  <h2>Proposed repairs</h2>
  <div class="two">
    <div>
      <p>None of these is applied to the published transcription. Offsets are zero-based positions in the unchanged 1,721-digit stream. The eight small edits below, together with the two competing closing insertions and the two competing peace-join repairs, combine into eight full-letter parses in which every non-terminal unit parses and both table switches survive. Those parses cost 19 or 24 specified digit edits, not counting the four selective 99→g readings and the initial mark displacement. A valid segmentation is not a solution: several phrases in every candidate remain unreadable.</p>
      <p>At offsets 2, 443, 449, 708 and 793, treating the presumed surplus digits as null 8s gives exactly the same code sequence as deleting them, at equal cost. The comparison scans show that 3 and 8 are hard to tell apart in this hand. Parsing cannot decide between the two.</p>
    </div>
    <div class="scroll"><table class="repairs"><thead><tr><th>Offset</th><th>From</th><th>To</th><th>Supplies</th></tr></thead><tbody>
<tr><td class="ln">2</td><td class="tok">3</td><td class="tok">(delete)</td><td>lets 31159 + 31217 + 31214 parse; opening adjective still unresolved</td></tr>
<tr><td class="ln">195</td><td class="tok">31168</td><td class="tok">31368</td><td><em>s</em> in Statssecretario</td></tr>
<tr><td class="ln">325</td><td class="tok">30073</td><td class="tok">31073</td><td><em>sich</em> in vorsichtig (30073 is not a valid unit)</td></tr>
<tr><td class="ln">1046</td><td class="tok">31329</td><td class="tok">31326</td><td><em>un + d</em> before wohl leicht</td></tr>
<tr><td class="ln">1061</td><td class="tok">55</td><td class="tok">95</td><td><em>en</em> in entschließen</td></tr>
<tr><td class="ln">1139</td><td class="tok">31389</td><td class="tok">31399</td><td><em>Engelland</em>, paired with Preuss</td></tr>
<tr><td class="ln">1216</td><td class="tok">55</td><td class="tok">95</td><td><em>en</em> in setzen</td></tr>
<tr><td class="ln">1414</td><td class="tok">31168</td><td class="tok">31368</td><td><em>s</em> in beseres</td></tr>
<tr><td class="ln">624–626</td><td class="tok">…</td><td class="tok">+31, 9→3 · or delete 119</td><td>join before honorablen Frieden; two competing repairs</td></tr>
<tr><td class="ln">1369</td><td class="tok">(none)</td><td class="tok">+3111531 · or +31</td><td>entgegensehe; the short form needs the <em>gege</em> reading of 31115</td></tr>
</tbody></table></div>
  </div>
</section>

<section class="wide" id="checks">
  <h2>Mechanical verification</h2>
  <div class="two">
    <div>
      <p>Running <code>python3 run_checks.py</code> in the published folder reproduces every figure on this page from the checked-in transcription and keys, with the standard library only. It was rerun on 18 September 2026 before this page was written and left the checkout clean. Passing these checks proves that each conjecture parses as claimed. It does not certify a complete decipherment, and the script says so on its last line.</p>
      <p>The two external controls matter most. The chancellery's own worked example was transcribed independently and every unit boundary and its table switch agree with the parser. A separate 1756 Kaunitz letter with surviving plaintext, reproduced in the Antal study, yields two disjoint windows that align on the same key readings: <em>Nachricht</em>, <em>glücklichen</em>, <em>Ankunft</em>, and <em>so den 13 Marti an Euer Excellenz abgefert…</em> with its date codes and table switch. The span between the two windows is not aligned, so they are not one continuous match.</p>
    </div>
    <table class="checks"><tbody>
<tr><td>1,721</td><td>digits conserved by the baseline parser, giving 423 units</td><td class="ok">passes</td></tr>
<tr><td>2</td><td>table switches (876 at 662, 899 at 1349) and one period (897 at 1220)</td><td class="ok">passes</td></tr>
<tr><td>13</td><td>fragment alignments on unchanged digits, from the memorandum to the closing</td><td class="ok">passes</td></tr>
<tr><td>202 / 74</td><td>digits and units of the chancellery's worked example; all boundaries and switch 818 agree</td><td class="ok">passes</td></tr>
<tr><td>53 + 48</td><td>digits in two disjoint windows of the 1756 Kaunitz letter aligned to plaintext</td><td class="ok">passes</td></tr>
<tr><td>4</td><td>contexts where Prima 31210 = me / mer / men reads consistently (nunmehro, immer ×2, Benehmen)</td><td class="ok">passes</td></tr>
<tr><td>11</td><td>local repair cases reproducing their stated code sequences</td><td class="ok">passes</td></tr>
<tr><td>8</td><td>joint full-letter candidates, 19 or 24 edits each</td><td class="ok">passes</td></tr>
<tr><td>239</td><td>distinct ordinary units in the baseline parse audited against the numerical key: 91 with recorded alternatives, 18 with open notes</td><td class="ok">recorded</td></tr>
</tbody></table>
  </div>
</section>

<section class="wide" id="open">
  <h2>What remains open</h2>
  <div class="two">
    <div>
      <h3>In the text</h3>
      <ul>
        <li>The opening adjective in row 1.</li>
        <li>The join after <em>den spanischen Hof</em> in row 6, where <em>bis zu solchen Resolutionen</em> is only a candidate.</li>
        <li>The recto/verso join before <em>honorablen Frieden</em>.</li>
        <li>The sentence leading from <em>gibt mir zumahlen</em> into the matching statements.</li>
        <li>The connective before <em>Minorca</em>, which decides whether Spain's participation is conditional, expected or promised.</li>
        <li><em>Bereit</em>, where the key reads <em>berg</em>.</li>
        <li>The start of the closing, <em>Verlangen</em> and the length of the <em>entgegensehe</em> insertion.</li>
        <li>The four 99→g occurrences, and the incomplete terminal 3.</li>
      </ul>
    </div>
    <div>
      <h3>In the sources</h3>
      <ul>
        <li>No image of the letter has been found. Cryptiana links none. The best archival lead is <a href="https://www.archivinformationssystem.at/detail.aspx?ID=4225949">HHStA Frankreich Varia 28-14</a>, five Starhemberg letters to Rosenberg from April to December 1758 catalogued under Spain, Bernis, Minorca, mediation and peace plans, with no item-level listing and no scans.</li>
        <li>No printed plaintext. Two OCR copies of Arneth's <em>Geschichte Maria Theresia's</em>, volume 5, were searched for the date, Rosenberg, Wall and Minorca without a match; a volume 6 lead from a Bernis footnote turned out to concern 1762. Fraktur OCR limits both negatives.</li>
        <li>The Antal study reports sixteen parallel letters in the Slovak National Archive (Esterházy Čeklís, box 634). They are not in DECODE and no public transcription was found.</li>
        <li>The key tables themselves. The working TSVs are provisional readings of the DECODE facsimiles; the <em>gege</em> alternative at 31115 and the <em>g</em> alternative at 31427 in particular need a careful look at the originals.</li>
      </ul>
      <p>A scan of the letter would settle most of the first list at once, since nearly every open point is a damaged run of digits rather than a missing key entry.</p>
    </div>
  </div>
</section>

<footer class="colophon">
  <div>
    <h3>Sources</h3>
    <ul>
      <li>Target: <a href="https://cryptiana.web.fc2.com/code/variable2.htm#Starhemberg">Cryptiana, Starhemberg 1758</a>, transcription credited to Alexandre Pillon. The original image was not available to us.</li>
      <li>Key: DECODE <a href="https://de-crypt.org/decrypt-web/RecordsView/1695">R1695</a> (alphabetical and numerical Prima and Secunda) and <a href="https://de-crypt.org/decrypt-web/RecordsView/1698">R1698</a> (numerical copies); instructions and worked example in <a href="https://de-crypt.org/decrypt-web/RecordsView/1696">R1696</a> and <a href="https://de-crypt.org/decrypt-web/RecordsView/1697">R1697</a>. The facsimiles are not redistributed.</li>
      <li>System: Antal, Mírka and Kováč, <a href="https://doi.org/10.1080/01611194.2025.2457096">Development of obfuscation techniques in Vienna during the early modern era</a>, Cryptologia (online 2025), Appendix C and Figures 1–2.</li>
      <li>Zinner: <a href="https://archive.org/stream/mmoiresetjournal01will/mmoiresetjournal01will_djvu.txt">Wille, Mémoires et journal</a>, vol. 1, 5 September 1759, p. 120.</li>
    </ul>
  </div>
  <div>
    <h3>Files and status</h3>
    <p>The published folder <a href="{REPO}/tree/main/starhemberg-1758">starhemberg-1758</a> holds the unchanged cipher rows, the working keys, the baseline parser, the fragment alignments, the two external calibrations, the audit ledger of key corrections, the proposed repairs, the eight joint candidates, and a one-command runner. This page is generated from <code>source-transcription.txt</code> and <code>two-table-output.txt</code> there.</p>
    <p>This is a reproducible partial reading. It makes no claim to a complete or first decipherment, and the English on this page is a translation of a reconstruction, not of an established text. The unresolved connective before Minorca in particular means the summary must not be quoted as the letter's promise of Spanish participation.</p>
  </div>
</footer>"""
    (DOCS / "starhemberg-reading.html").write_text(page(
        "Chiffre aus Paris",
        "Starhemberg's ciphered Paris letter of 23 May 1758: partial German reading with the 1752 Austrian key, English translation, proposed repairs, checks and what remains open.",
        body))



# ---------------------------------------------------------------- index

def index():
    body = f"""<header class="masthead">
  <p class="eyebrow">Working notes · September 2026</p>
  <h1>Unsolved ciphers</h1>
  <p class="standfirst">Attempts on historical ciphers that are short, context-rich, and listed as unsolved. Started after Vals AI reported Claude Fable 5.1 reading Thomas Urquhart's Cyphral Distich; the question was whether the same approach, an agent plus a person checking its work, gets anywhere on the rest of the list.</p>
</header>

<div class="entries">
  <div class="entry">
    <h2><a href="ferdinand-reading.html">Ferdinand correspondence</a></h2>
    <p class="where">Brussels / Vienna, 16 November 1635 and 22 February 1640</p>
    <p class="status">Substantially deciphered · residual gaps</p>
    <p>Winter quarters at Trier, recruitment in Westphalia, and a request for 100,000 florins. A known Latin draft supplies the 1635 alphabet; a separate syllable supplement extends the reading through both 1640 pages. Uncertain glyphs and copying errors remain explicit. No first-solve claim.</p>
    <p class="go"><a href="ferdinand-reading.html">Ciphertext, Latin and English</a></p>
    <p><a href="{REPO}/tree/main/ferdinand-1635-1640">Readings, key evidence, transcriptions and decoder</a>.</p>
  </div>
  <div class="entry">
    <h2><a href="ottobon-reading.html">Carta en cifra de Venecia</a></h2>
    <p class="where">Ottobon to Mocenigo, 27 April 1589 · BNE Mss/994, ff. 34–38</p>
    <p class="status">Substantially deciphered</p>
    <p>A Venetian dispatch to the ambassador in France, with the enclosed reply to Henri III's envoy Gondi, who had come to ask for aid and a league. The Republic's surviving key, <em>Ziffra prima</em>, reads all seven cipher pages. Intercepted in Savoy in 1589 and broken then by Philip II's cipher secretary, whose working was lost.</p>
    <p class="go"><a href="ottobon-reading.html">Page-by-page reading</a></p>
    <p>Manuscript images, Italian and English side by side. <a href="{REPO}/tree/main/ottobon-1589">Write-up, transcription, key excerpt and decoder</a>.</p>
  </div>
  <div class="entry">
    <h2><a href="forster-reading.html">Les voyes de prudence</a></h2>
    <p class="where">Sir Richard Forster, 13 May 1644 · AD Val-d'Oise, 68 H 8</p>
    <p class="status">Deciphered · not a first reading</p>
    <p>A ciphered passage in a letter by the treasurer of Henrietta Maria's household: counsel that preserving one's life is no failing before God. Mixed letter-and-number homophonic substitution, 207 symbols, three repairs. George Lasry and Norbert Biermann had read it earlier, and Robert Pitt published a key the same day; no priority is claimed.</p>
    <p class="go"><a href="forster-reading.html">Ciphertext, French and English</a></p>
    <p>With the 37 cipher words and the key. <a href="{REPO}/tree/main/forster-1644">Write-up, solver and verification</a>.</p>
  </div>
  <div class="entry">
    <h2><a href="starhemberg-reading.html">Chiffre aus Paris</a></h2>
    <p class="where">Starhemberg, Paris, 23 May 1758 · Cryptiana transcription</p>
    <p class="status">Partially deciphered</p>
    <p>A numerical cipher letter from Austria's ambassador at Versailles on drawing Spain into the Seven Years' War: the memorandum handed to Wall, Minorca as the price, a courier named Zinner. The 1752 Prima/Secunda key (DECODE R1695, R1698) gives connected German across the letter, but with no image of the original several joins do not parse and the exact full text is open.</p>
    <p class="go"><a href="starhemberg-reading.html">Cipher rows, German and English</a></p>
    <p>With the baseline key output, the proposed repairs and the checks. <a href="{REPO}/tree/main/starhemberg-1758">Write-up, keys, scripts and audit</a>.</p>
  </div>
</div>

<div class="more">
  <h3>Also in the repository</h3>
  <ul>
    <li><a href="{REPO}/tree/main/royalist-1646">Intercepted royalist letters, May 1646</a> (BL Add MS 72438 ff. 9-10). Open, partial: the cipher is identified as key no. 129 of Lord Digby's captured cabinet and about 45 values are fixed.</li>
    <li><a href="{REPO}/tree/main/burgess-1912">Gelett Burgess, <em>The Master of Mysteries</em> (1912)</a>, the third hidden message. Open; the notes list what was tested.</li>
    <li><a href="{REPO}/blob/main/SHORTLIST.md">Shortlist</a> of candidates, with per-item status checks.</li>
  </ul>
</div>

<footer class="colophon">
  <div>
    <h3>Sources</h3>
    <p>Satoshi Tomokiyo, <a href="https://cryptiana.web.fc2.com/code/unsolved.htm">Unsolved Historical Ciphers</a>. Klaus Schmeh, <a href="https://scienceblogs.de/klausis-krypto-kolumne/the-top-50-unsolved-encrypted-messages/">Top 50 unsolved encrypted messages</a>. Nick Pelling, <a href="https://ciphermysteries.com/">Cipher Mysteries</a>.</p>
  </div>
  <div>
    <h3>About</h3>
    <p>Andy Aymeloglu. Work uses Claude Code and native Codex agents. Scripts reproduce decoding from the transcriptions; handwriting judgments require comparison with the cited images. <a href="{REPO}">Code and data on GitHub</a>.</p>
  </div>
</footer>"""
    (DOCS / "index.html").write_text(page(
        "Unsolved ciphers",
        "Attempts on historical ciphers listed as unsolved: a Venetian dispatch of 1589 and a royalist letter of 1644 read, Ferdinand correspondence of 1635/1640 recovered, an Austrian letter of 1758 partly read, all reproducible.",
        body))


if __name__ == "__main__":
    ottobon_reading()
    forster_reading()
    starhemberg_reading()
    build_ferdinand(ROOT, DOCS, page, CRUMBS, REPO)
    index()
    (DOCS / ".nojekyll").write_text("")
    print("built", ", ".join(sorted(p.name for p in DOCS.glob("*.html"))))
