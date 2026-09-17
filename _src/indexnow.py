#!/usr/bin/env python3
"""Tell the IndexNow search engines (Bing and the others that share its submissions) which pages changed.

Usage: python3 _src/indexnow.py BEFORE AFTER [--dry-run]   pages whose content changed between two commits
       python3 _src/indexnow.py --all [--dry-run]           every page in sitemap.xml
A page counts as changed when its fingerprint in lastmod.json differs, so markup-only builds send nothing; pages that
disappeared are sent too, so the engines drop them. .github/workflows/indexnow.yml runs this after GitHub Pages has
published each push. The key file <KEY>.txt at the site root proves the submissions come from this site.
"""
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import content as C  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
KEY = "1d90d0a5996318c79cf4bd9071698dd3"
ENDPOINT = "https://api.indexnow.org/indexnow"
STAMPS = "_src/lastmod.json"


def stamps_at(commit):
    shown = subprocess.run(["git", "show", f"{commit}:{STAMPS}"], cwd=ROOT, capture_output=True, text=True)
    return json.loads(shown.stdout) if shown.returncode == 0 else {}


def changed_pages(before, after):
    old, new = stamps_at(before), stamps_at(after)
    paths = sorted(p for p in old.keys() | new.keys() if (old.get(p) or {}).get("hash") != (new.get(p) or {}).get("hash"))
    return [f'{C.SITE["url"]}/{p}' for p in paths]


def all_pages():
    return re.findall(r"<loc>([^<]+)</loc>", (ROOT / "sitemap.xml").read_text(encoding="utf-8"))


def submit(urls):
    body = json.dumps({"host": C.SITE["url"].split("://", 1)[1], "key": KEY,
                       "keyLocation": f'{C.SITE["url"]}/{KEY}.txt', "urlList": urls}).encode()
    request = urllib.request.Request(ENDPOINT, data=body, headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status, response.read().decode(errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace")


def main(args):
    dry = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]
    if args == ["--all"]:
        urls = all_pages()
    elif len(args) == 2:
        urls = changed_pages(*args)
    else:
        print(__doc__)
        return 2
    print(f"pagine da segnalare: {len(urls)}")
    for u in urls:
        print("  ", u)
    if not urls or dry:
        return 0
    status, text = submit(urls)
    # 200: received; 202: received, the key file is still being checked.
    print(f"IndexNow: {status} {text[:200]}".rstrip())
    return 0 if status in (200, 202) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
