#!/usr/bin/env python3
"""Build one detail page per i5 project into projects/, reusing index.html's styles.

Run from the repo root:  python3 scripts/build_project_pages.py
Facts here must stay true (see PRODUCT.md): no prices, plot sizes or claims that
are not confirmed. Sample (lorem ipsum) listings get no detail pages.
"""
import re, html, os, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
OUT = ROOT / "projects"
U = "https://images.unsplash.com/photo-"
TEL = "+917200141515"

P = [
  dict(slug="i5-palace", name="i5 Palace", type="plots", loc="Nellikuppam - Keezhur, Chengalpattu", img="1500382017468-9049fed747ef",
       facts=[("Property type","Residential plots"),("Township size","92 acres"),("Approval","DTCP"),("Community","Gated"),("Location","Nellikuppam - Keezhur, near GST Road and Guduvanchery")],
       appr="DTCP", flagship=True,
       overview="Located at Nellikuppam - Keezhur, i5 Palace offers DTCP approved plots in a planned, gated community close to GST Road and Guduvanchery, one of Chennai's fastest-growing suburbs.",
       highlights=["92-acre planned township","DTCP approved layout","Gated community","Wide internal roads","Parks and open spaces","Near GST Road","Bank loan assistance"]),
  dict(slug="i5-aurowin-enclave", name="i5 Aurowin Enclave", type="plots", loc="Chennai", img="1628624747186-a941c476b7ef",
       facts=[("Property type","Residential plots"),("Approval","DTCP")], appr="DTCP"),
  dict(slug="i5-wonder-city", name="i5 Wonder City", type="plots", loc="Chennai", img="1592595896551-12b371d546d5",
       facts=[("Property type","Residential plots"),("Approval","DTCP")], appr="DTCP"),
  dict(slug="i5-palace-city", name="i5 Palace City", type="plots", loc="Chennai", img="1449844908441-8829872d2607",
       facts=[("Property type","Residential plots"),("Approval","DTCP")], appr="DTCP"),
  dict(slug="gokul-avenue", name="Gokul Avenue", type="villas", loc="Chennai", img="1613490493576-7fde63acd811",
       facts=[("Property type","Independent villas"),("Community","Gated")], appr=""),
  dict(slug="i5-ava-palace", name="i5 AVA Palace", type="apartments", loc="Chennai", img="1545324418-cc1a3fa10c00",
       facts=[("Property type","Apartments"),("Approval","RERA")], appr="RERA"),
  dict(slug="spyka-bliss", name="Spyka Bliss", type="apartments", loc="Chennai", img="1512917774080-9991f1c4c750",
       facts=[("Property type","Apartments"),("Approval","RERA")], appr="RERA"),
  dict(slug="kurumba-i5-farms", name="Kurumba i5 Farms", type="farmland", loc="Tamil Nadu", img="1464226184884-fa280b87c399",
       facts=[("Property type","Managed farmland"),("Use","Weekend home")], appr=""),
  dict(slug="tamara-farms", name="Tamara Farms", type="farmland", loc="Tamil Nadu", img="1523348837708-15d4a09cfac2",
       facts=[("Property type","Managed farmland"),("Use","Weekend home")], appr=""),
]
TL = dict(plots="Plots", villas="Villas", apartments="Apartments", farmland="Farmland")
DESC = dict(plots="residential plot", villas="villa", apartments="apartment", farmland="managed farmland")

src = INDEX.read_text()
css = src[src.index("<style>")+7: src.index("</style>")]
css = css.replace('url("assets/', 'url("../assets/')
head_links = src[src.index('<link rel="icon"'): src.index("<style>")]
head_links = "\n".join(l for l in head_links.split("\n") if "images.unsplash.com/photo-" not in l or "preconnect" in l)
sprite = re.search(r'<svg width="0" height="0".*?</svg>', src, re.S).group(0)
logo = re.search(r'<a href="#top"><img .*?></a>', src).group(0).replace('href="#top"', 'href="../index.html"').replace("this.src='assets/", "this.src='../assets/")
footer = re.search(r"<footer>.*?</footer>", src, re.S).group(0)
footer = re.sub(r'href="#', 'href="../index.html#', footer).replace("this.src='assets/", "this.src='../assets/")
wa_svg = re.search(r'<a class="wa"[^>]*>\s*(<svg viewBox="0 0 32 32">.*?</svg>)', src, re.S).group(1)

DETAIL_CSS = """
/* ===== project detail page ===== */
.crumbs{font-size:var(--fs-small);color:var(--text);padding:18px 0}
.crumbs a{color:var(--text);text-decoration:underline;text-underline-offset:3px;text-decoration-color:#cfcbc2}
.crumbs a:hover{color:var(--ink)}
.crumbs span[aria-current]{color:var(--ink);font-weight:600}
.pd-head{display:flex;justify-content:space-between;align-items:end;gap:24px;flex-wrap:wrap;padding-bottom:24px}
.pd-head h1{font-size:var(--fs-h2);line-height:1.1;letter-spacing:-.015em}
.pd-head .loc{display:flex;gap:6px;align-items:center;color:var(--text);margin-top:8px}
.pd-head .loc .ico{width:18px;height:18px;color:var(--muted)}
.pd-type{font-size:var(--fs-label);font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--c);margin-bottom:6px}
.pd-price{text-align:right}
.pd-price b{display:block;font-size:var(--fs-item)}
.pd-price span{font-size:var(--fs-small);color:var(--text)}
.pd-gallery{position:relative;aspect-ratio:21/9;background:#d9d6d0;overflow:hidden}
.pd-gallery img{width:100%;height:100%;object-fit:cover}
.pd-gallery .badges{top:14px;left:14px}
.pd-grid{display:grid;grid-template-columns:minmax(0,1fr) 360px;gap:40px;align-items:start;padding:40px 0 80px}
.pd-sec{padding:28px 0;border-bottom:1px solid var(--line)}
.pd-sec:first-child{padding-top:0}
.pd-sec h2{font-size:1.5rem;margin-bottom:14px}
.pd-sec p{color:var(--text);max-width:68ch}
.pd-facts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));border-top:1px solid var(--line)}
.pd-facts div{padding:14px 16px 14px 0;border-bottom:1px solid var(--line)}
.pd-facts dt{font-size:var(--fs-label);font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.pd-facts dd{font-weight:600;margin-top:2px}
.pd-hl{list-style:none;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px 24px}
.pd-hl li{display:flex;gap:10px;align-items:flex-start}
.pd-hl .ico{color:var(--green);width:20px;height:20px;margin-top:2px;stroke-width:2}
.pd-docs{list-style:none;display:flex;flex-wrap:wrap;gap:8px}
.pd-docs li{background:var(--chip);padding:8px 12px;font-size:.9375rem}
.pd-steps{list-style:none;counter-reset:s;display:grid;gap:14px}
.pd-steps li{counter-increment:s;display:grid;grid-template-columns:36px 1fr;gap:12px;align-items:start}
.pd-steps li::before{content:counter(s);width:32px;height:32px;border-radius:50%;background:var(--chip);display:grid;place-items:center;font-weight:700;color:var(--brand-ink)}
.pd-steps b{display:block}
.pd-steps span{color:var(--text);font-size:.9375rem}
.pd-note{font-size:var(--fs-small);color:var(--muted);margin-top:14px}
.pd-side{position:sticky;top:100px;border:1px solid var(--line);background:#fff}
.pd-adv{display:flex;gap:14px;align-items:center;padding:20px;border-bottom:1px solid var(--line)}
.pd-adv .av{width:52px;height:52px;font-size:1.125rem}
.pd-adv b{display:block}
.pd-adv div span{display:flex;align-items:center;gap:4px;font-size:var(--fs-small);color:var(--text)}
.pd-adv .ico{width:14px;height:14px;color:#2f6b22;stroke-width:2.4}
.pd-quick{display:grid;grid-template-columns:1fr 1fr;border-bottom:1px solid var(--line)}
.pd-quick a{display:flex;align-items:center;justify-content:center;gap:8px;padding:14px;font-weight:600;min-height:48px}
.pd-quick a+a{border-left:1px solid var(--line)}
.pd-quick .ico{width:18px;height:18px}
.pd-form{padding:20px}
.pd-form h2{font-size:1.25rem;margin-bottom:4px}
.pd-form>p{color:var(--text);font-size:var(--fs-small);margin-bottom:16px}
.pd-form .btn{width:100%}
.sim{background:var(--soft);padding:64px 0}
.sim h2{font-size:var(--fs-h2);margin-bottom:24px}
.sim .results{grid-template-columns:repeat(3,minmax(0,1fr))}
.lst h3 a,.lst-img>a{color:inherit}
.lst h3 a:hover{color:var(--brand-ink)}
@media (max-width:1024px){.pd-grid{grid-template-columns:minmax(0,1fr) 300px;gap:28px}.sim .results{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:860px){.pd-grid{grid-template-columns:1fr}.pd-side{position:static}.pd-gallery{aspect-ratio:16/9}.pd-price{text-align:left}}
@media (max-width:600px){.pd-facts,.pd-hl{grid-template-columns:1fr}.sim .results{grid-template-columns:1fr}.pd-grid{padding:28px 0 56px}}
"""

def imgs(pid, w, h):
    return f"{U}{pid}?auto=format&fit=crop&w={w}&q=60&h={h}"

def badges(p):
    b = []
    if p.get("flagship"): b.append('<span class="bdg bdg-feat">Flagship</span>')
    if p["appr"]: b.append(f'<span class="bdg bdg-ok"><svg class="ico" aria-hidden="true"><use href="#i-check"/></svg>{p["appr"]} approved</span>')
    return "".join(b)

def card(p):
    src = imgs(p["img"], 640, 400)
    dl = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in p["facts"][:2])
    return f'''<article class="lst" data-type="{p["type"]}">
          <div class="lst-img"><a href="{p["slug"]}.html" tabindex="-1" aria-hidden="true"><img src="{src}" alt="" loading="lazy" decoding="async" width="640" height="400"></a><span class="illus">Illustrative image</span><div class="badges">{badges(p)}</div></div>
          <div class="lst-body"><p class="lst-type">{TL[p["type"]]}</p><h3><a href="{p["slug"]}.html">{p["name"]}</a></h3><p class="loc"><svg class="ico" aria-hidden="true"><use href="#i-pin"/></svg>{p["loc"]}</p><dl>{dl}</dl><p class="lst-price"><b>Price on request</b></p></div>
          <div class="lst-act"><a href="tel:{TEL}" aria-label="Call about {p["name"]}">Call</a><a href="{p["slug"]}.html#enquire">View &amp; book</a></div>
        </article>'''

def page(p):
    name = p["name"]; esc_name = html.escape(name)
    similar = [q for q in P if q["type"] == p["type"] and q is not p]
    similar += [q for q in P if q["type"] != p["type"] and q is not p]
    similar = similar[:3]
    facts = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in p["facts"])
    overview = p.get("overview") or (f"{name} is a {DESC[p['type']]} project by i5 Housing &amp; Properties in {p['loc']}. "
                                     "Contact our advisor for the exact location, current availability, sizes and pricing, and to arrange a free site visit.")
    hl = ""
    if p.get("highlights"):
        hl = '<section class="pd-sec"><h2>Highlights</h2><ul class="pd-hl">' + "".join(
            f'<li><svg class="ico" aria-hidden="true"><use href="#i-check"/></svg>{h}</li>' for h in p["highlights"]) + "</ul></section>"
    wa_text = f"Hi i5 Housing, I'd like to know more about {name}."
    wa = "https://wa.me/917200141515?text=" + re.sub(r"[^A-Za-z0-9]", lambda m: "%%%02X" % ord(m.group(0)), wa_text)
    hero = imgs(p["img"], 1600, 686)
    hero_set = f'{imgs(p["img"], 800, 450)} 800w, {imgs(p["img"], 1200, 514)} 1200w, {hero} 1600w'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc_name} | {TL[p["type"]]} in {html.escape(p["loc"])} | i5 Housing Chennai Marketplace</title>
<meta name="description" content="{esc_name}: {DESC[p['type']]} project by i5 Housing &amp; Properties in {html.escape(p['loc'])}. {html.escape(p['appr']+' approved. ' if p['appr'] else '')}Price on request. Book a free site visit.">
{head_links}
<style>{css}{DETAIL_CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{sprite}
<header class="nav">
  <div class="wrap">
    <div class="nav-brand">{logo}<small>Chennai property marketplace</small></div>
    <ul>
      <li><a href="../index.html#listings">Properties</a></li>
      <li><a href="../index.html#localities">Localities</a></li>
      <li><a href="../index.html#i5-palace">Featured</a></li>
      <li><a href="../index.html#faq">FAQ</a></li>
    </ul>
    <div class="nav-cta"><a class="nav-tel" href="tel:{TEL}"><svg class="ico" aria-hidden="true"><use href="#i-phone"/></svg>+91 72001 41515</a><a class="btn btn-brand" href="#enquire">Book a Free Site Visit</a></div>
  </div>
</header>

<main id="main" style="--c:var(--c-{p["type"]})">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a> › <a href="../index.html#listings">Properties</a> › <a href="../index.html#listings">{TL[p["type"]]}</a> › <span aria-current="page">{esc_name}</span></nav>
    <div class="pd-head">
      <div><p class="pd-type">{TL[p["type"]]}</p><h1>{esc_name}</h1><p class="loc"><svg class="ico" aria-hidden="true"><use href="#i-pin"/></svg>{p["loc"]}</p></div>
      <div class="pd-price"><b>Price on request</b><span>Call for current availability and pricing</span></div>
    </div>
    <div class="pd-gallery"><img src="{hero}" srcset="{hero_set}" sizes="(max-width:1232px) calc(100vw - 32px), 1200px" alt="" fetchpriority="high" decoding="async" width="1600" height="686"><span class="illus">Illustrative image</span><div class="badges">{badges(p)}</div></div>

    <div class="pd-grid">
      <div>
        <section class="pd-sec"><h2>Overview</h2><p>{overview}</p></section>
        <section class="pd-sec"><h2>Key facts</h2><dl class="pd-facts">{facts}</dl></section>
        {hl}
        <section class="pd-sec"><h2>Documents you receive</h2><ul class="pd-docs"><li>Sale deed</li><li>Approval copies</li><li>Encumbrance certificate</li><li>Patta</li><li>Other title documents as applicable</li></ul><p class="pd-note">Approval details are shared with every buyer before booking.</p></section>
        <section class="pd-sec"><h2>How buying works</h2><ol class="pd-steps">
          <li><div><b>Tell us your needs</b><span>Share your budget, preferred location and purpose.</span></div></li>
          <li><div><b>Visit the site</b><span>We arrange free transport and a guided tour.</span></div></li>
          <li><div><b>Verify and book</b><span>Review all documents, then book your plot or home.</span></div></li>
          <li><div><b>Register</b><span>We help with the loan process and registration.</span></div></li>
        </ol></section>
      </div>
      <aside class="pd-side" id="enquire" aria-label="Contact the developer">
        <div class="pd-adv"><span class="av av-i5" aria-hidden="true">i5</span><div><b>i5 Housing &amp; Properties</b><span><svg class="ico" aria-hidden="true"><use href="#i-shield"/></svg>Verified developer · Since 2010</span></div></div>
        <div class="pd-quick"><a href="tel:{TEL}"><svg class="ico" aria-hidden="true"><use href="#i-phone"/></svg>Call</a><a href="{wa}" target="_blank" rel="noopener"><svg class="ico" aria-hidden="true"><use href="#i-wa"/></svg>WhatsApp</a></div>
        <form class="pd-form" id="visitForm">
          <h2>Book a free site visit</h2>
          <p>Free pick-up and drop on weekdays and weekends.</p>
          <div class="fld"><label for="v-name">Name</label><input id="v-name" name="name" autocomplete="name" placeholder="Your full name" required></div>
          <div class="fld"><label for="v-phone">Mobile number</label><input id="v-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="e.g. 98765 43210" required pattern="\\+?[0-9][0-9 \\-]{{8,14}}[0-9]" title="Enter a 10-digit mobile number, with country code if outside India"></div>
          <p class="note">This opens WhatsApp with your details filled in. Press send there and an advisor will call you back.</p>
          <button class="btn btn-brand" type="submit"><svg class="ico" aria-hidden="true"><use href="#i-wa"/></svg>Book My Free Site Visit</button>
          <p class="sent" role="status" hidden></p>
          <small>We respect your privacy. Your details are only used to contact you about this enquiry.</small>
        </form>
      </aside>
    </div>
  </div>
</main>

<section class="sim" aria-labelledby="simh">
  <div class="wrap">
    <h2 id="simh">Similar properties</h2>
    <div class="results">
        {"".join(card(q) for q in similar)}
    </div>
  </div>
</section>

{footer}

<a class="wa" href="{wa}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">
  {wa_svg}
</a>
<div class="mbar"><a href="tel:{TEL}"><svg class="ico" aria-hidden="true"><use href="#i-phone"/></svg>Call</a><a href="{wa}" target="_blank" rel="noopener"><svg class="ico" aria-hidden="true"><use href="#i-wa"/></svg>WhatsApp</a><a href="#enquire">Site Visit</a></div>

<script>
document.getElementById('yr').textContent=new Date().getFullYear();
document.getElementById('visitForm').addEventListener('submit',e=>{{
  e.preventDefault();const f=e.target,btn=f.querySelector('[type=submit]'),note=f.querySelector('.sent');
  const msg=`Hi i5 Housing, I'd like to book a free site visit to {name}.\\nName: ${{f.name.value}}\\nPhone: ${{f.phone.value}}\\nPlease call me to fix a time.`;
  const url='https://wa.me/917200141515?text='+encodeURIComponent(msg);
  btn.disabled=true;setTimeout(()=>btn.disabled=false,3000);
  const w=window.open(url,'_blank');
  note.innerHTML=w?'Your visit to {name} is one step away. Press send in WhatsApp and our advisor will call you to fix a time. Nothing opened? <a href="'+url+'" target="_blank" rel="noopener">Open WhatsApp again</a> or call <a href="tel:{TEL}">+91 72001 41515</a>.'
    :'Your browser stopped WhatsApp from opening, so your details are still here. <a href="'+url+'" target="_blank" rel="noopener">Open WhatsApp</a> or call <a href="tel:{TEL}">+91 72001 41515</a>.';
  note.hidden=false;if(w)f.reset();
}});
</script>
</body>
</html>
'''

OUT.mkdir(exist_ok=True)
for p in P:
    (OUT / f'{p["slug"]}.html').write_text(page(p))

# link index.html cards to their pages (idempotent)
idx = INDEX.read_text()
for p in P:
    h = f'<h3>{p["name"]}</h3>'
    if h in idx:
        idx = idx.replace(h, f'<h3><a href="projects/{p["slug"]}.html">{p["name"]}</a></h3>', 1)
if ".lst h3 a{" not in idx:
    idx = idx.replace("</style>", ".lst h3 a{color:inherit}\n.lst h3 a:hover{color:var(--brand-ink);text-decoration:underline;text-underline-offset:3px}\n</style>", 1)
INDEX.write_text(idx)
print("built", len(P), "project pages")
