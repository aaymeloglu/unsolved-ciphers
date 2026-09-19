#!/usr/bin/env python3
"""Reproduce the added runs and the exact cost of proposed readings. No dependencies."""
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
key = {k: v for k, v in json.loads((HERE / "baseline-key.json").read_text()).items()
       if not k.startswith("_")}
lines = {}
for line in (HERE / "baseline-transcription.txt").read_text().splitlines():
    if line.startswith("P"):
        tag, body = line.split(":", 1)
        lines[tag] = body.split()
repairs = {(r["line"], r["pos"]): r for r in
           json.loads((HERE / "baseline-repairs.json").read_text())["repairs"]}
counts = Counter()
for tag, tokens in lines.items():
    for pos, token in enumerate(tokens, 1):
        if (tag, pos) in repairs:
            assert repairs[tag, pos]["printed"] == token
            counts["I"] += 1
        else:
            counts[key[token]["grade"]] += 1
assert sum(map(len, lines.values())) == 308
assert counts == {"S": 294, "C": 2, "I": 12}

additions = json.loads((HERE / "additions.json").read_text())
extra_counts = Counter()
extra_tokens = 0
for run in additions["runs"]:
    raw, proposed = [], []
    for token in run["tokens"]:
        extra_tokens += 1
        entry = key.get(token) or additions["gloss_values"].get(token)
        raw.append(entry["value"] if entry else "?")
        proposal = additions["proposals"].get(token)
        if proposal:
            proposed.append("[" + proposal["value"] + "]")
            extra_counts[proposal["grade"]] += 1
        else:
            proposed.append(entry["value"])
            extra_counts[entry["grade"]] += 1
    print(run["id"], "printed:", " ".join(run["tokens"]))
    print("  key/gloss:", "".join(raw), " proposed:", "".join(proposed))
assert extra_tokens == 14
assert extra_counts == {"S": 10, "C": 3, "I": 1}
print("Expanded inventory:", len(lines) + len(additions["runs"]), "runs,",
      308 + extra_tokens, "printed groups; proposed grades:", dict(counts + extra_counts))

tokens = lines["P522.2"]
literal = "".join(key[t]["value"] for t in tokens)
target = "diemetfvndament"  # Preserve historical v for modern u.
assert len(literal) == len(target)
changes = [(i, tokens[i-1], a, b) for i, (a, b) in
           enumerate(zip(literal, target), 1) if a != b]
assert changes == [(5, "17", "n", "e"), (6, "12", "i", "t"), (7, "5", "c", "f")]
print("P522.2 literal:", literal)
print("  die met fvndament requires:", changes)

literal = "".join(key[t]["value"] for t in lines["P522.4"])
target = "tenprincipalen"
assert literal == "tenprincipaln"
assert literal[:-1] + "e" + literal[-1] == target
print("P522.4:", literal, "-> ten principal [e]n: one inserted e")
print("P582.4:", "".join(key[t]["value"] for t in lines["P582.4"]),
      "remains unresolved; [vl]ote / [vlo]ote are contextual supplements, not decoded text")

# Independent source inventory must agree with the current published edition.
import importlib.util
spec = importlib.util.spec_from_file_location("current_vp", HERE.parent / "verify.py")
current = importlib.util.module_from_spec(spec)
spec.loader.exec_module(current)
current_key, current_lines, current_repairs = current.load()
assert len(current_lines) == 20
assert sum(len(ts) for _, ts in current_lines) == 322
for run in additions["runs"]:
    assert dict(current_lines)[run["id"]] == run["tokens"]
current_ed = current.edited(current_key, current_lines, current_repairs)
assert Counter(r.grade for rs in current_ed.values() for r in rs) == {"S": 304, "C": 5, "I": 13}
assert "".join(r.value for r in current_ed["P522.2"]) == "diemnicvndament"
assert "".join(r.value for r in current_ed["P522.4"]) == "tenprincipaln"
assert "".join(r.value for r in current_ed["P582.4"]) == "ote"
assert current_key["43"]["grade"] == "M"
assert current_ed["P523.2"][3].grade == "I"
print("Current edition agrees with the source inventory and preserves unresolved output.")
