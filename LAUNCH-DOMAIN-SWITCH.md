# Domain switch runbook: redwhiteandclix.org → new site

Decided 2026-09-25 (Clint): for this phase the Squarespace store STAYS, moved to
`shop.redwhiteandclix.org`. The new Instatic site on Railway takes over
`redwhiteandclix.org` and `www`. Target: mid-October 2026, well before Nov 7–8.

Nothing here has been done yet. Every step changes live DNS or a live store.

## Current state (checked 2026-09-25)

| Item | Value | How checked |
|---|---|---|
| Registrar | Squarespace Domains (ex-Google Domains), expires 2027-03-18 | `whois` |
| DNS host | Squarespace, `ns-cloud-a1..a4.googledomains.com` | `dig NS` |
| Apex A | 198.185.159.144/145, 198.49.23.144/145 (Squarespace) | `dig A` |
| www | CNAME `ext-sq.squarespace.com` | `dig CNAME` |
| MX | none. Email is redwhiteandclix@gmail.com, unaffected by the move | `dig MX` |
| TXT | `google-site-verification=ZSSjNf…` (keep), `v=spf1 -all` (keep) | `dig TXT` |
| shop. | does not exist | `dig` |

## The blocker: Squarespace DNS cannot point the apex at Railway

Railway needs CNAME flattening / ALIAS for a root domain. Its docs
(docs.railway.com/networking/domains/working-with-domains) list SquareSpace
among providers that do NOT support it; Cloudflare does. So:

**Move DNS hosting to Cloudflare (free). The registration stays at Squarespace.**

## Steps, in order

1. **Access.** Wesley's Squarespace login (or Clint added as a contributor with
   domain + commerce permissions). A Cloudflare account (agency or Wesley's).
2. **Cloudflare zone.** Add `redwhiteandclix.org`; import records. Confirm the two
   TXT records came across. Do NOT change nameservers yet.
3. **Squarespace store on shop.** In the Squarespace site: Settings → Domains →
   connect `shop.redwhiteandclix.org`; add the records it gives to the
   Cloudflare zone (DNS only / grey cloud). Make `shop.` the Squarespace site's
   primary domain once it verifies.
   - Hide or unlink the non-shop Squarespace pages (Home, About, Donate,
     services-store) so the old site does not live on as a duplicate.
   - Same pass: rename the product URL slugs and add Squarespace URL Mappings
     old→new (see "Product slugs" below).
4. **Railway custom domain.** On the `site` service add `redwhiteandclix.org` and
   `www.redwhiteandclix.org`. Add the CNAME + TXT records Railway gives to
   Cloudflare. Per Railway docs: if proxied (orange cloud) set SSL/TLS to
   **Full**, not Full (Strict).
5. **Nameservers.** In Squarespace Domains, switch nameservers to Cloudflare's.
   This is the actual cut-over moment. Railway issues certificates within ~1 hour.
6. **Railway variables.** Set `PUBLIC_ORIGIN` on `cms` to
   `https://www.redwhiteandclix.org` (origin checks reject requests otherwise;
   see deploy/railway/README.md). Decide apex vs www as canonical and redirect
   the other.
7. **Redirects** for every old Squarespace URL (below), at the Caddy `site` edge.
8. **Update the new site's Shop page links** from `www.redwhiteandclix.org/shop/p/…`
   to `shop.redwhiteandclix.org/shop/p/…` (new slugs), then publish.
9. **Verify** (cache-busted): every old URL returns 301 to the right place; new
   pages 200; shop checkout works on `shop.`; certificate valid on apex + www;
   Google Search Console property still verified.

## Redirects for old Squarespace URLs (27, from its sitemap 2026-09-25)

| Old | New |
|---|---|
| `/home` | `/` |
| `/about` | `/mission` |
| `/donate` | `/donate` (same path) |
| `/shop` | `/shop` (new page, same path) |
| `/shop/p/*` (21 products) | `https://shop.redwhiteandclix.org/shop/p/*` (then Squarespace maps old slug → new slug) |
| `/services-store`, `/services-store/*` (4) | `/register` |

Draft Caddy rules for `deploy/railway/edge/Caddyfile` (NOT applied):

```
redir /home / 301
redir /about /mission 301
redir /services-store /register 301
redir /services-store/* /register 301
@oldProduct path /shop/p/*
redir @oldProduct https://shop.redwhiteandclix.org{uri} 301
```

## Product slugs (Squarespace, rename in step 3)

| Product | Current slug | Proposed |
|---|---|---|
| RWC '25 Indoor | `product-2-5c6mb-j8mng-mp2lh` | `rwc-25-indoor-map` |
| RWC '25 Outdoor | `sjgqorj9whmeyoxjfmhyb8sgidl8hs` | `rwc-25-outdoor-map` |
| Temple Ruins, Outdoor | `temple-ruins-outdoor` | `temple-ruins-outdoor-map` |
| T-Shirt, Original Style | `t-shirt` | `rwc-original-style-tee` |
| T-Shirt, 2025 Variant | `t-shirt-hch6s` | `rwc-2025-variant-tee` |
| T-Shirt, Red. White. And Clix. | `t-shirt-z3z8h` | `red-white-and-clix-tee` |

Not verified: whether Squarespace auto-redirects a changed product slug. Add
URL Mappings regardless.

## Other launch blockers (not DNS) — reassessed 2026-09-26

- ~~Contact form: not wired~~ **NOT A BLOCKER. There is no contact form anywhere
  on the new site** — verified across every page. Contact is the email and phone
  links. The Privacy Policy now says so explicitly.
- ~~Legal pages: no attorney review~~ Clint's call, taken: ship. The pages now
  describe the site accurately for a launch with **no analytics, no cookies and
  no form**; the consent banner is built but dormant until a GA4 ID is set.
- Robots/canonical: staging canonicals already point at the real domain; re-check
  after the switch that nothing still references the Railway URL.
- **Assets that exist only on Squarespace.** The WLFI interview video was one of
  these and would have died with the switch — it is now saved to
  `99-Reference/media/`. Sweep for anything else before the store is touched.
- **Re-verify the event page after every publish.** It silently reverted once
  (see `CLIENT-FOLLOWUP.md`); the body is committed at
  `website/instatic/event-november-2026-body.md` for restoring verbatim.

## Squarespace store restyle — DONE 2026-09-26 (live)

Custom CSS saved and serving from Squarespace's `custom.css`. Source of truth:
`website/squarespace-custom.css`. Verified on the public product page, not just
in preview: ink header, surface body, ink title/price, action-red ADD TO CART at
10px radius, ink footer, nav contrast 17.74:1.

Two things preview caught that guessing would not have:

- `.header-nav-folder-title` is a `<button>` Squarespace paints pure black.
  Putting an ink background behind it made the "Veteran Resources" nav item
  **invisible**. Any future header work has to invert that class too.
- The product classes are 7.1, not 7.0: **`h1.product-title` and
  `.product-price`**, not `.ProductItem-*`. Squarespace's own rules outrank
  them, so they need `!important`.

Still to do on the store, none of it blocking: repoint the store nav back at the
main site (config, not CSS), and rename the 21 Printful catalogue product names
("Unisex t-shirt", "White glossy mug") which is a bigger UX win than the CSS was.

### Address: decided, leave it

The footer block was edited to read "West Lafayette, Indiana" instead of the
street address. The full street address plus `mapLat`/`mapLng` remains in
**Settings → Business Information**, which Squarespace emits into three JSON-LD
blocks per page. **Clint's call 2026-09-26: that is canonical, leave it.** Do
not re-litigate. If it ever does change, a PO box or the Armory address is the
usual answer for a nonprofit, not blank.

## Sequencing note (2026-09-26)

The step order above flips nameservers *last*, which means the apex, www, shop
and the Railway certificates all change in one moment. Safer alternative:

1. Build the Cloudflare zone with records **identical to today's**, verify them.
2. Flip nameservers early. Nothing visible changes — Squarespace still serves.
3. Then add `shop.`, then Railway's records, testing each before the apex moves.
4. Repoint apex + www last, as a single small change you can revert.

Same destination, but each step is independently verifiable and reversible
instead of one simultaneous cut-over.
