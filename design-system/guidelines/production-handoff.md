# Production handoff

## Editing and exports
Use the studio to change editable SVG text without flattening. Keep copy close to the length of the master; long text must be reviewed in the preview. A blue or red dashed crop guide is an authoring aid; exports omit guides. Use SVG for editable handoff, PNG for crisp digital graphics, JPG for photo-heavy uploads, PDF for document review. Downloaded PNG/JPG uses the canvas dimensions in the template, not the scaled preview size. Font files and logo are embedded in exported SVGs. In applications that ignore embedded fonts, install the bundled TTFs, then reopen.

Browser Print / Save PDF on index.html uses US Letter pages, background graphics on, margins none and browser headers/footers off. The supplied PDF already applies those settings. All layouts remain editable in HTML/SVG; the PDF is the review/export format.

Print masters use US Letter trim (8.5 × 11 in). The contact card is 3.5 × 2 in at 300 canvas pixels per inch. Add printer-specified bleed (commonly 0.125 in) in the production file; these review masters do not include bleed, crop marks, a CMYK ICC profile or PDF/X certification. The 700px raster logo does not become vector by putting it inside SVG. At 300ppi its native width is 2.33in; request vector masters for larger print. CMYK values in the reference are mathematical approximations only; use the printer's profile and proof for conversion.

## One idea into a campaign
1. Capture the fact, source, reporting date, approved copy and one CTA.
2. Start with the matching content family; use portrait for the detailed composition, landscape for the concise split composition, story for the protected central stack.
3. Keep sources in the art for factual data. Move detailed explanation to a linked report or carousel.
4. Use the platform-map and specification file to choose a canvas. Check the actual uploader crop; interface overlays can change.
5. Export PNG/JPG for digital delivery. Keep the SVG as the editable record.

## Tokens and extensions
`tokens/tokens.json` is the simple CSS-oriented token map; `tokens/design-tokens.dtcg.json` is an interchange export. Complex CSS strings (shadows, easing, clamp) remain string tokens and may need mapping in design-tool importers. CSS is split by colors, typography, spacing, effects and social. Existing rwc token names are preserved. New success/info styles use blue, errors use red, warnings use ink and written labels; no new green/yellow palette is introduced.

New platforms should add dimensions, safe_rect_xywh, crop notes and a source in platform-specifications.json. Do not recolor another client's kit. The content family architecture is reusable; brand assets, tokens and typography are client-specific.

## Data and accessibility
Every chart includes title, subtitle, series labels, source/date and footnote slots. Schematic geometry is not data. Populate a verified dataset, calculate scales and labels, and keep an accessible table beside complex charts. Use line dashes, symbols and labels as well as color. Do not export bracketed values as campaign results.

Use 44px touch targets, visible focus, readable error messages, 16–18px minimum web body type and 12–14px captions. Normal text pairings have measured contrast in the reference. All user interface semantic statuses have text labels. Reduced-motion preference is honored. Components are specimens, not a certified production application.

## Ownership
Wesley Robertson is the brand guardian. Agency lead: Clint Sanchez, BlakSheep Creative. Record approvals of new taglines, identity masters, sponsor or beneficiary statements and public results. Review before each event and quarterly. This delivery sends no client communication and publishes nothing.
