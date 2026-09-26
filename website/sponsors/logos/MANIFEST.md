# Sourced sponsor logos

Every file here came from the brand's **own website**, which is the right place
to take a mark from — not an image search, not a clipart aggregator, not a
screenshot. Sourced September 23, 2026.

Nothing here confirms who is a current sponsor. See
`06-Reports/sponsor-logo-audit.md`.

## Use these — they are real upgrades

| Sponsor | On the live site now | Sourced | Why it wins |
| --- | --- | --- | --- |
| Printing Partners | 247 x 122 **screenshot of their website** | `printing-partners.svg` | vector, and no longer a screenshot |
| Purdue Federal Credit Union | 200 x 200 JPEG | `purdue-federal.svg` | vector |
| Culver's | 640 x 400 JPEG | `culvers.svg` | vector |
| Board & Dice | 239 x 227 JPEG | `board-and-dice.svg` | vector |
| WLFI | raster | `wlfi.svg` | vector, 1816 x 747 |
| Paizo | 256 x 330 | `paizo.png` 1300 x 475 | 5x the pixels, official |
| VFW | 474 x 474 **Bing image-search grab** (`OIP (1).webp`) | `vfw.png` 275 x 87 | authentic file rather than a search result |
| Texas Roadhouse | 840 x 484 **clipart-aggregator PNG** | `texas-roadhouse.png` 613 x 330 | official, transparent, full colour |
| GAMA | small raster | `gama.png` 459 x 157 | official |
| Spotlight Strategies | 627 x 143 **screenshot of their website** | `spotlight-strategies.png` 600 x 109 | official file, transparent, no page background |
| 4imprint | 1216 x 288 raster | `4imprint.svg` | vector — extracted from their sprite, see below |

## Keep what the live site already has

Resolution is not uniformly the problem. These current files are considerably
larger than anything published on the brand's own site, so swapping them in
would make the wall *worse*:

| Sponsor | Live site | Sourced | Verdict |
| --- | --- | --- | --- |
| Gen Con | 2500 x 1659 | 554 x 397 | keep current |
| Valvoline | 2500 x 1699 | 197 x 57 | keep current |
| Sticker Ninja | 1884 x 752 | 747 x 411 | keep current |
| Noble Knight | 1200 x 1200 | 170 x 85 | keep current |
| Red Raven Games | 1196 x 1104 | 512 x 512 | keep current |
| BCW Supplies | 1696 x 576 | `bcw-supplies.png` 227 x 76 | keep current |
| Wyrd Games | 474 x 474 | `wyrd-games.webp` 183 x 105 | keep current — Squarespace caps the header logo at source size |
| Mission Breakout | 2420 x 2420 | their site's `mission_breakout_sub_logo.png` 213 x 39 | keep current |

Their provenance is still unverified — they are simply good enough that a
smaller official file is not an improvement.

## Neither option is good

| Sponsor | Problem |
| --- | --- |
| Chaosium | Live file is 651 x 651 but has a **grey background baked in**, which will show as a box on the wall. The official header logo is only 204 x 60. Ask the brand for a transparent asset. |

## GamerMats is now GameHead

`gamermats.com` **redirects to `gamehead.com`**, whose page title reads
"GameHead.com - GameHead | GamerMats". The brand has been renamed or absorbed.

That makes the live site's entry doubly wrong: the logo shown for it is
AI-generated (see the audit), and the name it is generated for is no longer the
company's. `gamehead.png` (1200 x 1200, official) is here, but **which name to
display is Wesley's call** — whether the sponsor is GameHead the company or
GamerMats the product line.

## 4imprint: extracted from an SVG sprite

4imprint does not ship a standalone logo file. Their header references
`/icons/iconLibrary.svg#svgLogo-4imprint` — one `<symbol>` inside an 80KB
sprite. `4imprint.svg` here is that symbol lifted into a standalone file with
the symbol's own `viewBox` (0 0 140 53).

Verified before use: it references no `url(#…)`, `xlink:href` or `<use>` left
behind in the sprite, carries only the two brand fills (#02458b, #221f20), and
renders correctly in a browser. An extracted symbol that silently loses a
clipPath is the usual failure here, so it was rendered and looked at rather
than assumed.

## No logo file exists to take

| Sponsor | What their site actually has |
| --- | --- |
| Smith IPM | A text wordmark in the header, no logo image. Only a favicon. |
| Polished Perfection | Header is text only; the page carries photos and a business card image, no mark. |
| DeFouw Automotive | Header logo is not a plain `<img>`; needs a closer look or a request to them. |
| Mayday Games | Shopify header carries only icons; no logo asset exposed. |

For these the honest move is to ask the business for their logo file. Both
Smith IPM and Polished Perfection are currently represented on the live site by
screenshots of their websites, so anything they send will be an improvement.

## Still to source

| Sponsor | Status |
| --- | --- |
| Blue Moon Comics | **`bluemooncomics.net` does not resolve.** The shop trades as *BlueMoon Comics Strikes Back* (2405 S Earl Ave, Lafayette) and appears to run on Facebook only — so the wall's AI-generated logo is also under a name the business does not use in full. Ask the shop. |
| Pressed in Pink | Not findable by search. Ask Wesley. |
| Paladin Games | Not findable by search. Ask Wesley. |
| Farmers Market | Too generic to identify safely. Ask Wesley which market. |
| Calvary Church | The file on the live site already looks like the genuine mark. |
| Squarespace | Their website platform, not a sponsor — and moot once the site moves off it. |

The long tail here is small local businesses with little or no web presence.
Chasing them by search risks attaching the **wrong** company's logo to a
sponsor, which is worse than a soft JPEG. The right move is a list from Wesley
with each sponsor's correct name, URL and logo file.

## Batch 2 — sourced 2026-09-24 (Wesley's confirmed sponsor list)

Every file came from the company's own site or its own CDN. Each raster file was opened and looked at. Each SVG was rendered in headless Chrome and looked at. No existing file in this folder was changed.

| Sponsor | file | format + dimensions | exact source URL | notes |
| --- | --- | --- | --- | --- |
| KFC | `kfc.svg` | SVG, viewBox 526 x 180 | inline header `<svg id="Graphics">` on https://global.kfc.com/ | Red (#f5002b) KFC wordmark with ®, transparent. KFC's global brand site. www.kfc.com returns 403 (Akamai) to curl, so the US site was not checked. Wordmark only, no Colonel. |
| Meijer | `meijer.svg` | SVG | https://newsroom.meijer.com/images/meijer-logo.svg | Full-colour (red + blue dots), transparent. Taken from Meijer's own newsroom because www.meijer.com returns 403. |
| Fastenal | `fastenal.png` | PNG 638 x 139, no alpha | https://careers.fastenal.com/wp-content/uploads/2023/08/fastenal-logo-blue-white.png | Standard blue box with white wordmark. The blue box is part of the mark, so no extra background is needed. www.fastenal.com and investor.fastenal.com return 403. Taken from Fastenal's own careers site. |
| The Home Depot | `the-home-depot-white.svg` | SVG, viewBox 186 x 186 | https://corporate.homedepot.com/themes/custom/bootstrap_thd/images/logo-site-header-homedepot.svg | **White-only knockout.** Must sit on Home Depot orange **#F96302** (their CSS `--bs-primary`), where it renders as the correct logo. On white it is invisible. www.homedepot.com returns 403. |
| Squarespace | `squarespace-white.svg` | SVG, viewBox 208 x 30 | inline `global-navigation__logo--desktop` svg on https://www.squarespace.com/ | **White-only** (fill="white"). Needs a dark background. A black version would mean recolouring the file, which was not done. |
| GMT Games | `gmt-games.png` | PNG 463 x 463, alpha | https://www.gmtgames.com/skins/custom/images/gmt-games-logo.png (CSS background of `.header-logo`) | Red rounded square with white text. Self-contained, works on any background. There is no SVG at the same path (404). |
| Level 99 Games | `level-99-games.png` | PNG 6674 x 1587, alpha | https://www.level99games.com/cdn/shop/files/l99-games_horizontal-green_a2356496-63cb-4108-b44c-382af7586dbb.png?v=1683147330 | Horizontal logo: green icon and black text. Transparent. Dark-on-light. |
| Ultimate Guard | `ultimate-guard.svg` (+ `ultimate-guard-signet.svg`) | SVG, viewBox 824 x 99 (signet 81 x 99) | https://ultimateguard.com/media/f2/15/24/1685597656/UG%20Logo%20-%202022%20-%20Wordmark%20-%20Single%20-%20Black.svg (og:image) ; signet: https://ultimateguard.com/media/88/3c/71/1685599983/UG%20Logo%20-%202022%20-%20Signet%20-%20Black.svg | Black (#222221) on transparent. Dark-on-light. |
| Quiver Time | `quiver-time.png` | PNG 1662 x 371, alpha | https://quivertime.com/wp-content/uploads/2019/02/Quiver-Time-Logo-Long.png (full-size original of the header `header_logo` 1024w) | Black script "Quiver" wordmark. Dark-on-light. Quiver Time sells card cases, not published games. Matched on the name only. |
| Mayday Games | `mayday-games.png`, `mayday-games.ai`, `mayday-games-2100w.png` | PNG 500 x 72 alpha; AI (PDF-compatible vector); PNG 2100 x 600 alpha | https://cdn.shopify.com/s/files/1/1098/0948/files/mayday-logo.png and https://cdn.shopify.com/s/files/1/1098/0948/files/logo.ai, linked as "Download The Mayday Logo" under Resources on https://www.maydaygames.com/pages/in-the-news | These are the official press downloads. `-2100w.png` was **rasterized locally** from the official .ai at 6x, with nothing edited. Dark grey/black wordmark. Dark-on-light. |
| DeFouw Automotive | `defouw-automotive.png` | PNG 1515 x 485, alpha | https://defouw.com/assets/images/image01.png?v=46158caa | This is the homepage lead image, directly above "Welcome to DeFOUW Automotive, Lafayette's full-service dealership since 1961". Address confirmed on the site: 320 Sagamore Pkwy S, Lafayette IN. Blue and silver with light-grey car outline. **Best on white or light.** The silver parts wash out on pale grey. |
| Smith IPM | `smith-ipm.webp` | WebP 512 x 296, alpha | https://smithipm.com/wp-content/uploads/2023/09/cropped-cropped-SmithIPM_Favicon.webp | The filename says "Favicon", but this is the full logo: "Smith IPM – Always a quality experience" in a red hexagon. It is the site's JSON-LD `logo` and appears on the page. Last batch's note "text wordmark only" was wrong. Dark-on-light. Title confirms Lafayette, Indiana. |
| Tippecanoe Memory Gardens | `tippecanoe-memory-gardens.png` | PNG 1434 x 321, alpha | https://www.tippecanoememorygardens.com/wp-content/uploads/2024/12/2022-TMG-Only-LOGO.png (JSON-LD `logo`) | Blue dove and blue serif text. Transparent. Dark-on-light. A smaller 472 x 116 header version also exists (/2024/01/logo.png). Site lists Lafayette, IN 47906. |
| Arni's Restaurant | `arnis.png` | PNG 400 x 400, alpha | https://meetyouatarnis.com/wp-content/uploads/2022/04/Arnis-Logo-2022.png (JSON-LD `logo`) | Black circular "Meet You at Arni's Restaurant" badge. Self-contained on any background. It is soft/JPEG-ish at 400px. The header "arnis-logo-copy-1.svg" is only a wrapper around a 300 x 114 raster, so it is not a vector. arnis.com is a parked domain. |
| Lauren Ashley Design | `lauren-ashley-design-white.svg` | SVG, viewBox 1845 x 810 | inline Wix vector-image `svg[data-type="ugc"]` on https://www.lashleydesign.com/ | **White-only**, needs a dark background. Reads "LAUREN ASHLEY DESIGN — STUDIO" in a frame. The viewBox has a lot of empty padding (artwork bbox 37,241 to 1805,540), so crop it when placing. Site title reads "Interior Design in Lafayette, IN". |

### Unresolved in this batch

| Sponsor | Why |
| --- | --- |
| Paladin Games | No website found. Searches show only an Instagram "@paladinsgames" (Paladins Games Store) with no location confirmed, and unrelated video-game results. Ask Wesley for the URL or the file. |
| Blue Moon Comics Strikes Back | No own website. bluemooncomics.net does not resolve. bluemooncomics.com is a **different shop** (San Rafael, CA). The Lafayette shop (2405 S Earl Ave) appears on Facebook only. Nothing taken. **Do not reuse the current AI-generated wall image**, which includes Spider-Man (Marvel IP). Ask the shop for their logo file. |
