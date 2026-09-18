"""Build the Ferdinand reading from the published Markdown editions and transcripts."""
import html
import re


def quoted_paragraphs(path, heading, end_heading):
    text=path.read_text().split(heading,1)[1].split(end_heading,1)[0]
    paragraphs=[]
    current=[]
    for line in text.splitlines()+['']:
        if line.startswith('>'):
            part=line[1:].strip()
            if part:
                current.append(part)
                continue
        if current:
            paragraphs.append(' '.join(current))
            current=[]
    assert paragraphs, (path,heading)
    return ''.join('<p>'+html.escape(re.sub(r'\*\*(.*?)\*\*',r'\1',p))+'</p>' for p in paragraphs)


def build(root, docs, page, crumbs, repo):
    folder=root/'ferdinand-1635-1640'
    sections=[]
    for year,record,suffix,title,desc in [
        ('1635','R1889','working','Winter quarters at Trier','Brussels, 16 November 1635 · Cardinal-Infante Ferdinand to the future Ferdinand III'),
        ('1640','R1890','reviewed','Recruitment and 100,000 florins','Vienna, 22 February 1640 · Ferdinand III to Cardinal-Infante Ferdinand')]:
        edition=folder/f'READING-{year}.md'
        latin=quoted_paragraphs(edition,'## Readable Latin','## English translation')
        english=quoted_paragraphs(edition,'## English translation','## Apparatus')
        cipher=[]
        for line in (folder/f'transcriptions/{record}-{suffix}.txt').read_text().splitlines():
            if line and not line.startswith('#'):
                label,text=line.split(' ',1)
                cipher.append(f'<p><span class="rn">{html.escape(label)}</span> {html.escape(text)}</p>')
        literal_name='R1889-expanded-literal.txt' if year=='1635' else 'R1890-supplemented-reviewed-literal.txt'
        literal=html.escape((folder/'results'/literal_name).read_text())
        notes=('The draft supports the supplied readings, including civitas and iam. Their cipher signs remain disputed. '
               'The city name, surrounding-places wording and verb forms differ at some points between draft and copy.' if year=='1635' else
               'One obscured sign and two occurrences of 14 remain unmapped. Hatzfeld is a probable name identification. '
               'The literal output retains igitua, materi and expredse; the Latin edition marks their repairs.')
        sections.append(f'''<section class="folio" id="letter-{year}">
<header class="folio-head"><h2>{title}</h2><p>{desc}</p></header>
<div class="cols">
<div class="col cipher"><h3>Cipher transcription</h3><div class="rows">{''.join(cipher)}</div></div>
<div class="col it"><h3>Readable Latin</h3>{latin}</div>
<div class="col en"><h3>English translation</h3>{english}</div>
</div>
<div class="apparatus"><h4>Reading notes</h4><p>{notes}</p>
<p><a href="{repo}/blob/main/ferdinand-1635-1640/READING-{year}.md">Full discrepancy apparatus</a> ·
<a href="{repo}/blob/main/ferdinand-1635-1640/transcriptions/{record}-{suffix}.txt">Transcription</a></p>
<details><summary>Literal decoder output, with no editorial repairs</summary><pre style="white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px;line-height:1.6">{literal}</pre></details>
</div></section>''')
    body=f'''{crumbs.format(f'<a href="{repo}/tree/main/ferdinand-1635-1640">Ferdinand: write-up and files</a>')}
<header class="masthead">
<p class="eyebrow">Brussels, Secrétairerie d'État Allemande, inv. 540 · 1635 / 1640</p>
<h1>Winter quarters and the price of recruitment</h1>
<p class="standfirst">Two ciphered letters between Cardinal-Infante Ferdinand and Ferdinand III: a refusal of imperial winter quarters at Trier, and an urgent request for 100,000 florins to raise troops in Westphalia.</p>
<p class="status">Both bodies readable · residual signs and copying errors</p>
</header>
<div class="lede"><div>
<h3>The recovered correspondence</h3>
<p>In 1635 the Cardinal-Infante argues that Trier's royal garrison and the prince-elector need the local resources, making it difficult to quarter imperial troops there. In 1640 Ferdinand III orders counter-recruitment in response to preparations by the Elector of Cologne and the Westphalian estates. He asks for money to be placed with his commissioners in Cologne, subject to controlled disbursement.</p>
<p><a href="#letter-1635">Read 1635</a> · <a href="#letter-1640">Read 1640</a> · <a href="{repo}/tree/main/ferdinand-1635-1640">Evidence and reproducible decoder</a></p>
<h3>How to read this edition</h3>
<p>The columns show the transcription, edited Latin and English for each whole letter; they are not word-aligned. Cipher row labels are retained. Braces in the transcription enclose clear writing. Square brackets in the Latin mark supplied or repaired readings; the translation incorporates those restorations. Literal output below each letter preserves unknown signs and malformed words.</p>
</div><div><div class="callout"><h3>What is established</h3>
<p>The 1635 draft R954 and cipher R1889 were already linked by DECODE. Their alignment supplied the alphabet, which was tested on a separate passage. Applying it unchanged to 1640 was followed by a distinct syllable supplement: 60 added values, no changes to the earlier assignments. The two pages then read continuously. A complete historical key sheet has not been recovered.</p>
<p>Prior publication remains unestablished. No first-solve or discovery claim is made. Several exact glyph readings, singleton assignments and apparent copying errors remain explicitly qualified.</p></div>
<details><summary>Evidence grades and limitations</summary>
<p>1635: 445 C, 18 M. Reviewed 1640: 416 C, 347 M, 19 I. C means a value derived from the 1635 plaintext draft. The contextual 1640 additions remain conservatively M, with no controlled cryptanalytic S claim. I marks reviewed source amendments. Grades concern the literal units, not the editorial restorations in the Latin.</p></details>
</div></div>
{''.join(sections)}
<footer class="colophon"><div><h3>Sources</h3>
<p>DECODE <a href="https://de-crypt.org/decrypt-web/RecordsView/954">R954</a>, <a href="https://de-crypt.org/decrypt-web/RecordsView/1889">R1889</a> and <a href="https://de-crypt.org/decrypt-web/RecordsView/1890">R1890</a>. Source ciphertext transcriptions by XZ, January 2021; our working layers record normalization and image-review amendments. Manuscript images were accessed with the DECODE project's permission and are not redistributed.</p>
<p><a href="{repo}/blob/main/ferdinand-1635-1640/SOURCES.md">Source and prior-publication audit</a></p>
</div><div><h3>Reproduce and inspect</h3><p>Run <code>python3 verify.py</code> in the published Ferdinand directory. It checks the committed readings, evidence tables and grades without modifying them. The full Latin apparatus distinguishes draft variants, source-review amendments and editorial repairs.</p>
<p>Research and publication: 18 September 2026. <a href="{repo}/blob/main/ferdinand-1635-1640/1634-ASSESSMENT.md">The separate 1634 cipher remains open.</a></p></div></footer>'''
    (docs/'ferdinand-reading.html').write_text(page('Ferdinand correspondence, 1635 / 1640','Cipher transcriptions, recovered Latin and English translations of the Ferdinand correspondence, with evidence and explicit remaining gaps.',body))
