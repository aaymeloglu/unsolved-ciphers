"""Expand the reviewed, normalized sign alignments and check their display text."""
import csv
import re
import unicodedata

from first_pass import decode
from pathlib import Path

HERE = Path(__file__).parent
VOWELS = dict(zip("12345", "uoiea"))
BASE = {
    "2": "c", "2b": "b", "3": "d", "4": "g", "5": "m", "6": "p",
    "7": "r", "8": "t", "9": "v", "G": "g", "Gz": "z", "S": "qu",
    "x": "l", "y": "f", "r": "s", "t": "n",
}
BARE = {
    "0": "c", "2": "o", "3": "a", "6": "s", "p": "u", "c": "l",
    "y": "n", "d": "r", "r": "h", "G": "g", "A": "a", "A_m": "m",
    "P?": "p", "X": "x", "Q": "e", "W": "i", "Z": "t", "+": "n", "F": "et",
    "n#": "nn", "ss": "ss", "s": "s", "t#": "tt", "L#": "ll", "G#": "gg", "α": "per",
    "D": "che", "D^n": "con", "M": "non", "B": "ancora",
}

def expand(sign):
    if sign in BARE:
        return BARE[sign]
    if re.fullmatch(r"#\d+", sign):
        return sign[1:]
    base, vowel = sign.split("^")
    return BASE[base] + VOWELS[vowel]

def letters(s):
    ascii_s = unicodedata.normalize("NFD", s.casefold())
    return re.sub(r"[^a-z0-9]", "", ascii_s).replace("v", "u")

if __name__ == "__main__":
    rows_expected = [f"R{i:02}" for i in range(1, 23)] + [f"V{i:02}" for i in range(1, 20)]
    decoded = []
    for line in (HERE / "192-first-pass.txt").read_text().splitlines():
        if line and not line.startswith("#"):
            row, *signs = line.split()
            decoded.append((row, "".join(map(decode, signs))))
    if [row for row, _ in decoded] != rows_expected:
        raise ValueError("Expected recto lines 1–22 and verso lines 1–19")
    first_pass = "".join(f"{row} {plain}\n" for row, plain in decoded)
    if first_pass != (HERE / "192-first-pass-decode.txt").read_text():
        raise ValueError("Transcription and saved first-pass output disagree")
    with (HERE / "passages.tsv").open() as source:
        rows = list(csv.DictReader(source, delimiter="\t"))
    for row in rows:
        values = [expand(s) for s in row["signs"].split()]
        actual = "".join(values)
        if letters(actual) != letters(row["reading"]):
            raise ValueError((row["location"], row["reading"], actual))
        print(row["location"], "·".join(values), row["reading"], sep="\t")
