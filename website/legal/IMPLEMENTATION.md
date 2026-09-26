# What must be true before the rewritten policies can be published

The rewritten Privacy and Cookie policies make specific, checkable promises.
Publishing them before these are implemented would make the pages false, which
is worse than the accurate "no cookies" pages they replace.

## 1. Consent banner — blocks everything else

- [ ] Banner appears on first visit, on every page.
- [ ] **GA4 does not load until Accept is clicked.** Not "loads and waits" —
      the tag must not be on the page at all. A banner that appears after the
      tracker has already fired is decorative, and the Cookie Policy explicitly
      promises it is not.
- [ ] **Decline sets no cookies and sends no request to Google.**
- [ ] Accept and Decline are equally prominent. No pre-ticked boxes, no
      dark-pattern "Accept" in colour against a grey "Decline".
- [ ] The choice is stored in **localStorage**, not a cookie. The Cookie Policy
      says so explicitly, and storing "no" in a cookie would be self-defeating.
- [ ] Clearing site data makes the banner ask again.
- [ ] Banner is keyboard operable, has a visible focus outline, and is
      announced to screen readers — the Accessibility statement commits to
      WCAG 2.2 AA and this is a new blocking control on every page.
- [ ] Banner does not cover the page content permanently or trap focus.

## 2. Content Security Policy

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
