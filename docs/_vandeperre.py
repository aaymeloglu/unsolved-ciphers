"""Build the Vande Perre page from transcription.txt, key.json and repairs.json via
vande-perre-1653/verify.py, so the page shows exactly what the decoder reproduces."""
import html
import importlib.util

# Dutch and English per run, in transcription order. Blank Dutch = unresolved.
TEXT = {
    "P431.1": ("ick segghe een cijffer", "I mean a cipher"),
    "P500.1": ("in een viandich land", "in a hostile country"),
    "P500.2": ("een redelijcke dispositie tot handelinge wert gespeurt, die wel diende waergenomen",
               "a reasonable disposition to negotiate is noticed, which ought to be taken up"),
    "P500.3": ("regeringe met impatientie op nader ordre van ons verwac[hten]",
               "the government await further orders from us with impatience"),
    "P522.1": ("de goede dispositie", "the good disposition"),
    "P522.2": ("die m… fundament", "Birch: “who upon good grounds”"),
    "P522.3": ("wij gequalificeert eenige nadere propositie doen", "we [were] authorised to make some further proposal"),
    "P522.4": ("ten principal en", "chiefly, and"),
    "P522.5": ("14 daghen", "fourteen days"),
    "P576.1": ("ons tot voordeel gerekent", "reckoned to our advantage"),
    "P582.1": ("thien schepen", "ten ships"),
    "P582.2": ("[Jarmuyen] geloopen", "[at Yarmouth] run [away]"),
    "P582.3": ("bewaren", "to guard"),
    "P582.4": ("", ""),
    "P582.5": ("gebreck", "want [of]"),
    "P582.6": ("masten", "masts [found]"),
}
CONTEXT = {
    "P431.1": "a character to open a lockt chest",
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
PAGE = {"P431": ("p. 431", "Westminster, 29 August 1653", "n460"), "P500": ("p. 500", "Westminster, 3 October 1653", "n529"), "P522": ("p. 522", "October 1653", "n551"),
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
    ("p. 431", "n460", "Westminster, 29 August 1653"),
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
  <p class="eyebrow">Deciphered · two fragments open · 19 September 2026</p>
  <h1>Vande Perre to de Bruyne, 1653</h1>
  <p class="standfirst">The Dutch ambassador in London during the peace talks of 1653 wrote to the pensionary of Zeeland with his most sensitive words in cipher. Thurloe’s office intercepted the letters and translated them, leaving the ciphered words as numbers, and Birch printed them that way in 1742. The cipher, a 22-letter alphabetical substitution with a symbol for <em>ee</em> and a few code groups, covers short phrases only, and it was recovered from the printed digits alone.</p>
</header>
{STYLE}
<section>
  <h2>What is enciphered</h2>
  <p>Not whole letters. Vande Perre wrote in Dutch and put only the sensitive phrases in cipher, a few words at a time. Thurloe’s office intercepted the letters and translated the clear parts into English, leaving the ciphered phrases as numbers; Birch printed the translations that way. Across five letters there are sixteen ciphered runs, 308 symbols in all. The longest is 70 symbols, one Dutch sentence (P500.2); most are one to five words. Solving it meant recovering the cipher alphabet from those fragments and reading each one.</p>
  <p>Below, each run as it stands on Birch’s page, then the decoder’s output, the Dutch and an English translation. In the decoded line <code>[..]</code> marks a repair of an evident misprint or an inferred value; in the Dutch and English, square brackets hold editorial supplements. The small English words over some runs are Birch’s glosses, which show that Thurloe’s office read those passages in 1653. Each image links to the full page on the Internet Archive.</p>
</section>
<section>
  <h2>The ciphered passages</h2>
  {rows}
  <p>Birch printed short English glosses over some runs: “the good dispositions do”, “who upon good grounds”, “we were qualified with some farther propositions that would do”, “chiefly”, “fourteen days”, “ten ships at Yarmouth”, “were run away”, “left”. They show that Thurloe’s office read at least these passages in 1653. The key was found without them, and it reads <em>wij</em>, <em>gequalificeert</em>, <em>nadere propositie</em>, <em>principalen</em>, <em>thien schepen</em> and <em>geloopen</em> under the matching glosses. The London letter of 4/14 November has no gloss: its run reads “The said change [in the council] is <em>ons tot voordeel gerekent</em>”, reckoned to our advantage.</p>
</section>
<section>
  <h2>Key</h2>
  <p>{c['S']} of {sum(c.values())} printed symbols are read by this key (grade S), {c['C']} are code groups whose values come from Birch’s glosses (C: 617 <em>de</em> under “the good dispositions”, 115 Yarmouth under “ten ships at Yarmouth”, with <em>to</em> in clear before it), and {c['I']} are repairs of misprints or inferred values (I). The symbol 77 stands for <em>ee</em>: it occurs in <em>gequalificeert</em> and in <em>een cijffer</em>. The 57 of P500.1 sits where <em>een</em> needs its <em>ee</em>; it is a homophone of 77 or a misprint for it. No surviving key has been found; the letter values are a cryptanalytic result, and the two code groups rest on the 1653 translators. <code>frac</code> is the fraction-like sort Birch sets for 11; it reads <em>ij</em>.</p>
  {keyrow}
  <p>A key-shuffle permutation on the printed digits, scored by dictionary segmentation under the repository’s Dutch corpus, gives z = 5.2 (p = 0.001, 1000 shuffles). The kit’s annealer, run ciphertext-only, recovers 16 to 19 of the 22 values and scores the key above every search result. Details in the <a href="{repo}/blob/main/vande-perre-1653/README.md#method-and-what-the-controls-say">method notes</a>.</p>
</section>
<section>
  <h2>Misprints repaired</h2>
  <p>The printed digits are kept as they are in <code>transcription.txt</code>; each change below is applied only in the reading.</p>
  <table class="key"><thead><tr><th>Run.position</th><th>Printed</th><th>Read as</th><th>Reason</th></tr></thead><tbody>{reprows}</tbody></table>
</section>
<section>
  <h2>Open points</h2>
  <ul>
    <li>P522.2 <code>diemnicvndament</code>, glossed “who upon good grounds”: <em>die m…</em> and <em>…ndament</em> point to <em>die met fundament</em> (who with good grounds), but the printed <em>12. 5.</em> between them would have to stand for <em>27. 8.</em> (<em>t f</em>), two errors in a row; with 28 read as <em>u</em> the rest fits. Not established.</li>
    <li>P582.4 <code>ote</code> (“the fleet [ote] will not go out”) is unresolved: three symbols, no Dutch word, no gloss.</li>
    <li>The letter values have no <em>u</em>: 28 is <em>v</em>, and <em>gespeurt</em> and <em>gequalificeert</em> print 17 (<em>n</em>) where <em>u</em> is wanted. Either <em>u</em> was written with the <em>n</em> symbol or the print confuses 16 and 17 (16 never occurs).</li>
    <li>The 29 August letter announces a cipher sent “by a third hand”: “a character to open a lockt chest, <em>ick segghe een cijffer</em>”. That sentence is itself in the cipher read here, so what was sent may have been the code list rather than a new alphabet.</li>
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
