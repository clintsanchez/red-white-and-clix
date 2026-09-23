# Contact page

Page: https://red-white-and-clicks.local/contact/ (1217).

Reused the imported Elementor layout. Updated the title, introductory copy, logo, description, contact details, Facebook link and map address. Logo, description, mailing address, email, phone and Facebook URL use native Meta Box Options dynamic tags. Map query currently contains the confirmed GBP street address. Footer navigation unchanged.

Embedded existing WS Form 4, Contact Us, instead of creating a duplicate. Fields: first name (required), last name, email (required), optional phone, message (required), existing contact consent checkbox (required), Send message button. Page-scoped styling retains the kit's white fields and gold button.

## Form actions

- Save to Submissions.
- Notify `#option_get(options,email)` with subject `New contact inquiry — #option_get(options,s)`. Recipient resolves to redwhiteandclix@gmail.com.
- Reply-To uses `#field(30)`, the visitor email field, correcting the original submit-button reference.
- Redirect to the completed `/confirmation/contact/` page using the shared Single Confirmation template. An inline message remains as a fallback. Agency standard requires dedicated confirmation pages; see `12-CONFIRMATION-PAGES.md`.
- Honeypot enabled; generic Section label hidden; form republished.

WS Form API Allow Updates was initially disabled. The user explicitly authorized enabling it; it is now enabled. Form changes used WS Form abilities. The Reply-To and honeypot settings, not exposed by those edit schemas, were patched through the native WS Form meta API with normal capability checks.

## Verification

Published form definition verified: database, email and message actions; dynamic recipient; correct Reply-To and honeypot. Desktop/mobile screenshots and browser results are in `website/wordpress-contact/review/`. Browser validity checks cover empty required fields, invalid email and completed required fields without submitting. No test email was sent; live email deliverability remains untested and depends on the production mail setup.

Before-change backup (including full WS Form definition):
`/Users/clintsanchez/Local Sites/red-white-and-clicks/conf/backups/contact-page-20260923-000128.json`
