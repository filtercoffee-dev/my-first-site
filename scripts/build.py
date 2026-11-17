#!/usr/bin/env python3
"""Build the Northlight test site: index.html (home) and lumen.html (product page).

Run from the repo root:  python3 scripts/build.py

Northlight is a FICTIONAL brand used for testing layout, responsiveness,
animation and loading speed. Nothing is for sale; products, prices and specs
are invented. Devices are drawn as inline SVG, so there are no product photos.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CDN = "https://cdn.jsdelivr.net/gh/filtercoffee-dev/my-first-site@3d0a8afa2ebcb06c3fb64555117ec69cc44e27d2/assets"

CSS = r"""
@font-face{font-family:"Archivo";font-style:normal;font-weight:400 700;font-display:swap;src:url("%(cdn)s/fonts/archivo-sub.woff2") format("woff2"),url("assets/fonts/archivo-sub.woff2") format("woff2");unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+20B9,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
:root{
  --ink:#0d1014; --text:#454b54; --muted:#636a74; --line:#dfe2e6;
  --bg:#ffffff; --mist:#f1f3f5; --night:#0b0d10; --night-2:#15181d; --night-line:#2a2f37; --night-text:#b9c0ca;
  --link:#0b7a68; --link-night:#62dfc8; --cta:#0d1014; --hot:#ff6a3d;
  --r:28px; --gap:14px; --nav-h:48px;
  --fs-fine:.75rem; --fs-small:.875rem; --fs-body:1.0625rem; --fs-sub:clamp(1.125rem,2vw,1.625rem);
  --fs-h3:clamp(1.5rem,2.6vw,2.25rem); --fs-h2:clamp(2rem,4.4vw,3.5rem); --fs-h1:clamp(2.5rem,7vw,5.25rem);
  --ease:cubic-bezier(.16,1,.3,1);
}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%%;accent-color:var(--link);caret-color:var(--link)}
@media (prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
::selection{background:#bfeee4;color:var(--ink)}
:focus-visible{outline:2px solid var(--link);outline-offset:3px;border-radius:4px}
.dark :focus-visible,.gnav :focus-visible,footer :focus-visible{outline-color:var(--link-night)}
[id]{scroll-margin-top:calc(var(--nav-h) + 16px)}
body{font-family:"Archivo",system-ui,Arial,sans-serif;font-size:var(--fs-body);line-height:1.5;color:var(--ink);background:var(--bg);-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
svg{display:block}
h1,h2,h3{font-weight:700;letter-spacing:-.03em;line-height:1.04;text-wrap:balance}
p{text-wrap:pretty}
.wrap{width:min(1080px,100%% - 40px);margin-inline:auto}
.skip{position:absolute;left:12px;top:-60px;z-index:200;background:#fff;color:var(--ink);padding:10px 14px;font-weight:600;border-radius:8px}
.skip:focus{top:8px}
.ico{width:18px;height:18px;stroke:currentColor;fill:none;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}

/* global nav */
.gnav{position:sticky;top:0;z-index:100;height:var(--nav-h);background:rgba(11,13,16,.82);color:#e9ecef;-webkit-backdrop-filter:saturate(160%%) blur(18px);backdrop-filter:saturate(160%%) blur(18px);font-size:var(--fs-small)}
.gnav .wrap{height:100%%;display:flex;align-items:center;justify-content:space-between;gap:16px}
.brand{display:inline-flex;align-items:center;gap:8px;font-weight:700;letter-spacing:-.02em;font-size:1rem;min-height:44px}
.brand svg{width:20px;height:20px}
.gnav ul{display:flex;gap:clamp(14px,2.6vw,34px);list-style:none}
.gnav ul a{display:block;padding:14px 0;color:#c9ced6;transition:color .2s}
.gnav ul a:hover,.gnav ul a[aria-current]{color:#fff}
.gnav-tools{display:flex;align-items:center;gap:4px}
.icon-btn{width:44px;height:44px;display:grid;place-items:center;border:0;background:none;color:#e9ecef;cursor:pointer;border-radius:50%%}
.icon-btn:hover{color:#fff}
.menu-btn{display:none}
.bag-n{position:absolute;margin:14px 0 0 16px;min-width:15px;height:15px;border-radius:8px;background:var(--hot);color:#fff;font-size:.625rem;font-weight:700;display:grid;place-items:center;padding:0 4px}
.bag-n[hidden]{display:none}

/* mobile menu */
.sheet{position:fixed;inset:var(--nav-h) 0 0 0;z-index:99;background:var(--night);color:#fff;padding:20px 28px 40px;overflow:auto;opacity:0;visibility:hidden;transform:translateY(-8px);transition:opacity .25s var(--ease),transform .25s var(--ease),visibility .25s}
.sheet.open{opacity:1;visibility:visible;transform:none}
.sheet a{display:block;font-size:1.75rem;font-weight:700;letter-spacing:-.02em;padding:12px 0;border-bottom:1px solid var(--night-line)}

/* ribbon */
.ribbon{background:var(--mist);text-align:center;font-size:var(--fs-small);padding:12px 20px;color:var(--text)}
.ribbon a{color:var(--link);font-weight:600}
.ribbon a:hover{text-decoration:underline;text-underline-offset:3px}

/* tiles */
.stack{display:grid;gap:var(--gap);padding:var(--gap) 0}
.tile{position:relative;overflow:hidden;text-align:center;background:var(--mist);padding:clamp(44px,6vw,72px) 20px 0;display:flex;flex-direction:column;align-items:center;min-height:clamp(520px,62vw,720px)}
.tile.dark{background:var(--night);color:#fff}
.tile.tint{background:linear-gradient(180deg,#e9f6f2,#f6f1ea)}
.tile h2{font-size:var(--fs-h1)}
.tile .sub{font-size:var(--fs-sub);margin-top:10px;color:var(--text);max-width:28ch;line-height:1.3;letter-spacing:-.01em}
.tile.dark .sub{color:var(--night-text)}
.new{color:var(--hot);font-weight:600;font-size:var(--fs-small);margin-bottom:8px}
.links{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:20px}
.pill{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:0 22px;border-radius:999px;font-weight:600;font-size:1rem;border:1.5px solid transparent;cursor:pointer;font-family:inherit;transition:background .2s,color .2s,border-color .2s,transform .12s}
.pill:active{transform:scale(.97)}
.pill-solid{background:var(--cta);color:#fff}
.pill-solid:hover{background:#2a3038}
.dark .pill-solid{background:#fff;color:var(--ink)}
.dark .pill-solid:hover{background:#dfe3e8}
.pill-line{border-color:currentColor;color:var(--link)}
.pill-line:hover{background:var(--link);color:#fff;border-color:var(--link)}
.dark .pill-line{color:var(--link-night)}
.dark .pill-line:hover{background:var(--link-night);color:var(--ink);border-color:var(--link-night)}
.art{margin-top:auto;padding-top:36px;width:100%%;display:flex;justify-content:center;align-items:flex-end}
.art svg{width:min(100%%,var(--w,520px));height:auto}

.duo{display:grid;grid-template-columns:1fr 1fr;gap:var(--gap);padding:0 var(--gap) var(--gap)}
.duo .tile{border-radius:var(--r);min-height:clamp(440px,44vw,580px);padding-top:clamp(36px,4vw,56px)}
.duo .tile h2{font-size:var(--fs-h2)}
.duo .tile .sub{font-size:clamp(1rem,1.5vw,1.25rem)}

/* carousel */
.shelf{padding:72px 0 80px}
.shelf-head{display:flex;justify-content:space-between;align-items:end;gap:20px;margin-bottom:24px}
.shelf-head h2{font-size:var(--fs-h2)}
.shelf-btns{display:flex;gap:10px}
.round{width:44px;height:44px;border-radius:50%%;border:0;background:var(--mist);display:grid;place-items:center;cursor:pointer;color:var(--ink);transition:background .2s}
.round:hover{background:#e2e6ea}
.round:disabled{opacity:.35;cursor:default}
.track{display:flex;gap:var(--gap);overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;padding:0 max(20px,calc((100vw - 1080px)/2));scroll-padding-inline:max(20px,calc((100vw - 1080px)/2))}
.track::-webkit-scrollbar{display:none}
.story{flex:0 0 min(78vw,400px);scroll-snap-align:start;border-radius:var(--r);min-height:480px;padding:28px;display:flex;flex-direction:column;color:#fff;position:relative;overflow:hidden;background:var(--c1)}
.story::before{content:"";position:absolute;inset:0;background:radial-gradient(120%% 80%% at 80%% 100%%,var(--c2),transparent 60%%)}
.story>*{position:relative}
.story small{font-size:var(--fs-small);font-weight:600;opacity:.85}
.story h3{font-size:var(--fs-h3);margin-top:8px;max-width:12ch}
.story p{margin-top:auto;opacity:.92;max-width:26ch}

/* text band */
.band{padding:96px 0;text-align:center}
.band h2{font-size:var(--fs-h2);max-width:18ch;margin-inline:auto}
.band p{color:var(--text);font-size:var(--fs-sub);line-height:1.35;max-width:36ch;margin:16px auto 0}
.perks{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--gap);margin-top:48px;text-align:left}
.perk{background:var(--mist);border-radius:var(--r);padding:28px}
.perk svg{width:28px;height:28px;color:var(--link);margin-bottom:18px}
.perk h3{font-size:1.25rem;letter-spacing:-.02em;margin-bottom:6px}
.perk p{font-size:1rem;color:var(--text);margin:0;max-width:none;line-height:1.5}

/* footer */
footer{background:var(--mist);color:var(--muted);font-size:var(--fs-fine);line-height:1.6;padding:28px 0 32px}
.fine{border-bottom:1px solid var(--line);padding-bottom:18px;display:grid;gap:8px}
.fine b{color:var(--ink)}
.dir{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;padding:24px 0;border-bottom:1px solid var(--line)}
.dir h3{font-size:var(--fs-fine);letter-spacing:0;color:var(--ink);margin-bottom:8px;font-weight:600}
.dir ul{list-style:none;display:grid}
.dir a{display:inline-block;padding:6px 0}
.dir a:hover,.legal a:hover{color:var(--ink);text-decoration:underline;text-underline-offset:3px}
.dir details summary{list-style:none;cursor:default}
.dir details summary::-webkit-details-marker{display:none}
.legal{display:flex;justify-content:space-between;gap:12px 24px;flex-wrap:wrap;padding-top:18px}
.legal nav{display:flex;gap:18px;flex-wrap:wrap}

/* reveal on scroll */
.rv{opacity:0;transform:translateY(24px);transition:opacity .9s var(--ease),transform .9s var(--ease)}
.rv.in{opacity:1;transform:none}
.no-js .rv{opacity:1;transform:none}
@supports (animation-timeline:view()){
  @media (prefers-reduced-motion:no-preference){
    .zoom svg{animation:zoom linear both;animation-timeline:view();animation-range:entry 0%% cover 55%%}
    @keyframes zoom{from{transform:scale(.86) translateY(6%%)}to{transform:none}}
  }
}

/* ---------- product page ---------- */
.lnav{position:sticky;top:var(--nav-h);z-index:90;background:rgba(255,255,255,.86);-webkit-backdrop-filter:saturate(160%%) blur(18px);backdrop-filter:saturate(160%%) blur(18px);border-bottom:1px solid var(--line)}
.lnav .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:56px}
.lnav b{font-size:1.25rem;letter-spacing:-.02em}
.lnav div{display:flex;align-items:center;gap:22px;font-size:var(--fs-small)}
.lnav div a:not(.pill){color:var(--text);padding:12px 0}
.lnav div a:not(.pill):hover{color:var(--ink)}
.lnav .pill{min-height:36px;padding:0 16px;font-size:var(--fs-small)}
.p-hero{background:var(--night);color:#fff;text-align:center;padding:clamp(56px,8vw,96px) 20px 0;overflow:hidden}
.p-hero h1{font-size:var(--fs-h1)}
.p-hero .sub{font-size:var(--fs-sub);color:var(--night-text);margin:12px auto 0;max-width:30ch;line-height:1.3}
.p-hero .price{margin-top:16px;color:#fff;font-size:1rem}
.feat{padding:clamp(72px,10vw,128px) 0}
.feat .wrap{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,6vw,80px);align-items:center}
.feat.flip .copy{order:2}
.feat h2{font-size:var(--fs-h2)}
.feat p{color:var(--text);font-size:var(--fs-sub);line-height:1.35;margin-top:16px;max-width:28ch}
.feat .stat{display:flex;gap:32px;margin-top:28px;flex-wrap:wrap}
.feat .stat b{display:block;font-size:var(--fs-h3);letter-spacing:-.03em;line-height:1}
.feat .stat span{font-size:var(--fs-small);color:var(--muted)}
.panel{border-radius:var(--r);background:var(--mist);min-height:420px;display:grid;place-items:center;padding:32px;overflow:hidden}
.panel.dark{background:var(--night)}
.panel svg{width:min(100%%,360px);height:auto}
.finish{background:var(--mist);padding:clamp(72px,9vw,112px) 0;text-align:center}
.finish h2{font-size:var(--fs-h2)}
.finish .phone{--body:#20252d;--edge:#3a414c;--glow:#62dfc8;margin:36px auto 0;width:min(70vw,300px)}
.finish .phone svg{width:100%%;height:auto}
.finish .phone *{transition:fill .5s var(--ease),stop-color .5s var(--ease)}
.swatches{display:flex;justify-content:center;gap:14px;margin-top:28px}
.sw{width:44px;height:44px;border-radius:50%%;border:0;background:none;cursor:pointer;display:grid;place-items:center}
.sw i{width:28px;height:28px;border-radius:50%%;background:var(--c);box-shadow:inset 0 0 0 1px rgba(0,0,0,.18)}
.sw[aria-pressed="true"] i{box-shadow:inset 0 0 0 1px rgba(0,0,0,.18),0 0 0 3px var(--mist),0 0 0 5px var(--link)}
.finish .name{margin-top:10px;font-weight:600;min-height:1.5em}
.compare{padding:clamp(72px,9vw,112px) 0}
.compare h2{font-size:var(--fs-h2);text-align:center;margin-bottom:36px}
.table{overflow-x:auto}
table{border-collapse:collapse;width:100%%;min-width:560px;font-size:1rem}
th,td{text-align:left;padding:16px 14px;border-bottom:1px solid var(--line);vertical-align:top}
thead th{font-size:1.25rem;letter-spacing:-.02em}
tbody th{font-weight:500;color:var(--muted);font-size:var(--fs-small)}
td{font-variant-numeric:tabular-nums}
.buy{background:var(--night);color:#fff;text-align:center;padding:clamp(72px,9vw,112px) 20px}
.buy h2{font-size:var(--fs-h2)}
.buy p{color:var(--night-text);margin-top:12px}
.toast{position:fixed;left:50%%;bottom:24px;transform:translate(-50%%,20px);background:var(--ink);color:#fff;padding:14px 20px;border-radius:14px;font-size:var(--fs-small);opacity:0;visibility:hidden;transition:opacity .3s var(--ease),transform .3s var(--ease),visibility .3s;z-index:120;max-width:calc(100vw - 32px);text-align:center}
.toast.show{opacity:1;visibility:visible;transform:translate(-50%%,0)}

@media (max-width:860px){
  .gnav ul{display:none}
  .menu-btn{display:grid}
  .duo{grid-template-columns:1fr}
  .perks{grid-template-columns:1fr}
  .feat .wrap{grid-template-columns:1fr}
  .feat.flip .copy{order:0}
  .dir{grid-template-columns:1fr;gap:0;padding:8px 0}
  .dir details{border-bottom:1px solid var(--line)}
  .dir details:last-child{border-bottom:0}
  .dir details summary{cursor:pointer;display:flex;justify-content:space-between;align-items:center;min-height:44px}
  .dir details summary::after{content:"+";font-size:1.1rem;color:var(--muted)}
  .dir details[open] summary::after{content:"−"}
  .dir h3{margin:0}
  .dir ul{padding-bottom:10px}
  .dir a{padding:9px 0}
  .lnav div a:not(.pill){display:none}
}
@media (max-width:520px){
  :root{--r:22px;--gap:10px}
  .story{min-height:420px}
}
@media (prefers-reduced-motion:reduce){
  .rv{opacity:1;transform:none;transition:none}
  .pill:active{transform:none}
  .sheet,.toast,.finish .phone *{transition:none}
}
""" % {"cdn": CDN}

# ---------------- device art (original inline SVG) ----------------
def phone(w=300, idp="p", wall=("#62dfc8", "#3b6cf0", "#0b0d10")):
    return f'''<svg viewBox="0 0 300 600" width="{w}" role="img" aria-label="Illustration of the Lumen phone">
  <defs><linearGradient id="{idp}w" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{wall[0]}"/><stop offset=".55" stop-color="{wall[1]}"/><stop offset="1" stop-color="{wall[2]}"/></linearGradient>
  <linearGradient id="{idp}b" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="var(--edge,#3a414c)"/><stop offset=".5" stop-color="var(--body,#20252d)"/><stop offset="1" stop-color="var(--edge,#3a414c)"/></linearGradient></defs>
  <rect x="8" y="8" width="284" height="584" rx="52" fill="url(#{idp}b)"/>
  <rect x="20" y="20" width="260" height="560" rx="42" fill="#06070a"/>
  <rect x="24" y="24" width="252" height="552" rx="38" fill="url(#{idp}w)"/>
  <clipPath id="{idp}c"><rect x="24" y="24" width="252" height="552" rx="38"/></clipPath>
  <g clip-path="url(#{idp}c)"><circle cx="210" cy="330" r="150" fill="#fff" opacity=".1"/><circle cx="90" cy="470" r="110" fill="#000" opacity=".16"/></g>
  <rect x="108" y="38" width="84" height="24" rx="12" fill="#06070a"/>
  <rect x="112" y="548" width="76" height="5" rx="2.5" fill="#fff" opacity=".7"/>
</svg>'''

def laptop(w=640):
    return f'''<svg viewBox="0 0 640 400" width="{w}" role="img" aria-label="Illustration of the Arc laptop">
  <defs><linearGradient id="lw" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffb28f"/><stop offset=".5" stop-color="#ff6a3d"/><stop offset="1" stop-color="#5b2bd6"/></linearGradient>
  <linearGradient id="lb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d9dde2"/><stop offset="1" stop-color="#aab1ba"/></linearGradient></defs>
  <rect x="92" y="14" width="456" height="300" rx="18" fill="#15181d"/>
  <rect x="104" y="26" width="432" height="276" rx="8" fill="url(#lw)"/>
  <clipPath id="lc"><rect x="104" y="26" width="432" height="276" rx="8"/></clipPath>
  <circle cx="420" cy="230" r="150" fill="#fff" opacity=".12" clip-path="url(#lc)"/>
  <path d="M40 318h560l-18 44a14 14 0 0 1-13 9H71a14 14 0 0 1-13-9z" fill="url(#lb)"/>
  <rect x="270" y="318" width="100" height="9" rx="4.5" fill="#8d95a0"/>
</svg>'''

def tablet(w=520):
    return f'''<svg viewBox="0 0 520 380" width="{w}" role="img" aria-label="Illustration of the Slate tablet">
  <defs><linearGradient id="tw" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#0b7a68"/><stop offset=".6" stop-color="#62dfc8"/><stop offset="1" stop-color="#f4e7b0"/></linearGradient></defs>
  <rect x="10" y="10" width="500" height="360" rx="30" fill="#20252d"/>
  <rect x="26" y="26" width="468" height="328" rx="16" fill="url(#tw)"/>
  <path d="M26 290c90-70 170-40 250-90s140-60 218-30v168a16 16 0 0 1-16 16H42a16 16 0 0 1-16-16z" fill="#06231e" opacity=".35"/>
  <circle cx="260" cy="18" r="3" fill="#3a414c"/>
</svg>'''

def watch(w=260):
    return f'''<svg viewBox="0 0 260 380" width="{w}" role="img" aria-label="Illustration of the Pulse watch">
  <rect x="78" y="0" width="104" height="110" rx="26" fill="#2a2f37"/><rect x="78" y="270" width="104" height="110" rx="26" fill="#2a2f37"/>
  <rect x="38" y="74" width="184" height="232" rx="54" fill="#d9dde2"/>
  <rect x="50" y="86" width="160" height="208" rx="44" fill="#0b0d10"/>
  <circle cx="130" cy="190" r="62" fill="none" stroke="#2a2f37" stroke-width="14"/>
  <path d="M130 128a62 62 0 1 1-54 32" fill="none" stroke="#ff6a3d" stroke-width="14" stroke-linecap="round"/>
  <circle cx="130" cy="190" r="38" fill="none" stroke="#2a2f37" stroke-width="12"/>
  <path d="M130 152a38 38 0 0 1 33 57" fill="none" stroke="#62dfc8" stroke-width="12" stroke-linecap="round"/>
  <rect x="222" y="150" width="12" height="42" rx="6" fill="#aab1ba"/>
</svg>'''

def buds(w=320):
    return f'''<svg viewBox="0 0 320 300" width="{w}" role="img" aria-label="Illustration of the Halo earbuds and case">
  <rect x="50" y="110" width="220" height="170" rx="56" fill="#f4f5f7" stroke="#dfe2e6" stroke-width="2"/>
  <path d="M50 178h220" stroke="#dfe2e6" stroke-width="2"/><circle cx="160" cy="200" r="5" fill="#62dfc8"/>
  <g fill="#fff" stroke="#dfe2e6" stroke-width="2"><ellipse cx="112" cy="70" rx="34" ry="38"/><rect x="100" y="84" width="20" height="70" rx="10"/>
  <ellipse cx="208" cy="70" rx="34" ry="38"/><rect x="200" y="84" width="20" height="70" rx="10"/></g>
  <circle cx="104" cy="62" r="9" fill="#20252d"/><circle cx="216" cy="62" r="9" fill="#20252d"/>
</svg>'''

MARK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2l2.6 6.9L22 12l-7.4 3.1L12 22l-2.6-6.9L2 12l7.4-3.1z" fill="currentColor"/></svg>'
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Crect width='24' height='24' rx='5' fill='%230b0d10'/%3E"
           "%3Cpath d='M12 4l2 5.4L20 12l-6 2.6L12 20l-2-5.4L4 12l6-2.6z' fill='%2362dfc8'/%3E%3C/svg%3E")
ICONS = {
    "search": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.3-4.3"/></svg>',
    "bag": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 8h14l-1 12H6z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>',
    "menu": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 8h16M4 16h16"/></svg>',
    "left": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="m14 6-6 6 6 6"/></svg>',
    "right": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="m10 6 6 6-6 6"/></svg>',
    "truck": '<svg viewBox="0 0 24 24" class="ico" aria-hidden="true"><path d="M3 6h11v10H3zM14 10h4l3 3v3h-7z"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/></svg>',
    "swap": '<svg viewBox="0 0 24 24" class="ico" aria-hidden="true"><path d="M4 8h14l-3-3M20 16H6l3 3"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" class="ico" aria-hidden="true"><path d="M12 3 4 6v6c0 4.4 3.4 8.1 8 9 4.6-.9 8-4.6 8-9V6z"/><path d="m8.5 12 2.5 2.5 4.5-5"/></svg>',
}
NAV = [("Store", "index.html#top"), ("Phone", "lumen.html"), ("Tablet", "index.html#slate"), ("Laptop", "index.html#arc"), ("Watch", "index.html#pulse"), ("Audio", "index.html#halo"), ("Support", "index.html#support")]


def head(title, desc):
    return f'''<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex">
<link rel="icon" type="image/svg+xml" href="{FAVICON}">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="{CDN}/fonts/archivo-sub.woff2" crossorigin>
<script>document.documentElement.classList.remove('no-js')</script>
<style>{CSS}</style>
</head>'''


def gnav(current):
    cur = ' aria-current="page"'
    items = "".join(f'<li><a href="{h}"{cur if n == current else ""}>{n}</a></li>' for n, h in NAV)
    sheet = "".join(f'<a href="{h}">{n}</a>' for n, h in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="gnav">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Northlight home">{MARK}Northlight</a>
    <nav aria-label="Main"><ul>{items}</ul></nav>
    <div class="gnav-tools">
      <button class="icon-btn" type="button" aria-label="Search" data-toast="Search is not connected on this test site.">{ICONS["search"]}</button>
      <button class="icon-btn" type="button" aria-label="Shopping bag" id="bagBtn" data-toast="Your bag is a demo. Nothing can be bought here.">{ICONS["bag"]}<span class="bag-n" id="bagN" hidden>0</span></button>
      <button class="icon-btn menu-btn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="sheet" id="menuBtn">{ICONS["menu"]}</button>
    </div>
  </div>
</header>
<nav class="sheet" id="sheet" aria-label="Mobile">{sheet}</nav>'''


def footer():
    cols = [("Shop and learn", ["Store", "Lumen phone", "Slate tablet", "Arc laptop", "Pulse watch", "Halo audio"]),
            ("Account", ["Manage your ID", "Order status", "Saved items"]),
            ("Northlight Store", ["Find a store", "Trade in", "Financing", "Gift cards"]),
            ("About", ["Newsroom", "Careers", "Environment", "Contact"])]
    def lis(items):
        return "".join('<li><a href="#top">' + i + "</a></li>" for i in items)
    dirs = "".join(f"<details open><summary><h3>{t}</h3></summary><ul>{lis(items)}</ul></details>" for t, items in cols)
    return f'''<footer id="support">
  <div class="wrap">
    <div class="fine">
      <p><b>Northlight is a fictional brand.</b> This is a test site for layout, responsiveness, animation and loading speed. Nothing shown here is a real product and nothing is for sale.</p>
      <p>1. Prices, specifications and battery figures are invented placeholders. 2. Device images are illustrations drawn in code, not photographs.</p>
    </div>
    <div class="dir" id="dir">{dirs}</div>
    <div class="legal"><span>© <span id="yr"></span> Northlight test site. Not a real company.</span><nav aria-label="Legal"><a href="#top">Privacy</a><a href="#top">Terms</a><a href="#top">Site map</a></nav></div>
  </div>
</footer>
<div class="toast" id="toast" role="status" aria-live="polite"></div>'''


JS = r"""
(()=>{
  const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
  $('#yr').textContent=new Date().getFullYear();
  // mobile menu
  const mb=$('#menuBtn'),sheet=$('#sheet');
  const setMenu=o=>{sheet.classList.toggle('open',o);mb.setAttribute('aria-expanded',o);document.body.style.overflow=o?'hidden':''};
  mb.addEventListener('click',()=>setMenu(!sheet.classList.contains('open')));
  sheet.addEventListener('click',e=>{if(e.target.closest('a'))setMenu(false)});
  addEventListener('keydown',e=>{if(e.key==='Escape')setMenu(false)});
  matchMedia('(min-width:861px)').addEventListener('change',e=>{if(e.matches)setMenu(false)});
  // toast
  const toast=$('#toast');let tt;
  const say=m=>{toast.textContent=m;toast.classList.add('show');clearTimeout(tt);tt=setTimeout(()=>toast.classList.remove('show'),3200)};
  $$('[data-toast]').forEach(b=>b.addEventListener('click',()=>say(b.dataset.toast)));
  // demo bag
  let bag=0;const bn=$('#bagN');
  $$('[data-add]').forEach(b=>b.addEventListener('click',()=>{bag++;bn.textContent=bag;bn.hidden=false;say(b.dataset.add+' added to your demo bag. Nothing is actually for sale.')}));
  // reveal on scroll
  const rv=$$('.rv');
  if('IntersectionObserver' in window&&!matchMedia('(prefers-reduced-motion: reduce)').matches){
    const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{rootMargin:'0px 0px -12% 0px'});
    rv.forEach(el=>io.observe(el));
  }else rv.forEach(el=>el.classList.add('in'));
  // footer directory: accordions on small screens only
  const wide=matchMedia('(min-width:861px)'),dets=$$('#dir details');
  const syncDir=()=>dets.forEach(d=>d.open=wide.matches);syncDir();wide.addEventListener('change',syncDir);
  dets.forEach(d=>d.querySelector('summary').addEventListener('click',e=>{if(wide.matches)e.preventDefault()}));
  // carousel
  const track=$('#track');
  if(track){
    const prev=$('#prev'),next=$('#next');
    const step=()=>{const c=track.querySelector('.story');return c?c.getBoundingClientRect().width+14:320};
    const upd=()=>{prev.disabled=track.scrollLeft<4;next.disabled=track.scrollLeft+track.clientWidth>track.scrollWidth-4};
    prev.addEventListener('click',()=>track.scrollBy({left:-step(),behavior:'smooth'}));
    next.addEventListener('click',()=>track.scrollBy({left:step(),behavior:'smooth'}));
    track.addEventListener('scroll',upd,{passive:true});addEventListener('resize',upd);upd();
  }
  // finish picker
  const ph=$('#finishPhone');
  if(ph){
    const name=$('#finishName');
    $$('.sw').forEach(b=>b.addEventListener('click',()=>{
      $$('.sw').forEach(x=>x.setAttribute('aria-pressed',x===b?'true':'false'));
      ph.style.setProperty('--body',b.dataset.body);ph.style.setProperty('--edge',b.dataset.edge);
      name.textContent=b.dataset.name;
    }));
  }
})();
"""


def home():
    stories = [("Photography", "Night, handled.", "Lumen keeps colour true after dark.", "#1c2433", "#3b6cf0"),
               ("Health", "A calmer day.", "Pulse nudges you to breathe, move and rest.", "#3a1f16", "#ff6a3d"),
               ("Work", "Carry less.", "Arc is 1.1 kg of everything you need.", "#10302a", "#0b7a68"),
               ("Sound", "Quiet, on demand.", "Halo fades the world when you ask it to.", "#2a1f3d", "#8a5cf6"),
               ("Create", "Draw anywhere.", "Slate turns a sofa into a studio.", "#33290f", "#d9a514")]
    cards = "".join(f'<article class="story" style="--c1:{a};--c2:{b}"><small>{k}</small><h3>{t}</h3><p>{p}</p></article>' for k, t, p, a, b in stories)
    return f'''{head("Northlight (test site): phones, tablets, laptops, watches and audio", "Northlight is a fictional device brand used as a test site for layout, responsiveness, animation and loading speed. Nothing here is real or for sale.")}
<body id="top">
{gnav("Store")}
<p class="ribbon">Demo notice: Northlight is a fictional brand and this is a test site. <a href="#support">Read the fine print</a></p>

<main id="main">
<div class="stack">
  <section class="tile dark" aria-labelledby="t1">
    <p class="new rv">New</p>
    <h2 id="t1" class="rv">Lumen 12 Pro</h2>
    <p class="sub rv">Light, finally on your side.</p>
    <div class="links rv"><a class="pill pill-solid" href="lumen.html">Learn more</a><a class="pill pill-line" href="lumen.html#buy">Buy</a></div>
    <div class="art zoom" style="--w:300px">{phone(300, "h")}</div>
  </section>

  <section class="tile" id="arc" aria-labelledby="t2">
    <h2 id="t2" class="rv">Arc 14</h2>
    <p class="sub rv">All day. All yours. 1.1 kg.</p>
    <div class="links rv"><a class="pill pill-solid" href="#arc" data-toast="The Arc page is not built on this test site.">Learn more</a><a class="pill pill-line" href="#arc" data-add="Arc 14">Buy</a></div>
    <div class="art zoom" style="--w:640px">{laptop()}</div>
  </section>

  <section class="tile tint" id="slate" aria-labelledby="t3">
    <h2 id="t3" class="rv">Slate Air</h2>
    <p class="sub rv">A sketchbook that never runs out of pages.</p>
    <div class="links rv"><a class="pill pill-solid" href="#slate" data-toast="The Slate page is not built on this test site.">Learn more</a><a class="pill pill-line" href="#slate" data-add="Slate Air">Buy</a></div>
    <div class="art zoom" style="--w:520px">{tablet()}</div>
  </section>
</div>

<div class="duo">
  <section class="tile dark" id="pulse" aria-labelledby="d1">
    <h2 id="d1" class="rv">Pulse 4</h2><p class="sub rv">Your day, in two rings.</p>
    <div class="links rv"><a class="pill pill-solid" href="#pulse" data-toast="The Pulse page is not built on this test site.">Learn more</a><a class="pill pill-line" href="#pulse" data-add="Pulse 4">Buy</a></div>
    <div class="art" style="--w:210px;padding-bottom:28px">{watch()}</div>
  </section>
  <section class="tile" id="halo" aria-labelledby="d2">
    <h2 id="d2" class="rv">Halo Buds</h2><p class="sub rv">Six hours of quiet in your pocket.</p>
    <div class="links rv"><a class="pill pill-solid" href="#halo" data-toast="The Halo page is not built on this test site.">Learn more</a><a class="pill pill-line" href="#halo" data-add="Halo Buds">Buy</a></div>
    <div class="art" style="--w:280px;padding-bottom:28px">{buds()}</div>
  </section>
  <section class="tile tint" aria-labelledby="d3">
    <h2 id="d3" class="rv">Trade in</h2><p class="sub rv">Hand back the old one. Take credit towards the new.</p>
    <div class="links rv"><a class="pill pill-line" href="#top" data-toast="Trade in is a placeholder on this test site.">See how it works</a></div>
    <div class="art" style="--w:170px">{phone(170, "ti", ("#f4e7b0", "#ff6a3d", "#5b2bd6"))}</div>
  </section>
  <section class="tile dark" aria-labelledby="d4">
    <h2 id="d4" class="rv">Northlight Care</h2><p class="sub rv">Two years of cover for drops, spills and bad days.</p>
    <div class="links rv"><a class="pill pill-line" href="#top" data-toast="Care plans are a placeholder on this test site.">Learn more</a></div>
    <div class="art" style="--w:170px">{phone(170, "nc", ("#8a5cf6", "#3b6cf0", "#0b0d10"))}</div>
  </section>
</div>

<section class="shelf" aria-labelledby="sh">
  <div class="wrap shelf-head"><h2 id="sh">Made for the way you live</h2>
    <div class="shelf-btns"><button class="round" id="prev" type="button" aria-label="Previous stories">{ICONS["left"]}</button><button class="round" id="next" type="button" aria-label="Next stories">{ICONS["right"]}</button></div></div>
  <div class="track" id="track" tabindex="0" role="region" aria-label="Stories carousel">{cards}</div>
</section>

<section class="band" aria-labelledby="bh">
  <div class="wrap">
    <h2 id="bh" class="rv">Buying should be the easy part</h2>
    <p class="rv">Placeholder services, shown to test a three-up row.</p>
    <div class="perks">
      <div class="perk rv">{ICONS["truck"]}<h3>Free delivery</h3><p>On every order, to your door or a pickup point.</p></div>
      <div class="perk rv">{ICONS["swap"]}<h3>Easy trade in</h3><p>Credit towards a new device when you return an old one.</p></div>
      <div class="perk rv">{ICONS["shield"]}<h3>Two year cover</h3><p>Repairs and replacements with Northlight Care.</p></div>
    </div>
  </div>
</section>
</main>

{footer()}
<script>{JS}</script>
</body>
</html>
'''


def lumen():
    finishes = [("Graphite", "#20252d", "#3a414c"), ("Mist", "#d9dde2", "#f4f5f7"), ("Fjord", "#1f4e63", "#3d7f99"), ("Ember", "#a8442a", "#d9765a")]
    sw = "".join(f'<button class="sw" type="button" aria-pressed="{"true" if i == 0 else "false"}" aria-label="{n}" data-name="{n}" data-body="{b}" data-edge="{e}" style="--c:{b}"><i></i></button>' for i, (n, b, e) in enumerate(finishes))
    return f'''{head("Lumen 12 Pro | Northlight (test site)", "Lumen 12 Pro is a fictional phone on the Northlight test site. Specs and prices are placeholders; nothing is for sale.")}
<body id="top">
{gnav("Phone")}
<div class="lnav"><div class="wrap"><b>Lumen 12 Pro</b><div><a href="#camera">Camera</a><a href="#battery">Battery</a><a href="#finish">Finishes</a><a href="#compare">Compare</a><a class="pill pill-solid" href="#buy">Buy</a></div></div></div>

<main id="main">
<section class="p-hero" aria-labelledby="ph">
  <p class="new rv">New</p>
  <h1 id="ph" class="rv">Lumen 12 Pro</h1>
  <p class="sub rv">Light, finally on your side.</p>
  <p class="price rv">From ₹79,900 (placeholder price)</p>
  <div class="art zoom" style="--w:340px">{phone(340, "lh")}</div>
</section>

<section class="feat" id="camera">
  <div class="wrap">
    <div class="copy"><h2 class="rv">A camera that reads the room</h2><p class="rv">A larger sensor gathers more light, so evenings look like evenings and faces look like faces.</p>
      <div class="stat rv"><div><b>48 MP</b><span>Main sensor</span></div><div><b>f/1.6</b><span>Aperture</span></div><div><b>5x</b><span>Optical zoom</span></div></div></div>
    <div class="panel dark rv"><svg viewBox="0 0 360 360" role="img" aria-label="Illustration of a camera lens"><circle cx="180" cy="180" r="150" fill="#15181d" stroke="#2a2f37" stroke-width="2"/><circle cx="180" cy="180" r="112" fill="#0b0d10" stroke="#3a414c" stroke-width="10"/><circle cx="180" cy="180" r="70" fill="#101a2c"/><circle cx="180" cy="180" r="42" fill="#1b3a6b"/><circle cx="180" cy="180" r="18" fill="#06070a"/><circle cx="150" cy="148" r="16" fill="#62dfc8" opacity=".55"/><circle cx="206" cy="210" r="7" fill="#fff" opacity=".5"/></svg></div>
  </div>
</section>

<section class="feat flip" id="battery" style="padding-top:0">
  <div class="wrap">
    <div class="copy"><h2 class="rv">Two days, one charge</h2><p class="rv">A denser cell and a calmer chip mean you stop thinking about the percentage.</p>
      <div class="stat rv"><div><b>41 hrs</b><span>Mixed use</span></div><div><b>30 min</b><span>To 60%</span></div></div></div>
    <div class="panel rv"><svg viewBox="0 0 360 200" role="img" aria-label="Illustration of a full battery"><rect x="20" y="40" width="290" height="120" rx="28" fill="none" stroke="#0d1014" stroke-width="8"/><rect x="318" y="76" width="22" height="48" rx="8" fill="#0d1014"/><rect x="36" y="56" width="230" height="88" rx="16" fill="#0b7a68"/><rect x="36" y="56" width="230" height="40" rx="16" fill="#62dfc8" opacity=".35"/></svg></div>
  </div>
</section>

<section class="finish" id="finish" aria-labelledby="fh">
  <div class="wrap">
    <h2 id="fh" class="rv">Four finishes. Pick yours.</h2>
    <div class="phone" id="finishPhone">{phone(300, "fp")}</div>
    <div class="swatches" role="group" aria-label="Choose a finish">{sw}</div>
    <p class="name" id="finishName" aria-live="polite">Graphite</p>
  </div>
</section>

<section class="compare" id="compare" aria-labelledby="ch">
  <div class="wrap">
    <h2 id="ch" class="rv">Which Lumen is right for you?</h2>
    <div class="table rv" tabindex="0" role="region" aria-label="Comparison table"><table>
      <thead><tr><th scope="col"><span class="skip" style="position:static">Feature</span></th><th scope="col">Lumen 12 Pro</th><th scope="col">Lumen 12</th><th scope="col">Lumen SE</th></tr></thead>
      <tbody>
        <tr><th scope="row">Display</th><td>6.7 in, 120 Hz</td><td>6.1 in, 120 Hz</td><td>6.1 in, 60 Hz</td></tr>
        <tr><th scope="row">Main camera</th><td>48 MP, 5x zoom</td><td>48 MP, 2x zoom</td><td>12 MP</td></tr>
        <tr><th scope="row">Battery</th><td>41 hrs</td><td>33 hrs</td><td>26 hrs</td></tr>
        <tr><th scope="row">Storage</th><td>256 GB to 1 TB</td><td>128 GB to 512 GB</td><td>128 GB</td></tr>
        <tr><th scope="row">From</th><td>₹79,900</td><td>₹59,900</td><td>₹39,900</td></tr>
      </tbody></table></div>
  </div>
</section>

<section class="buy dark" id="buy" aria-labelledby="by">
  <h2 id="by" class="rv">Lumen 12 Pro</h2>
  <p class="rv">From ₹79,900. Placeholder price on a test site.</p>
  <div class="links rv"><button class="pill pill-solid" type="button" data-add="Lumen 12 Pro">Add to bag</button><a class="pill pill-line" href="index.html">Back to store</a></div>
</section>
</main>

{footer()}
<script>{JS}</script>
</body>
</html>
'''


(ROOT / "index.html").write_text(home())
(ROOT / "lumen.html").write_text(lumen())
print("built index.html and lumen.html")
