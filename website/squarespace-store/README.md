# Store chrome — make shop.redwhiteandclix.org indistinguishable from www

`code-injection-header.html` and `code-injection-footer.html` put the live
site's exact header and footer on the Squarespace store: the same markup, the
same CSS (extracted from the published Instatic stylesheet), the same mobile
menu script. Every link returns to www, plus a cart link the store needs.
Squarespace's own header, footer and "Made with Squarespace" badge are hidden.

**Blocked on plan.** The store is on Squarespace **Basic** (`website_basic`).
Code Injection needs **Core** or above; saving returns 403 from
`/api/config/SaveInjectionSettings`. Nothing was saved.

Previewed by injecting client-side into the live store on 2026-09-27:
header 107 px (www: 107.5), six nav links in www order in Space Grotesk,
Donate pill #b91c1c, 64 px logo, Squarespace chrome hidden, content starting
directly below the header, product titles in Archivo Black. At 390 px the
burger opens and closes (Escape works) with no horizontal overflow.

To apply after upgrading: Website → Pages → Website Tools → Code Injection.
Paste the header file into HEADER and the footer file into FOOTER.

The CSS inside is extracted from www. If the main site's header or footer
changes, regenerate these files rather than hand-editing them.
