#!/usr/bin/env python3
"""HTTP smoke test: serve the repo root and fetch every route + answer markers."""
import http.server, os, socketserver, sys, threading, urllib.request, urllib.error, functools
sys.path.insert(0, os.path.dirname(__file__))
from registry import PAGES
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARKERS = {"/": ["What's new in One Shot right now", "SUMMER", "Autumn Event", "RANKED", "One Shot Remastered"],
           "/codes/": ["FREE13", "Release Crate", "FREE12", "DISPUTED", "Enter Code...", "Shooter Game Group"],
           "/how-to-play/": ["Up to 8 players per server", "[BEGINNER] One Shot", "permanent ban"],
           "/progression/": ["Long awaited ranked gamemode!", "4 NEW GUNS", "Premium Crate"],
           "/trello/": ["Mnpfw4C5", "Tempest Media", "czh7DKTSu7"]}
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
handler = functools.partial(Q, directory=ROOT)
with socketserver.TCPServer(("127.0.0.1", 0), handler) as srv:
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    fails = 0; n = 0
    for p in PAGES + [{"route": "/sitemap.xml"}, {"route": "/robots.txt"}, {"route": "/assets/answers.css"}, {"route": "/adsterra/runtime.js"}]:
        n += 1
        try:
            body = urllib.request.urlopen(f"http://127.0.0.1:{port}{p['route']}").read().decode("utf-8")
        except urllib.error.HTTPError as e:
            print("FAIL", p["route"], e.code); fails += 1; continue
        for m in MARKERS.get(p["route"], []):
            n += 1
            if m.replace("'", "&#x27;") not in body and m not in body:
                print("FAIL marker", p["route"], m); fails += 1
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{port}/no-such-page/"); print("FAIL 404 route returned 200"); fails += 1
    except urllib.error.HTTPError as e:
        n += 1
        if e.code != 404: print("FAIL 404 code", e.code); fails += 1
    srv.shutdown()
print(("TEST FAIL" if fails else "TEST PASS") + f": {n} checks, {fails} failures")
sys.exit(1 if fails else 0)
