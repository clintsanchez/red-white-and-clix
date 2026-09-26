# What must be true before the rewritten policies can be published

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

**`GA_MEASUREMENT_ID` is still empty**, so Accept currently records the choice
and loads nothing. That is deliberate — it keeps the build order the policies
promise. Setting it is step 3 below, and is NOT sufficient on its own without
step 2.

## 2. Content Security Policy — still open, and it is a plugin job

There is **no CSP site setting**. `/admin/api/cms/site` has no such field; the
publisher hardcodes the meta tag. Changing it means a `publish.html` filter,
the same hook `plugins/blaksheep-seo` already uses to rewrite published HTML.
Do not bolt it onto the SEO plugin — it needs its own small plugin.

Current meta CSP is `default-src 'self'; script-src 'self'` — **this blocks GA4
outright.** It must be loosened, minimally:

```
script-src 'self' https://www.googletagmanager.com;
connect-src 'self' https://www.google-analytics.com https://*.analytics.google.com https://*.google-analytics.com;
img-src 'self' data: https:;
```

Loosen no further than needed. Do **not** add `'unsafe-inline'` to `script-src`
to make a GTM snippet work — use an external file or a nonce.

## 3. GA4 property settings

Each of these is asserted in the Privacy Policy and must match:

- [ ] **Data retention: 14 months** (default is 2 months — must be changed).
- [ ] **Google Signals: OFF.**
- [ ] **Advertising personalisation: OFF.**
- [ ] **Cookie expiry: 13 months** (`cookie_expires: 33696000`). GA4 default is
      2 years; the Cookie Policy table says 13 months.
- [ ] No User-ID and no Measurement Protocol uploads.
- [ ] No Google Ads link.
- [ ] Confirm the property is on the nonprofit's own Google account, not an
      agency account, so the data is theirs.

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
