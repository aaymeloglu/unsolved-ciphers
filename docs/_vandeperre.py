"""Build the Vande Perre page from transcription.txt, key.json and repairs.json via
vande-perre-1653/verify.py, so the page shows exactly what the decoder reproduces."""
import html
import importlib.util

# Dutch and English per run, in transcription order. Blank Dutch = unresolved.
TEXT = {
    "P500.1": ("in [57] n viandich land", "in [?] hostile country"),
    "P500.2": ("een redelijcke dispositie tot handelinge wert gespeurt, die wel diende waergenomen",
               "a reasonable disposition to negotiate is noticed, which ought to be taken up"),
    "P500.3": ("regeringe met impatientie op nader ordre van ons verwac[hten]",
               "the government await further orders from us with impatience"),
    "P522.1": ("[617] goede dispositie", "[617] good disposition"),
    "P522.2": ("", "Birch: “who upon good grounds”"),
    "P522.3": ("wij gequalificeert eenige nadere propositie doen", "we [were] authorised to make some further proposal"),
    "P522.4": ("ten principal[e]n", "chiefly"),
    "P522.5": ("14 daghen", "fourteen days"),
    "P576.1": ("ons tot voordeel gerekent", "reckoned to our advantage"),
    "P582.1": ("thien schepen", "ten ships"),
    "P582.2": ("[115] geloopen", "run [115]"),
    "P582.3": ("bewaren", "to guard"),
    "P582.4": ("", ""),
    "P582.5": ("gebreck", "want [of]"),
    "P582.6": ("masten", "masts [found]"),
}
CONTEXT = {
    "P500.1": "keep me at present out of harm’s way.",
    "P500.2": "Adding only to this, that at present here",
    "P500.3": "We hear that many of",
    "P522.1": "which we very much long for.",
    "P522.2": "and yesterday in particular a person",
    "P522.3": "can speak of it, told me, in case",
    "P522.4": "the work",
    "P522.5": "within",
    "P576.1": "The said change is",
    "P582.1": "Yesterday we heard, that the men of",
    "P582.2": "to",
    "P582.3": "to look to them",
    "P582.4": "the fleet",
    "P582.5": "Here is also want of masts.",
    "P582.6": "van",
}
PAGE = {"P500": ("p. 500", "Westminster, 3 October 1653", "n529"), "P522": ("p. 522", "October 1653", "n551"),
        "P576": ("p. 576", "London, 4/14 November 1653", "n605"), "P582": ("p. 582", "Westminster, 11/21 November 1653", "n611")}
# Runs shown together because they share one printed line.
MERGE = {"P582.6": "P582.5"}
RAW = "https://raw.githubusercontent.com/aaymeloglu/unsolved-ciphers/main/vande-perre-1653/pages"
STYLE = """<style>
.run { margin:28px 0 34px; }
.run .tag { font-size:12px; letter-spacing:.06em; text-transform:uppercase; color:var(--muted, #7a6f63); margin:0 0 6px; }
.run img { width:100%; height:auto; display:block; border:1px solid rgba(0,0,0,.08); }
.run dl { display:grid; grid-template-columns:max-content minmax(0,1fr); gap:4px 16px; margin:10px 0 0; }
.run dt { font-size:12px; letter-spacing:.06em; text-transform:uppercase; color:var(--muted, #7a6f63); padding-top:3px; }
.run dd { margin:0; min-width:0; overflow-wrap:anywhere; }
.run dd code { word-break:break-all; }
.run dd.nl { font-style:italic; }
</style>"""
LETTERS = [
    ("p. 500", "n529", "Westminster, 3 October 1653 NS"),
    ("p. 522", "n551", "October 1653"),
    ("p. 576", "n605", "London, 4/14 November 1653"),
    ("p. 582", "n611", "Westminster, 11/21 November 1653"),
]


def build(root, docs, page, crumbs, repo):
    spec = importlib.util.spec_from_file_location("vp_verify", root / "vande-perre-1653" / "verify.py")
    v = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(v)
    from cipherkit.grades import counts, render
    key, lines, repairs = v.load()
    ed = v.edited(key, lines, repairs)
    c = counts(r for rs in ed.values() for r in rs)
    ia = "https://archive.org/details/collectionofstat01thur/page/"

    blocks = []
    for tag, toks in lines:
        if tag in MERGE:
            continue
        tags = [tag] + [t for t, into in MERGE.items() if into == tag]
        where, date, leaf = PAGE[tag.split(".")[0]]
        reading = " | ".join(render(ed[t]) for t in tags)
        dutch = " … ".join(TEXT[t][0] for t in tags if TEXT[t][0])
        english = " … ".join(TEXT[t][1] for t in tags if TEXT[t][1])
        label = tag if len(tags) == 1 else f"{tag}–{tags[-1].split('.')[1]}"
        blocks.append(
            f'<div class="run"><p class="tag">{label} · {where} · {html.escape(date)}</p>'
            f'<a href="{ia}{leaf}" title="Full page on the Internet Archive"><img src="{RAW}/{tag}.jpg" alt="Birch, Thurloe State Papers i, {where}: the printed passage for {label}" loading="lazy"></a>'
            f'<dl><dt>Decoded</dt><dd><code>{html.escape(reading)}</code></dd>'
            f'<dt>Dutch</dt><dd class="nl">{html.escape(dutch) if dutch else "<em>unresolved</em>"}</dd>'
            f'<dt>English</dt><dd>{html.escape(english)}</dd></dl></div>')
    rows = "".join(blocks)
    letters = [(k, val["value"]) for k, val in key.items() if val["grade"] == "S"]
    keyrow = ("<table class=\"key\"><thead><tr>" + "".join(f"<th>{html.escape(k)}</th>" for k, _ in letters)
              + "</tr></thead><tbody><tr>" + "".join(f"<td>{html.escape(val)}</td>" for _, val in letters)
              + "</tr></tbody></table>")
    reprows = "".join(
        f"<tr><td>{r['line']}.{r['pos']}</td><td><code>{html.escape(r['printed'])}</code></td>"
        f"<td>{html.escape(r['value'])}</td><td>{html.escape(r['why'])}</td></tr>" for r in repairs)
    sources = "".join(
        f"<li><a href=\"{ia}{leaf}\">{p}</a>, {html.escape(d)}</li>" for p, leaf, d in LETTERS)

    body = f"""{crumbs.format(f'<a href="{repo}/tree/main/vande-perre-1653">write-up and files</a>')}
<header class="masthead">
  <p class="eyebrow">Deciphered · three code groups open · 14 September 2026</p>
  <h1>Vande Perre to de Bruyne, 1653</h1>
  <p class="standfirst">The Dutch ambassador in London during the peace talks of 1653 wrote to the pensionary of Zeeland with his most sensitive words in cipher. Thurloe’s office intercepted the letters and translated them, leaving the ciphered words as numbers, and Birch printed them that way in 1742. The cipher, a 22-letter alphabetical substitution with a few code groups, covers short phrases only, and it was recovered from the printed digits alone.</p>
</header>
{STYLE}
<section>
  <h2>What is enciphered</h2>
  <p>Not whole letters. Vande Perre wrote in Dutch and put only the sensitive phrases in cipher, a few words at a time. Thurloe’s office intercepted the letters and translated the clear parts into English, leaving the ciphered phrases as numbers; Birch printed the translations that way. Across four letters there are fifteen ciphered runs, 291 symbols in all. The longest is 70 symbols, one Dutch sentence (P500.2); most are one to five words. Solving it meant recovering the cipher alphabet from those fragments and reading each one.</p>
  <p>Below, each run as it stands on Birch’s page, then the decoder’s output, the Dutch and an English translation. In the decoded line <code>(?)</code> is an unread code group and <code>[..]</code> a repair of an evident misprint. In the Dutch and English, square brackets hold code-group numbers and editorial supplements. The small English words over some runs are Birch’s glosses, which show that Thurloe’s office read those passages in 1653. Each image links to the full page on the Internet Archive.</p>
</section>
<section>
  <h2>The ciphered passages</h2>
  {rows}
  <p>Birch printed short English glosses over some runs: “the good dispositions do”, “who upon good grounds”, “we were qualified with some farther propositions that would do”, “chiefly”, “fourteen days”, “ten ships at Yarmouth”, “were run away”, “left”. They show that Thurloe’s office read at least these passages in 1653. The key was found without them, and it reads <em>wij</em>, <em>gequalificeert</em>, <em>nadere propositie</em>, <em>principalen</em>, <em>thien schepen</em> and <em>geloopen</em> under the matching glosses. The London letter of 4/14 November has no gloss: its run reads “The said change [in the council] is <em>ons tot voordeel gerekent</em>”, reckoned to our advantage.</p>
</section>
<section>
  <h2>Key</h2>
  <p>{c['S']} of {sum(c.values())} printed symbols are read by this key (grade S), {c['M']} are unread code groups (57, 617, 115; M), and {c['I']} are repairs of misprints (I). No surviving key or contemporary Dutch decipherment has been found, so this is a cryptanalytic result. <code>frac</code> is the fraction-like sort Birch sets for 11; it reads <em>ij</em>.</p>
  {keyrow}
  <p>A key-shuffle permutation on the printed digits, scored by dictionary segmentation under the repository’s Dutch corpus, gives z = 4.2 (p = 0.001, 1000 shuffles). The kit’s annealer, run ciphertext-only, recovers 16 to 19 of the 22 values and scores the key above every search result. Details in the <a href="{repo}/blob/main/vande-perre-1653/README.md#method-and-what-the-controls-say">method notes</a>.</p>
</section>
<section>
  <h2>Misprints repaired</h2>
  <p>The printed digits are kept as they are in <code>transcription.txt</code>; each change below is applied only in the reading.</p>
  <table class="key"><thead><tr><th>Run.position</th><th>Printed</th><th>Read as</th><th>Reason</th></tr></thead><tbody>{reprows}</tbody></table>
</section>
<section>
  <h2>Open points</h2>
  <ul>
    <li>Code groups 57, 617 and 115 occur once each. The glosses suggest 617 is an article or <em>de</em> and 115 is <em>wech</em> (away). If 57 stood for <em>ee</em>, P500.1 would read <em>in een viandich land</em> (in a hostile country). None is established.</li>
    <li>P522.2 <code>diemnicvndament</code>, glossed “who upon good grounds”, does not divide into Dutch as printed. P582.4 <code>ote</code> (“the fleet [ote] will not go out”) is unresolved.</li>
    <li>A short run in an earlier Vande Perre letter of the same volume, a few pages before p. 435, after “a character to open a lockt chest”, begins <em>ick segghe</em> (“I say”) under this key; the rest has not been checked against the page image.</li>
    <li>The Beverning and Vande Perre letter to Boreel of 1 September 1653 (p. 435) uses a different cipher and remains unread.</li>
  </ul>
</section>
<section>
  <h2>Sources and files</h2>
  <p>Thomas Birch, ed., <em>A Collection of the State Papers of John Thurloe</em>, vol. 1 (London, 1742), Internet Archive <a href="https://archive.org/details/collectionofstat01thur">collectionofstat01thur</a>:</p>
  <ul>{sources}</ul>
  <p>Satoshi Tomokiyo, <a href="https://cryptiana.web.fc2.com/code/unsolved.htm">Unsolved Historical Ciphers</a>, “Dutch ciphers (1653)”. The page is generated from <code>transcription.txt</code>, <code>key.json</code> and <code>repairs.json</code> in the <a href="{repo}/tree/main/vande-perre-1653">repository</a>, where <code>verify.py</code> reproduces the reading and <code>solve.py</code> the ciphertext-only search.</p>
</section>"""
    (docs / "vandeperre-reading.html").write_text(page(
        "Vande Perre to de Bruyne, 1653",
        "The Dutch cipher in Thurloe's intercepts of Vande Perre's letters to the pensionary of Zeeland, October-November 1653, read from Birch's printed digits: a disposition to negotiate, the government's impatience, ten ships run, want of masts.",
        body))
