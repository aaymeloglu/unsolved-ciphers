#!/usr/bin/env python3
"""Fetch records, images and attached documents from the DECODE database (de-crypt.org).

    python3 tools/decode.py meta R8345          # metadata, image and document names (no login)
    python3 tools/decode.py fetch R8345         # download into decode-private/R8345/
    python3 tools/decode.py login               # store credentials once, outside the repo
    python3 tools/decode.py status              # where credentials come from, whether they work

Standard library only. Written to be run by an agent: every failure prints what happened and
what to do next, and the exit code says which case it is.

Credentials are read from DECODE_USER / DECODE_PASSWORD if set, otherwise from
~/.config/decode/credentials (JSON, mode 0600, written by `login`). The session cookie is kept
next to that file, so repeated fetches and parallel workers do not log in each time. Nothing
credential-related is ever written inside the repository.

DECODE's terms: images may not be redistributed. Downloads go to decode-private/, which is
gitignored, and tests/test_decode_tool.py fails if any DECODE image is tracked.
"""
from __future__ import annotations

import argparse
import getpass
import hashlib
import html
import http.cookiejar
import http.server
import json
import os
import re
import secrets
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from dataclasses import dataclass, field
from pathlib import Path

BASE = "https://de-crypt.org"
REPO = Path(__file__).resolve().parent.parent
DEFAULT_OUT = REPO / "decode-private"
PI_CONTACT = "Beata Megyesi, beata.megyesi@ling.su.se (DECODE project lead, Stockholm University)"

# filesrv answers a request it will not serve with HTTP 200 and this PNG ("Insufficient
# permissions to so see the full image"), for images and documents alike.
PLACEHOLDER_SHA256 = "1e47167c4db694fe06f61f4c5650ac54eff2ce3ee2eff9dea78c7f15aa55b606"
PLACEHOLDER_SIZE = (986, 568)

EXIT_OK, EXIT_NO_CREDENTIALS, EXIT_BAD_CREDENTIALS, EXIT_NO_PERMISSION, EXIT_ERROR = 0, 2, 3, 4, 5


class DecodeError(Exception):
    def __init__(self, message: str, code: int = EXIT_ERROR):
        super().__init__(message)
        self.code = code


# ---------------------------------------------------------------- credentials and session

def config_dir() -> Path:
    base = os.environ.get("XDG_CONFIG_HOME") or os.path.join(os.path.expanduser("~"), ".config")
    return Path(base) / "decode"


def credentials_path() -> Path:
    return Path(os.environ.get("DECODE_CREDENTIALS") or config_dir() / "credentials")


def session_path() -> Path:
    return credentials_path().with_name("session.cookies")


def load_credentials() -> tuple[str, str, str] | None:
    """(username, password, source) or None. The environment wins over the file."""
    user, password = os.environ.get("DECODE_USER"), os.environ.get("DECODE_PASSWORD")
    if user and password:
        return user, password, "environment (DECODE_USER / DECODE_PASSWORD)"
    path = credentials_path()
    if path.exists():
        try:
            data = json.loads(path.read_text())
            return data["username"], data["password"], str(path)
        except (ValueError, KeyError) as e:
            raise DecodeError(f"{path} is not a valid credentials file ({e}). "
                              "Rerun `python3 tools/decode.py login`.")
    return None


def write_private(path: Path, text: str) -> None:
    """Write a 0600 file atomically, so parallel workers never read half of it."""
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write(text)
    os.replace(tmp, path)


def save_credentials(user: str, password: str) -> Path:
    path = credentials_path()
    write_private(path, json.dumps({"username": user, "password": password}))
    return path


NO_CREDENTIALS = """\
decode.py: this needs a DECODE login and none is configured.

Next step for the agent: ask the user once for their de-crypt.org username and password
(they can register free at https://de-crypt.org/). Offer two ways, preferring the first:

  1. Run `python3 tools/decode.py login` yourself. With no terminal attached it opens a form
     in the user's browser on 127.0.0.1; the password goes straight into the credentials
     file and never enters the conversation. Tell the user to look for the browser tab.
  2. If there is no local browser (remote or cloud session), the user pastes the username and
     password in chat and you run:
       printf '%s' 'PASSWORD' | python3 tools/decode.py login --username USER --password-stdin

Either way they are verified against DECODE and saved to {path} (mode 0600, outside the
repo), and every later session and worker uses them without asking again.
Meanwhile, anything in the repo's own transcriptions and verifiers needs no DECODE access."""


class Client:
    """A DECODE session. Anonymous until a request needs a login; then logs in once."""

    def __init__(self, credentials: tuple[str, str, str] | None = None, opener=None,
                 persist: bool = True):
        self.credentials = credentials
        self.persist = persist and opener is None
        self.jar = http.cookiejar.MozillaCookieJar(str(session_path()))
        if self.persist and session_path().exists():
            try:
                self.jar.load(ignore_discard=True, ignore_expires=True)
            except (OSError, http.cookiejar.LoadError):
                pass
        self.opener = opener or urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar))
        self.opener.addheaders = [("User-Agent", "unsolved-ciphers decode.py (research; stdlib urllib)")]
        self.logged_in = False

    def get(self, path: str, data: bytes | None = None) -> tuple[str, bytes, str]:
        """(final url, body, content type)."""
        url = path if path.startswith("http") else BASE + path
        for attempt in range(3):
            try:
                with self.opener.open(url, data, timeout=120) as r:
                    return r.geturl(), r.read(), r.headers.get("Content-Type", "")
            except urllib.error.HTTPError as e:
                if e.code in (429, 502, 503, 504) and attempt < 2:
                    time.sleep(5 * (attempt + 1))
                    continue
                raise DecodeError(f"HTTP {e.code} from {url}")
            except urllib.error.URLError as e:
                if attempt < 2:
                    time.sleep(3)
                    continue
                raise DecodeError(f"cannot reach {url}: {e.reason}. Check network access to de-crypt.org.")
        raise AssertionError("unreachable")

    def login(self) -> None:
        if self.credentials is None:
            raise DecodeError(NO_CREDENTIALS.format(path=credentials_path()), EXIT_NO_CREDENTIALS)
        user, password, source = self.credentials
        _, body, _ = self.get("/decrypt-web/login")
        form = dict(re.findall(r'name="(csrf_name|csrf_value)" value="([^"]*)"', body.decode("utf-8", "replace")))
        if len(form) != 2:
            raise DecodeError("DECODE's login page has changed (no CSRF fields found); "
                              "tools/decode.py needs updating.")
        form.update(username=user, password=password)
        final, _, _ = self.get("/decrypt-web/login", urllib.parse.urlencode(form).encode())
        if final.rstrip("/").endswith("/login"):
            raise DecodeError(
                f"decode.py: DECODE rejected the username/password from {source}.\n\n"
                "Next step for the agent: tell the user DECODE refused this login and ask for the "
                "correct one, then store it again with `python3 tools/decode.py login` (see "
                "`python3 tools/decode.py login --help`).", EXIT_BAD_CREDENTIALS)
        self.logged_in = True
        if self.persist:
            path = session_path()
            path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            self.jar.save(str(path), ignore_discard=True, ignore_expires=True)
            os.chmod(path, 0o600)

    def file(self, name: str) -> bytes | None:
        """File bytes, or None when DECODE serves its permissions placeholder instead."""
        _, body, _ = self.get("/decrypt-custom/filesrv/?file=" + urllib.parse.quote(name))
        return None if is_placeholder(body) else body


def is_placeholder(body: bytes) -> bool:
    if hashlib.sha256(body).hexdigest() == PLACEHOLDER_SHA256:
        return True
    # Same picture re-encoded: a small PNG of exactly the placeholder's dimensions.
    if body[:8] == b"\x89PNG\r\n\x1a\n" and len(body) < 100_000 and body[12:16] == b"IHDR":
        w, h = int.from_bytes(body[16:20], "big"), int.from_bytes(body[20:24], "big")
        return (w, h) == PLACEHOLDER_SIZE
    return False


# ---------------------------------------------------------------- record pages

@dataclass
class Document:
    name: str
    label: str
    category: str


@dataclass
class Record:
    id: int
    fields: dict[str, str] = field(default_factory=dict)
    images: list[str] = field(default_factory=list)
    documents: list[Document] = field(default_factory=list)

    @property
    def public(self) -> bool:
        return self.fields.get("access_mode", "").strip().lower() == "public"

    def as_json(self) -> dict:
        return {"id": self.id, "url": f"{BASE}/decrypt-web/RecordsView/{self.id}",
                "fields": self.fields, "images": self.images,
                "documents": [d.__dict__ for d in self.documents]}


def _text(fragment: str) -> str:
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", fragment))).strip()


def parse_record(page: str, record_id: int) -> Record:
    rec = Record(record_id)
    for m in re.finditer(r'<tr id="r_(\w+)"[^>]*>(.*?)</tr>', page, re.S):
        cells = re.findall(r"<td[^>]*>(.*?)</td>", m.group(2), re.S)
        if len(cells) >= 2:
            value = _text(cells[1])
            if value:
                rec.fields[m.group(1)] = value
    seen = set()
    for name in re.findall(r'alt="(IMG_R\d+_I\d+_P\d+\.\w+)"', page) + \
            re.findall(r"(?<![A-Z_])(IMG_R\d+_I\d+_P\d+\.\w+)", page):
        if name not in seen:
            seen.add(name)
            rec.images.append(name)
    rec.images.sort(key=lambda n: [int(x) for x in re.findall(r"\d+", n)])
    for m in re.finditer(r"filesrv/\?file=(DOC_[^'\"<>]+)['\"][^>]*>.*?<p>(.*?)</p>", page, re.S):
        label = _text(m.group(2))
        cat = re.search(r"\[([^\]]+)\]\s*$", label)
        rec.documents.append(Document(m.group(1), label[:cat.start()].strip() if cat else label,
                                      cat.group(1) if cat else ""))
    return rec


def record_id(arg: str) -> int:
    m = re.fullmatch(r"[Rr]?(\d+)", arg.strip())
    if not m:
        raise DecodeError(f"{arg!r} is not a DECODE record id (expected R8345 or 8345).")
    return int(m.group(1))


def fetch_record(client: Client, rid: int) -> Record:
    final, body, _ = client.get(f"/decrypt-web/RecordsView/{rid}")
    page = body.decode("utf-8", "replace")
    if "/RecordsView/" not in final or 'id="r_id"' not in page:
        raise DecodeError(f"DECODE has no record {rid} (the view redirected to {final}).")
    return parse_record(page, rid)


# ---------------------------------------------------------------- commands

def cmd_meta(args) -> int:
    client = Client(load_credentials())
    for rid in map(record_id, args.records):
        print(json.dumps(fetch_record(client, rid).as_json(), ensure_ascii=False, indent=2))
    return EXIT_OK


def fetch_one(client: Client, rid: int, out: Path, images: bool, docs: bool, force: bool) -> dict:
    rec = fetch_record(client, rid)
    folder = out / f"R{rid}"
    folder.mkdir(parents=True, exist_ok=True)
    wanted = ([(n, "image", None) for n in rec.images] if images else []) + \
             ([(d.name, "document", d) for d in rec.documents] if docs else [])
    manifest_path = folder / "manifest.json"
    old = {}
    if manifest_path.exists():
        old = {f["name"]: f for f in json.loads(manifest_path.read_text()).get("files", [])}
    files, denied, needs_login = [], [], []
    for name, kind, doc in wanted:
        dest = folder / name
        if dest.exists() and not force and name in old:
            files.append(old[name])
            continue
        body = client.file(name)
        if body is None and not client.logged_in:
            if client.credentials is None:
                needs_login.append(name)
                continue
            client.login()
            body = client.file(name)
        if body is None:
            denied.append(name)
            continue
        dest.write_bytes(body)
        entry = {"name": name, "kind": kind, "bytes": len(body),
                 "sha256": hashlib.sha256(body).hexdigest(),
                 "url": f"{BASE}/decrypt-custom/filesrv/?file={name}"}
        if doc:
            entry.update(label=doc.label, category=doc.category)
        files.append(entry)
        print(f"  {name}  {len(body):,} bytes", file=sys.stderr)
    manifest = {"record": rec.as_json(), "fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "files": files, "denied": denied, "needs_login": needs_login,
                "terms": "DECODE images may not be redistributed. Do not commit this folder."}
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    return manifest


def cmd_fetch(args) -> int:
    client = Client(load_credentials())
    out = Path(args.out).resolve()
    status = EXIT_OK
    for rid in map(record_id, args.records):
        print(f"R{rid}:", file=sys.stderr)
        m = fetch_one(client, rid, out, not args.documents_only, not args.images_only, args.force)
        got = len(m["files"])
        print(f"R{rid}: {got} file(s) in {out / f'R{rid}'}", file=sys.stderr)
        if m["needs_login"]:
            status = max(status, EXIT_NO_CREDENTIALS)
            print(f"R{rid}: {len(m['needs_login'])} file(s) need a DECODE login: "
                  f"{', '.join(m['needs_login'][:4])}{' ...' if len(m['needs_login']) > 4 else ''}",
                  file=sys.stderr)
        if m["denied"]:
            status = max(status, EXIT_NO_PERMISSION)
            holder = m["record"]["fields"].get("current_holder") or m["record"]["fields"].get("c_holder", "this holding")
            print(f"""
decode.py: logged in, but DECODE will not serve {len(m['denied'])} file(s) of R{rid} to this account
({', '.join(m['denied'][:4])}{' ...' if len(m['denied']) > 4 else ''}). Images from {holder}
are restricted to accounts the DECODE team has granted access; thumbnails and metadata stay open.

Next step for the agent: tell the user, and offer to draft (not send) a short access request to
{PI_CONTACT}, naming their DECODE username, the record ids, and the research purpose. Access is
per account and was granted within days when asked. Once granted, just rerun this fetch; the
tool logs in again by itself. Meanwhile look for a public copy of the same manuscript in the
holding library's own viewer (BNE Biblioteca Digital Hispánica, Gallica, PARES, the BL's
Digitised Manuscripts), and check the repo for an existing transcription of this record.""",
                  file=sys.stderr)
    if status == EXIT_NO_CREDENTIALS:
        print("\n" + NO_CREDENTIALS.format(path=credentials_path()), file=sys.stderr)
    return status


LOGIN_FORM = """<!doctype html><meta charset=utf-8><title>DECODE login for unsolved-ciphers</title>
<style>body{{font:16px system-ui;max-width:28em;margin:4em auto;padding:0 1em}}input{{display:block;width:100%;
margin:.3em 0 1em;padding:.5em;font:inherit}}button{{padding:.5em 1.2em;font:inherit}}</style>
<h1>DECODE login</h1><p>Your de-crypt.org username and password are checked against DECODE and saved
to <code>{path}</code> on this machine (readable only by you). They are not sent anywhere else and
do not enter the agent's conversation.</p><p style="color:#a00">{error}</p>
<form method=post><input type=hidden name=token value="{token}">
<label>Username<input name=username autocomplete=username required autofocus></label>
<label>Password<input name=password type=password autocomplete=current-password required></label>
<button>Save</button></form>"""


def browser_login(timeout: int) -> tuple[str, str]:
    """Collect credentials through a one-shot form on 127.0.0.1 and verify them."""
    token = secrets.token_urlsafe(16)
    result: dict = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            pass

        def page(self, error=""):
            body = LOGIN_FORM.format(path=html.escape(str(credentials_path())), token=token,
                                     error=html.escape(error)).encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            self.page()

        def do_POST(self):
            n = int(self.headers.get("Content-Length", 0))
            form = urllib.parse.parse_qs(self.rfile.read(n).decode())
            if form.get("token", [""])[0] != token:
                self.send_error(403)
                return
            user, password = form.get("username", [""])[0], form.get("password", [""])[0]
            try:
                Client((user, password, "browser form"), persist=False).login()
            except DecodeError as e:
                self.page("DECODE refused that username and password. Try again." if e.code == EXIT_BAD_CREDENTIALS else str(e))
                return
            result.update(user=user, password=password)
            body = b"<!doctype html><meta charset=utf-8><p style='font:16px system-ui;margin:4em'>Saved. You can close this tab.</p>"
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(body)

    server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    url = f"http://127.0.0.1:{server.server_port}/"
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f"decode.py: waiting for the user to enter their DECODE login at {url} "
          f"(opened in the browser; waiting {timeout} s).", file=sys.stderr, flush=True)
    if not webbrowser.open(url):
        server.shutdown()
        raise DecodeError(f"decode.py: no browser could be opened for the login form ({url}).\n\n"
                          "Next step for the agent: this session has no local browser. Ask the user to "
                          "paste their DECODE username and password, then run\n"
                          "  printf '%s' 'PASSWORD' | python3 tools/decode.py login --username USER --password-stdin",
                          EXIT_NO_CREDENTIALS)
    deadline = time.time() + timeout
    while "user" not in result and time.time() < deadline:
        time.sleep(0.5)
    time.sleep(0.5)
    server.shutdown()
    if "user" not in result:
        raise DecodeError("decode.py: no login was entered in the browser form before the timeout.\n\n"
                          "Next step for the agent: ask the user whether they saw the tab; if the "
                          "session has no local browser, use the --password-stdin route instead.",
                          EXIT_NO_CREDENTIALS)
    return result["user"], result["password"]


def cmd_login(args) -> int:
    if args.password_stdin:
        if not args.username:
            raise DecodeError("--password-stdin needs --username.")
        user, password = args.username, sys.stdin.read().rstrip("\r\n")
        Client((user, password, "the --password-stdin input"), persist=False).login()
    elif sys.stdin.isatty() and not args.browser:
        user = args.username or input("DECODE username: ").strip()
        password = getpass.getpass("DECODE password: ")
        Client((user, password, "the terminal prompt"), persist=False).login()
    else:
        user, password = browser_login(args.timeout)
    path = save_credentials(user, password)
    session_path().unlink(missing_ok=True)
    print(f"decode.py: login verified and saved to {path}. Fetches will use it from now on.", file=sys.stderr)
    return EXIT_OK


def cmd_status(args) -> int:
    creds = load_credentials()
    if creds is None:
        print(f"credentials: none (set DECODE_USER/DECODE_PASSWORD or run `python3 tools/decode.py login`; "
              f"file would be {credentials_path()})")
        return EXIT_NO_CREDENTIALS
    print(f"credentials: {creds[0]} from {creds[2]}")
    Client(creds).login()
    print("login: accepted by de-crypt.org")
    return EXIT_OK


def cmd_logout(args) -> int:
    for p in (session_path(), credentials_path()) if args.forget else (session_path(),):
        p.unlink(missing_ok=True)
        print(f"removed {p}", file=sys.stderr)
    return EXIT_OK


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="decode.py", description=(__doc__ or "").split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("meta", help="print record metadata, image and document names as JSON")
    p.add_argument("records", nargs="+")
    p.set_defaults(func=cmd_meta)
    p = sub.add_parser("fetch", help="download a record's images and documents")
    p.add_argument("records", nargs="+")
    p.add_argument("--out", default=str(DEFAULT_OUT), help="default: decode-private/ in the repo (gitignored)")
    p.add_argument("--images-only", action="store_true")
    p.add_argument("--documents-only", action="store_true")
    p.add_argument("--force", action="store_true", help="download again even if already present")
    p.set_defaults(func=cmd_fetch)
    p = sub.add_parser("login", help="verify and store a DECODE login outside the repo")
    p.add_argument("--username")
    p.add_argument("--password-stdin", action="store_true", help="read the password from stdin")
    p.add_argument("--browser", action="store_true", help="use the local browser form even in a terminal")
    p.add_argument("--timeout", type=int, default=600, help="seconds to wait for the browser form")
    p.set_defaults(func=cmd_login)
    p = sub.add_parser("status", help="show where credentials come from and test them")
    p.set_defaults(func=cmd_status)
    p = sub.add_parser("logout", help="drop the cached session (--forget also deletes stored credentials)")
    p.add_argument("--forget", action="store_true")
    p.set_defaults(func=cmd_logout)
    args = ap.parse_args(argv)
    try:
        return args.func(args)
    except DecodeError as e:
        print(str(e) if str(e).startswith("decode.py:") else f"decode.py: {e}", file=sys.stderr)
        return e.code
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
