"""Page registry for one-shot.wiki (static, no framework runtime).

Each page's visible <main> lives in _build/pages/<key>.html. build.py wraps it
with the shared head, header, footer, JSON-LD and (for eligible routes) the
Adsterra runtime. lastmod/dateModified only change when the page's visible
answer changes; title-only or shell changes keep the previous date.
"""
DOMAIN = "https://one-shot.wiki"
GAME_URL = "https://www.roblox.com/games/111600158364583/One-Shot"
CSS = ["/_next/static/chunks/164kaxlsh5.z1.css", "/assets/answers.css"]

PAGES = [
    {"key": "home", "route": "/", "file": "index.html", "lastmod": "2026-10-02", "priority": "1", "changefreq": "weekly", "ads": True,
     "title": "One Shot Wiki (Roblox): Codes, Autumn Event, Ranked & Guides",
     "description": "One Shot Wiki for the Roblox one-bullet FFA: working codes (SUMMER, FREE13), the Autumn Event with 4 new guns until Oct 16, the new Ranked mode and duel tips.",
     "crumb": None, "faq": True},
    {"key": "codes", "route": "/codes/", "file": "codes/index.html", "lastmod": "2026-10-02", "priority": "0.8", "changefreq": "weekly", "ads": True,
     "title": "One Shot Codes (October 2026): SUMMER, FREE13 & Free Crates",
     "description": "Working One Shot codes checked Oct 2, 2026: SUMMER (Release Crate) and FREE13 (Crate), disputed FREE12, expired codes, and how to redeem in the Store.",
     "crumb": "Codes", "faq": True},
    {"key": "how-to-play", "route": "/how-to-play/", "file": "how-to-play/index.html", "lastmod": "2026-10-02", "priority": "0.7", "changefreq": "monthly", "ads": True,
     "title": "How to Play One Shot on Roblox: Rules, Reload & First Match",
     "description": "How One Shot on Roblox works: one bullet per gun, 8-player FFA servers, the reload window, the Beginner place, free crates and a step-by-step first match plan.",
     "crumb": "How to Play", "faq": True},
    {"key": "movement-aim", "route": "/movement-aim/", "file": "movement-aim/index.html", "lastmod": "2026-08-10", "priority": "0.7", "changefreq": "monthly", "ads": True,
     "title": "One Shot Movement & Aim Guide: Slide, Strafe & Shot Timing",
     "description": "Practical movement, crosshair placement, shot timing, and reload-survival fundamentals for One Shot on Roblox.",
     "crumb": "Movement & Aim", "faq": False},
    {"key": "progression", "route": "/progression/", "file": "progression/index.html", "lastmod": "2026-10-02", "priority": "0.7", "changefreq": "monthly", "ads": True,
     "title": "One Shot Progression: Crates, Levels, Daily Quests & Ranked",
     "description": "How One Shot progression works: crate types from codes, weapon skins, levels, daily quests, leaderboards, the Autumn Event and the Ranked mode (Oct 2-16, 2026).",
     "crumb": "Progression", "faq": True},
    {"key": "trello", "route": "/trello/", "file": "trello/index.html", "lastmod": "2026-10-02", "priority": "0.6", "changefreq": "monthly", "ads": False,
     "title": "One Shot Trello & Discord (Roblox): Which Links Are Real?",
     "description": "Is there a One Shot Trello? The board most sites list belongs to One Shot Remastered, a different game. Here is the real One Shot Discord, group and game link.",
     "crumb": "Trello & Discord", "faq": True},
    {"key": "sources", "route": "/sources/", "file": "sources/index.html", "lastmod": "2026-10-02", "priority": "0.5", "changefreq": "monthly", "ads": False,
     "title": "Sources & Editorial Policy | One Shot Field Guide",
     "description": "Primary sources, code-verification rule, and correction policy for the independent One Shot Roblox fan guide.",
     "crumb": "Sources", "faq": False},
    {"key": "privacy", "route": "/privacy/", "file": "privacy/index.html", "lastmod": "2026-08-10", "priority": "0.3", "changefreq": "yearly", "ads": False,
     "title": "Privacy Policy | One Shot Field Guide",
     "description": "Privacy information for the independent One Shot fan guide, including data handling and external links.",
     "crumb": "Privacy", "faq": False},
    {"key": "terms", "route": "/terms/", "file": "terms/index.html", "lastmod": "2026-08-10", "priority": "0.3", "changefreq": "yearly", "ads": False,
     "title": "Terms of Use | One Shot Field Guide",
     "description": "Terms governing use of the independent One Shot Roblox fan guide, its content, links and ads.",
     "crumb": "Terms", "faq": False},
    {"key": "disclosure", "route": "/disclosure/", "file": "disclosure/index.html", "lastmod": "2026-08-10", "priority": "0.3", "changefreq": "yearly", "ads": False,
     "title": "Fan Site Disclosure | One Shot Field Guide",
     "description": "Ownership, affiliation, editorial, and monetization disclosure for the independent One Shot fan guide.",
     "crumb": "Disclosure", "faq": False},
    {"key": "contact", "route": "/contact/", "file": "contact/index.html", "lastmod": "2026-08-10", "priority": "0.3", "changefreq": "yearly", "ads": False,
     "title": "Contact | One Shot Field Guide",
     "description": "Report a source-backed correction or find the right official support channel for One Shot and Roblox issues.",
     "crumb": "Contact", "faq": False},
]
NOT_FOUND = {"key": "404", "files": ["404.html", "404/index.html", "_not-found/index.html"],
             "title": "404: Page not found | One Shot Field Guide",
             "description": "This page does not exist. Go back to the One Shot guide home, codes or how-to-play pages."}
