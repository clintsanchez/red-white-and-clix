# What must be true before the rewritten policies can be published

> **STATUS 2026-09-27 — ANALYTICS IS LIVE.** GA4 `G-GTE1H95NCS` is firing on
> `www.redwhiteandclix.org`, behind the consent banner, confirmed in Google
> Analytics Realtime and verified independently in a browser: before Accept
> there is no `googletagmanager` request, no `dataLayer` and no beacon; after
> Accept the tag loads and one collect beacon is sent. The choice persists as
> `rwc-consent: granted`.
>
> Sections 1 and 2 are done. **Sections 3 and 4 are now overdue, not pending** —
> the Privacy and Cookie pages still say the site runs no analytics, and that
> is false as of today. Both pages promise in writing that they would be
> updated *before* tracking went live, not after. Fixing that wording is the
> next thing that happens on this file.

The rewritten Privacy and Cookie policies make specific, checkable promises.
Publishing them before these are implemented would make the pages false, which
is worse than the accurate "no cookies" pages they replace.

## 1. Consent banner — BUILT 2026-09-25 and behaviour-tested

`src/scripts/consent.js` (source of truth: `website/instatic/scripts/consent.js`),
all-pages runtime, body-end. Every item below was verified by driving the real
script and the real published CSS in a browser, not by reading the code:

- [x] Banner appears on first visit, on every page.
- [x] **GA4 does not load until Accept is clicked** — verified no
      `googletagmanager` script and no `dataLayer` exist before the click.
- [x] **Decline sets no cookies and sends no request to Google** — verified
      `document.cookie` empty and no GA script after declining.
- [x] Accept and Decline are equally prominent — same class, same computed
      background and colour, both 44px tall and 120px wide. Decline is first in
      the DOM, so it is first in the tab order.
- [x] The choice is stored in **localStorage** (`rwc-consent`), not a cookie.
- [x] Reopening works — a "Cookie settings" button in the footer clears the
      stored answer and brings the banner back, then focuses its first button.
- [x] Keyboard operable with a visible focus outline; banner is the first child
      of `<body>` so it is reachable without tabbing the whole page. Focus moves
      to `<main>` on dismissal rather than being dropped on `<body>`.
- [x] Non-modal, bottom-anchored, does not trap focus.
- [x] GA loader verified with a stub ID: emits `js` + `config` with
      `allow_google_signals: false`, `allow_ad_personalization_signals: false`,
      `cookie_expires: 33696000` (13 months) and `anonymize_ip: true`.

**`GA_MEASUREMENT_ID` is set to `G-GTE1H95NCS`** as of 2026-09-27, and a
cross-domain linker covers `redwhiteandclix.org` and `shop.redwhiteandclix.org`.
The linker flag alone is not enough: both hosts must also be registered on the
GA4 property, or every journey to the store is logged as a referral and no
purchase is credited to what earned it. See section 3.

## 2. Content Security Policy — DONE 2026-09-27, via `blaksheep.csp` v1.0.2

There is **no CSP site setting**. `/admin/api/cms/site` has no such field; the
publisher hardcodes the meta tag. Changing it means a `publish.html` filter,
the same hook `plugins/blaksheep-seo` already uses to rewrite published HTML.
Do not bolt it onto the SEO plugin — it needs its own small plugin.

Built as `website/instatic/plugins/blaksheep-csp` and installed as
`blaksheep.csp` v1.0.2, permissions `["cms.hooks"]` only. The published policy
is now:

```
script-src  'self' https://www.googletagmanager.com
connect-src 'self' https://www.google-analytics.com https://*.analytics.google.com
                   https://*.google-analytics.com https://*.googletagmanager.com
```

Nothing else widened, and `'unsafe-inline'` is never added — `consent.js` is an
external file and needs none.

**An `allowAnalytics` setting turns the whole rewrite off**; switch it to Off
and republish to restore the self-only policy. That is the rollback, and it has
already been used in anger.

Three things cost real time here, recorded so they are not rediscovered:

- **v1.0.0 broke the live site.** The regex was `content=["']([^"']*)["']`, and
  a CSP value contains `'self'`, so it captured only `default-src ` and emitted
  a policy with an empty `default-src` and `script-src` twice. Browsers honour
  the *first* occurrence of a directive, so the site's own JavaScript was
  blocked for every visitor until the kill switch was flipped. The filter now
  refuses to emit anything containing a duplicate or empty directive.
- **v1.0.1 installed clean and did nothing.** It reported active with no error
  across two publishes. The cause was a named export alongside the default;
  Instatic decides whether a module is a plugin by sniffing the default export,
  so `activate()` never ran. Export a default and nothing else.
- **The manifest is `plugin.json`,** `author` is `{name, url}` not a string,
  setting `type` is a closed union that excludes `boolean`, and declaring an
  `entrypoints.editor` demands the `editor.code` permission — which grants
  unsandboxed JavaScript in the admin window and is not worth taking for a
  server-only plugin.

## 3. GA4 property settings — DONE 2026-09-27

Property `556079419`, stream "RWC Website", `G-GTE1H95NCS`. Set in the GA admin
and checked on screen; the rename is also confirmed through the Data API.

- [x] **Google Signals: OFF** — was already off.
- [x] **Ads personalisation: disallowed in 0 of 307 regions.** Was *allowed in
      all 307*. The tag already sent `allow_ad_personalization_signals: false`,
      but the Privacy Policy says personalisation is disabled, so the property
      now matches the words.
- [x] **User-provided data collection: OFF** — was already off.
- [x] **Event data retention: 14 months** — was the 2-month default. User data
      was already 14.
- [x] **No Google Ads links.**
- [x] **Domains: `Ends with redwhiteandclix.org`.** Google had suggested an
      *exact* match on the bare domain, which matches neither `www.` nor
      `shop.` — the hosts actually in use.
- [x] Renamed from "Red White and Clix Email" to "Red White and Clix — Website".
- [x] Time zone `America/New_York`, currency USD — correct as created.
- [ ] **Add Wesley as an administrator.** The property was created on
      2026-09-26 by the agency; the data should be the nonprofit's.

**Correction to earlier notes:** the Squarespace store at
`shop.redwhiteandclix.org` carries **no Google tag at all**. Store visits and
purchases are therefore not measured, whatever the domain settings say — the
linker in `consent.js` cannot credit a sale nothing is recording. And because
`www.` and `shop.` share a registrable domain, GA4 would share its cookie across
them without cross-domain linking anyway. Measuring the store means adding the
tag in Squarespace, which would also need the store to gate it on consent to
keep the Cookie Policy true. Not done; a decision for later.

## 4. Contact form → GoHighLevel

- [ ] Submitted **server-side** to the GHL API. Do not embed a GHL form or
      script: `frame-src 'none'` and `script-src 'self'` both forbid it, and the
      Privacy Policy states GHL "sets no cookies on this site".
- [ ] Fields limited to name, email, optional phone, message. The policy says
      "only what you type" — do not silently attach IP, referrer or UTM tags to
      the contact record.
- [ ] Phone genuinely optional, and labelled as such.
- [ ] **No automatic mailing-list opt-in.** The policy promises this in bold.
      If a GHL workflow adds contacts to a campaign, it must be disabled.
- [ ] A deletion path exists that actually removes the GHL record.
- [ ] Two-year retention after last contact is set or diarised. A promise with
      no mechanism behind it is not a retention policy.

## 5. Consistency sweep

- [ ] Terms and Conditions still say registration is not completed on this site
      — still true, GHL only receives an enquiry. Re-read after the form is wired.
- [ ] Nothing else on the site claims "no cookies" or "no analytics".
- [ ] Set the **Last updated** date on both pages, and remove the draft banners,
      only when all of the above is done.

## 6. Still needs a lawyer

Wesley has no attorney. These pages are written to be accurate and readable, not
to be legal advice, and the Terms are flagged in their own text as the page that
most needs counsel. The honest position to give him: accurate self-description is a
good foundation, and it is not a substitute for review.

## 5. Policy wording — DONE 2026-09-27

Both pages were rewritten in the CMS the same day analytics went live, which
is the order they promise. Verified by fetching the published pages and
grepping for every stale phrase: "does not run analytics", "sets no cookies at
all", "not yet published", "no analytics are running", "before it goes live,
not after" — all gone from both.

Also corrected a mistake that predates analytics: both pages named **Printify**
as the merchandise store. The live store is Squarespace at
`shop.redwhiteandclix.org`. Printify is a second, smaller storefront that
`/shop` still links to, and that duplication is unresolved — see the QC notes.

**Deliberately not stated: a data-retention period.** The property is on
Google's defaults and nobody has confirmed the number, so the policy describes
the mechanism instead of asserting a figure. If a number is wanted, read it off
the GA4 property first and then add it here — an unverified retention claim is
exactly the kind of thing these pages exist to avoid.

Still true and still outstanding: neither page has been reviewed by a lawyer,
and both still carry the "Draft for review" notice saying so.
