import os

import pytest

from cipherkit import CharLM, normalize, strip_gutenberg

FIXTURE = os.path.join(os.path.dirname(__file__), "fixtures", "english_sample.txt")


@pytest.fixture(scope="session")
def english_raw() -> str:
    with open(FIXTURE, encoding="utf-8", errors="replace") as f:
        return strip_gutenberg(f.read())


@pytest.fixture(scope="session")
def english_text(english_raw) -> str:
    return normalize(english_raw, keep_spaces=True)


@pytest.fixture(scope="session")
def english_lm(english_text) -> CharLM:
    # Model from the first 80%; tests that need "unseen" plaintext take it from the last 20%.
    cut = int(len(english_text) * 0.8)
    return CharLM.from_text(english_text[:cut].replace(" ", ""), order=4)


@pytest.fixture(scope="session")
def english_tail(english_text) -> str:
    cut = int(len(english_text) * 0.8)
    return english_text[cut:]
