#!/usr/bin/env python3
"""Check the generated site: every internal link, image and anchor must resolve; external links are fetched.

Usage: python3 _src/check.py [--external]
"""
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urldefrag

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "_src", "node_modules"}


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        for key in ("href", "src"):
            if key in a and a[key] and not (tag == "use" or a[key].startswith("#i-")):
                self.refs.append(a[key])


def pages():
    for path in ROOT.rglob("*.html"):
        if not SKIP_DIRS.intersection(path.relative_to(ROOT).parts):
            yield path


def parse(path):
    c = Collector()
    c.feed(path.read_text(encoding="utf-8"))
    return c


def main():
    external = set()
    problems = []
    checked = 0
    cache = {}
    for page in sorted(pages()):
        info = parse(page)
        cache[page] = info
        for ref in info.refs:
            if ref.startswith(("http://", "https://")):
                external.add(ref)
                continue
            if ref.startswith(("mailto:", "tel:", "data:")):
                continue
            url, frag = urldefrag(ref)
            target = (page.parent / url).resolve() if url else page
            if target.is_dir() or url.endswith("/") or url in ("", "./"):
                target = target / "index.html" if target.is_dir() or url.endswith("/") else target
            checked += 1
            if not target.exists():
                problems.append(f"{page.relative_to(ROOT)} → {ref} (file mancante)")
                continue
            if frag and target.suffix == ".html":
                ids = cache[target].ids if target in cache else parse(target).ids
                if frag not in ids:
                    problems.append(f"{page.relative_to(ROOT)} → {ref} (ancora #{frag} mancante)")
    print(f"link interni controllati: {checked}, problemi: {len(problems)}")
    for p in problems:
        print("  ", p)

    bad_external = []
    if "--external" in sys.argv:
        for url in sorted(external):
            # Canonical and hreflang URLs point at the deployed site, which only exists after a push.
            if "fonts.g" in url or url.startswith("https://anthonygozzini.github.io/"):
                continue
            out = subprocess.run(["curl", "-s", "-o", "/dev/null", "-L", "-m", "25", "-A", "Mozilla/5.0", "-w", "%{http_code}", url],
                                 capture_output=True, text=True)
            code = out.stdout.strip()
            ok = code.startswith(("2", "3")) or (code == "999" and "linkedin.com" in url)
            if not ok:
                bad_external.append(f"{code} {url}")
        print(f"link esterni controllati: {len([u for u in external if 'fonts.g' not in u])}, non raggiungibili: {len(bad_external)}")
        for b in bad_external:
            print("  ", b)
    return 1 if problems or bad_external else 0


if __name__ == "__main__":
    sys.exit(main())
