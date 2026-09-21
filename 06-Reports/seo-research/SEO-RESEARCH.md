# SEO Research: redwhiteandclix.org

> Audit date: 2026-09-21 · Market: United States / Lafayette, Indiana · Sitemap URLs: 27

## Executive assessment

The site is crawlable and every sitemap URL returned HTTP 200, but its search foundation is diluted by duplicate homepage URLs, weak event-page metadata, incorrect entity schema, excessive heading markup, poor image descriptions and a commerce-heavy sitemap. The clearest near-term search opportunity is owning the intersection of **HeroClix events**, **veteran gaming**, and **Lafayette/Indiana**, supported by accurate event and nonprofit evidence.

SE Ranking was connected but reported `0/25,000` API units and returned HTTP 402 for audit, keyword, traffic and backlink endpoints. Google PageSpeed returned a project quota error. No ranking, traffic, backlink or performance numbers are estimated in this report.

## Priority fixes

| Rank | Issue | Severity | Scope | Recommended fix | Effort |
|---:|---|---|---|---|---|
| 1 | `/` and `/home` both return 200 while sitemap lists `/home` and root canonical points to `/` | High | Homepage | 301 `/home` to `/`; include only canonical `/` in sitemap and internal links | S |
| 2 | Event hub title is “Store 2 — Red White and Clix” | High | `/services-store` | Rename page and title to “2026 HeroClix Events in Lafayette, Indiana” | S |
| 3 | Event and donation pages have empty meta descriptions | High | 2 key pages | Add unique, action-focused descriptions | S |
| 4 | Donation page has no H1 | High | `/donate` | Add one descriptive H1 | S |
| 5 | Homepage has roughly 30 H1 elements, including sponsor names and decorative marks | High | Homepage | Keep one descriptive H1; change section/sponsor headings to H2/H3 or text | M |
| 6 | Sitewide `LocalBusiness` schema describes the nonprofit as open `00:00–00:00` every day | High | Sitewide | Remove LocalBusiness or replace with appropriate `NGO`/`Organization`; distinguish mailing and event locations | M |
| 7 | No `Event` schema on the event hub | High | Events | Add one Event entity per confirmed event with date, venue, offer and registration URL | M |
| 8 | 58/62 homepage images, 7/11 event-hub images and 6/10 about images lack alt text | Medium | Key pages | Add contextual alt for meaningful images; use empty alt for decorative images | M |
| 9 | Product-heavy sitemap creates 20 merchandise/event-product URLs against 3 core mission pages | Medium | Sitemap/site architecture | Consolidate weak/duplicate products; noindex retired listings; build mission, impact, events and resources hubs | L |
| 10 | Organization schema has blank description and empty `sameAs` | Medium | Sitewide | Add mission description, official Facebook and verified profiles | S |

## Technical and indexability findings

- `robots.txt` permits normal and named AI crawlers while blocking Squarespace system/query URLs. It references the sitemap correctly.
- The sitemap itself returns `X-Robots-Tag: noindex`, which is normal for a sitemap document and does not block listed URLs.
- All 27 sitemap URLs return 200. No 404 entries were detected.
- `/home` is a duplicate, separately accessible homepage. The root URL is canonical in the homepage HTML but absent from the sitemap.
- HTTPS and HSTS are enabled. `X-Content-Type-Options: nosniff` and `X-Frame-Options: SAMEORIGIN` are present on the homepage. HSTS lacks `includeSubDomains` and `preload`; this is lower priority than content/indexation work.
- Canonicals were self-referential on `/about`, `/donate`, and `/services-store`.
- Pages are large in raw HTML: homepage ~1.09 MB, about ~279 KB, event hub ~256 KB, donation ~232 KB. Image/script weight likely warrants performance work, but Lighthouse metrics were unavailable.

## On-page findings

| URL | Current title | Main issue | Recommended search intent |
|---|---|---|---|
| `/` | Red White and Clix \| Connect & Support Veterans Today | Generic title; H1 hierarchy broken | Veteran-founded HeroClix events in Indiana |
| `/about` | About \| Join the Movement Today — Red White and Clix | Three H1s; generic “About” | Founder story and veteran gaming mission |
| `/donate` | Donate — Red White and Clix | No H1 or description; trust content incomplete | Donate to veteran-focused gaming events |
| `/services-store` | Store 2 — Red White and Clix | Placeholder title and empty description | 2026 HeroClix tournaments in Lafayette |

Recommended homepage title: **Red White and Clix | Veteran HeroClix Events in Indiana**  
Recommended homepage H1: **Play HeroClix. Build Community. Stand With Veterans.**

Recommended event title: **2026 HeroClix Events in Lafayette, Indiana | RWC**  
Recommended event description: **Register for Red White and Clix HeroClix events on November 7–8, 2026, in Lafayette, Indiana. View formats, fees, schedules and venue details.**

Recommended donation description: **Support Red White and Clix, a veteran-founded 501(c)(3) using tabletop gaming events to build community and support veteran-focused causes.**

## Search opportunity

### Priority topic cluster

1. **HeroClix events and tournaments** — event hub, Modern format, Team Sealed, travel/venue and beginner guidance.
2. **Veteran gaming community** — why gaming and tabletop play can create connection, with careful sourcing and no clinical promises.
3. **Indiana/Lafayette local relevance** — event venue, local partners, supported organization and area resources.
4. **Veteran nonprofit transparency** — beneficiary, allocation, annual outcomes, IRS status and sponsor participation.

### Recommended keyword map

| Page | Primary phrase | Supporting phrases |
|---|---|---|
| Homepage | veteran gaming nonprofit | gaming events for veterans; veteran tabletop community; Indiana veteran nonprofit |
| Events hub | HeroClix tournament Indiana | HeroClix event Lafayette; HeroClix tournament 2026; Midwest HeroClix event |
| 300 Modern | HeroClix 300 Modern tournament | HeroClix Modern format; Lafayette HeroClix tournament |
| Team Sealed | HeroClix Team Sealed event | 3v3 HeroClix; HeroClix team tournament |
| About | veteran-founded gaming nonprofit | Wesley Robertson; Red White and Clix mission |
| Donate | donate to veteran gaming nonprofit | support veterans through gaming; Indiana veteran charity |
| Impact | veteran nonprofit impact report | RWC beneficiary; gaming fundraiser results |
| Resources | veteran resources Lafayette Indiana | Indiana veteran support resources |

Search volumes and difficulty are intentionally absent until SE Ranking units are restored.

## Local SEO

- Website/IRS mailing address and Facebook/event venue serve different purposes. Label them explicitly as **mailing address** and **event venue** instead of forcing one NAP value everywhere.
- The Facebook page still points to an old GoDaddy domain and Yahoo email; update it to the current domain and Gmail address.
- The Google Business Profile link could not be fully audited due Google’s unusual-traffic challenge. Confirm category, service area, website, phone, description, photos and whether the listing represents an office visitors can actually access.
- Create a dedicated Lafayette event-location section with venue address, directions, parking, accessibility and lodging. Do not mark the armory as the organization’s permanent office.
- Seek citations/links from the supported veteran organization, sponsors, venue, Lafayette tourism/community calendars and reputable tabletop event directories.

## Structured data

Current valid JSON-LD types are `WebSite`, `Organization` and `LocalBusiness`. The implementation needs semantic correction:

- Keep `WebSite` and use a stable `@id`.
- Use `NGO` or `Organization` for Red White and Clix, including legal name, URL, logo, email, phone, tax ID where appropriate, and verified `sameAs` URLs.
- Remove the misleading `LocalBusiness` block unless RWC operates a staffed public location with real hours.
- Add `Event` markup to each confirmed event with `name`, `startDate`, `endDate`, `eventStatus`, `eventAttendanceMode`, `location`, `offers`, `organizer`, image and registration URL.
- Add `BreadcrumbList` to internal pages and product pages.
- Use `Product`/`Offer` only where price and availability are authoritative. Resolve the current Squarespace/HCUnits price conflicts first.
- Do not add FAQ schema to placeholder or unverified donation answers.

## Image SEO

- Homepage: 62 images; 58 missing/empty alt attributes.
- About: 10 images; 6 missing/empty alt attributes.
- Event hub: 11 images; 7 missing/empty alt attributes.
- Donation: 6 images; 2 missing/empty alt attributes.
- The sitemap includes numerous sponsor logos, screenshots, generated-image filenames and repeated logo URLs. Replace filenames and alt text with clear descriptions where meaningful.
- Use authentic event photography as the main visual evidence. Keep generated art and mockups out of documentary contexts.
- Resize oversized originals, use WebP/AVIF where Squarespace permits, define dimensions and avoid loading below-the-fold galleries eagerly.
- Decorative separators and repeated logos should use empty alt text, not duplicated keyword text.

## Content and authority plan

### First 30 days

1. Fix homepage duplication, event metadata, H1 hierarchy and schema.
2. Reconcile all event fees and registration URLs.
3. Publish one authoritative 2026 event page with complete logistics.
4. Correct Facebook and verify GBP fields.
5. Add alt text to the 20 highest-value real photographs and all functional images.

### 30–60 days

1. Publish an impact/transparency page modeled on Stack Up’s clarity: beneficiary, allocation, results, annual report and governing documents.
2. Publish a newcomer HeroClix event guide and Team Sealed/Modern format explainers.
3. Build a veteran resources page with qualified local/state resources and careful disclaimers.
4. Add Event, Organization/NGO and Breadcrumb schema.

### 60–90 days

1. Earn links from veteran-serving partners, sponsors, venue/community calendars and tabletop organizations.
2. Publish post-event results with verified attendance, funds raised, beneficiary handoff and photographs.
3. Connect Google Search Console and GA4; track organic registration clicks and completed paid registrations separately.
4. Restore SE Ranking units and rerun quantitative keyword, backlink, competitor-gap and AI-visibility modules.

## Measurement

Track nonbranded impressions/clicks, branded impressions, event-page organic entrances, registration-link clicks, completed registrations, sponsor inquiries, donation completions, indexed canonical pages and referring domains. Define the baseline period before measuring the client’s “double traffic” goal.

## Evidence and limitations

Evidence includes live HTML and headers fetched September 21, 2026; live robots.txt and sitemap; 27-URL status checks; existing site snapshot; public search results; GHL intake and organization research. GSC, GA4, GBP administrative data, SE Ranking metrics, CrUX and Lighthouse scores were unavailable. Recommendations involving live profile ownership or event facts require client confirmation before implementation.

