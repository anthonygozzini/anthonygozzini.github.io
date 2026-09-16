#!/usr/bin/env python3
"""Generate the static site from content.py: English at the repository root, Italian under it/.

Usage: python3 _src/build.py [--preview]
  --preview  write links as .../index.html, so pages also work when opened straight from disk.
"""
import datetime
import hashlib
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import content as C  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PREVIEW = "--preview" in sys.argv
LANGS = ("en", "it")
LOCALES = {"en": "en_US", "it": "it_IT"}
STAMPS_FILE = Path(__file__).resolve().parent / "lastmod.json"
stamps = json.loads(STAMPS_FILE.read_text(encoding="utf-8")) if STAMPS_FILE.exists() else {}
MONTHS = {
    "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "it": ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"],
}
warnings = []


def esc(s):
    return html.escape(str(s), quote=True)


def tr(value, lang):
    if isinstance(value, dict) and set(value) == {"en", "it"}:
        return value[lang]
    return value


def fmt_month(date, lang):
    parts = date.split("-")
    if len(parts) == 1:
        return parts[0]
    return f"{MONTHS[lang][int(parts[1]) - 1]} {parts[0]}"


def fmt_day(date, lang):
    y, m, d = date.split("-")
    return f"{int(d)} {MONTHS[lang][int(m) - 1]} {y}"


class Page:
    def __init__(self, lang, path):
        self.lang = lang
        self.path = path
        self.full = ("it/" if lang == "it" else "") + path
        self.prefix = "../" * self.full.count("/")

    def link(self, target, lang=None):
        if target.startswith(("http://", "https://", "mailto:")):
            return target
        if target == "cal":
            return C.SITE["cal"]
        if target == "cv":
            return self.prefix + C.SITE["cv"]
        path, _, frag = target.partition("#")
        full = ("it/" if (lang or self.lang) == "it" else "") + path
        if PREVIEW:
            full += "index.html"
        url = (self.prefix + full) or "./"
        return url + (f"#{frag}" if frag else "")

    def asset(self, rel):
        return f"{self.prefix}assets/{rel}"

    def raw(self, path):
        """Link to a folder that exists once for both languages, such as play/sgamers/."""
        return self.prefix + path + ("index.html" if PREVIEW and path.endswith("/") else "")


ICONS = {
    "home": '<path d="M3 10.5 12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.2-4 4.3-6 8-6s6.8 2 8 6"/>',
    "code": '<path d="m8 6-6 6 6 6M16 6l6 6-6 6"/>',
    "pen": '<path d="M4 20h4L19.5 8.5a2.1 2.1 0 0 0-3-3L5 17z"/><path d="m14.5 7.5 3 3"/>',
    "box": '<path d="M3 7.5 12 3l9 4.5v9L12 21l-9-4.5z"/><path d="M3 7.5 12 12l9-4.5M12 12v9"/>',
    "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20.5l1.4-4.8A8 8 0 1 1 21 12z"/>',
    "calendar": '<rect x="3" y="4.5" width="18" height="16" rx="2"/><path d="M3 9.5h18M8 3v3M16 3v3"/>',
    "linkedin": '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M8 10.5V17M8 7.2v.1M12 17v-6.5M12 13.5a2.5 2.5 0 0 1 5 0V17"/>',
    "github": '<path d="M9 19c-4.3 1.4-4.3-2.5-6-3m12 5v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1.1-.3-3.5 1.3a12.3 12.3 0 0 0-6.2 0C6.5 2.8 5.4 3.1 5.4 3.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4 9.5c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V21"/>',
    "arrow": '<path d="M7 17 17 7M8 7h9v9"/>',
    "right": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "moon": '<path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/>',
    "monitor": '<rect x="3" y="4" width="18" height="12.5" rx="2"/><path d="M8.5 20.5h7M12 16.5v4"/>',
    "tag": '<path d="M3 12V4a1 1 0 0 1 1-1h8l9 9-9 9z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
    "game": '<rect x="2" y="7" width="20" height="11" rx="5.5"/><path d="M7 10.5v4M5 12.5h4M15.5 11.5h.01M18 13.5h.01"/>',
    "flag": '<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>',
    "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/>',
    "cap": '<path d="m2 9 10-5 10 5-10 5z"/><path d="M6 11v5c3 2.5 9 2.5 12 0v-5M22 9v6"/>',
    "bot": '<rect x="4" y="8" width="16" height="12" rx="3"/><path d="M12 4v4M9 13h.01M15 13h.01M9 17h6"/>',
    "mic": '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.8-3.5 3.3-5.5 6.5-5.5s5.7 2 6.5 5.5M16 4.8a3.5 3.5 0 0 1 0 6.4M18 14.8c1.8.8 3 2.5 3.5 5.2"/>',
    "coin": '<circle cx="12" cy="12" r="9"/><path d="M14.8 9.2A3 3 0 0 0 12 8c-1.7 0-3 .9-3 2s1.3 1.7 3 2 3 .9 3 2-1.3 2-3 2a3 3 0 0 1-2.8-1.2M12 6v2M12 16v2"/>',
    "plane": '<path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/>',
    "download": '<path d="M12 4v12M7 11l5 5 5-5M5 20h14"/>',
    "check": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    "copy": '<rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V5a1 1 0 0 1 1-1h10"/>',
    "send": '<path d="M21 3 10 14M21 3l-7 18-4-7-7-4z"/>',
    "whatsapp": '<path d="M3.5 20.5 5 16a8.5 8.5 0 1 1 3 3z"/><path d="M9 9.5c0 3 2.5 5.5 5.5 5.5l1-1.5-2-1-1 1a3.8 3.8 0 0 1-2-2l1-1-1-2z"/>',
}


def icon(name, cls="i"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'


def sprite():
    symbols = "".join(
        f'<symbol id="i-{k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{v}</symbol>'
        for k, v in ICONS.items())
    return f'<svg width="0" height="0" style="position:absolute" aria-hidden="true">{symbols}</svg>'


# The width each kind of image is drawn at, measured in Chrome from the layout in site.css (sidebar from 881px, content
# capped at 1100px from 1516px), so the browser picks the smallest WebP that covers it. check_sizes.py re-measures them.
SIZES = {
    "grid": "(max-width: 600px) calc(100vw - 62px), (max-width: 880px) calc(50vw - 51px), "
            "(max-width: 1180px) calc(50vw - 221px), (max-width: 1516px) calc(25vw - 139px), 240px",
    "grid3": "(max-width: 880px) calc(50vw - 51px), (max-width: 1180px) calc(33.3vw - 160px), "
             "(max-width: 1516px) calc(33.3vw - 171px), 332px",
    "feature": "(max-width: 880px) calc(100vw - 66px), (max-width: 1100px) calc(100vw - 405px), "
               "(max-width: 1180px) calc(53.5vw - 233px), (max-width: 1516px) calc(53.5vw - 248px), 560px",
    "project": "(max-width: 696px) calc(100vw - 38px), (max-width: 880px) 658px, (max-width: 1035px) calc(100vw - 377px), 658px",
    "post": "(max-width: 796px) calc(100vw - 36px), (max-width: 880px) 760px, (max-width: 1135px) calc(100vw - 375px), 760px",
    "play": "(max-width: 960px) 100vw, 960px",
}
STYLE = (ROOT / "assets" / "site.css").read_text(encoding="utf-8")


def picture(page, file, alt, sizes, priority="lazy", extra=""):
    """A JPEG with WebP copies from images.py. priority: "lazy" below the fold, "high" for the image that is the page's LCP."""
    if not (file and (ROOT / "assets" / "img" / file).exists()):
        warnings.append(f"immagine mancante: assets/img/{file}")
        return ""
    stem = Path(file).with_suffix("").as_posix().replace("/", "--")
    sized = sorted((int(w), f.name) for f in (ROOT / "assets" / "img" / "sized").glob(f"{stem}-*.webp")
                   for base, _, w in [f.stem.rpartition("-")] if base == stem and w.isdigit())
    loading = {"lazy": ' loading="lazy"', "high": ' fetchpriority="high"'}.get(priority, "")
    img = f'<img src="{page.asset("img/" + file)}" alt="{esc(alt)}"{extra}{loading}>'
    if not sized:
        warnings.append(f"copie webp mancanti per assets/img/{file}: esegui python3 _src/images.py")
        return img
    srcset = ", ".join(f'{page.asset("img/sized/" + name)} {w}w' for w, name in sized)
    return f'<picture><source type="image/webp" srcset="{srcset}" sizes="{sizes}">{img}</picture>'


def cover(page, file, alt, sizes, priority="lazy"):
    return picture(page, file, alt, SIZES[sizes], priority)


def logo(page, key, name, cls="tile"):
    for ext in ("svg", "png"):
        if (ROOT / "assets" / "logos" / f"{key}.{ext}").exists():
            return f'<span class="{cls}"><img src="{page.asset(f"logos/{key}.{ext}")}" alt="" loading="lazy"></span>'
    warnings.append(f"logo mancante: {key}")
    initials = "".join(w[0] for w in name.split()[:2]).upper()
    return f'<span class="{cls} tile-text" aria-hidden="true">{esc(initials)}</span>'


def ext_attrs(href):
    return ' target="_blank" rel="noopener"' if href.startswith("http") else ""


def card(href, title, text, meta="", top="", external=False, tag="a"):
    arrow = f'<span class="card-arrow">{icon("arrow")}</span>' if external else ""
    open_tag = f'<a class="card" href="{href}"{ext_attrs(href) if external else ""}>' if tag == "a" else '<div class="card">'
    close_tag = "</a>" if tag == "a" else "</div>"
    return (f'{open_tag}{top}<h3 class="card-title">{esc(title)}{arrow}</h3>'
            f'<p class="card-text">{esc(text)}</p>'
            + (f'<p class="card-meta">{esc(meta)}</p>' if meta else "") + close_tag)


def lang_switch(page):
    links = []
    for code in LANGS:
        current = ' aria-current="true"' if code == page.lang else ""
        links.append(f'<a class="seg-btn" href="{page.link(page.path, code)}" hreflang="{code}" lang="{code}"{current}>{code.upper()}</a>')
    return f'<div class="seg seg-lang" role="group" aria-label="{esc(tr(C.UI["language"], page.lang))}">{"".join(links)}</div>'


def theme_switch(page):
    buttons = "".join(
        f'<button type="button" class="seg-btn" data-theme-set="{mode}" aria-pressed="{"true" if mode == "auto" else "false"}">{esc(tr(C.UI["theme_" + mode], page.lang))}</button>'
        for mode in ("light", "dark", "auto"))
    return f'<div class="seg seg-theme" role="group" aria-label="{esc(tr(C.UI["theme"], page.lang))}">{buttons}</div>'


def sidebar(page, key):
    lang = page.lang
    out = [f'<aside class="sidebar"><a class="brand" href="{page.link("")}"><span class="brand-mark" aria-hidden="true">AG</span><span class="brand-name">Anthony Gozzini</span></a>',
           f'<nav class="nav" aria-label="{esc(tr(C.UI["pages"], lang))}">']
    groups = [
        (None, [n for n in C.NAV if "group" not in n]),
        ("resources", [n for n in C.NAV if n.get("group") == "resources"]),
        ("connect", [n for n in C.NAV if n.get("group") == "connect"]),
    ]
    number = 0
    for group, items in groups:
        if group:
            out.append(f'<div class="nav-sep"></div><p class="nav-label">{esc(tr(C.UI[group], lang))}</p>')
        out.append('<ul class="nav-list">')
        for n in items:
            number += 1
            current = ' aria-current="page"' if n["key"] == key else ""
            out.append(f'<li><a class="nav-item" href="{page.link(n["path"])}" data-shortcut="{number}"{current}>{icon(n["icon"])}<span>{esc(tr(n["label"], lang))}</span><kbd class="kbd">{number}</kbd></a></li>')
        if group == "connect":
            for label, href, ic in ((tr(C.UI["book_call"], lang), C.SITE["cal"], "calendar"),
                                    ("LinkedIn", C.SITE["linkedin"], "linkedin"),
                                    ("GitHub", C.SITE["github"], "github")):
                out.append(f'<li><a class="nav-item" href="{href}" target="_blank" rel="noopener">{icon(ic)}<span>{esc(label)}</span><span class="nav-ext">{icon("arrow")}</span></a></li>')
        out.append("</ul>")
    out.append(f'</nav><div class="sidebar-foot">{lang_switch(page)}{theme_switch(page)}</div></aside>')
    return "".join(out)


def mobile_top(page):
    label = esc(tr(C.UI["theme"], page.lang))
    return (f'<header class="mtop"><a class="brand" href="{page.link("")}" aria-label="Anthony Gozzini"><span class="brand-mark" aria-hidden="true">AG</span><span class="brand-name">Anthony Gozzini</span></a>'
            f'<div class="mtop-actions">{lang_switch(page)}<button type="button" class="icon-btn" data-theme-cycle aria-label="{label}">'
            f'{icon("sun", "i i-light")}{icon("moon", "i i-dark")}{icon("monitor", "i i-auto")}</button></div></header>')


def tabbar(page, key):
    items = []
    for n in C.NAV:
        current = ' aria-current="page"' if n["key"] == key else ""
        items.append(f'<a class="tab-item" href="{page.link(n["path"])}"{current}>{icon(n["icon"])}<span>{esc(tr(n["label"], page.lang))}</span></a>')
    return f'<nav class="tabbar" aria-label="{esc(tr(C.UI["pages"], page.lang))}">{"".join(items)}</nav>'


def content_digest(body):
    """Fingerprint of what a reader gets: the visible text plus each image and its alt text, not the markup around them."""
    body = re.sub(r"<(script|style)\b.*?</\1>", " ", body, flags=re.S)
    images = [(re.search(r'\ssrc="([^"]*)"', attrs).group(1), (re.search(r'\salt="([^"]*)"', attrs) or [None, ""])[1])
              for attrs in re.findall(r"<img\b([^>]*)>", body)]
    text = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", body)).split())
    return hashlib.sha256((text + repr(images)).encode("utf-8")).hexdigest()[:16]


def modified(page, body):
    """Date the page's content last changed: kept while its content_digest is the same, today once it differs."""
    digest = content_digest(body)
    entry = stamps.get(page.full)
    # Preview bodies carry index.html links, so their hash never matches: keep the published date.
    if entry and (entry["hash"] == digest or PREVIEW):
        return entry["date"]
    today = datetime.date.today().isoformat()
    if not PREVIEW:
        stamps[page.full] = {"hash": digest, "date": today}
    return today


def graph(page, title, description, page_type, extra=(), main=None):
    base = C.SITE["url"] + "/"
    url = base + page.full
    me = {"@id": base + "#person"}
    nodes = [
        {"@type": "Person", "@id": me["@id"], "name": C.SITE["name"], "url": base, "image": base + "assets/img/anthony.jpg",
         "jobTitle": C.SITE["job_title"], "description": tr(C.SITE["description"], page.lang),
         "sameAs": [C.SITE["linkedin"], C.SITE["github"]], "knowsAbout": C.SITE["knows_about"],
         "knowsLanguage": list(LANGS), "homeLocation": {"@type": "Country", "name": C.SITE["country"]}},
        {"@type": "WebSite", "@id": base + "#website", "url": base, "name": C.SITE["name"], "inLanguage": list(LANGS), "publisher": me},
        {"@type": page_type, "@id": url + "#webpage", "url": url, "name": title, "description": description,
         "inLanguage": page.lang, "isPartOf": {"@id": base + "#website"},
         ("mainEntity" if page_type == "ProfilePage" else "about"): me},
        *extra,
    ]
    if main:
        nodes[2]["mainEntity"] = {"@id": main}
    text = json.dumps({"@context": "https://schema.org", "@graph": nodes}, ensure_ascii=False, separators=(",", ":"))
    return '<script type="application/ld+json">' + text.replace("</", "<\\/") + "</script>\n"


def post_graph(page, post, description, date_modified):
    base = C.SITE["url"] + "/"
    url = base + page.full
    title = tr(post["title"], page.lang)
    return [
        {"@type": "BlogPosting", "@id": url + "#article", "headline": title, "description": description,
         "datePublished": post["date"], "dateModified": date_modified, "inLanguage": page.lang,
         "image": base + "assets/img/" + post["cover"], "mainEntityOfPage": {"@id": url + "#webpage"},
         "author": {"@type": "Person", "@id": base + "#person", "name": C.SITE["name"], "url": base},
         "publisher": {"@id": base + "#person"}, "isPartOf": {"@id": base + "#website"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": tr(C.WRITING["title"], page.lang), "item": base + Page(page.lang, "writing/").full},
            {"@type": "ListItem", "position": 2, "name": title, "item": url}]},
    ]


def head_tags(page, title, description, meta):
    """Title, description, canonical, language alternates, markdown copy, JSON-LD and social tags."""
    lang = page.lang
    base = C.SITE["url"] + "/"
    both = meta.get("both_langs", True)
    tags = f'<title>{esc(title)}</title>\n<meta name="description" content="{esc(description)}">\n'
    if C.SITE["google_verification"] and page.full == "" and not meta.get("noindex"):
        tags += f'<meta name="google-site-verification" content="{esc(C.SITE["google_verification"])}">\n'
    if meta.get("noindex"):
        tags += '<meta name="robots" content="noindex">\n'
    else:
        url = base + page.full
        tags += f'<link rel="canonical" href="{url}">\n'
        if both:
            tags += "".join(
                f'<link rel="alternate" hreflang="{code}" href="{base}{("it/" if code == "it" else "") + page.path}">' for code in LANGS)
            tags += f'<link rel="alternate" hreflang="x-default" href="{base}{page.path}">\n'
        tags += (f'<link rel="alternate" type="text/markdown" href="{url}index.md">\n'
                 f'<link rel="describedby" href="{base}llms.txt">\n'
                 f'<meta property="og:url" content="{url}">\n')
        if meta.get("published"):
            tags += f'<meta property="article:published_time" content="{meta["published"]}">\n'
        tags += meta.get("jsonld", "")
    tags += (f'<meta property="og:type" content="{meta.get("type", "website")}">\n'
             f'<meta property="og:site_name" content="{esc(C.SITE["name"])}">\n'
             f'<meta property="og:locale" content="{LOCALES[lang]}">\n')
    if both:
        tags += "".join(f'<meta property="og:locale:alternate" content="{LOCALES[c]}">\n' for c in LANGS if c != lang)
    return tags + (f'<meta property="og:title" content="{esc(title)}">\n'
                   f'<meta property="og:description" content="{esc(description)}">\n'
                   f'<meta property="og:image" content="{base}assets/img/{meta.get("image", "og.jpg")}">\n'
                   f'<meta property="og:image:alt" content="{esc(meta.get("image_alt", tr(C.HOME["title"], lang)))}">\n'
                   '<meta name="twitter:card" content="summary_large_image">\n')


def inline_style(page):
    """site.css inside the page: one request fewer before the first paint, and GitHub Pages caches files for 10 minutes anyway.

    The fonts are deliberately not preloaded: Chrome holds the first paint for preloaded fonts (RenderBlockingFonts), and on
    GitHub Pages that hold ran to its 1.5 s cap on most pages even after the fonts had arrived (traced 2026-09-16)."""
    return re.sub(r"""url\(\s*['"]?(?!data:)([^'")]+)['"]?\s*\)""", lambda m: f"url({page.asset(m.group(1))})", STYLE)


def document(page, key, title, description, body, width, meta):
    lang = page.lang
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{head_tags(page, title, description, meta)}<meta name="theme-color" content="#E9EDF2">
<link rel="icon" href="{page.asset('favicon.svg')}" type="image/svg+xml">
<style>{inline_style(page)}</style>
<script>try{{var t=localStorage.getItem('ag-theme');if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
</head>
<body>
<a class="skip" href="#main">{esc(tr(C.UI["skip"], lang))}</a>
{sprite()}
<div class="spot" aria-hidden="true"></div>
{mobile_top(page)}
<div class="shell">
{sidebar(page, key)}
<main id="main" class="panel">
<div class="page page-{width}">
{body}
</div>
<footer class="foot"><p>© 2026 Anthony Gozzini</p><p>{esc(tr(C.UI["footer"], lang))}</p></footer>
</main>
</div>
{tabbar(page, key)}
<script src="{page.asset('site.js')}" defer></script>
</body>
</html>
"""


def greeting_script(lang):
    """Swap the fallback greeting for the time of day before the first paint, so the heading never changes size on screen."""
    words = json.dumps(tr(C.UI["greetings"], lang), ensure_ascii=False)
    return ("(function(){var w=" + words + ",h=new Date().getHours();"
            "document.currentScript.previousElementSibling.textContent=h>=5&&h<12?w[0]:h>=12&&h<18?w[1]:w[2]})();")


def section_head(title, href=None, label=None):
    more = f'<a class="view-all" href="{href}">{esc(label)}</a>' if href else ""
    return f'<div class="block-head"><h2>{esc(title)}</h2>{more}</div>'


def update_card(page, u):
    lang = page.lang
    top = f'<span class="tile tile-icon">{icon(u["icon"])}</span>'
    meta = fmt_month(u["date"], lang)
    if u.get("href"):
        href = page.link(u["href"])
        return card(href, tr(u["title"], lang), tr(u["text"], lang), meta, top, external=href.startswith("http"))
    return card("", tr(u["title"], lang), tr(u["text"], lang), meta, top, tag="div")


def post_cover(page, post, sizes, priority="lazy"):
    return cover(page, post.get("cover"), tr(post["title"], page.lang), sizes, priority)


def affidaty_card(page, a, sizes):
    lang = page.lang
    image = cover(page, "affidaty/" + tr(a["cover"], lang), tr(a["title"], lang), sizes)
    return card(tr(a["url"], lang), tr(a["title"], lang), tr(a["excerpt"], lang), f'{tr(a["date"], lang)} · Affidaty',
                f'<div class="card-cover banner">{image}</div>', external=True)


def render_home(page):
    lang = page.lang
    H = C.HOME
    tips = []
    for t in H["tips"]:
        text = esc(tr(t["text"], lang))
        if t.get("href"):
            href = page.link(t["href"])
            attrs = ' download' if t["href"] == "cv" else ext_attrs(href)
            text += f' — <a href="{href}"{attrs}>{esc(tr(t["link"], lang))}</a>'
        cls = "tip tip-desktop" if t.get("desktop") else "tip"
        tips.append(f'<div class="{cls}"><p>{text}</p></div>')

    projects = [p for p in C.PROJECTS["items"] if p.get("home")]
    project_cards = "".join(
        card(page.link("projects/") + f'#{p["slug"]}', tr(p["name"], lang), tr(p["summary"], lang), p["year"],
             f'<div class="card-cover">{cover(page, p["cover"], tr(p["name"], lang), "grid", "high" if i == 0 else "lazy")}</div>')
        for i, p in enumerate(projects))

    writing = []
    for post in C.WRITING["posts"]:
        writing.append(card(page.link(f'writing/{post["slug"]}/'), tr(post["title"], lang), tr(post["excerpt"], lang),
                            fmt_day(post["date"], lang), f'<div class="card-cover banner">{post_cover(page, post, "grid")}</div>'))
    for a in C.WRITING["affidaty"][: max(0, 4 - len(writing))]:
        writing.append(affidaty_card(page, a, "grid"))

    updates = "".join(update_card(page, u) for u in C.UPDATES[:4])
    tools = {t["key"]: t for t in C.TOOLS["items"]}
    tool_cards = "".join(
        card(tools[k]["url"], tools[k]["name"], tr(tools[k]["use"], lang), "", logo(page, k, tools[k]["name"], "tile"), external=True)
        for k in H["home_tools"])

    return f"""<section class="hero">
<h1 class="greeting">{esc(tr(C.UI["greeting_fallback"], lang))}</h1>
<script>{greeting_script(lang)}</script>
<p class="intro">{esc(tr(H["intro"], lang))}</p>
<p class="intro-more"><a href="{page.link('about/')}">{esc(tr(H["intro_link"], lang))} →</a></p>
</section>
<section class="tips" aria-label="Tips">{"".join(tips)}</section>
<section class="block">{section_head(tr(H["projects"], lang), page.link("projects/"), tr(C.UI["view_all"], lang))}<div class="grid grid-4">{project_cards}</div></section>
<section class="block">{section_head(tr(H["writing"], lang), page.link("writing/"), tr(C.UI["view_all"], lang))}<div class="grid grid-4">{"".join(writing)}</div></section>
<section class="block">{section_head(tr(H["updates"], lang), page.link("about/#updates"), tr(C.UI["view_all"], lang))}<div class="grid grid-4">{updates}</div></section>
<section class="block">{section_head(tr(H["tools"], lang), page.link("tools/"), tr(C.UI["view_all"], lang))}<div class="grid grid-4">{tool_cards}</div></section>"""


def timeline(items, lang):
    rows = "".join(
        f'<div class="t-row"><p class="when">{esc(tr(i["when"], lang))}</p><div>'
        f'<p class="role">{esc(tr(i["role"], lang))} <span class="org">· {esc(tr(i["org"], lang))}</span></p>'
        f'<p class="t-text">{esc(tr(i["text"], lang))}</p></div></div>'
        for i in items)
    return f'<div class="timeline">{rows}</div>'


def render_about(page):
    lang = page.lang
    A = C.ABOUT
    short = "".join(f"<p>{esc(p)}</p>" for p in tr(A["bio_default"], lang))
    long = "".join(f"<p>{esc(p)}</p>" for p in tr(A["bio_long"], lang))

    updates = []
    for u in C.UPDATES[: A["updates_count"]]:
        title = esc(tr(u["title"], lang))
        if u.get("href"):
            href = page.link(u["href"])
            title = f'<a href="{href}"{ext_attrs(href)}>{title}</a>'
        updates.append(f'<li class="update"><span class="tile tile-icon">{icon(u["icon"])}</span>'
                       f'<div><p class="update-title">{title}</p><p class="update-text">{esc(tr(u["text"], lang))}</p></div>'
                       f'<time class="update-date" datetime="{u["date"]}">{fmt_month(u["date"], lang)}</time></li>')

    principles = "".join(
        f'<div class="principle"><h3>{esc(tr(p["title"], lang))}</h3><p>{esc(tr(p["text"], lang))}</p></div>'
        for p in C.PRINCIPLES)

    return f"""<header class="page-head about-head">
{picture(page, "anthony.jpg", "Anthony Gozzini", "72px", "eager", ' class="portrait" width="96" height="96"')}
<h1>{esc(tr(A["title"], lang))}</h1>
</header>
<div class="bio-toggle"><span class="bio-label">{esc(tr(A["bio_label"], lang))}</span>
<div class="seg" role="group" aria-label="{esc(tr(A["bio_label"], lang))}">
<button type="button" class="seg-btn" data-bio="short" aria-pressed="true" aria-controls="bio-short bio-long">{esc(tr(A["bio_short"], lang))}</button>
<button type="button" class="seg-btn" data-bio="long" aria-pressed="false" aria-controls="bio-short bio-long">{esc(tr(A["bio_long_label"], lang))}</button>
</div></div>
<div class="bio" id="bio-short" data-bio-panel="short">{short}</div>
<div class="bio" id="bio-long" data-bio-panel="long" hidden>{long}</div>

<section class="section" id="updates"><h2>{esc(tr(A["updates"], lang))}</h2><ul class="updates">{"".join(updates)}</ul></section>

<section class="section" id="career"><h2>{esc(tr(A["career"], lang))}</h2>
<p class="section-lead">{esc(tr(A["career_intro"], lang))} <a href="{C.SITE['linkedin']}" target="_blank" rel="noopener">{esc(tr(A["career_link"], lang))}</a></p>
{timeline(C.CAREER, lang)}
<h3 class="sub-head">{esc(tr(A["education"], lang))}</h3>
{timeline(C.EDUCATION, lang)}</section>

<section class="section" id="how-i-work"><h2>{esc(tr(A["how"], lang))}</h2><div class="principles">{principles}</div></section>"""


def render_projects(page):
    lang = page.lang
    P = C.PROJECTS
    items = []
    for i, p in enumerate(P["items"]):
        name = tr(p["name"], lang)
        links = []
        for link in p["links"]:
            href = page.raw(link["href"]) if link.get("raw") else page.link(link["href"])
            glyph = icon("right") if link.get("internal") or link.get("raw") else icon("arrow")
            links.append(f'<a href="{href}"{ext_attrs(href)}>{esc(tr(link["label"], lang))}{glyph}</a>')
        links_html = f'<div class="project-links">{"".join(links)}</div>' if links else ""
        items.append(f"""<article class="project" id="{p['slug']}">
<div class="project-cover">{cover(page, p['cover'], name, "project", "high" if i == 0 else "lazy")}</div>
<div class="project-body">
<div class="project-head"><h2>{esc(name)}</h2><span class="project-year">{esc(p['year'])}</span></div>
<p class="project-summary">{esc(tr(p['summary'], lang))}</p>
<p class="project-text">{esc(tr(p['text'], lang))}</p>
<p class="project-tags">{' · '.join(esc(t) for t in tr(p['tags'], lang))}</p>
{links_html}
</div></article>""")
    return f"""<header class="page-head"><h1>{esc(tr(P["title"], lang))}</h1><p class="lead">{esc(tr(P["intro"], lang))}</p></header>
<div class="projects">{"".join(items)}</div>"""


def render_writing(page):
    lang = page.lang
    W = C.WRITING
    mine = []
    for i, p in enumerate(W["posts"]):
        href = page.link(f'writing/{p["slug"]}/')
        meta = f'{fmt_day(p["date"], lang)} · {p["minutes"]} {tr(C.UI["min_read"], lang)}'
        mine.append(f'<a class="card card-feature" href="{href}"><div class="card-cover">{post_cover(page, p, "feature", "high" if i == 0 else "lazy")}</div>'
                    f'<div class="card-feature-body"><p class="card-meta">{esc(meta)}</p>'
                    f'<h3 class="card-title">{esc(tr(p["title"], lang))}</h3><p class="card-text">{esc(tr(p["excerpt"], lang))}</p>'
                    f'<span class="card-cta">{esc(tr(C.UI["read"], lang))}{icon("right")}</span></div></a>')
    affidaty = "".join(affidaty_card(page, a, "grid3") for a in W["affidaty"])
    return f"""<header class="page-head"><h1>{esc(tr(W["title"], lang))}</h1><p class="lead">{esc(tr(W["intro"], lang))}</p></header>
<section class="block block-first"><h2 class="block-title">{esc(tr(W["mine_label"], lang))}</h2><div class="features">{"".join(mine)}</div></section>
<section class="block"><h2 class="block-title">{esc(tr(W["affidaty_label"], lang))}</h2><div class="grid grid-3">{affidaty}</div></section>"""


def render_post(page, post):
    lang = page.lang
    return f"""<nav class="crumbs" aria-label="Breadcrumb"><a href="{page.link('writing/')}">{esc(tr(C.WRITING["title"], lang))}</a><span aria-hidden="true">›</span><span class="crumb-current">{esc(tr(post["title"], lang))}</span></nav>
<header class="post-head">
<span class="pill">{post["minutes"]} {esc(tr(C.UI["min_read"], lang))}</span>
<h1 class="post-title">{esc(tr(post["title"], lang))}</h1>
<p class="post-excerpt">{esc(tr(post["excerpt"], lang))}</p>
<div class="post-meta">{picture(page, "anthony.jpg", "", "40px", "eager", ' width="40" height="40"')}
<div><p class="post-author">{esc(tr(C.UI["by"], lang))} Anthony Gozzini</p>
<p class="post-date">{esc(tr(C.UI["published"], lang))} <time datetime="{post["date"]}">{fmt_day(post["date"], lang)}</time></p></div></div>
</header>
<div class="post-cover">{post_cover(page, post, "post", "high")}</div>
<article class="prose">{tr(post["body"], lang).replace("{play}", page.raw("play/sgamers/"))}</article>"""


def render_tools(page):
    lang = page.lang
    T = C.TOOLS
    tabs = [("all", tr(C.UI["all_categories"], lang))] + [(k, tr(v, lang)) for k, v in T["categories"].items()]
    tab_html = "".join(
        f'<button type="button" role="tab" class="tab" data-filter="{k}" aria-selected="{"true" if k == "all" else "false"}">{esc(v)}</button>'
        for k, v in tabs)
    rows = "".join(
        f'<a class="tool-row" href="{t["url"]}" target="_blank" rel="noopener" data-cat="{t["cat"]}">'
        f'{logo(page, t["key"], t["name"], "tile tile-lg")}'
        f'<div class="tool-main"><p class="tool-name">{esc(t["name"])}<span class="tool-arrow">{icon("arrow")}</span></p>'
        f'<p class="tool-use">{esc(tr(t["use"], lang))}</p></div>'
        f'<span class="tool-cat">{esc(tr(T["categories"][t["cat"]], lang))}</span></a>'
        for t in T["items"])
    return f"""<header class="page-head"><h1>{esc(tr(T["title"], lang))}</h1><p class="lead">{esc(tr(T["intro"], lang))}</p></header>
<div class="tabs" role="tablist" aria-label="{esc(tr(T["title"], lang))}">{tab_html}</div>
<div class="tool-list">{rows}</div>"""


def render_contact(page):
    lang = page.lang
    K = C.CONTACT
    S = C.SITE
    channels = [
        ("mail", "Email", S["email"], "mailto:" + S["email"], True),
        ("whatsapp", "WhatsApp", "@" + S["whatsapp"].rsplit("/", 1)[-1], S["whatsapp"], False),
        ("send", "Telegram", "@" + S["telegram"].rsplit("/", 1)[-1], S["telegram"], False),
        ("linkedin", "LinkedIn", "in/" + S["linkedin"].rstrip("/").rsplit("/", 1)[-1], S["linkedin"], False),
        ("github", "GitHub", S["github"].rsplit("/", 1)[-1], S["github"], False),
        ("download", tr(K["cv"], lang), tr(K["cv_text"], lang), page.link("cv"), False),
    ]
    rows = []
    for ic, label, value, href, copy in channels:
        attrs = " download" if href.endswith(".pdf") else ext_attrs(href)
        corner = "" if copy else f'<span class="channel-arrow">{icon("download" if attrs == " download" else "arrow")}</span>'
        # The copy button sits beside the link, not inside it: a button inside <a> is invalid HTML.
        button = (f'<button type="button" class="copy-btn" data-copy="{esc(value)}" data-copied="{esc(tr(C.UI["copied"], lang))}">{icon("copy")}<span>{esc(tr(C.UI["copy"], lang))}</span></button>'
                  if copy else "")
        rows.append(f'<div class="channel-card"><a class="channel-hit" href="{href}"{attrs}>'
                    f'<span class="channel-top"><span class="tile tile-icon">{icon(ic)}</span>{corner}</span>'
                    f'<span class="channel-label">{esc(label)}</span><span class="channel-value">{esc(value).replace("@", "@<wbr>") if copy else esc(value)}</span></a>{button}</div>')
    offers = "".join(
        f'<div class="offer"><h3>{esc(tr(o["title"], lang))}</h3><p>{esc(tr(o["text"], lang))}</p>'
        f'<p class="offer-proof">{icon("check")}<span>{esc(tr(o["proof"], lang))}</span></p></div>'
        for o in K["offers"])
    return f"""<header class="page-head"><h1>{esc(tr(K["title"], lang))}</h1><p class="lead">{esc(tr(K["intro"], lang))}</p></header>
<div class="cta">
<a class="btn btn-primary" href="{S['cal']}" target="_blank" rel="noopener">{icon("calendar")}<span>{esc(tr(K["cta_call"], lang))}</span></a>
<a class="btn" href="mailto:{S['email']}">{icon("mail")}<span>{esc(tr(K["cta_email"], lang))}</span></a>
</div>
<section class="section"><h2>{esc(tr(K["channels"], lang))}</h2><div class="channels">{"".join(rows)}</div></section>
<section class="section"><h2>{esc(tr(K["help"], lang))}</h2><div class="offers">{offers}</div></section>"""


def render_404(page):
    N = C.NOT_FOUND
    buttons = "".join(
        f'<a class="btn{" btn-primary" if code == page.lang else ""}" href="{page.link("", code)}" hreflang="{code}" lang="{code}">{icon("home")}<span>{esc(tr(N["home"], code))}</span></a>'
        for code in LANGS)
    notes = "".join(f'<p class="lead" lang="{code}">{esc(tr(N["text"], code))}</p>' for code in LANGS)
    return f"""<header class="page-head"><h1>{esc(tr(N["title"], page.lang))}</h1>{notes}</header>
<div class="cta">{buttons}</div>"""


PLAY_STYLE = (".ag-back{position:fixed;top:14px;left:16px;z-index:10;font:500 14px/1 system-ui,sans-serif;color:#fff;background:rgba(18,20,23,.72);padding:9px 13px;border-radius:9px;text-decoration:none}"
              ".ag-back:hover{background:#121417}"
              "#unity-container.unity-desktop{position:relative;left:auto;top:auto;transform:none;width:960px;margin:64px auto 0}"
              "#unity-container.unity-mobile{position:relative;width:100%;height:auto;aspect-ratio:16/10}#unity-footer{height:38px}"
              ".ag-play{position:absolute;left:0;top:0;z-index:2;width:100%;aspect-ratio:16/10;padding:0;border:0;background:#231F20;cursor:pointer}"
              ".ag-play img{width:100%;height:100%;display:block;object-fit:cover}"
              ".ag-play span{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);padding:14px 22px;border-radius:12px;background:#121417;color:#fff;font:600 18px/1 system-ui,sans-serif;white-space:nowrap}"
              ".ag-play:hover span,.ag-play:focus-visible span{background:#08629A}"
              ".ag-about{max-width:960px;margin:28px auto 56px;padding:0 16px;box-sizing:border-box;font:16px/1.65 system-ui,sans-serif;color:#2B3038}"
              ".ag-about h1{margin:0 0 6px;font-size:28px;line-height:1.2;font-weight:600;color:#121417}"
              ".ag-about p{margin:0 0 14px}.ag-lead{font-size:18px;color:#121417}.ag-about a{color:#121417}")


def play_blocks(page):
    """The parts of play/sgamers/index.html that the build owns; the Unity loader around them is left as exported."""
    P = C.PLAY
    project = next(p for p in C.PROJECTS["items"] if p["slug"] == P["project"])
    base = C.SITE["url"] + "/"
    url = base + page.full
    name = tr(project["name"], "en")
    others = [l for l in project["links"] if not l.get("raw")]
    links = " · ".join(f'<a href="{page.link(l["href"])}"{ext_attrs(l["href"])}>{esc(tr(l["label"], "en"))}</a>' for l in others)
    about = (f'<main class="ag-about"><h1>{esc(name)}</h1><p class="ag-lead">{esc(tr(project["summary"], "en"))}</p>'
             f'<p>{esc(tr(project["text"], "en"))}</p><p class="ag-links">{links}</p></main>')
    article = next((l["href"] for l in others if l.get("internal")), None)
    game = {"@type": "Game", "@id": url + "#game", "additionalType": "https://www.wikidata.org/wiki/Q7889", "name": name, "url": url,
            "description": tr(project["summary"], "en"), "image": base + "assets/img/" + project["cover"], "inLanguage": "en",
            "dateCreated": P["created"], "datePublished": P["published"],
            "author": {"@type": "Person", "@id": base + "#person", "name": C.SITE["name"], "url": base}}
    if article:
        game["subjectOf"] = {"@id": base + article + "#article"}
    meta = {"both_langs": False, "image": project["cover"], "image_alt": name,
            "jsonld": graph(page, P["title"], P["description"], "WebPage", [game], main=game["@id"])}
    top = f'<a class="ag-back" href="{page.link("projects/#" + project["slug"])}">← Anthony Gozzini</a><style>{PLAY_STYLE}</style>'
    facade = (f'<button type="button" id="ag-play" class="ag-play">{picture(page, project["cover"], "", SIZES["play"], "high")}'
              f'<span>▶ {esc(P["play_label"])}</span></button>')
    # Unity's template stylesheet goes inline like site.css, so nothing blocks the first paint.
    unity_css = (ROOT / page.full / "TemplateData" / "style.css").read_text(encoding="utf-8")
    unity_css = re.sub(r"url\('([^']+)'\)", r"url('TemplateData/\1')", unity_css)
    head = "\n" + head_tags(page, P["title"], P["description"], meta) + f"<style>{unity_css}</style>\n"
    return {"head": head, "top": top, "facade": facade, "about": about}


def fill_play(page, blocks):
    path = ROOT / page.full / "index.html"
    text = path.read_text(encoding="utf-8")
    for name, block in blocks.items():
        pattern = re.compile(rf"<!-- ag:{name} -->.*?<!-- /ag:{name} -->", re.S)
        if not pattern.search(text):
            warnings.append(f"{page.full}index.html: manca il segnaposto <!-- ag:{name} -->")
            return None
        text = pattern.sub(lambda m: f"<!-- ag:{name} -->{block}<!-- /ag:{name} -->", text, count=1)
    text = re.sub(r'<html lang="[^"]*">', '<html lang="en">', text, count=1)
    path.write_text(text, encoding="utf-8")
    return path


def site_url(path="", lang="en", md=False):
    return C.SITE["url"] + "/" + ("it/" if lang == "it" else "") + path + ("index.md" if md else "")


def md_href(href, lang):
    """Where a content link points in the markdown copies: other pages' markdown, files and outside URLs as they are."""
    if href.startswith(("http://", "https://")):
        return href
    if href == "cal":
        return C.SITE["cal"]
    if href == "cv":
        return site_url(C.SITE["cv"])
    return site_url(href.partition("#")[0], lang, md=True)


def plain(label):
    return label.rstrip(" →↗↓")


def md_join(parts):
    return "\n\n".join(p for p in parts if p) + "\n"


def md_list(lines):
    return "\n".join(lines)


def md_update(u, lang):
    title = tr(u["title"], lang)
    if u.get("href"):
        title = f'[{title}]({md_href(u["href"], lang)})'
    return f'- {fmt_month(u["date"], lang)}: {title}. {tr(u["text"], lang)}'


def md_post_line(post, lang):
    return f'- [{tr(post["title"], lang)}]({site_url("writing/" + post["slug"] + "/", lang, True)}) ({fmt_day(post["date"], lang)}): {tr(post["excerpt"], lang)}'


def md_affidaty_line(a, lang):
    return f'- [{tr(a["title"], lang)}]({tr(a["url"], lang)}) ({tr(a["date"], lang)}, Affidaty): {tr(a["excerpt"], lang)}'


SECTIONS = {"about": C.ABOUT, "projects": C.PROJECTS, "writing": C.WRITING, "tools": C.TOOLS, "contact": C.CONTACT}


def md_home(lang):
    H = C.HOME
    tools = {t["key"]: t for t in C.TOOLS["items"]}
    affidaty = C.WRITING["affidaty"][: max(0, 4 - len(C.WRITING["posts"]))]
    return md_join([
        f'# {tr(H["title"], lang)}', f'> {tr(C.SITE["description"], lang)}', tr(H["intro"], lang),
        md_list(f'- {tr(t["text"], lang)}: [{plain(tr(t["link"], lang))}]({md_href(t["href"], lang)})' for t in H["tips"] if t.get("href")),
        f'## {tr(H["projects"], lang)}',
        md_list(f'- [{tr(p["name"], lang)}]({site_url("projects/", lang, True)}) ({p["year"]}): {tr(p["summary"], lang)}' for p in C.PROJECTS["items"]),
        f'## {tr(H["writing"], lang)}',
        md_list([md_post_line(p, lang) for p in C.WRITING["posts"]] + [md_affidaty_line(a, lang) for a in affidaty]),
        f'## {tr(H["updates"], lang)}', md_list(md_update(u, lang) for u in C.UPDATES[:4]),
        f'## {tr(H["tools"], lang)}', md_list(f'- [{tools[k]["name"]}]({tools[k]["url"]}): {tr(tools[k]["use"], lang)}' for k in H["home_tools"]),
        f'## {tr(C.MD["pages"], lang)}',
        md_list(f'- [{tr(n["label"], lang)}]({site_url(n["path"], lang, True)}): {tr(SECTIONS[n["key"]]["description"], lang)}' for n in C.NAV if n["key"] in SECTIONS),
    ])


def md_timeline(items, lang):
    return md_list(f'- {tr(i["when"], lang)}: {tr(i["role"], lang)}, {tr(i["org"], lang)}. {tr(i["text"], lang)}' for i in items)


def md_about(lang):
    A = C.ABOUT
    principles = [f'### {tr(p["title"], lang)}\n\n{tr(p["text"], lang)}' for p in C.PRINCIPLES]
    return md_join([
        f'# {tr(A["title"], lang)} — Anthony Gozzini', f'> {tr(A["description"], lang)}',
        f'## {tr(C.MD["short_bio"], lang)}', *tr(A["bio_default"], lang),
        f'## {tr(C.MD["long_bio"], lang)}', *tr(A["bio_long"], lang),
        f'## {tr(A["updates"], lang)}', md_list(md_update(u, lang) for u in C.UPDATES[: A["updates_count"]]),
        f'## {tr(A["career"], lang)}', f'{tr(A["career_intro"], lang)} [{plain(tr(A["career_link"], lang))}]({C.SITE["linkedin"]})',
        md_timeline(C.CAREER, lang),
        f'### {tr(A["education"], lang)}', md_timeline(C.EDUCATION, lang),
        f'## {tr(A["how"], lang)}', *principles,
    ])


def md_project_link(link, lang):
    if link.get("raw"):
        return f'[{tr(link["label"], lang)}]({site_url(link["href"], md=True)})'
    return f'[{tr(link["label"], lang)}]({md_href(link["href"], lang)})'


def md_projects(lang):
    P = C.PROJECTS
    parts = [f'# {tr(P["title"], lang)} — Anthony Gozzini', f'> {tr(P["description"], lang)}', tr(P["intro"], lang)]
    for p in P["items"]:
        parts += [f'## {tr(p["name"], lang)} ({p["year"]})', tr(p["summary"], lang), tr(p["text"], lang),
                  f'{tr(C.MD["tags"], lang)}: {", ".join(tr(p["tags"], lang))}']
        if p["links"]:
            parts.append(f'{tr(C.MD["links"], lang)}: ' + ", ".join(md_project_link(l, lang) for l in p["links"]))
    return md_join(parts)


def md_writing(lang):
    W = C.WRITING
    return md_join([
        f'# {tr(W["title"], lang)} — Anthony Gozzini', f'> {tr(W["description"], lang)}', tr(W["intro"], lang),
        f'## {tr(W["mine_label"], lang)}', md_list(md_post_line(p, lang) for p in W["posts"]),
        f'## {tr(W["affidaty_label"], lang)}', md_list(md_affidaty_line(a, lang) for a in W["affidaty"]),
    ])


def md_tools(lang):
    T = C.TOOLS
    parts = [f'# {tr(T["title"], lang)} — Anthony Gozzini', f'> {tr(T["description"], lang)}', tr(T["intro"], lang)]
    for key, label in T["categories"].items():
        parts += [f"## {tr(label, lang)}", md_list(f'- [{t["name"]}]({t["url"]}): {tr(t["use"], lang)}' for t in T["items"] if t["cat"] == key)]
    return md_join(parts)


def md_contact(lang):
    K = C.CONTACT
    S = C.SITE
    offers = [f'### {tr(o["title"], lang)}\n\n{tr(o["text"], lang)}\n\n{tr(C.MD["proof"], lang)}: {tr(o["proof"], lang)}' for o in K["offers"]]
    return md_join([
        f'# {tr(K["title"], lang)} — Anthony Gozzini', f'> {tr(K["description"], lang)}', tr(K["intro"], lang),
        md_list([f'- [{tr(K["cta_call"], lang)}]({S["cal"]})', f'- Email: {S["email"]}',
                 f'- [WhatsApp]({S["whatsapp"]})', f'- [Telegram]({S["telegram"]})',
                 f'- [LinkedIn]({S["linkedin"]})', f'- [GitHub]({S["github"]})',
                 f'- [{tr(K["cv"], lang)}]({site_url(S["cv"])}): {tr(K["cv_text"], lang)}']),
        f'## {tr(K["help"], lang)}', *offers,
    ])


def prose_md(text):
    text = text.replace("{play}", site_url(C.PLAY["path"]))
    text = re.sub(r'<a href="([^"]*)">(.*?)</a>', r"[\2](\1)", text)
    text = re.sub(r"<h2>(.*?)</h2>", r"## \1", text)
    text = re.sub(r"</?p>", "", text)
    if re.search(r"</?[a-z][^>]*>", text):
        warnings.append("markdown: tag HTML rimasto nel testo di un articolo")
    return "\n\n".join(line.strip() for line in html.unescape(text).splitlines() if line.strip())


def md_post(lang, post):
    meta = (f'{tr(C.UI["by"], lang)} Anthony Gozzini · {tr(C.UI["published"], lang)} {fmt_day(post["date"], lang)}'
            f' · {post["minutes"]} {tr(C.UI["min_read"], lang)}')
    return md_join([f'# {tr(post["title"], lang)}', meta, f'> {tr(post["excerpt"], lang)}', prose_md(tr(post["body"], lang))])


def md_play():
    P = C.PLAY
    project = next(p for p in C.PROJECTS["items"] if p["slug"] == P["project"])
    links = [f'- [{tr(C.MD["html"], "en")}: play in your browser]({site_url(P["path"])})']
    links += [f'- {md_project_link(l, "en")}' for l in project["links"] if not l.get("raw")]
    return md_join([f'# {P["title"].rsplit(" — ", 1)[0]}', f'> {P["description"]}',
                    tr(project["summary"], "en"), tr(project["text"], "en"), md_list(links)])


def llms_txt():
    en = "en"
    S = C.SITE
    projects = []
    for p in C.PROJECTS["items"]:
        code = next((l["href"] for l in p["links"] if l["href"].startswith("https://github.com/")), None)
        projects.append(f'- [{tr(p["name"], en)}]({code or site_url("projects/", en, True)}): {tr(p["summary"], en)}')
    projects.append(f'- [{C.PLAY["title"].rsplit(" — ", 1)[0]}]({site_url(C.PLAY["path"], md=True)}): {C.PLAY["description"]}')
    italian = [f'- [Home]({site_url("", "it", True)}): {tr(S["description"], "it")}']
    italian += [f'- [{tr(n["label"], "it")}]({site_url(n["path"], "it", True)}): {tr(SECTIONS[n["key"]]["description"], "it")}' for n in C.NAV if n["key"] in SECTIONS]
    italian += [md_post_line(p, "it") for p in C.WRITING["posts"]]
    return md_join([
        f'# {S["name"]}', f'> {tr(S["description"], en)}',
        *tr(C.ABOUT["bio_default"], en),
        f'{tr(C.CONTACT["intro"], en)} Email: {S["email"]}. Book a call: {S["cal"]}',
        "The site is in English at the root and in Italian under /it/. Every page has a markdown copy: add index.md to its URL.",
        f'## {tr(C.MD["pages"], en)}',
        md_list([f'- [Home]({site_url(md=True)}): {tr(S["description"], en)}']
                + [f'- [{tr(n["label"], en)}]({site_url(n["path"], en, True)}): {tr(SECTIONS[n["key"]]["description"], en)}' for n in C.NAV if n["key"] in SECTIONS]),
        f'## {tr(C.MD["articles"], en)}', md_list(md_post_line(p, en) for p in C.WRITING["posts"]),
        f'## {tr(C.PROJECTS["title"], en)}', md_list(projects),
        f'## {C.MD["optional"]}',
        md_list([f'- [CV]({site_url(S["cv"])}): {tr(C.CONTACT["cv_text"], en)}',
                 f'- [LinkedIn]({S["linkedin"]}): full career history',
                 f'- [GitHub]({S["github"]}): code and releases']
                + [line.replace("- [", f'- [{C.MD["italian"]}: ', 1) for line in italian]
                + [md_affidaty_line(a, en) for a in C.WRITING["affidaty"]]),
    ])


def write(page, key, title, description, body, width, meta, out=None):
    out = out or ROOT / page.full / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(document(page, key, title, description, body, width, meta), encoding="utf-8")
    return out


def main():
    written = []
    pages = [
        ("about", "about/", render_about, C.ABOUT, "ProfilePage"),
        ("projects", "projects/", render_projects, C.PROJECTS, "CollectionPage"),
        ("writing", "writing/", render_writing, C.WRITING, "CollectionPage"),
        ("tools", "tools/", render_tools, C.TOOLS, "WebPage"),
        ("contact", "contact/", render_contact, C.CONTACT, "ContactPage"),
    ]
    markdown_pages = {"about": md_about, "projects": md_projects, "writing": md_writing, "tools": md_tools, "contact": md_contact}
    urls = []
    markdown = []

    def add_markdown(page, text):
        out = ROOT / page.full / "index.md"
        out.write_text(text, encoding="utf-8")
        markdown.append(out)

    def emit(page, key, title, description, body, width, page_type, md, meta=None, extra=lambda date: ()):
        date = modified(page, body)
        meta = dict(meta or {}, jsonld=graph(page, title, description, page_type, extra(date)))
        written.append(write(page, key, title, description, body, width, meta))
        add_markdown(page, md)
        urls.append((page.full, date))

    for lang in LANGS:
        page = Page(lang, "")
        emit(page, "home", tr(C.HOME["title"], lang), tr(C.SITE["description"], lang), render_home(page), "wide", "WebPage", md_home(lang))
        for key, path, render, section, page_type in pages:
            page = Page(lang, path)
            width = "wide" if key == "writing" else "narrow"
            emit(page, key, f'{tr(section["title"], lang)} — Anthony Gozzini', tr(section["description"], lang), render(page), width, page_type,
                 markdown_pages[key](lang))
        for post in C.WRITING["posts"]:
            page = Page(lang, f'writing/{post["slug"]}/')
            description = tr(post["description"], lang)
            meta = {"type": "article", "published": post["date"], "image": post["cover"], "image_alt": tr(post["title"], lang)}
            emit(page, "writing", f'{tr(post["title"], lang)} — Anthony Gozzini', description, render_post(page, post), "post", "WebPage",
                 md_post(lang, post), meta, lambda date, page=page, post=post, description=description: post_graph(page, post, description, date))

    page = Page("en", C.PLAY["path"])
    blocks = play_blocks(page)
    # The game itself is part of the page's content, so a new build also moves its date.
    builds = "".join(hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted((ROOT / page.full / "Build").iterdir()))
    date = modified(page, blocks["facade"] + blocks["about"] + builds)
    filled = fill_play(page, blocks)
    if filled:
        written.append(filled)
    add_markdown(page, md_play())
    urls.append((page.full, date))

    # GitHub Pages serves this file for any missing path at any depth, so its links must be root-absolute.
    page = Page("en", "")
    page.prefix = "/"
    written.append(write(page, "", f'{tr(C.NOT_FOUND["title"], "en")} — Anthony Gozzini', tr(C.SITE["description"], "en"),
                         render_404(page), "narrow", {"noindex": True}, ROOT / "404.html"))

    sitemap = "".join(f"<url><loc>{C.SITE['url']}/{u}</loc><lastmod>{d}</lastmod></url>" for u, d in urls)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sitemap}</urlset>\n', encoding="utf-8")
    # Search engines index the HTML pages; the markdown copies are for AI agents, so keep them out of search results.
    (ROOT / "robots.txt").write_text("User-agent: Googlebot\nUser-agent: Bingbot\nDisallow: /*.md$\n\n"
                                     f"User-agent: *\nAllow: /\n\nSitemap: {C.SITE['url']}/sitemap.xml\n", encoding="utf-8")
    (ROOT / "llms.txt").write_text(llms_txt(), encoding="utf-8")
    if not PREVIEW:
        kept = {u: stamps[u] for u, _ in urls}
        STAMPS_FILE.write_text(json.dumps(kept, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    expected = len(LANGS) * (1 + len(pages) + len(C.WRITING["posts"])) + 2
    print(f"pagine scritte: {len(written)} (attese {expected}){' · modalità anteprima' if PREVIEW else ''}")
    print(f"copie markdown scritte: {len(markdown)} (attese {len(urls)})")
    for w in sorted(set(warnings)):
        print("attenzione:", w)
    return 0 if len(written) == expected and len(markdown) == len(urls) else 1


if __name__ == "__main__":
    sys.exit(main())
