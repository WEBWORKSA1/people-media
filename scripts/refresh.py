# -*- coding: utf-8 -*-
"""Auto-refresh People.Media data feeds (run by GitHub Actions).
- data/videos.json    <- latest uploads from curated YouTube channels (public RSS)
- data/headlines.json <- latest uplifting headlines from public RSS feeds (title + link only)
Then rebuilds the static site. Standard library only. Failing feeds are skipped, never fatal."""
import json, os, sys, datetime, urllib.request, xml.etree.ElementTree as ET, subprocess, html, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "Mozilla/5.0 (PeopleMediaBot; +https://people.media)"}

# YouTube channel IDs (public RSS: https://www.youtube.com/feeds/videos.xml?channel_id=...)
CHANNELS = [
    ("TED", "UCAuUUnT6oDeKwE6v1NGQxug"),
    ("TEDx Talks", "UCsT0YIqwnpJCM-mx7-gSA4Q"),
    ("Great Big Story", "UCajXeitgFL-rb5-gXI-aG8Q"),
    ("Goalcast", "UCWYK1jQRQHumkIL9TbVOGSA"),
    ("TED-Ed", "UCsooa4yRKGN_zEE8iknghZA"),
]
# Positive / human-interest news RSS feeds (we store only titles + links)
FEEDS = [
    ("Good News Network", "https://www.goodnewsnetwork.org/feed/"),
    ("Positive News", "https://www.positive.news/feed/"),
    ("Reasons to be Cheerful", "https://reasonstobecheerful.world/feed/"),
    ("The Better India", "https://thebetterindia.com/feed/"),
    ("Upworthy", "https://www.upworthy.com/feeds/feed.rss"),
    ("Good Good Good", "https://www.goodgoodgood.co/articles/rss.xml"),
]

def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def youtube():
    ns = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015", "media": "http://search.yahoo.com/mrss/"}
    out = []
    for name, cid in CHANNELS:
        try:
            root = ET.fromstring(fetch("https://www.youtube.com/feeds/videos.xml?channel_id=" + cid))
            for e in root.findall("a:entry", ns)[:6]:
                vid = e.findtext("yt:videoId", default="", namespaces=ns)
                title = e.findtext("a:title", default="", namespaces=ns)
                pub = e.findtext("a:published", default="", namespaces=ns)
                if vid and title and "#shorts" not in title.lower():
                    out.append({"id": vid, "title": title, "channel": name, "published": pub})
            print("youtube ok:", name)
        except Exception as ex:
            print("youtube skip:", name, ex)
    out.sort(key=lambda v: v["published"], reverse=True)
    # interleave channels for variety
    seen, mixed = {}, []
    for v in out:
        seen.setdefault(v["channel"], []).append(v)
    while any(seen.values()):
        for ch in list(seen):
            if seen[ch]: mixed.append(seen[ch].pop(0))
    return mixed[:30]

def clean(t):
    t = html.unescape(re.sub(r"<[^>]+>", "", t or "")).strip()
    return re.sub(r"\s+", " ", t)[:180]

def headlines():
    items = []
    for name, url in FEEDS:
        try:
            root = ET.fromstring(fetch(url))
            entries = root.findall(".//item") or root.findall(".//{http://www.w3.org/2005/Atom}entry")
            n = 0
            for it in entries:
                title = clean(it.findtext("title") or it.findtext("{http://www.w3.org/2005/Atom}title"))
                link = (it.findtext("link") or "").strip()
                if not link:
                    l = it.find("{http://www.w3.org/2005/Atom}link"); link = l.get("href") if l is not None else ""
                date = it.findtext("pubDate") or it.findtext("{http://www.w3.org/2005/Atom}updated") or ""
                if title and link.startswith("http"):
                    items.append({"title": title, "link": link, "source": name, "date": date}); n += 1
                if n >= 5: break
            print("feed ok:", name, n)
        except Exception as ex:
            print("feed skip:", name, ex)
    # round-robin by source so no single publisher dominates
    by, mixed = {}, []
    for i in items: by.setdefault(i["source"], []).append(i)
    while any(by.values()):
        for s in list(by):
            if by[s]: mixed.append(by[s].pop(0))
    return mixed[:24]

def write(name, payload, key):
    path = os.path.join(ROOT, "data", name)
    old = {}
    try:
        with open(path, encoding="utf-8") as f: old = json.load(f)
    except Exception: pass
    if not payload.get(key) and old.get(key):
        print("keeping previous", name, "(fetch returned nothing)"); return
    with open(path, "w", encoding="utf-8") as f: json.dump(payload, f, ensure_ascii=False, indent=1)

if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="minutes")
    write("videos.json", {"updated": now, "videos": youtube()}, "videos")
    write("headlines.json", {"updated": now, "items": headlines()}, "items")
    subprocess.run([sys.executable, os.path.join(ROOT, "src", "build.py")], check=True)
