# Red White and Clix — handoff

Updated September 21, 2026. **Intake, research and design deliverables complete. Website planning prepared; implementation remains pending decisions and access.**

Start with [onboarding status](ONBOARDING-STATUS.md) and [website planning](08-Website-Planning/README.md).

## Completed

- Original GHL survey retained in the existing client brief; no repeat intake.
- Existing organization, records, social, asset, marketing and SEO research in `06-Reports/` and `99-Reference/`.
- Supplied logo, brand package and selected documentary image references preserved.
- 77-page design system PDF/HTML; 45 components; 224 editable templates and PNG previews; 74 tokens and bundled fonts.
- Separate nine-variant vector logo kit in SVG, vector PDF and PNG. Alternative arrangements remain proposed.
- Five Agency-in-a-BOX files reconciled with existing research and restored to the local canonical client folder; dashboard updated without replacing other client records.
- Website scope brief, home/events/about/donation drafts, measurement/access handoff, focused decision sheet and 14-item implementation backlog.

## Immediate review

1. Settle website platform, scope, budget, target milestone and maintenance owner.
2. Reconcile the recorded Squarespace/HCUnits pricing conflict and choose the authoritative checkout for each event format.
3. Define the 80-registration goal; establish real registration counts and a traffic baseline.
4. Arrange delegated access to the relevant website, registration, analytics and Facebook accounts.
5. Confirm beneficiary/allocations/receipts and permissions before donor/sponsor/photo content is released.

Current event facts are carried from September 21 research: November 7–8, 2026, Lafayette National Guard Armory. Recheck the affected facts before publication. The event venue and mailing address have different roles.

## Access and evidence boundaries

The recorded current platform is Squarespace. A platform change is not yet settled. No website deployment, profile edit or client message occurred during this continuation. Recurring publishing and completed-registration tracking are not configured.

Existing reports record GBP/Candid verification limits, missing analytics baselines, uncollected primary interviews and unavailable quantitative SEO data. Those limits remain. A credential-file reference does not prove working account access on this machine; secrets must stay out of shared documents.

## Current locations

- Working repository: `/Users/clintsanchez/Documents/Claude/Red, White, and Clix/`
- Git remote: `https://github.com/clintsanchez/red-white-and-clix.git`; repository cloned on `main`. New deliverables have not been committed or pushed in this session.
- pCloud client: `/Users/clintsanchez/pCloud Drive/Documents/BlakSheep Creative/Clients/Red White and Clix/`
- Agency client: `/Users/clintsanchez/Documents/Claude/agency-in-a-box/Agency-in-a-BOX/vault/01-Clients/Red White and Clix/`
- Downloads: `/Users/clintsanchez/Downloads/Red White and Clix Design Kit/`
- Existing Trello board: https://trello.com/b/qwUSKYIS/red-white-and-clix — referenced from prior handoff; not modified or reverified in this continuation.

See [CLIENT-FOLLOWUP.md](CLIENT-FOLLOWUP.md) for the complete unresolved list. Answers should update the [decision log](08-Website-Planning/04-DECISIONS-FOR-WES.md).

## Website preview — September 21, 2026

A platform-neutral local preview now implements Home, Events, Our story and Give, with internal review notes. Open [the preview](website/preview/index.html). It uses the design-system tokens/fonts and supplied original logo. Registration/donation controls remain disabled until authoritative links and facts are confirmed. No website account changes or deployment have occurred.

Verification passed for five pages at 1440, 768, 390 and 320px: no horizontal overflow, one H1 per page, local links/anchors, images, mobile navigation, FAQ disclosures, disabled checkout and the keyboard skip link. Screenshots and results are in `website/preview/review/`. Platform, budget, access and remaining fact decisions are still open.


## September 22 — local Elementor template framing

Clint selected Elementor and uploaded the Triple-A kit. The current pass preserves template content and styling; it does not apply project copy or the earlier custom website preview. Twelve page layouts are inserted, shared Theme Builder templates assigned, missing original navigation/logo restored, and local visibility settings corrected. See [template placement](08-Website-Planning/07-ELEMENTOR-TEMPLATE-PLACEMENT.md). Events and Donate remain drafts. Production migration/launch remains separate.


## September 22 — Events content type and templates

Created the Meta Box Events CPT and 25 fields, with Elementor Single Event (1459), Events Archive (1460) and Event Card (1461) templates assembled from the imported kit. Archive: `/events/`. Real event entries are still pending verified details. Temporary test records were removed. See [Events implementation](08-Website-Planning/08-EVENTS-IMPLEMENTATION.md).

## Header/footer branding pass — September 22, 2026

Existing Elementor Header 1304 / Footer 1273 now use supplied RWC logo attachment 1491 with responsive sizing. Footer organization/newsletter copy, confirmed contact details, and copyright updated. Existing kit layout, colors, typography and navigation preserved. Fixed inherited paragraph overlaps and mobile contact wrapping. Global kit logo was not changed. Placeholder sponsor assets, social destinations, legal/footer menu destinations, and newsletter integration remain pending. No forms submitted. See `08-Website-Planning/09-HEADER-FOOTER-IMPLEMENTATION.md` and `website/wordpress-header-footer/review/` for backup location and review artifacts.

## Global options wiring — September 22, 2026

Header/footer now derive logo and business details from the existing Options → Global Settings Meta Box group (25), option array `options`, rather than static widget values. Existing field IDs retained; `ceo` relabeled Founder / Contact. Five missing fields added. Native Meta Box Elementor tags supply logos, footer paragraphs, copyright company name, contact text and mailto/tel links. Footer navigation unchanged. No new runtime plugin. Nine in-memory substitution checks plus desktop/mobile browser checks passed. See `08-Website-Planning/10-GLOBAL-OPTIONS.md` for keys, backup and scope.

## Contact page and WS Form

Contact page 1217 now has RWC copy and dynamic Meta Box business details, correct address map, and WS Form 4. Form actions save inquiries, notify the Options email, and show an on-page confirmation. Reply-To fixed to visitor email field 30; honeypot enabled. User authorized WS Form API Allow Updates. No external test email sent. See `08-Website-Planning/11-CONTACT-PAGE.md`.

## Agency confirmation-page standard

All agency forms use dedicated confirmation pages, per user instruction. Do not replace redirects with inline-only messages. Created shared Elementor Single Confirmation 1510 for the existing confirmation CPT, Meta Box Confirmation Content group 1508, and contact confirmation 1509 (`/confirmation/contact/`). WS Form 4 published redirect restored. Based on Divine Cleaning and Tiger Town patterns, styled with current RWC components. See `08-Website-Planning/12-CONFIRMATION-PAGES.md`.

Confirmation template 1510 now uses the agency 66/33 content/sidebar pattern: dynamic confirmation text on the left; Call us, Email us and Visit Facebook buttons on the right, sourced from global Options. Stacks on mobile. Export refreshed.
