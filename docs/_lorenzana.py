"""Build the facing Italian and English texts from the Lorenzana edition."""
import csv
from html import escape


def paragraphs(path):
    return [escape(block) for block in path.read_text().strip().split("\n\n")
            if not block.startswith("#")]


def build(root, docs, page, crumbs, repo):
    folder = root / "lorenzana-1432"
    source = f"{repo}/tree/main/lorenzana-1432"
    pairs = zip(paragraphs(folder / "reading-it.md"),
                paragraphs(folder / "translation-en.md"), strict=True)
    reading = "\n".join(f'<div class="two"><p lang="it">{it}</p><p>{en}</p></div>'
                        for it, en in pairs)
    with (folder / "april.tsv").open() as stream:
        runs = list(csv.DictReader(stream, delimiter="\t"))
    with (folder / "literal.tsv").open() as stream:
        literal = dict(csv.reader(stream, delimiter="\t"))
    rows = "\n".join(f'<tr><th scope="row">{escape(run["line"])}</th>'
                     f'<td><code>{escape(run["signs"])}</code></td>'
                     f'<td lang="it">{escape(literal[run["line"]])}</td></tr>'
                     for run in runs)
    title = "Bernardo de’ Medici to Averardo, 17 April 1432"
    desc = "From Lorenzana, Bernardo asks whether Florence means his men to plunder the inhabitants of five castles."
    body = f"""{crumbs.format(f'<a href="{source}">Write-up and files</a>')}
<header class="masthead"><p class="eyebrow">Lorenzana · 17 April 1432 · ASF MAP V, c. 208r</p>
<h1>{title}</h1><p class="standfirst">{desc}</p></header>
<main><section class="wide"><h2>The letter</h2>
<p>Italian and English, paragraph by paragraph. Brackets mark uncertain words, gaps and editorial supplies.</p>
<div class="two"><h3>Italian</h3><h3>English</h3></div>{reading}</section>
<section class="wide"><h2>The cipher in manuscript order</h2>
<p>Twenty sign values come from a glossed letter of 8 December 1431. Five more are inferred from this letter.
The table shows the literal key output with proposed word divisions. The Italian above regularizes spelling.</p>
<div class="scroll"><table><thead><tr><th>Line</th><th>Cipher signs</th><th>Literal reading</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<p><a href="https://archiviodistatofirenze.cultura.gov.it/map/riproduzione/?id=6242">Manuscript recto</a> ·
<a href="{source}">Key, evidence grades and verification</a></p></section></main>"""
    (docs / "lorenzana-reading.html").write_text(page(title, desc, body))
