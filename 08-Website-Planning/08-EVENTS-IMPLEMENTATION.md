# Events implementation — September 22, 2026

## Editing

- Events admin: https://red-white-and-clicks.local/wp-admin/edit.php?post_type=rwc_event
- Add an event: https://red-white-and-clicks.local/wp-admin/post-new.php?post_type=rwc_event
- Archive: https://red-white-and-clicks.local/events/
- Single URL pattern: `/events/<event-slug>/`
- Elementor Single Event template: 1459
- Elementor Events Archive template: 1460
- Elementor Event Card loop template: 1461

Use the normal event editor for the title, description, excerpt, featured image and Event Details fields. The Elementor templates supply the layout automatically; there is no need to build each event as a separate Elementor page.

## Data model

Meta Box owns the database-backed `rwc_event` post type (definition 1457) and Event Details field group (1458, key `rwc-event-details`). No duplicate PHP content-type registration. Data uses ordinary postmeta, not a custom table. The archive setting was added to Meta Box's saved definition because Novamira's create-post-type ability does not expose that setting.

Native fields: title, body, excerpt, featured image, revisions.

| Field | Key | Type |
|---|---|---|
| Start date and time | `rwc_event_start` | datetime |
| End date and time | `rwc_event_end` | datetime |
| Timezone | `rwc_event_timezone` | text |
| Check-in time | `rwc_event_check_in` | text |
| Event status | `rwc_event_status` | select |
| Game / format | `rwc_event_format` | text |
| Venue name | `rwc_event_venue` | text |
| Venue address | `rwc_event_address` | textarea |
| Directions URL | `rwc_event_map_url` | url |
| Online event URL | `rwc_event_online_url` | url |
| Registration URL | `rwc_event_registration_url` | url |
| Registration deadline | `rwc_event_registration_deadline` | datetime |
| Entry price | `rwc_event_price` | number |
| Currency | `rwc_event_currency` | text |
| Fee basis | `rwc_event_fee_basis` | select |
| Capacity | `rwc_event_capacity` | number |
| Capacity unit | `rwc_event_capacity_unit` | select |
| Organizer name | `rwc_event_organizer` | text |
| Organizer email | `rwc_event_email` | email |
| Organizer phone | `rwc_event_phone` | text |
| Rules / event pack URL | `rwc_event_rules_url` | url |
| Schedule | `rwc_event_schedule` | textarea |
| Refund policy | `rwc_event_refund_policy` | textarea |
| Accessibility / travel notes | `rwc_event_accessibility` | textarea |
| Details last verified | `rwc_event_verified_on` | date |

Dates are entered in the event's IANA timezone and stored as local `Y-m-d H:i:s` values. Start/timezone are required in the editor. Confirm end >= start when entering data; cross-field chronological validation is not automated. Blank prices are unconfirmed, not free. Price and currency remain separate from fee basis; capacity remains separate from capacity unit.

## Template sources and behavior

- Archive hero from Archive Post 1329; details/body structure from Single Post 1335; labels, buttons and card shell from Home 1376. Existing page content and the active kit are retained.
- Single template binds post title, featured image and content plus event metadata. Optional directions/rules/online links appear only when valid URLs are present.
- Archive uses the main event query in a native Elementor Loop Grid, nine per page, 3/2/1 columns. Each card shows its own title, date/time, venue, status and event URL. Events are ordered ascending by stored local start date; different timezones are displayed correctly but ordering is by local date/time, not normalized UTC. Past and cancelled events remain listed with their status.
- Events archive condition: `include/archive/rwc_event_archive`. The kit's generic archive excludes that scope. Single condition: `include/singular/rwc_event`.
- Registration CTA is hidden for blank/invalid URLs and Cancelled, Postponed, Sold out or Completed statuses. No checkout or payment handling was added.
- Added Events under the existing Pages dropdown on desktop and mobile. Renamed the old empty draft page's slug to `events-page-draft` to prevent future archive collisions; its content is preserved.

## Implementation notes

All WordPress writes used Novamira MCP. Meta Box schema creation and supported Elementor dynamic bindings used dedicated abilities. Narrow native Elementor fallbacks handled legacy section/column trees and text-editor WYSIWYG dynamic bindings that Novamira's validators rejected. Layouts remain editable in Elementor.

`website/wordpress-events/rwc-events-runtime.php` is the source for the small helper loaded at `wp-content/novamira-sandbox/rwc-events-runtime.php`. It sorts the archive, formats displayed dates, and controls optional CTA visibility. The Novamira sandbox loader currently loads it; retain the loader or package this helper as a normal site plugin during production handoff. The CPT and fields themselves are owned by Meta Box.

## Verification

Two temporary, explicitly labeled sample events verified separate loop contexts, chronological order, formatted dates, scheduled/cancelled CTAs, and layouts at 1440px and 390px. All six populated-page checks returned HTTP 200 with no horizontal overflow. Missing registration and optional URLs were separately checked. Test event IDs 1478/1479 were deleted; no sample events remain.

The empty archive was checked for its Events heading and no-events message. Review screenshots and JSON evidence are in `website/wordpress-events/review/`; populated screenshots show temporary test data only. Design preflight is retained there; inherited kit styling is authoritative for this template-reuse pass.

No real event facts, fees, payment settings or production content were published. Templates apply automatically once confirmed events are added.
