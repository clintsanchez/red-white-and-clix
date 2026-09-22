# Global business settings

Updated September 22, 2026 through Novamira MCP.

Edit the business information in WordPress **Options → Global Settings**:
`https://red-white-and-clicks.local/wp-admin/admin.php?page=options`

Reused the existing Meta Box Options page (29), Global Settings field group (25, `group_6654c9fcd58a3`), and `options` option array. No duplicate settings page or custom runtime plugin was added.

| Admin field | Existing/new key | Value/use |
| --- | --- | --- |
| Company Name | `s` (existing) | Red White and Clix; footer copyright |
| Logo | `logo` (existing) | Attachment 1491; both header/footer logos |
| Founder / Contact | `ceo` (existing key, relabeled) | Wesley Robertson |
| Email | `email` (existing) | Footer display and mailto link |
| Phone Number | `phone_address` (existing) | Footer display and tel link |
| Business Description | `business_description` | Footer organization paragraph |
| Home Base / Service Area | `home_base` | Lafayette, Indiana / Midwest footer text |
| Website URL | `website_url` | Confirmed production website; available for future bindings |
| Facebook URL | `facebook_url` | Confirmed Facebook profile; available for future bindings |
| Newsletter Introduction | `newsletter_intro` | Footer newsletter paragraph |

Values come from `00-Client-Brief.md` and the approved header/footer copy. Existing license, white-logo, address, GBP-address, and map fields were retained without inventing values. The home base is stored separately from a street address.

## Elementor bindings

Existing Header 1304 and Footer 1273 use native `meta-box-settings-image`, `meta-box-settings-text`, and `meta-box-settings-url` dynamic tags with keys such as `options:logo` and `options:email`. Contact repeater rows use dynamic text and URLs; the mailto/tel prefixes are composed with the dynamic field values. Copyright derives the company name from `options:s`; its year is currently 2026.

The connector rejects dynamic tags on the legacy logo media-preview control (and previously rejected legacy wysiwyg controls), so native Elementor document saves were used for these bindings and the nested contact repeater. Styling, template structure and display conditions were preserved. Footer navigation and social destinations were not changed. These bindings cover the header/footer; original demo content elsewhere remains separate.

## Verification and recovery

A render test temporarily overrode options in memory, without saving test values. All nine checks passed: both logos, company name, email text/link, phone link, location, business description, and newsletter text. Saved options remained unchanged. Evidence: `website/wordpress-header-footer/review/options-binding-verification.json`.

Browser checks at 1440 and 390 px: HTTP 200, correct actual logo, no horizontal overflow, mobile menu expands.

Before-change backup:
`/Users/clintsanchez/Local Sites/red-white-and-clicks/conf/backups/global-options-20260922-205824.json`
