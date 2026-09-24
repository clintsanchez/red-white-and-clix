# Sponsors table — created September 23, 2026

A **data table**, not a post type. A sponsor needs a logo and an outbound link,
not a URL of its own; making it routable would mint ~30 near-empty
`/sponsors/<name>` pages, which is thin content working directly against the
per-page SEO work. Switch it to a post type only if sponsors ever need their
own write-ups.

- Table id: `9nmAscb8ScyoQq_OC7Lrj` (the API wants this, NOT the slug `sponsors`)
- Kind: `data` — grid-authored, no draft/published workflow, no route

## Schema

| Field | id | Type | Notes |
| --- | --- | --- | --- |
| Name | `name` | text | primary field |
| Logo | `logo` | media | stores the media asset id as a plain string |
| Site URL | `site_url` | url | outbound link |
| Tier | `tier` | select | `proud_supporter`, `community_partner` |
| Sort order | `sort_order` | number | wall ordering, in tens |

Tier and Sort order are beyond the three fields originally asked for; a wall
needs grouping and ordering. The two tier options mirror the groupings the
live Squarespace site already uses rather than tiers invented here.

## Select option values ARE preserved here

`EVENTS-MODEL.md` records that a post type's select options had their authored
values discarded and replaced with generated ids. That did **not** happen on
this data table: `Proud supporter` kept the value `proud_supporter`. Do not
assume either behaviour — read the schema back after creating a select.

## Two API gotchas

1. **Create/act on rows by table ID.** `POST /admin/api/cms/data/tables/sponsors/rows`
   returns `{"error":"Table not found"}`; the id works. Same asymmetry as Events.
2. **Creating a table needs step-up auth.** `POST /admin/api/cms/data/tables`
   returns 401 and the UI raises a "Confirm your password" prompt. Creating
   *rows* does not.

## Current rows

Ten, each with an official logo sourced from the brand's own site:

| Name | Tier | Logo |
| --- | --- | --- |
| WLFI News | proud_supporter | SVG |
| Culver's | proud_supporter | SVG |
| Purdue Federal Credit Union | proud_supporter | SVG |
| VFW | proud_supporter | PNG |
| GAMA | community_partner | PNG |
| Paizo | community_partner | PNG |
| Board & Dice | community_partner | SVG |
| Texas Roadhouse | community_partner | PNG |
| Printing Partners | community_partner | SVG |
| Spotlight Strategies | community_partner | PNG |

Ten rows. All media assets verified serving 200 with the right content type.

**These rows are not a claim about who sponsors the event.** The names come
from the wall on the live Squarespace site. Wesley still has to confirm which
are current and that we may display each mark — see
`06-Reports/sponsor-logo-audit.md`. Nothing renders them on the site yet.
