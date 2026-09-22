# Red White and Clix — vector logo variants

September 21, 2026 · Working artwork prepared by BlakSheep Creative.

Open `preview.html` or `Red White and Clix Logo Variants.pdf` to compare all nine variants. Use the files in `svg/` as the editable masters. The original supplied PNG is preserved in `source/original-logo.png`.

## Included

- Primary full-color badge, faithfully traced from the supplied artwork
- Full-color badge with white outline for dark backgrounds
- Full-color badge with black outline
- Single-color black badge with transparent letter knockouts
- Single-color white badge with transparent letter knockouts
- Black letterforms without the dial — proposed variant
- White letterforms without the dial — proposed variant
- Wide arrangement for light backgrounds — proposed lockup
- Wide arrangement for dark backgrounds — proposed lockup

Each variant includes an SVG, vector PDF and transparent PNG at 2400px wide. SVGs contain path geometry, with no embedded images, fonts or linked resources. All lettering and the memorial detail are paths traced from the supplied original; the wide lockups rearrange those existing word shapes without recreating them with a font.

## Use

The original black dial and its white/red/blue content are retained in the primary master. The single-color badge converts the word areas to transparent knockouts while retaining the memorial shape. The letterforms-only variants intentionally remove the dial. These variants are working options for review, not automatically adopted identity replacements.

White SVG, PNG and PDF files may appear blank on white. Place them on a dark surface to inspect them. Dark preview panels are only display aids and are not baked into those files. The primary badge itself contains the original black dial shape.

Preserve at least 10% clear space. Fine detail is limited by the source image and remains intricate; use size-specific proofs for small print, cutting or embroidery. A simplified small-size icon/favicon is not part of this delivery. The PDF artwork uses RGB vector colors; perform the printer's requested color conversion and prepress checks in the final layout.

## How it was made

The supplied RGBA image was classified into its four brand colors and transparency. Neutral antialiasing pixels remain neutral rather than becoming blue artifacts. Binary spline tracing preserved the outlines and internal cutouts; tiny isolated one-pixel speckles were removed. The original raster geometry is retained rather than replacing letterforms or inventing memorial details.

The trace was rendered back at the original resolution and visually compared against the source. The automated color/alpha classification comparison is recorded in `review/quality-report.json`; it is a diagnostic, not a guarantee of every small detail. Each production PDF was checked for vector drawing content and absence of embedded images.

Rebuild with Python, Pillow 12.3.0, vtracer 0.6.15 and Playwright 1.63.0; PDF verification uses PyMuPDF 1.28.2. Run `tools/build_vectors.py` then `tools/export_vectors.py`. The source masks and intermediate traces are included for reproducibility.
