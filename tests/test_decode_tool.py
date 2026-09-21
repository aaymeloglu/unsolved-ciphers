"""tools/decode.py against recorded DECODE pages and a fake server, plus the no-images guard."""
import importlib.util
import json
import os
import re
import stat
import struct
import subprocess
import sys
import zlib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "tests" / "fixtures" / "decode_record_4736.html"

spec = importlib.util.spec_from_file_location("decode_tool", ROOT / "tools" / "decode.py")
assert spec and spec.loader
decode = importlib.util.module_from_spec(spec)
sys.modules["decode_tool"] = decode  # dataclasses look their module up here
spec.loader.exec_module(decode)


def png(width, height):
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    chunk = struct.pack(">I", len(ihdr)) + b"IHDR" + ihdr + struct.pack(">I", zlib.crc32(b"IHDR" + ihdr))
    return b"\x89PNG\r\n\x1a\n" + chunk


PLACEHOLDER = png(986, 568)
JPEG = b"\xff\xd8\xff\xe0" + b"scan" * 100


class Response:
    def __init__(self, url, body):
        self.url, self.body, self.headers = url, body, {"Content-Type": ""}

    def geturl(self):
        return self.url

    def read(self):
        return self.body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class FakeDecode:
    """Serves the recorded record page; filesrv honours `anonymous` and `granted` sets."""

    def __init__(self, password="right", anonymous=(), granted=()):
        self.password, self.anonymous, self.granted = password, set(anonymous), set(granted)
        self.logged_in, self.logins, self.addheaders = False, 0, []

    def open(self, url, data=None, timeout=None):
        path = url.replace(decode.BASE, "")
        if path.startswith("/decrypt-web/RecordsView/4736"):
            return Response(url, FIXTURE.read_bytes())
        if path.startswith("/decrypt-web/RecordsView/"):
            return Response(decode.BASE + "/decrypt-web/RecordsList", b"<html></html>")
        if path == "/decrypt-web/login" and data is None:
            return Response(url, b'<input type="hidden" name="csrf_name" value="n">'
                                 b'<input type="hidden" name="csrf_value" value="v">')
        if path == "/decrypt-web/login":
            self.logins += 1
            ok = b"password=" + self.password.encode() in (data or b"")
            self.logged_in = ok
            return Response(decode.BASE + ("/decrypt-web/RecordsList" if ok else "/decrypt-web/login"), b"")
        name = path.split("file=", 1)[1]
        served = name in self.anonymous or (self.logged_in and name in self.granted)
        return Response(url, JPEG if served else PLACEHOLDER)


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "cfg"))
    for var in ("DECODE_USER", "DECODE_PASSWORD", "DECODE_CREDENTIALS"):
        monkeypatch.delenv(var, raising=False)

    def serve(server):
        monkeypatch.setattr(decode.urllib.request, "build_opener", lambda *a: server)
        return server
    return serve


IMAGES = ["IMG_R4736_I27769_P1.jpg", "IMG_R4736_I27769_P2.jpg", "IMG_R4736_I27769_P3.jpg"]
DOCS = ["DOC_4736_2023-Mar-31-14-06-45_63387.xlsx", "DOC_4736_2023-Mar-31-14-07-17_49580.pdf"]


def test_parse_record_page():
    rec = decode.parse_record(FIXTURE.read_text(), 4736)
    assert rec.images == IMAGES
    assert [d.name for d in rec.documents] == DOCS
    assert {d.category for d in rec.documents} == {"key"}
    assert rec.documents[0].label == "key reconstruction - Excel (Jakub Mírka)"
    assert rec.public and "Plzni" in rec.fields["current_holder"]


def test_placeholder_detection():
    assert decode.is_placeholder(PLACEHOLDER)
    assert not decode.is_placeholder(png(3000, 4000))
    assert not decode.is_placeholder(JPEG)


def test_record_ids():
    assert decode.record_id("R8345") == decode.record_id("8345") == 8345
    with pytest.raises(decode.DecodeError):
        decode.record_id("BL Add MS 32091")


def test_credentials_file_is_private_and_env_wins(env, monkeypatch):
    path = decode.save_credentials("alice", "pw")
    assert stat.S_IMODE(os.stat(path).st_mode) == 0o600
    assert decode.load_credentials()[:2] == ("alice", "pw")
    monkeypatch.setenv("DECODE_USER", "bob")
    monkeypatch.setenv("DECODE_PASSWORD", "pw2")
    assert decode.load_credentials()[:2] == ("bob", "pw2")


def test_public_images_without_login_then_asks_for_credentials(env, tmp_path, capsys):
    env(FakeDecode(anonymous=IMAGES))
    code = decode.main(["fetch", "R4736", "--out", str(tmp_path / "out")])
    assert code == decode.EXIT_NO_CREDENTIALS
    manifest = json.loads((tmp_path / "out" / "R4736" / "manifest.json").read_text())
    assert [f["name"] for f in manifest["files"]] == IMAGES
    assert manifest["needs_login"] == DOCS
    assert "ask the user once" in capsys.readouterr().err


def test_login_fetches_the_rest_and_reuses_what_it_has(env, tmp_path):
    server = env(FakeDecode(anonymous=IMAGES, granted=DOCS))
    decode.save_credentials("alice", "right")
    assert decode.main(["fetch", "R4736", "--out", str(tmp_path / "out")]) == decode.EXIT_OK
    assert server.logins == 1
    assert decode.main(["fetch", "R4736", "--out", str(tmp_path / "out")]) == decode.EXIT_OK
    assert server.logins == 1  # nothing left to download, so no second login


def test_logged_in_without_permission(env, tmp_path, capsys):
    env(FakeDecode(granted=DOCS))
    decode.save_credentials("alice", "right")
    code = decode.main(["fetch", "R4736", "--out", str(tmp_path / "out")])
    assert code == decode.EXIT_NO_PERMISSION
    err = capsys.readouterr().err
    assert "Megyesi" in err and "draft (not send)" in err
    manifest = json.loads((tmp_path / "out" / "R4736" / "manifest.json").read_text())
    assert manifest["denied"] == IMAGES


def test_bad_credentials(env, tmp_path, capsys):
    env(FakeDecode())
    decode.save_credentials("alice", "wrong")
    assert decode.main(["fetch", "R4736", "--out", str(tmp_path / "out")]) == decode.EXIT_BAD_CREDENTIALS
    assert "refused" in capsys.readouterr().err


def test_unknown_record(env, capsys):
    env(FakeDecode())
    assert decode.main(["meta", "R99999999"]) == decode.EXIT_ERROR
    assert "no record 99999999" in capsys.readouterr().err


def test_no_decode_files_tracked():
    """DECODE images and attachments may not be redistributed."""
    try:
        tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True,
                                 check=True).stdout.splitlines()
    except (OSError, subprocess.CalledProcessError):
        pytest.skip("not a git checkout")
    bad = [p for p in tracked if p.startswith("decode-private/")
           or re.search(r"(^|/)(TH_)?IMG_R\d+_I\d+_P\d+\.\w+$|(^|/)DOC_\d+_[\w-]+\.\w+$", p)]
    assert not bad, f"DECODE files are tracked: {bad}"
