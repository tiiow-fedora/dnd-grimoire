"""Grimoire - local D&D campaign companion.

Serves index.html on 127.0.0.1 and keeps all campaign data in data/grimoire.json.
Double-click (or use the desktop shortcut) to open it in its own app window.
The server quits by itself a few minutes after the window is closed.
"""
import json
import os
import shutil
import socket
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("GRIMOIRE_PORT", "8765"))
DATA = os.environ.get("GRIMOIRE_DATA") or os.path.join(ROOT, "data", "grimoire.json")
BACKUPS = os.path.join(os.path.dirname(DATA), "backups")
IDLE_QUIT = 300  # seconds without a heartbeat from the window
MAX_BODY = 200 * 1024 * 1024

state = {"last_ping": time.time(), "seen": False}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body=b"", ctype="application/json"):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            with open(os.path.join(ROOT, "index.html"), "rb") as f:
                self._send(200, f.read(), "text/html; charset=utf-8")
        elif path == "/api/data":
            if os.path.exists(DATA):
                with open(DATA, "rb") as f:
                    self._send(200, f.read())
            else:
                self._send(200, b"{}")
        elif path == "/api/ping":
            state["last_ping"] = time.time()
            state["seen"] = True
            self._send(200, b'{"ok":true}')
        else:
            self._send(404, b'{"error":"not found"}')

    def do_POST(self):
        if self.path.split("?")[0] != "/api/data":
            return self._send(404, b'{"error":"not found"}')
        n = int(self.headers.get("Content-Length") or 0)
        if n <= 0 or n > MAX_BODY:
            return self._send(400, b'{"error":"bad size"}')
        raw = self.rfile.read(n)
        try:
            obj = json.loads(raw)
        except ValueError:
            return self._send(400, b'{"error":"bad json"}')
        # a stale window from before multi-campaign support must not clobber the new format
        if not isinstance(obj, dict) or not obj.get("campaigns"):
            return self._send(409, b'{"error":"outdated page, reload"}')
        # optimistic concurrency: a window must have loaded the current revision to overwrite it
        cur = 0
        if os.path.exists(DATA):
            try:
                with open(DATA, "rb") as f:
                    cur = int(json.load(f).get("rev", 0))
            except (ValueError, OSError):
                cur = 0
        if int(obj.get("rev", 0)) != cur:
            return self._send(409, b'{"error":"stale"}')
        obj["rev"] = cur + 1
        raw = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        os.makedirs(os.path.dirname(DATA), exist_ok=True)
        os.makedirs(BACKUPS, exist_ok=True)
        if os.path.exists(DATA):
            shutil.copy2(DATA, DATA + ".bak")
            daily = os.path.join(BACKUPS, "grimoire-%s.json" % time.strftime("%Y%m%d"))
            if not os.path.exists(daily):
                shutil.copy2(DATA, daily)
        tmp = DATA + ".tmp"
        with open(tmp, "wb") as f:
            f.write(raw)
        os.replace(tmp, DATA)
        state["last_ping"] = time.time()
        self._send(200, json.dumps({"ok": True, "rev": cur + 1}).encode())


def port_in_use():
    with socket.socket() as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", PORT)) == 0


def find_browser():
    roots = [os.environ.get("ProgramFiles(x86)"), os.environ.get("ProgramFiles"), os.environ.get("LocalAppData")]
    rel = [r"Microsoft\Edge\Application\msedge.exe", r"Google\Chrome\Application\chrome.exe"]
    for r in rel:
        for base in roots:
            if base:
                p = os.path.join(base, r)
                if os.path.exists(p):
                    return p
    return None


def open_window():
    if os.environ.get("GRIMOIRE_NOWINDOW"):
        return
    url = "http://127.0.0.1:%d/" % PORT
    exe = find_browser()
    if exe:
        flags = 0x00000008 | 0x00000200  # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
        subprocess.Popen([exe, "--app=" + url, "--window-size=1480,940"], creationflags=flags, close_fds=True)
    else:
        import webbrowser
        webbrowser.open(url)


def watchdog():
    started = time.time()
    while True:
        time.sleep(10)
        idle = time.time() - state["last_ping"]
        if state["seen"] and idle > IDLE_QUIT:
            os._exit(0)
        if not state["seen"] and time.time() - started > 180:
            os._exit(0)


def main():
    if port_in_use():
        open_window()  # already running: just show another window
        return
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    threading.Thread(target=watchdog, daemon=True).start()
    threading.Thread(target=open_window, daemon=True).start()
    server.serve_forever()


if __name__ == "__main__":
    main()
