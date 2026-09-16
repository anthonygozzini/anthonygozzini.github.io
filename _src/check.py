#!/usr/bin/env python3
"""Check the generated site: every internal link, image and anchor must resolve; external links are fetched.

Usage: python3 _src/check.py [--external]
"""
import html
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urldefrag

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "_src", "node_modules"}
SITE = "https://anthonygozzini.github.io/"
# Google cuts desktop snippets at about 920px, which for this site's text is roughly 155 characters.
DESCRIPTION_MAX = 155


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.ids = [], set()
        self.meta, self.canonical, self.markdown, self.jsonld, self._in_ld = {}, [], [], [], False
        self.lang = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta" and (a.get("name") or a.get("property")):
            self.meta.setdefault(a.get("name") or a.get("property"), []).append(a.get("content") or "")
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical.append(a.get("href"))
        if tag == "link" and a.get("rel") == "alternate" and a.get("type") == "text/markdown":
            self.markdown.append(a.get("href"))
        self._in_ld = tag == "script" and a.get("type") == "application/ld+json"
        self._in_style = tag == "style"
        if "id" in a:
            self.ids.add(a["id"])
        for key in ("href", "src"):
            if key in a and a[key] and not (tag == "use" or a[key].startswith("#i-")):
                self.refs.append(a[key])
        if a.get("srcset"):
            # Candidates are separated by a comma and a space: data: URLs carry a bare comma of their own.
            self.refs += [candidate.split()[0] for candidate in re.split(r",\s+", a["srcset"])]

    def handle_data(self, data):
        if self._in_ld:
            self.jsonld.append(data)
        if getattr(self, "_in_style", False):
            self.refs += re.findall(r"""url\(\s*['"]?(?!data:)([^'")]+)['"]?\s*\)""", data)

    def handle_endtag(self, tag):
        self._in_ld = self._in_style = False


def pages():
    for path in ROOT.rglob("*.html"):
        if not SKIP_DIRS.intersection(path.relative_to(ROOT).parts):
            yield path


def parse(path):
    c = Collector()
    c.feed(path.read_text(encoding="utf-8"))
    return c


def site_file(url):
    """The local file behind a URL of this site, or None when the path belongs to another repository's Pages."""
    path = urldefrag(url)[0].removeprefix(SITE)
    if path and not (ROOT / path.split("/", 1)[0]).exists():
        return None
    return ROOT / path / "index.html" if path == "" or path.endswith("/") else ROOT / path


def markdown_problems(name, text):
    problems = []
    for url in sorted(set(re.findall(r"\]\((" + re.escape(SITE) + r"[^)\s]*)\)", text))):
        target = site_file(url)
        if target is not None and not target.exists():
            problems.append(f"{name}: link a un file mancante {url}")
    if re.search(r"</?[a-z][^>]*>", text):
        problems.append(f"{name}: contiene tag HTML")
    return problems


def llms_problems(locs):
    """llms.txt as llmstxt.org defines it: an H1, a blockquote summary, then H2 sections of links; every page reachable from it."""
    path = ROOT / "llms.txt"
    if not path.exists():
        return ["llms.txt: manca"]
    text = path.read_text(encoding="utf-8")
    blocks = [b for b in text.split("\n\n") if b.strip()]
    problems = []
    if not blocks or not re.fullmatch(r"# [^\n]+", blocks[0]):
        problems.append("llms.txt: la prima riga non è un titolo H1")
    if len(blocks) < 2 or not blocks[1].startswith("> "):
        problems.append("llms.txt: manca il riassunto in blockquote dopo il titolo")
    for block in blocks[2:]:
        if block.startswith("#") and not re.fullmatch(r"## [^\n]+", block):
            problems.append(f"llms.txt: intestazione non ammessa: {block.splitlines()[0]}")
    after_h2 = False
    for block in blocks[2:]:
        after_h2 = after_h2 or block.startswith("## ")
        if after_h2 and not block.startswith("## ") and not all(re.match(r"- \[[^\]]+\]\([^)]+\)", l) for l in block.splitlines()):
            problems.append(f"llms.txt: sezione con righe che non sono link: {block.splitlines()[0][:60]}")
    linked = set(re.findall(r"\]\((" + re.escape(SITE) + r"[^)\s]*index\.md)\)", text))
    missing = [loc for loc in locs if loc + "index.md" not in linked]
    if missing:
        problems.append(f"llms.txt: pagine non raggiungibili: {missing}")
    return problems + markdown_problems("llms.txt", text)


CDN = re.compile(r"^https://cdn\.jsdelivr\.net/gh/anthonygozzini/anthonygozzini\.github\.io@([0-9a-f]{40})/(.+)$")


def cdn_problems(urls):
    """Every jsDelivr link must name a commit that has the file, byte for byte what is in the working tree."""
    pinned = [(m.group(1), m.group(2)) for m in map(CDN.match, sorted(urls)) if m]
    if not pinned:
        return 0, []
    def git(*args, stdin=None):
        return subprocess.run(["git", "-C", str(ROOT), *args], input=stdin, capture_output=True, text=True).stdout.splitlines()
    committed = git("rev-parse", *[f"{sha}:{path}" for sha, path in pinned])
    current = git("hash-object", *[str(ROOT / path) for _, path in pinned])
    problems = []
    for (sha, path), old, new in zip(pinned, committed + [""] * len(pinned), current + [""] * len(pinned)):
        if not (ROOT / path).exists():
            problems.append(f"CDN {sha[:7]}/{path}: il file non esiste più")
        elif old != new:
            problems.append(f"CDN {sha[:7]}/{path}: diverso dal file attuale (ricostruisci dopo il commit)")
    return len(pinned), problems


def font_problems(pages):
    """Every character a page shows must be in the font build.py embeds (see _src/fonts.py), or it falls back mid-word."""
    coverage = ROOT / "_src" / "fonts" / "coverage.txt"
    if not coverage.exists():
        return ["_src/fonts/coverage.txt manca: esegui python3 _src/fonts.py"]
    faces = dict(line.split("\t", 1) for line in coverage.read_text(encoding="utf-8").splitlines())
    sans = set(faces["geist-sans.woff2"])
    problems = []
    for page in pages:
        text = page.read_text(encoding="utf-8")
        if "document.fonts.add(new FontFace(" not in text:
            continue
        text = re.sub(r"<(script|style)\b.*?</\1>", " ", text, flags=re.S)
        shown = set(html.unescape(re.sub(r"<[^>]+>", " ", text)))
        missing = sorted(c for c in shown - sans if not c.isspace())
        if missing:
            problems.append(f"{page.relative_to(ROOT)}: caratteri fuori dal font incorporato {''.join(missing)} (aggiungili in _src/fonts.py)")
    return problems


def seo_problems(cache):
    """Every sitemap URL: its own description within the snippet limit, a matching canonical and og:url, valid JSON-LD naming the
    person, and a markdown copy that the page links to."""
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    locs = re.findall(r"<loc>([^<]+)</loc>", sitemap)
    problems = llms_problems(locs)
    if len(locs) != len(re.findall(r"<lastmod>\d{4}-\d{2}-\d{2}</lastmod>", sitemap)):
        problems.append("sitemap.xml: non tutte le URL hanno <lastmod>")
    robots = ROOT / "robots.txt"
    if not robots.exists() or f"Sitemap: {SITE}sitemap.xml" not in robots.read_text(encoding="utf-8"):
        problems.append("robots.txt: manca o non dichiara la sitemap")
    elif "Disallow: /*.md$" not in robots.read_text(encoding="utf-8"):
        problems.append("robots.txt: le copie markdown non sono escluse dai motori di ricerca")
    seen = {}
    for loc in locs:
        path = ROOT / loc.removeprefix(SITE) / "index.html"
        name = path.relative_to(ROOT)
        info = cache.get(path)
        if info is None:
            problems.append(f"{loc}: nessuna pagina generata")
            continue
        descriptions = info.meta.get("description", [])
        if len(descriptions) != 1:
            problems.append(f"{name}: {len(descriptions)} meta description")
            continue
        text = descriptions[0]
        if len(text) > DESCRIPTION_MAX:
            problems.append(f"{name}: description di {len(text)} caratteri (max {DESCRIPTION_MAX})")
        if text in seen:
            problems.append(f"{name}: description uguale a {seen[text]}")
        seen.setdefault(text, name)
        if info.canonical != [loc] or info.meta.get("og:url") != [loc]:
            problems.append(f"{name}: canonical {info.canonical} / og:url {info.meta.get('og:url')} diversi da {loc}")
        try:
            nodes = [n for block in info.jsonld for n in json.loads(block)["@graph"]]
        except (ValueError, KeyError) as e:
            problems.append(f"{name}: JSON-LD non valido ({e})")
            continue
        if not any(n.get("@type") == "Person" and n.get("sameAs") for n in nodes):
            problems.append(f"{name}: JSON-LD senza Person con sameAs")
        if info.lang not in ("en", "it"):
            problems.append(f"{name}: lang={info.lang}")
        md = path.with_name("index.md")
        if info.markdown != [loc + "index.md"]:
            problems.append(f"{name}: link alla copia markdown {info.markdown}")
        if not md.exists() or not md.read_text(encoding="utf-8").startswith("# "):
            problems.append(f"{md.relative_to(ROOT)}: manca o non inizia con un titolo")
        else:
            problems += markdown_problems(md.relative_to(ROOT), md.read_text(encoding="utf-8"))
    return locs, problems


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
            base = ROOT if url.startswith("/") else page.parent
            target = (base / url.lstrip("/")).resolve() if url else page
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

    seo = seo_problems(cache)
    print(f"pagine SEO controllate: {len(seo[0])}, problemi: {len(seo[1])}")
    for p in seo[1]:
        print("  ", p)
    problems += seo[1]
    cdn_count, cdn = cdn_problems(external)
    print(f"link al CDN controllati: {cdn_count}, problemi: {len(cdn)}")
    for p in cdn:
        print("  ", p)
    problems += cdn
    fonts = font_problems(cache)
    print(f"pagine con font incorporati controllate: {len(cache)}, problemi: {len(fonts)}")
    for p in fonts:
        print("  ", p)
    problems += fonts

    bad_external = []
    if "--external" in sys.argv:
        for url in sorted(external):
            # Canonical and hreflang URLs point at the deployed site, which only exists after a push.
            if "fonts.g" in url or url.startswith("https://anthonygozzini.github.io/") or CDN.match(url):
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
