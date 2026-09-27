# Make the store match www — Squarespace steps (Basic plan)

Everything below is done in the store's Squarespace admin
(`arugula-lily-jaaz.squarespace.com/config`). The automated session was
stopped by a permission check before these could be applied, so they are
listed in order for a person to do.

## 1. Custom CSS
Website → Pages → Website Tools → **Custom CSS**. Replace the contents with
`custom-css.css` from this folder. Save.

Previewed on the live store: header 106 px (www 107), 64 px logo, pill nav in
Space Grotesk 15.17 px white, red #b91c1c pill buttons, Archivo Black product
titles, black footer, "Made with Squarespace" hidden, no horizontal overflow
at 1440 or 390 px.

## 2. Shop as the homepage
Pages → Shop → ⚙ → **Set as Homepage**. (Clicked during the session but not
confirmed; check it took.)

## 3. Navigation
In **Main Navigation** keep only Shop. Add four **Link** items (+ → Link) and
order them:

| Title | URL |
|---|---|
| Events | https://www.redwhiteandclix.org/events |
| Our Mission | https://www.redwhiteandclix.org/mission |
| Veteran Resources | https://www.redwhiteandclix.org/resources |
| Shop | (the existing Shop page) |
| Support Us | https://www.redwhiteandclix.org/support |

## 4. Header button → Donate
Edit the site header → **Button**. It currently reads "Register today" and goes
to HCUnits. Change to text **Donate**, link
`https://www.redwhiteandclix.org/donate`. On www the red header pill is
Donate; Register lives in the page content.

## 5. Retire the old pages
**Disable** (page ⚙ → turn the page off) — do not just unlink, because
Squarespace ignores a redirect while a page still exists at that URL:
Home, Donate, Events (`/services-store`), Sponsors, About, the Veteran
Resources folder and its List of Resources page, and New Dropdown.

**Check the old Events store first.** `/services-store` is a product
collection with event-entry products (300 Modern, 3v3 Team Sealed, and a third).
If any are still purchasable, someone can pay for an entry here instead of
registering on HCUnits. Disable or delete those products.

## 6. Redirects
Settings → Developer Tools → **URL Mappings**, paste:

```
/home -> /shop 301
/about -> https://www.redwhiteandclix.org/mission 301
/donate -> https://www.redwhiteandclix.org/donate 301
/services-store -> https://www.redwhiteandclix.org/events 301
/services-store/november-event -> https://www.redwhiteandclix.org/events/november-2026 301
/services-store/p/300-modern-1 -> https://www.redwhiteandclix.org/register 301
/services-store/p/3v3-team-sealed -> https://www.redwhiteandclix.org/register 301
/services-store/p/advanced-service-bjxak -> https://www.redwhiteandclix.org/register 301
```

## 7. Footer content
Edit the footer section so its text matches www. Three columns plus a bar:

- **Red, White, and Clix** — "A veteran-founded tabletop event community." —
  "One Community. One Mission."
- **Explore** — Events, Our Mission, Founder's Story, Veteran Resources, Shop,
  Support Us (all to www except Shop)
- **Get in touch** — redwhiteandclix@gmail.com · (574) 265-9585 · button
  "Register for Nov 7–8" → https://www.redwhiteandclix.org/register
- Bar: "© 2026 Red, White, and Clix" · Privacy · Terms · Accessibility ·
  Cookies · Disclaimer · Sitemap (all to www)

Remove the old "Founded by disabled Army National Guard veteran…" block.
Colours and fonts come from the CSS; only the words and links need changing.

## What cannot match on Basic
- **Mobile menu**: Squarespace's own overlay, restyled black, not the www burger.
- **Checkout**: hosted by Squarespace; only logo and colours are configurable
  (Commerce → Checkout).
- **Cookie banner**: Squarespace's, restyled to the site's colours, with its own
  wording.
Upgrading to Core would allow `code-injection-*.html`, which removes the first
and makes the header and footer identical to www.
