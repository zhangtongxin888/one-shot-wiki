#!/usr/bin/env python3
"""Structural + fact-rule lint for the built HTML."""
import html, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from registry import DOMAIN, PAGES, NOT_FOUND
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = []
def err(m): errors.append(m)
def read(rel): return open(os.path.join(ROOT, rel), encoding="utf-8").read()
routes = {p["route"] for p in PAGES}
# Codes that may never appear as working (fabrication guard). Extend when a code is disproven.
BANNED_WORKING = {"AUTUMN", "RANKED", "FALL", "FREE14"}
for p in PAGES:
    s = read(p["file"]); r = p["route"]
    if s.count("<title>") != 1: err(f"{r}: title count")
    if len(re.findall(r"<h1[\s>]", s)) != 1: err(f"{r}: h1 count")
    if f'<link rel="canonical" href="{DOMAIN}{r}"/>' not in s: err(f"{r}: canonical")
    for tag in ['name="description"', 'property="og:title"', 'property="og:url"', 'name="twitter:card"', 'name="twitter:title"']:
        if tag not in s: err(f"{r}: missing {tag}")
    if 'content="index, follow"' not in s: err(f"{r}: robots not indexable")
    if "__next_f" in s or re.search(r"_next/static/chunks/[^\"]+\.js", s): err(f"{r}: framework runtime leftover")
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: json.loads(m)
        except Exception as e: err(f"{r}: bad JSON-LD {e}")
    for href in re.findall(r'href="(/[^"#]*)', s):
        if href.startswith(("/_next/", "/media/", "/assets/", "/adsterra/")):
            if not os.path.exists(os.path.join(ROOT, href.lstrip("/"))): err(f"{r}: missing asset {href}")
            continue
        if href not in routes: err(f"{r}: internal link to unknown route {href}")
    for src in re.findall(r'src="(/[^"]+)"', s):
        if not os.path.exists(os.path.join(ROOT, src.lstrip("/"))): err(f"{r}: missing src {src}")
    if p["ads"] != ("/adsterra/runtime.js" in s): err(f"{r}: ads runtime mismatch")
    # code rule: every working row must name >= 3 sources
    for row in re.findall(r'<tr data-code-status="working"([^>]*)>(.*?)</tr>', s, re.S):
        n = int(re.search(r'data-source-count="(\d+)"', row[0]).group(1))
        cells = re.findall(r"<td>(.*?)</td>", row[1], re.S)
        named = [x for x in re.split(r";\s*", re.sub(r"<[^>]+>", "", cells[2])) if x.strip()]
        code = re.sub(r"<[^>]+>", "", cells[0]).strip()
        if n < 3 or len(named) < 3 or len(named) != n: err(f"{r}: working code {code} lacks 3 named sources ({len(named)}/{n})")
        if code in BANNED_WORKING: err(f"{r}: banned code {code} listed as working")
# orphan check: every route linked from at least one other page
linked = set()
for p in PAGES:
    for href in re.findall(r'href="(/[^"#]*)', read(p["file"])):
        if p["route"] != href: linked.add(href)
for p in PAGES:
    if p["route"] != "/" and p["route"] not in linked: err(f"{p['route']}: orphan")
sm = read("sitemap.xml")
for p in PAGES:
    if f"<loc>{DOMAIN}{p['route']}</loc>" not in sm: err(f"sitemap missing {p['route']}")
if "Sitemap: https://one-shot.wiki/sitemap.xml" not in read("robots.txt"): err("robots sitemap line")
for f in NOT_FOUND["files"]:
    if 'content="noindex"' not in read(f): err(f"{f}: 404 must be noindex")
if errors:
    print("LINT FAIL"); [print(" -", e) for e in errors]; sys.exit(1)
print(f"LINT PASS: {len(PAGES)} pages, links, metadata, JSON-LD, sitemap, 3-source code rule")
