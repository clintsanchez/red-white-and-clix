# Sitemap and image audit

## Sitemap

- 27 URLs, all returning HTTP 200 on September 21, 2026.
- Root `/` is canonical but absent; `/home` is present and independently returns 200.
- 18 merchandise product URLs, 3 event product/detail URLs, one event index, three core pages and one shop index.
- `changefreq: daily` is applied to pages that do not appear to change daily. Search engines may ignore it; use accurate `lastmod` and reserve daily frequency for truly changing pages.
- Remove retired, duplicate, placeholder or noncanonical listings. Retain URLs that provide distinct value and have accurate inventory/pricing.

## Images on sampled pages

| Page | Images | Missing/empty alt | Coverage gap |
|---|---:|---:|---:|
| Homepage | 62 | 58 | 94% |
| About | 10 | 6 | 60% |
| Event hub | 11 | 7 | 64% |
| Donate | 6 | 2 | 33% |
| **Total** | **89** | **73** | **82%** |

Not every empty alt is an error: decorative art should remain empty. Sponsor logos, event photographs, venue imagery and functional linked images need useful alternatives. Audit each image by purpose rather than filling every field with keywords.

