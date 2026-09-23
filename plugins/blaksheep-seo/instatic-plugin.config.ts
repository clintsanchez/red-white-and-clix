import { definePlugin, permissions } from '@core/plugin-sdk'

/**
 * BlakSheep SEO — per-page <head> metadata for Instatic.
 *
 * Instatic 0.0.20 resolves an ordinary page's title through
 * `documentMeta.title -> settings.metaTitle -> page.title -> site.name`, and
 * `documentMeta` is only supplied on post-type ENTRY routes. Ordinary pages
 * therefore share one site-wide title and one site-wide description, and the
 * publisher emits no canonical or Open Graph tags at all.
 *
 * This plugin fills that gap through the `publish.html` filter, which hands a
 * plugin the finished document plus `{ siteId, pageId, slug }` on every
 * HTML-emitting public route.
 *
 * Scope: ORDINARY PAGES ONLY. On an entry route the renderer reports the
 * template page's id and slug rather than the entry's own (see
 * `renderPublishedEntry` in server/publish/publicRenderer.ts), so neither a
 * canonical URL nor a per-entry lookup can be derived there. Entries already
 * carry native `seoTitle` / `seoDescription`, so the plugin no-ops on any page
 * it holds no record for, and the panel refuses to store records against
 * template pages.
 */
export default definePlugin({
  id: 'blaksheep.seo',
  name: 'BlakSheep SEO',
  version: '1.1.1',
  description:
    'Per-page meta title, description, canonical URL and social tags, edited from a panel in the site editor.',
  author: {
    name: 'BlakSheep Creative',
    url: 'https://blaksheepcreative.com/services/web-design-development/nonprofit-ngo/',
  },
  permissions: [
    permissions.cmsHooks,
    permissions.cmsStorage,
    // An editor panel is a React component running in the admin window, so
    // the host requires `editor.code` on top of `editor.panels`.
    permissions.editorCode,
    permissions.editorPanels,
    permissions.editorStoreRead,
  ],
  resources: [
    {
      id: 'page-seo',
      title: 'Page SEO',
      singularLabel: 'Page SEO record',
      pluralLabel: 'Page SEO records',
      fields: [
        { id: 'pageId', label: 'Page id', type: 'text', required: true },
        { id: 'slug', label: 'Page slug', type: 'text', required: true },
        { id: 'title', label: 'Meta title', type: 'text' },
        { id: 'description', label: 'Meta description', type: 'longtext' },
        { id: 'ogImage', label: 'Social image URL', type: 'text' },
        { id: 'noindex', label: 'Hide from search engines', type: 'boolean' },
      ],
    },
  ],
  settings: [
    {
      id: 'siteUrl',
      type: 'url',
      label: 'Site URL',
      description:
        'Absolute origin of the live site, e.g. https://www.redwhiteandclix.org. Required for canonical and og:url — both are omitted while this is blank, because a wrong canonical is worse than none.',
      default: '',
    },
    {
      id: 'defaultOgImage',
      type: 'text',
      label: 'Default social image',
      description:
        'Used for og:image when a page has no image of its own. Absolute URL, or a site-root path like /uploads/rwc/og-default.png.',
      default: '',
    },
    {
      id: 'siteName',
      type: 'text',
      label: 'Site name',
      description: 'Used for og:site_name — the name social platforms show above the card.',
      default: '',
    },
    {
      id: 'locale',
      type: 'text',
      label: 'Locale',
      description: 'Used for og:locale, e.g. en_US. Leave blank to omit the tag.',
      default: '',
    },
    {
      id: 'twitterCard',
      type: 'select',
      label: 'Card style',
      options: [
        { label: 'Large image', value: 'summary_large_image' },
        { label: 'Summary', value: 'summary' },
      ],
      default: 'summary_large_image',
    },
    {
      id: 'defaultOgImageAlt',
      type: 'text',
      label: 'Default social image alt text',
      description: 'Describes the default image for screen readers. Only applied to that image.',
      default: '',
    },
    {
      id: 'defaultOgImageWidth',
      type: 'text',
      label: 'Default social image width',
      description:
        'Pixel width of the default image, e.g. 1200. Stated only for that image — a page-specific image has no dimensions the plugin can vouch for.',
      default: '',
    },
    {
      id: 'defaultOgImageHeight',
      type: 'text',
      label: 'Default social image height',
      description: 'Pixel height of the default image, e.g. 630.',
      default: '',
    },
    {
      id: 'titleSuffix',
      type: 'text',
      label: 'Title suffix',
      description:
        'Appended to a page meta title that does not already contain it, e.g. " | Red, White, and Clix". Leave blank to use titles exactly as typed.',
      default: '',
    },
  ],
})
