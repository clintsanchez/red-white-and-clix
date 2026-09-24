# Event photos from Wesley — inventory, September 23, 2026

Wesley emailed 102 photographs with his content packet. **They are Facebook
thumbnails, not the photographs**, and cannot be used on the site.

## Measured, not estimated

Zip: `redwhiteandclixwebsite.zip`, 1.7MB for 102 images — about 17KB each.

| Long edge | Count |
| --- | --- |
| under 800px | **100** |
| 800–1199px | 0 |
| 1200–1999px | 0 |
| 2000px+ | 2 |

Median image: **206 x 206, 11KB**. Smallest 205 x 206. Only two are real
photographs, one of them 3840 x 2160.

Facebook downsizes images attached to an email, so what arrived is a preview of
each photo rather than the photo.

## Why upscaling was rejected

Enlarging a 206px file to a usable 1200px web width is a 5.8x jump with
**0.029 real source pixels per output pixel**. A test render confirmed it: soft
and smeared rather than blocky, because Lanczos trades one artefact for
another. There is no detail in a 5KB file to recover.

AI upscalers (Real-ESRGAN, Topaz and similar) do not recover detail, they
generate it — including faces. These are documentary photographs of
identifiable veterans at real events, so inventing facial detail is not
acceptable here, and it would sit badly beside the AI-generated sponsor logos
we are asking the client to replace.

## Scraping the live site does not solve it

The live Squarespace site was crawled in full: 27 pages, 544 unique image URLs.
Matching by Facebook photo id against the 99 ids in the zip:

- **3** are recoverable from the site at a genuinely better size
  (e.g. 206x206 5KB -> 1200x904 130KB via `?format=original`)
- **96** do not appear on the site at all

The earlier `05-Photos/site-pull` archive tells the same story: of 333 assets,
242 are merchandise product shots and only 11 are event photographs. The site
simply does not display these photos.

## What was asked for

A reply was **sent** on 2026-09-23 asking Wesley to run Facebook's *Download
Your Information* export with **Media quality: High**, with two shortcuts
offered: camera-roll originals if the photos are his, or a handful at full size
if he knows which ones he wants on the site.

## Still open

- Which event each batch of photos is from. **Do not infer this from filenames**
  — the Facebook ids carry no reliable date, and `CLAUDE.md` forbids it.
- Reuse restrictions.
- **Consent to publish photographs of identifiable people.** Not yet asked.
  Must be settled before any of these appear on the public site.

When the originals arrive, archive them to pCloud `05-Photos/` following the
existing convention: `<hash10>-<original-filename>` plus a `MANIFEST.json`
carrying sha256, dimensions, provenance, category and rights. Descriptive
slugs and alt text belong on the published subset only, not the archive, and
must describe the scene rather than name anyone.
