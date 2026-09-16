#!/usr/bin/env python3
"""Check that every <picture>'s sizes attribute matches the width the image is really drawn at, in headless Chrome.

Usage: python3 _src/check_sizes.py
Needs google-chrome and the websockets package. Serves the repository on a local port while it runs.
A sizes value may overshoot the drawn width by up to TOLERANCE (the browser then fetches at most one step larger);
it must never undershoot, or the image would be blurry.
"""
import functools
import http.server
import json
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
from pathlib import Path

from websockets.sync.client import connect

ROOT = Path(__file__).resolve().parent.parent
PAGES = ["", "projects/", "writing/", "writing/rebuilding-sgamers/", "about/", "it/", "play/sgamers/"]
# (width, height, device pixel ratio, mobile): Lighthouse's phone and desktop, plus the layout breakpoints in between.
VIEWPORTS = [(412, 823, 1.75, True), (600, 900, 2, True), (700, 900, 2, True), (1024, 768, 1, False),
             (1150, 800, 1, False), (1350, 940, 1, False), (1600, 900, 1, False), (1920, 1080, 1, False)]
TOLERANCE = 0.10

MEASURE = """(() => {
  const probe = document.createElement('div');
  probe.style.cssText = 'position:absolute;visibility:hidden;height:0';
  document.body.appendChild(probe);
  const evaluate = (sizes) => {
    for (const entry of sizes.split(/,(?![^(]*\\))/).map((s) => s.trim())) {
      const m = entry.match(/^(\\(.*\\))\\s+(.+)$/);
      if (m && !matchMedia(m[1]).matches) continue;
      probe.style.width = m ? m[2] : entry;
      return probe.getBoundingClientRect().width;
    }
  };
  const out = [...document.querySelectorAll('picture')].map((p) => {
    const img = p.querySelector('img');
    const sizes = p.querySelector('source').getAttribute('sizes');
    return {src: img.getAttribute('src'), drawn: img.getBoundingClientRect().width, declared: evaluate(sizes), sizes};
  });
  probe.remove();
  return out;
})()"""


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main():
    site_port, chrome_port = free_port(), free_port()
    server = http.server.ThreadingHTTPServer(("127.0.0.1", site_port), functools.partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    profile = tempfile.mkdtemp()
    chrome = subprocess.Popen(["google-chrome", "--headless=new", "--no-sandbox", f"--remote-debugging-port={chrome_port}",
                               f"--user-data-dir={profile}", "about:blank"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    problems, checked = [], 0
    try:
        for _ in range(50):
            try:
                targets = json.load(urllib.request.urlopen(f"http://127.0.0.1:{chrome_port}/json"))
                break
            except OSError:
                time.sleep(0.2)
        page = next(t for t in targets if t["type"] == "page")
        with connect(page["webSocketDebuggerUrl"], max_size=None) as ws:
            counter = iter(range(1, 10**6))

            def send(method, **params):
                n = next(counter)
                ws.send(json.dumps({"id": n, "method": method, "params": params}))
                while True:
                    msg = json.loads(ws.recv())
                    if msg.get("id") == n:
                        return msg.get("result", {})

            for width, height, dpr, mobile in VIEWPORTS:
                send("Emulation.setDeviceMetricsOverride", width=width, height=height, deviceScaleFactor=dpr, mobile=mobile)
                for path in PAGES:
                    send("Page.navigate", url=f"http://127.0.0.1:{site_port}/{path}")
                    time.sleep(0.8)
                    rows = send("Runtime.evaluate", expression=MEASURE, returnByValue=True)["result"]["value"]
                    for r in rows:
                        if r["drawn"] == 0:
                            continue
                        checked += 1
                        low, high = r["drawn"] - 1, r["drawn"] * (1 + TOLERANCE) + 2
                        if not low <= r["declared"] <= high:
                            problems.append(f"{width}px /{path} {r['src']}: disegnata {r['drawn']:.0f}px, dichiarata {r['declared']:.0f}px")
    finally:
        chrome.terminate()
        server.shutdown()
        shutil.rmtree(profile, ignore_errors=True)
    print(f"immagini misurate: {checked} ({len(VIEWPORTS)} schermi, {len(PAGES)} pagine), problemi: {len(problems)}")
    for p in sorted(set(problems)):
        print("  ", p)
    return 1 if problems or not checked else 0


if __name__ == "__main__":
    sys.exit(main())
