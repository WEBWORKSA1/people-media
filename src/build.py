# -*- coding: utf-8 -*-
"""Static site generator for People.Media.
Run:  python3 src/build.py   (writes HTML to the repository root)
No dependencies beyond the Python standard library."""
import json, os, html, datetime, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content_articles import ARTICLES
from content_people import PEOPLE

SITE = "https://people.media"
NAME = "People.Media"
TAGLINE = "Real people. Real stories. Real impact."
ADSENSE = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>'
INQUIRY_URL = "https://web.works/contact"
TODAY = datetime.date.today().isoformat()
E = html.escape

def load_json(name, default):
    p = os.path.join(ROOT, "data", name)
    try:
        with open(p, encoding="utf-8") as f: return json.load(f)
    except Exception: return default

LOGO = '''<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="15" cy="20" r="11" fill="#ff5a36"/><circle cx="25" cy="20" r="11" fill="#0e7c7b" style="mix-blend-mode:multiply"/><circle cx="20" cy="20" r="3.2" fill="#fbf7f1"/></svg>'''

NAV = [("index.html","Home"),("stories.html","Stories"),("people.html","People"),("videos.html","Videos"),("contests.html","Contests"),("get-featured.html","Get Featured"),("advertise.html","Advertise"),("support.html","Support")]

def head(title, desc, path, extra_ld=None, og_type="website"):
    url = SITE + "/" + ("" if path == "index.html" else path)
    ld = [{"@context":"https://schema.org","@type":"Organization","name":NAME,"url":SITE,"logo":SITE+"/assets/img/favicon.svg","slogan":TAGLINE},
          {"@context":"https://schema.org","@type":"WebSite","name":NAME,"url":SITE,"potentialAction":{"@type":"SearchAction","target":SITE+"/stories.html?q={q}","query-input":"required name=q"}}]
    if extra_ld: ld.append(extra_ld)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#ff5a36">
<meta property="og:site_name" content="{NAME}"><meta property="og:type" content="{og_type}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/assets/img/og.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="google-adsense-account" content="ca-pub-6620975821265271">
{ADSENSE}
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="manifest.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,600;0,9..144,700;1,9..144,600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
<link rel="alternate" type="application/rss+xml" title="{NAME} Stories" href="feed.xml">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="inquiry" role="note">Contact, if you are interested in this website / domain name / Sponsorship / Advertisement / Partnership — <a href="{INQUIRY_URL}" target="_blank" rel="noopener">Contact&nbsp;→</a></div>
'''

def header(active):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h==active else ""}>{t}</a>' for h,t in NAV)
    return f'''<header class="site-head"><div class="wrap head-row">
<a class="logo" href="index.html" aria-label="{NAME} home">{LOGO}<span>People<span class="dot">.</span>Media</span></a>
<nav class="nav" id="nav" aria-label="Main">{links}<a href="submit.html" class="btn btn-primary btn-sm" style="margin-left:6px">Share your story</a></nav>
<div class="head-actions"><button class="icon-btn" data-theme-toggle aria-label="Toggle dark mode">◐</button><button class="icon-btn menu-btn" id="menuBtn" aria-label="Menu" aria-expanded="false" aria-controls="nav">☰</button></div>
</div></header>
<div class="reading-bar" aria-hidden="true"></div>
'''

def newsletter_form(compact=False, src="footer"):
    return f'''<form class="newsletter" data-form="Newsletter" data-success="You're on the list. Your first People.Media Weekly arrives this Friday.">
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
<input type="hidden" name="source" value="{src}">
<label class="sr-only" for="nl-{src}">Email</label><input id="nl-{src}" type="email" name="email" required placeholder="Your email address" autocomplete="email">
<button class="btn btn-primary" type="submit">Subscribe free</button></form>'''

def footer():
    return f'''<footer class="site-foot"><div class="wrap">
<div class="foot-grid">
<div><a class="logo" href="index.html" style="color:#fff">{LOGO}<span>People<span class="dot">.</span>Media</span></a>
<p style="margin-top:12px">{TAGLINE} An independent, people-powered media platform celebrating everyday heroes, creators and changemakers.</p>
<p class="fine" style="color:#a59a8e">Weekly stories, zero spam:</p>{newsletter_form(src="footer")}</div>
<div><h4>Read</h4><ul><li><a href="stories.html">All stories</a></li><li><a href="people.html">People profiles</a></li><li><a href="videos.html">Video stories</a></li><li><a href="people-100.html">People.Media 100</a></li><li><a href="feed.xml">RSS feed</a></li></ul></div>
<div><h4>Participate</h4><ul><li><a href="submit.html">Share your story</a></li><li><a href="submit.html#nominate">Nominate someone</a></li><li><a href="contests.html">Contests &amp; prizes</a></li><li><a href="careers.html">Join the team</a></li><li><a href="support.html">Support us</a></li></ul></div>
<div><h4>Business</h4><ul><li><a href="get-featured.html">Get featured</a></li><li><a href="advertise.html">Advertise &amp; sponsor</a></li><li><a href="advertise.html#partner">Partnerships</a></li><li><a href="{INQUIRY_URL}" target="_blank" rel="noopener">Domain &amp; site inquiries</a></li></ul></div>
<div><h4>Company</h4><ul><li><a href="about.html">About</a></li><li><a href="editorial-policy.html">Editorial policy</a></li><li><a href="contact.html">Contact</a></li><li><a href="privacy.html">Privacy &amp; cookies</a></li><li><a href="terms.html">Terms of use</a></li><li><a href="disclaimer.html">Disclaimer &amp; trademark</a></li></ul></div>
</div>
<div class="legal"><span>© <span data-year>2026</span> {NAME}. All original content © {NAME}. "People.Media" is an independent brand and is not affiliated with any similarly named publisher, magazine or dating service. <a href="disclaimer.html">Trademark &amp; copyright notice</a>.</span><span>Ads by Google AdSense · Sponsored content is always labelled.</span></div>
</div></footer>
<div class="cookie" id="cookie" role="dialog" aria-label="Cookie preferences"><strong>Cookies &amp; ads</strong><p class="fine" style="margin:6px 0 0">We use essential cookies and Google AdSense, which may use cookies to show personalized or non-personalized ads. See our <a href="privacy.html">Privacy &amp; Cookie Policy</a>.</p><div class="row"><button class="btn btn-primary btn-sm" data-consent="all">Accept all</button><button class="btn btn-ghost btn-sm" data-consent="essential">Essential only</button></div></div>
<div class="modal" id="nlModal" role="dialog" aria-modal="true" aria-label="Newsletter"><div class="modal-box"><button class="icon-btn x" data-close aria-label="Close">✕</button><span class="eyebrow">People.Media Weekly</span><h3>Five stories that restore your faith in people. Every Friday.</h3><p class="fine">Join readers who start their weekend with real stories, creator tips and contest announcements.</p>{newsletter_form(src="modal")}</div></div>
<a class="btn btn-primary float-cta" href="get-featured.html">★ Get featured</a>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script src="assets/js/config.js"></script>
<script src="assets/js/main.js" defer></script>
</body></html>'''

def page(path, title, desc, body, active=None, ld=None, og_type="website"):
    out = head(title, desc, path, ld, og_type) + header(active or path) + f'<main id="main">{body}</main>' + footer()
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f: f.write(out)
    PAGES.append(path)

PAGES = []

def story_card(a):
    return f'''<article class="card fade" data-item data-cat="{a['cat']}">
<a href="story-{a['slug']}.html" class="card-media {a['gr']}" aria-hidden="true" tabindex="-1">{E(a['tag'])}</a>
<div class="card-body"><div class="meta"><span class="tag coral">{E(a['tag'])}</span><span>{a['mins']} min read</span></div>
<h3><a href="story-{a['slug']}.html">{E(a['title'])}</a></h3><p>{E(a['dek'])}</p></div></article>'''

def person_card(p):
    href = "people-100.html" if p["slug"] == "nominate-your-hero" else f"person-{p['slug']}.html"
    return f'''<article class="card fade" data-item data-cat="{p['cat']}" data-score="0">
<a href="{href}" class="card-media {p['gr']}" style="font-size:2.6rem" aria-hidden="true" tabindex="-1">{E(p['initials'])}</a>
<div class="card-body"><div class="meta"><span class="tag teal">{E(p['cat'].title())}</span><span>{E(p['country'])}</span></div>
<h3><a href="{href}">{E(p['name'])}</a></h3><p>{E(p['summary'])}</p>
<div class="card-foot"><span class="fine">{E(p['role'])}</span><button class="boost" data-boost="{p['slug']}" data-base="0" aria-pressed="false">▲ Boost <b>0</b></button></div></div></article>'''

def headlines_html(limit=8):
    d = load_json("headlines.json", {"items": []})
    items = d.get("items", [])[:limit]
    if not items: return '<p class="fine">Fresh headlines load after the next automatic refresh.</p>'
    return "".join(f'<a href="{E(i["link"])}" target="_blank" rel="noopener nofollow"><span>{E(i["title"])}</span><small>{E(i["source"])}</small></a>' for i in items)

def cta_featured():
    return '''<section><div class="wrap"><div class="cta-band fade">
<div><span class="eyebrow" style="background:rgba(255,255,255,.18);color:#fff">For founders, creators &amp; professionals</span>
<h2>Your story, professionally told — and seen by the right people.</h2>
<p>Get a published People.Media profile or interview, written by an editor, optimized for search and shared across our channels. A credible third-party feature you can show investors, clients and employers.</p>
<ul class="checks"><li>Editor-written profile or Q&amp;A interview</li><li>Permanent, search-optimized page with your links</li><li>Newsletter + social promotion options</li><li>"As featured on People.Media" badge for your site</li></ul>
<div class="pill-row"><a class="btn btn-dark" href="get-featured.html">See packages</a><a class="btn btn-ghost" style="border-color:#fff;color:#fff" href="get-featured.html#apply">Apply in 2 minutes</a></div></div>
<div class="form-card" style="color:var(--ink)"><h3 style="margin-top:0">Quick feature enquiry</h3>
<form class="form" data-form="Get Featured (quick)" data-success="Thanks! An editor will email you within 2 business days with next steps and availability.">
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
<label>Name<input name="name" required autocomplete="name"></label>
<label>Email<input type="email" name="email" required autocomplete="email"></label>
<label>What should we know?<select name="interest" required><option value="">Choose…</option><option>Founder / startup story</option><option>Creator / influencer profile</option><option>Professional / expert interview</option><option>Nonprofit / community hero</option><option>Brand partnership</option></select></label>
<button class="btn btn-primary btn-block" type="submit">Get my feature plan →</button>
<p class="fine">No obligation. We reply within 2 business days.</p></form></div>
</div></div></section>'''

def support_ask():
    return '''<div class="support-ask"><h3 style="margin-top:0">Stories like this are free because readers like you chip in.</h3>
<p>People.Media is independent. Your support funds reporting, video production, contest prizes and paying contributors. Every contribution — big or small — keeps real people's stories in the spotlight.</p>
<div class="pill-row"><a class="btn btn-primary" href="support.html">Support People.Media</a><a class="btn btn-ghost" href="support.html#monthly">Become a monthly supporter</a></div></div>'''

# ---------------------------------------------------------------- HOME
def build_home():
    feat = ARTICLES[0]
    cards = "".join(story_card(a) for a in ARTICLES[1:7])
    people = "".join(person_card(p) for p in PEOPLE[:4])
    body = f'''
<section class="hero"><div class="wrap hero-grid">
<div><span class="eyebrow">● The people-powered media network</span>
<h1>Every person is a <em>story</em> worth telling.</h1>
<p class="lead">People.Media celebrates everyday heroes, creators, founders and changemakers — with original stories, video, live birthdays, contests and a stage for your own story.</p>
<div class="hero-cta"><a class="btn btn-primary" href="submit.html">Share your story</a><a class="btn btn-ghost" href="get-featured.html">Get featured</a><a class="btn btn-ghost" href="stories.html">Read stories</a></div>
<div class="hero-stats"><span><b>{len(ARTICLES)}</b>original guides</span><span><b>{len(PEOPLE)-1}</b>people profiles</span><span><b>Daily</b>live updates</span><span><b>Monthly</b>contests &amp; prizes</span></div></div>
<div class="mosaic" aria-hidden="true">
<div class="tile gr1"><span>Founders</span></div><div class="tile gr2"><span>Creators</span></div><div class="tile gr4"><span>Teachers</span></div>
<div class="tile gr5"><span>Artists</span></div><div class="tile gr6"><span>Neighbours</span></div><div class="tile gr7"><span>You?</span></div></div>
</div></section>

<section style="padding-top:10px"><div class="wrap grid g2">
<a class="card fade" href="story-{feat['slug']}.html" style="text-decoration:none">
<div class="card-media {feat['gr']}" style="aspect-ratio:16/8">Featured guide</div>
<div class="card-body"><div class="meta"><span class="tag coral">{feat['tag']}</span><span>{feat['mins']} min read</span></div><h2 style="font-size:1.8rem;margin:0">{E(feat['title'])}</h2><p>{E(feat['dek'])}</p></div></a>
<div class="grid" style="gap:16px">
<div class="kpi fade"><span class="eyebrow">Born today · <span data-today></span></span><div id="bornToday" class="born" data-limit="4"><p class="fine">Loading today's birthdays…</p></div><p class="fine" style="margin-top:10px">Live from Wikipedia's public "On this day" feed.</p></div>
</div></div></section>

<section class="alt"><div class="wrap">
<div class="sec-head"><div><h2>Latest stories &amp; guides</h2><p>Original, practical reads on storytelling, personal brand, creators and community.</p></div><a class="btn btn-ghost" href="stories.html">All stories →</a></div>
<div class="grid g3">{cards}</div></div></section>

<section><div class="wrap">
<div class="sec-head"><div><h2>Trending people</h2><p>Boost the people who inspire you — the community decides who trends.</p></div><a class="btn btn-ghost" href="people.html">All profiles →</a></div>
<div class="grid g4" data-sort-boost>{people}</div></div></section>

<section class="dark"><div class="wrap">
<div class="sec-head"><div><h2 style="color:#fff">Watch: stories that move</h2><p>Hand-picked talks and human stories, refreshed automatically several times a day.</p></div><a class="btn btn-primary" href="videos.html">Video hub →</a></div>
<div class="grid g3" id="videoGrid" data-limit="3"><p>Loading videos…</p></div></div></section>

{cta_featured()}

<section class="alt"><div class="wrap grid g2" style="align-items:start">
<div class="fade"><span class="eyebrow">This month's contest</span><h2>Theme: “The Day Everything Changed”</h2>
<p>Tell a true story in 300–1,000 words or a video under 3 minutes. Winners are published, promoted to our community and share a prize pool funded by sponsors and supporters.</p>
<div class="countdown" data-countdown=""><div><b>00</b><small>days</small></div><div><b>00</b><small>hrs</small></div><div><b>00</b><small>min</small></div><div><b>00</b><small>sec</small></div></div>
<div class="pill-row mt"><a class="btn btn-primary" href="contests.html#enter">Enter the contest</a><a class="btn btn-ghost" href="advertise.html#sponsor-contest">Sponsor a prize</a></div></div>
<div class="fade"><span class="eyebrow">Good news around the web</span><h2>Today's uplifting headlines</h2><div class="ticker" id="headlines" data-limit="6">{headlines_html(6)}</div><p class="fine mt">Headlines link to the original publishers. Auto-refreshed.</p></div>
</div></section>

<section><div class="wrap grid g3">
<div class="kpi fade"><h3>📣 Share your story</h3><p>Free editorial consideration for real stories of courage, creativity and community.</p><a class="btn btn-ghost btn-sm" href="submit.html">Submit</a></div>
<div class="kpi fade"><h3>🏆 Nominate a hero</h3><p>Help us find the 2027 People.Media 100 — everyday people making an outsized difference.</p><a class="btn btn-ghost btn-sm" href="people-100.html">Nominate</a></div>
<div class="kpi fade"><h3>💛 Support independent stories</h3><p>Fund contributor pay, video production and prizes. Monthly supporters get perks.</p><a class="btn btn-primary btn-sm" href="support.html">Support</a></div>
</div></section>

<section class="alt"><div class="wrap center"><h2>The weekly dose of good people</h2><p class="lead" style="margin:0 auto 18px">Five stories, one creator tip and every new contest — Fridays. Free forever.</p><div style="max-width:560px;margin:0 auto">{newsletter_form(src="home")}</div></div></section>
'''
    page("index.html", f"{NAME} — {TAGLINE}", "People.Media is a people-powered media platform: inspiring human stories, people profiles, creator guides, videos, monthly contests and a stage to share your own story or get featured.", body, "index.html")

# ---------------------------------------------------------------- STORIES
def build_stories():
    cats = [("all","All"),("storytelling","Storytelling"),("career","Career & Brand"),("creators","Creators"),("community","Community"),("video","Video"),("inspiration","Inspiration")]
    chips = "".join(f'<button class="chip{" active" if c=="all" else ""}" data-cat="{c}">{t}</button>' for c,t in cats)
    cards = "".join(story_card(a) for a in ARTICLES)
    body = f'''<section class="article-hero"><div class="wrap"><span class="eyebrow">Stories &amp; guides</span><h1>Stories worth your time</h1><p class="lead">Original, practical reads on telling stories, building a reputation, earning as a creator and strengthening communities.</p></div></section>
<section style="padding-top:0"><div class="wrap" data-filter-scope>
<div class="toolbar"><input class="search" type="search" placeholder="Search stories…" aria-label="Search stories">{chips}</div>
<div class="grid g3">{cards}</div><p data-empty style="display:none" class="center fine mt">No stories match — try another search.</p>
</div></section>{cta_featured()}'''
    page("stories.html", f"Stories & Guides — {NAME}", "Original storytelling guides, personal branding playbooks, creator economy explainers and community stories from People.Media.", body, "stories.html")

def build_article(a, idx):
    nxt = ARTICLES[(idx + 1) % len(ARTICLES)]; prv = ARTICLES[idx - 1]
    rel = "".join(story_card(x) for x in ARTICLES if x["slug"] != a["slug"] and x["cat"] == a["cat"])[:0] or "".join(story_card(x) for x in [nxt, prv, ARTICLES[(idx + 2) % len(ARTICLES)]])
    ld = {"@context":"https://schema.org","@type":"Article","headline":a["title"],"description":a["dek"],"datePublished":a["date"],"dateModified":a["date"],"author":{"@type":"Organization","name":NAME+" Editorial"},"publisher":{"@type":"Organization","name":NAME,"logo":{"@type":"ImageObject","url":SITE+"/assets/img/favicon.svg"}},"mainEntityOfPage":SITE+"/story-"+a["slug"]+".html"}
    body = f'''<article><header class="article-hero"><div class="wrap"><div class="article">
<div class="breadcrumbs"><a href="index.html">Home</a> / <a href="stories.html">Stories</a> / {E(a['tag'])}</div>
<span class="tag coral">{E(a['tag'])}</span><h1 style="margin-top:12px;font-size:clamp(2rem,4vw,3rem)">{E(a['title'])}</h1><p class="lead" style="max-width:none">{E(a['dek'])}</p>
<div class="byline"><span>By People.Media Editorial</span>·<time datetime="{a['date']}">{datetime.date.fromisoformat(a['date']).strftime('%d %B %Y')}</time>·<span>{a['mins']} min read</span></div>
</div></div></header>
<div class="wrap"><div class="article">
<div class="card-media {a['gr']}" style="border-radius:var(--radius);aspect-ratio:21/9">{E(a['tag'])}</div>
<div class="share"><button class="btn btn-ghost btn-sm" data-share="x">Share on X</button><button class="btn btn-ghost btn-sm" data-share="li">LinkedIn</button><button class="btn btn-ghost btn-sm" data-share="wa">WhatsApp</button><button class="btn btn-ghost btn-sm" data-share="fb">Facebook</button><button class="btn btn-ghost btn-sm" data-share="copy">Copy link</button></div>
<div class="prose">{a['body']}</div>
{support_ask()}
<div class="form-card"><h3 style="margin-top:0">Get the next guide in your inbox</h3>{newsletter_form(src="article-"+a['slug'])}</div>
</div></div></article>
<section class="alt mt"><div class="wrap"><h2>Keep reading</h2><div class="grid g3">{rel}</div></div></section>'''
    page(f"story-{a['slug']}.html", f"{a['title']} — {NAME}", a["dek"], body, "stories.html", ld, "article")

# ---------------------------------------------------------------- PEOPLE
def build_people():
    cats = [("all","All"),("changemakers","Changemakers"),("leaders","Leaders"),("scientists","Scientists"),("artists","Artists"),("athletes","Athletes")]
    chips = "".join(f'<button class="chip{" active" if c=="all" else ""}" data-cat="{c}">{t}</button>' for c,t in cats)
    cards = "".join(person_card(p) for p in PEOPLE)
    body = f'''<section class="article-hero"><div class="wrap"><span class="eyebrow">People profiles</span><h1>People who changed the story</h1><p class="lead">Short, fact-checked profiles of remarkable lives — and a growing directory of everyday changemakers nominated by our community.</p></div></section>
<section style="padding-top:0"><div class="wrap" data-filter-scope>
<div class="toolbar"><input class="search" type="search" placeholder="Search people…" aria-label="Search people">{chips}</div>
<div class="grid g4">{cards}</div><p data-empty style="display:none" class="center fine mt">No one matches — try another search.</p>
</div></section>
<section class="alt"><div class="wrap grid g2" style="align-items:center"><div><h2>Born today</h2><p>Live birthdays of notable people from Wikipedia's public feed, updated every day automatically. <span data-today></span>.</p><a class="btn btn-primary" href="people-100.html">Nominate an everyday hero</a></div><div id="bornToday" class="born" data-limit="8"><p class="fine">Loading…</p></div></div></section>{cta_featured()}'''
    page("people.html", f"People Profiles — {NAME}", "Fact-checked profiles of remarkable people, live birthdays and a community directory of everyday changemakers on People.Media.", body, "people.html")

def build_person(p):
    if p["slug"] == "nominate-your-hero":
        return
    ld = {"@context":"https://schema.org","@type":"ProfilePage","mainEntity":{"@type":"Person","name":p["name"],"birthDate":p["born"],"deathDate":p["died"] or None,"description":p["summary"]}}
    body = f'''<article><header class="article-hero"><div class="wrap"><div class="article">
<div class="breadcrumbs"><a href="index.html">Home</a> / <a href="people.html">People</a> / {E(p['name'])}</div>
<span class="tag teal">{E(p['role'])}</span><h1 style="margin-top:12px">{E(p['name'])}</h1><p class="lead" style="max-width:none">{E(p['summary'])}</p>
<div class="pill-row"><button class="boost" data-boost="{p['slug']}" data-base="0">▲ Boost <b>0</b></button><button class="btn btn-ghost btn-sm" data-share="native">Share</button><button class="btn btn-ghost btn-sm" data-share="copy">Copy link</button></div>
</div></div></header>
<div class="wrap"><div class="article">
<div class="facts"><dl><dt>Known for</dt><dd>{E(p['known'])}</dd><dt>Born</dt><dd>{E(p['born'])}</dd>{f"<dt>Died</dt><dd>{E(p['died'])}</dd>" if p['died'] else ""}<dt>Country</dt><dd>{E(p['country'])}</dd></dl></div>
<div class="prose">{p['body']}</div>
<p class="fine">Profile written by People.Media Editorial from widely documented public sources. Spotted an error? <a href="contact.html">Tell us</a> — see our <a href="editorial-policy.html">corrections policy</a>.</p>
{support_ask()}</div></div></article>
<section class="alt"><div class="wrap"><h2>More people</h2><div class="grid g4">{"".join(person_card(x) for x in PEOPLE if x['slug']!=p['slug'])[:0] or "".join(person_card(x) for x in [q for q in PEOPLE if q['slug']!=p['slug']][:4])}</div></div></section>'''
    page(f"person-{p['slug']}.html", f"{p['name']}: {p['role']} — {NAME}", p["summary"], body, "people.html", ld, "profile")

# ---------------------------------------------------------------- VIDEOS
def build_videos():
    body = '''<section class="article-hero"><div class="wrap"><span class="eyebrow">Video hub</span><h1>Stories you can watch</h1><p class="lead">Talks and human stories from leading channels, refreshed automatically. Tap any video to play it right here.</p><p class="fine" data-videos-updated></p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="grid g3" id="videoGrid" data-limit="24"><p>Loading videos…</p></div></div></section>
<section class="alt"><div class="wrap grid g2" style="align-items:center"><div><h2>Make a video story</h2><p>Learn to shoot a documentary-style portrait on your phone, then enter it in our monthly contest.</p><div class="pill-row"><a class="btn btn-primary" href="story-phone-documentary-portrait.html">Read the guide</a><a class="btn btn-ghost" href="contests.html">See contests</a></div></div>
<div class="form-card"><h3 style="margin-top:0">Suggest a video or channel</h3><form class="form" data-form="Video suggestion" data-success="Thanks! Our editors review suggestions weekly.">
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off"><label>YouTube link<input type="url" name="video_url" required placeholder="https://www.youtube.com/watch?v=…"></label><label>Why should people watch it?<textarea name="why" required></textarea></label><label>Your email<input type="email" name="email" required></label><button class="btn btn-primary" type="submit">Suggest</button></form></div></div></section>'''
    page("videos.html", f"Video Stories — {NAME}", "Watch inspiring talks and human stories on People.Media's auto-updated video hub.", body, "videos.html")

# ---------------------------------------------------------------- GET FEATURED (lead gen)
PACKAGES = [
    ("spotlight","Spotlight","$149","one-time","A clean, editor-polished profile from your answers to our questionnaire.",["Questionnaire-based profile (500–700 words)","Permanent page with up to 3 links","1 photo, SEO title &amp; description","\"As featured\" badge","Delivered in 7 business days"],False),
    ("feature","Feature Interview","$399","one-time","A real interview with an editor, written as a story people want to read.",["30-min recorded interview","900–1,400 word feature story","Up to 5 photos + 1 embedded video","Newsletter mention + 2 social posts","Badge, press-kit PDF of your feature"],True),
    ("signature","Signature Story","$999","one-time","Our premium package for founders, brands and public figures.",["Two interviews + research","1,500–2,500 word cover story","Homepage placement for 7 days","Dedicated newsletter + video short","Priority 5-day turnaround"],False),
]
def build_featured():
    cards = ""
    for k,t,pr,per,desc,feats,pop in PACKAGES:
        cards += f'''<div class="price-card fade{" pop" if pop else ""}">{'<span class="badge">Most popular</span>' if pop else ""}<h3 style="margin:0">{t}</h3><div class="price">{pr} <small>{per}</small></div><p class="fine">{desc}</p><ul class="checks light-checks">{"".join(f"<li>{f}</li>" for f in feats)}</ul><a class="btn {"btn-primary" if pop else "btn-ghost"} btn-block" href="get-featured.html?package={k}#apply">Choose {t}</a></div>'''
    opts = "".join(f'<button type="button" class="opt" data-v="{k}">{t}<small>{pr}</small></button>' for k,t,pr,*_ in PACKAGES) + '<button type="button" class="opt" data-v="not-sure">Not sure yet<small>Help me choose</small></button>'
    body = f'''<section class="hero"><div class="wrap hero-grid"><div><span class="eyebrow">Get featured</span><h1>Be the story people <em>remember</em>.</h1>
<p class="lead">A professionally written People.Media feature gives you independent, shareable credibility — for fundraising, sales, hiring, speaking and press.</p>
<div class="hero-cta"><a class="btn btn-primary" href="#apply">Apply in 2 minutes</a><a class="btn btn-ghost" href="#packages">Compare packages</a></div>
<ul class="checks light-checks"><li>Editor-written — you approve facts before publishing</li><li>Permanent, mobile-fast, search-optimized page</li><li>Transparent labelling: paid features are marked "Partner Feature"</li></ul></div>
<div class="form-card fade"><h3 style="margin-top:0">Who we feature</h3><div class="grid g2" style="gap:10px"><div class="kpi">🚀 Founders &amp; startups</div><div class="kpi">🎥 Creators &amp; influencers</div><div class="kpi">🎓 Experts &amp; professionals</div><div class="kpi">🤝 Nonprofits &amp; local heroes</div><div class="kpi">🎨 Artists &amp; authors</div><div class="kpi">🏢 Brands with a human story</div></div></div></div></section>

<section class="alt" id="packages"><div class="wrap"><div class="sec-head"><div><h2>Feature packages</h2><p>Simple, one-time pricing. No subscriptions. Free editorial submissions remain open to everyone.</p></div></div><div class="grid g3">{cards}</div>
<p class="fine center mt">Agencies &amp; bulk features: <a href="#apply">ask for volume pricing</a>. Prices in USD; local currency invoicing available.</p></div></section>

<section><div class="wrap grid g3">
<div class="kpi fade"><b>1</b><h3>Apply</h3><p>Tell us about you in two minutes. No payment to apply.</p></div>
<div class="kpi fade"><b>2</b><h3>Interview</h3><p>An editor sends a questionnaire or schedules your interview.</p></div>
<div class="kpi fade"><b>3</b><h3>Publish &amp; share</h3><p>Approve facts, go live, get your badge and share kit.</p></div></div></section>

<section class="alt" id="apply"><div class="wrap grid g2" style="align-items:start">
<div><span class="eyebrow">Apply now</span><h2>Start your feature</h2><p>Applying is free. We reply within 2 business days with a feature plan and payment link only if we're a good fit.</p>
<details><summary>Is a paid feature an advertisement?</summary><p>Paid features are clearly labelled "Partner Feature" in line with advertising disclosure standards. Editorial independence is kept: we fact-check and may decline stories that are misleading.</p></details>
<details><summary>Can I review before publishing?</summary><p>Yes — you review for factual accuracy. Our editors keep final say over style and structure.</p></details>
<details><summary>What if I'm not accepted?</summary><p>You pay nothing. We'll explain why and suggest a free submission or a better-fit package.</p></details>
<details><summary>How long does the page stay live?</summary><p>Permanently, as long as People.Media operates, unless you ask us to remove it.</p></details>
<details><summary>Can my company pay and get an invoice?</summary><p>Yes. We provide invoices for businesses on request.</p></details></div>
<div class="form-card" data-steps>
<div class="steps"><span></span><span></span><span></span></div>
<form class="form" data-form="Get Featured application" data-success="Application received! An editor will email your feature plan within 2 business days.">
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
<div class="step"><h3 style="margin:0">1 · Choose a package</h3><div class="opt-grid" data-choice data-required><input type="hidden" name="package">{opts}</div>
<label>I am a…<select name="profile_type" required><option value="">Choose…</option><option>Founder / business owner</option><option>Creator / influencer</option><option>Expert / professional</option><option>Nonprofit / community leader</option><option>Artist / author</option><option>Agency (on behalf of a client)</option></select></label>
<button type="button" class="btn btn-primary" data-next>Continue →</button></div>
<div class="step"><h3 style="margin:0">2 · Your story</h3>
<label>Headline of your story (one line)<input name="headline" required placeholder="e.g., From a 2-person garage to 40 jobs in our town"></label>
<label>What makes it worth reading?<textarea name="story" required placeholder="The moment, the obstacle, the change…"></textarea></label>
<label>Links (website, socials, press)<input name="links" placeholder="https://"></label>
<div class="pill-row"><button type="button" class="btn btn-ghost" data-prev>← Back</button><button type="button" class="btn btn-primary" data-next>Continue →</button></div></div>
<div class="step"><h3 style="margin:0">3 · Contact</h3>
<div class="row"><label>Full name<input name="name" required autocomplete="name"></label><label>Email<input type="email" name="email" required autocomplete="email"></label></div>
<div class="row"><label>Phone / WhatsApp (optional)<input name="phone" autocomplete="tel"></label><label>Country<input name="country" autocomplete="country-name"></label></div>
<label>Timeline<select name="timeline"><option>As soon as possible</option><option>Within 30 days</option><option>Within 90 days</option><option>Just exploring</option></select></label>
<label class="consent"><input type="checkbox" required name="consent" value="yes"> I agree to be contacted about my application and accept the <a href="privacy.html">Privacy Policy</a>.</label>
<div class="pill-row"><button type="button" class="btn btn-ghost" data-prev>← Back</button><button class="btn btn-primary" type="submit">Submit application ✓</button></div></div>
</form></div></div></section>'''
    page("get-featured.html", f"Get Featured on {NAME} — Professional Profiles & Interviews", "Get a professionally written profile or interview on People.Media. Credible, permanent, search-optimized features for founders, creators, experts and nonprofits.", body, "get-featured.html")

# ---------------------------------------------------------------- ADVERTISE / SPONSOR / PARTNER
def build_advertise():
    tiers = [("Newsletter Sponsor","from $250 / issue",["Top placement in People.Media Weekly","Logo, 60-word message, link","Clearly labelled \"Sponsored\""]),
             ("Branded Story Series","from $2,500 / series",["3–5 human-interest stories on a theme you care about","Editorial standards, labelled \"Presented by\"","Video short + social distribution"]),
             ("Contest Prize Sponsor","from $500 / month",["Your brand on a monthly contest","Prize presentation + winner story","Lead list of opted-in participants (with consent)"]),
             ("Category Sponsor","from $1,000 / month",["Own a section (e.g., Founders or Creators)","Native placements across the section","Quarterly performance report"])]
    cards = "".join(f'<div class="price-card fade"><h3 style="margin:0">{t}</h3><div class="price" style="font-size:1.5rem">{p}</div><ul class="checks light-checks">{"".join(f"<li>{x}</li>" for x in f)}</ul></div>' for t,p,f in tiers)
    body = f'''<section class="hero"><div class="wrap hero-grid"><div><span class="eyebrow">Advertise · Sponsor · Partner</span><h1>Put your brand next to <em>good people</em>.</h1><p class="lead">Reach readers who come to People.Media for stories of courage, creativity and community — a brand-safe, positive environment.</p><div class="hero-cta"><a class="btn btn-primary" href="#enquire">Request the media kit</a><a class="btn btn-ghost" href="{INQUIRY_URL}" target="_blank" rel="noopener">Domain / acquisition enquiries</a></div></div>
<div class="form-card fade"><h3 style="margin-top:0">Why People.Media</h3><ul class="checks light-checks"><li>Brand-safe, uplifting editorial environment</li><li>Native formats that respect readers</li><li>Transparent labelling builds trust (and performance)</li><li>Contest &amp; community integrations for real engagement</li></ul></div></div></section>
<section class="alt"><div class="wrap"><h2>Sponsorship formats</h2><div class="grid g4">{cards}</div><p class="fine mt">Display advertising on this site is served by Google AdSense. Direct sponsorships are separate and always labelled.</p></div></section>
<section id="partner"><div class="wrap grid g3"><div class="kpi fade"><h3>Media partners</h3><p>Content syndication and co-produced series with publishers and podcasts.</p></div><div class="kpi fade"><h3>Nonprofits &amp; NGOs</h3><p>Amplify beneficiaries' stories with consent-first storytelling and fundraising links.</p></div><div class="kpi fade" id="sponsor-contest"><h3>Brands &amp; employers</h3><p>Sponsor prizes, employee-story series or scholarships in your name.</p></div></div></section>
<section class="alt" id="enquire"><div class="wrap grid g2" style="align-items:start"><div><h2>Request the media kit</h2><p>Tell us your goals and budget range. We'll send our current audience numbers, rates and availability within 2 business days.</p><p>Interested in acquiring or partnering on the People.Media website or domain itself? <a href="{INQUIRY_URL}" target="_blank" rel="noopener">Contact our team</a>.</p></div>
<div class="form-card"><form class="form" data-form="Advertising / sponsorship enquiry" data-success="Thanks! We'll send the media kit and availability within 2 business days.">
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
<div class="row"><label>Name<input name="name" required></label><label>Work email<input type="email" name="email" required></label></div>
<div class="row"><label>Company<input name="company" required></label><label>Website<input name="website" type="url" placeholder="https://"></label></div>
<label>Interested in<select name="interest" required><option value="">Choose…</option><option>Newsletter sponsorship</option><option>Branded story series</option><option>Contest prize sponsorship</option><option>Category sponsorship</option><option>Partnership / syndication</option><option>Website / domain acquisition</option><option>Other</option></select></label>
<label>Monthly budget<select name="budget"><option>Under $500</option><option>$500–$2,000</option><option>$2,000–$10,000</option><option>$10,000+</option></select></label>
<label>Goals<textarea name="message" required></textarea></label>
<label class="consent"><input type="checkbox" required name="consent" value="yes"> I agree to the <a href="privacy.html">Privacy Policy</a>.</label>
<button class="btn btn-primary" type="submit">Send enquiry</button></form></div></div></section>'''
    page("advertise.html", f"Advertise, Sponsor & Partner — {NAME}", "Sponsor newsletters, branded story series, contest prizes and categories on People.Media, or enquire about partnerships.", body, "advertise.html")

# ---------------------------------------------------------------- CONTESTS
def build_contests():
    body = f'''<section class="hero"><div class="wrap hero-grid"><div><span class="eyebrow">Monthly story contest</span><h1>Tell it true. <em>Win</em> big.</h1><p class="lead">Every month we pick a theme. You tell a true story — in writing or on video. Judges and the community pick winners who get published, promoted and paid.</p>
<div class="countdown" data-countdown=""><div><b>00</b><small>days</small></div><div><b>00</b><small>hrs</small></div><div><b>00</b><small>min</small></div><div><b>00</b><small>sec</small></div></div>
<div class="hero-cta"><a class="btn btn-primary" href="#enter">Enter now — free</a><a class="btn btn-ghost" href="advertise.html#sponsor-contest">Sponsor a prize</a></div></div>
<div class="form-card fade"><span class="eyebrow">Current theme</span><h2 style="margin:0">“The Day Everything Changed”</h2><p>A single day that split your life into before and after — a call, a meeting, a mistake, a kindness.</p><div class="facts" style="margin:0"><dl><dt>Formats</dt><dd>Written (300–1,000 words) or video (≤ 3 min)</dd><dt>Entry fee</dt><dd>Free</dd><dt>Prize pool</dt><dd>Funded by sponsors &amp; supporters — announced on this page</dd><dt>Closes</dt><dd>31 December 2026, 23:59 (IST)</dd></dl></div></div></div></section>
<section class="alt"><div class="wrap grid g3">
<div class="price-card fade"><span class="badge">1st</span><h3>Grand Winner</h3><p>Cash prize from the pool, a Signature Story feature, homepage placement and a winner badge.</p></div>
<div class="price-card fade"><span class="badge">2nd</span><h3>Runner-up</h3><p>Cash prize, Feature Interview package and newsletter spotlight.</p></div>
<div class="price-card fade"><span class="badge">★</span><h3>Community Choice</h3><p>Chosen by reader boosts on shortlisted entries. Prize plus a Spotlight profile.</p></div></div></section>
<section><div class="wrap grid g2"><div><h2>Judging criteria</h2><ul class="checks light-checks"><li><b>Truth &amp; specificity (30%)</b> — real, vivid, verifiable</li><li><b>Story craft (30%)</b> — moment, obstacle, change</li><li><b>Emotional impact (25%)</b> — does it stay with you?</li><li><b>Theme fit (15%)</b></li></ul><p class="fine">Shortlists are reviewed by People.Media editors and guest judges. Community Choice votes are reviewed for fraud before results are announced.</p></div>
<div><h2>Rules in brief</h2><ul><li>Open worldwide to individuals 18+ (under-18s may enter with guardian consent in Youth categories when announced).</li><li>One entry per person per month. Must be your own original work and a true story.</li><li>You keep copyright; you grant People.Media a non-exclusive licence to publish and promote your entry.</li><li>No purchase necessary. Void where prohibited. Prizes are paid within 30 days of announcement.</li><li>Full terms are in our <a href="terms.html#contests">Terms of Use</a>.</li></ul></div></div></section>
<section class="alt" id="enter"><div class="wrap grid g2" style="align-items:start"><div><h2>Enter the contest</h2><p>Paste your story or a link to your video (YouTube unlisted, Google Drive or Dropbox). We confirm every entry by email.</p><p>Need help? Read <a href="story-how-to-tell-your-story.html">How to Tell Your Life Story</a> and <a href="story-phone-documentary-portrait.html">Shoot a Video Portrait on Your Phone</a>.</p></div>
<div class="form-card"><form class="form" data-form="Contest entry" data-success="Your entry is in! Watch your inbox for confirmation and shortlist news.">
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off"><input type="hidden" name="contest" value="The Day Everything Changed">
<div class="row"><label>Full name<input name="name" required></label><label>Email<input type="email" name="email" required></label></div>
<div class="row"><label>Country<input name="country" required></label><label>Format<select name="format" required><option>Written story</option><option>Video story</option></select></label></div>
<label>Title<input name="title" required></label>
<label>Your story (or video link)<textarea name="entry" required style="min-height:200px"></textarea></label>
<label class="consent"><input type="checkbox" required name="original" value="yes"> This is my original, true story and I accept the contest rules.</label>
<label class="consent"><input type="checkbox" name="newsletter" value="yes"> Send me future contest themes (optional).</label>
<button class="btn btn-primary" type="submit">Submit entry</button></form></div></div></section>'''
    page("contests.html", f"Story Contests & Prizes — {NAME}", "Enter People.Media's free monthly true-story contest. Written or video entries, judged on craft and impact, with prizes, publication and promotion.", body, "contests.html")

# ---------------------------------------------------------------- SUPPORT / DONATE
def build_support():
    body = f'''<section class="hero"><div class="wrap hero-grid"><div><span class="eyebrow">Support People.Media</span><h1>Keep real people in the <em>spotlight</em>.</h1><p class="lead">We're independent. Reader support pays contributors, funds video, finances contest prizes, and lets us hire storytellers from the communities we cover.</p>
<div class="progress" data-goal><i></i></div><p class="fine" data-goal-label></p>
<div class="impact mt"><div><b>$10</b><span>covers a contributor's interview recording &amp; transcription</span></div><div><b>$50</b><span>funds a reader-nominated hero's profile, start to finish</span></div><div><b>$250</b><span>adds a cash prize to a monthly contest</span></div><div><b>$1,000</b><span>funds a mini-documentary about an everyday changemaker</span></div></div></div>
<div class="form-card fade" id="donate"><h3 style="margin-top:0">Choose your support</h3>
<div class="seg" role="tablist"><button class="" data-f="once">One-time</button><button class="on" data-f="monthly" id="monthly">Monthly</button><button data-f="yearly">Yearly</button></div>
<div class="amounts mt" id="amounts"></div>
<label class="mt">Other amount<input id="otherAmt" type="number" min="1" inputmode="decimal" placeholder="Enter amount"></label>
<p style="margin:12px 0"><strong>Your support:</strong> <span id="donSummary"></span></p>
<div id="payLinks" class="pill-row"></div>
<form class="form mt" data-form="Donation pledge" data-success="Thank you! We'll email a secure payment link and your supporter welcome pack within 1 business day.">
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off"><input type="hidden" name="amount" id="donAmount"><input type="hidden" name="frequency" id="donFreq">
<label>Direct my support to<select name="purpose"><option>Where it's needed most (operations)</option><option>Paying contributors &amp; hiring talent</option><option>Contest prizes</option><option>Video production</option><option>Promotion &amp; marketing of featured stories</option><option>Micro-grants for storytellers</option></select></label>
<div class="row"><label>Name<input name="name" required></label><label>Email<input type="email" name="email" required></label></div>
<label class="consent"><input type="checkbox" name="supporter_wall" value="yes"> List my first name on the Supporter Wall</label>
<button class="btn btn-primary btn-block" type="submit">Pledge my support →</button>
<p class="fine">People.Media is not a registered charity; contributions are not tax-deductible. You'll receive a secure payment link from us — we never ask for card details by email.</p></form></div></div></section>
<section class="alt"><div class="wrap"><h2>Supporter perks</h2><div class="grid g4">
<div class="price-card fade"><h3>Friend</h3><div class="price">$5<small>/mo</small></div><ul class="checks light-checks"><li>Supporter-only newsletter</li><li>Name on Supporter Wall</li></ul></div>
<div class="price-card fade pop"><span class="badge">Best value</span><h3>Insider</h3><div class="price">$10<small>/mo</small></div><ul class="checks light-checks"><li>All Friend perks</li><li>Early contest themes</li><li>Vote on next story series</li></ul></div>
<div class="price-card fade"><h3>Patron</h3><div class="price">$50<small>/mo</small></div><ul class="checks light-checks"><li>All Insider perks</li><li>"Made possible by" credit on a story</li><li>Quarterly editorial call</li></ul></div>
<div class="price-card fade"><h3>Founding Circle</h3><div class="price">$1,000<small> once</small></div><ul class="checks light-checks"><li>Lifetime Patron perks</li><li>Founding Circle page credit</li><li>Name a contest prize</li></ul></div></div></div></section>
<section><div class="wrap grid g2"><div><h2>Where the money goes</h2><p>We publish an annual transparency note. Planned allocation of reader support:</p><div class="facts"><dl><dt>45%</dt><dd>Contributor pay, interviews &amp; hiring storytellers</dd><dt>20%</dt><dd>Contest prizes &amp; micro-grants</dd><dt>15%</dt><dd>Video production</dd><dt>12%</dt><dd>Promotion &amp; marketing of featured stories</dd><dt>8%</dt><dd>Hosting, tools &amp; operations</dd></dl></div></div>
<div><h2>Supporter Wall</h2><p class="fine">Founding supporters appear here (first names only, with permission).</p><div class="wall"><span>Your name could be first ✨</span></div>
<h2 class="mt">Other ways to help</h2><ul><li><a href="submit.html">Share a story</a> or <a href="people-100.html">nominate a hero</a></li><li><a href="careers.html">Volunteer or join the team</a></li><li>Share our stories with a friend</li><li>Corporate matching &amp; sponsorship: <a href="advertise.html#enquire">talk to us</a></li></ul></div></div></section>'''
    page("support.html", f"Support & Donate — {NAME}", "Support independent, people-powered storytelling. One-time, monthly or yearly contributions fund contributors, video, contest prizes and promotion on People.Media.", body, "support.html")

# ---------------------------------------------------------------- CAREERS (hiring talent)
def build_careers():
    roles = [("Contributing Writer (freelance)","Remote · paid per story","Interview and write 800–1,500 word human-interest profiles."),
             ("Video Storyteller (freelance)","Remote · paid per video","Shoot and edit 1–3 minute documentary portraits on phone or camera."),
             ("Community Ambassador","Remote · volunteer + perks","Find nominees and stories in your city; host local storytelling meetups."),
             ("Social Media Editor (part-time)","Remote · contract","Turn stories into short-form video and carousels; grow our channels."),
             ("Partnerships &amp; Sponsorship Lead","Remote · commission-based","Bring brands, nonprofits and employers into sponsored series and prizes."),
             ("Translator / Localization Volunteer","Remote · volunteer","Help stories reach readers in Hindi, Spanish, Arabic, French and more.")]
    cards = "".join(f'<article class="card fade"><div class="card-body"><span class="tag teal">{l}</span><h3>{t}</h3><p>{d}</p><a class="btn btn-ghost btn-sm" href="#apply" style="align-self:start">Apply</a></div></article>' for t,l,d in roles)
    body = f'''<section class="article-hero"><div class="wrap"><span class="eyebrow">Careers &amp; talent</span><h1>Tell stories that matter — with us</h1><p class="lead">We're building a global network of storytellers. Freelance, part-time and volunteer roles, fully remote.</p></div></section>
<section style="padding-top:0"><div class="wrap grid g3">{cards}</div></section>
<section class="alt" id="apply"><div class="wrap grid g2" style="align-items:start"><div><h2>Apply</h2><p>Send us your details and two samples of your work. We review applications on a rolling basis and reply to every applicant.</p><p class="fine">People.Media is an equal-opportunity platform. We welcome storytellers of every background, especially from communities rarely covered by mainstream media.</p></div>
<div class="form-card"><form class="form" data-form="Talent application" data-success="Application received — we review weekly and will be in touch.">
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
<div class="row"><label>Full name<input name="name" required></label><label>Email<input type="email" name="email" required></label></div>
<div class="row"><label>Role<select name="role" required><option value="">Choose…</option>{"".join(f"<option>{t}</option>" for t,_,_ in roles)}<option>Other / open application</option></select></label><label>City &amp; country<input name="location" required></label></div>
<label>Portfolio / sample links<textarea name="samples" required placeholder="Two links to your best work"></textarea></label>
<label>Why People.Media?<textarea name="message"></textarea></label>
<label class="consent"><input type="checkbox" required name="consent" value="yes"> I agree to the <a href="privacy.html">Privacy Policy</a>.</label>
<button class="btn btn-primary" type="submit">Send application</button></form></div></div></section>'''
    page("careers.html", f"Careers, Freelance & Volunteer Roles — {NAME}", "Join People.Media as a freelance writer, video storyteller, ambassador, social editor or partnerships lead. Remote roles worldwide.", body, "careers.html")

# ---------------------------------------------------------------- SUBMIT / NOMINATE
def nominate_form(src):
    return f'''<form class="form" data-form="People.Media 100 nomination" data-success="Nomination received! We'll contact you if we need more details.">
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off"><input type="hidden" name="source" value="{src}">
<div class="row"><label>Nominee's name<input name="nominee" required></label><label>Nominee's city &amp; country<input name="nominee_location" required></label></div>
<label>Category<select name="category" required><option value="">Choose…</option><option>Community hero</option><option>Founder / entrepreneur</option><option>Creator / artist</option><option>Teacher / mentor</option><option>Health &amp; care</option><option>Environment</option><option>Youth (18–25)</option></select></label>
<label>What impact have they made? (be specific)<textarea name="impact" required></textarea></label>
<label>Evidence links<input name="evidence" placeholder="News, socials, website…"></label>
<div class="row"><label>Your name<input name="name" required></label><label>Your email<input type="email" name="email" required></label></div>
<label class="consent"><input type="checkbox" required name="consent" value="yes"> I believe the nominee would be comfortable being considered, and I agree to the <a href="privacy.html">Privacy Policy</a>.</label>
<button class="btn btn-primary" type="submit">Submit nomination</button></form>'''

def build_submit():
    body = f'''<section class="article-hero"><div class="wrap"><span class="eyebrow">Share your story</span><h1>Your story belongs here</h1><p class="lead">Free editorial submissions are open to everyone. Our editors read every story and contact you before anything is published.</p></div></section>
<section style="padding-top:0"><div class="wrap grid g2" style="align-items:start">
<div class="form-card"><h2 style="margin-top:0">Submit a story</h2><form class="form" data-form="Story submission" data-success="Story received! An editor will read it and reply within 7 days.">
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
<div class="row"><label>Your name<input name="name" required></label><label>Email<input type="email" name="email" required></label></div>
<label>Whose story is it?<select name="whose" required><option>My own</option><option>Someone I know (with their permission)</option><option>My organization</option></select></label>
<label>Story title<input name="title" required></label>
<label>The story (or a summary + links)<textarea name="story" required style="min-height:220px"></textarea></label>
<label>Photos / video links (optional)<input name="media" placeholder="Google Drive, Dropbox, YouTube…"></label>
<label class="consent"><input type="checkbox" required name="consent" value="yes"> I have the right to share this story and agree to the <a href="terms.html">Terms</a> and <a href="privacy.html">Privacy Policy</a>.</label>
<button class="btn btn-primary" type="submit">Send my story</button></form></div>
<div><h2>What we look for</h2><ul class="checks light-checks"><li>True, first-hand or well-documented stories</li><li>A clear moment, obstacle and change</li><li>Courage, creativity, kindness or community impact</li><li>Consent from everyone identifiable</li></ul>
<div class="notice mt">Want a guaranteed, professionally written feature with a timeline? See <a href="get-featured.html">Get Featured</a>.</div>
<div class="form-card mt" id="nominate"><h2 style="margin-top:0">Nominate someone for the People.Media 100</h2>{nominate_form("submit")}</div></div>
</div></section>'''
    page("submit.html", f"Share Your Story or Nominate Someone — {NAME}", "Submit your true story to People.Media for free editorial consideration, or nominate an everyday hero for the People.Media 100.", body, "submit.html")

def build_100():
    body = f'''<section class="hero"><div class="wrap hero-grid"><div><span class="eyebrow">People.Media 100 · Class of 2027</span><h1>100 everyday people making an <em>outsized</em> difference.</h1><p class="lead">Not celebrities. Not billionaires. The teachers, founders, caregivers, creators and neighbours who quietly change things. Nominations are free and open worldwide.</p><div class="hero-cta"><a class="btn btn-primary" href="#nominate">Nominate now</a><a class="btn btn-ghost" href="story-write-a-winning-nomination.html">How to write a winning nomination</a></div></div>
<div class="form-card fade"><h3 style="margin-top:0">Key dates</h3><div class="facts" style="margin:0"><dl><dt>Now</dt><dd>Nominations open</dd><dt>31 Mar 2027</dt><dd>Nominations close</dd><dt>May 2027</dt><dd>Finalists contacted &amp; interviewed</dd><dt>Jul 2027</dt><dd>List published + honoree celebration</dd></dl></div><p class="fine">No fees to nominate or be selected. No one can pay for a place on the list.</p></div></div></section>
<section class="alt"><div class="wrap grid g4"><div class="kpi fade"><h3>Community</h3><p>Local heroes &amp; volunteers</p></div><div class="kpi fade"><h3>Founders</h3><p>Businesses that lift communities</p></div><div class="kpi fade"><h3>Creators</h3><p>Art, media and culture</p></div><div class="kpi fade"><h3>Youth 18–25</h3><p>Next-generation changemakers</p></div></div></section>
<section id="nominate"><div class="wrap grid g2" style="align-items:start"><div><h2>Methodology</h2><p>Editors review every nomination against four criteria: measurable impact, evidence, originality, and potential for the recognition to unlock further good. Finalists are interviewed and fact-checked. Sponsors never influence selection.</p><p>Honorees receive a published profile, the People.Media 100 badge and an invitation to our virtual celebration.</p></div><div class="form-card">{nominate_form("people-100")}</div></div></section>'''
    page("people-100.html", f"People.Media 100 — Nominate an Everyday Hero", "Nominate everyday people making an outsized difference for the People.Media 100. Free, global, editor-selected.", body, "people.html")

# ---------------------------------------------------------------- COMPANY / LEGAL
def prose_page(path, title, desc, inner, eyebrow):
    body = f'<section class="article-hero"><div class="wrap"><div class="article"><span class="eyebrow">{eyebrow}</span><h1>{E(title)}</h1><p class="fine">Last updated: {datetime.date.today().strftime("%d %B %Y")}</p></div></div></section><section style="padding-top:0"><div class="wrap"><div class="article prose">{inner}</div></div></section>'
    page(path, f"{title} — {NAME}", desc, body, path)

def build_company():
    prose_page("about.html","About People.Media","About People.Media: an independent, people-powered media platform celebrating everyday heroes, creators and changemakers.",f'''
<p class="lead" style="max-width:none">People.Media exists to put real people at the centre of media — not only the famous few, but the founders, creators, teachers, caregivers and neighbours whose stories rarely get told.</p>
<h2>What we do</h2><ul><li><strong>Original stories and guides</strong> on storytelling, personal brand, the creator economy and community.</li><li><strong>People profiles</strong> — fact-checked profiles of remarkable lives and a growing directory of everyday changemakers.</li><li><strong>Video</strong> — curated talks and human stories, refreshed automatically.</li><li><strong>Contests and the People.Media 100</strong> — giving anyone a path to be published and recognized.</li><li><strong>Get Featured</strong> — professionally written, clearly labelled profiles for founders, creators and professionals.</li></ul>
<h2>How we're funded</h2><p>We are independent. Our revenue comes from display advertising (Google AdSense), clearly labelled sponsorships and partner features, and reader support. Advertisers and sponsors never decide what we cover editorially. See our <a href="editorial-policy.html">Editorial Policy</a>.</p>
<h2>Our values</h2><ul><li><strong>Consent first.</strong> We tell stories with people, not about them.</li><li><strong>Accuracy.</strong> We verify facts and correct mistakes openly.</li><li><strong>Dignity.</strong> No poverty porn, no clickbait at someone's expense.</li><li><strong>Transparency.</strong> Paid content is always labelled.</li></ul>
<h2>Get in touch</h2><p>Use our <a href="contact.html">contact form</a>. For enquiries about this website, the domain name, sponsorship, advertising or partnership, <a href="{INQUIRY_URL}" target="_blank" rel="noopener">contact our business team</a>.</p>''',"About")

    prose_page("editorial-policy.html","Editorial Policy & Standards","People.Media editorial standards: accuracy, consent, corrections, sponsored content labelling and independence.",'''
<h2>Independence</h2><p>Editorial decisions are made by People.Media editors. Advertisers, sponsors and supporters do not choose, review or approve editorial stories.</p>
<h2>Accuracy and fact-checking</h2><p>We verify key facts — names, dates, figures and claims — with the subject and, where possible, independent sources. Profiles of public figures are written from widely documented public records.</p>
<h2>Consent and privacy</h2><p>We obtain consent from people featured in personal stories. We minimise identifying details where publication could cause harm, and we take special care with minors, health, finances and vulnerable people.</p>
<h2>Labelling of paid content</h2><p>Paid profiles purchased through Get Featured are labelled <strong>"Partner Feature"</strong>. Sponsored series are labelled <strong>"Presented by [Sponsor]"</strong>. Newsletter sponsorships are labelled <strong>"Sponsored"</strong>. Affiliate links, if used, are disclosed in the article.</p>
<h2>Corrections</h2><p>If we get something wrong, we fix it promptly and note significant corrections at the end of the article. Report an error through our <a href="contact.html">contact form</a>.</p>
<h2>Removal requests</h2><p>People featured in personal stories may request updates, anonymization or removal. We review every request with care and respond within 7 days.</p>
<h2>AI and automation</h2><p>Automated tools refresh our video and headline listings, which link to original publishers. Editorial articles and profiles are reviewed by humans before publication.</p>
<h2>User submissions</h2><p>Submitted stories may be edited for length, clarity and accuracy. We will not publish a submitted personal story without confirming consent.</p>''',"Standards")

    body = f'''<section class="article-hero"><div class="wrap"><span class="eyebrow">Contact</span><h1>Talk to People.Media</h1><p class="lead">Questions, corrections, story tips or partnership ideas — we read everything and reply within 2 business days.</p></div></section>
<section style="padding-top:0"><div class="wrap grid g2" style="align-items:start"><div class="form-card"><form class="form" data-form="Contact" data-success="Message received — we'll reply within 2 business days.">
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
<div class="row"><label>Name<input name="name" required autocomplete="name"></label><label>Email<input type="email" name="email" required autocomplete="email"></label></div>
<label>Topic<select name="topic" required><option value="">Choose…</option><option>General question</option><option>Story tip</option><option>Correction</option><option>Removal / privacy request</option><option>Get featured</option><option>Advertising / sponsorship</option><option>Partnership</option><option>Website / domain enquiry</option></select></label>
<label>Message<textarea name="message" required></textarea></label>
<label class="consent"><input type="checkbox" required name="consent" value="yes"> I agree to the <a href="privacy.html">Privacy Policy</a>.</label>
<button class="btn btn-primary" type="submit">Send message</button></form></div>
<div><div class="kpi"><h3>Business enquiries</h3><p>Interested in this website, the domain name, sponsorship, advertisement or partnership?</p><a class="btn btn-dark" href="{INQUIRY_URL}" target="_blank" rel="noopener">Contact the business team →</a></div>
<div class="kpi mt"><h3>Quick links</h3><ul><li><a href="get-featured.html">Get featured</a></li><li><a href="advertise.html">Advertise &amp; sponsor</a></li><li><a href="submit.html">Submit a story</a></li><li><a href="careers.html">Careers</a></li><li><a href="support.html">Support us</a></li></ul></div></div></div></section>'''
    page("contact.html", f"Contact — {NAME}", "Contact People.Media for questions, story tips, corrections, partnerships and business enquiries.", body, "contact.html")

    prose_page("privacy.html","Privacy & Cookie Policy","People.Media privacy and cookie policy, including Google AdSense advertising cookies and your choices.",'''
<p>This policy explains what information People.Media ("we") collects, how we use it and your choices.</p>
<h2>Information you give us</h2><p>When you submit a form (newsletter, story submission, nomination, contest entry, feature application, donation pledge, job application or contact form) we receive the information you enter, such as your name, email address and message. Form submissions are delivered to our team by a third-party form processing service (FormSubmit). We use this information only to respond to you and provide the service you requested.</p>
<h2>Information collected automatically</h2><p>Like most websites, our hosting provider may log technical data such as IP address, browser type and pages visited for security and performance. We store a few preferences in your browser's local storage (theme, cookie choice, boosts you've made, newsletter prompt timing). These never leave your device.</p>
<h2>Advertising — Google AdSense</h2><p>We use Google AdSense to display ads. Third-party vendors, including Google, use cookies to serve ads based on a user's prior visits to this website or other websites. Google's use of advertising cookies enables it and its partners to serve ads to users based on their visit to this site and/or other sites on the Internet.</p><p>You may opt out of personalized advertising by visiting <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener">Google Ads Settings</a>. You can also opt out of some third-party vendors' use of cookies for personalized advertising at <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener">aboutads.info</a>. Learn more about <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">how Google uses information from sites that use its services</a>.</p>
<h2>Embedded content</h2><p>Videos are embedded using YouTube's privacy-enhanced mode (youtube-nocookie.com) and load only when you press play. Our "Born today" widget requests public data from Wikipedia's API. Fonts are served by Google Fonts.</p>
<h2>Cookies and your choices</h2><p>On your first visit we ask for your cookie preference. Choosing "Essential only" requests non-personalized ads. Visitors in the EEA, UK and Switzerland may also be shown Google's certified consent message. You can clear cookies and local storage in your browser at any time.</p>
<h2>Sharing</h2><p>We do not sell your personal information. We share it only with service providers needed to operate the site (form delivery, hosting, email) or when required by law.</p>
<h2>Retention</h2><p>We keep submissions only as long as needed for the purpose you provided them, or as required by law. You may ask us to delete your data at any time.</p>
<h2>Children</h2><p>People.Media is not directed to children under 13, and we do not knowingly collect their personal data.</p>
<h2>Your rights</h2><p>Depending on where you live (for example under GDPR, UK GDPR, CCPA/CPRA or India's DPDP Act), you may have rights to access, correct, delete or restrict use of your data. Contact us through our <a href="contact.html">contact form</a> and choose "Removal / privacy request".</p>
<h2>Changes</h2><p>We may update this policy and will change the "last updated" date above.</p>''',"Privacy")

    prose_page("terms.html","Terms of Use","Terms of use for People.Media, including user submissions, contests, paid features and intellectual property.",'''
<p>By using People.Media you agree to these terms.</p>
<h2>Use of the site</h2><p>You may read, share links to and quote short excerpts of our content with attribution. You may not copy substantial portions, scrape the site, or use it for unlawful purposes.</p>
<h2>User submissions</h2><p>When you submit a story, nomination, contest entry or other content, you confirm you have the right to share it and that it is truthful to the best of your knowledge. You keep ownership; you grant People.Media a worldwide, non-exclusive, royalty-free licence to edit, publish, translate and promote it across our website, newsletter and social channels. You can ask us to remove published content at any time.</p>
<h2 id="contests">Contests</h2><p>No purchase is necessary to enter or win. Entrants must be 18+ unless a youth category states otherwise and guardian consent is provided. One entry per person per contest. Entries must be original and true. Judging criteria are published on each contest page; judges' decisions are final. Community Choice votes may be audited and fraudulent votes removed. Prizes are paid within 30 days of announcement, may be subject to local taxes payable by winners, and are void where prohibited. We may cancel or modify a contest if circumstances beyond our control require it.</p>
<h2>Paid features and sponsorships</h2><p>Paid features are labelled. We may decline or require changes to content that is misleading, unlawful or inconsistent with our editorial policy. Refunds: full refund if we decline after payment; otherwise refunds are available before the interview takes place.</p>
<h2>Supporter contributions</h2><p>Contributions support our operations and are not tax-deductible. Recurring support can be cancelled at any time.</p>
<h2>Third-party links</h2><p>We link to external sites (including headline sources and YouTube). We are not responsible for their content or policies.</p>
<h2>Disclaimer and liability</h2><p>Content is provided for general information and inspiration and is not professional advice. To the extent permitted by law, People.Media is not liable for indirect or consequential losses arising from use of the site.</p>
<h2>Changes</h2><p>We may update these terms; continued use means you accept the updated terms.</p>''',"Legal")

    prose_page("disclaimer.html","Disclaimer, Trademark & Copyright Notice","People.Media disclaimer, trademark notice and copyright policy, including non-affiliation with similarly named brands.",'''
<h2>Trademark notice and non-affiliation</h2><p><strong>"People.Media"</strong>, the People.Media name as written with a dot, and the overlapping-circles logo are brand identifiers of this website. People.Media is an independent publication. <strong>It is not affiliated with, endorsed by, or connected to</strong> PEOPLE magazine or People.com, any company or service operating under the name "People Media" (including former or current online dating businesses), or any other similarly named publisher, broadcaster or agency. Any third-party trademarks mentioned on this site belong to their respective owners and are used only for identification, commentary or reference (nominative fair use).</p>
<p>We deliberately avoid using any third party's logos, typography, colour schemes or taglines, and our name is always presented as "People.Media" (with the dot) to distinguish it.</p>
<h2>Copyright</h2><p>All original text, design, code and graphics on People.Media are © People.Media unless otherwise stated. Headlines in our auto-updated "good news" listing are short titles linking to the original publishers, who own their content. Embedded videos are played via YouTube's official embed player and remain the property of their creators. Birthday data is drawn from Wikipedia's public API under its licence terms.</p>
<p>We do not use stock photos of real people without rights. Illustrations on this site are original graphic designs.</p>
<h2>Copyright complaints (DMCA / takedown)</h2><p>If you believe content on People.Media infringes your copyright, please use our <a href="contact.html">contact form</a> (topic: "Removal / privacy request") with: your contact details, a description of the work, the URL of the material, a statement of good-faith belief, and a statement that the information is accurate and that you are the owner or authorized to act. We respond promptly and remove infringing material.</p>
<h2>General disclaimer</h2><p>Information on this site is published in good faith for general information and inspiration only. It is not legal, financial, medical or professional advice. Profiles of historical figures are summaries of widely documented public information. Contest prizes, feature packages and rates may change.</p>
<h2>Advertising disclosure</h2><p>This site displays ads served by Google AdSense and may publish labelled sponsored content and partner features. Earnings from ads and sponsorships help keep content free.</p>''',"Legal")

def build_404():
    body = '<section class="hero"><div class="wrap center"><span class="eyebrow">404</span><h1>This story hasn\'t been written yet.</h1><p class="lead" style="margin:0 auto 20px">The page you\'re looking for doesn\'t exist. Maybe it\'s yours to tell?</p><div class="pill-row" style="justify-content:center"><a class="btn btn-primary" href="index.html">Go home</a><a class="btn btn-ghost" href="stories.html">Read stories</a><a class="btn btn-ghost" href="submit.html">Share your story</a></div></div></section>'
    page("404.html", f"Page not found — {NAME}", "Page not found.", body, "")

# ---------------------------------------------------------------- SEO files
def build_seo():
    urls = []
    for p in PAGES:
        if p == "404.html": continue
        pr = "1.0" if p == "index.html" else ("0.8" if p.startswith(("story-","person-")) else "0.7")
        urls.append(f"<url><loc>{SITE}/{'' if p=='index.html' else p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>")
    with open(os.path.join(ROOT,"sitemap.xml"),"w",encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n")
    with open(os.path.join(ROOT,"robots.txt"),"w",encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nUser-agent: Mediapartners-Google\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    with open(os.path.join(ROOT,"ads.txt"),"w",encoding="utf-8") as f:
        f.write("google.com, pub-6620975821265271, DIRECT, f08c47fec0942fa0\n")
    items = "".join(f"<item><title>{E(a['title'])}</title><link>{SITE}/story-{a['slug']}.html</link><guid>{SITE}/story-{a['slug']}.html</guid><pubDate>{datetime.datetime.fromisoformat(a['date']).strftime('%a, %d %b %Y 08:00:00 +0000')}</pubDate><description>{E(a['dek'])}</description></item>" for a in ARTICLES)
    with open(os.path.join(ROOT,"feed.xml"),"w",encoding="utf-8") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{NAME}</title><link>{SITE}</link><description>{TAGLINE}</description><language>en</language>{items}</channel></rss>')

if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    build_home(); build_stories()
    for i, a in enumerate(ARTICLES): build_article(a, i)
    build_people()
    for p in PEOPLE: build_person(p)
    build_videos(); build_featured(); build_advertise(); build_contests(); build_support(); build_careers(); build_submit(); build_100(); build_company(); build_404()
    build_seo()
    print(f"Built {len(PAGES)} pages")
