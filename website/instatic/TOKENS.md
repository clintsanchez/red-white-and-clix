# Instatic Core Framework tokens — applied September 22, 2026

Applied to the local Instatic instance (localhost:3022) from
`design-system/tokens/tokens.json` and `website/css-tokens.css`.

## Colors — 9 tokens

| Token | Hex | Role |
|---|---|---|
| `--rwc-logo-red` | #FF0000 | Mark and non-text accents ONLY. ~4:1 on white, fails as text |
| `--rwc-logo-blue` | #0072FF | Mark and non-text accents |
| `--rwc-action` | #B91C1C | Buttons, primary CTA, anything text-bearing in red |
| `--rwc-link` | #0050B3 | Links, focus ring |
| `--rwc-ink` | #111827 | Body text, inverse section grounds |
| `--rwc-surface` | #F5F7FA | Light section grounds |
| `--rwc-border` | #D1D5DB | Card and control borders |
| `--rwc-white` | #FFFFFF | Established |
| `--rwc-black` | #000000 | Established |

Instatic auto-generates opacity steps (`-5` .. `-90`), darker shades (`-d-1..4`)
and lighter tints (`-l-1..4`) for each, plus `text-` / `bg-` / `border-`
utility classes.

## Fonts

- `var(--font-rwc-font-heading)` — Archivo Black 400, self-hosted, latin
- `var(--font-rwc-font-body)` — Space Grotesk 400/500/700, self-hosted, latin

Note the doubled `font-` prefix: Instatic prepends `font-` to the `variable`
value. Renaming would orphan the originals (there is no delete-token tool), so
the names stand as-is.

## Scales — TUNED EMPIRICALLY, DO NOT TRUST THE INPUTS

`site_set_type_scale` and `site_set_spacing_scale` do NOT emit the px values you
pass. First attempt: requested a 14px base, got 17.1px; requested a 4-96px
spacing ramp, got 1-32px. The inputs below are the DETUNED values that produce
the correct output. Re-read with `site_read_styles` after any change.

Type — `min {fontSize: 11.45, scaleRatio: 1.145}`, `max {fontSize: 14.4, scaleRatio: 1.2}`,
steps `xs,s,m,l,xl,2xl,3xl,4xl`, group `aquHrN5XgU7KaMOaDkPer`:

| Var | Renders | Kit target |
|---|---|---|
| `--text-xs` | 13.9 -> 16px | caption 14 |
| `--text-s` | 16 -> 19.2px | label 16 |
| `--text-m` | 18.4 -> 23px | body 18 |
| `--text-l` | 21 -> 27.7px | - |
| `--text-xl` | 24 -> 33px | h3 24 |
| `--text-2xl` | 27.5 -> 39.8px | h2 28-48 |
| `--text-3xl` | 31.5 -> 47.8px | - |
| `--text-4xl` | 36 -> 57.3px | h1 36-72 |

`--text-4xl` tops out at 57px, short of the kit's 72px h1. Display headings use
an explicit `clamp(36px, 5vw, 72px)` class instead of the top ramp step.

Spacing — `min {size: 16.7, scaleRatio: 1.485}`, `max {size: 23.5, scaleRatio: 1.5}`,
steps `3xs,2xs,xs,s,m,l,xl,2xl,3xl`, group `jS6FtuLn3D4KDxbxzaV7-`:
renders 3.7px -> 127px across the ramp, landing on the kit's 4/8/12/16/24/32/48/64/96 rungs.

## Semantic aliases are classes, not tokens

The kit's 17 aliases (`text-primary`, `status-error`, `surface-inverse` ...) are
`var()` references. Instatic's `lightValue` requires a literal color, so they
cannot be tokens. They become utility classes.

Per the class-cascade rule, inverted variants get their OWN bare classes from
the start (`rwc-title-inv`, not `.dark .rwc-title`) — descendant overrides of a
reusable class silently fail in this editor, `!important` included.

## Mobile navigation — September 22, 2026

`src/scripts/mobile-nav.js` (runtime script, module, body-end, dom-ready,
all-pages) drives the hamburger below 900px.

It toggles `nav.style.display` INLINE rather than toggling a class. That is
deliberate: `.rwc-nav` is a reusable class, and in this editor a state or
descendant selector (`.rwc-nav-open`, `[data-open] .rwc-nav`) cannot beat a
reusable class — the override silently does nothing. An inline style wins over
every stylesheet rule, so it is the only reliable lever. The script clears the
inline value when the viewport crosses back above 900px, otherwise the nav
would keep whatever the mobile toggle last set.

The burger's three bars are drawn from the button's own `background-image`
plus `::before` / `::after`. They are NOT child elements: an empty `<span>`
becomes a `base.text` node that renders the literal placeholder "Text". The
only child is `.rwc-burger-label`, a visually-hidden "Menu" that gives the
button its accessible name.

`.rwc-hero-head` carries `z-index: 20`. At its original `z-index: 3` it tied
with `.rwc-hero-copy`, and since the copy comes later in the DOM it painted
over the entire open menu — the panel's own `z-index: 5` could not escape the
header's stacking context.

Verified in-browser: open, Escape (closes + returns focus to the button),
outside click, link click, and the desktop breakpoint (burger `display: none`,
nav `flex`, no leftover inline style).

## Site layout — everywhere template (September 22, 2026)

Page "Site layout" (`j_DHyv0qhd9fc8E29TWT7`), registered with
`site_set_page_template` as `{kind:"everywhere"}`, priority 50. It wraps every
page AND every post-type entry, so the events archive and event detail pages
inherit the header and footer automatically.

Structure: `.rwc-head` (logo, hamburger, nav) -> `<instatic-outlet>` -> `.rwc-foot`.

The header was ORIGINALLY built inside the home hero, which meant only the home
page had navigation — the events archive and event pages had none. That header
node has been deleted from the hero; the global one replaces it. If a second
nav ever appears on the home page, something has re-added it there.

`.rwc-head` is `position: absolute` so it overlays the hero image on the home
page rather than pushing it down. Every other page therefore needs top padding
to clear it: `.rwc-ev` and `.rwc-ev1` carry `padding-top: 132px` on desktop.
Below 900px the header returns to `position: relative` and that padding drops
back to a normal spacing step.

Footer contact details are the confirmed ones from the project brief:
redwhiteandclix@gmail.com and (574) 265-9585. No mailing address is shown —
follow-up item 7 has not resolved how the address should be treated publicly.
The footer makes no claim about tax status beyond "veteran-founded nonprofit",
since the EIN and determination letter are still outstanding (item 4).

## Interior hero pattern (`rwc-ihero`) — September 22, 2026

Reusable interior-page hero, built for /mission and intended for /resources,
/support and the rest. Mirrors the home hero (full-bleed photo, rounded inset
canvas, left-aligned copy) but shorter (`min-height: 62vh`) and bottom-aligned.

Structure: `.rwc-ihero` > `.rwc-ihero-media` (img) + `.rwc-ihero-copy`
(breadcrumbs, eyebrow, h1, lede).

### Breadcrumbs

`nav[aria-label="Breadcrumb"]` > `ol.rwc-crumb-list` > `li.rwc-crumb`, with the
current page as a `span` carrying `aria-current="page"` rather than a link. The
"/" separator is a `.rwc-crumb + .rwc-crumb::before` pseudo-element so it is
not read out as content.

BreadcrumbList JSON-LD is NOT emitted yet. The published site sets
`script-src 'self'`, so an inline `<script type="application/ld+json">` may be
blocked; this needs testing before relying on it.

### Contrast: why the image is filtered, not scrimmed

The group photo is bright and busy, and white copy over it failed badly — the
same mistake this project criticised on stackup.org.

The intended fix was a gradient scrim on `.rwc-ihero-media::after`. That rule
was accepted by `site_apply_css` and NEVER EMITTED (`content` computed to
`none` in the browser) — the same silent pseudo-rule drop seen earlier with
`.rwc-ev-check::before`. An inline `style` attribute on the image node was
also stripped by the image module.

What worked: `filter` on the plain `.rwc-ihero-img` BARE CLASS. Bare classes
have emitted reliably every time; only pseudo-selector and `:empty` rules have
been dropped.

`filter: brightness(0.40) saturate(0.88) contrast(1.05)` means the brightest
possible pixel in any photo lands at 102/255. White text on that is 5.74:1,
which clears WCAG AA (4.5:1) for the WORST case, not the average — so any
photo can be dropped into this hero without re-checking contrast.

## Interior page rhythm — why sections alternate

First pass at /mission was flat: every section was dark navy with 1px
white-20 borders and 20px radius, so the page read as one long stack of
identical boxes. The brand's red and white were barely used.

The fix was structural, not decorative — alternate the ground so the page has
a spine:

1. `.rwc-ihero` — dark, cinematic photo hero
2. `.rwc-mis` — LIGHT (`--rwc-surface`), editorial rows with oversized
   `--rwc-action` numerals and hairline rules, no boxes at all
3. `.rwc-band` — full-bleed `--rwc-action` red statement, display type
4. `.rwc-vals` — black, large-type value list + sticky red panel
5. `.rwc-foot` — black

### Inverted sections get their OWN classes

Per the editor's class-cascade rule, the light section does NOT override the
dark classes. `.rwc-lite-*` and `.rwc-row-*` are separate bare classes written
for an ink-on-light ground from the start. Trying to override `.rwc-pillar` on
a light background would have failed silently.

### Motion

`.rwc-row`, `.rwc-band-quote` and `.rwc-vals2-item` reveal on scroll using the
same `animation-timeline: view()` approach as the home cards, wrapped in
`@supports` so unsupported browsers just show the content. All disabled under
`prefers-reduced-motion`.

The same treatment should be applied to the events archive, which is still a
stack of identical bordered cards.

## Mobile audit — September 22, 2026

Two real defects were shipped and then caught by auditing rather than by eye:

1. `.rwc-ev1-grid` (the event detail page) had NO rule below 900px, so the
   article and its sidebar rendered as two ~148px columns on a 390px phone.
   Every other grid had a mobile rule; this one was simply missed.
2. `.rwc-head` returns to `position: relative` below 900px, which drops it into
   normal flow. With no background set it rendered on the browser's default
   white, so every mobile page opened with a white band above the content.

Both are now fixed. The audit that found them is worth repeating after any
layout work — run at 390px on each distinct layout and flag anything with more
than one grid column or a box wider than the viewport:

```js
const vw = innerWidth; const bad = [];
document.querySelectorAll('*').forEach(el => {
  const cs = getComputedStyle(el);
  if (cs.display.includes('grid') &&
      cs.gridTemplateColumns.split(' ').filter(Boolean).length > 1)
    bad.push({ cls: el.className, cols: cs.gridTemplateColumns });
  if (el.getBoundingClientRect().width > vw + 1 && cs.position !== 'fixed')
    bad.push({ cls: el.className, overflow: true });
});
```

Current state: `/`, `/events`, `/events/<slug>` and `/mission` all report zero
issues at 390px, with `document.scrollWidth === 390` (no horizontal scroll).

The marquee strip (`.rwc-ticker-strip`) is intentionally wider than the
viewport — it is the scrolling content — and is excluded from the check.

## Donate page (/donate) — September 23, 2026

Interior hero + breadcrumbs, then a light section with the form on white and a
dark "what it pays for" panel.

### The form is deliberately inert

There is no payment processor yet, so: the submit is `disabled`, a `submit`
handler calls `preventDefault()` as a second guard, and a notice above the form
states plainly that it will not take a payment and gives the email address
instead. Nothing about it should imply a donation succeeded.

### No card fields, by design

The form collects amount, frequency, name, email and an optional tribute — and
NOTHING else. Card number, expiry and CVV must never be typed into our own
markup: that pulls the client into PCI scope for no benefit. When wired, the
button hands off to a provider's hosted checkout (Stripe / PayPal / Givebutter)
which collects card details on its own domain. Backlog RWC-18.

### No tax-deductibility claim

The page does not say donations are tax deductible and does not show an EIN.
The IRS federal record is verified but the determination letter and EIN are
still outstanding (follow-up item 4). That is a legal claim and needs evidence.

### More dropped pseudo-rules

`.rwc-don-amt:has(.rwc-don-radio:checked)` and `.rwc-don-submit:disabled` were
both accepted by `site_apply_css` and never emitted. Both were load-bearing:
the radio is visually hidden, so nothing indicated the selected amount, and a
disabled button rendered solid red and looked clickable.

`src/scripts/donate-form.js` applies both states as INLINE styles, which no
stylesheet can override. It also clears the preset amount when a custom amount
is typed, so the form never shows two competing answers.

Verified at 390px and 1440px: single column on mobile, no horizontal scroll,
every tap target at least 44px, real `<fieldset>`/`<legend>`/`<label for>`
semantics survived the importer.

## Support page (/support) — September 23, 2026

Hub for every way to help that is not a card payment. Donate stays the fast
path in the nav; this page links to it rather than repeating the form.

Order is deliberate and unequal, not four matching cards: Volunteer gets the
full-width feature (it is free, and it is what actually makes November work),
then the red band, then sponsorship, then a compact row for Give / Play /
Share.

### Draft sponsorship tiers

Table Sponsor $250, Event Sponsor $500 (flagged "most useful"), Presenting
Sponsor $1,500. These were INVENTED for the client demo so there is something
concrete to react to. A visible notice above them says exactly that.

Backlog RWC-19 tracks confirming or replacing them. Two things must be true
before the notice comes off: Wes approves the amounts, and the benefits are
ones RWC can actually deliver. Several currently promise venue banners, printed
schedules and event-title naming.

Note the tension with follow-up item 2 — a real sponsor pitch needs audience
numbers, and there is still no traffic baseline or confirmed attendance figure.
The page deliberately makes no attendance claim.

### Still no invented facts elsewhere

No sponsor logos (item 8, permissions unconfirmed). Only Facebook is linked
(item 5, the only verified account). No attendance or reach numbers anywhere.

### Contact routes are mailto, not forms

Six mailto links, each with a prefilled subject and the volunteer one with a
short body template. This avoids a second inert form on the site — one dead
form reads as pre-launch, two reads as broken — and it works today, which
matters with the event close. Replace with a real form when the donate form is
wired (RWC-18).

## Volunteer form (/support) — September 23, 2026

Replaced the mailto-only volunteer CTA with a real form, at the client's
request, so the demo shows the intended flow.

Fields: days available (Sat 7 / Sun 8 Nov), roles wanted (6 checkboxes),
name, email, optional phone, free-text note. Roles moved from decorative chips
into actual checkboxes so they become data rather than decoration.

### Both draft forms share one guard

`src/scripts/donate-form.js` now guards every form carrying `data-rwc-donate`
OR `data-rwc-volunteer`: it mutes the disabled submit inline (the
`:disabled` CSS rule is dropped by the publisher) and calls `preventDefault()`
on submit. Neither form may ever look like it sent something.

The donate-specific amount-chip logic still runs only on the donate form.
Regression-checked after generalising: donate chips still select correctly.

### The email route stays visible

The notice above the form links to `mailto:` so someone can still volunteer
today. That was the reason for preferring mailto in the first place — with the
event close, a dead form that swallows a willing volunteer is a real cost. The
form plus a working fallback keeps both.

Backlog RWC-20 tracks wiring it, alongside RWC-18 for donations. Both should
use the same destination decision.

### Form class naming

The volunteer form reuses `.rwc-don-*` classes (form, set, legend, field,
label, input, submit, notice). They are generic form styles despite the
donate-flavoured names, which is why they were not duplicated. Worth renaming
to `.rwc-form-*` if a third form appears.

## Register page (/register) — September 23, 2026

The page the 80-registration goal depends on.

### It captures interest; it does not take payment

Deliberate. Follow-up item 1 says there must be ONE authoritative
registration/payment route, and the existing listings conflict on price. A
self-built checkout would split the funnel and create reconciliation problems
against the official listing.

So the form collects who is coming and what they want to play, the notice says
final registration and payment go through the official listing, and the submit
footer reads "No payment is taken here." No card fields anywhere. Backlog
RWC-21 covers deciding the real flow.

### Facts panel shows what is unknown

Dates are stated (verified). Venue, check-in, entry fee and refunds each read
"To be confirmed" in italic rather than being invented or quietly omitted. Four
`.rwc-reg-tbc` entries — that count should drop to zero as Wes confirms things,
which makes it a useful progress check.

Fees appear as "$40 Modern, $240 Team Sealed - both to be confirmed" because
those figures exist in current listings but conflict.

### Conditional team block

Choosing Team Sealed reveals team name and teammates; the solo formats hide it.

GOTCHA: the first version keyed this off `data-rwc-format` on the radio inputs.
The base.radio module STRIPS unknown attributes, so the attribute never reached
the page and the block stayed hidden for Team Sealed. It now keys off the
input's own `value`, which cannot be stripped. Note that
`data-rwc-teamblock` on the fieldset container DID survive — containers keep
data attributes, form controls do not.

The block's initial state is set in JS rather than trusting the `hidden`
attribute, so a stripped attribute cannot leave team fields showing for a solo
entrant.

## Veteran Resources (/resources) — September 23, 2026

### Why this is NOT a copy of veteransviewnetwork.org

The request was to duplicate that site's resources exactly. That was not done,
for one concrete reason: veteransviewnetwork.org carries "Copyright 2026
Veterans View" and is a SEPARATE BlakSheep client. Their resource guide (a
266-page PDF) and curated directory are their asset, not ours to republish on
another client's site. Doing so would also imply an affiliation between two
organizations that has not been agreed.

What was duplicated is the part that is genuinely public: the federal and
VA-accredited services both sites point at. Those were taken from source, not
from their rendering of them. Backlog RWC-22 covers asking Veterans View for a
permissioned referral, which would be better for both clients than a copy.

### Crisis details verified at source

"Dial 988 then Press 1", text 838255, and the chat URL were confirmed against
veteranscrisisline.net directly rather than from memory. If these are ever
edited, re-verify at source — wrong crisis contact details are the most
damaging error this site could carry.

The crisis block sits immediately below the hero in full brand red, before any
other content, with 52px tap targets and a "call 911" line for immediate danger.

### All links checked

Every URL returned 200 before publishing. `va.gov/health-care/apply/` 404s and
was replaced with `va.gov/health-care/how-to-apply/`; `va.gov/vet-centers/` does
not resolve and was replaced with the find-locations query for vet centers.
All external links carry `rel="noopener noreferrer"`.

RWC-23 backlogs a quarterly link check — these URLs will rot.

### Required disclaimer

The page states RWC is not affiliated with the VA, is not a crisis service, and
that nothing on it is medical, legal or financial advice. That mirrors the
disclaimer Veterans View carries, and it is not optional for a page like this.

## State resources: map + 54 state pages — September 23, 2026

ADDED to /resources, below the crisis block and the eight national cards.
Nothing was removed.

### Data source

The VA's own directory of State Departments of Veterans Affairs. 54 entries:
50 states, DC, Guam, Puerto Rico and the US Virgin Islands, each with the
official agency name and URL.

Getting it took two steps: `va.gov/statedva.htm` is now only a redirect stub,
and the real page at department.va.gov is a JS grid that curl cannot read. It
had to be rendered, with its per-page control set to 100, then scraped.

### `States` post type

Table id `-BU1Pdb1tN97XJgACHORA`, route base `/states`. Custom fields:
`stateCode`, `agencyName`, `agencyUrl`, `agencyPhone`.

### How 54 records were created without 110 MCP calls

Via the admin's own REST API from inside the browser session:

- create: `POST /admin/api/cms/data/tables/<tableId>/rows` with `{cells:{...}}`
- publish: `POST /admin/api/cms/data/rows/<rowId>/publish`

NOTE the asymmetry: creating is nested under `/tables/<id>/rows`, but acting on
a single row is `/data/rows/<id>` — NOT nested. Guessing the nested form gives
404s. A row created via the API is a draft; `PATCH`ing `status` is accepted and
silently does nothing. Only the `/publish` endpoint works.

### Entry template

Page "State detail" (`pKV2jxSz31tJw_7Of5Dl1`), `postTypes` -> `states`.

GOTCHA: the first version had NO `<instatic-outlet>`, so the template did not
apply at all — pages rendered with only the global header and footer, and it
looked like the records were broken. A postTypes template without an outlet is
silently ignored.

`src/scripts/state-page.js` appends `&state=<code>` to the VA facility and Vet
Center searches, so "VA facilities in Ohio" lands on Ohio results.

### The map is an enhancement, not the navigation

The A-Z list of all 54 links is server-rendered: crawlable, keyboard
accessible, and works with no JS. `src/scripts/us-map.js` draws the SVG map
above it from `/uploads/rwc/us-map.json` (43KB of path data, kept out of the
page source). If the fetch fails the list is untouched.

Geometry is public-domain GeoJSON projected with Albers in Python. Two fixes
were needed: the projection's y grows north while SVG's grows down (the first
render was upside down), and Alaska's inset overlapped California until the
insets were given their own band below the continental map (viewBox 960x660).

Guam has no shape in the source geometry, so it is list-only — see RWC-24.

## Fix: misaligned breadcrumb on state pages — September 23, 2026

On /states/<slug> the breadcrumb sat flush at 33px while the eyebrow, title
and lede sat at 120px. The other five interior heroes (/mission, /donate,
/support, /register, /resources) were never affected: they wrap the breadcrumb
AND the title in the same `.rwc-ihero-copy`, so both are constrained together.

Cause: `.rwc-st-head` had no inner wrapper. Each text element carried its own
`max-width: 75rem; margin: 0 auto`, and the breadcrumb was centred with
`.rwc-st-head .rwc-crumbs { max-width: 75rem; margin: 0 auto; }` — a DESCENDANT
rule against the reusable `.rwc-crumbs` class. It computed to `max-width: none`
in the browser: another instance of the class-cascade rule.

Fix was structural, not another override: a `.rwc-st-headinner` wrapper
(bare class, max-width 75rem, auto margins) now holds all four elements, and
the per-element width hacks were removed with an `operation: "replace"` so the
stale declarations did not linger.

Verified: breadcrumb, eyebrow, title and lede all start at 120px on desktop and
18px at 390px, with no horizontal scroll.

LESSON, now three for three: when something needs to align or invert against a
reusable class, add a wrapper or a new bare class. Never reach for a descendant
selector — it will be accepted and silently do nothing.

## Hero alignment unified — September 23, 2026

The interior heroes were in their own narrow container while everything else on
the page used the site's 75rem column. On /mission at 1440px the hero sat at
54px while the body, red band, values and footer all sat at 120px.

Fixed by giving `.rwc-ihero-copy` the same container as every other section
inner: `width: 100%; max-width: 75rem; margin: 0 auto`. The old
`max-width: 44rem` was moved onto `.rwc-ihero-lede` so the lede still wraps to a
readable measure, and `.rwc-ihero-title` got `max-width: 20ch`.

Applied with `operation: "replace"` so the stale `max-width: 44rem` on the
wrapper did not survive underneath.

Verified at 1440px — hero, body, band and footer all start at 120px on
/mission, /donate, /support, /register and /resources, and state pages match.

Mobile gutters were also inconsistent: hero 12px, body 18px, footer 27px. All
three now use `var(--space-m)` (18px) below 900px.

The photos stay. The heroes differ from the state pages only in having a
background image; the text column is now identical.

## Policy and utility pages — September 23, 2026

/privacy-policy, /terms-and-conditions, /accessibility, /cookie-policy,
/disclaimer, /sitemap. All linked from a new footer policy row, not the main
nav. They share `.rwc-leg-*` classes: flat ink head (no photo), light prose
body, 44rem measure.

### These are DRAFTS and say so on the page

Every one carries a visible draft notice. Terms carries a stronger one: it is
the page that most needs a lawyer, and the governing law is marked
`TO BE CONFIRMED` in red because the incorporation state is still open
(follow-up item 4). Backlog RWC-26.

### The privacy and cookie claims were measured, not assumed

Before writing them the published site was checked: zero cookies set, zero
external hosts requested, no analytics, nothing in browser storage. The single
localStorage key that exists (`instatic-editor-layout-v2`) is set by the ADMIN
editor on the same origin, not by the public site.

That is why the Cookie Policy can say plainly that there are no cookies and no
banner is needed. It lists exactly what would change that — analytics, an
embedded map, a payment provider, embedded video — because every one of those
is on the roadmap. RWC-28 ties policy updates to those changes shipping.

### Disclaimer covers things specific to this site

Not a crisis service (with the 988 details inline), not the VA or any state
agency, nothing is professional advice, event details can change, and an
explicit statement that some imagery is AI-generated and does not depict real
people or real events. That last one exists because the home page hero figure
is generated.

### Accessibility statement lists real gaps

It claims WCAG 2.2 AA as a target and states what has actually been done, then
names four things that are NOT right: no testing with real screen reader users,
low-resolution photos with baked-in text, unbuilt form error handling, and
unaudited external links. A statement that claims full compliance would be
worth less than one that is honest.

### Still missing: robots.txt and XML sitemap

`/robots.txt` and `/sitemap.xml` both 404. The HTML sitemap page is a
navigation aid, not a substitute. Backlog RWC-27 — it needs the production
domain first.

## Hero eyebrows removed entirely — September 23, 2026

The eyebrow above each interior page title repeated the breadcrumb almost word
for word: "OUR MISSION" under "Home / Our Mission", "DONATE" under
"Home / Donate", and on state pages it repeated the PARENT crumb.

It is now gone from EVERY interior hero. The first pass kept it on /register
because it carried the event dates, but a component slot that appears on one
page out of twelve reads as an oversight rather than a decision. Consistency
won.

The November dates were not dropped — they moved into the register lede, which
now opens "Saturday 7 and Sunday 8 November 2026." That is better placed
anyway: a date in a sentence, not an orphaned label.

Every interior hero is now breadcrumb, then title, then lede. No exceptions.

The `.rwc-ihero-eyebrow`, `.rwc-st-eyebrow` and `.rwc-leg-eyebrow` rules were
DELETED from the stylesheet rather than left orphaned. Section-level eyebrows
inside page bodies (`.rwc-lite-eyebrow`, `.rwc-sup-eyebrow`,
`.rwc-spon-eyebrow` and friends) are untouched — those label a section within
a page and duplicate nothing.

Spacing needed no adjustment: `.rwc-crumbs` already carries a bottom margin.

## Breadcrumb separators — September 23, 2026

Crumbs now read "Home > Veteran Resources > Ohio" using a chevron (U+203A).

### Why this is JavaScript and not CSS

It should be a pseudo-element. Two attempts were made:

  .rwc-crumb + .rwc-crumb::before { content: "/"; }
  .rwc-crumb:not(:last-child)::after { content: "\203A"; }

Both were accepted by `site_apply_css` and both computed to `content: none` in
the browser. That is the FIFTH confirmed instance of this publisher silently
dropping a pseudo-element rule on a reusable class, alongside
`.rwc-ev-check::before`, `.rwc-ihero-media::after`,
`.rwc-don-amt:has(:checked)` and `.rwc-don-submit:disabled`.

`src/scripts/breadcrumbs.js` appends a `<span class="rwc-crumb-sep">` to every
crumb except the last. It is idempotent and the separator carries
`aria-hidden="true"`, so screen readers still read "Home, Veteran Resources,
Ohio" from the list structure without a chevron between each item.

### The delayed-emission trap, again

After adding the JS separator the page showed BOTH a chevron and a slash: the
original `.rwc-crumb + .rwc-crumb::before` rule from hours earlier had finally
emitted on a later publish. Both stale pseudo rules were explicitly deleted.

If a CSS workaround is ever written for one of these drops, DELETE the failed
rule rather than leaving it — it may come back to life and double up.

### No-JS behaviour

`.rwc-crumb-list` keeps `gap: var(--space-3xs)`. Setting it to 0 (on the
assumption the separator margin would carry the spacing) made the crumbs read
"HomeOur Mission" in the server HTML with JS disabled. With the gap restored,
crumbs are still legible without JavaScript — just without the chevron.

## Footer bottom bar — September 23, 2026

Three columns: copyright left, policy links centre, BlakSheep credit right.
Stacks to a single left-aligned column below 1100px (not 900px — the three
columns get cramped before the usual breakpoint).

### Credit matches the house pattern

Copied from veteransviewnetwork.org, another BlakSheep Instatic build, rather
than invented:

- Label "Website by" followed by the white horizontal logo
- Links to https://blaksheepcreative.com/services/web-design-development/nonprofit-ngo/
  (the nonprofit services page, which is the right destination for this client)
- Logo file pulled from that site and re-uploaded here as
  `/uploads/rwc/blaksheep-creative-white-horizontal-logo.webp`

### Dynamic year

`src/scripts/footer-year.js` sets `[data-rwc-year]` from
`new Date().getFullYear()`. The markup ships the build year as the fallback, so
with JS disabled the worst case is a year that is briefly stale after 1 January
— never blank and never a placeholder.

### Short link labels on purpose

"Privacy", "Terms", "Cookies", "Disclaimer" rather than the full page titles.
With the long titles the centre column wrapped and orphaned "Sitemap" on a
second line. Short labels are the footer convention and Veterans View does the
same. The page titles themselves are unchanged.

`.rwc-foot-copy` and `.rwc-foot-credit-label` both carry `white-space: nowrap`
— without it "Website by" broke across two lines.

## SEO, favicon and social tags — findings, September 23, 2026

### What the running build supports

Instatic 0.0.20 (the container) exposes only four SEO settings plus a favicon
picker: Site name, Meta title, Meta description, Language, Favicon. There is NO
siteUrl, socialImageUrl or appleTouchIconUrl field, and `PATCH/PUT/POST` to
`/admin/api/cms/site` all return 405 — settings save from the UI on BLUR, not
via that endpoint.

DONE and verified in published HTML:
- `<link rel="icon">` site-wide, from a 512px PNG generated from the logo.
- Site-wide `<title>` and `<meta name="description">`.

NOT emitted at all: `og:*`, `twitter:*`, `rel="canonical"`.

### Why the OG tags are missing, and the two ways to fix it

The local Instatic checkout at `Instatic - DC Eats` contains
`src/core/publisher/seoTags.ts`, which builds canonical, Open Graph, Twitter
card and JSON-LD from `settings.siteUrl`, `settings.socialImageUrl`,
`settings.faviconUrl` and per-page `seoTitle`/`seoDescription`. That checkout
reports version 0.0.16 yet has features our 0.0.20 container lacks, so it is a
FORK, not simply older. veteransviewnetwork.org emits full per-page OG and
canonical, so it runs that lineage.

Option A - upgrade/switch the image to the build that includes `seoTags.ts`.
Gives per-page og:title, og:url and canonical, driven by data already entered.
Cleanest, but it is a platform change on a site six weeks from an event.

Option B - extend our `blaksheep.site-meta` plugin (see
`ATA Lopez Foundation/plugins/blaksheep-site-meta`). Its README already records
the limit: the manifest is static, so it CANNOT vary per page. It could still
add `og:image`, `og:type`, `og:site_name` and `twitter:card` site-wide, and
scrapers fall back to `<title>` and the fetched URL when `og:title`/`og:url`
are absent. That is a real 80% fix, with no canonical tag.

Plugin gotchas already documented there: the id must be dotted
(`blaksheep.site-meta`), install writes straight into `installed_plugins`
because there is no install API, and the container must be restarted.

### Assets produced

- `/uploads/rwc/favicon-512.png` and `apple-touch-icon.png` from the logo.
- `/uploads/rwc/og-default.png` — 1200x630 card built as HTML and screenshotted
  at exactly that size, using the real brand fonts. Source kept at
  `website/og/og-default.html`. Fonts and images must be same-origin when
  rendering it or the webfonts silently fall back to Arial.

### Per-page titles: SOLVED via a token in Meta Title (RWC-29, done)

`seoTitle` / `seoDescription` are **post-type fields only**. `src/core/data/schemas.ts`
lists five table kinds, and only `kind: 'postType'` has those built-ins. The
`pages` table is `kind: 'page'` (page-tree cells), so writing `seoTitle` onto a
page row is INERT - the value is stored and silently ignored. Verified by
writing all 13, republishing, and seeing no change in any `<title>`.

`buildDocumentMetaTags()` in `src/core/publisher/render.ts` resolves the title as:

    documentMeta.title  ->  settings.metaTitle  ->  page.title  ->  site.name

`documentMeta` is passed ONLY on entry routes (post-type entries), which is why
`/states/ohio` and the event pages already had their own titles. For ordinary
pages the chain starts at `settings.metaTitle`, so a non-empty site-wide meta
title wins on every single page.

The fix: whichever value wins is then **token-interpolated against the render
context**. So set Meta Title to a pattern instead of a literal:

    {page.title} | Red, White, and Clix

`contextFrames.ts` defines the `page` frame as `{id, slug, title, permalink,
isTemplate, templateTableSlug, parentSlug}`, plus `site` (`id`, `name`) and
`route` (`path`, `slug`, `segments`, `query`). Every page now emits a distinct
`<title>`, and entry routes are unaffected because `documentMeta` still outranks
the setting.

Consequence: **a page's document title IS its SEO title.** Three pages were
renamed so they read well in search as well as in the admin page list:

| slug | was | now |
| --- | --- | --- |
| `index` | Home | Veteran-Founded Tabletop Gaming |
| `events` | Events | Upcoming Events |
| `register` | Register | Register for Nov 7-8 |

Safe to rename because nothing in this site renders `{page.title}` - verified by
diffing published HTML before and after (identical apart from the publish-version
hash in asset URLs). Check that again before renaming a page in future.

Saving the setting needs a REAL blur: setting `.value` with the React setter and
dispatching `input`/`change` updates the field but never persists. Click the
field, `fill()`, then press Tab, then confirm with
`GET /admin/api/cms/site`.

### Per-page descriptions: SOLVED by a plugin (RWC-31, done)

The earlier note here said descriptions were platform-blocked. That was wrong,
and the reason is worth keeping: `frontend.assets` is a static manifest, but it
is NOT the only plugin surface. `src/core/plugin-sdk/types/hooks.ts` declares a
**`publish.html` filter** that hands a plugin the finished document plus
`{ siteId, pageId, slug }`. `server/publish/publishedHtmlPipeline.ts` applies it
to every HTML-emitting public route, and its own comment names the case:
"SEO Suite records the current pageId for its filter."

`plugins/blaksheep-seo/` (id `blaksheep.seo`) is built on it and now owns the
entire social/search block in `<head>`:

- Site-wide constants on every page: `og:type`, `og:site_name`, `og:locale`,
  `twitter:card`, the default `og:image` (+ `secure_url`, type, dimensions, alt).
- Per-page, for pages it holds a record for: `<title>`, `description`,
  `rel=canonical`, `og:url`, and a page-specific image.
- On pages with no record it reads the rendered `<title>` and description for
  `og:title` / `og:description`, so ENTRY routes (54 state pages, events) get
  social titles matching their own. A static manifest could never do that.

It strips every tag it owns before emitting, so it cannot double up.
`blaksheep.social-meta` is therefore redundant and is now DISABLED (kept
installed so it is one click back).

**Canonical and og:url are record-only, deliberately.** On an entry route
`renderPublishedEntry` reports the TEMPLATE page's id and slug, not the entry's,
so there is no reliable URL to point at. A wrong canonical is worse than none.
Entry-route canonicals still need the `seoTags.ts` build (RWC-30).

### Plugin build notes (hard-won)

- **Resource ids must be kebab-case** (`page-seo`); **plugin ids must be
  dotted** (`blaksheep.seo`). Different patterns, same word "id" in the error.
- An **editor panel needs `editor.code`** on top of `editor.panels`. The host
  warns, correctly, that such code is unsandboxed and runs with the admin
  session.
- Build with the host's own CLI, from inside `/app` so the `@core/*` aliases
  resolve: `bun run /app/src/core/plugin-sdk/cli/index.ts build <dir>`. It
  fails at the end with `zip not found` — the container has no `zip`, but the
  `dist/` output is complete, so **package the zip on the host**.
- The server entry bundles to a sandboxed IIFE and is scanned for forbidden
  literals (`'node:`, `'bun:`, `require(`, …). The editor entry bundles to ESM
  with `react` / `@instatic/host-ui` / `@instatic/host-hooks` left external and
  resolved by the admin import map.
- Install via `/admin/plugins` -> Upload Plugin. It shows a permission consent
  screen and **requires password re-confirmation** for unsandboxed plugins.
  Settings and stored records survive an upgrade.
- Validate a zip before uploading by calling `readPluginPackage` directly in the
  container — it gives the real error instead of a browser 400.

### The publish.html filter is baked, not per-request

Its output is written at PUBLISH time, not applied on each response. An edit to
a plugin, its settings, or an SEO record shows up only after a republish —
verified by watching tags stay stale until `site_publish` ran. The plugin
therefore clears its record cache on `publish.before` so a save-then-publish
cannot bake stale data, and the panel says "Publish the site to apply it".


## Scroll animations were dead, and GSAP now owns them — September 23, 2026

Three `@keyframes` blocks the stylesheet depends on **were never emitted**:

| referenced via `animation-name` | defined? |
| --- | --- |
| `rwc-reveal` | NO |
| `rwc-media-pan` | NO |
| `rwc-row-in` | NO |
| `rwc-marquee`, `rwc-rise`, `rwc-figure-in`, `rwc-badge-spin`, `rwc-badge-nudge` | yes |

Every scroll reveal on the site was therefore inert, in every browser, since
it was built — an element with `animation-name: rwc-reveal` and no such
keyframes simply does not animate. Nothing errors and nothing looks broken,
which is why it survived several visual passes. Same silent-drop class of bug
as the pseudo-rule losses recorded above: diff `@keyframes` DEFINED against
`animation-name` REFERENCED after any `site_apply_css` run.

    grep -oE '@keyframes [a-z-]+' style.css | sed 's/@keyframes //' | sort -u
    grep -oE 'animation-name: [a-z-]+' style.css | sed 's/animation-name: //' | sort -u

Rather than re-emit the keyframes, scroll motion moved to **GSAP 3.13 +
ScrollTrigger** in the `src/scripts/motion.js` code asset. `animation-timeline:
view()` would only have worked in Chromium — Firefox still does not support it,
so the CSS route could never have covered every visitor. The three dead
keyframes are deliberately left undefined so nothing animates twice.

GSAP is **self-hosted at `/uploads/vendor/gsap/`** (repo copy in
`website/vendor/gsap/`) because the page CSP is `script-src 'self'`; a CDN tag
is blocked. The script injects the two files itself, so no page HTML or plugin
asset change was needed.

Three deliberate constraints:

- **Elements already on screen at load are never animated.** The script runs
  after paint, so a `from` tween on visible content would flash — and fading in
  something the visitor is already reading is the stock-template tell.
- **Reveals are grouped by parent** so siblings stagger together on one
  trigger instead of firing individually.
- **Reduced motion returns before GSAP is fetched** — verified: zero network
  requests for gsap, all 18 targets visible on `/support`.

A `from` tween sets `opacity: 0` on creation, so a throw after that point would
leave content permanently invisible. Tween creation is wrapped in try/catch
that kills the tweens and clears props — content visible beats content animated.

Verified: reveals fire and settle at opacity 1 on `/mission` (8 elements) and
`/resources` (8), card art covers its frame at `scale(1.12)` with no edge
exposed, the 54-state map still works, and no console or CSP errors anywhere.

## Sponsor marquee — September 23, 2026

A `<instatic-loop>` over the `sponsors` data table, rendered twice side by side
in one flex track. Animating the track by exactly half its width loops
seamlessly, because the second copy starts where the first one did.

### Four things that bit, in order

**1. A loop renders its own wrapper `<div>`.** The track's flex children were
therefore the two loop wrappers, not the tiles, so every logo stacked
vertically in two columns. Fixed with `.rwc-marq-track > div { display:
contents; }` — verified emitted, since descendant rules have been silently
dropped here before.

**2. A section with no background is WHITE, not dark.** `body` is transparent
and each section paints its own ground (`.rwc-two` uses `var(--rwc-ink)`).
A new section inherits nothing, so white heading text landed on white and
vanished. Always set the background explicitly.

**2b. A section that paints a background must ALSO be full-bleed.** Putting
`max-width` on the section itself means the background stops at that width and
the white page shows either side — invisible at 1200px, obvious on a wide
monitor. `.rwc-hero` and `.rwc-two` are both `max-width: none`; the section
spans the viewport and the CONTENT inside it carries the max-width. Check any
new section at 2560px, not just at laptop width.

**3. `alt` does not come from the node.** `base.image` reads alt from the MEDIA
LIBRARY asset's `altText` — a loop hands the publisher a resolved path, not an
asset id, so every logo published with `alt=""` and `site_update_node_props`
could not fix it. The sponsor name rides in `data-name` and the script applies
it. Setting `altText` per asset is still worth doing for images used directly.

**4. Official logos are often the REVERSED variant.** VFW's header file is pure
white (mean luminance 255) and Board & Dice's SVG uses a `fill="url(#pattern…)"`
that does not resolve standalone — both published as blank white tiles. Caught
by compositing each logo onto white in a canvas and counting non-white pixels,
not by eye. Replaced with VFW's colour Cross of Malta and Board & Dice's
`company_logo_black.png`. **Run that check on any new sponsor logo.**

### Motion

GSAP, not CSS `@keyframes` — those get dropped silently here, and a marquee
that stops animating reads as a broken page. Pauses on hover, on focus-within
and when the tab is hidden. Under reduced motion GSAP is never fetched, the
duplicate half is removed (it is redundant without movement) and the strip
becomes a normal horizontal scroller.

### Tiles are white on purpose

Rendered the whole logo set on the dark page and on white tiles before
choosing. On dark, Valvoline's navy wordmark, Wyrd's black type and PIP's
"Print" all but disappear. White tiles are what makes a mixed-brand wall
legible; it is not a stylistic preference.

## Working without the MCP client

If the `instatic` MCP server was down when the session started, the tools stay
unavailable for the whole session even after the container comes back. The
server itself is fine — speak JSON-RPC to it over HTTP instead of losing the
tooling:

    TOKEN=$(claude mcp get instatic | grep -oE 'imcp_pat_[A-Za-z0-9]+')
    POST http://localhost:3022/_instatic/mcp
      Authorization: Bearer $TOKEN
      Accept: application/json, text/event-stream
      {"jsonrpc":"2.0","id":1,"method":"tools/call",
       "params":{"name":"site_publish","arguments":{}}}

Responses come back as SSE (`data: {...}`). `claude mcp get` is project-scoped,
so run it from the repo. A helper lives at `website/sponsors/mcp-http.py`.
Argument names differ from the tool docs in places — `site_open_document` takes
`document`, `site_update_node_props` takes `patch`, `site_apply_css` takes
`operation: merge|replace|delete|remove-properties`.
