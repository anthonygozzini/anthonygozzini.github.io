#!/usr/bin/env python3
"""Generate the static site from content.py: English at the repository root, Italian under it/.

Usage: python3 _src/build.py [--preview]
  --preview  write links as .../index.html, so pages also work when opened straight from disk.
"""
import hashlib
import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import content as C  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PREVIEW = "--preview" in sys.argv
LANGS = ("en", "it")
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


def cover(page, file, alt=""):
    if file and (ROOT / "assets" / "img" / file).exists():
        return f'<img src="{page.asset("img/" + file)}" alt="{esc(alt)}" loading="lazy">'
    warnings.append(f"copertina mancante: assets/img/{file}")
    return ""


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
    return (f'<header class="mtop"><a class="brand" href="{page.link("")}"><span class="brand-mark" aria-hidden="true">AG</span><span class="brand-name">Anthony Gozzini</span></a>'
            f'<div class="mtop-actions">{lang_switch(page)}<button type="button" class="icon-btn" data-theme-cycle aria-label="{label}">'
            f'{icon("sun", "i i-light")}{icon("moon", "i i-dark")}{icon("monitor", "i i-auto")}</button></div></header>')


def tabbar(page, key):
    items = []
    for n in C.NAV:
        current = ' aria-current="page"' if n["key"] == key else ""
        items.append(f'<a class="tab-item" href="{page.link(n["path"])}"{current}>{icon(n["icon"])}<span>{esc(tr(n["label"], page.lang))}</span></a>')
    return f'<nav class="tabbar" aria-label="{esc(tr(C.UI["pages"], page.lang))}">{"".join(items)}</nav>'


def document(page, key, title, description, body, width):
    lang = page.lang
    base = C.SITE["url"] + "/"
    hreflangs = "".join(
        f'<link rel="alternate" hreflang="{code}" href="{base}{("it/" if code == "it" else "") + page.path}">' for code in LANGS)
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{base}{page.full}">
{hreflangs}<link rel="alternate" hreflang="x-default" href="{base}{page.path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:image" content="{base}assets/img/og.jpg">
<meta name="theme-color" content="#E9EDF2">
<link rel="icon" href="{page.asset('favicon.svg')}" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600&family=Geist+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="{page.asset('site.css')}">
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


def post_cover(page, post):
    return cover(page, post.get("cover"), tr(post["title"], page.lang))


def affidaty_card(page, a):
    lang = page.lang
    image = cover(page, "affidaty/" + tr(a["cover"], lang), tr(a["title"], lang))
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
             f'<div class="card-cover">{cover(page, p["cover"], tr(p["name"], lang))}</div>')
        for p in projects)

    writing = []
    for post in C.WRITING["posts"]:
        writing.append(card(page.link(f'writing/{post["slug"]}/'), tr(post["title"], lang), tr(post["excerpt"], lang),
                            fmt_day(post["date"], lang), f'<div class="card-cover banner">{post_cover(page, post)}</div>'))
    for a in C.WRITING["affidaty"][: max(0, 4 - len(writing))]:
        writing.append(affidaty_card(page, a))

    updates = "".join(update_card(page, u) for u in C.UPDATES[:4])
    tools = {t["key"]: t for t in C.TOOLS["items"]}
    tool_cards = "".join(
        card(tools[k]["url"], tools[k]["name"], tr(tools[k]["use"], lang), "", logo(page, k, tools[k]["name"], "tile"), external=True)
        for k in H["home_tools"])

    return f"""<section class="hero">
<h1 class="greeting" data-greeting>{esc(tr(C.UI["greeting_fallback"], lang))}</h1>
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
<img class="portrait" src="{page.asset('img/anthony.jpg')}" alt="Anthony Gozzini" width="96" height="96">
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
    for p in P["items"]:
        name = tr(p["name"], lang)
        links = []
        for link in p["links"]:
            href = page.raw(link["href"]) if link.get("raw") else page.link(link["href"])
            glyph = icon("right") if link.get("internal") or link.get("raw") else icon("arrow")
            links.append(f'<a href="{href}"{ext_attrs(href)}>{esc(tr(link["label"], lang))}{glyph}</a>')
        links_html = f'<div class="project-links">{"".join(links)}</div>' if links else ""
        items.append(f"""<article class="project" id="{p['slug']}">
<div class="project-cover">{cover(page, p['cover'], name)}</div>
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
    for p in W["posts"]:
        href = page.link(f'writing/{p["slug"]}/')
        meta = f'{fmt_day(p["date"], lang)} · {p["minutes"]} {tr(C.UI["min_read"], lang)}'
        mine.append(f'<a class="card card-feature" href="{href}"><div class="card-cover">{post_cover(page, p)}</div>'
                    f'<div class="card-feature-body"><p class="card-meta">{esc(meta)}</p>'
                    f'<h3 class="card-title">{esc(tr(p["title"], lang))}</h3><p class="card-text">{esc(tr(p["excerpt"], lang))}</p>'
                    f'<span class="card-cta">{esc(tr(C.UI["read"], lang))}{icon("right")}</span></div></a>')
    affidaty = "".join(affidaty_card(page, a) for a in W["affidaty"])
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
<div class="post-meta"><img src="{page.asset('img/anthony.jpg')}" alt="" width="40" height="40">
<div><p class="post-author">{esc(tr(C.UI["by"], lang))} Anthony Gozzini</p>
<p class="post-date">{esc(tr(C.UI["published"], lang))} <time datetime="{post["date"]}">{fmt_day(post["date"], lang)}</time></p></div></div>
</header>
<div class="post-cover">{post_cover(page, post)}</div>
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


def write(page, key, title, description, body, width):
    out = ROOT / page.full / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(document(page, key, title, description, body, width), encoding="utf-8")
    return out


def main():
    written = []
    pages = [
        ("about", "about/", render_about, C.ABOUT["title"]),
        ("projects", "projects/", render_projects, C.PROJECTS["title"]),
        ("writing", "writing/", render_writing, C.WRITING["title"]),
        ("tools", "tools/", render_tools, C.TOOLS["title"]),
        ("contact", "contact/", render_contact, C.CONTACT["title"]),
    ]
    urls = []
    for lang in LANGS:
        page = Page(lang, "")
        written.append(write(page, "home", tr(C.HOME["title"], lang), tr(C.SITE["description"], lang), render_home(page), "wide"))
        urls.append(page.full)
        for key, path, render, title in pages:
            page = Page(lang, path)
            width = "wide" if key == "writing" else "narrow"
            written.append(write(page, key, f"{tr(title, lang)} — Anthony Gozzini", tr(C.SITE["description"], lang), render(page), width))
            urls.append(page.full)
        for post in C.WRITING["posts"]:
            page = Page(lang, f'writing/{post["slug"]}/')
            written.append(write(page, "writing", f'{tr(post["title"], lang)} — Anthony Gozzini', tr(post["excerpt"], lang), render_post(page, post), "post"))
            urls.append(page.full)
    sitemap = "".join(f"<url><loc>{C.SITE['url']}/{u}</loc></url>" for u in urls)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sitemap}</urlset>\n', encoding="utf-8")
    expected = len(LANGS) * (1 + len(pages) + len(C.WRITING["posts"]))
    print(f"pagine scritte: {len(written)} (attese {expected}){' · modalità anteprima' if PREVIEW else ''}")
    for w in sorted(set(warnings)):
        print("attenzione:", w)
    return 0 if len(written) == expected else 1


if __name__ == "__main__":
    sys.exit(main())
