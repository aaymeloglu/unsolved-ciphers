"""Reproduce the readings, compare the December check with key permutations."""
import argparse
import csv
import random
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent))
from cipherkit.grades import Reading, counts, summary_line

def rows(name):
    with (BASE / name).open(encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))

def decode(signs, key):
    return "".join(" " if s == " " else key.get(s, "?") for s in signs)

def distance(left, right):
    previous = list(range(len(right) + 1))
    for index, a in enumerate(left, 1):
        current = [index]
        for j, b in enumerate(right, 1):
            current.append(min(current[-1] + 1, previous[j] + 1,
                               previous[j - 1] + int(a != b)))
        previous = current
    return previous[-1]

def check_score(check, key):
    errors = 0
    for row in check:
        output = decode(row["signs"], key).split()
        gloss = row["gloss"].replace("v", "u").split()
        errors += sum(distance(a, b) for a, b in zip(output, gloss, strict=True))
    return errors

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--controls", action="store_true")
    args = parser.parse_args()
    dec = {r["sign"]: r["value"] for r in rows("december-key.tsv")}
    additions = {r["sign"]: r["value"] for r in rows("april-key.tsv")}
    if dec.keys() & additions.keys():
        raise SystemExit("An April addition overwrites a December value")
    extended = {**dec, **additions}
    april = rows("april.tsv")
    manuscript = rows("transcription.tsv")
    manuscript_lines = {
        row["line"]: "".join(re.findall(r"\{([^}]+)\}", row["text (braces enclose cipher)"])).replace(" ", "")
        for row in manuscript
    }
    by_line = {}
    for row in april:
        line = row["line"].rstrip("abc")
        by_line[line] = by_line.get(line, "") + row["signs"].replace(" ", "")
    if by_line != {line: signs for line, signs in manuscript_lines.items() if signs}:
        raise SystemExit("Cipher runs in transcription.tsv differ from april.tsv")

    report = []
    graded = []
    grade_key = {sign: "C" for sign in dec} | {sign: "I" for sign in additions}
    for row in april:
        signs = row["signs"]
        if set(signs) - (extended.keys() | {" "}):
            raise SystemExit(f"Unregistered sign on line {row['line']}")
        graded.extend(Reading(sign, extended[sign], grade_key[sign])
                      for sign in signs if sign != " ")
        report.append(row["line"] + "\t" + decode(signs, extended))
    literal = "\n".join(report) + "\n"
    if literal != (BASE / "literal.tsv").read_text():
        raise SystemExit("Literal reading differs from the saved transcription or key")
    print(literal, end="")
    print("line\tgrades")
    for row in april:
        print(row["line"], decode(row["signs"], grade_key), sep="\t")
    grades = counts(graded)
    if (grades["C"], grades["I"]) != (294, 45):
        raise SystemExit("Evidence grades differ from the published counts")
    print(summary_line(grades))
    check = rows("december-check.tsv")
    for row in check:
        print("December", row["line"], decode(row["signs"], dec), sep="\t")
    if args.controls:
        rng = random.Random(1432)
        baseline = []
        values = list(dec.values())
        trials = 1000
        for _ in range(trials):
            rng.shuffle(values)
            baseline.append(check_score(check, dict(zip(dec, values, strict=True))))
        target = check_score(check, dec)
        denominator = sum(len(r["gloss"].replace(" ", "")) for r in check)
        if (target, denominator, min(baseline)) != (6, 41, 23):
            raise SystemExit("December comparison differs from the published control")
        print(f"December word-aligned edits {target}/{denominator}. Best shuffled {min(baseline)}. "
              f"Shuffles as good {sum(x <= target for x in baseline)}/{trials}.")
    signs = "".join(r["signs"].replace(" ", "") for r in april)
    print(f"April {len(signs)} sign positions, {sum(s in dec for s in signs)} under December key, "
          f"{len(set(signs))} distinct sign labels.")

if __name__ == "__main__":
    main()
