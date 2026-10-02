#!/usr/bin/env python3
"""Build one-shot.wiki static HTML from _build/pages/*.html (no dependencies)."""
import html, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from registry import DOMAIN, GAME_URL, CSS, PAGES, NOT_FOUND  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRAG = os.path.join(ROOT, "_build", "pages")

def esc(s):
    return html.escape(s, quote=True)

NAV = [("/how-to-play/", "How to Play"), ("/movement-aim/", "Movement &amp; Aim"), ("/progression/", "Progression"),
       ("/codes/", "Codes"), ("/trello/", "Trello &amp; Discord")]

def header():
    desk = "".join(f'<a href="{h}">{t}</a>' for h, t in NAV)
    mob = '<a href="/">Home</a>' + desk + '<a href="/sources/">Sources</a>'
    return ('<div class="site-shell"><div class="independence-notice" role="note"><span>UNOFFICIAL FAN WIKI</span>Not affiliated with or endorsed by Roblox or the One Shot creators.</div>'
            '<header class="site-header"><a class="brand" aria-label="One Shot Wiki home" href="/"><span class="brand-icon" aria-hidden="true"><img alt="" width="38" height="38" decoding="async" src="/media/one-shot-icon.png"/></span><span class="brand-copy"><strong>ONE SHOT</strong><small>Field Wiki</small></span></a>'
            f'<nav class="desktop-nav" aria-label="Primary navigation">{desk}</nav>'
            f'<a class="header-play" href="{GAME_URL}" target="_blank" rel="noreferrer">Play now <span aria-hidden="true">↗</span></a>'
            f'<details class="mobile-menu"><summary aria-label="Open navigation"><span></span><span></span></summary><nav aria-label="Mobile navigation">{mob}<a href="{GAME_URL}" target="_blank" rel="noreferrer">Play on Roblox ↗</a></nav></details></header>')

FOOTER = ('<footer class="site-footer"><div class="footer-brand"><span class="logo-mark" aria-hidden="true">＋</span><div><strong>ONE SHOT WIKI</strong><p>Independent, source-led field notes.</p></div></div>'
          '<div class="footer-links"><div><strong>GUIDES</strong><a href="/how-to-play/">How to Play</a><a href="/movement-aim/">Movement &amp; Aim</a><a href="/progression/">Progression</a><a href="/codes/">Codes</a><a href="/trello/">Trello &amp; Discord</a></div>'
          '<div><strong>ABOUT</strong><a href="/sources/">Sources</a><a href="/disclosure/">Disclosure</a><a href="/contact/">Contact</a></div>'
          '<div><strong>LEGAL</strong><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a></div></div>'
          f'<div class="footer-bottom"><p>© 2026 One Shot Wiki. Fan-made and not affiliated with Roblox or Shooter Game Group.</p><a href="{GAME_URL}" target="_blank" rel="noreferrer">Official game page ↗</a></div></footer></div>')

ADS = ('\n  <!-- adsterra-code-handoff:artifact-runtime:start -->\n'
       '  <script type="module" src="/adsterra/runtime.js" data-adsterra-artifact-runtime data-global-fallback="true"></script>\n'
       '  <!-- adsterra-code-handoff:artifact-runtime:end -->\n')

WEBSITE_LD = {"@context": "https://schema.org", "@type": "WebSite", "name": "One Shot Wiki", "alternateName": "One Shot Fan Wiki",
              "url": DOMAIN, "description": "An independent fan-made guide to the Roblox experience One Shot.", "inLanguage": "en", "isAccessibleForFree": True}
GAME_LD = {"@context": "https://schema.org", "@type": "VideoGame", "name": "One Shot", "url": GAME_URL, "sameAs": GAME_URL,
           "description": "A fast-paced free-for-all Roblox deathmatch where every weapon carries one bullet at a time.",
           "gamePlatform": ["PC", "Mobile", "Xbox", "PlayStation"],
           "author": {"@type": "Organization", "name": "Shooter Game Group", "url": "https://www.roblox.com/communities/186538912/Shooter-Game-Group"}}

def strip_tags(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()

def faq_items(main):
    out = []
    for m in re.finditer(r'<article class="faq-item"><h3>(.*?)</h3>(.*?)</article>', main, re.S):
        out.append({"@type": "Question", "name": strip_tags(m.group(1)),
                    "acceptedAnswer": {"@type": "Answer", "text": strip_tags(m.group(2))}})
    return out

def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>"

def head(title, desc, canonical, robots="index, follow", og_type="website"):
    t, d = esc(title), esc(desc)
    css = "".join(f'<link rel="stylesheet" href="{c}"/>' for c in CSS)
    canon = f'<link rel="canonical" href="{canonical}"/>' if canonical else ""
    og_url = f'<meta property="og:url" content="{canonical}"/>' if canonical else ""
    return ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>'
            f'{css}<meta name="theme-color" content="#0a0d0f"/><meta name="color-scheme" content="dark"/><title>{t}</title><meta name="description" content="{d}"/>'
            '<meta name="application-name" content="One Shot Wiki"/><meta name="author" content="One Shot Wiki Editors"/><meta name="referrer" content="origin-when-cross-origin"/>'
            f'<meta name="robots" content="{robots}"/><meta name="googlebot" content="{robots}, max-video-preview:-1, max-image-preview:large, max-snippet:-1"/>'
            f'{canon}<meta property="og:site_name" content="One Shot Wiki"/><meta property="og:type" content="{og_type}"/><meta property="og:title" content="{t}"/><meta property="og:description" content="{d}"/>{og_url}'
            '<meta property="og:image" content="https://one-shot.wiki/og.png"/><meta property="og:image:width" content="1200"/><meta property="og:image:height" content="630"/><meta property="og:image:alt" content="One Shot Wiki — unofficial fan guide"/>'
            f'<meta name="twitter:card" content="summary_large_image"/><meta name="twitter:title" content="{t}"/><meta name="twitter:description" content="{d}"/><meta name="twitter:image" content="https://one-shot.wiki/og.png"/>'
            '<link rel="icon" href="/media/one-shot-icon.png"/><link rel="apple-touch-icon" href="/media/one-shot-icon.png"/></head>')

def render(page):
    main = open(os.path.join(FRAG, page["key"] + ".html"), encoding="utf-8").read().strip()
    url = DOMAIN + page["route"]
    h1 = strip_tags(re.search(r"<h1[^>]*>(.*?)</h1>", main, re.S).group(1))
    graph = []
    if page["crumb"]:
        graph.append({"@type": "Article", "headline": h1, "description": page["description"], "url": url,
                      "dateModified": page["lastmod"], "inLanguage": "en",
                      "author": {"@type": "Organization", "name": "One Shot Wiki Editors"},
                      "publisher": {"@type": "Organization", "name": "One Shot Wiki Editors"}})
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": page["crumb"], "item": url}]})
    if page.get("faq"):
        q = faq_items(main)
        if q:
            graph.append({"@type": "FAQPage", "mainEntity": q})
    page_ld = ld({"@context": "https://schema.org", "@graph": graph}) if graph else ""
    body = ('<body><a class="skip-link" href="#main-content">Skip to content</a>' + ld(WEBSITE_LD) + header() + ld(GAME_LD)
            + main + FOOTER + page_ld + (ADS if page["ads"] else "\n") + "</body></html>\n")
    return head(page["title"], page["description"], url, og_type="website" if page["route"] == "/" else "article") + body

def render_404():
    main = open(os.path.join(FRAG, "404.html"), encoding="utf-8").read().strip()
    return head(NOT_FOUND["title"], NOT_FOUND["description"], None, robots="noindex") + \
        '<body><a class="skip-link" href="#main-content">Skip to content</a>' + header() + main + FOOTER + "\n</body></html>\n"

def sitemap():
    rows = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in PAGES:
        rows.append(f'<url>\n<loc>{DOMAIN}{p["route"]}</loc>\n<lastmod>{p["lastmod"]}</lastmod>\n<changefreq>{p["changefreq"]}</changefreq>\n<priority>{p["priority"]}</priority>\n</url>')
    rows.append("</urlset>")
    return "\n".join(rows) + "\n"

def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def main():
    for p in PAGES:
        write(p["file"], render(p))
    for f in NOT_FOUND["files"]:
        write(f, render_404())
    write("sitemap.xml", sitemap())
    print(f"built {len(PAGES)} pages + 404 + sitemap")

if __name__ == "__main__":
    main()
