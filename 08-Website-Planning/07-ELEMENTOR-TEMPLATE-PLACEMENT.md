# Elementor template placement — September 22, 2026

User direction: populate the local website from the uploaded Triple-A templates, preserving the original layout and content. No Red White and Clix copy or visual rebranding in this pass. Elementor is the selected builder.

## Page mapping

| Template | Source ID | Page ID | Local URL |
|---|---:|---:|---|
| Home | 1376 | 1204 | https://red-white-and-clicks.local/ |
| About Us | 1374 | 1205 | https://red-white-and-clicks.local/about/ |
| Teams | 1372 | 1206 | https://red-white-and-clicks.local/about/team/ |
| Pricing | 1367 | 1208 | https://red-white-and-clicks.local/pricing-plans/ |
| FAQ | 1351 | 1211 | https://red-white-and-clicks.local/faqs/ |
| News | 1337 | 1216 | https://red-white-and-clicks.local/blog-list/ |
| Contact Us | 1332 | 1217 | https://red-white-and-clicks.local/contact/ |
| Partners | 1364 | 1380 | https://red-white-and-clicks.local/partners/ |
| Track Order | 1340 | 1381 | https://red-white-and-clicks.local/track-order/ |
| Merchandise | 1326 | 1382 | https://red-white-and-clicks.local/merchandise/ |
| Login | 1314 | 1383 | https://red-white-and-clicks.local/login/ |
| Coming soon | 1307 | 1384 | https://red-white-and-clicks.local/coming-soon/ |

## Shared templates and restored dependencies

- Header 1304 and Footer 1273 assigned sitewide; Theme Builder condition cache regenerated.
- Single Post 1335, Archive Post 1329, Single Product 1300, Archive Product 1309, 404 1311, and Popup 1316 retain imported display conditions.
- Corrected source-demo page IDs: Cart template 1323 → page 1260; Checkout 1321 → 1261; My Account 1319 → 1262.
- Active Triple-A kit 1264 retained; source typography, colors, widget IDs, spacing, images and responsive settings preserved.
- Restored the original Triple-A logo (attachment 1455) from the template author's demo. This is template artwork, not the project's final identity.
- Restored five missing navigation menus from the author’s rendered demo, including original labels and hierarchy. Header/footer widgets now point at these menus. Matching page destinations point to the local pages. Original placeholder footer links and source product-detail link remain unchanged where no local counterpart exists.
- Disabled WooCommerce coming-soon locally so the imported shop templates can render. Removed the inherited SEOPress catch-all 404-to-home redirect so the kit's 404 design renders. Site remains noindex.

## Method and verification

All site changes went through Novamira MCP. Its dedicated Elementor content writer rejected legacy section/column trees and old alignment values. To preserve the requested exact layouts, the narrow fallback used Elementor's native document save API through Novamira execute-php. All 12 page trees compare equal to their imported source templates after saving. Menu bindings used the dedicated element-edit ability.

Desktop (1440px) and mobile (390px) checks covered 17 routes with no broken images or horizontal overflow. Utility routes were rechecked after visibility corrections. Screenshots and machine-readable results are in `website/wordpress-template-review/`.

The design preflight flagged generic Inter/purple CSS present in the full served HTML. No redesign was made: explicit template-preservation instructions govern this pass. The rendered kit retains Chakra Petch/Hind and its original palette.

## Limits and next pass

The site has zero products and only its existing single blog post. Dynamic product/news sections therefore cannot visually match the vendor's populated demo; no sample records were fabricated or imported. Empty-cart/checkout/account states are the site's real WooCommerce states. No payment setup or form submissions were performed.

Events and Donate remain untouched drafts: the kit has no matching templates, and repurposing a different template would be a separate content/layout decision. Other unrelated blueprint pages remain untouched. The Coming soon design is an ordinary preview page; it does not put the entire site into maintenance mode.

No production deployment occurred.

## Rollback

Before placement, all 46 existing page/template records and metadata were saved outside the public web root:
`/Users/clintsanchez/Local Sites/red-white-and-clicks/conf/backups/elementor-template-placement-20260922-191828.json`

Visibility settings backup:
`/Users/clintsanchez/Local Sites/red-white-and-clicks/conf/backups/template-visibility-20260922-192555.json`

New pages: 1380–1384. New navigation menus: 36–40. Restored logo: 1455.
