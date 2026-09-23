# BlakSheep SEO

> Plugin id: `blaksheep.seo`

Per-page `<head>` metadata for Instatic — the job Yoast does for WordPress.

Instatic 0.0.20 resolves an ordinary page's title through
`documentMeta.title -> settings.metaTitle -> page.title -> site.name`, and
supplies `documentMeta` only on post-type **entry** routes. Ordinary pages
therefore share one site-wide title and one site-wide description, and the
publisher emits no canonical or Open Graph tags at all.

This plugin closes that gap through the **`publish.html` filter**, which hands a
plugin the finished document plus `{ siteId, pageId, slug }` on every
HTML-emitting public route.

## What it emits

On **every** page:

- `og:type`, `og:site_name`, `og:locale`, `twitter:card`
- the default `og:image` (+ `og:image:secure_url`, type, width, height, alt)
- `og:title` / `og:description` / `twitter:title` / `twitter:description`, read
  from the rendered document when the page has no record of its own — so entry
  routes get social titles matching their real `<title>`

On pages it holds a **record** for, additionally:

- a replaced `<title>` and `<meta name="description">`
- `rel="canonical"` and `og:url`
- a page-specific `og:image`
- `noindex,nofollow` when the page is marked hidden

It strips every tag it owns before emitting, so it cannot produce duplicates —
including duplicates of tags injected by another plugin's `frontend.assets`.

## What it deliberately does not do

- **No canonical or `og:url` on entry routes.** `renderPublishedEntry` reports
  the TEMPLATE page's id and slug rather than the entry's, so there is no
  reliable URL to point at. A wrong canonical is worse than none.
- **No `og:image:width` / `height` for a page-specific image.** Dimensions are
  only stated for the configured default image, whose size the operator
  declared in settings.
- **No records for template pages.** The panel refuses them; setting a title
  there would apply it to every entry rendered from that template.

## Editing

The **SEO** panel in the site editor's left sidebar edits whichever page is
open: title, description, social image, and a hide-from-search switch, with a
search preview and character guidance.

Edits apply **on the next publish** — the pipeline bakes its output at publish
time rather than per request. The plugin clears its record cache on
`publish.before` so a save followed immediately by a publish cannot bake stale
data.

## Settings

| Setting | Notes |
| --- | --- |
| Site URL | Required for canonical and `og:url`; both are omitted while blank |
| Default social image | Absolute URL or site-root path |
| Site name / Locale | `og:site_name`, `og:locale` |
| Card style | `summary_large_image` or `summary` |
| Default image alt / width / height | Applied only to the default image |
| Title suffix | Appended to a record title that does not already contain it |

## Permissions

`cms.hooks`, `cms.storage`, `editor.panels`, `editor.store.read`, and
`editor.code` — the last is required by the host for any editor panel, and it
means the panel's JavaScript runs unsandboxed in the admin window with the same
access as the admin UI. Install shows a consent screen and requires password
re-confirmation.

## Building

The container has no `zip`, so build inside it and package on the host. Run from
`/app` so the `@core/*` aliases resolve:

```bash
docker cp plugins/blaksheep-seo <container>:/app/plugin-src/blaksheep-seo
docker exec -u root <container> chown -R bun:bun /app/plugin-src
docker exec -w /app <container> \
  bun run /app/src/core/plugin-sdk/cli/index.ts build /app/plugin-src/blaksheep-seo
# ends with "zip not found" — dist/ is complete
docker cp <container>:/app/plugin-src/blaksheep-seo/dist ./dist
cd dist && zip -r ../blaksheep-seo.plugin.zip .
```

Then `/admin/plugins` -> Upload Plugin. Settings and stored records survive an
upgrade.

Two id rules that produce the same confusing error: **resource ids must be
kebab-case** (`page-seo`), **plugin ids must be dotted** (`blaksheep.seo`).
