# Red White and Clix — organization research

Researched 2026-09-21. Intake and public-source research for BSC; no live account or website changes made.

## Source hierarchy

Use the GHL submission for client goals and preferences, IRS records for federal exemption, current HCUnits listings for event dates, and the client website/Facebook for self-published descriptions. Published claims are not automatically independently verified. Keep recommendations separate from facts. Raw client intake is in the gitignored `memory/ghl-onboarding-raw.json`.

## Organization and mission

Red White and Clix organizes tabletop gaming events, especially HeroClix, to build community and raise funds and awareness for veteran causes. The survey identifies veteran homelessness and suicide as the mission focus. The founder is Wesley (Wes) Robertson. The audience is gamers, veterans, military families and supporters, primarily Indiana and the Midwest, with sponsors as a secondary audience. Source: GHL submission and [official site](https://www.redwhiteandclix.org/).

The [About page](https://www.redwhiteandclix.org/about) describes Wes's Indiana Army National Guard service, personal connection to veteran support, and a memorial to his father, Major Edwin C. Robertson. These are self-published biographical claims. Use the founder's approved framing; detailed personal health history need not become default marketing copy.

The site identifies Mary T. Klinker Veterans Resource Center as the 2026 supported charity through its labeled graphic. It also presents testimonials and many sponsor logos. Obtain the current beneficiary arrangement, impact totals, and sponsor permissions before making stronger financial or endorsement claims.

## Verified federal record

The [IRS Indiana EO Business Master File](https://www.irs.gov/pub/irs-soi/eo_in.csv), retrieved September 21, contains RED WHITE AND CLIX INC, EIN 41-4723161, in care of Wesley Robertson. It lists subsection 03, status 01, ruling 202603, deductibility 1, foundation 15. The [IRS code guide](https://www.irs.gov/pub/irs-soi/eo-info.pdf) identifies these as 501(c)(3), unconditional exemption, a March 2026 ruling, deductible contributions, and public-support classification. Exact row saved in `99-Reference/irs-bmf-match.json`.

The ruling date is not the incorporation or first-event date. The survey says 3–5 years; Facebook says third year; the site references events in 2024 and 2025. Record these separately. Indiana corporate standing and the determination letter have not been independently retrieved.

## Current event, not the archived 2025 circuit

The [2026 HCUnits circuit](https://hcunits.net/circuits/red_white_and_clix_2026/) lists November 7–8, 2026 at Lafayette National Guard Armory, 5218 Haggerty Ln, Lafayette, IN 47905.

| Event | Listing on September 21 | Source |
|---|---|---|
| RWC 300 MODERN | Saturday November 7, 9 AM EST; $40; 300 points; open registration | [HCUnits 9151](https://hcunits.net/events/9151/) |
| Team Sealed | Sunday November 8, 9 AM EST; 3v3; listed fee $240 | [HCUnits 9152](https://hcunits.net/events/9152/) |

Confirm whether the team fee is per team and confirm check-in versus play time. The Modern listing displayed 3 players and Team Sealed 0 parties at capture; these are platform snapshots, not verified paid-registration totals. The [2025 circuit](https://hcunits.net/circuits/red_white_and_clix_2025/events/) is historical, dated November 15–16, 2025. Do not reuse those dates for the campaign.

## Goals and positioning from the survey

- Double website traffic and reach at least 80 registrations for the November event.
- Establish the details and finances for a secondary event within six months.
- Complete website overhaul; simplify ongoing maintenance.
- Professional, inspirational and warm voice. No politics or divisive content.
- Emphasize community, welcoming competition and tangible veteran support.
- Requested content includes social posts, short and long video, newsletters and infographics.
- Admired sites: Stack Up, Operation Gratitude and Wounded Warrior Project. These are inspiration references, not declared direct competitors.

## Findings that affect the next phase

1. **Registration consistency:** Squarespace `/services-store` displays $0 for Modern and Team Sealed, while HCUnits lists $40 and $240. A Hot Clix product displays $199 and sold out. Confirm the authoritative purchase route and remove conflicting stale listings during the rebuild.
2. **Donation confidence:** `/donate` contains placeholder FAQ answers, including deductibility and destination of funds. Federal exemption is now supported by IRS data, but actual fundraising allocation and receipt language still need organizational confirmation.
3. **Facebook identity drift:** Public Facebook links the old `site-l8hvdft0w.godaddysites.com` domain and a Yahoo email, while the survey and current site use redwhiteandclix.org and redwhiteandclix@gmail.com. Facebook's address is the event armory; the website/IRS address is the organization mailing location. These have different roles, not necessarily an error.
4. **Two merchandise catalogs:** Squarespace sells shirts, accessories and gaming maps; the separate Printify shop displays apparel and a blanket. Confirm which catalog should be primary and preserve order fulfillment expectations.
5. **Hotel block:** Homepage advertises a $399 nightly group rate and October 7 deadline. Confirm directly with the organizer before promoting; no booking was made.
6. **Measurement:** No traffic baseline or paid-registration reconciliation was supplied. Define the comparable traffic period and track registration clicks and confirmed bookings separately.
7. **Photo quality:** Real event images are available, including room-wide play, group photos and prizes. Some founder/archive photos are only 206×206. AI-named artwork and product mockups are separately flagged and must not be presented as event photography.
8. **Content quality:** One indexed image description incorrectly describes the organization as a reality TV show. Donation statistics lack dated citations on the captured page. Correct metadata and validate those statistics before reusing them.

## Research boundaries

Facebook's public profile was readable; its full history may require login. Google Business Profile stopped at an unusual-traffic challenge. Candid stopped at security verification. Neither challenge was bypassed. An IRS primary-source check supplied the federal nonprofit verification independently. No additional organization-owned Instagram, LinkedIn company page, YouTube, X, TikTok or Discord account was verified through survey, website links, or public search. Absence from search does not prove an account does not exist.

## Evidence

- `99-Reference/site-snapshot/`: 27 sitemap pages, plain-text captures, page/link inventory, homepage source and sitemap.
- `99-Reference/facebook.json` and `facebook.png`: public page capture.
- `99-Reference/printify.json`: current public product catalog capture.
- `99-Reference/candid.json`: recorded access limitation.
- `99-Reference/hcunits-*.txt`: current event details.
- `06-Reports/site-assets-manifest.json`: every downloaded source, hash, dimensions and categorization.
- `06-Reports/facebook-assets-manifest.json`: separate Facebook collection outcome.
