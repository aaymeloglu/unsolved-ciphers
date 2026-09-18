from cipherkit import cipher_tokens, parse, segments, symbol_counts


def test_groups():
    toks = parse("# comment\nc77 g72 | d10 h40\n", style="groups")
    assert [t.kind for t in toks] == ["cipher", "cipher", "sep", "cipher", "cipher"]
    assert cipher_tokens(toks) == ["c77", "g72", "d10", "h40"]
    assert segments(toks) == [["c77", "g72"], ["d10", "h40"]]


def test_mixed_auto():
    toks = parse("the 113 10 26 of 222 31")
    assert [t.kind for t in toks] == ["clear", "cipher", "cipher", "cipher", "clear", "cipher", "cipher"]
    assert segments(toks) == [["113", "10", "26"], ["222", "31"]]


def test_annotated_auto():
    toks = parse("31214=bis 69=ld 8=∅ 33115")
    assert toks[0].reading == "bis"
    assert toks[3].reading is None
    assert cipher_tokens(toks) == ["31214", "69", "8", "33115"]


def test_letters_auto():
    toks = parse("QKDF\nLSUR")
    assert cipher_tokens(toks) == list("QKDFLSUR")
    assert symbol_counts(toks)["Q"] == 1
