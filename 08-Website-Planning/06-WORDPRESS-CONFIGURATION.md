# Local WordPress configuration

Configured September 22, 2026 through Novamira MCP (`novamira-red-white-and-cl`), using its `novamira/execute-php` ability. Target: https://red-white-and-clicks.local. This authorizes local WordPress setup; production migration and launch remain separate.

## Applied settings

- `blogname`: `Red White and Clix`
- `blogdescription`: `Tabletop gaming in support of veterans.`
- `timezone_string`: `America/Indiana/Indianapolis`
- `date_format`: `F j, Y`
- `time_format`: `g:i a`
- `permalink_structure`: `/%postname%/`
- `blog_public`: `0`
- `users_can_register`: `0`
- `default_role`: `subscriber`
- `default_comment_status`: `closed`
- `default_ping_status`: `closed`
- `default_pingback_flag`: `0`
- `page_for_posts`: `0`

Home remains the static front page (1204). Resources is no longer incorrectly assigned as the blog index. Existing page content was preserved. Created empty draft page shells: Events (1250), Donate (1251); neither contains completed layouts or checkout functionality.

Timezone follows the client brief: Lafayette, Indiana, not the agency/Mac timezone.

## Verification and rollback

All settings were read back and verified during the MCP request, with no PHP warnings. Rewrite rules were refreshed. Previous settings and planned changes are saved outside the public web root at:

`/Users/clintsanchez/Local Sites/red-white-and-clicks/conf/backups/novamira-core-settings-20260922-143154.json`

## Remaining implementation

Build the pages using the selected editing approach and existing brand kit. Review generic blueprint pages, empty privacy policy, navigation, organization SEO, brand logo/icon, forms, and checkout details before launch. Keep search indexing discouraged while this local build is in development; revisit at production launch. No production website changes were made.
