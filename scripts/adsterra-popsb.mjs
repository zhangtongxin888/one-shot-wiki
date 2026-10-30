#!/usr/bin/env node
/* Adsterra Pop + Social Bar only (2026-10-29). Run LAST after the static build:
     node scripts/adsterra-popsb.mjs <outDir>
   Reads scripts/adsterra-socialbar.json {"socialBarScriptUrl": "..."}.
   - Writes scripts/adsterra-runtime-popsb.js (sha256 d3aa9c32...) over every
     <outDir>/adsterra/*runtime.js that pages load.
   - Removes Banner/Native: <aside class="ad-placement|ad-slot"> blocks and any
     hard-coded atOptions / bauval.org/22 / bauval.org/21 snippets.
   - adsterra-config: slots=[]; existing Popunder key kept untouched;
     Social Bar enabled on content pages only (never legal pages / 404 / cleanPage). */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const here = path.dirname(fileURLToPath(import.meta.url));
const out = path.resolve(process.argv[2] || "out");
const { socialBarScriptUrl } = JSON.parse(fs.readFileSync(path.join(here, "adsterra-socialbar.json"), "utf8"));
if (!/^https:\/\/bauval\.org\/14\/[0-9a-f]{32}$/.test(socialBarScriptUrl)) throw new Error("bad socialBarScriptUrl");
const runtime = fs.readFileSync(path.join(here, "adsterra-runtime-popsb.js"));
const CLEAN = new Set(["about","accessibility","advertising-policy","affiliate-disclosure","contact","cookie-policy","cookies","disclosure","dmca","editorial-policy","legal","privacy","sources","terms","corrections","editorial","methodology","404","_not-found","500"]);
const SKIP = new Set(["node_modules","_build","scripts","src","tests",".git",".vercel"]);
const CFG_RE = /(<script[^>]*id="adsterra-config"[^>]*>)([\s\S]*?)(<\/script>)/;
const HARD_RE = [
  /<script[^>]*>\s*(?:window\.)?atOptions\s*=[\s\S]*?<\/script>\s*<script[^>]*bauval\.org\/22\/[^>]*><\/script>/g,
  /<script[^>]*src="https:\/\/bauval\.org\/2[12]\/[^"]*"[^>]*><\/script>/g,
  /<div id="container-[0-9a-f]{32}"><\/div>/g,
];
function stripBlocks(html, name) {
  const open = new RegExp(`<${name}\\b[^>]*class="[^"]*\\b(?:ad-placement|ad-slot)\\b[^"]*"[^>]*>`, "g");
  let m;
  while ((m = open.exec(html))) {
    const tag = new RegExp(`<\\/?${name}\\b[^>]*>`, "g"); tag.lastIndex = m.index + m[0].length;
    let depth = 1, t, end = -1;
    while ((t = tag.exec(html))) { depth += t[0][1] === "/" ? -1 : 1; if (!depth) { end = t.index + t[0].length; break; } }
    if (end < 0) break;
    html = html.slice(0, m.index) + html.slice(end); removed++; open.lastIndex = m.index;
  }
  return html;
}
let pages = 0, sb = 0, removed = 0, rts = new Set();
function walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) { if (!SKIP.has(e.name)) walk(p); continue; }
    if (!e.name.endsWith(".html")) continue;
    const segs = path.relative(out, p).split(path.sep).map((s) => s.replace(/\.html$/, "").toLowerCase());
    const clean = segs.some((s) => CLEAN.has(s));
    let html = fs.readFileSync(p, "utf8"); const before = html;
    html = stripBlocks(stripBlocks(html, "aside"), "div");
    for (const re of HARD_RE) html = html.replace(re, () => { removed++; return ""; });
    const m = html.match(CFG_RE);
    if (m) {
      let cfg = null; try { cfg = JSON.parse(m[2]); } catch {}
      if (cfg) {
        cfg.slots = []; if (Array.isArray(cfg.reserve)) cfg.reserve = [];
        const on = !clean && !cfg.cleanPage && !/<title>[^<]*(404|not found)/i.test(html);
        cfg.enableSocialBar = on; cfg.socialBarScriptUrl = on ? socialBarScriptUrl : "";
        if (on) sb++;
        html = html.replace(CFG_RE, (_a, o, _b, c) => o + JSON.stringify(cfg).replace(/</g, "\\u003c") + c);
      }
    }
    for (const r of html.matchAll(/src="(\/adsterra\/[a-z-]*runtime\.js)"/g)) rts.add(r[1]);
    if (html !== before) { fs.writeFileSync(p, html); pages++; }
  }
}
walk(out);
rts.add("/adsterra/runtime.js");
for (const r of rts) { const f = path.join(out, r); if (fs.existsSync(f) && !fs.readFileSync(f, "utf8").includes('getElementById("adsterra-config")')) continue; /* keep the site's own /adsterra/runtime.js (src/lint.mjs requires it); Pop+SB run from pop-runtime.js */ fs.mkdirSync(path.dirname(f), { recursive: true }); fs.writeFileSync(f, runtime); }
{ const lj = path.join(out, "adsterra", "late.js"), lp = path.join(here, "adsterra-late-popsb.js");
  if (fs.existsSync(lj) && fs.existsSync(lp)) fs.copyFileSync(lp, lj); }
console.log(`adsterra-popsb: pages=${pages} socialBar=${sb} removedAdBlocks=${removed} runtimes=${[...rts].join(",")}`);
