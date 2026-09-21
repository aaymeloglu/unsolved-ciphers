"""Render the annotated manuscript edition without publishing source photographs."""
import html
import json
import re


def inline(text):
    text = html.escape(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', text)
    return text


def paragraphs(text):
    return ''.join('<p>'+inline(p)+'</p>' for p in text.split('\n\n'))


def build(root, docs, repo, page):
    folder = root / 'starhemberg-1758/edition-2026-09-21'
    read = lambda name: json.loads((folder / name).read_text())
    passages = read('passages.json')
    rows = {r['line']: r['transcription'] for r in read('manuscript-lines.json')}
    verification = read('verification.json')
    base = repo + '/blob/main/starhemberg-1758/edition-2026-09-21/'
    link = lambda name, label: f'<a href="{base}{name}">{label}</a>'
    body = f'''<p class="crumbs"><a href="index.html">Unsolved ciphers</a> / Starhemberg</p>
<header class="masthead">
  <p class="eyebrow">Paris, 23 May 1758 · 21 manuscript cipher lines · 1,726 digits</p>
  <h1>Chiffre aus Paris</h1>
  <p class="standfirst">Starhemberg on the memorandum to Wall, Farinelli’s matching statement, and hopes that ceding Minorca to Spain would bring Spain into the war.</p>
  <p class="status">Substantially deciphered, with a complete proposed reading</p>
</header>
<section class="wide"><h2>Reading and evidence</h2><div class="two"><div>
<p>The surviving 1752 Austrian Prima/Secunda key supports a connected reading of the letter. The central sentence pairs <strong>Farinelli speaking to the recipient</strong> with <strong>Wall speaking to the French ambassador</strong>: their closely agreeing statements raise hopes of Spanish participation. The letter also concerns forwarding reports, the memorandum delivered to Wall, and further confidential negotiations.</p>
<p>This is a reconstruction with <strong>eleven conjectural digit-edit sites</strong>, four contextual readings of 99 as g, and several uncertain key variants. The reconstruction covers the whole letter; uncertainty concerns particular words, repairs and conventions, rather than large unread passages. An exact decipherment is not established. Square brackets flag substantial restorations or lexical doubts. Spelling, word boundaries, inflection and expansion of abbreviated key entries are editorial throughout; unbracketed prose does not certify every ending.</p>
</div><div>
<p>Manuscript photographs supplied by <strong>Satoshi Tomokiyo</strong>, with <strong>Alexandre Pillon’s permission</strong>, on 21 September 2026 support the collation. The margin shows five digits absent from the Cryptiana transcription: 5 at the end of V1, 11 at V2, and 31 at V9. The photographed digits are preserved separately from the proposed repairs.</p>
<p>R means recto and V verso. Cipher paragraph boundaries fall within some manuscript lines, so boundary lines repeat below. Spacing and punctuation retain transcription conventions; control placements require explicit interpretation. The final digit of the group adopted as 31405 in V5 may be 5 or 6.</p>
<p>{link('README.md', 'Full annotated edition')} · {link('manuscript-tokens.json', 'Graded source tokens')} · {link('emended-tokens.json', 'Graded emended tokens')} · {link('alignment.tsv', 'Token-to-manuscript alignment')}</p>
</div></div></section>'''
    for i, p in enumerate(passages):
        cipher = ''.join(f'<p><span class="rn">{r}</span>{html.escape(rows[r])}</p>' for r in p['rows'])
        source = f'<div class="rows">{cipher}</div>' if cipher else '<p class="clear">Written in clear in the manuscript.</p>'
        body += f'''<section class="folio" id="passage-{i}">
<header class="folio-head"><h2>{p['title']}</h2><p>{'Ciphertext and reconstructed reading' if cipher else 'Manuscript prose'}</p></header>
<div class="cols"><figure class="scan">{source}<figcaption>Transcription; source photographs are not reproduced.</figcaption></figure>
<div class="col it"><h3>German</h3>{paragraphs(p['de'])}</div>
<div class="col en"><h3>English</h3>{paragraphs(p['en'])}</div></div>
<div class="apparatus"><h4>Reading note</h4><p>{inline(p['note'])}</p></div></section>'''

    repairs = ''.join(f"<tr><td>{e['offset']}</td><td><code>{e['from']} → {e['to'] or '∅'}</code></td><td>{html.escape(e['reason'])}</td></tr>" for e in read('emendations.json')['edits'])
    body += f'''<section class="wide"><h2>What remains uncertain</h2><div class="two"><div>
<ul>
<li><strong>Opening adjective:</strong> the roots so / stat? / lich suggest stattlich, but the wording and translation “impressive” remain tentative.</li>
<li><strong>Bereit and Verlangen:</strong> contextual readings. The key gives berg at the group adopted as 31405; the alternative 31406 does not establish bereit. The letters of 31427 remain uncertain.</li>
<li><strong>Gegen:</strong> longer handwritten ge-variants at Prima 31115 and Secunda 31010/31126 appear to give gege. Their exact letters remain a paleographic judgment, supported by three contexts.</li>
<li><strong>Four 99 values:</strong> Hoffnung twice, vorsichtig and gschicktes require an inferred g. The numerical tables give Prima 99 = man and Secunda 99 = er. Alphabetical g headings have gg-like forms resembling 99, which could explain an encipherer’s mistake but do not establish a general 99 = g mapping. Secunda er remains appropriate in Zi / n / er, normalized to Zinner.</li>
</ul></div><div><ul>
<li><strong>Framing:</strong> unmarked 883 occurs at both boundaries. Treating the pair as framing is a hypothesis not documented by the inspected instructions. Both groups remain in the source.</li>
<li><strong>Punctuation and the peace join:</strong> the initial 854 boundary requires interpreting a displaced mark. The manuscript’s defective 119 at the recto/verso join is suppressed in the proposed reading; an alternative restoring en has equal edit cost.</li>
<li><strong>Minorca:</strong> the literal connective is scho / n. Its rendering as “indeed,” punctuation, and the relation of the clauses are editorial. The passage is not evidence of an unconditional Spanish promise.</li>
<li><strong>Recipient:</strong> the letter supplies no personal name. Rosenberg is a contextual possibility. “This court” is interpreted as the Spanish court, although the author writes from Paris.</li>
</ul></div></div>
<p>Further investigation could include a complete audit of the key’s handwritten alternatives and extended comparison with surviving worked examples and contemporary decipherments, especially for 99 and repeated 55. These avenues have not been exhausted, but no specific comparison has been identified that would resolve those readings, and no recovery from these proposed checks has been demonstrated. Whether further work would improve the decipherment is unknown. The proposed repairs remain conjectural.</p>
</section>
<section class="wide"><h2>Explicit proposed repairs</h2>
<p>These eleven sites cost thirteen digit edits. None is an observed correction from the photographs. Offsets are zero-based positions in the 1,721-digit Cryptiana baseline; {link('alignment.tsv', 'the alignment')} gives physical manuscript positions. Contextual g readings, framing and grammatical expansion are additional assumptions.</p>
<div class="scroll"><table><thead><tr><th>Baseline offset</th><th>Digit edit</th><th>Reason</th></tr></thead><tbody>{repairs}</tbody></table></div></section>
<section class="wide"><h2>Reproducibility and evidence grades</h2><div class="two"><div>
<p>The manuscript parse conserves all <strong>1,726 digits</strong>, with 413 units and two structurally invalid groups. The separately emended stream has 1,721 digits, 404 units and no invalid groups. Its length matching the Cryptiana baseline is coincidental. Table switches remain Prima 876 → Secunda and Secunda 899 → Prima.</p>
<p>Source grades: <strong>398 H, 12 M, 3 I</strong>. Emended grades: <strong>378 H, 8 M, 18 I</strong>. H denotes historical key evidence; M uncertainty; I inference. Counts include nulls and controls. The three source I units are the framing pair and displaced punctuation. These grades do not measure authenticated prose or transcription accuracy.</p>
</div><div><p>Run <code>python3 starhemberg-1758/run_checks.py</code> from the repository root. The edition’s <code>build.py --check</code> verifies committed outputs. Digit conservation, explicit repair accounting, two table switches and the valid emended parse are mechanical checks, not independent authentication of the conjectures.</p>
<p>{link('collation.json', 'Observed collation')} · {link('key-evidence.json', 'Key evidence')} · {link('emendations.json', 'Repair ledger')} · {link('verification.json', 'Verification')} · {link('manuscript-roots.txt', 'Source roots')} · {link('emended-roots.txt', 'Emended roots')}</p>
</div></div></section>
<footer class="colophon"><div><h3>Sources and attribution</h3>
<p><a href="https://cryptiana.web.fc2.com/code/variable2.htm#Starhemberg">Cryptiana transcription, credited to Alexandre Pillon</a>; manuscript photographs via Satoshi Tomokiyo with Pillon’s permission. Neither those photographs nor the DECODE images are redistributed.</p>
<p>1752 key: <a href="https://de-crypt.org/decrypt-web/RecordsView/1695">DECODE R1695</a> and <a href="https://de-crypt.org/decrypt-web/RecordsView/1698">R1698</a>. Instructions and worked example: <a href="https://de-crypt.org/decrypt-web/RecordsView/1696">R1696</a> and <a href="https://de-crypt.org/decrypt-web/RecordsView/1697">R1697</a>. Facsimiles accessed with the DECODE project's permission.</p>
</div><div><h3>Research</h3><p><a href="https://doi.org/10.1080/01611194.2025.2457096">Antal, Mírka and Kováč</a> describe the cipher system, not a solution of this letter. <a href="https://archive.org/stream/mmoiresetjournal01will/mmoiresetjournal01will_djvu.txt">Wille’s journal</a>, 5 September 1759, vol. 1, p. 120, names a courier Zinner; this does not prove identity.</p>
<p>Research and edition: Andy Aymeloglu with OpenAI Codex, 17–21 September 2026. Substantially deciphered, with a complete proposed reading and explicit uncertainties. No claim of a first decipherment. {link('README.md', 'Edition and sources')}.</p></div></footer>'''
    # Ensure the summary and edition counts cannot silently diverge.
    assert verification['grade_counts'] == {'manuscript': {'H': 398, 'M': 12, 'I': 3}, 'emended': {'H': 378, 'M': 8, 'I': 18}}
    (docs / 'starhemberg-reading.html').write_text(page('Chiffre aus Paris', 'Starhemberg, 23 May 1758: substantially deciphered, with a complete proposed German reading, English translation and explicit uncertainties.', body))
