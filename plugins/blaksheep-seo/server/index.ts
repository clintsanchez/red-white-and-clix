import type { ServerPluginApi, ServerPluginModule } from '@core/plugin-sdk'

/**
 * Server entrypoint — owns the whole social/search block in <head>.
 *
 * Runs on EVERY public HTML response via the `publish.html` filter, in two
 * layers:
 *
 *   1. Site-wide constants (og:type, og:site_name, og:locale, twitter:card,
 *      default og:image) on every page — the job the older static
 *      `blaksheep.social-meta` plugin did through `frontend.assets`.
 *   2. Per-page overrides for any page this plugin holds a record for —
 *      title, description, canonical, og:url and a page-specific image.
 *
 * Layer 1 matters because `og:title` / `og:description` are read from the
 * rendered document when there is no record, so ENTRY routes (state pages,
 * events) get social titles matching their own <title> and description. A
 * static manifest could never vary those.
 *
 * The pipeline's output is BAKED at publish time, not applied per request, so
 * edits reach the live site on the next publish. The record cache is cleared on
 * `publish.before` — without that, saving in the panel and publishing a second
 * later could bake a stale record.
 *
 * Canonical and og:url are still record-only: on an entry route the renderer
 * reports the TEMPLATE page's id and slug (`renderPublishedEntry` in
 * server/publish/publicRenderer.ts), so there is no reliable URL to point at.
 * Emitting a guess would be worse than emitting nothing.
 */

const RESOURCE = 'page-seo'
const CACHE_TTL_MS = 15_000

interface SeoRecord {
  pageId: string
  slug: string
  title?: string
  description?: string
  ogImage?: string
  noindex?: boolean
}

function escapeAttr(value: string): string {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

/** `index` is the site root; every other slug is its own path segment. */
function permalinkFor(slug: string): string {
  const trimmed = slug.replace(/^\/+|\/+$/g, '')
  return trimmed === 'index' || trimmed === '' ? '/' : `/${trimmed}`
}

function joinUrl(origin: string, path: string): string {
  return `${origin.replace(/\/+$/, '')}${path.startsWith('/') ? path : `/${path}`}`
}

/**
 * Absolute-ise an image reference. Scrapers do not reliably resolve a relative
 * og:image, so a relative path without a configured site URL yields nothing
 * rather than a tag that will not resolve.
 */
function absoluteImage(value: string, siteUrl: string): string | null {
  if (!value) return null
  if (/^https?:\/\//i.test(value)) return value
  if (!siteUrl) return null
  return joinUrl(siteUrl, value)
}

function stripMetaByName(html: string, names: string[]): string {
  let out = html
  for (const name of names) {
    const re = new RegExp(`[ \\t]*<meta[^>]*\\bname=["']${name}["'][^>]*>\\s*`, 'gi')
    out = out.replace(re, '\n  ')
  }
  return out
}

function stripMetaByProperty(html: string, properties: string[]): string {
  let out = html
  for (const property of properties) {
    const re = new RegExp(`[ \\t]*<meta[^>]*\\bproperty=["']${property}["'][^>]*>\\s*`, 'gi')
    out = out.replace(re, '\n  ')
  }
  return out
}

function stripCanonical(html: string): string {
  return html.replace(/[ \t]*<link[^>]*\brel=["']canonical["'][^>]*>\s*/gi, '\n  ')
}

/** Read the rendered <title> so og:title can mirror it on entry routes. */
function existingTitle(html: string): string {
  const match = html.match(/<title>([\s\S]*?)<\/title>/i)
  return match ? match[1].trim() : ''
}

function existingDescription(html: string): string {
  const match = html.match(
    /<meta[^>]*\bname=["']description["'][^>]*\bcontent=["']([^"']*)["'][^>]*>/i,
  )
  return match ? match[1].trim() : ''
}

function applyTitleSuffix(title: string, suffix: string): string {
  if (!suffix) return title
  return title.includes(suffix.trim()) ? title : `${title}${suffix}`
}

/** Guess a MIME type from the extension; only used for the default image. */
function imageMimeType(url: string): string | null {
  const clean = url.split('?')[0].toLowerCase()
  if (clean.endsWith('.png')) return 'image/png'
  if (clean.endsWith('.jpg') || clean.endsWith('.jpeg')) return 'image/jpeg'
  if (clean.endsWith('.webp')) return 'image/webp'
  if (clean.endsWith('.gif')) return 'image/gif'
  return null
}

const OG_PROPERTIES_OWNED = [
  'og:type',
  'og:site_name',
  'og:locale',
  'og:title',
  'og:description',
  'og:url',
  'og:image',
  'og:image:secure_url',
  'og:image:type',
  'og:image:width',
  'og:image:height',
  'og:image:alt',
]

const META_NAMES_OWNED = [
  'robots',
  'twitter:card',
  'twitter:title',
  'twitter:description',
  'twitter:image',
  'twitter:image:alt',
]

export default {
  async activate(api: ServerPluginApi) {
    let cache: Map<string, SeoRecord> | null = null
    let cachedAt = 0

    async function records(): Promise<Map<string, SeoRecord>> {
      const now = Date.now()
      if (cache && now - cachedAt < CACHE_TTL_MS) return cache
      const next = new Map<string, SeoRecord>()
      try {
        // A site has far fewer pages than the 1000-row cap; one read covers it.
        const result = await api.cms.storage.collection(RESOURCE).list({ limit: 1000 })
        for (const record of result.records) {
          const data = record.data as unknown as SeoRecord
          if (data && typeof data.pageId === 'string') next.set(data.pageId, data)
        }
      } catch (error) {
        // Never let an SEO lookup take down a page response.
        api.plugin.log('[blaksheep.seo] storage read failed:', String(error))
        return cache ?? next
      }
      cache = next
      cachedAt = now
      return next
    }

    // A publish is the moment the filter's output gets baked, so drop the
    // cache first and read every record fresh.
    api.cms.hooks.on('publish.before', () => {
      cache = null
      cachedAt = 0
    })

    api.cms.hooks.filter(
      'publish.html',
      async (html: string, context: { pageId: string; slug: string }) => {
        const setting = (key: string) => (api.cms.settings.get<string>(key) ?? '').trim()

        const record = (await records()).get(context.pageId)
        const siteUrl = setting('siteUrl')
        const siteName = setting('siteName')
        const locale = setting('locale')
        const twitterCard = setting('twitterCard') || 'summary_large_image'
        const defaultImage = setting('defaultOgImage')
        const defaultImageAlt = setting('defaultOgImageAlt')
        const defaultImageWidth = setting('defaultOgImageWidth')
        const defaultImageHeight = setting('defaultOgImageHeight')

        const title = record?.title
          ? applyTitleSuffix(record.title.trim(), api.cms.settings.get<string>('titleSuffix') ?? '')
          : existingTitle(html)
        const description = (record?.description ?? '').trim() || existingDescription(html)
        const canonical = record && siteUrl ? joinUrl(siteUrl, permalinkFor(record.slug)) : null

        const pageImage = (record?.ogImage ?? '').trim()
        const usingDefaultImage = pageImage === ''
        const image = absoluteImage(pageImage || defaultImage, siteUrl)

        let out = html

        if (record?.title) {
          out = out.replace(/<title>[\s\S]*?<\/title>/i, `<title>${escapeAttr(title)}</title>`)
        }
        // Replace rather than append — the site-wide description tag is already
        // in the document, and two description tags is worse than one.
        if (record?.description) out = stripMetaByName(out, ['description'])

        out = stripMetaByName(out, META_NAMES_OWNED)
        out = stripMetaByProperty(out, OG_PROPERTIES_OWNED)
        if (canonical) out = stripCanonical(out)

        const tags: string[] = []

        if (record?.noindex) tags.push('<meta name="robots" content="noindex,nofollow">')
        if (record?.description) {
          tags.push(`<meta name="description" content="${escapeAttr(description)}">`)
        }
        if (canonical) tags.push(`<link rel="canonical" href="${escapeAttr(canonical)}">`)

        // --- Site-wide constants -------------------------------------------
        tags.push('<meta property="og:type" content="website">')
        if (siteName) tags.push(`<meta property="og:site_name" content="${escapeAttr(siteName)}">`)
        if (locale) tags.push(`<meta property="og:locale" content="${escapeAttr(locale)}">`)

        // --- Per-document values -------------------------------------------
        if (title) tags.push(`<meta property="og:title" content="${escapeAttr(title)}">`)
        if (description) {
          tags.push(`<meta property="og:description" content="${escapeAttr(description)}">`)
        }
        if (canonical) tags.push(`<meta property="og:url" content="${escapeAttr(canonical)}">`)

        if (image) {
          tags.push(`<meta property="og:image" content="${escapeAttr(image)}">`)
          if (image.startsWith('https://')) {
            tags.push(`<meta property="og:image:secure_url" content="${escapeAttr(image)}">`)
          }
          // Dimensions and type are only stated for the CONFIGURED default
          // image, whose size the operator has declared. A page-specific
          // image has no dimensions we can vouch for, and a wrong
          // og:image:width is worse than an absent one.
          if (usingDefaultImage) {
            const mime = imageMimeType(image)
            if (mime) tags.push(`<meta property="og:image:type" content="${mime}">`)
            if (defaultImageWidth) {
              tags.push(`<meta property="og:image:width" content="${escapeAttr(defaultImageWidth)}">`)
            }
            if (defaultImageHeight) {
              tags.push(
                `<meta property="og:image:height" content="${escapeAttr(defaultImageHeight)}">`,
              )
            }
            if (defaultImageAlt) {
              tags.push(`<meta property="og:image:alt" content="${escapeAttr(defaultImageAlt)}">`)
            }
          }
        }

        // --- Twitter --------------------------------------------------------
        tags.push(`<meta name="twitter:card" content="${escapeAttr(twitterCard)}">`)
        if (title) tags.push(`<meta name="twitter:title" content="${escapeAttr(title)}">`)
        if (description) {
          tags.push(`<meta name="twitter:description" content="${escapeAttr(description)}">`)
        }
        if (image) {
          tags.push(`<meta name="twitter:image" content="${escapeAttr(image)}">`)
          if (usingDefaultImage && defaultImageAlt) {
            tags.push(`<meta name="twitter:image:alt" content="${escapeAttr(defaultImageAlt)}">`)
          }
        }

        const block = tags.map((tag) => `  ${tag}`).join('\n')
        if (/<\/head>/i.test(out)) return out.replace(/<\/head>/i, `${block}\n</head>`)
        return out
      },
    )

    api.plugin.log('[blaksheep.seo] publish.html filter registered')
  },
} satisfies ServerPluginModule
