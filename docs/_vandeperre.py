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
    "P522.2": ("", "Birch: “who upon good grounds”"),
    "P522.3": ("wij gequalificeert eenige nadere propositie doen", "we [were] authorised to make some further proposal"),
    "P522.4": ("ten principal [e]n", "chiefly, and"),
    "P522.5": ("14 daghen", "fourteen days"),
    "P523.1": ("", "Major-General Harrison (printed gloss)"),
    "P523.2": ("ana[ba]ptisten", "Anabaptists"),
    "P523.3": ("", "Denmark (printed gloss)"),
    "P523.4": ("", "queen of Sweden (printed gloss)"),
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
PAGE = {"P431": ("p. 431", "Westminster, 29 August 1653", "n460"), "P500": ("p. 500", "Westminster, 3 October 1653", "n529"), "P522": ("p. 522", "Westminster, 10 October 1653 NS", "n551"),
        "P523": ("p. 523", "Westminster, 10 October 1653 NS", "n552"),
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
    ("p. 522", "n551", "Westminster, 10 October 1653 NS"),
    ("p. 523", "n552", "Continuation, 10 October 1653 NS"),
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
            f'<dt>Dutch</dt><dd class="nl">{html.escape(dutch) if dutch else ("<em>wording not recovered</em>" if tag in {"P523.1", "P523.3", "P523.4"} else "<em>unresolved</em>")}</dd>'
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
  <p class="standfirst">Paulus van de Perre, the Dutch ambassador in London during the peace talks of 1653, wrote to the pensionary of Zeeland with his most sensitive words in cipher. Thurloe’s office intercepted the letters and translated them, leaving the ciphered words as numbers, and Birch printed them that way in 1742. The cipher covers short phrases using a 22-letter alphabetical substitution, printed groups read as <em>ee</em>, and word codes. The alphabet was recovered from the printed digits; contemporary English glosses supply the code meanings.</p>
</header>
{STYLE}
<section>
  <h2>What is enciphered</h2>
  <p>Not whole letters. Vande Perre wrote in Dutch and put only the sensitive phrases in cipher, a few words at a time. Thurloe’s office intercepted the letters and translated the clear parts into English, leaving the ciphered phrases as numbers; Birch printed the translations that way. The verified outbound inventory contains twenty ciphered runs across five letters, 322 printed groups in all, including the continuation on p. 523. This is a checked inventory of these passages, not proof that no further cipher occurs elsewhere in the correspondence. The longest is 70 symbols, one Dutch sentence (P500.2); most are one to five words. The alphabet reads most of these fragments; two short strings remain unresolved.</p>
  <p>Below, each run as it stands on Birch’s page, then the decoder’s output, the Dutch and an English translation. In the decoded line <code>[..]</code> marks a proposed repair or inferred value; in the Dutch and English, square brackets hold editorial supplements. English labels in braces identify code meanings without claiming to recover their exact Dutch wording. The small English words over some runs are glosses transmitted by Birch from the contemporary translations; these passages had already been read in 1653. Each image links to the full page on the Internet Archive.</p>
</section>
<section>
  <h2>The ciphered passages</h2>
  {rows}
  <p>Birch printed short English glosses over some runs: “the good dispositions do”, “who upon good grounds”, “we were qualified with some farther propositions that would do”, “chiefly”, “fourteen days”, “ten ships at Yarmouth”, “were run away”, “left”. They show that Thurloe’s office read at least these passages in 1653. The alphabet was found without them. With the explicitly listed repairs, it reads <em>wij</em>, <em>gequalificeert</em>, <em>nadere propositie</em>, <em>principal</em>, <em>thien schepen</em> and <em>geloopen</em> under the matching glosses. The London letter of 4/14 November has no gloss: its run reads “The said change [in the council] is <em>ons tot voordeel gerekent</em>”, reckoned to our advantage.</p>
</section>
<section>
  <h2>Key</h2>
  <p>{c['S']} of {sum(c.values())} printed groups map through the cryptanalytic key (grade S), {c['C']} are read from contemporary glosses (C), and {c['I']} are proposed repairs or inferred values (I). These count token mappings, not securely understood meaning: the letters of both unresolved fragments are included in S. No surviving key has been located.</p>
  {keyrow}
  <p>The five C groups are 617, the article <em>de</em> or <em>die</em>; 115, Yarmouth (the Dutch spelling <em>Jarmuyen</em> is supplied); 109, Major-General Harrison; 76, Denmark; and 52, the queen of Sweden. The p. 523 letter says Harrison and the Anabaptists are losing influence, and that Colonel Wurts, claiming to act for Denmark, receives a Swedish pension. These meanings were already supplied by the historical translators.</p>
  <p>The printed 77 reads <em>ee</em>, but an intentional digraph and joined <code>7.7</code> are both possible. The singleton 57 is read as <em>ee</em> by inference. In P523.2, <code>43</code> is left unknown in the key and provisionally read <em>ba</em> in <em>ana[ba]ptisten</em>; splitting it into <code>4.3</code> gives those letters, while a syllable code is another possibility. <code>frac</code> denotes the fraction-like printed sort read as <em>ij</em>.</p>
  <p>A conditional key-shuffle test on the 322 printed groups gives z = 18.0, p = 0.001 (1,000 shuffles, repository Dutch corpus). Code and unknown boundaries, <em>ij</em> and <em>ee</em> are held fixed; only the single-letter S values are shuffled, and no repairs are applied. This compares the chosen key with random relabellings, not with all keys obtainable by a search, and gives no probability that an individual repair is correct. A separate ciphertext-only annealing experiment on the archived 308-group discovery corpus recovers 17–18 of 22 letter values in its best seeds. See the <a href="{repo}/blob/main/vande-perre-1653/README.md#method-and-what-the-controls-say">method notes</a>.</p>
</section>
<section>
  <h2>Proposed repairs</h2>
  <p>The printed digits are kept as they are in <code>transcription.txt</code>; each change below is applied only in the reading.</p>
  <table class="key"><thead><tr><th>Run.position</th><th>Printed</th><th>Read as</th><th>Reason</th></tr></thead><tbody>{reprows}</tbody></table>
</section>
<section>
  <h2>Open points</h2>
  <ul>
    <li>P522.2 <code>diemnicvndament</code> is glossed “who upon good grounds”. The conjecture <em>die met fvndament</em> requires three consecutive substitutions: position 5, <code>17 → 7</code> (<em>n → e</em>); position 6, <code>12 → 27</code> (<em>i → t</em>); and position 7, <code>5 → 8</code> (<em>c → f</em>). Normalizing <em>v</em> to <em>u</em> is separate. The original wording is unresolved.</li>
    <li>P582.4 <code>ote</code>, after English “fleet”, is unresolved. A retained Dutch word ending, <em>[vl]ote</em> or <em>[vlo]ote</em>, is a possibility: the paragraph also juxtaposes English “to look to them” with Dutch <em>bewaren</em>, and “want of masts” with <em>gebreck van masten bevonden</em>. No prefix is encoded by the surviving three groups.</li>
    <li>P522.4 literally reads <code>tenprincipaln</code>. The proposed <em>ten principal [e]n</em> supplies an <em>e</em>; word division alone does not produce it. The boundary and exact wording remain uncertain.</li>
    <li>The letter values have no <em>u</em>: 28 is <em>v</em>, and <em>gespeurt</em> and <em>gequalificeert</em> print 17 (<em>n</em>) where <em>u</em> is wanted. Either <em>u</em> was written with the <em>n</em> symbol or the print confuses 16 and 17 (16 never occurs).</li>
    <li>The 29 August letter announces a cipher sent “by a third hand”: “a character to open a lockt chest, <em>ick segghe een cijffer</em>”. The cipher was discussed again on 5 September and its safe receipt acknowledged on 3 October. These references do not establish whether the enclosure contained an alphabet, a code list, or both.</li>
    <li>The Beverning and Vande Perre letter to Boreel of 1 September 1653 (p. 435) uses a different cipher and remains unread.</li>
  </ul>
</section>
<section>
  <h2>Further manuscript evidence</h2>
  <p>The strongest next source is <a href="https://archives.bodleian.ox.ac.uk/repositories/2/archival_objects/820123">Bodleian MS. Rawl. A.7, old p. 47</a>: Van de Perre to Bruyne, 17 October 1653, explicitly catalogued as a copy partly in Dutch and partly in cipher. <a href="https://archive.org/details/CatalogiCodicumManuscriptorumBiblioth/page/n13/mode/1up">Macray’s 1862 catalogue, col. 12, item 4</a>, lists it among material omitted from Birch. The manuscript has not been seen, its calendar style is unspecified, and use of this key is unverified.</p>
  <p>Two Zeeland bundles are verified catalogue leads: <a href="https://hdl.handle.net/21.12113/7EE8C3AD46AB40FC882D10532E14648A">access 2, inventory 3188</a>, Johan de Brune’s incoming letters, 1652–1658; and <a href="https://hdl.handle.net/21.12113/22565F7402054D48A6003DDC0EFA75F3">inventory 3101.1</a>, England correspondence, 1652–1656, explicitly including copies returned by the other envoys after Van de Perre’s death. Both public image manifests were empty on 19 September 2026. Neither bundle’s contents have been inspected.</p>
  <p>For the damaged October passage, Birch p. 522 prints the manuscript reference “Vol. X p. 471”, although A.10 mainly covers December 1653–February 1654. A.6 contains other 10 October letters at pp. 463 and 474, making A.6 p. 471 a plausible alternative to check, not a verified correction. The November passage points to A.8 old p. 102. Old pagination needs confirmation against modern foliation.</p>
  <p>The reverse letter, De Bruyne to Van de Perre, <a href="https://archive.org/details/collectionofstat01thur/page/n581/mode/1up">31 October 1653 NS, Birch p. 552</a>, contains <code>118</code> without a resolving gloss. It is a likely code group with unknown meaning and unverified key, recorded separately from the 322 outbound groups.</p>
  <p>Searches of Birch’s OCR, Colenbrander’s first-war documents, the <em>First Dutch War</em> indexes and relevant text, and the Bodleian and Zeeland catalogues found no parallel wording that resolves either damaged fragment. These were targeted searches, not an inspection of every manuscript or printed page. The 1725 embassy <em>Verbael</em> remains incompletely inspected. The <a href="{repo}/blob/main/vande-perre-1653/evidence-audit/README.md">evidence audit</a> records coverage and retained sources; the <a href="{repo}/blob/main/vande-perre-1653/evidence-audit/ARCHIVAL-TARGETS.md">retrieval specification</a> identifies the next documents. No key or target manuscript image has been obtained.</p>
</section>
<section>
  <h2>Sources and files</h2>
  <p>Thomas Birch, ed., <em>A Collection of the State Papers of John Thurloe</em>, vol. 1 (London, 1742), Internet Archive <a href="https://archive.org/details/collectionofstat01thur">collectionofstat01thur</a>:</p>
  <ul>{sources}</ul>
  <p>The envoy is identified as Paulus in Birch’s index and the <a href="https://www.dbnl.org/tekst/molh003nieu05_01/molh003nieu05_01_0674.php">NNBW biography</a>.</p>
  <p>Satoshi Tomokiyo, <a href="https://cryptiana.web.fc2.com/code/unsolved.htm">Unsolved Historical Ciphers</a>, “Dutch ciphers (1653)”. The page is generated from <code>transcription.txt</code>, <code>key.json</code> and <code>repairs.json</code> in the <a href="{repo}/tree/main/vande-perre-1653">repository</a>, where <code>verify.py</code> reproduces the reading and <code>solve.py</code> the ciphertext-only search.</p>
</section>"""
    (docs / "vandeperre-reading.html").write_text(page(
        "Vande Perre to de Bruyne, 1653",
        "The Dutch cipher in Thurloe's intercepts of Vande Perre's letters to the pensionary of Zeeland, August-November 1653, read from Birch's printed digits: a disposition to negotiate, the government's impatience, ten ships run, want of masts.",
        body))
