"""Write this edition in Cyphersolver's layout, for targets/ercole1544/aymeloglu/.

    uv run python gonzaga-1545/export_cyphersolver.py <path to targets/ercole1544/aymeloglu>

Writes the transcriptions and decryptions with WAINUT's line labels (A 78r ... G 175v), the reading
and translation as IT[..]/EN[..] blocks from the README table with Cyphersolver's hole marks,
departures.tsv, doubts.md (the lines for NOTES.md "## Transcription doubts"), key.tsv,
vatican-register.md, the frozen transcriptions and the blind readers' rows.
"""
import difflib
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_edition as ce  # noqa: E402
import decode  # noqa: E402

LAB = {"A78r": "A", "A78v": "B", "A79r": "C", "B174r": "D", "B174v": "E", "B175r": "F", "B175v": "G"}
SIDE = {"78r": "A", "78v": "B", "79r": "C", "174r": "D", "174v": "E", "175r": "F", "175v": "G"}
META = {"A": ("0078_0079", "cc. 78r-79r, Ercole Gonzaga to Ferrante Gonzaga, Mantua, 4 May 1544", ["A78r", "A78v", "A79r"]),
        "B": ("0174_0175", "cc. 174r-175v, Ercole Gonzaga to Ferrante Gonzaga, Mantua, 9 January 1544", ["B174r", "B174v", "B175r", "B175v"])}
# README marks that Cyphersolver writes differently: a doubtful or unread stretch inside a word, with its size in words.
FIX = [("pensau[28]a", "[?pensaua]"), ("Mirand…la", "[?Mirandola]"), ("manda… fra", "[... 3] fra"), ("disfa…rla", "[?disfarla]"),
       ("particol…ar", "[?particolar]"), ("uo… operar…", "[?uole] [?operar]"), ("illustrissi… a", "[?illustrissime] a"),
       ("bisogno di …,", "bisogno di [... 3],")]


def lines(path):
    return [ln for ln in open(os.path.join(HERE, path), encoding="utf-8").read().split("\n") if ln.strip()]


def conv(x):
    for a, b in FIX:
        x = x.replace(a, b)
    x = re.sub(r"\[([^\]\[?]+)\?\]", r"[?\1]", x)
    return x.replace("…", "[...]")


def tag(c):
    p1, l1, p2, l2 = re.match(r"(\d+[rv]) (\d+)(?:\s*–\s*(?:(\d+[rv]) )?(\d+))?", c).groups()
    return f"{SIDE[p1]}{int(l1):02d}-{SIDE[p2 or p1]}{int(l2 or l1):02d}"


def main(out):
    os.makedirs(os.path.join(out, "frozen"), exist_ok=True)
    os.makedirs(os.path.join(out, "blind"), exist_ok=True)
    w = lambda name, rows: open(os.path.join(out, name), "w", encoding="utf-8").write("\n".join(rows) + "\n")
    readme = open(os.path.join(HERE, "README.md"), encoding="utf-8").read()
    sec = readme[readme.index("## Reading"):readme.index("### Where the January cipher breaks off")]
    part = {"A": sec[sec.index("### Letter A"):sec.index("### Letter B")], "B": sec[sec.index("### Letter B"):]}
    for name, (f, title, pages) in META.items():
        rows = [[x.strip() for x in ln.strip().strip("|").split(" | ")] for ln in part[name].split("\n") if re.match(r"\| \d", ln)]
        it = [f"# Reading of {title} (Andrew Aymeloglu, 25 Nov 2026)", "",
              f"Built from `transcription_{f}.txt` and `decryption_{f}.txt` in this folder. Line labels are those of WAINUT's files in the parent folder (A 78r, B 78v, C 79r, D 174r, E 174v, F 175r, G 175v).", "",
              "Marks: an unmarked word is what the key gives for the signs, in their spelling; word division, capitals and punctuation are editorial. A letter in brackets inside a word (`co[n]`, `[g]enti`) is supplied: the transcription has another sign there, and the word is counted as a hole. `[?word]` is a word proposed where a sign is doubtful or a code is read from context. `[...]` is one unread word and `[... 3]` three. `[63]` is a code with no value. A name or title without brackets is a code read from `key.tsv`.", ""]
        en = [f"# Translation of {title}", "", f"Same blocks and the same holes as `reading_{f}.md`.", ""]
        for c in rows:
            it += [f"IT[{tag(c[0])}]: {conv(c[1])}", ""]
            en += [f"EN[{tag(c[0])}]: {conv(c[2])}", ""]
        w(f"reading_{f}.md", it[:-1])
        w(f"translation_{f}.md", en[:-1])
        tr = [f"# {title}. Edited transcription, 25 Nov 2026.",
              "# Signs set off by spaces. Letters are cipher letters as written; 2o 3o 4o are figure groups with a ring; L is the L sign, Lnn an L with raised figures (WAINUT writes L^nn).",
              "# {a/b}: a sign in doubt between two shapes, likelier first. x!: a sign supplied by the editor where the frozen shape reading has another; see departures.tsv. ?: not read. |: a space in the line.",
              f"# Line labels as in ../transcription_{f}.txt."]
        de = [f"# {title}. Output of key.tsv on transcription_{f}.txt, line by line, unedited (decode.py).",
              "# [word]: a word or name code from the key. [x] inside a word: the letter of a supplied sign (x! in the transcription). <nn>: a group with no value. {a/b}: the two decodes of a doubtful sign. ?: not read."]
        for p in pages:
            c, d = lines(f"edition/{p}.cipher.txt"), lines(f"edition/{p}.it.txt")
            assert len(c) == len(d), p
            for i, (x, y) in enumerate(zip(c, d), 1):
                tr.append(f"{LAB[p]}{i:02d} {x}")
                de.append(f"{LAB[p]}{i:02d} {y}")
        w(f"transcription_{f}.txt", tr)
        w(f"decryption_{f}.txt", de)
    key = decode.load_key()
    blind = {}
    for n in (1, 2, 3, 4):
        for k in json.load(open(os.path.join(HERE, "blind", f"crops-set{n}.key.json"))):
            blind.setdefault((k["page"], k["line"]), []).append(k["id"])
    dep, doubts = ["label\tposition\tkind\tedited\tfrozen\tdecodes\tblind_crops_on_line"], []
    for p, lab in LAB.items():
        frozen = [ln.split() for ln in lines(f"transcription/{p}.C.txt")]
        for n, (fz, new) in enumerate(zip(frozen, [ln.split() for ln in lines(f"edition/{p}.cipher.txt")]), 1):
            sm = difflib.SequenceMatcher(a=[ce.strip_alts(t) for t in fz], b=[ce.strip_alts(t.rstrip("!")) if len(t) > 1 else t for t in new], autojunk=False)
            old = {}
            for op, i1, i2, j1, j2 in sm.get_opcodes():
                for j in range(j1, j2):
                    old[j] = fz[i1 + (j - j1)] if op == "equal" else " ".join(fz[i1:i2])
            for j, t in enumerate(new):
                kind = "supplied" if len(t) > 1 and t.endswith("!") else "doubt" if t.startswith("{") else "unread" if t in ("?", "??") else None
                if not kind:
                    continue
                d = "?" if kind == "unread" else ce.decode_for_check(t, key)
                b = ",".join(blind.get((p, n), []))
                where = f"{lab}{n:02d}, sign {j + 1}, in `{' '.join(new[max(0, j - 2):j + 3])}`"
                tailb = f"; blind crops cut on this line: {b} (aymeloglu/blind/)" if b else ""
                dep.append(f"{lab}{n:02d}\t{j + 1}\t{kind}\t{t}\t{old.get(j, '')}\t{d}\t{b}")
                if kind == "supplied":
                    doubts.append(f"- `{t.rstrip('!')}` ({where}) - read: supplied, plain {d}; checked: image, decode, transcription; the frozen shape reading has `{old.get(j, '')}` here, the word needs `{t.rstrip('!')}`, so the letter is bracketed in the reading and the word counted as a hole{tailb}")
                elif kind == "doubt":
                    doubts.append(f"- `{t}` ({where}) - read: unresolved, keeps its mark; checked: image, decode, transcription; the shape allows both and the decode does not decide{tailb}")
                else:
                    doubts.append(f"- `?` ({where}) - read: not read; checked: image, decode; blot or faded sign")
    w("departures.tsv", dep)
    w("doubts.md", doubts)
    shutil.copy(os.path.join(HERE, "key.tsv"), os.path.join(out, "key.tsv"))
    shutil.copy(os.path.join(HERE, "source-search.md"), os.path.join(out, "vatican-register.md"))
    for p in LAB:
        shutil.copy(os.path.join(HERE, "transcription", f"{p}.C.txt"), os.path.join(out, "frozen"))
    for f in os.listdir(os.path.join(HERE, "blind")):
        if f.endswith(".tsv") or f.endswith(".key.json"):
            shutil.copy(os.path.join(HERE, "blind", f), os.path.join(out, "blind"))
    print(len(dep) - 1, "departure rows;", len(doubts), "doubt lines")


if __name__ == "__main__":
    main(sys.argv[1])
