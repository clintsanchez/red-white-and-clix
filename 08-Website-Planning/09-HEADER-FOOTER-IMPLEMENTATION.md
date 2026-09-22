# Header and footer — September 22, 2026

Updated the existing Elementor Header (1304) and Footer (1273) through the Novamira MCP connection. Both retain their entire-site display conditions. Interpreted the user's request as retaining the current design and navigation for this pass.

## Changes

- Uploaded the supplied original `brand/red-white-and-clix-logo.png` as media attachment 1491, with descriptive alt text.
- Assigned that image directly to the two header/footer logo widgets. The global kit logo and other page widgets were not changed.
- Set responsive logo widths: header 110 / 86 / 72 px for desktop / tablet / mobile; footer 160 / 144 / 144 px. Preserved image proportions.
- Replaced footer placeholder paragraphs with organization and newsletter copy based on `00-Client-Brief.md`.
- Replaced demo contact details with the confirmed email and phone; described Lafayette, Indiana as the home base rather than an office street address. Email and phone now have mailto/tel links.
- Updated copyright to 2026 Red White and Clix.
- Removed imported negative bottom margins on the organization and newsletter paragraphs to prevent text overlap. Added wrapping to the contact list so the full email address fits on mobile.

## Preserved / pending

The kit typography, colors, section structure, menu destinations and labels, sponsor logo placeholders, and social icon placeholders remain. Newsletter wording is updated, but its existing form actions were not changed and no subscription or email was submitted. A mailing-list integration is not verified by this work. Navigation, actual sponsor assets, social destinations, and legal page links need a subsequent content pass.

## Recovery and review

Before-change backup outside the public web root:
`/Users/clintsanchez/Local Sites/red-white-and-clicks/conf/backups/header-footer-20260922-205011.json`

Desktop (1440 px) and mobile (390 px) screenshots and browser results are in `website/wordpress-header-footer/review/`. Checks cover rendered header/footer, image loading, horizontal overflow, and mobile menu expansion on the Events archive.
