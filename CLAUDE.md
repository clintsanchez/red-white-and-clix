# Red White and Clix — project instructions

Client onboarded September 21, 2026 from Wesley Robertson's completed GHL survey. This is the client working repo. Read `HANDOFF.md`, `00-Client-Brief.md`, `.agents/product-marketing.md` and `06-Reports/organization-research.md` first.

## Confirmed basics

- Current site: https://www.redwhiteandclix.org/ on Squarespace. Do not assume WordPress or invent credentials.
- Contact: Wesley Robertson; redwhiteandclix@gmail.com; `tel:+15742659585`.
- GHL contact: `TGwjKOcOvCWWCnmObL4o`.
- Primary goal: 80 November registrations and double traffic. November 7–8, 2026 event verified on HCUnits.
- No politics or divisive content. Welcoming, professional, warm and motivating voice.
- IRS federal record verified; operational history and incorporation date remain distinct.
- Current platforms/prices differ across sources. Read the conflict list before writing copy.

## Sources and assets

- `brand/brand.yaml`, `brand/context.md`, `brand/guidelines.md`: persistent brand package.
- `brand-style-guide.md`, `DESIGN.md`, `website/css-tokens.css`: synchronized logo palette and proposed UI rules.
- pCloud `Clients/Red White and Clix/05-Photos/`: originals, source URLs/hashes/dimensions in manifests.
- Preserve client-uploaded logo. Do not label generated artwork or product mockups as real events.
- Don't identify people, confirm sponsor endorsement, or infer event dates from image filenames alone.
- `99-Reference/`: captured evidence. Social follower counts and prices are dated snapshots.
- Credentials stay in gitignored `CREDENTIALS.local.md` with mode 0600. Never echo them into reports.

## Next work

Onboarding is complete. Resolve `CLIENT-FOLLOWUP.md` and plan the website/registration work. Trello: https://trello.com/b/qwUSKYIS/red-white-and-clix. No social profile edits and no purchases made.

Status as of 2026-09-25: the site is built on Instatic and deployed to Railway **staging only** (`https://site-production-0334.up.railway.app`, `/admin` behind basic auth). Squarespace is still the live site; no DNS changed. Live on staging and verified: 40 sponsors, the November 2026 event page and listing, Register (links to HCUnits events 9151/9152), Donate (PayPal/Venmo), Support Us (volunteer section removed), /prizes, /shop (Shop in the menu). Edit through the Instatic admin API, not a seed push; see `deploy/railway/README.md` and Claude memory `rwc-instatic-railway-admin-api`. Clint clicks Publish.

2026-09-25 (later): Wesley's five replies are actioned on staging, all in DRAFT awaiting
Clint's Publish — sponsor corrections (Board & Dice only, Allplay added, "Pressed in Pink by
Zoe Lewellen", Blue Moon Comics + Kylee Rogers + Rebecca Gibson + Jaime Williams as Archivo
Black wordmark SVGs, Arni's confirmed), a homepage Mary T. Klinker beneficiary section that
states no allocation percentage, BCW quantity 6, and the stale "With thanks to" line removed.
Sponsor DATA is published; the static pages are not. Sponsor row edits go through
`PATCH /admin/api/cms/data/rows/:id` and media through `POST /admin/api/cms/media` in an
authenticated browser — the Data workspace is not exposed to the MCP content tools.

Open: one consolidated email to Wesley is drafted in Gmail and NOT sent (questions in `CLIENT-FOLLOWUP.md`); Squarespace store moves to `shop.redwhiteandclix.org` and DNS moves to Cloudflare at launch (`LAUNCH-DOMAIN-SWITCH.md`, held until Clint says); legal pages and the contact form still block launch.
