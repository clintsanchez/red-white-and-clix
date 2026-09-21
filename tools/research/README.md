# Research scripts

Client-scoped capture scripts used on September 21, 2026; retain as an implementation record. Paths are explicit to this client. They are not a generalized production crawler.

- `collect_site.py`: sitemap pages, source image URLs, dimensions and SHA-256. Initial input sitemap was saved in `/private/tmp/rwc-onboarding/`; restore it from `99-Reference/site-snapshot/sitemap.xml` before rerunning.
- `browser_research.py`: public-page evidence capture in a fresh Playwright context.
- `facebook_public_pull.py`: follows photo links exposed by the public page and saves publicly served image bytes. No browser profile or cookie extraction. Initial fallback snapshot is `99-Reference/facebook.json`; temporary paths should be adjusted before a rerun.

Google/Candid challenges were recorded and not bypassed. Browser-plugin initialization failed with an unsupported `node:process` import, so fresh Python Playwright was used as the user authorized. The first photo run timed out; a second public run saved 18 images. Manifest categories and byte deduplication were added during final review.
