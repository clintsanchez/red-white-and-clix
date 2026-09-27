# GHL dedicated sending domain — send.redwhiteandclix.org

Added 2026-09-27 in GHL sub-account `yNbQAVmIAdetff2yf45O` (Settings → Email
Services → Dedicated Domain And IP). DNS is on Squarespace Domains. All six
records live on the `send.` subdomain; the apex (no MX, `v=spf1 -all`) is
untouched. GHL auto-deletes the domain if unverified by 2026-10-27.

| Type | Host (Squarespace "Host") | Priority | Value |
|---|---|---|---|
| TXT | send | | v=spf1 include:spf.leadconnectorhq.com include:mailgun.org ~all |
| TXT | smtp._domainkey.send | | k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC2IXszbiJ2FeYV/wDDMAUl5lgu6+PghjMEJf86TkXLvOIpo2KjDvBrghfT0/YjNkQbYKtlMqztFzKCD4eEd30bXdZUayECIJxLFCImsmfR/xbROwpn2EEcvRNBdFdGCis3YVaCAfvPgZVwg7TsowMjGu4UBw5cqeR4T18nbtVBBwIDAQAB |
| CNAME | email.send | | mailgun.org |
| MX | send | 10 | mxa.mailgun.org |
| MX | send | 10 | mxb.mailgun.org |
| TXT | _dmarc.send | | v=DMARC1;p=none; |

Do not fill GHL's Reply Address (it pulls replies out of Conversations); use
Forward to assigned user. Set the Dedicated Header From address on the root
domain (e.g. hello@redwhiteandclix.org), never the gmail.com address.

## Applied 2026-09-27

All six records added in Squarespace Domains (one SMS 2FA code from Wesley's
phone covered the whole session) and confirmed at ns-cloud-a1.googledomains.com
and 8.8.8.8. GHL verification passed the same day: status Active, SSL issued,
warm-up Stage 1 (1,000/day). Dedicated header set to
"Red, White, and Clix <hello@redwhiteandclix.org>"; the business_email custom
value that workflows use as From was changed to the same address.

**Side effect, repaired:** adding the MX records made Squarespace silently drop
its "Email Security" preset, which held the apex `v=spf1 -all` (and, per
earlier notes, a DMARC/DKIM pair whose exact values were never recorded and
were not in any resolver cache). Restored as custom records:

| Type | Host | Value |
|---|---|---|
| TXT | @ | v=spf1 -all |
| TXT | _dmarc | v=DMARC1; p=none; |

`-all` stays correct because mail leaves via send.; DMARC at the apex is
required by Gmail/Yahoo for the hello@ From address. Tighten to
`p=quarantine` once a few weeks of aggregate reports show DKIM passing.
