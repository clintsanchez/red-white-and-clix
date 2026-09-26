import sys; sys.path.insert(0,'/private/tmp')
from rwcmcp import call

CSS = """
.rwc-ms2 { background: var(--rwc-surface); max-width: none; margin: 0; padding: var(--space-3xl) var(--space-l); font-family: var(--font-rwc-font-body); }
.rwc-ms2-inner { max-width: 66rem; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fit, minmax(20rem, 1fr)); gap: var(--space-xl); }
.rwc-ms2-block { min-width: 0; }
.rwc-ms2-eyebrow { font-size: var(--text-xs); letter-spacing: 0.18em; font-weight: 700; color: var(--rwc-action); margin: 0 0 var(--space-s); }
.rwc-ms2-text { font-size: var(--text-m); line-height: 1.55; color: var(--rwc-ink); margin: 0; }
.rwc-trk { background: var(--rwc-ink); max-width: none; margin: 0; padding: var(--space-3xl) var(--space-l); font-family: var(--font-rwc-font-body); }
.rwc-trk-inner { max-width: 66rem; margin: 0 auto; }
.rwc-trk-eyebrow { font-size: var(--text-xs); letter-spacing: 0.18em; font-weight: 700; color: var(--rwc-white); margin: 0 0 var(--space-s); }
.rwc-trk-title { font-family: var(--font-rwc-font-heading); font-size: var(--text-2xl); line-height: 1.1; letter-spacing: -0.025em; color: var(--rwc-white); margin: 0 0 var(--space-l); }
.rwc-trk-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(17rem, 1fr)); gap: var(--space-l); }
.rwc-trk-card { min-width: 0; padding: var(--space-l); border-left: 3px solid var(--rwc-logo-red); background: var(--rwc-white-5); border-radius: 14px; }
.rwc-trk-year { font-size: var(--text-xs); letter-spacing: 0.18em; font-weight: 700; color: var(--rwc-white-70); margin: 0 0 var(--space-2xs); }
.rwc-trk-fig { font-family: var(--font-rwc-font-heading); font-size: var(--text-xl); line-height: 1.1; color: var(--rwc-white); margin: 0 0 var(--space-s); }
.rwc-trk-text { font-size: var(--text-s); line-height: 1.65; color: var(--rwc-white); margin: 0; }
.rwc-trk-now { font-size: var(--text-s); line-height: 1.65; color: var(--rwc-white); margin: var(--space-l) 0 0; max-width: 44rem; }
.rwc-cred { background: var(--rwc-surface); max-width: none; margin: 0; padding: var(--space-2xl) var(--space-l); font-family: var(--font-rwc-font-body); }
.rwc-cred-inner { max-width: 66rem; margin: 0 auto; }
.rwc-cred-eyebrow { font-size: var(--text-xs); letter-spacing: 0.18em; font-weight: 700; color: var(--rwc-action); margin: 0 0 var(--space-m); }
.rwc-cred-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr)); gap: var(--space-m); list-style: none; margin: 0; padding: 0; }
.rwc-cred-item { font-size: var(--text-s); line-height: 1.5; color: var(--rwc-ink); padding-left: var(--space-m); border-left: 2px solid var(--rwc-border); }
.rwc-cred-note { font-size: var(--text-xs); line-height: 1.6; color: var(--rwc-ink); margin: var(--space-m) 0 0; opacity: 0.75; }
"""

VISION = ('A world where veterans and the communities around them are connected through shared '
 'experiences, inclusive engagement, and meaningful support, ensuring veterans are seen, valued, '
 'and never isolated or forgotten.')
MISSION = ('Red White and Clix bridges veterans and their communities through open and inclusive '
 'tabletop gaming events that create meaningful connection, raise awareness of veteran needs, and '
 'generate community-supported funding for veteran-focused causes through shared experiences and fun.')

SEC_A = (
 '<section class="rwc-ms2"><div class="rwc-ms2-inner">'
 '<div class="rwc-ms2-block"><p class="rwc-ms2-eyebrow">OUR VISION</p>'
 f'<p class="rwc-ms2-text">{VISION}</p></div>'
 '<div class="rwc-ms2-block"><p class="rwc-ms2-eyebrow">OUR MISSION</p>'
 f'<p class="rwc-ms2-text">{MISSION}</p></div>'
 '</div></section>')

SEC_B = (
 '<section class="rwc-trk"><div class="rwc-trk-inner">'
 '<p class="rwc-trk-eyebrow">WHAT THE MONEY HAS DONE</p>'
 '<h2 class="rwc-trk-title">Two years, two causes, counted honestly.</h2>'
 '<div class="rwc-trk-grid">'
 '<div class="rwc-trk-card"><p class="rwc-trk-year">YEAR ONE</p>'
 '<p class="rwc-trk-fig">$15,000 raised &middot; $4,000 donated</p>'
 '<p class="rwc-trk-text">Our first event raised $15,000. After the venue, prizes and catering '
 'were paid for, $4,000 went directly to veteran-focused causes. Closing that gap is exactly why '
 'we chase sponsorship so hard &mdash; every sponsored table means more of what you give reaches '
 'the cause. The organisations we funded report that money was instrumental in reaching 28 '
 'veterans in crisis.</p></div>'
 '<div class="rwc-trk-card"><p class="rwc-trk-year">YEAR TWO</p>'
 '<p class="rwc-trk-fig">An equestrian therapy facility</p>'
 '<p class="rwc-trk-text">The second year&rsquo;s fundraising went to a new equestrian therapy '
 'facility, which is open and free to use for veterans and first responders.</p></div>'
 '</div>'
 '<p class="rwc-trk-now">This year we are raising funds to support the Mary T. Klinker Veteran '
 'Resource Center in Lafayette, Indiana. We will publish what the weekend raised and what was '
 'donated, the same way we have here.</p>'
 '</div></section>')

SEC_C = (
 '<section class="rwc-cred"><div class="rwc-cred-inner">'
 '<p class="rwc-cred-eyebrow">ON THE RECORD</p>'
 '<ul class="rwc-cred-list">'
 '<li class="rwc-cred-item">IRS-recognized 501(c)(3) nonprofit</li>'
 '<li class="rwc-cred-item">EIN 41-4723161</li>'
 '<li class="rwc-cred-item">Registered on SAM.gov</li>'
 '<li class="rwc-cred-item">Veteran-led and board-governed</li>'
 '<li class="rwc-cred-item">Recognized for community impact by U.S. Senator Jim Banks</li>'
 '</ul>'
 '<p class="rwc-cred-note">Contributions are tax deductible to the extent allowed by law. We do '
 'not give tax advice &mdash; ask us and we will tell you what we can substantiate.</p>'
 '</div></section>')

print('css  ->', call('site_apply_css', {'operation':'merge','css':CSS}))
call('site_open_document', {'document':{'type':'page','id':'wv6irIfvw0sfX_YBf1hrJ'}})
ROOT='9vinTfiASnVgSzRGcYceR'
print('A ->', call('site_insert_html', {'parentId':ROOT,'index':2,'html':SEC_A})['nodeIds'])
print('B ->', call('site_insert_html', {'parentId':ROOT,'index':4,'html':SEC_B})['nodeIds'])
print('C ->', call('site_insert_html', {'parentId':ROOT,'index':5,'html':SEC_C})['nodeIds'])
