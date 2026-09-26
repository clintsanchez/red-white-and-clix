import sys; sys.path.insert(0,'/private/tmp')
from rwcmcp import call

PID='a76QQn3JaVtQCVpXY5XkQ'; ROOT='HIebrjShW0QLQzPnWQkyg'

CSS = """
.rwc-fdr { background: var(--rwc-surface); max-width: none; margin: 0; padding: var(--space-3xl) var(--space-l); font-family: var(--font-rwc-font-body); }
.rwc-fdr-inner { max-width: 44rem; margin: 0 auto; }
.rwc-fdr-eyebrow { font-size: var(--text-xs); letter-spacing: 0.18em; font-weight: 700; color: var(--rwc-action); margin: 0 0 var(--space-s); }
.rwc-fdr-title { font-family: var(--font-rwc-font-heading); font-size: var(--text-3xl); line-height: 1.05; letter-spacing: -0.03em; color: var(--rwc-ink); margin: 0 0 var(--space-m); }
.rwc-fdr-lede { font-size: var(--text-m); line-height: 1.6; color: var(--rwc-ink); margin: 0 0 var(--space-xl); }
.rwc-fdr-h2 { font-family: var(--font-rwc-font-heading); font-size: var(--text-xl); line-height: 1.15; letter-spacing: -0.02em; color: var(--rwc-ink); margin: var(--space-2xl) 0 var(--space-s); }
.rwc-fdr-p { font-size: var(--text-s); line-height: 1.75; color: var(--rwc-ink); margin: 0 0 var(--space-m); }
.rwc-fdr-pull { font-family: var(--font-rwc-font-heading); font-size: var(--text-l); line-height: 1.3; color: var(--rwc-ink); margin: var(--space-xl) 0; padding-left: var(--space-m); border-left: 3px solid var(--rwc-logo-red); }
.rwc-fdr-crisis { background: var(--rwc-ink); border-radius: 14px; padding: var(--space-l); margin: var(--space-xl) 0; }
.rwc-fdr-crisis-title { font-family: var(--font-rwc-font-heading); font-size: var(--text-m); line-height: 1.2; color: var(--rwc-white); margin: 0 0 var(--space-s); }
.rwc-fdr-crisis-text { font-size: var(--text-s); line-height: 1.7; color: var(--rwc-white); margin: 0; }
.rwc-fdr-crisis-link { color: var(--rwc-white); font-weight: 700; border-bottom: 2px solid var(--rwc-logo-red); text-decoration: none; }
.rwc-fdr-cta { display: inline-block; font-size: var(--text-s); font-weight: 700; color: var(--rwc-ink); text-decoration: none; padding-bottom: 4px; border-bottom: 2px solid var(--rwc-logo-red); min-height: 44px; margin-top: var(--space-m); }
"""

def p(t): return f'<p class="rwc-fdr-p">{t}</p>'
def h2(t): return f'<h2 class="rwc-fdr-h2">{t}</h2>'

CRISIS = ('<aside class="rwc-fdr-crisis">'
 '<p class="rwc-fdr-crisis-title">If any of this is close to home right now</p>'
 '<p class="rwc-fdr-crisis-text">The Veterans Crisis Line is free, confidential and open 24 hours '
 'a day. Dial <a class="rwc-fdr-crisis-link" href="tel:988">988 then press 1</a>, text '
 '<a class="rwc-fdr-crisis-link" href="sms:838255">838255</a>, or '
 '<a class="rwc-fdr-crisis-link" href="https://www.veteranscrisisline.net/get-help-now/chat/" '
 'target="_blank" rel="noopener">chat online</a>. If there is immediate danger to life, call 911. '
 'We run gaming events. We are not a crisis service and nobody monitors this website for '
 'emergencies.</p></aside>')

BODY = (
 '<section class="rwc-fdr"><div class="rwc-fdr-inner">'
 '<p class="rwc-fdr-eyebrow">FOUNDER&rsquo;S STORY</p>'
 '<h1 class="rwc-fdr-title">Wesley Robertson</h1>'
 '<p class="rwc-fdr-lede">Red, White, and Clix exists because one veteran came home, found the '
 'war had followed him, and was handed a way back by people who did not know him.</p>'

 + h2('Mosul, 2004')
 + p('Wesley Robertson served as a Combat Engineer in the Indiana Army National Guard from 1999 '
     'to 2006. In 2004 he deployed to Mosul, Iraq, operating out of Forward Operating Base Marez '
     'in support of Explosive Ordnance Disposal operations. The work put him close to the daily '
     'realities of that war, where the risks were constant and the stakes were measured in lives.')

 + h2('The part that came home with him')
 + p('The challenges did not end when the deployment did. Over time he was diagnosed with severe '
     'Post-Traumatic Stress Disorder, and later with Primary Progressive Multiple Sclerosis. Those '
     'diagnoses changed the shape of his life, his health, his career and his sense of stability.')
 + p('Harder still, several of the people he served with did not survive the years after coming '
     'home. Watching brothers-in-arms lose that fight left a mark, and with it a sense of '
     'responsibility to do something. The realisation that the war continued long after the '
     'battlefield became the turning point.')
 + CRISIS

 + h2('Somebody showed up')
 + p('During one of the worst stretches of his life, Wesley received help from a veteran-focused '
     'charity. It was practical support, but it was also proof that somebody had bothered &mdash; '
     'that he was not doing this alone. He has been open since about how much that mattered, and '
     'about the fact that it came from strangers.')
 + '<p class="rwc-fdr-pull">Motivated by both loss and gratitude, he built the thing he wished had '
   'found him sooner.</p>'

 + h2('Why a gaming event')
 + p('Because it works. A tournament hall is one of the few places where people who would never '
     'otherwise meet end up sitting across a table for six hours, talking. No clipboard, no '
     'intake form, no having to announce that you are struggling. Just a game, and the '
     'conversation that happens around it.')
 + p('That is the whole design. Create somewhere connection happens naturally, conversations come '
     'easier, and support can be raised in a way that feels human rather than clinical.')

 + h2('Where it has got to')
 + p('Two events in, the model has held up. The first raised $15,000, of which $4,000 went '
     'directly to veteran-focused causes once the venue, prizes and catering were paid for. The '
     'second year funded a new equestrian therapy facility that is open and free to veterans and '
     'first responders. This year the beneficiary is the Mary T. Klinker Veteran Resource Center.')
 + p('Red, White, and Clix is now an IRS-recognized 501(c)(3), and Wesley is still the one setting '
     'out the tables.')
 + '<a class="rwc-fdr-cta" href="/mission" target="_self">Read the mission</a>'
 + '</div></section>')

print('css  ->', call('site_apply_css', {'operation':'merge','css':CSS}))
call('site_open_document', {'document':{'type':'page','id':PID}})
r = call('site_insert_html', {'parentId':ROOT,'index':0,'html':BODY})
print('body ->', r.get('nodeIds') or r)
