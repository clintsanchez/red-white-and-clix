# Start here — Claude Design

This repository contains the brand kit and the current WordPress website work for Red White and Clix.

## Current website design source

Use `website/wordpress-snapshot/site.json` for the actual Elementor section/widget trees, active kit settings, menus, Meta Box field definitions, and business options. Local assets are in `website/wordpress-snapshot/assets/`, mapped from WordPress URLs by `asset-map.json`. The `.local` site itself is only available on the developer's Mac.

Use the latest desktop/mobile screenshots in `website/wordpress-header-footer/review/`, the event template screenshots in `website/wordpress-events/review/`, and page screenshots in `website/wordpress-template-review/` as visual references. Event screenshots containing sample events are layout fixtures; those events have been deleted. Business details are authoritative in `00-Client-Brief.md` and the exported global options.

The current website uses the imported Triple-A Elementor kit's layout and typography. Header/footer branding and business details are connected to Meta Box Options. Footer navigation is intentionally unchanged. Sponsor/social placeholders and demo page content are not approved business content.

## Existing brand kit

`design-system/` contains the earlier complete brand design kit: HTML reference, CSS/JSON tokens, component specimens, templates, fonts, images and PDFs. `brand/vector-logo-kit/` contains logo variants. `deliverables/` contains shareable PDFs and other exports. The oversized complete-kit ZIP is omitted from Git; its unpacked files are included.

The earlier brand kit uses Archivo Black / Space Grotesk, while the current imported website uses Chakra Petch / Hind. Treat these as distinct sources when preparing a kit. Do not silently present the older static website preview as the current WordPress design.

For a website kit, extract foundations and reusable components from the active Elementor kit and template snapshot, retaining the supplied RWC logo. Document any proposed reconciliation with the brand kit separately. Preserve existing content unless a content change is explicitly requested.
