# Shared confirmation pages

## Agency standard

User direction: all agency websites use a dedicated confirmation page after form submission. Preserve/create the appropriate page and redirect action. An inline success message may remain as a fallback, but does not replace the confirmation page.

## Reference pattern

Reviewed the saved Elementor confirmation screenshot from Divine Cleaning (`confirmation-quote.png`), Tiger Town Construction's `memory/ttc-confirmation-pages.md`, and TL Septic's exported confirmation Meta Box schema. Pattern: Confirmation CPT, shared Elementor Single Confirmation template, field-driven heading/message, next steps and follow-up buttons. Local TCMHA and Load and Geaux database snapshots also contain the standard Confirmation CPT but no finished Elementor confirmation template. Other sites were read only.

## Implemented on Red White and Clix

- Existing `confirmation` CPT retained.
- Meta Box group 1508: Confirmation Content (`confirmation-content`).
- Elementor Theme Builder template 1510: **Single Confirmation**, condition `include/singular/confirmation`.
- Contact confirmation post 1509: https://red-white-and-clicks.local/confirmation/contact/.
- Existing contact page hero/body shells and 404 button reused with this site's global styles. Other clients' design assets were not imported.
- Fields: `conf_h1`, `conf_content`, `conf_next_steps`, `conf_button_label`, `conf_button_url`, `conf_secondary_label`, `conf_secondary_url`.
- Contact copy confirms receipt, explains review/follow-up, and links to Events and Home. No invented response-time guarantee.
- WS Form 4 retains database/email actions and inline fallback; published redirect now points to `/confirmation/contact/`.
- SEOPress confirmation single/archive noindex enabled independently of local site-wide noindex. Existing four blueprint confirmation posts retained; template has generic fallbacks. They still need tailored copy before use by other forms.

## Reuse

Create or duplicate a post under **Confirmations**, choose a slug, and populate its Confirmation Content fields. The shared layout applies automatically. Set its WS Form redirect to the resulting permalink and republish the form. Duplicate the Theme Builder template only if a genuinely different layout is required, with non-overlapping display conditions.

An Elementor JSON export is available at `website/wordpress-confirmations/single-confirmation.json`. Cross-site imports require mapping the destination site's global styles/assets and setting display conditions; this export references the current site's media/global IDs.

## Verification

Contact confirmation returns HTTP 200 at 1440/390 px, one correct H1, both correct CTA links, no horizontal overflow, and a noindex robots tag. Published WS Form action inspected and points to the correct URL. No external email or real form submission was sent. Screenshots/results: `website/wordpress-confirmations/review/`.

## Sidebar layout refinement

Updated per user approval: 66.666% content / 33.334% right sidebar on desktop and tablet, stacked in content-first order on mobile. The hero has one Confirmation H1; the left column contains the field-driven confirmation heading/message, next steps and follow-up buttons. The right column contains Stay connected and three full-width buttons: Call us, Email us, Visit Facebook. Destinations use Meta Box Options (`phone_address`, `email`, `facebook_url`). Desktop 1440, tablet 768 and mobile 390 checks showed no horizontal overflow and the correct column proportions/stacking. Backup: `conf/backups/confirmation-sidebar-20260923-002557.json` under the Local site.
