"""Every cipher folder has a row on the Pages index, whatever the outcome."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = re.compile(r"^[a-z-]+-\d{4}(-\d{4})?$")

# Folders shown on the index under another folder's row: folder -> text that row must contain.
COVERED_BY = {
    "ferdinand-1634": "ferdinand-reading.html",
}


def target_folders():
    for readme in sorted(ROOT.glob("*/README.md")) + sorted(ROOT.glob("*/*/README.md")):
        rel = readme.parent.relative_to(ROOT)
        if TARGET.match(rel.name) and all(not part.startswith((".", "_")) for part in rel.parts):
            yield rel.as_posix()


def test_every_target_folder_is_on_the_index():
    index = (ROOT / "docs" / "index.html").read_text()
    folders = list(target_folders())
    assert "amiens-1513" in folders and "milan-1494/niccolini-1492" in folders
    missing = [f for f in folders
               if COVERED_BY.get(f, f"/main/{f}") not in index]
    assert not missing, (
        f"no row on the Pages index for {missing}: add one in index() in docs/_build_site.py "
        "(open and failed attempts included) and regenerate"
    )
