# Red White and Clix — Complete design kit

Edition 1.0 · September 21, 2026 · Prepared by BlakSheep Creative.

Open `index.html` for the complete visual reference. It is self-contained and works offline. Choose Print / Save PDF or use the supplied PDF in `exports/`.
Open `template-studio.html` to browse templates, edit text, toggle crop guides, and download SVG, PNG, or JPG. Changes stay in the browser until you save an SVG; reopening a template resets it. Save your edited SVG before switching templates. Source SVGs also open in vector editors; install the included fonts first when your editor does not support embedded font CSS.

## Included
- Visual brand system and component reference (HTML and PDF)
- CSS tokens, JSON token map, and DTCG-style token export
- Native HTML components with shared CSS
- Editable SVG social, chart, print and slide masters
- Bundled Archivo Black and Space Grotesk fonts with OFL licenses
- Official supplied logo and 14 documentary photo references with provenance
- Platform configuration, template inventory, source briefs and handoff documentation

## Start a design
1. Read `2 - Brand Guidelines.md` and `3 - Visual Identity.md`.
2. Duplicate a relevant template in the studio or your vector editor.
3. Replace all bracketed or CONFIRM fields with sourced information.
4. Confirm photographic rights/context, event details, sponsor status and CTA destination.
5. Check small-screen readability and crop preview, then export.

## Status
The supplied logo and existing palette/typefaces are established. The UI, layouts, component system and templates are a working extension for review. The proposed campaign line has not replaced “One Community. One Mission.” No new logo lockups or faithful vector master have been invented. Chart drawings are schematic placeholders, not reported results; use verified data to calculate final geometry. Shared platform masters do not imply ownership of those accounts.

## For developers
Link `styles.css` or import the individual token files. `components/*.html` are framework-free standalone specimens; copy the markup inside main into your project. Buttons and forms in the reference are visual specimens, with no backend, checkout or newsletter submission. The future website is not implemented by this kit.

## Rebuild
With Python 3.12+, install the packages in `tools/requirements.txt`. Run `python tools/build_kit.py`, then `python tools/export_and_check.py`. The builder reads the existing repository brand files and the client photo directory; it is intended for the agency workspace. The exported HTML/SVG/CSS/PDF files themselves have no build dependency.
