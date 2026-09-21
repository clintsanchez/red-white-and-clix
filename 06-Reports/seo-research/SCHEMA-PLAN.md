# Red White and Clix — schema plan

## Replace the sitewide entity model

Use one `NGO` or `Organization` entity with a stable `@id`, complete description, legal name, URL, logo, email, telephone, tax ID if approved, and verified `sameAs` links. Remove `LocalBusiness` unless the organization maintains a staffed public location and real opening hours. Never publish `00:00–00:00` as operating hours.

## Add Event entities

Each event needs a separate `Event` object. Confirm the price, whether Team Sealed pricing is per team, registration URL, start/end times and image before publishing. Use the Lafayette National Guard Armory as `Place` for the event, not as the organization’s mailing address.

## Supporting types

- `WebSite` on the root entity graph.
- `BreadcrumbList` on internal pages.
- `Product` and `Offer` for active merchandise only.
- `Article` for evergreen guides and event recaps.
- Avoid `FAQPage` until every answer is verified and visible.

Validation sequence: Schema.org parser, Google Rich Results Test for supported types, then URL Inspection after deployment.

