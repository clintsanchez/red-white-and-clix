# Squarespace asset rescue — 2026-09-26

Run before the DNS cutover, because **every one of these files dies the moment
`redwhiteandclix.org` stops pointing at Squarespace.** The WLFI interview video
was the first thing found this way; this sweep is the rest.

Crawled all 27 URLs in the Squarespace sitemap, extracted every
`squarespace-cdn.com` asset reference, and pulled each at `?format=original`.

**332 files, 121 MB, zero failures.** Archived to pCloud at
`Clients/Red White and Clix/05-Photos/squarespace-rescue-2026-09-26/`, sorted
into the categories below. Not committed — 121 MB does not belong in a public
repo, and most of it is disposable.

| Count | Size | Category | Verdict |
|---|---|---|---|
| 194 | 31.7 MB | `product-mockups` | Printful/Printify renders. Regenerable, keep as backup only. |
| 58 | 15.1 MB | `other` | Mixed. Needs eyes. |
| 37 | 69.4 MB | `ai-generated` | ChatGPT/Gemini artwork, Feb–May 2026. |
| 21 | 1.4 MB | `sponsor-logos` | Mostly superseded by the better sources already in `website/sponsors/logos/`. |
| **10** | **2.9 MB** | **`event-photos-FULLRES`** | **The find. See below.** |
| 7 | 0.1 MB | `event-photos-thumbnails-USELESS` | 206x206. Same junk he emailed. |
| 5 | 0.3 MB | `LICENSING-RISK` | See below. |

## The event photos

Since 2026-09-23 the position has been that we had no usable event photography
— the 102 images Wesley emailed were **206x206 Facebook thumbnails**, ~11 KB
each, which is why AI upscaling was refused (see `no-ai-upscaling-of-real-people`
in Claude memory) and why a Facebook *Download Your Information* export was
requested and never arrived.

**Ten full-resolution originals were on his own Squarespace site the whole time:**

- 2048x1536, 1542x2048 (x2), 1536x2048 (x2), 1736x1302, 1355x1800, 1200x904,
  1109x831, 720x960

That is up to **99x the pixel count** of the emailed versions. The Facebook
export is no longer needed for these ten.

Seven more in the same set are still 206x206 — he uploaded thumbnails to
Squarespace too, so the export may still be worth chasing for the rest.

**Consent is still unresolved for these.** Wesley's 2026-09-26 position (posed
shots, two years public, no complaints) covers publication in principle, but
these are higher resolution and more identifiable than anything discussed.

## LICENSING-RISK — five files on the live site today

Filenames indicate unlicensed use. Not a guess; these are the sizes and naming
conventions those services use for previews:

| File | What the name means | On |
|---|---|---|
| `istockphoto-1401203567-612x612.jpg` | iStock **comp/preview** size | `/home` |
| `american-soldier-uniform-civil-man-260nw-1244136541.webp` | Shutterstock **watermark-preview** size (`260nw`) | `/donate` |
| `maxresdefault.jpg` | YouTube video thumbnail | `/services-store`, `/services-store/p/300-modern-1` |
| `OIP (1).webp` | Bing image-search result filename | `/home` |
| `R.jpg` | Bing/Google image-search result filename | `/home` |

**None of these reached the new site** — verified across every page and the
repo. They die with the Squarespace cutover, which is the right outcome. Worth
mentioning to Wesley only as a "do not re-add these" note; it is the same class
of problem he already spotted himself with the Spider-Man logo.

## Method note

`?format=original` on a Squarespace CDN URL serves the uploaded file rather
than a resized derivative. That is what recovered the full-resolution photos —
the pages themselves only ever request `?format=500w` and similar.
