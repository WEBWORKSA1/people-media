# People.Media

**Real people. Real stories. Real impact.** This is a people-powered media website built for the domain **People.Media**. It is a static site, so it runs on the GitHub Pages free plan, served from the `main` branch.

## What's inside

**Content**
- 12 original guides and 11 fact-checked people profiles.
- Born-Today birthdays, live from Wikipedia's public feed.
- A video hub and good-news headlines, both refreshed automatically every 6 hours by `.github/workflows/auto-refresh.yml`.

**Revenue**
- **Lead generation:** a Get Featured page with three packages and a three-step application form, plus a quick-enquiry band on major pages.
- **Advertising:** an Advertise / Sponsor / Partner page with a media-kit form, and Google AdSense auto ads on every page (`ca-pub-6620975821265271`, with `ads.txt` in place).
- **Support:** a donations page (one-time, monthly or yearly; choose where the money goes: operations, hiring, prizes, video, promotion, grants) with perk tiers.
- **Contests and recognition:** monthly story contests with prizes, and People.Media 100 nominations.
- **Careers:** hiring for freelance, part-time and volunteer roles.

**Trust pages** (needed for AdSense approval)
- About, Editorial Policy, Contact, Privacy & Cookies, Terms, and Disclaimer & Trademark.
- Every page carries the business-inquiry bar linking to the web.works contact page.

## Edit and rebuild

```bash
python3 src/build.py      # regenerate all pages from src/content_*.py
python3 scripts/refresh.py  # fetch videos and headlines, then rebuild
```

Payment handles, the fundraising goal and contest dates live in `assets/js/config.js`.

## Go-live checklist

1. **Turn on hosting:** Settings → Pages → Deploy from branch → `main` / root.
2. **Connect the domain:**
   - Settings → Pages → Custom domain → `people.media`.
   - At the registrar, add `A` records for `@` pointing to 185.199.108.153, 185.199.109.153, 185.199.110.153 and 185.199.111.153.
   - Add a `CNAME` record for `www` pointing to `webworksa1.github.io`.
   - Turn on Enforce HTTPS.
3. **Activate the forms:** submit any form once, then confirm the FormSubmit activation email in the site inbox.
4. **Apply to AdSense:** add `people.media` in AdSense, enable Auto ads, and turn on Google's consent message (CMP) for EEA/UK visitors.
5. **Register with Search Console:** submit `https://people.media/sitemap.xml`.

See `PROMPT.md` for the phase-wise build prompt and `RESEARCH.md` for notes on the 39 benchmark sites.
