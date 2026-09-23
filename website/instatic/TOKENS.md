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
