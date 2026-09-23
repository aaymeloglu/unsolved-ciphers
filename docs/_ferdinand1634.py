"""The partial 1634 reading within the three-letter Ferdinand correspondence page."""
import csv
import html
import json


def build_section(root, repo):
    folder = root / 'ferdinand-1634'
    rows = list(csv.DictReader((folder / 'alignment.tsv').open(), delimiter='\t'))
    spans = json.loads((folder / 'apparatus.json').read_text())
    grades = json.loads((folder / 'grades.json').read_text())
    escape = html.escape
    link = f'{repo}/blob/main/ferdinand-1634'
    descriptions = [
        ('The welfare of the House of Austria', 'After the clear salutation and cum, p. 1',
         'The proposed opening concerns establishing the welfare of “our most august house.” The intended formula is recognizable, but two vowel readings require editorial correction. The two terminal signs have inherited empty assignments.'),
        ('Protected princes and the French expedition', 'After facile colligere liceat, pp. 1–2',
         'Readable stretches concern princes who have placed themselves under another’s protection, especially Württemberg and Baden-Durlach; the effects on both correspondents’ interests; and efforts against their house’s enemies. The exact construction after “he … no …” remains unresolved. The conjecture intermissurum would mean “would leave unattempted,” but it is not established. The subject should not be identified more specifically as the French king from this reading alone.'),
        ('A request for an armed diversion', 'After Eandem perbenevole rogans, p. 2',
         'The wording refers to attention divided among several directions, military movement and diversion, and the common interest of the House of Austria. The surrounding clear text invokes the glory of Nördlingen. The means requested, the middle of the sentence and the final comparison remain uncertain; this is a summary of recognizable content, not a complete translation.'),
        ('The closing request', 'p. 3, followed by the same words in clear',
         '“Not refuse to advance [it].” The seventeen cipher groups reproduce promovere haud dedignetur, allowing u/v normalization. The three following signs remain outside this direct match.'),
    ]

    def proposed(span):
        if span['status'] == 'terminal':
            return f'<span class="loc">⟦terminal: {escape(span["literal"] or "∅") }⟧</span>'
        if span['proposed'] is None:
            return f'<code>⟦{escape(span["literal"])}⟧</code>'
        text = escape(span['proposed'])
        if span['status'] == 'conjecture':
            text = '[' + text + '?]'
        elif span['status'] == 'emendation':
            text += '<sup>†</sup>'
        return f'<span title="{escape(span["id"] + ": " + span["note"], quote=True)}">{text}</span>'

    parts = [f'''
<section class="wide" id="letter-1634">
  <h2>1634: the French Rhine expedition</h2>
  <p class="legend">Ferdinand, King of Hungary and Bohemia, to Cardinal-Infante Ferdinand · Stuttgart, 28 October 1634 · DECODE R1887</p>
  <span class="status">Partial decipherment · several passages remain unresolved</span>
  <p>This letter uses a separate repertoire of graphic signs, numbers and syllable groups. Repeated formulas and the surrounding clear Latin constrain a proposed key; no external key or corresponding plaintext draft was used. The cleartext repetition of the closing phrase provides a direct check.</p>
  <p>The elected transcription contains {grades['tokens']} groups, including one partly clipped group provisionally counted as one. {grades['unknown']} occurrences are unmapped and {grades['assigned_empty']} have inherited empty assignments. Assigned values are not a measure of verified accuracy. The <a href="{link}/alignment.tsv">source alignment</a> retains probable readings and alternatives.</p>
  <p class="legend">Left: elected cipher labels. Middle: proposed Latin; † marks an editorial emendation, [word?] a conjecture, and ⟦…⟧ unresolved literal output. Orthographic normalization is recorded in the apparatus. Right: the sense of recognizable stretches, not a continuous translation. Each fold-out shows literal output and the evidence needed for the proposed reading.</p>
</section>''']
    for seg, (title, context, sense) in enumerate(descriptions):
        rr = [r for r in rows if int(r['segment']) == seg]
        aa = [a for a in spans if a['segment'] == seg]
        cipher = []
        for line in dict.fromkeys(r['physical_line'] for r in rr):
            tokens = ' '.join(r['token'] for r in rr if r['physical_line'] == line)
            cipher.append(f'<p><span class="rn">{line}</span> {escape(tokens)}</p>')
        notes = []
        for a in aa:
            changes = '; '.join(f'{e["before"] or "∅"} → {e["after"] or "∅"}' for e in a['edits'])
            notes.append(f'<tr><td class="ln">{a["id"]}<br>{a["first"]}–{a["last"]}</td><td class="tok">{escape(a["literal"] or "∅")}</td><td>{proposed(a)}</td><td><b>{escape(a["status"])}</b><br>{escape(a["note"])}' +
                         (f'<br><small>Letter changes: {escape(changes)}</small>' if changes else '') + '</td></tr>')
        latin = ' '.join(proposed(a) for a in aa)
        parts.append(f'''
<section class="folio" id="r1887-passage-{seg+1}">
  <header class="folio-head"><h2>{title}</h2><p>R1887 · {context}</p></header>
  <div class="cols">
    <figure class="scan"><div class="rows">{''.join(cipher)}</div><figcaption>Transliterated graphic labels and cipher groups from <a href="{link}/transcription.txt">the elected transcription</a>. A caret denotes a diacritic; p? is a clipped p-initial group. Private manuscript images are not redistributed.</figcaption></figure>
    <div class="col it"><h3>Proposed Latin · partial</h3><p>{latin}</p></div>
    <div class="col en"><h3>Sense and limits</h3><p>{sense}</p></div>
  </div>
  <div class="apparatus"><details class="groups"><summary>Literal output and reading decisions</summary>
    <div class="scroll"><table><thead><tr><th>Span and occurrence IDs</th><th>Literal output</th><th>Proposed wording</th><th>Evidence and editorial changes</th></tr></thead><tbody>{''.join(notes)}</tbody></table></div>
    <p class="fn">The literal column applies the published key without editorial repairs; ∅ is an assigned empty value and ? is unmapped. Letter edits include both normalization and substantive emendation. The <a href="{link}/apparatus.json">machine-readable apparatus</a> records exact character offsets.</p>
  </details></div>
</section>''')
    parts.append(f'''
<section class="wide" id="key-1634">
  <h2>The 1634 key and its limits</h2>
  <div class="two"><div>
    <p>The proposed syllable families generally retain the plaintext vowel: <code>ab … ub</code> give <em>ma … mu</em>, <code>xar/xer/xir/xur</code> give <em>ta/te/ti/tu</em>, and <code>pan/pen/pin/pun</code> give <em>la/le/li/lu</em>. Graphic homophones and numerical syllables supplement them. These assignments are reconstructed from context; they do not come from a surviving key sheet.</p>
    <p>The visible <code>#</code> after <code>hi</code> supplies the s in <em>-tendis hisce</em>. A second, partly clipped group is recorded as <code>p?</code>. Distinct flat, stemmed and compound oval signs are kept separate rather than forced into one value.</p>
    <p><a href="{link}/key.json">Proposed key</a> · <a href="{link}/observations.json">Source alternatives and conditional hypotheses</a> · <a href="{link}/literal.txt">Full literal output</a></p>
  </div><div>
    <p><em>Intermissurum</em> still requires tin → tun. <em>Subvertendis</em> requires joining separate <code>10 8</code> as an unverified <code>108=b</code>. <em>Facilius mihi</em> requires a new value f for the flat oval and completion of the clipped group to pin. These conjectural values are not installed in the key.</p>
    <p>Literal grades: <b>17 C, 457 M</b>. C is restricted to the closing phrase directly matched to cleartext. M covers contextual assignments and unresolved signs, without implying that all are equally doubtful. Non-orthographic supplied or changed letters in the proposed text are separately graded I. There is no H or S claim for 1634.</p>
    <p>The <a href="{link}/verify.py">portable verifier</a> reproduces 474 groups and checks all 38 reading spans, the amendments, grades and isolation of conjectural values. It checks consistency, not the truth of every reading. Exploratory fixed-key shuffle scores were not adjusted for key search and manual selection and are not used here as accuracy claims.</p>
  </div></div>
</section>''')
    return '\n'.join(parts)
