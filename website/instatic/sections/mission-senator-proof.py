import sys; sys.path.insert(0,'/private/tmp')
from rwcmcp import call

IMG = '/uploads/HCPXYn-uTlAJD67zAku3Y-senator-jim-banks-letter-red-white-and-clix.png'
ALT = ('Letter on United States Senate letterhead from Senator Jim Banks of Indiana, commending '
       'Wesley Robertson for raising funds and awareness for veteran-focused charities through '
       'tabletop gaming.')

CSS = """
.rwc-proof { background: var(--rwc-surface); max-width: none; margin: 0; padding: var(--space-3xl) var(--space-l); font-family: var(--font-rwc-font-body); }
.rwc-proof-inner { max-width: 68rem; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fit, minmax(20rem, 1fr)); gap: var(--space-2xl); align-items: start; }
.rwc-proof-copy { min-width: 0; }
.rwc-proof-eyebrow { font-size: var(--text-xs); letter-spacing: 0.18em; font-weight: 700; color: var(--rwc-action); margin: 0 0 var(--space-m); }
.rwc-proof-quote { font-family: var(--font-rwc-font-heading); font-size: var(--text-2xl); line-height: 1.15; letter-spacing: -0.025em; color: var(--rwc-ink); margin: 0 0 var(--space-m); }
.rwc-proof-sub { font-size: var(--text-s); line-height: 1.7; color: var(--rwc-ink); margin: 0 0 var(--space-m); }
.rwc-proof-cite { font-size: var(--text-xs); letter-spacing: 0.12em; font-weight: 700; text-transform: uppercase; color: var(--rwc-ink); margin: 0 0 var(--space-xl); opacity: 0.8; }
.rwc-proof-listhead { font-size: var(--text-xs); letter-spacing: 0.18em; font-weight: 700; color: var(--rwc-action); margin: 0 0 var(--space-s); }
.rwc-proof-list { list-style: none; margin: 0; padding: 0; display: grid; gap: var(--space-2xs); }
.rwc-proof-item { font-size: var(--text-s); line-height: 1.6; color: var(--rwc-ink); padding-left: var(--space-s); border-left: 2px solid var(--rwc-border); }
.rwc-proof-note { font-size: var(--text-xs); line-height: 1.6; color: var(--rwc-ink); margin: var(--space-m) 0 0; opacity: 0.75; }
.rwc-proof-figure { margin: 0; min-width: 0; }
.rwc-proof-link { display: block; border-radius: 10px; }
.rwc-proof-img { display: block; width: 100%; height: auto; border-radius: 10px; border: 1px solid var(--rwc-border); box-shadow: 0 18px 40px rgba(17,24,39,0.16); }
.rwc-proof-cap { font-size: var(--text-xs); line-height: 1.6; color: var(--rwc-ink); margin: var(--space-s) 0 0; opacity: 0.75; }
"""

SEC = (
 '<section class="rwc-proof"><div class="rwc-proof-inner">'
 '<div class="rwc-proof-copy">'
   '<p class="rwc-proof-eyebrow">ON THE RECORD</p>'
   '<blockquote class="rwc-proof-quote">&ldquo;Stories like yours reflect the very best of '
   'Indiana.&rdquo;</blockquote>'
   '<p class="rwc-proof-sub">&ldquo;I write to commend you for your work raising funds and '
   'awareness for veteran-focused charities. Through your efforts, you have not only supported '
   'veterans in need but also brought people together in your community through tabletop '
   'gaming.&rdquo;</p>'
   '<p class="rwc-proof-cite">Senator Jim Banks &middot; United States Senator for Indiana</p>'
   '<p class="rwc-proof-listhead">ALSO ON THE RECORD</p>'
   '<ul class="rwc-proof-list">'
     '<li class="rwc-proof-item">IRS-recognized 501(c)(3) nonprofit</li>'
     '<li class="rwc-proof-item">EIN 41-4723161</li>'
     '<li class="rwc-proof-item">Registered on SAM.gov</li>'
     '<li class="rwc-proof-item">Veteran-led and board-governed</li>'
   '</ul>'
   '<p class="rwc-proof-note">Contributions are tax deductible to the extent allowed by law. We '
   'do not give tax advice &mdash; ask us and we will tell you what we can substantiate.</p>'
 '</div>'
 '<figure class="rwc-proof-figure">'
   f'<a class="rwc-proof-link" href="{IMG}" target="_blank" rel="noopener">'
   f'<img class="rwc-proof-img" src="{IMG}" alt="{ALT}" width="1086" height="1448" '
   'loading="lazy" decoding="async"></a>'
   '<figcaption class="rwc-proof-cap">The letter as received, February 2026. The recipient&rsquo;s '
   'home address has been removed for privacy. Senator Banks commends the work; he does not '
   'endorse the organization or its fundraising.</figcaption>'
 '</figure>'
 '</div></section>')

print('css ->', call('site_apply_css', {'operation':'merge','css':CSS}))
call('site_open_document', {'document':{'type':'page','id':'wv6irIfvw0sfX_YBf1hrJ'}})
# replace the old credibility section with this one
print('del cred ->', call('site_delete_node', {'nodeId':'daFGJFstjCyNzchofToH7'}))
print('ins proof ->', call('site_insert_html', {'parentId':'9vinTfiASnVgSzRGcYceR','index':5,'html':SEC}).get('nodeIds'))
