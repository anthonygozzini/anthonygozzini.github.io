#!/usr/bin/env python3
"""Check the responsive images in headless Chrome: every <picture>'s sizes attribute matches the width the image is
really drawn at, and nothing PageSpeed's phone downloads trips its "Improve image delivery" insight.

Usage: python3 _src/check_sizes.py
Needs google-chrome and the websockets package. Serves the repository on a local port while it runs.
A sizes value may overshoot the drawn width by up to TOLERANCE (the browser then fetches at most one step larger);
it must never undershoot, or the image would be blurry.
"""
import functools
import http.server
import json
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import urllib.parse
import urllib.request
from pathlib import Path

from websockets.sync.client import connect

ROOT = Path(__file__).resolve().parent.parent
# Every page in the sitemap, in both languages.
PAGES = [loc.removeprefix("https://anthonygozzini.github.io/")
         for loc in re.findall(r"<loc>([^<]+)</loc>", (ROOT / "sitemap.xml").read_text(encoding="utf-8"))]
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


# PageSpeed's phone and the rule of its "Improve image delivery" insight, including its bug (Lighthouse issue #17080): the
# drawn size is taken in CSS pixels, ignoring the 1.75 pixel ratio, and an image is reported once that "waste" passes
# 12,288 bytes (4,096 without srcset).
PSI_PHONE = (412, 823, 1.75, "Mozilla/5.0 (Linux; Android 11; moto g power (2022)) AppleWebKit/537.36 (KHTML, like Gecko) "
             "Chrome/130.0 Mobile Safari/537.36")
PSI_THRESHOLD = {True: 12288, False: 4096}
LOADED = """[...document.images].filter((i) => i.complete && i.currentSrc && !i.currentSrc.endsWith('.svg')).map((i) => ({
  src: new URL(i.currentSrc).pathname, w: i.getBoundingClientRect().width, h: i.getBoundingClientRect().height,
  nw: i.naturalWidth, nh: i.naturalHeight, responsive: !!(i.closest('picture') || i.srcset)}))"""


class Browser:
    def __init__(self, ws):
        self.ws, self.counter = ws, iter(range(1, 10**7))

    def send(self, method, session=None, **params):
        n = next(self.counter)
        msg = {"id": n, "method": method, "params": params}
        if session:
            msg["sessionId"] = session
        self.ws.send(json.dumps(msg))
        while True:
            reply = json.loads(self.ws.recv())
            if reply.get("id") == n:
                return reply.get("result", {})

    def open(self, context=None):
        target = self.send("Target.createTarget", url="about:blank", **({"browserContextId": context} if context else {}))
        return self.send("Target.attachToTarget", targetId=target["targetId"], flatten=True)["sessionId"]


def check_sizes(browser, base):
    problems, checked = [], 0
    session = browser.open()
    for width, height, dpr, mobile in VIEWPORTS:
        browser.send("Emulation.setDeviceMetricsOverride", session, width=width, height=height, deviceScaleFactor=dpr, mobile=mobile)
        for path in PAGES:
            browser.send("Page.navigate", session, url=base + path)
            time.sleep(0.8)
            for r in browser.send("Runtime.evaluate", session, expression=MEASURE, returnByValue=True)["result"]["value"]:
                if r["drawn"] == 0:
                    continue
                checked += 1
                if not r["drawn"] - 1 <= r["declared"] <= r["drawn"] * (1 + TOLERANCE) + 2:
                    problems.append(f"{width}px /{path} {r['src']}: disegnata {r['drawn']:.0f}px, dichiarata {r['declared']:.0f}px")
    return problems, checked


def check_pagespeed_phone(browser, base):
    """Load each page cold, as PageSpeed does, and apply its image rule to everything the phone downloaded."""
    width, height, dpr, agent = PSI_PHONE
    problems, checked = [], 0
    for path in PAGES:
        context = browser.send("Target.createBrowserContext")["browserContextId"]
        session = browser.open(context)
        browser.send("Emulation.setDeviceMetricsOverride", session, width=width, height=height, deviceScaleFactor=dpr, mobile=True)
        browser.send("Emulation.setUserAgentOverride", session, userAgent=agent)
        browser.send("Page.navigate", session, url=base + path)
        time.sleep(1.5)
        # Scroll in steps so every lazy image enters the viewport, then wait until all of them have finished.
        browser.send("Runtime.evaluate", session, awaitPromise=True, expression="""(async () => {
          for (let y = 0; y < document.body.scrollHeight; y += innerHeight / 2) { scrollTo(0, y); await new Promise((r) => setTimeout(r, 150)); }
          for (let i = 0; i < 50 && ![...document.images].every((img) => img.complete); i++) await new Promise((r) => setTimeout(r, 100));
        })()""")
        for r in browser.send("Runtime.evaluate", session, expression=LOADED, returnByValue=True)["result"]["value"]:
            if not r["w"]:
                continue
            checked += 1
            named = re.search(r"-(\d+)\.(?:avif|webp)$", r["src"])
            file_w = int(named.group(1)) if named else r["nw"]
            file_h = round(file_w * r["nh"] / r["nw"])
            size = (ROOT / urllib.parse.unquote(r["src"]).lstrip("/")).stat().st_size
            waste = size * (1 - r["w"] * r["h"] / (file_w * file_h))
            if waste > PSI_THRESHOLD[r["responsive"]]:
                problems.append(f"/{path} {r['src'].rsplit('/', 1)[-1]}: {size} byte, {file_w}px mostrata a {r['w']:.0f}px, "
                                f"spreco secondo PageSpeed {waste:.0f} byte")
        browser.send("Target.disposeBrowserContext", browserContextId=context)
    return problems, checked


def main():
    site_port, chrome_port = free_port(), free_port()
    server = http.server.ThreadingHTTPServer(("127.0.0.1", site_port), functools.partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    profile = tempfile.mkdtemp()
    chrome = subprocess.Popen(["google-chrome", "--headless=new", "--no-sandbox", f"--remote-debugging-port={chrome_port}",
                               f"--user-data-dir={profile}", "about:blank"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    base = f"http://127.0.0.1:{site_port}/"
    try:
        for _ in range(50):
            try:
                version = json.load(urllib.request.urlopen(f"http://127.0.0.1:{chrome_port}/json/version"))
                break
            except OSError:
                time.sleep(0.2)
        with connect(version["webSocketDebuggerUrl"], max_size=None) as ws:
            browser = Browser(ws)
            sizes, measured = check_sizes(browser, base)
            phone, loaded = check_pagespeed_phone(browser, base)
    finally:
        chrome.terminate()
        server.shutdown()
        shutil.rmtree(profile, ignore_errors=True)
    print(f"immagini misurate: {measured} ({len(VIEWPORTS)} schermi, {len(PAGES)} pagine), problemi: {len(sizes)}")
    for p in sorted(set(sizes)):
        print("  ", p)
    print(f"immagini caricate dal telefono di PageSpeed: {loaded}, che segnalerebbe: {len(phone)}")
    for p in sorted(set(phone)):
        print("  ", p)
    return 1 if sizes or phone or not measured or not loaded else 0


if __name__ == "__main__":
    sys.exit(main())
