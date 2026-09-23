# Events post type — created September 22, 2026

Instatic post type, created in the Data workspace at `/admin/data`. Not
creatable through the MCP connector: there is no create-collection or add-field
tool, so this was built by driving the admin UI with Playwright.

- Table id: `ZeWhbhCUi5tOq8tS2MbxX` (NOT "events" — the MCP wants this id)
- Slug: `events`, route base `/events`, entry URLs `/events/<slug>`
- Kind: post type (routable + draft/scheduled/published workflow), chosen over
  a plain data table so each event has a URL that can carry its own markup.

## Schema

Built-in: `title`, `slug`, `body`, `featuredMedia`, `seoTitle`, `seoDescription`.

| Field | Type | Required | Maps to |
|---|---|---|---|
| `startDate` | dateTime | yes | schema.org `startDate` |
| `endDate` | dateTime | yes | schema.org `endDate` |
| `checkInTime` | text | no | — (follow-up 1) |
| `venueName` | text | no | `location.name` (follow-up 7) |
| `venueAddress` | longText | no | `location.address` (follow-up 7) |
| `registrationUrl` | url | no | `offers.url` (follow-up 1) |
| `beneficiary` | text | no | — (follow-up 3) |
| `hotelBlockUrl` | url | no | — (follow-up 8) |
| `hotelDeadline` | date | no | — (follow-up 8) |
| `refundPolicy` | longText | no | — (follow-up 1) |
| `eventStatus` | select | no | `eventStatus` |
| `ticketTiers` | repeater | no | `offers[]` |

`ticketTiers` item fields: `tierName` (text), `price` (number),
`perTeam` (boolean), `capacity` (number). A repeater is used instead of a
related table because Instatic supports one natively and the tiers only ever
belong to one event.

## Gotcha: select option values are generated, not authored

The option values entered as `EventScheduled` / `EventPostponed` /
`EventCancelled` were DISCARDED. Instatic assigned its own ids and kept the
authored text only as the label:

- Scheduled  -> `VursR4-TyWOPvFfXtwZtY`
- Postponed  -> `aDTTiz7HwEMkNUcvf9hi4`
- Cancelled  -> `HG84fss1TT_9Uv_OaqTjx`

So JSON-LD must map the option LABEL to
`https://schema.org/EventScheduled` etc. Never emit the stored value — it is a
meaningless id, and it will change if the options are recreated.

## Current rows

`november-2026` (`qJ8ZPPHsEBphzdDnWBI4r`) — status DRAFT, deliberately.

Only the dates are verified (November 7-8, 2026, confirmed on HCUnits). The
times are recorded as 00:00 and 23:59 because `startDate`/`endDate` are
required and the real check-in time is unknown — these are day boundaries, not
a claim about when the event starts. Every other factual field is empty.

Do not publish this record, and do not emit its JSON-LD, until items 1, 3, 7
and 8 of `CLIENT-FOLLOWUP.md` come back from Wesley. Empty fields must emit no
markup rather than placeholder markup.

## Sample records — DELETE BEFORE LAUNCH

Four fictional records exist purely to build and test the template. Every title
is prefixed `SAMPLE —`, every venue is "Sample ...", every address is
`000 Example Street, Sampletown, IN 00000`, and the registration URL is
`example.com`. None of them describe a real event.

| Slug | Purpose | Status |
|---|---|---|
| `sample-spring-clix-open` | full data, two ticket tiers | published |
| `sample-summer-team-sealed` | deliberately sparse — proves empty fields degrade cleanly | published |
| `sample-winter-charity-clash` | eventStatus = Cancelled | published |
| `sample-autumn-clix-classic-2025` | past-dated, for the past/upcoming split | DRAFT (publish was blocked) |

The past-dated sample could not be published, so the "PAST EVENT" flag and the
past-sorting branch in `events-list.js` are written but NOT yet verified
against a real row.

The real record `november-2026` remains a draft and was never given fake data.

## Loop findings

Custom fields DO resolve as loop tokens — `{currentEntry.venueName}`,
`{currentEntry.checkInTime}`, `{currentEntry.startDate}` all render.

The loop CANNOT sort by a custom field. `data-order-by` accepts only
publishedAt / createdAt / updatedAt / slug, so ordering by event date is done
in `src/scripts/events-list.js` on top of a complete server-rendered list.
Without JavaScript the events still render, just in publish order.

Dates render as raw ISO (`2027-01-23T09:00:00`). The card uses
`<time datetime="{currentEntry.startDate}">` so the markup is correct without
JavaScript, and the script rewrites the visible text via `Intl.DateTimeFormat`.

## Gotcha: site_apply_css silently dropped rules

`.rwc-ev-check::before` and `.rwc-ev-venue:empty` were accepted by
`site_apply_css` (it reported them created) but were NOT emitted into the
published stylesheet across two publishes — the stylesheet content hash did not
change. They appeared on a later publish. Other pseudo rules in the same sheet
(`.rwc-burger::before` and friends) were never affected.

Do not trust `cssRulesCreated`. Fetch `/_instatic/css/style-*.css` and grep for
the selector. Working around it in JavaScript while the CSS is also live
produces doubled output — that is exactly how "Check-in Check-in 8:30 AM"
happened.

## Single (entry) template — /events/<slug>

Page "Event detail" (`Om0ljprDOSbqKSWNO0OQA`), registered via
`site_set_page_template` with `{kind:"postTypes", tableSlugs:["events"]}`.
The record body flows into an `<instatic-outlet>`; the sidebar renders the
structured fields.

Entry tokens DO resolve outside a loop — `{currentEntry.title}`,
`{currentEntry.venueName}`, `{currentEntry.startDate}` all render on the entry
route, including inside `data-` attributes on a container.

Calendar and map live in `src/scripts/event-detail.js`:

- Google Calendar link built from startDate/endDate as UTC basic format.
- `.ics` generated client-side as a Blob, filename from the slug.
- Map is a LINK-OUT to OpenStreetMap search, not an embedded iframe. An embed
  needs either stored coordinates or a keyed provider, and an iframe loads a
  third party on every view. If a real embedded map is wanted later, add
  `latitude` / `longitude` number fields and switch to an OSM bbox embed.
- Any sidebar row whose field is empty hides itself AND its label.

## BLOCKER: featured images do not render

`featuredMedia` is set correctly on the records — `content_get_document`
returns the media id, and the images are real entries in the Media library
(uploaded through the admin UI with Playwright, because `media_upload` needs
base64 and `sourceUrl` refuses loopback).

But `{currentEntry.featuredMedia}` resolves to an EMPTY STRING, in both the
entry template and inside a loop. Consequences:

- An `<img src="{currentEntry.featuredMedia}">` is stripped at publish time.
- `data-x="{currentEntry.featuredMedia}"` renders as `data-x=""`.
- `{currentEntry.featuredMedia.src}`, `.url`, `.path` and
  `{currentEntry.firstImage}` are not recognised at all — unknown tokens are
  removed entirely, which is how you can tell `featuredMedia` IS recognised
  and simply yields nothing.

`src/scripts/event-detail-media.js` collapses the empty frame so no blank box
renders. It is a guard, not a fix, and stops firing once images work.

Options, none yet chosen:
1. Add a plain `url` field (e.g. `featuredImageUrl`) and use that token.
   Works today; editors paste a URL instead of picking from the library.
2. Find the correct media binding for `base.image` (not documented in the
   repo docs; may need the editor's own media picker, which cannot be dynamic
   per entry).
3. Raise it upstream as a bug.

## CORRECTION: featured images work — the snapshot was stale

An earlier note in this file called the media binding a publisher bug. That was
wrong, and the wrong diagnosis is worth keeping visible because the failure
mode is easy to misread.

Featured images use Instatic's NATIVE binding, set through the editor:
select the image node -> "Bind Image" -> pick the field. That writes a
structured entry to `node.dynamicBindings[propKey]`; it is NOT token
interpolation, so `{currentEntry.featuredMedia}` in an `src` never works and
`site_update_node_props` cannot set it (that tool patches `props`).

The real reason it appeared broken:

**Entry pages render a PUBLISHED SNAPSHOT of the row.** The record was
published at 02:09; `featuredMedia` was set at 02:21. The page kept rendering
the 02:09 version, which had no image. Re-publishing the RECORD (not the site)
fixed it immediately.

So after changing any field on an already-published record, re-publish that
record or the site will keep serving the old values. `site_publish` alone is
not enough.

Once bound, Instatic generates responsive variants automatically — the page
serves `...-w900.webp` from a `srcset` of 64/320/640/900w.

`featuredImageUrl` was added as a workaround before this was understood. It is
NOT used by any template. See backlog RWC-17 to remove it.

## Map: parked, not abandoned (backlog RWC-15)

`src/scripts/event-detail-media.js` contains a working tile map — Web Mercator
projection, tile grid, centred pin, screen-reader label, attribution. It is
disabled behind `MAP_ENABLED = false`.

Two blockers, both external:

1. The published site sends
   `Content-Security-Policy: default-src 'self'; frame-src 'none'; ...` as a
   `<meta http-equiv>` in every page, so ALL iframes are blocked. There is no
   CSP setting in the admin UI. That rules out a normal map embed.
   The same policy allows `img-src 'self' data: https:`, which is why the
   tile-as-image approach was taken.
2. No usable tile host. `tile.openstreetmap.org` refuses hotlinking and serves
   403 "Access blocked" tiles. `basemaps.cartocdn.com` serves watermarked
   tiles without a key and dropped one request in four under test.

To finish: get a free key (MapTiler, Stadia, Thunderforest), set `TILE_URL` to
the provider's `{z}/{x}/{y}` template and `MAP_ENABLED = true`. Nothing else
changes.

Until then the sidebar shows the "Open in maps" link, which needs no key and
loads no third party. Records without coordinates use that link regardless.
