#!/usr/bin/env python3
"""Beam search over lexicon words for a homophonic cipher with known word boundaries.

Constraint: same cipher symbol -> same letter. Different symbols may share a letter.
This is the method that read the Forster letter (README, step 3); the character-model
annealer in solver.py did not.

    uv run python dict_solver.py [beam] [skip_penalty] [maxlen_forced]

The lexicon is the vocabulary of `cipherkit.corpora` fr (Xivrey's Henri IV letters, Avenel's
Richelieu, Montaigne, Brantôme, Descartes), which already carries 16th- and 17th-century
spellings (estoit, roy, luy), filtered to words seen at least three times (the Internet Archive
OCR contributes fragments below that), plus the generated variants the 2026-09 run used, the
curated 17th-century forms in lex_old.txt, and the same short list of names and forms from the
letter's world. The 2026-09 run used Corneille and Descartes from Gutenberg with a modern
frequency list; those files were not kept.
"""
import collections
import json
import math
import re
import sys

from cipherkit import BASE_FOLDS, WordLM, cached, normalize
from cipherkit.corpora import text

BEAM = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
SKIP = float(sys.argv[2]) if len(sys.argv) > 2 else -25.0
MAXLEN = int(sys.argv[3]) if len(sys.argv) > 3 else 7  # words longer than this may be skipped
ALPH = "abcdefghiklmnopqrstuxyz"  # the letter writes i for j and u for v, and has no w
FOLDS = {**BASE_FOLDS, "j": "i", "v": "u"}

# ---------- ciphertext ----------
words, cur = [], []
for ln in open("ct.txt", encoding="utf-8").read().split("\n"):
    ln = re.sub(r"\[.*?\]", "|", ln)
    for num, comma, bar in re.findall(r"(\d+|[a-z])\.?|(,)|(\|)", ln):
        if comma or bar:
            if cur:
                words.append(cur)
                cur = []
        else:
            cur.append(num)
if cur:
    words.append(cur)

# ---------- lexicon with 17th-c. variants ----------
corpus = normalize(text("fr"), alphabet=ALPH, folds=FOLDS, keep_spaces=True)
lex = cached("lex_fr_iu.pkl", lambda: WordLM.from_text(corpus), WordLM.load)
MIN_COUNT = 3  # below this a corpus "word" is usually an OCR fragment from the Internet Archive editions
freq = collections.Counter()
for w, c in lex.uni.items():
    if c < MIN_COUNT:
        continue
    if re.fullmatch(r"[ivxlc]{2,}", w) and w not in ("il", "ci", "vil"):
        continue
    if w in ("var", "ibid", "op", "cit", "fol", "vol", "tom", "sc", "sq"):
        continue
    freq[w] += c
    v = set()
    if w.endswith("ait"):
        v.add(w[:-3] + "oit")
    if w.endswith("aient"):
        v.add(w[:-5] + "oient")
    if w.endswith("ais"):
        v.add(w[:-3] + "ois")
    if w.endswith("i") and len(w) > 2:
        v.add(w[:-1] + "y")
    if w.endswith("oi"):
        v.add(w[:-2] + "oy")
    if w.endswith("ui"):
        v.add(w[:-2] + "uy")
    for x in v:
        if x != w:
            freq[x] += max(1, c // 3)
for line in open("lex_old.txt", encoding="utf-8"):
    p = line.split()
    if p and p[-1] == "50":
        freq[normalize(p[0], alphabet=ALPH, folds=FOLDS)] += 30
for w in ['exeter','excester','exester','oxford','oxfort','londres','paris','bristol','bristoll','yorck','yorke','falmouth','plimouth','plymouth','pendennis','essex','waller','digby','iermyn','jermyn','goring','hopton','maurice','rupert','ruprecht','cornouaille','cornwall','devon','somerset','bath','reyne','royne','roy','madame','maiesté','maieste','majeste','monseigneur','mazarin','mazarini','richelieu','louvre','angleterre','escosse','irlande','parlement','armee','armées','armees','cavalerie','infanterie','argent','poudre','munitions','vaisseaux','vaisseau','navire','navires','port','mer','passage','lettres','lettre','chiffre','nouvelles','secours','asseurer','asseure','asseuré','asseurance','tousiours','desia','encores','encor','ceste','cest','cestuy','ceux','celle','celles','iceluy','icelle','laquelle','lequel','lesquels','auquel','duquel','sieur','sr','mr','md','mons','vostre','nostre','sa','maté','mate','majesté','sadite','ledit','ladite','lesdits','susdit','susdite']:
    freq[normalize(w, alphabet=ALPH, folds=FOLDS)] += 40
print("lexicon size", len(freq), file=sys.stderr)
bylen = collections.defaultdict(list)
for w, c in freq.items():
    bylen[len(w)].append((w, math.log(c + 1)))
for k in bylen:
    bylen[k].sort(key=lambda x: -x[1])


def consistent(cw, pw, m):
    add = {}
    for s, ch in zip(cw, pw):
        v = m.get(s, add.get(s))
        if v is None:
            add[s] = ch
        elif v != ch:
            return None
    return add


# dynamic ordering: prefer short words sharing many symbols with what is already assigned
order, remaining, assigned = [], list(range(len(words))), set()
while remaining:
    def key(i):
        w = words[i]
        L = len(w)
        return (-(len(set(w) & assigned) / L), L if L <= MAXLEN else 100 + L)
    i = min(remaining, key=key)
    order.append(i)
    remaining.remove(i)
    assigned |= set(words[i])
print("order", [(i + 1, " ".join(words[i])) for i in order], file=sys.stderr)

beam = [(0.0, {}, [])]
for idx in order:
    cw = words[idx]
    L = len(cw)
    cands = bylen.get(L, [])
    newbeam = []
    for sc, m, hist in beam:
        n = 0
        for pw, lc in cands:
            add = consistent(cw, pw, m)
            if add is None:
                continue
            m2 = dict(m)
            m2.update(add)
            newbeam.append((sc + lc, m2, hist + [(idx, pw)]))
            n += 1
            if n >= 400:
                break
        if n == 0 or L > MAXLEN:
            newbeam.append((sc + SKIP, m, hist + [(idx, "?" * L)]))
    newbeam.sort(key=lambda x: -x[0])
    seen, pruned = set(), []
    for st in newbeam:
        k = tuple(sorted(st[1].items()))
        if k in seen:
            continue
        seen.add(k)
        pruned.append(st)
        if len(pruned) >= BEAM:
            break
    beam = pruned
    print(f"word {idx + 1} ({' '.join(cw)}): beam {len(beam)} best {beam[0][0]:.1f}", file=sys.stderr)


def render(m):
    return " ".join("".join(m.get(s, "?") for s in w) for w in words)


for sc, m, hist in beam[:15]:
    print(f"{sc:.1f} | {render(m)}")
print(json.dumps(beam[0][1], sort_keys=True))
