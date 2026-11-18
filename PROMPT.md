# People.Media — Phase-Wise Build Prompt

Use these prompts in order to rebuild, extend or re-create People.Media with any AI coding assistant. Each phase is self-contained and ends with acceptance checks.

---

## The winning concept (why this idea)

**People.Media = "the people-powered media network."** Human stories, people profiles, creator guides, video, monthly contests, the annual *People.Media 100* list and a paid **Get Featured** service.

Why this beats other uses of the domain:

| Option | Traffic potential | Revenue per visitor | AdSense approval odds | Verdict |
|---|---|---|---|---|
| Celebrity gossip | High, but saturated (PEOPLE, TMZ) | Low | Medium (trademark & copyright risk) | ✗ |
| "Net worth / bio" database | High | Low–medium | Low (thin content gets rejected) | ✗ |
| Social network for people | Needs a backend; GitHub Pages can't host it | — | — | ✗ |
| **People-powered stories + Get Featured + contests** | Medium–high (evergreen guides, profiles, shareable stories) | **High** (paid features $149–$999, sponsorships, ads, supporters) | **High** (original, people-first, brand-safe) | ✓ |

Revenue stack, highest $/visitor first:
1. **Get Featured** packages: Spotlight $149, Feature Interview $399, Signature Story $999. This follows Entrepreneur's paid contributor network ($3,000/yr) and Fast Company's paid award entries.
2. **Sponsorships**: newsletter, branded series, contest prizes, category ownership.
3. **Google AdSense** auto ads on every page.
4. **Supporters**: one-time, monthly or yearly, with perk tiers. This follows NPR, The Guardian, Good News Network and Longreads.
5. **Contests**: they generate leads and content, and sponsors fund the prizes.

---

## PHASE 1 — Foundation, brand and AdSense-safe skeleton

> Build a static, multi-page website for the domain **People.Media** that GitHub Pages (free plan, `main` branch, root folder) can host. Use only HTML, CSS and vanilla JS, plus a Python standard-library generator (`src/build.py`) that writes every page to the repo root so header and footer stay identical everywhere.
>
> **Brand:** "People.Media — Real people. Real stories. Real impact." Visual style is editorial warmth: ink `#16120f` on paper `#fbf7f1`, coral `#ff5a36`, teal `#0e7c7b`, gold `#f2b134`. Headings use Fraunces (serif) and body text uses Inter. Logo is two overlapping circles (coral and teal) with a paper-coloured dot. Include dark mode, rounded cards and soft shadows.
>
> **Every page must include:**
> - In `<head>`: `<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>` and `<meta name="google-adsense-account" content="ca-pub-6620975821265271">`.
> - At the very top, a bar reading "Contact, if you are interested in this website / domain name / Sponsorship / Advertisement / Partnership", linked to `https://web.works/contact`. Do not print the URL as visible text.
> - A sticky header with nav: Home, Stories, People, Videos, Contests, Get Featured, Advertise, Support, plus a "Share your story" button. Include a dark-mode toggle and a mobile menu.
> - A footer with a newsletter form, four link columns (Read, Participate, Business, Company), a non-affiliation trademark line and an AdSense disclosure.
> - A cookie consent banner. "Essential only" should set `requestNonPersonalizedAds = 1`.
> - Canonical URL, Open Graph tags, and JSON-LD (`Organization`, `WebSite` with `SearchAction`, plus `Article` or `ProfilePage` where relevant).
> - Root files: `ads.txt` (`google.com, pub-6620975821265271, DIRECT, f08c47fec0942fa0`), `robots.txt` (allow Mediapartners-Google), `sitemap.xml`, `feed.xml` (RSS), `manifest.webmanifest`, `404.html` and `.nojekyll`.
>
> **Acceptance:** every page passes HTML validation, works at 390px width with no horizontal scroll, and contains the AdSense script exactly once.

## PHASE 2 — Original content (what AdSense approval depends on)

> Write **12 original long-form guides** of 600–1,000 words each, with H2 structure, internal links and a support ask at the end. Topics:
> 1. Telling your story
> 2. Personal-brand playbook
> 3. Getting featured in media
> 4. 11 creator income streams
> 5. Interviewing anyone
> 6. Why everyday heroes matter
> 7. Writing a winning nomination
> 8. Phone documentary portraits
> 9. Ethics of sharing stories
> 10. Lessons from comeback stories
> 11. About-section writing
> 12. Family oral history
>
> Write **11 fact-checked profiles** of historical figures (Wangari Maathai, A. P. J. Abdul Kalam, Marie Curie, Nelson Mandela, Frida Kahlo, Ada Lovelace, Srinivasa Ramanujan, Florence Nightingale, Jesse Owens, Rosalind Franklin, Nikola Tesla). Each gets a Quick Facts box and a "Why their story matters" section.
>
> Build these trust pages: About, Editorial Policy (independence, fact-checking, consent, "Partner Feature" labelling, corrections, removal requests, use of automation), Contact, Privacy & Cookies (including the Google AdSense cookie wording and opt-out links), Terms (including contest rules), and Disclaimer & Trademark (not affiliated with PEOPLE magazine, People.com, any "People Media" company, or any similarly named brand; copyright and DMCA process).
>
> **Never:** fabricate testimonials, view counts, supporter numbers or quotes, or use photos of real people you don't have rights to. Use original gradient art instead.
>
> **Acceptance:** at least 25 indexable pages of original text, no placeholder "lorem ipsum", and every page linked from the sitemap.

## PHASE 3 — Lead generation (the money engine)

> Build `get-featured.html`:
> - Hero with a value proposition and a "who we feature" grid.
> - Three pricing cards (Spotlight $149, Feature Interview $399 marked "Most popular", Signature Story $999).
> - A three-step process section.
> - FAQ written to handle objections: is it an ad, can I review it, what if I'm rejected, does it stay permanent, do you invoice.
> - A **three-step application form**: package and profile type → story headline, story and links → contact details, timeline and consent. Include progress dots, per-step validation and `?package=` preselection.
>
> Add a reusable **quick feature enquiry** CTA band on Home, Stories and People. Add `advertise.html` with four sponsorship formats, partner types, a media-kit request form, and a domain/website acquisition link to `web.works/contact`.
>
> **All forms:**
> - Send through FormSubmit's AJAX endpoint.
> - The destination inbox **must never appear in HTML or as visible text**. Assemble it only at submit time from an encoded, split, reversed base64 string.
> - Include a honeypot field, inline success state and a toast.
>
> **Acceptance:** run `grep -r "@gmail" .` and confirm it returns nothing. A test submission reaches the inbox.

## PHASE 4 — Donations and support for operations, promotion, hiring and prizes

> Build `support.html` with:
> - A fundraising goal progress bar, configured in `assets/js/config.js`.
> - Impact tiers ($10, $50, $250, $1,000).
> - A One-time / Monthly / Yearly toggle with preset amounts and a custom amount field.
> - An allocation picker: operations, paying contributors and hiring, contest prizes, video, promotion and marketing, micro-grants.
> - Instant-pay buttons that appear only when handles are configured (Stripe Payment Link, PayPal.me, Buy Me a Coffee, Ko-fi, UPI).
> - A pledge form that always works.
> - Perk tiers: Friend $5, Insider $10, Patron $50, Founding Circle $1,000.
> - A "where the money goes" table, a supporter wall, and the note that contributions are not tax-deductible.
>
> Build `careers.html` with six remote roles (writer, video storyteller, ambassador, social editor, partnerships lead, translator) and an application form.

## PHASE 5 — Contests, nominations and community

> Build `contests.html`:
> - Monthly theme with a live countdown.
> - Prize cards (Grand Winner, Runner-up, Community Choice).
> - Weighted judging criteria and rules in brief.
> - Entry form for written or video entries, with originality and rules consent.
>
> Build `people-100.html`: annual list with key dates, methodology ("no one can pay for a place") and a nomination form. Build `submit.html` with a free story submission form plus the nomination form.
>
> Add **Boost** buttons on people cards and profiles (stored in localStorage, honest counts that start at 0). Add a search box and category chips on Stories and People.

## PHASE 6 — Self-updating, automated content

> - **Born Today** widget: fetch `https://en.wikipedia.org/api/rest_v1/feed/onthisday/births/MM/DD` client-side, show people with thumbnails, and cache per day.
> - **Video hub**: `scripts/refresh.py` reads public YouTube channel RSS feeds (TED, TEDx, Great Big Story, Goalcast, TED-Ed) and writes `data/videos.json`. The page renders lite embeds (thumbnail first, `youtube-nocookie` iframe on click).
> - **Good-news headlines**: the same script reads public RSS feeds (Good News Network, Positive News, Reasons to be Cheerful, The Better India, Upworthy, Good Good Good). Store **title + link + source only** (copyright-safe), round-robin by source, and write `data/headlines.json`.
> - The script then re-runs `src/build.py` so the headlines are baked into the HTML for SEO.
> - `.github/workflows/auto-refresh.yml` runs on a 6-hour cron, on manual dispatch, and on pushes to `src/` or `scripts/`. It commits changes to `main` and pings the Pages build API.
>
> **Acceptance:** the workflow passes, and `data/*.json` show a fresh `updated` timestamp.

## PHASE 7 — Interactivity and polish

> Add: reading progress bar, entrance animations (content must stay visible without JS and for crawlers), share buttons (X, LinkedIn, WhatsApp, Facebook, copy, native share), a newsletter modal (only after scrolling 1,600px, at most once per 7 days, never for subscribers), a floating "Get featured" CTA, accessible focus states, a skip link and reduced-motion support.

## PHASE 8 — Deploy, connect the domain, apply to AdSense

1. Push to `github.com/webworksa1/people-media` on the `main` branch.
2. In Settings → Pages, set Source to *Deploy from a branch*, then `main` / `(root)`.
3. Connect the custom domain:
   - In Settings → Pages, set Custom domain to `people.media` and enable **Enforce HTTPS**.
   - At the registrar, add `A` records for `@` pointing to 185.199.108.153, 185.199.109.153, 185.199.110.153 and 185.199.111.153.
   - Add a `CNAME` record for `www` pointing to `webworksa1.github.io`.
4. Activate FormSubmit by submitting any form once, then clicking the confirmation email that arrives in the site inbox.
5. In AdSense, add the site `people.media` (AdSense only accepts a root domain, not a github.io sub-path). Confirm `https://people.media/ads.txt` loads. Enable Auto ads. Turn on Google's certified CMP under Privacy & messaging for EEA/UK visitors.
6. In Google Search Console, verify the domain and submit `sitemap.xml`.

## PHASE 9 — Growth roadmap (expandable)

- Publish two new guides and two new profiles every week, and add each to `src/content_*.py`.
- Publish monthly contest winners as stories, then turn each into a short video.
- Use every paid feature to bring in referrals from the featured person.
- Add a "Partner Feature" template and a jobs board for sponsors.
- Localize into Hindi and Spanish.
- Add regional editions of the People.Media 100.
