#!/usr/bin/env python3
"""Check that the CSS build.py cuts for each page styles it exactly like the full site.css, in headless Chrome.

Usage: python3 _src/check_css.py
For every sitemap page and 404.html, on a phone, a tablet and a desktop, in light and dark theme and with the states
site.js toggles (long bio, tool filter), every element's computed style (and its ::before/::after) must be identical
with the page's own <style> and with the full site.css put in its place. Needs google-chrome and websockets.
"""
import functools
import http.server
import json
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_sizes import Browser, Quiet, free_port  # noqa: E402

from websockets.sync.client import connect  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PAGES = [loc.removeprefix("https://anthonygozzini.github.io/")
         for loc in re.findall(r"<loc>([^<]+)</loc>", (ROOT / "sitemap.xml").read_text(encoding="utf-8"))
         if "play/" not in loc] + ["404.html"]
VIEWPORTS = [(412, 823, 1.75, True), (900, 1000, 1, False), (1350, 940, 1, False)]
# (label, JS run before both snapshots): the themes and the states site.js switches at runtime.
STATES = [
    ("chiaro", ""),
    ("scuro", "document.documentElement.setAttribute('data-theme','dark')"),
    ("scuro di sistema", "__media('dark')"),
    ("bio lunga e filtro", "document.querySelectorAll('[data-bio-panel]').forEach(p=>p.hidden=!p.hidden);"
                           "document.querySelectorAll('[data-bio]').forEach(b=>b.setAttribute('aria-pressed',String(b.getAttribute('aria-pressed')!=='true')));"
                           "document.querySelectorAll('[data-cat]').forEach((r,i)=>r.hidden=i%2===0);"
                           "document.querySelectorAll('[data-filter]').forEach((t,i)=>t.setAttribute('aria-selected',String(i===1)))"),
]
# site.css animates colours for up to 0.15 s; both snapshots wait for that to finish.
TRANSITIONS = 0.4
SNAPSHOT = """(() => {
  const out = [];
  for (const el of document.querySelectorAll('*')) {
    for (const pseudo of [null, '::before', '::after']) {
      const cs = getComputedStyle(el, pseudo);
      let s = '';
      for (let i = 0; i < cs.length; i++) s += cs[i] + ':' + cs.getPropertyValue(cs[i]) + ';';
      out.push(s);
    }
  }
  return out;
})()"""
NAME = """[...document.querySelectorAll('*')].map((el) => el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.split(' ').join('.') : ''))"""


def main():
    full_css = (ROOT / "assets" / "site.css").read_text(encoding="utf-8")
    site_port, chrome_port = free_port(), free_port()
    server = http.server.ThreadingHTTPServer(("127.0.0.1", site_port), functools.partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    profile = tempfile.mkdtemp()
    chrome = subprocess.Popen(["google-chrome", "--headless=new", "--no-sandbox", f"--remote-debugging-port={chrome_port}",
                               f"--user-data-dir={profile}", "about:blank"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    problems, compared = [], 0
    try:
        for _ in range(100):
            try:
                version = json.load(urllib.request.urlopen(f"http://127.0.0.1:{chrome_port}/json/version"))
                break
            except OSError:
                time.sleep(0.2)
        with connect(version["webSocketDebuggerUrl"], max_size=None) as ws:
            browser = Browser(ws)
            session = browser.open()
            for width, height, dpr, mobile in VIEWPORTS:
                browser.send("Emulation.setDeviceMetricsOverride", session, width=width, height=height, deviceScaleFactor=dpr, mobile=mobile)
                for path in PAGES:
                    for label, script in STATES:
                        media = "dark" if "__media" in script else "light"
                        browser.send("Emulation.setEmulatedMedia", session, features=[{"name": "prefers-color-scheme", "value": media}])
                        browser.send("Page.navigate", session, url=f"http://127.0.0.1:{site_port}/{path}")
                        time.sleep(0.6)
                        if script and "__media" not in script:
                            browser.send("Runtime.evaluate", session, expression=script)
                            time.sleep(TRANSITIONS)
                        cut = browser.send("Runtime.evaluate", session, expression=SNAPSHOT, returnByValue=True)["result"]["value"]
                        browser.send("Runtime.evaluate", session, expression=f"document.querySelector('head style').textContent={json.dumps(full_css)}")
                        time.sleep(TRANSITIONS)
                        whole = browser.send("Runtime.evaluate", session, expression=SNAPSHOT, returnByValue=True)["result"]["value"]
                        names = browser.send("Runtime.evaluate", session, expression=NAME, returnByValue=True)["result"]["value"]
                        compared += len(cut)
                        if len(cut) != len(whole):
                            problems.append(f"{width}px {label} /{path}: numero di elementi diverso")
                            continue
                        for i, (a, b) in enumerate(zip(cut, whole)):
                            if a != b:
                                da, db = dict(x.split(":", 1) for x in a.split(";") if ":" in x), dict(x.split(":", 1) for x in b.split(";") if ":" in x)
                                diff = sorted(k for k in da.keys() | db.keys() if da.get(k) != db.get(k))[:3]
                                element = names[i // 3] + ("", "::before", "::after")[i % 3]
                                problems.append(f"{width}px {label} /{path} {element}: {', '.join(f'{k} {da.get(k)} ≠ {db.get(k)}' for k in diff)}")
    finally:
        chrome.terminate()
        server.shutdown()
        shutil.rmtree(profile, ignore_errors=True)
    print(f"stili confrontati: {compared} ({len(VIEWPORTS)} schermi, {len(PAGES)} pagine, {len(STATES)} stati), differenze: {len(problems)}")
    for p in problems[:30]:
        print("  ", p)
    return 1 if problems or not compared else 0


if __name__ == "__main__":
    sys.exit(main())
