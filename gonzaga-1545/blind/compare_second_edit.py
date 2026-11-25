"""Word-by-word agreement between the edition of B174r and the independent second edit.

    uv run python gonzaga-1545/blind/compare_second_edit.py

Words broken at a line end are joined; brackets around a supplied letter are ignored, so the
comparison is of the words read, not of how each editor marked them.
"""
import difflib
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))


def words(path):
    text = re.sub(r"-\s+", "", " ".join(open(path, encoding="utf-8").read().split("\n")))
    return text.split()


def norm(w):
    return w if re.fullmatch(r"\[[^\]]+\]", w) else re.sub(r"[\[\]]", "", w)


a = words(os.path.join(HERE, "..", "edition", "B174r.it.txt"))
b = words(os.path.join(HERE, "B174r-second-edit", "B174r.it.txt"))
sm = difflib.SequenceMatcher(None, [norm(w) for w in a], [norm(w) for w in b], autojunk=False)
same = sum(i2 - i1 for op, i1, i2, j1, j2 in sm.get_opcodes() if op == "equal")
print(f"edition {len(a)} words, second edit {len(b)} words, {same} the same ({same / len(a):.1%})")
for op, i1, i2, j1, j2 in sm.get_opcodes():
    if op != "equal":
        print("  edition:    ", " ".join(a[max(0, i1 - 2):i2 + 2]))
        print("  second edit:", " ".join(b[max(0, j1 - 2):j2 + 2]))
