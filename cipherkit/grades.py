"""The per-group grade vocabulary of CONVENTIONS.md section 1, in code.

Every decoder in this repo grades each cipher group it reads. The five grades, in the order
the conventions list them:

    H  read from a primary key source (a surviving key or table)
    C  read from known plaintext (a contemporary decipherment, a printed sibling)
    S  determined by cryptanalysis alone, claimed only next to a control
    M  uncertain: alternatives, unread signs, groups absent from the key
    I  inferred or supplied: restorations, emendations, repairs

`counts` refuses any other label, so a folder cannot invent a sixth grade. `render` is the
conventions' rendering: H, C and S values as they are, M in parentheses, I in square brackets.
"""
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass

GRADES = ("H", "C", "S", "M", "I")


@dataclass
class Reading:
    token: str
    value: str          # plaintext, or "?" when the key has nothing for the token
    grade: str          # one of GRADES
    basis: str = ""     # free text: "in Ziffra prima", "R954 alignment", ...


def check_grade(grade: str) -> str:
    """Return `grade` if it is one of GRADES, else raise ValueError."""
    if grade not in GRADES:
        raise ValueError(f"unknown grade {grade!r}; grades are {', '.join(GRADES)}")
    return grade


def grade_token(token: str, key: Mapping[str, Mapping], default_grade: str = "M") -> Reading:
    """Look `token` up in a key of the moray key.json shape.

    `key[token]` is `{"value": ..., "grade": ..., "from": ...}`; `grade` falls back to
    `default_grade` when the entry lacks it, and `basis` is the entry's `from` (or `basis`)
    text. A token the key does not contain reads as "?" with grade `default_grade`, which is
    M by the conventions: a group absent from the key is uncertain.
    """
    check_grade(default_grade)
    entry = key.get(token)
    if entry is None:
        return Reading(token, "?", default_grade)
    grade = check_grade(str(entry.get("grade", default_grade)))
    basis = entry.get("basis", entry.get("from", ""))
    return Reading(token, str(entry["value"]), grade, str(basis))


def apply_key(tokens: Sequence[str], key: Mapping[str, Mapping], **kw) -> list[Reading]:
    """`grade_token` over a token sequence; keyword arguments go to `grade_token`."""
    return [grade_token(t, key, **kw) for t in tokens]


def counts(readings: Iterable[Reading]) -> dict[str, int]:
    """Tally readings by grade. Always returns all five grades in GRADES order, zeros
    included, and raises ValueError on a grade outside the vocabulary."""
    c = {g: 0 for g in GRADES}
    for r in readings:
        c[check_grade(r.grade)] += 1
    return c


def render(readings: Iterable[Reading], gap: str = "|") -> str:
    """The CONVENTIONS rendering: value as is for H, C and S, `(value)` for M, `[value]` for I.
    A reading whose token is `gap` is passed through as its value whatever its grade."""
    out = []
    for r in readings:
        if r.token == gap:
            out.append(r.value)
        elif check_grade(r.grade) == "M":
            out.append(f"({r.value})")
        elif r.grade == "I":
            out.append(f"[{r.value}]")
        else:
            out.append(r.value)
    return "".join(out)


def summary_line(c: Mapping[str, int]) -> str:
    """`"1537 H, 0 C, 0 S, 48 M, 54 I"`: every grade, in order, missing ones as 0."""
    for g in c:
        check_grade(g)
    return ", ".join(f"{c.get(g, 0)} {g}" for g in GRADES)
