#!/usr/bin/env python3
"""SEO audit for one-shot.wiki: titles, descriptions, H1, wiki-query ownership, dates."""
import html, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from registry import DOMAIN, PAGES
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = {"pages": [], "errors": [], "warnings": []}
titles = {}
sm = open(os.path.join(ROOT, "sitemap.xml")).read()
for p in PAGES:
    s = open(os.path.join(ROOT, p["file"]), encoding="utf-8").read()
    title = html.unescape(re.search(r"<title>(.*?)</title>", s).group(1))
    desc = html.unescape(re.search(r'<meta name="description" content="(.*?)"', s).group(1))
    h1 = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S).group(1)))).strip()
    row = {"route": p["route"], "title": title, "titleLen": len(title), "descLen": len(desc), "h1": h1, "lastmod": p["lastmod"]}
    out["pages"].append(row)
    if title in titles: out["errors"].append(f"duplicate title {title}")
    titles[title] = p["route"]
    if len(title) > 70: out["errors"].append(f"{p['route']}: title {len(title)} > 70")
    if not 70 <= len(desc) <= 165: out["errors"].append(f"{p['route']}: description length {len(desc)}")
    if "one shot" not in (title + h1).lower(): out["warnings"].append(f"{p['route']}: game name missing in title/H1")
    owns_wiki = "one shot wiki" in title.lower() or "one shot wiki" in h1.lower()
    if p["route"] == "/" and not owns_wiki: out["errors"].append("homepage must own 'One Shot Wiki'")
    if p["route"] != "/" and owns_wiki: out["errors"].append(f"{p['route']}: only homepage may claim 'One Shot Wiki' in title/H1")
    if f"<loc>{DOMAIN}{p['route']}</loc>\n<lastmod>{p['lastmod']}</lastmod>" not in sm: out["errors"].append(f"{p['route']}: sitemap lastmod mismatch")
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        d = json.loads(m)
        for g in d.get("@graph", []):
            if g.get("@type") == "Article" and g.get("dateModified") != p["lastmod"]:
                out["errors"].append(f"{p['route']}: dateModified {g.get('dateModified')} != lastmod {p['lastmod']}")
out["status"] = "fail" if out["errors"] else "pass"
print(json.dumps(out, indent=1, ensure_ascii=False))
sys.exit(1 if out["errors"] else 0)
