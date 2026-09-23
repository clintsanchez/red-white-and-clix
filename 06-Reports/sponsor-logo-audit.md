# Sponsor logo audit — live site, September 23, 2026

Source: the "Our proud supporters" / "Community partners" wall on
https://www.redwhiteandclix.org/. 33 unique logo images, plus a repeated
divider graphic. Every file was downloaded at `?format=original` and measured;
the flagged images were opened and looked at, not judged by filename.

**Nothing here confirms who is or is not a current sponsor.** It records only
which images the live site displays today.

## Headline: there is not one vector file on the wall

All 33 are raster. Many are small enough to look soft on a retina screen at the
size the wall renders them.

## Provenance problems

### Screenshots of the sponsor's own website (4)

Captured browser windows, complete with page background — not logo files.

| Sponsor | File | Original size |
| --- | --- | --- |
| Smith IPM | `Screenshot_27-3-2026_151623_smithipm.com.jpeg` | 296 x 178 |
| Polished Perfection | `Screenshot_18-4-2026_14457_www.polished-perfection-llc.com.jpeg` | 418 x 225 |
| Printing Partners | `Screenshot_21-3-2026_121834_www.printingpartners.net.jpeg` | 247 x 122 |
| Spotlight Strategies | `Screenshot_21-3-2026_123036_www.spotlight-strategies.com.jpg` | 627 x 143 |

### Pulled from image search or a marketplace (4)

| Sponsor | File | Tell |
| --- | --- | --- |
| VFW | `OIP (1).webp` | `OIP` is Bing image-search's download name |
| (unidentified) | `R.jpg` | same |
| Texas Roadhouse | `435-4351303_texas-roadhouse-logo-texas-roadhouse-logo.png` | clipart-aggregator naming |
| (unidentified) | `f0ee5172-....__CR0,42,3061,918_PT0_SX600_V1___.jpg` | Amazon product-image CDN |

### Not a logo at all (1)

`mayday-games-blue-backed-premium-card-sleeves-66x91mm-80-pack-main-7927-7927.jpg`
is a product photo of card sleeves standing in for the Mayday Games mark.

### AI-generated artwork presented as a company's logo (2 confirmed)

Five files are named `ChatGPT Image …`. They are NOT all generated — each was
opened and judged on what it shows:

| File | Verdict |
| --- | --- |
| Blue Moon Comics | **Generated.** Cartoon globe, comic pages, "POW!" burst — and a Spider-Man-style web-shooting hand, i.e. Marvel IP, inside a mark on a nonprofit's sponsor wall |
| GamerMats | **Appears generated.** Clean but does not match the brand's real mark |
| DeFouw Automotive | Looks like the genuine mark |
| Calvary Church | Looks like the genuine mark |
| (1 repeated vertical graphic) | Divider, not a logo |

A generated logo is a business's identity rendered wrong and published under
their name. That is the item to fix first, ahead of any resolution work.

## Smallest files, by original pixels

| Sponsor | Original | Note |
| --- | --- | --- |
| Printing Partners | 247 x 122 | screenshot |
| Purdue Federal Credit Union | 200 x 200 | |
| Board & Dice | 239 x 227 | official SVG exists |
| Smith IPM | 296 x 178 | screenshot |
| Culver's | 640 x 400 | official SVG exists |
| Polished Perfection | 418 x 225 | screenshot |

## Replacements sourced so far

From each brand's own website, which is the right place to take a mark from:

| Sponsor | Source | Format |
| --- | --- | --- |
| Culver's | `cdn.culvers.com/.../culvers-logo_….svg` | SVG |
| Board & Dice | `boardanddice.com/wp-content/uploads/2025/07/boarddice_logo.svg` | SVG |

Several sites (VFW, Gen Con, Paizo, Valvoline, Texas Roadhouse, WLFI, GAMA,
Noble Knight, BCW) refused scripted requests or render their header in
JavaScript; those need a browser pass rather than a plain fetch.

## Before any of these get republished

Two questions for Wesley, both of which outrank the image quality work:

1. **Which of these are current sponsors?** The wall mixes national brands,
   local businesses, a church and a hotel. `CLAUDE.md` is explicit that we do
   not confirm sponsor endorsement on our own.
2. **Do we have permission to display each mark?** Re-publishing 30+
   third-party trademarks on a nonprofit's site is the client's call, and
   several brands (Gen Con, Paizo, Valvoline) publish usage rules worth
   following.

The AI-generated Blue Moon Comics logo should come down regardless of the
answers.
