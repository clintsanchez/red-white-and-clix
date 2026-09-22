from pathlib import Path
import json, shutil, base64, html, re, math, hashlib, csv
K=Path(__file__).resolve().parents[1]
R=K.parent
CLIENT=Path('/Users/clintsanchez/pCloud Drive/Documents/BlakSheep Creative/Clients/Red White and Clix')
def put(p,s):
 p=K/p; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(s)
def js(p,o): put(p,json.dumps(o,indent=2,ensure_ascii=False))
def esc(s): return html.escape(str(s),quote=True)
def datauri(p): return 'data:'+('image/png' if str(p).endswith('.png') else 'image/jpeg')+';base64,'+base64.b64encode(Path(p).read_bytes()).decode()
for d in ['assets/logos','assets/icons','assets/photography','assets/references','tokens','components','templates/social','templates/charts','templates/print','templates/slides','guidelines','exports','tools']:(K/d).mkdir(parents=True,exist_ok=True)
shutil.copy2(R/'brand/red-white-and-clix-logo.png',K/'assets/logos/red-white-and-clix-logo.png')
photos=CLIENT/'05-Photos/selected-event-photos'
for p in photos.glob('*'):
 if p.is_file(): shutil.copy2(p,K/'assets/photography'/p.name)
for p in (R/'brand').glob('*.md'): shutil.copy2(p,K/'guidelines'/p.name)
for p in (R/'07-Design-Prompts').glob('*.md'): shutil.copy2(p,K/'assets/references'/p.name)
shutil.copy2(R/'CLIENT-FOLLOWUP.md',K/'guidelines/confirmation-register.md')
logo=datauri(K/'assets/logos/red-white-and-clix-logo.png')
fonts=''
for family,name,weight in [('Archivo Black','ArchivoBlack-Regular.ttf','400')]+[('Space Grotesk',f'SpaceGrotesk-{w}.ttf',str(w)) for w in [400,500,600,700]]:
 b=base64.b64encode((K/'assets/fonts'/name).read_bytes()).decode()
 fonts+=f'@font-face{{font-family:"{family}";src:url(data:font/ttf;base64,{b}) format("truetype");font-weight:{weight};font-style:normal;font-display:block;}}'
put('tokens/fonts.css','\n'.join(f'@font-face{{font-family:"{f}";src:url("../assets/fonts/{n}") format("truetype");font-weight:{w};font-display:swap;}}' for f,n,w in [('Archivo Black','ArchivoBlack-Regular.ttf','400')]+[('Space Grotesk',f'SpaceGrotesk-{w}.ttf',str(w)) for w in [400,500,600,700]]))
colors={'logo-red':'#FF0000','logo-blue':'#0072FF','white':'#FFFFFF','black':'#000000','action':'#B91C1C','link':'#0050B3','ink':'#111827','surface':'#F5F7FA','border':'#D1D5DB'}
alias={'text-primary':'ink','text-secondary':'ink','surface-primary':'white','surface-secondary':'surface','surface-inverse':'ink','text-inverse':'white','border-control':'ink','status-success':'link','status-info':'link','status-warning':'ink','status-error':'action','data-primary':'link','data-secondary':'action','data-tertiary':'ink','data-neutral':'border','focus':'link','action-hover':'ink','action-pressed':'black'}
vals={**colors,**{a:f'var(--rwc-{v})' for a,v in alias.items()}}
typevals={'font-heading':'"Archivo Black", Arial, sans-serif','font-body':'"Space Grotesk", Arial, sans-serif','body-size':'18px','body-leading':'1.6','h1':'clamp(36px,5vw,72px)','h2':'clamp(28px,4vw,48px)','h3':'24px','label':'16px','caption':'14px','display-leading':'1.08','heading-tracking':'-0.025em'}
spacevals={**{f'space-{n//4}':f'{n}px' for n in [4,8,12,16,24,32,48,64,96]},'content-width':'1200px','reading-width':'70ch','gutter':'32px','gutter-mobile':'16px','section':'64px','target':'44px'}
effectvals={'radius':'8px','radius-button':'8px','radius-card':'8px','radius-input':'8px','radius-modal':'8px','radius-pill':'999px','shadow-sm':'0 2px 8px rgb(17 24 39 / 8%)','shadow-md':'0 8px 24px rgb(17 24 39 / 12%)','shadow-lg':'0 16px 48px rgb(17 24 39 / 16%)','duration-fast':'120ms','duration':'180ms','ease':'cubic-bezier(.2,0,0,1)','focus-ring':'0 0 0 2px #FFFFFF, 0 0 0 5px #0050B3'}
socialvals={'social-margin':'64px','social-gutter':'32px','social-headline':'72px','social-body':'32px','social-caption':'24px','social-story-top':'250px','social-story-bottom':'320px','social-story-right':'160px'}
groups={'colors':vals,'typography':typevals,'spacing':spacevals,'effects':effectvals,'social':socialvals}
for name,v in groups.items():put(f'tokens/{name}.css',':root {\n'+''.join(f'  --rwc-{k}: {x};\n' for k,x in v.items())+'}\n')
flat={k:v for a in groups.values() for k,v in a.items()}
js('tokens/tokens.json',{'name':'Red White and Clix','version':'1.0.0','status':'Working design extension; original logo preserved; UI and creative direction proposed','tokens':flat,'assets':{'logo':'assets/logos/red-white-and-clix-logo.png'},'source':'Existing project DESIGN.md, brand-style-guide.md and RWC design briefs'})
dtcg={}
for group,v in groups.items():
 dtcg[group]={}
 for key,value in v.items():
  if value.startswith('#'):
   typ='color'; value={'colorSpace':'srgb','components':[int(value[i:i+2],16)/255 for i in [1,3,5]],'alpha':1,'hex':value}
  elif re.fullmatch(r'[0-9]+px',value):typ='dimension';value={'value':int(value[:-2]),'unit':'px'}
  elif value.startswith('var('):typ='color';value='{colors.'+value[10:-1]+'}'
  else:typ='string'
  dtcg[group][key]={'$type':typ,'$value':value}
js('tokens/design-tokens.dtcg.json',dtcg)
put('tokens/base.css','*{box-sizing:border-box}body{margin:0;color:var(--rwc-ink);background:var(--rwc-surface);font:var(--rwc-body-size)/var(--rwc-body-leading) var(--rwc-font-body)}h1,h2{font-family:var(--rwc-font-heading);font-weight:400;line-height:var(--rwc-display-leading);letter-spacing:var(--rwc-heading-tracking)}h3{font-size:var(--rwc-h3)}a{color:var(--rwc-link);text-underline-offset:3px}button,input,select,textarea{font:inherit}img,svg{max-width:100%}button,a,input,select,textarea,summary{touch-action:manipulation}:focus-visible{outline:3px solid var(--rwc-focus);outline-offset:3px;box-shadow:0 0 0 2px white}@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}}')
put('styles.css','\n'.join(f'@import url("tokens/{x}.css");' for x in ['fonts','colors','typography','spacing','effects','social','base'])+'\n@import url("components/components.css");')
put('components/components.css','''
.rwc-btn{display:inline-flex;justify-content:center;align-items:center;gap:8px;min-height:44px;padding:10px 20px;border:2px solid transparent;border-radius:var(--rwc-radius-button);background:var(--rwc-action);color:white;font:700 16px/1.3 var(--rwc-font-body);text-decoration:none;cursor:pointer;transition:background var(--rwc-duration) var(--rwc-ease)}.rwc-btn:hover{background:var(--rwc-action-hover)}.rwc-btn:active{background:var(--rwc-action-pressed)}.rwc-btn.secondary{background:white;border-color:var(--rwc-link);color:var(--rwc-link)}.rwc-btn.secondary:hover{background:var(--rwc-surface)}.rwc-btn:disabled{background:var(--rwc-surface);color:var(--rwc-ink);border-color:var(--rwc-border);cursor:not-allowed}.rwc-card{background:white;border:1px solid var(--rwc-border);border-radius:var(--rwc-radius-card);padding:24px}.rwc-card h3{margin:0 0 12px;font-size:24px;line-height:1.2}.rwc-card p{margin:10px 0}.rwc-meta{font-size:14px;line-height:1.5}.rwc-badge{display:inline-flex;align-items:center;gap:6px;background:var(--rwc-surface);border:1px solid var(--rwc-border);padding:5px 10px;border-radius:var(--rwc-radius);font-size:14px;font-weight:700}.rwc-badge.blue{background:var(--rwc-link);color:white;border-color:var(--rwc-link)}.rwc-badge.red{background:var(--rwc-action);color:white;border-color:var(--rwc-action)}.rwc-alert{border-left:4px solid var(--rwc-link);padding:16px;background:var(--rwc-surface)}.rwc-alert.error{border-color:var(--rwc-action)}.rwc-alert.warning{border:2px dashed var(--rwc-ink)}.rwc-field{display:grid;gap:6px;font-size:16px}.rwc-field input,.rwc-field select,.rwc-field textarea{width:100%;min-height:44px;border:1px solid var(--rwc-ink);border-radius:8px;padding:10px;background:white}.rwc-field [aria-invalid=true]{border:2px solid var(--rwc-action)}.rwc-field small{font-size:14px}.rwc-error{color:var(--rwc-action)}.rwc-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}.rwc-stack{display:grid;gap:16px}.rwc-row{display:flex;flex-wrap:wrap;align-items:center;gap:12px}.rwc-nav{display:flex;align-items:center;justify-content:space-between;gap:24px;background:var(--rwc-ink);color:white;padding:24px}.rwc-nav a{color:white}.rwc-logo{display:block;width:144px;height:144px;object-fit:contain;background:black;padding:12px}.rwc-cta{background:var(--rwc-ink);color:white;padding:32px;border-left:8px solid var(--rwc-logo-blue)}.rwc-cta h3{margin:0 0 12px}.rwc-stat{font:400 40px/1.2 var(--rwc-font-heading);margin:16px 0}.rwc-photo{width:100%;height:220px;object-fit:cover;border-radius:8px}.rwc-source{font-size:14px;border-top:1px solid var(--rwc-border);padding-top:12px}.rwc-check{display:flex;gap:12px;align-items:center;min-height:44px}.rwc-check input{width:20px;height:20px;accent-color:var(--rwc-link)}.rwc-table{width:100%;border-collapse:collapse;font-size:14px}.rwc-table th,.rwc-table td{text-align:left;padding:12px;border-bottom:1px solid var(--rwc-border)}.rwc-table th{background:var(--rwc-surface)}.rwc-steps{padding-left:24px}.rwc-steps li{padding:8px}.rwc-faq summary{padding:14px 0;cursor:pointer;font-weight:700;min-height:44px}.rwc-faq details{border-bottom:1px solid var(--rwc-border)}.rwc-icon{width:24px;height:24px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}.rwc-skeleton{background:var(--rwc-surface);border:1px dashed var(--rwc-border);padding:24px;text-align:center}.rwc-rating{letter-spacing:3px}.rwc-avatar{width:160px;height:160px;border-radius:50%;background:black;padding:24px}.rwc-progress{height:20px;background:var(--rwc-surface);border:1px dashed var(--rwc-ink)}@media(max-width:640px){.rwc-grid{grid-template-columns:1fr}.rwc-nav{flex-wrap:wrap}.rwc-card{padding:16px}}
''')
icons={'calendar':'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 11h18"/>','pin':'<path d="M20 10c0 6-8 11-8 11S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2"/>','arrow':'<path d="M4 12h16m-6-6 6 6-6 6"/>','check':'<path d="m5 12 4 4L19 6"/>','info':'<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7h.01"/>','people':'<circle cx="9" cy="7" r="3"/><path d="M3 21v-3a6 6 0 0 1 12 0v3M16 4a3 3 0 0 1 0 6m2 5a5 5 0 0 1 3 4v2"/>','mail':'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 6 9 7 9-7"/>','phone':'<path d="M6 3h3l2 5-3 2a12 12 0 0 0 6 6l2-3 5 2v3c0 2-2 3-4 3A18 18 0 0 1 3 7c0-2 1-4 3-4Z"/>','heart':'<path d="M20 5c-3-3-7-1-8 2-1-3-5-5-8-2-5 5 3 11 8 15 5-4 13-10 8-15Z"/>','clock':'<circle cx="12" cy="12" r="9"/><path d="M12 6v6l4 2"/>','download':'<path d="M12 3v12m-5-5 5 5 5-5M4 16v5h16v-5"/>','menu':'<path d="M4 6h16M4 12h16M4 18h16"/>','close':'<path d="m5 5 14 14M19 5 5 19"/>','external':'<path d="M14 3h7v7M21 3 10 14M10 3H3v18h18v-7"/>','document':'<path d="M14 3H5v18h14V8l-5-5Zm0 0v5h5M8 12h8M8 16h8"/>','game':'<rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="8" cy="8" r="1"/><circle cx="16" cy="16" r="1"/><circle cx="12" cy="12" r="1"/>'}
for name,path in icons.items():put(f'assets/icons/{name}.svg',f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><title>{name}</title>{path}</svg>')
def icon(n):return f'<svg class="rwc-icon" viewBox="0 0 24 24" aria-hidden="true">{icons[n]}</svg>'
def btn(t,cls=''):return f'<button type="button" class="rwc-btn {cls}">{esc(t)}</button>'
def badge(t,cls=''):return f'<span class="rwc-badge {cls}">{esc(t)}</span>'
def card(t,b):return f'<article class="rwc-card"><h3>{t}</h3>{b}</article>'
C={}
def comp(n,body,desc):C[n]={'html':body,'description':desc}
comp('Button',f'<div class="rwc-row">{btn("Register")}{btn("View event details","secondary")}<a href="#demo">Read the mission</a><button class="rwc-btn" disabled>Registration unavailable</button></div>','Primary, secondary, text, hover, pressed, focus and disabled. One main action; 44px minimum target.')
comp('Logo',f'<img class="rwc-logo" src="{logo}" alt="Red White and Clix">','Supplied raster artwork; black plate; preserve proportions and 10% clear space. Full artwork itself at least 120px for production.')
comp('Icon','<div class="rwc-row">'+''.join(icon(n) for n in icons)+'</div>','16 original simple line icons. 24px viewBox, 2px stroke; decorative icons hidden from assistive technology.')
comp('Badge','<div class="rwc-row">'+badge('300 Modern','blue')+badge('Team Sealed · 3v3')+badge('Status: confirm')+badge('Sponsor tier: confirm')+'</div>','Format, registration status and sponsor-tier variants. Meaning is written in words.')
comp('EventDetails',card('RWC 300 Modern',f'<p>{icon("calendar")} November 7, 2026</p><p>{icon("pin")} Lafayette National Guard Armory</p><p class="rwc-meta">5218 Haggerty Lane · Lafayette, Indiana</p>{badge("Fee + registration URL: confirm")}{btn("View event details")}'),'Date, venue, format, fee and authoritative action together. Copy is drawn from the September 21 project brief.')
comp('EventDate','<div class="rwc-row">'+badge('NOV 07–08','blue')+'<strong>2026 event weekend</strong></div>','Compact social and UI date block; never infer date from photography.')
comp('RegistrationAction',f'<div class="rwc-stack">{btn("Register for an event")}<span class="rwc-meta">Fee and checkout URL: CONFIRM BEFORE PUBLISHING</span></div>','Link variant in production after checkout route is confirmed. This specimen sends no registration.')
comp('Field','<label class="rwc-field">Email address<input type="email" placeholder="you@example.com" autocomplete="email"><small>We’ll use this to reply to your inquiry.</small></label>','Visible label, email keyboard, autocomplete and helper text.')
comp('FieldError','<label class="rwc-field">Email address<input type="email" value="player" aria-invalid="true" aria-describedby="email-error"><small id="email-error" class="rwc-error">Enter a complete email address, such as you@example.com.</small></label>','Error names the fix and is connected with aria-describedby; no color-only signal.')
comp('Select','<label class="rwc-field">I’m interested in<select><option>Playing</option><option>Sponsoring</option><option>Volunteering</option></select></label>','Native select, keyboard accessible. Options are inquiry categories, not promised services.')
comp('Checkbox','<label class="rwc-check"><input type="checkbox">Send me future event updates.</label>','Optional consent is unchecked by default; connected to a real policy before launch.')
comp('Textarea','<label class="rwc-field">Your question<textarea rows="3" placeholder="What would you like to know?"></textarea></label>','Plain language prompt and generous input area.')
comp('Alert','<div class="rwc-alert"><strong>Event update</strong><p>[Confirmed detail] has changed. Updated [date and time].</p><p>Authoritative link: CONFIRM BEFORE PUBLISHING</p></div>','Calm logistics alert; requires timestamp and authoritative source.')
comp('StatusMessage','<div class="rwc-stack"><div class="rwc-alert">✓ Success: your changes were saved.</div><div class="rwc-alert error">Error: review the highlighted field.</div></div>','Success/info use blue; errors use action red. Icon and text distinguish meaning.')
comp('ProductionWarning','<div class="rwc-alert warning"><strong>CONFIRM BEFORE PUBLISHING</strong><p>Fee, checkout route, beneficiary allocation and sponsor permission.</p></div>','Visible authoring placeholder; replace only after checking the underlying fact.')
comp('Navigation',f'<nav class="rwc-nav" aria-label="Example navigation"><strong>Red White and Clix</strong><a href="#events">Events</a><a href="#mission">Our mission</a><a href="#resources">Resources</a></nav>','Responsive navigation specimen. Final information architecture remains proposed.')
comp('Footer','<footer class="rwc-cta"><strong>Red White and Clix</strong><p>One Community. One Mission.</p><p class="rwc-meta">redwhiteandclix.org · 574-265-9585</p></footer>','Compact, standard and expanded variants; no invented social handles.')
comp('CTABand',f'<section class="rwc-cta"><h3>There’s a seat at the table for you.</h3><p>Competition, camaraderie and a shared purpose.</p>{btn("View the next event")}</section>','Dark band, single red action and a restrained blue edge.')
comp('EventCard',card('A weekend around the table','<p>November 7–8, 2026 · Lafayette, Indiana</p><p>300 Modern + Team Sealed · 3v3</p>'+btn('Explore the event')),'Event summary card with date and place visible before the action.')
comp('Schedule','<ol class="rwc-steps"><li><strong>Saturday, November 7</strong><br>RWC 300 Modern · start time: confirm</li><li><strong>Sunday, November 8</strong><br>Team Sealed · 3v3 · start time: confirm</li></ol>','Chronological timeline; no invented check-in times.')
comp('NewPlayerGuide',card('New to HeroClix?','<ol class="rwc-steps"><li>Check the format.</li><li>Review the event details.</li><li>Bring the required game materials.</li><li>Ask questions and practice good sportsmanship.</li></ol>'),'Helpful steps without promising loaners, coaching or beginner divisions.')
comp('VenueCard',card('Find the event','<p>Lafayette National Guard Armory</p><p>5218 Haggerty Lane<br>Lafayette, Indiana 47905</p><p class="rwc-meta">Event venue. Access and parking details: confirm.</p>'),'Venue is labeled separately from the mailing location.')
comp('BeneficiaryCard',card('[Confirmed beneficiary]','<p>[Approved description of the relationship]</p>'+badge('Relationship + logo permission: confirm')),'Neutral logo slot and relationship statement; no assumed endorsement.')
comp('SponsorGrid','<div class="rwc-grid">'+''.join('<div class="rwc-skeleton">[Approved sponsor logo]<br><small>Permission: confirm</small></div>' for _ in range(2))+'</div>','Equal visual weight within each confirmed tier. Preserve each supplied logo.')
comp('SponsorTier',card('[Confirmed sponsor tier]','<p>[Approved deliverables and availability]</p><p>Price: CONFIRM BEFORE PUBLISHING</p>'+btn('Ask about sponsorship')),'Tier benefits and price remain editable until defined.')
comp('DonationAllocation',card('Know what your gift supports','<table class="rwc-table"><tr><th>Allocation</th><th>Confirmed amount</th></tr><tr><td>Beneficiary</td><td>[Amount]</td></tr><tr><td>Event expenses</td><td>[Amount]</td></tr><tr><td>Program support</td><td>[Amount]</td></tr></table><p class="rwc-source">Source + reporting date: CONFIRM BEFORE PUBLISHING</p>'),'Allocation and transfer totals require records. No implied percentage split.')
comp('DonationFAQ','<section class="rwc-faq"><details open><summary>What does my gift support?</summary><p>[Approved beneficiary and allocation explanation]</p></details><details><summary>How will I receive a receipt?</summary><p>[Confirmed receipt process and contact]</p></details></section>','Native disclosure controls; donation answers need operational confirmation.')
comp('VolunteerCard',card('Help run a table worth returning to','<p>Support logistics, hospitality and the participant experience.</p><p class="rwc-meta">Available roles and dates: confirm.</p>'+btn('Volunteer with RWC')),'Recruitment CTA with clear role and date fields.')
comp('ResourceCard',card('Looking for veteran support?','<p>Find qualified local, state and national organizations in the resource guide.</p>'+btn('View veteran resources','secondary')),'Keep resource information separate from fundraising; verify provider details.')
comp('MerchandiseCard',card('Wear the mission','<div class="rwc-skeleton">[Approved product photography]</div><p>Product, availability, price and store URL: confirm.</p>'+btn('View the official store')),'Product images must be real product assets or labeled mockups.')
comp('Quote','<blockquote class="rwc-card"><h3>“[Approved quote]”</h3><p>[Name] · [Role or event context]</p><p class="rwc-source">Source · Date · Permission: confirm</p></blockquote>','Never fabricate testimony or attribution.')
comp('Review',card('[Approved review]','<p class="rwc-rating">[Verified rating]</p><p>[Exact approved review text]</p><p class="rwc-source">[Platform] · [Date] · [Source URL]</p>'),'Rating appears only if the source supplies it.')
comp('KPI',card('Confirmed registrations','<div class="rwc-stat">[Value]</div><p>[Reporting period]</p><p class="rwc-source">Source: registration records · Updated [date]</p>'),'One, two, three and four metric variants. Empty data stays a placeholder.')
comp('KPIGrid','<div class="rwc-grid">'+card('Attendance','<div class="rwc-stat">[Value]</div>')+card('Funds transferred','<div class="rwc-stat">[Value]</div>')+'</div><p class="rwc-source">Source + date: confirm for each metric.</p>','Responsive metric group with independent source fields.')
comp('Citation','<p class="rwc-source">Source: [Organization] · [Report title] · [Date]<br>[Source URL] · Reporting period: [Period]</p>','Readable evidence line. Required on statistics and researched content.')
comp('PhotoCaption','<p class="rwc-meta">[Event/context] · [Verified date]<br>Photo: [Photographer] · Permission: confirm · Documentary image</p>','Provenance and consent metadata stay attached to assets.')
comp('PhotoGallery','<div class="rwc-grid">'+''.join(f'<figure style="margin:0"><img class="rwc-photo" src="{datauri(p)}" alt="Documentary tabletop community photograph"><figcaption class="rwc-meta">Archive reference · context and permission: confirm</figcaption></figure>' for p in [(K/'assets/photography'/n) for n in ['fb-a773fb13f49d.jpg','fb-b1e412d378a4.jpg']])+'</div>','Authentic photo grid; individual caption and alt text before publication.')
comp('Comparison','<table class="rwc-table"><tr><th>Format</th><th>300 Modern</th><th>Team Sealed</th></tr><tr><td>Day</td><td>Saturday</td><td>Sunday</td></tr><tr><td>Team structure</td><td>Confirm</td><td>3v3</td></tr><tr><td>Fee basis</td><td>Confirm</td><td>Confirm per team</td></tr></table>','Compare the same dimensions; use labels rather than red/blue alone.')
comp('Checklist','<ul class="rwc-steps"><li>Confirm the format and registration route.</li><li>Check date and venue.</li><li>Review required game materials.</li><li>Save the organizer’s contact details.</li></ul>','Checklist supports short, long, process and review variants.')
comp('CarouselFooter','<div class="rwc-row"><strong>Red White and Clix</strong><span>02 / 07</span><span>Next →</span></div>','Persistent page numbering and optional swipe cue; real sequence count.')
comp('ImageContainer','<div class="rwc-grid"><div class="rwc-skeleton">[Framed photo]</div><div class="rwc-skeleton">[Screenshot + caption]</div></div>','Full bleed, framed, rounded, split, portrait, product and screenshot slots; do not invent device or product evidence.')
comp('BrowserFrame','<div class="rwc-card"><div class="rwc-meta">Website preview · redwhiteandclix.org</div><div class="rwc-skeleton">[Actual screenshot]</div></div>','Neutral browser frame for an actual site capture; no fabricated interface proof.')
comp('EmptyState',card('No results to show yet','<p>Add verified records and a reporting date to populate this view.</p>'+btn('Review source records','secondary')),'Honest empty state for unpopulated reporting.')
comp('Progress','<div class="rwc-stack"><strong>Registrations toward goal</strong><div class="rwc-progress" role="img" aria-label="No verified progress value available"></div><span>[Confirmed count] / [Approved goal] · source + date required</span></div>','No fabricated filled portion; determinate state requires numerator and denominator.')
comp('ContactCard',card('Let’s talk about your next step','<p>Wesley Robertson · Red White and Clix</p><p>redwhiteandclix@gmail.com<br>574-265-9585</p>'),'Contact card using client-provided details.')
for i,(name,v) in enumerate(C.items()):
 put(f'components/{name}.html',f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{name} · RWC</title><link rel="stylesheet" href="../styles.css"><body style="padding:32px;max-width:1000px"><main>{v["html"]}</main></body></html>')
js('components/inventory.json',[{'name':n,'path':f'components/{n}.html','description':v['description']} for n,v in C.items()])
# Editable canvas configuration. Defaults from the supplied brief are not represented as live platform guarantees.
formats={'square':(1080,1080),'portrait':(1080,1350),'story':(1080,1920),'landscape':(1200,630),'tall':(1000,1500),'widescreen':(1920,1080),'thumbnail':(1280,720),'wide-banner':(1500,500),'ultrawide':(1584,396),'facebook-cover':(851,315),'facebook-event':(1920,1005),'facebook-group':(1640,856),'linkedin-cover':(1512,256),'linkedin-cover-legacy':(1128,191),'youtube-banner':(2560,1440),'avatar':(800,800)}
spec=[]
for name,(w,h) in formats.items():
 source='Supplied universal and RWC design briefs';status='Editable production default; check platform preview before upload';safe=[64,64,w-128,h-128]
 if name=='story':safe=[64,250,856,1350]
 if name=='youtube-banner':safe=[508,509,1544,422];source='https://support.google.com/youtube/answer/10456525';status='Verified 2026-09-21; central zone conservatively scaled from official minimum-size safe area'
 if name=='linkedin-cover':safe=[320,40,872,160];source='https://www.linkedin.com/help/linkedin/answer/a563309';status='Verified 2026-09-21 dimensions; safe rectangle is a conservative design guide'
 if 'banner' in name or 'cover' in name or name=='ultrawide':
  if name not in ['youtube-banner','linkedin-cover']:safe=[int(w*.23),int(h*.14),int(w*.60),int(h*.65)]
 if name=='avatar':safe=[144,144,512,512]
 spec.append({'id':name,'width':w,'height':h,'ratio':round(w/h,3),'safe_rect_xywh':safe,'status':status,'source':source,'checked':'2026-09-21' if name in ['youtube-banner','linkedin-cover'] else None,'crop':'Keep text inside guide; verify mobile and desktop uploader crops.'})
js('tokens/platform-specifications.json',spec)
platforms={'Instagram':['square','portrait','landscape','story','avatar'],'Facebook':['square','portrait','landscape','story','facebook-cover','facebook-event','facebook-group','avatar'],'LinkedIn':['square','portrait','landscape','linkedin-cover','ultrawide','avatar'],'YouTube':['thumbnail','youtube-banner','avatar','square','portrait','story'],'Google Business Profile':['square','landscape','avatar'],'TikTok':['story','square','widescreen','avatar'],'X':['landscape','portrait','square','wide-banner','avatar'],'Threads':['square','portrait','landscape','avatar'],'Bluesky':['square','portrait','landscape','wide-banner','avatar'],'Pinterest':['tall','square','thumbnail','avatar'],'Snapchat':['story','avatar','wide-banner'],'Reddit':['square','portrait','landscape','ultrawide','avatar'],'Mastodon':['square','portrait','landscape','wide-banner','avatar'],'Email':['landscape','wide-banner']}
js('templates/platform-map.json',{'note':'Shared adaptable masters; platform accounts are not implied. Exact channel-specific upload sizes remain configuration values. LinkedIn legacy brief size is included separately.','platforms':platforms})
F=[]
def fam(id,title,headline,body,cta,kind='statement',fields=None):F.append(dict(id=id,title=title,headline=headline,body=body,cta=cta,kind=kind,fields=fields or []))
fam('mission','Mission statement','One Community. One Mission.','Veteran-founded tabletop events where competition, camaraderie and veteran support share the same table.','Explore the mission')
fam('save-date','Save the date','A weekend around the table.','November 7–8, 2026 · Lafayette National Guard Armory','View event details','event',['NOV 07–08 / 2026','Lafayette, Indiana','300 Modern + Team Sealed'])
fam('modern','300 Modern','Bring your best team.','RWC 300 Modern · Saturday, November 7, 2026','View 300 Modern','event',['Lafayette National Guard Armory','Fee: CONFIRM BEFORE PUBLISHING','Registration URL: CONFIRM'])
fam('team-sealed','Team Sealed','Three players. One team.','Team Sealed · 3v3 · Sunday, November 8, 2026','View Team Sealed','event',['Lafayette National Guard Armory','Fee + per-team basis: CONFIRM','Registration URL: CONFIRM'])
fam('event-update','Event update','Here’s the latest.','[Confirmed change] · Updated [date and time]','View current details','alert',['New detail: CONFIRM','Authoritative link: CONFIRM','Contact: 574-265-9585'])
fam('new-player','New-player welcome','New to HeroClix? Start here.','Review the format, bring your questions and join a community that values helpful competition.','Read the event guide','steps',['Check the format','Review date and venue','Bring required game materials'])
fam('competition','Competition','Serious play. Shared purpose.','Clear formats, fair competition and real camaraderie.','See the event schedule')
fam('community','Veterans and families','Camaraderie starts at a shared table.','Veterans, families, gamers and supporters participate as peers.','Join the community')
fam('donation','Donation appeal','Put purpose behind every table.','Your gift supports Red White and Clix and its veteran-focused mission.','Learn how to give','event',['Beneficiary: CONFIRM','Allocation: CONFIRM','Donation URL: CONFIRM'])
fam('transparency','Donation transparency','Know what your gift supports.','Every allocation and result needs a source and reporting date.','Read the impact report','data',['Beneficiary / [Confirm]','Expenses / [Confirm]','Amount transferred / [Confirm]'])
fam('sponsor','Sponsor recruitment','Stand behind a community that shows up.','Support a veteran-founded tabletop event with defined benefits and documented follow-through.','Become a sponsor','event',['Benefits: CONFIRM','Tier + availability: CONFIRM'])
fam('sponsor-spotlight','Sponsor spotlight','Thank you, [Sponsor].','[Approved description of sponsor support]','Meet our partners','image',['[Approved sponsor logo]','Permission: CONFIRM'])
fam('volunteer','Volunteer recruitment','Help make the gathering possible.','Support check-in, logistics, hospitality and the participant experience.','Volunteer with RWC','steps',['Available roles: CONFIRM','Date and time: CONFIRM','Signup link: CONFIRM'])
fam('beneficiary','Beneficiary spotlight','Meet [Beneficiary].','[Approved description of the organization and relationship]','Learn where support goes','image',['[Approved beneficiary logo]','Relationship + permission: CONFIRM'])
fam('impact','Impact statistic','Participation, documented.','[Reporting period] · Confirm each value before publishing.','Read the impact report','data',['Registrations / [Value]','Volunteers / [Value]','Funds transferred / [Value]'])
fam('results','Post-event results','What we accomplished together.','Thank you to every player, volunteer, sponsor and supporter.','View confirmed results','data',['Attendance / [Value]','Funds raised / [Value]','Beneficiary / [Confirm]'])
fam('founder','Founder story','Veteran-founded. Community-powered.','Wesley Robertson created RWC to connect tabletop camaraderie with veteran support.','Read the RWC story')
fam('resources','Veteran resources','Looking for support? Start here.','Explore qualified local, state and national organizations in the resource guide.','View veteran resources','steps',['Provider name: CONFIRM','Service + eligibility: CONFIRM','Current contact: CONFIRM'])
fam('merchandise','Merchandise','Wear the mission.','Explore current Red White and Clix merchandise through the official store.','View the official store','image',['[Approved product image]','Price + availability + URL: CONFIRM'])
fam('faq','FAQ','What should I know before I go?','[Approved answer to one event question]','Read the event guide','event',['Format / [Confirm details]','Registration / [Confirm route]','Fee / [Confirm amount]'])
fam('quote','Quote and testimonial','“[Approved testimonial]”','[Name] · [Role or event context]','Meet the community','quote',['Source: CONFIRM','Date + permission: CONFIRM'])
fam('countdown','Countdown','[Days] until we gather.','[Current event] · [Date] · [Venue]','View registration details','event',['Registration status: CONFIRM','Authoritative link: CONFIRM'])
fam('weather','Weather or cancellation','A change to the event.','[Confirmed operational update] · [Timestamp]','Read the full update','alert',['Current details: CONFIRM','Next step: CONFIRM','Contact: 574-265-9585'])
fam('photo-recap','Photo recap','Around the tables.','[Event/context] · [Verified date]','View the recap','image',['[Documentary event photograph]','Photo credit + permission: CONFIRM'])
fam('education','Educational checklist','Your next step starts here.','One clear action at a time.','Save the event guide','steps',['Read the current event format','Confirm your registration','Plan your trip','Practice good sportsmanship'])
# Additional universal content structures adapted to this client.
fam('comparison','Comparison','Choose your event format.','Compare the same details before making plans.','Compare event details','comparison',['300 Modern / Saturday','Team Sealed / Sunday','Fee and rules / CONFIRM'])
fam('myth-fact','Myth and fact','Check the details. Skip the guesswork.','[Common misconception] → [Source-supported clarification]','Read the source','comparison',['MYTH / [Claim to check]','FACT / [Verified explanation]'])
fam('case-study','Case study','From the table to the mission.','[Documented challenge, action and outcome]','Read the full story','steps',['Challenge / [Approved context]','Action / [Confirmed activity]','Result / [Verified outcome]'])
fam('problem-solution','Problem and solution','Make the next step clearer.','[Audience question] · [Verified answer or practical action]','View the guide','comparison',['Question / [Specific concern]','Next step / [Useful action]'])
fam('announcement','Announcement','A new chapter at the table.','[Confirmed announcement and effective date]','Read the announcement','alert',['Details: CONFIRM','Source + date: CONFIRM'])
js('templates/content-families.json',F)
# Font metrics determine wrapping; SVG text remains real, editable text.
import pymupdf
fh=pymupdf.Font(fontfile=str(K/'assets/fonts/ArchivoBlack-Regular.ttf'))
fb=pymupdf.Font(fontfile=str(K/'assets/fonts/SpaceGrotesk.ttf'))
def lines(s,width,size,heading=False):
 f=fh if heading else fb; out=[]
 for para in str(s).split('\n'):
  row=''
  for word in para.split():
   cand=(row+' '+word).strip()
   if row and f.text_length(cand,fontsize=size)>width:out.append(row);row=word
   else:row=cand
  out.append(row)
 return out

def txt(s,x,y,size=32,color='#111827',width=900,heading=False,id=None,maxlines=20):
 rows=lines(s,width,size,heading)
 while len(rows)>maxlines and size>16:size-=2;rows=lines(s,width,size,heading)
 lh=size*(1.12 if heading else 1.4)
 return '<text'+(f' id="{id}" data-editable="true"' if id else '')+f' data-width="{width}" x="{x}" y="{y}" fill="{color}" font-family="'+('Archivo Black' if heading else 'Space Grotesk')+f'" font-size="{size}" font-weight="'+('400' if heading else '500')+'">'+''.join(f'<tspan x="{x}" dy="{0 if i==0 else lh}">{esc(t)}</tspan>' for i,t in enumerate(rows))+'</text>',len(rows)*lh

def rect(x,y,w,h,fill,stroke=None,rx=0):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"'+(f' stroke="{stroke}"' if stroke else '')+f' rx="{rx}"/>'
def svgdoc(w,h,body,title,embed=False):return f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}"><title>{esc(title)}</title><style>{fonts if embed else ""}</style>{body}</svg>'

def make_social(f,fmt='square',theme='light'):
 w,h=formats[fmt];dark=theme=='dark';ink='#FFFFFF' if dark else colors['ink'];bg=colors['ink'] if dark else '#FFFFFF';sub='#F5F7FA' if dark else colors['ink']
 a=[rect(0,0,w,h,bg),rect(0,0,16,h,colors['logo-blue']),rect(16,0,8,h,colors['logo-red'])]
 x=64;top=76;cw=w-128;isstory=fmt=='story';land=w/h>1.5
 if isstory:top=290;cw=856
 a.append(txt('RED WHITE AND CLIX',x,top,22,sub,cw)[0])
 if fmt not in ['facebook-cover','linkedin-cover','linkedin-cover-legacy','ultrawide','wide-banner']:
  a.append(f'<image x="{w-204}" y="{top-34}" width="140" height="140" href="{logo}"/>')
 start=top+174;size=76 if w<=1280 else 106
 if land:start=top+132;size=52 if w<1300 else 92;cw=int(w*.53)-x
 head,ht=txt(f['headline'],x,start,size,ink,cw,True,'headline',maxlines=4)
 a.append(head);y=start+ht+24
 body,bh=txt(f['body'],x,y,30 if not land else 25,ink,cw,False,'body',maxlines=4);a.append(body);y+=bh+28
 fields=f['fields']
 if land:fx=int(w*.61);fy=top+154;fw=w-fx-64;fs=22
 else:fx=x;fy=y+4;fw=cw;fs=28
 if f['kind']=='image':
  ih=min(290,h-fy-180) if not land else min(240,h-fy-120)
  a.append(rect(fx,fy-10,fw,max(100,ih),'#F5F7FA','#D1D5DB',8))
  a.append(txt(fields[0] if fields else '[Approved image]',fx+24,fy+40,fs,colors['ink'],fw-48,maxlines=3,id='image-slot-label')[0]);fy+=max(100,ih)+24
  fields=fields[1:]
 if f['kind']=='data':
  for i,s in enumerate(fields):
   label,value=(s.split(' / ',1)+['[Value]'])[:2] if ' / ' in s else (s,'[Value]')
   a.append(rect(fx,fy-22,fw,82,'#F5F7FA',None,8));a.append(txt(label,fx+20,fy+4,20,colors['ink'],fw-40,id=f'field-{i}-label')[0]);a.append(txt(value,fx+20,fy+45,30,colors['link'],fw-40,True,id=f'field-{i}-value')[0]);fy+=96
 else:
  for i,s in enumerate(fields):
   if f['kind'] in ['steps','comparison']:prefix=f'{i+1:02}  '
   else:prefix=''
   t,th=txt(prefix+s,fx,fy+12,fs,ink,fw,False,f'field-{i}',maxlines=3);a.append(t);fy+=th+20
 if f['kind'] in ['data','quote','comparison','case-study']:
  a.append(txt('Source + reporting date: CONFIRM',fx,fy+8,19,ink,fw,id='source',maxlines=2)[0])
 cy=h-124 if not isstory else 1450
 cta_size=23 if land else 28
 a.append(rect(x,cy-38,min(cw,max(250,fb.text_length(f['cta'],fontsize=cta_size)+48)),64,colors['action'],None,8))
 a.append(txt(f['cta'],x+24,cy+4,cta_size,'#FFFFFF',cw-48,id='cta',maxlines=1)[0])
 a.append(txt('redwhiteandclix.org',x,h-40 if not isstory else 1570,22,ink,w-128,id='website')[0])
 # Guides are authoring-only and omitted from exported art by default.
 sr=next(s['safe_rect_xywh'] for s in spec if s['id']==fmt)
 a.append(f'<g id="safe-guides" style="display:none"><rect x="{sr[0]}" y="{sr[1]}" width="{sr[2]}" height="{sr[3]}" fill="none" stroke="#B91C1C" stroke-width="3" stroke-dasharray="14 10"/></g>')
 return svgdoc(w,h,''.join(a),f['title']+' / '+fmt)

T=[]
def register(id,title,category,fmt,svg,fields=None):
 p=f'templates/{category}/{id}.svg'
 put(p,svg.replace('<style>','<style>'+fonts,1))
 T.append({'id':id,'title':title,'category':category,'format':fmt,'path':p,'svg':svg,'fields':fields or []})
for f in F:
 for fmt in ['square','portrait','story','landscape']:
  register(f'{f["id"]}-{fmt}',f'{f["title"]} / {fmt}','social',fmt,make_social(f,fmt,'dark' if f['id'] in ['mission','competition','founder','countdown'] else 'light'))
# Countdown and operational variants are explicit editable masters.
for label in ['30 days','14 days','7 days','3 days','Tomorrow','Today']:
 f=dict(next(f for f in F if f['id']=='countdown'));f['headline']=label+' until we gather.' if 'days' in label else 'We gather '+label.lower()+'.'
 register('countdown-'+label.lower().replace(' ','-'),'Countdown / '+label,'social','square',make_social(f,'square','dark'))
for label in ['Schedule change','Venue change','Registration closing','Sold out','Weather notice','Cancellation']:
 f=dict(next(f for f in F if f['id']=='weather'));f['headline']='[Confirmed] '+label.lower()
 register('notice-'+label.lower().replace(' ','-'),'Operations / '+label,'social','square',make_social(f))
carousels={'first-event':['Your first Red White and Clix event','Check the current format and registration link','Review the schedule and venue details','Bring required game materials','Ask questions. Practice good sportsmanship.','Meet the community and learn what the event supports','View the current event guide'], 'mission-path':['From the table to the mission','Players register for a confirmed event','Sponsors and volunteers help make the gathering possible','RWC documents expenses and beneficiary terms','Confirmed support is transferred or delivered','Results are reported with sources and dates','Read the latest impact report'], 'five-ways':['Five ways to take part','Register for an event','Become a sponsor','Volunteer with RWC','Donate to the mission','Share verified event information','Choose your next step']}
for name,slides in carousels.items():
 for i,title in enumerate(slides):
  f=dict(id=name,title=f'Carousel / {name} / {i+1}',headline=title,body='One Community. One Mission.' if i==0 else ('Process template · confirm actual practice and report links.' if name=='mission-path' else 'Check the current event information at redwhiteandclix.org.'),cta='View the guide' if i==len(slides)-1 else 'Next →',kind='statement',fields=[])
  svg=make_social(f,'portrait','dark' if i in [0,len(slides)-1] else 'light')
  svg=svg.replace('</svg>',txt(f'{i+1:02} / {len(slides):02}',870,1308,22,'#FFFFFF' if i in [0,len(slides)-1] else '#111827',140,id='page-number')[0]+'</svg>')
  register(f'carousel-{name}-{i+1:02}',f['title'],'social','portrait',svg)
# Dedicated banners: central composition, no feed canvas resizing.
for fmt in ['wide-banner','ultrawide','facebook-cover','facebook-event','facebook-group','linkedin-cover','linkedin-cover-legacy','youtube-banner']:
 w,h=formats[fmt];sx,sy,sw,sh=next(s['safe_rect_xywh'] for s in spec if s['id']==fmt)
 mark=min(160,sh*.7);x=sx+mark+32;tw=sw-mark-32;size=min(70,sh*.20,tw/8.8)
 b=rect(0,0,w,h,'#111827')+rect(0,0,16,h,'#0072FF')+rect(16,0,8,h,'#FF0000')
 b+=f'<image x="{sx}" y="{sy+(sh-mark)/2}" width="{mark}" height="{mark}" href="{logo}"/>'
 b+=txt('One Community.\nOne Mission.',x,sy+sh*.35,size,'#FFFFFF',tw,True,'headline',3)[0]
 b+=txt('redwhiteandclix.org',x,sy+sh*.88,max(16,size*.33),'#FFFFFF',tw,id='website')[0]
 b+=f'<g id="safe-guides" style="display:none"><rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="none" stroke="#FFFFFF" stroke-dasharray="12 8"/></g>'
 register('banner-'+fmt,'Banner / '+fmt,'social',fmt,svgdoc(w,h,b,'Banner / '+fmt))
# Avatar preserves the entire mark; small-size legibility is deliberately documented as a limitation.
b=rect(0,0,800,800,'#000000')+f'<image x="144" y="144" width="512" height="512" href="{logo}"/>'
register('avatar-primary','Avatar / primary full mark','social','avatar',svgdoc(800,800,b,'Avatar primary'))
for f in [f for f in F if f['id'] in ['save-date','faq','photo-recap','founder','sponsor-spotlight','beneficiary','new-player','event-update']]:
 ff=dict(f);ff['fields']=['[Approved photo or actual screenshot]'];ff['kind']='image';ff['body']='';ff['cta']='Watch the story'
 register('thumbnail-'+f['id'],'Video / '+f['title'],'social','thumbnail',make_social(ff,'thumbnail','dark'))
for f in [f for f in F if f['id'] in ['education','comparison','impact','new-player']]:
 register('infographic-'+f['id'],'Infographic / '+f['title'],'social','tall',make_social(f,'tall'))
chart_names=['Vertical bar','Horizontal bar','Grouped bar','Stacked bar','100 percent stacked bar','Line','Multi series line','Area','Pie','Donut','Scatter','Bubble','Funnel','Waterfall','Gauge','Progress bar','Progress ring','Sparkline','Heat map','Ranking','Timeline','Comparison matrix']
def chart(name):
 a=[rect(0,0,960,640,'#FFFFFF'),txt(name,40,60,32,'#111827',880,True,id='title')[0],txt('[Metric] · [Reporting period]',40,100,21,width=880,id='subtitle')[0]]
 a+=[f'<path d="M80 150V460H870" fill="none" stroke="#D1D5DB" stroke-width="2"/>']
 blue='#0050B3';red='#B91C1C';ink='#111827'
 def text(s,x,y,sz=20):return txt(s,x,y,sz,ink,700)[0]
 if name in ['Vertical bar','Grouped bar','Stacked bar','100 percent stacked bar','Waterfall']:
  for i,x in enumerate([150,350,550,750]):
   y=230 if name!='Waterfall' else 180+i*55
   if name in ['Stacked bar','100 percent stacked bar']:
    a+=[rect(x,y,70,110,blue),rect(x,y+110,70,110,red)]
   else:a.append(rect(x,y,65,460-y,blue))
   if name=='Grouped bar':a.append(rect(x+72,y+40,42,460-y-40,red))
   a+=[text('[Value]',x-10,y-18,18),text(chr(65+i),x+15,495)]
 elif name in ['Horizontal bar','Ranking']:
  for i in range(4):a+=[rect(170,160+i*74,480 if name=='Horizontal bar' else 520-i*80,40,blue),text(chr(65+i),110,187+i*74),text('[Value]',720,187+i*74)]
 elif name in ['Line','Multi series line','Area','Sparkline']:
  d='M100 360 L270 310 L450 320 L630 230 L830 220'
  if name=='Area':a.append(f'<path d="{d}V460H100Z" fill="#F5F7FA"/>')
  a.append(f'<path d="{d}" fill="none" stroke="{blue}" stroke-width="5"/>')
  if name=='Multi series line':a.append(f'<path d="M100 400L270 360L450 380L630 300L830 320" fill="none" stroke="{red}" stroke-width="5" stroke-dasharray="12 8"/>')
  for x,y in [(100,360),(270,310),(450,320),(630,230),(830,220)]:a+=[f'<circle cx="{x}" cy="{y}" r="7" fill="{blue}"/>',text('[Value]',x-28,y-20,18)]
 elif name in ['Pie','Donut','Progress ring','Gauge']:
  a.append(f'<circle cx="350" cy="310" r="130" fill="{blue if name=="Pie" else "none"}" stroke="#D1D5DB" stroke-width="36"/>')
  if name!='Pie':a.append(f'<path d="M350 180A130 130 0 0 1 480 310" fill="none" stroke="{blue}" stroke-width="36"/>')
  if name=='Pie':a.append(f'<path d="M350 310V180A130 130 0 0 1 480 310Z" fill="{red}"/>')
  a+=[text('[Value]',550,290,30),text('[Label / denominator]',550,335,20)]
 elif name in ['Scatter','Bubble']:
  for i,(x,y) in enumerate([(180,340),(310,280),(430,350),(610,210),(780,260)]):a+=[f'<circle cx="{x}" cy="{y}" r="{22+i*5 if name=="Bubble" else 9}" fill="none" stroke="{blue}" stroke-width="4"/>',text(chr(65+i),x-6,y-40,18)]
 elif name=='Funnel':
  for i in range(4):
   x=120+i*60;ww=680-i*120;y=160+i*74
   a.append(f'<path d="M{x} {y}h{ww}l-45 55H{x+45}Z" fill="{blue}"/>');a.append(txt('[Stage] · [Value]',x+60,y+34,23,'#FFFFFF',ww-120)[0])
 elif name=='Progress bar':
  a+=[rect(100,270,720,64,'#F5F7FA','#D1D5DB',8),text('[Confirmed count] / [Approved goal]',100,245,26),text('Add verified data to set the filled length.',100,380,22)]
 elif name=='Heat map':
  for row in range(4):
   for col in range(7):a+=[rect(120+col*96,160+row*70,88,62,'#F5F7FA','#D1D5DB'),text('[V]',145+col*96,199+row*70,18)]
 elif name=='Timeline':
  a.append('<path d="M130 290H810" stroke="#0050B3" stroke-width="4"/>')
  for i in range(4):a+=[f'<circle cx="{150+i*210}" cy="290" r="10" fill="{blue}"/>',text('[Date]',120+i*210,250),text('[Step]',120+i*210,345)]
 elif name=='Comparison matrix':
  for i,row in enumerate([['Dimension','Option A','Option B'],['[Criterion]','[Value]','[Value]'],['[Criterion]','[Value]','[Value]'],['[Criterion]','[Value]','[Value]']]):
   for j,s in enumerate(row):a+=[rect(100+j*245,160+i*70,245,70,'#F5F7FA' if i==0 else '#FFFFFF','#D1D5DB'),text(s,120+j*245,204+i*70)]
 a+=[text('A — primary series     B – – secondary series',40,535,19),text('SCHEMATIC ONLY · geometry is not RWC data',40,566,18),text('Source: [Organization / record] · Updated [date] · [Footnote]',40,608,18)]
 return svgdoc(960,640,''.join(a),'Data / '+name)
for name in chart_names:register('chart-'+name.lower().replace(' ','-'),'Data / '+name,'charts','chart',chart(name))
js('templates/charts/data-schema.json',{'title':'','subtitle':'','unit':'','reportingPeriod':'','series':[{'name':'','lineStyle':'solid','symbol':'circle','values':[]}],'source':{'organization':'','url':'','retrievedAt':''},'footnote':'','note':'Populate from verified records; recompute geometry with a charting tool. Shipped SVGs are editable schematic templates, not data-driven reporting.'})
# Print masters use actual US Letter aspect; a separate 16:9 presentation family shares typography.
print_apps=[('overview','A seat at the table.','Veteran-founded tabletop events rooted in Indiana.', ['Mission / Build community through tabletop play','People / Players, veterans, families and supporters','Participation / Register, sponsor, volunteer or give']),('event-poster','Red White and Clix 2026','November 7–8 · Lafayette National Guard Armory',['Saturday / RWC 300 Modern','Sunday / Team Sealed · 3v3','Fee + registration URL / CONFIRM']),('event-schedule','Plan your event weekend.','Lafayette, Indiana · November 7–8, 2026',['Saturday / 300 Modern · time: confirm','Sunday / Team Sealed · time: confirm','Check-in, breaks and close / CONFIRM']),('registration-card','Your place at the table.','[Event] · [Date] · [Venue]',['Format / CONFIRM','Fee and fee basis / CONFIRM','Checkout URL / CONFIRM']),('format-explainer','Find your format.','Review the current event rules before registering.',['300 Modern / [Confirmed rules]','Team Sealed / [Confirmed rules]','Required materials / CONFIRM']),('new-player-guide','Your first RWC event.','A little preparation makes it easier to join in.',['Check the format and registration','Review schedule and venue','Bring game materials and good sportsmanship']),('venue-directions','Find the gathering.','Lafayette National Guard Armory',['5218 Haggerty Lane / Lafayette, IN 47905','Parking and access / CONFIRM','Organizer / 574-265-9585']),('sponsor-cover','Stand behind the table.','Red White and Clix · Sponsor prospectus',['Purpose / Veteran-focused tabletop community','Opportunity / [Confirmed benefits]','Contact / redwhiteandclix@gmail.com']),('sponsor-tiers','Choose how to support.','[Confirmed sponsor tiers and availability]',['Tier name / [Approved amount]','Deliverables / [Defined benefits]','Fulfillment / [Owner and date]']),('sponsor-thanks','Thank you, [Sponsor].','[Approved description of support]',['[Approved sponsor logo]','Permission / CONFIRM','Event and date / CONFIRM']),('beneficiary','See where support goes.','[Confirmed beneficiary name]',['Relationship / [Approved description]','Allocation / [Confirmed terms]','Reporting / [Source and date]']),('donation-appeal','Help put purpose behind play.','Support the RWC veteran-focused mission.',['Beneficiary / CONFIRM','Allocation / CONFIRM','Donation route / CONFIRM']),('donation-thanks','Thank you for your support.','[Approved donor acknowledgment text]',['Donor and date / [Confirmed fields]','Gift and reference / [Confirmed fields]','Receipt wording / CONFIRM']),('volunteer','Help make the event happen.','Join the team behind a welcoming gathering.',['Available roles / CONFIRM','Date and location / CONFIRM','Contact / redwhiteandclix@gmail.com']),('impact-cover','What we accomplished together.','Red White and Clix · [Reporting period]',['Attendance / [Verified count]','Funds transferred / [Verified amount]','Beneficiary / [Confirmed organization]']),('impact-statistics','Participation with a record.','[Reporting period and methodology]',['Registrations / [Value + source]','Volunteer hours / [Value + source]','Funds raised / [Value + source]']),('results','The gathering. The result.','[Verified event] · [Date]',['Attendance / [Value]','Support / [Confirmed allocation]','Next step / [Report URL]']),('resource-guide','Find your next source of support.','Veteran resource guide',['Provider / [Verified organization]','Service / [Eligibility and area]','Contact / [Current phone or URL]']),('merchandise','Wear the mission.','[Approved product and current availability]',['[Approved product photograph]','Price and options / CONFIRM','Official store URL / CONFIRM']),('letterhead','Red White and Clix','One Community. One Mission.',['[Date] · [Recipient]','[Subject]','[Approved correspondence]'])]
for id,title,sub,fields in print_apps:
 w,h=816,1056;b=rect(0,0,w,h,'#FFFFFF')+rect(0,0,12,h,'#0072FF')
 b+=txt('RED WHITE AND CLIX',56,68,18,width=520)[0]+f'<image x="620" y="44" width="140" height="140" href="{logo}"/>'
 tt,th=txt(title,56,266,48,'#111827',704,True,'headline',3);b+=tt
 yy=266+th+34;tt,th=txt(sub,56,yy,24,'#111827',704,id='body',maxlines=3);b+=tt;yy+=th+40
 for i,t in enumerate(fields):
  b+=rect(56,yy-22,704,80,'#F5F7FA',None,8);b+=txt(t,76,yy+9,22,'#111827',664,id=f'field-{i}',maxlines=2)[0];yy+=104
 b+=txt('redwhiteandclix.org · 574-265-9585',56,970,20,width=704,id='contact')[0];b+=txt('Working template · replace confirmation fields before publication',56,1004,14,width=704)[0]
 register(id,title,'print','letter',svgdoc(w,h,b,title))
# Contact card and email header masters.
f=dict(F[0]);f['headline']='Red White and Clix';f['body']='Wesley Robertson · redwhiteandclix@gmail.com · 574-265-9585';f['cta']='Visit redwhiteandclix.org'
register('email-header','Email / branded header','social','landscape',make_social(f,'landscape','dark'))
b=rect(0,0,1050,600,'#111827')+f'<image x="70" y="150" width="260" height="260" href="{logo}"/>'+txt('Wesley Robertson',390,200,40,'#FFFFFF',590,True,id='headline')[0]+txt('Red White and Clix\nredwhiteandclix@gmail.com\n574-265-9585\nredwhiteandclix.org',390,276,27,'#FFFFFF',590,id='contact')[0]
register('contact-card','Contact / business card','print','business-card',svgdoc(1050,600,b,'Contact card'))
for id,title,sub in [('title','One Community. One Mission.','Red White and Clix · [Presentation topic]'),('content','Make the next step clear.','[One idea with up to three concise supporting points]'),('data','Participation, documented.','[Verified metric] · [Source] · [Reporting date]'),('quote','“[Approved quote]”','[Name] · [Source] · [Date and permission]'),('photo','Around the tables.','[Verified event/date] · [Photo credit]'),('closing','Take your next seat.','redwhiteandclix.org · [One relevant action]')]:
 ff=dict(id=id,title=title,headline=title,body=sub,cta='redwhiteandclix.org',fields=['[Approved documentary photograph]'] if id=='photo' else [],kind='image' if id=='photo' else 'statement')
 register('slide-'+id,'Presentation / '+id,'slides','widescreen',make_social(ff,'widescreen','dark' if id in ['title','closing'] else 'light'))
# Template index includes native editable SVG paths; source HTML editor will hold lightweight copies.
js('templates/inventory.json',[{k:v for k,v in t.items() if k!='svg'} for t in T])
# Downloadable documentation and source hierarchy.
put('0 - READ ME FIRST.md','''# Red White and Clix — Complete design kit

Edition 1.0 · September 21, 2026 · Prepared by BlakSheep Creative.

Open `index.html` for the complete visual reference. It is self-contained and works offline. Choose Print / Save PDF or use the supplied PDF in `exports/`.
Open `template-studio.html` to browse templates, edit text, toggle crop guides, and download SVG, PNG, or JPG. Changes stay in the browser until you save an SVG; reopening a template resets it. Save your edited SVG before switching templates. Source SVGs also open in vector editors; install the included fonts first when your editor does not support embedded font CSS.

## Included
- Visual brand system and component reference (HTML and PDF)
- CSS tokens, JSON token map, and DTCG-style token export
- Native HTML components with shared CSS
- Editable SVG social, chart, print and slide masters
- Bundled Archivo Black and Space Grotesk fonts with OFL licenses
- Official supplied logo and 14 documentary photo references with provenance
- Platform configuration, template inventory, source briefs and handoff documentation

## Start a design
1. Read `2 - Brand Guidelines.md` and `3 - Visual Identity.md`.
2. Duplicate a relevant template in the studio or your vector editor.
3. Replace all bracketed or CONFIRM fields with sourced information.
4. Confirm photographic rights/context, event details, sponsor status and CTA destination.
5. Check small-screen readability and crop preview, then export.

## Status
The supplied logo and existing palette/typefaces are established. The UI, layouts, component system and templates are a working extension for review. The proposed campaign line has not replaced “One Community. One Mission.” No new logo lockups or faithful vector master have been invented. Chart drawings are schematic placeholders, not reported results; use verified data to calculate final geometry. Shared platform masters do not imply ownership of those accounts.

## For developers
Link `styles.css` or import the individual token files. `components/*.html` are framework-free standalone specimens; copy the markup inside main into your project. Buttons and forms in the reference are visual specimens, with no backend, checkout or newsletter submission. The future website is not implemented by this kit.

## Rebuild
With Python 3.12+, install the packages in `tools/requirements.txt`. Run `python tools/build_kit.py`, then `python tools/export_and_check.py`. The builder reads the existing repository brand files and the client photo directory; it is intended for the agency workspace. The exported HTML/SVG/CSS/PDF files themselves have no build dependency.
''')
for out,src in [('2 - Brand Guidelines.md','brand-style-guide.md'),('3 - Visual Identity.md','brand/identity.md'),('4 - Brand Voice.md','brand/voice.md'),('5 - Messaging.md','brand/messaging.md')]:shutil.copy2(R/src,K/out)
put('1 - MASTER PROMPT.md','''# Red White and Clix production prompt
Read the numbered brand documents, tokens/tokens.json, and the relevant template before designing. Preserve the client-supplied logo exactly. Use Archivo Black display and Space Grotesk body/UI. Derive styling from semantic tokens. Keep bright logo hues separate from darker action colors. Use one clear CTA and direct, welcoming language. Recompose layouts for each format. Use only sourced operational details; preserve visible CONFIRM BEFORE PUBLISHING fields when facts are unresolved. Do not fabricate quotes, ratings, sponsor relationships, prices, impact totals, or medical claims. Do not use political framing, camouflage, or the logo memorial detail as decoration. Keep documentary photography separate from mockups and illustration. Deliver editable source and an export; attach source/date to researched content. Follow guidelines/production-handoff.md.
''')
put('6 - Brand Context and Prices.md','''# Context and prices

Red White and Clix is a veteran-founded tabletop event community serving Lafayette/West Lafayette and the wider Midwest. Founder/contact: Wesley Robertson; redwhiteandclix@gmail.com; 574-265-9585; redwhiteandclix.org.

The project research dated September 21, 2026 records November 7–8, 2026 at Lafayette National Guard Armory, 5218 Haggerty Lane, Lafayette IN 47905. Saturday: RWC 300 Modern. Sunday: Team Sealed, 3v3. These samples are carried forward from supplied records, not newly verified event listings.

Prices and authoritative purchase routes conflict in captured sources. Do not publish an assumed price. Confirm the fee, per-person/per-team basis, registration link, refund policy, check-in time, hotel rate, product availability and store URL before release. Beneficiary terms, donation allocations, sponsor tiers/permissions and operational beginner support also require confirmation. Do not invent office hours, a new venue, an account handle, or a guarantee.

The brand package records federal nonprofit verification in September 2026. Do not treat a ruling date as a founding date, and do not expand it into tax advice or promises about individual gifts.
''')
put('guidelines/production-handoff.md','''# Production handoff

## Editing and exports
Use the studio to change editable SVG text without flattening. Keep copy close to the length of the master; long text must be reviewed in the preview. A blue or red dashed crop guide is an authoring aid; exports omit guides. Use SVG for editable handoff, PNG for crisp digital graphics, JPG for photo-heavy uploads, PDF for document review. Downloaded PNG/JPG uses the canvas dimensions in the template, not the scaled preview size. Font files and logo are embedded in exported SVGs. In applications that ignore embedded fonts, install the bundled TTFs, then reopen.

Browser Print / Save PDF on index.html uses US Letter pages, background graphics on, margins none and browser headers/footers off. The supplied PDF already applies those settings. All layouts remain editable in HTML/SVG; the PDF is the review/export format.

Print masters use US Letter trim (8.5 × 11 in). The contact card is 3.5 × 2 in at 300 canvas pixels per inch. Add printer-specified bleed (commonly 0.125 in) in the production file; these review masters do not include bleed, crop marks, a CMYK ICC profile or PDF/X certification. The 700px raster logo does not become vector by putting it inside SVG. At 300ppi its native width is 2.33in; request vector masters for larger print. CMYK values in the reference are mathematical approximations only; use the printer's profile and proof for conversion.

## One idea into a campaign
1. Capture the fact, source, reporting date, approved copy and one CTA.
2. Start with the matching content family; use portrait for the detailed composition, landscape for the concise split composition, story for the protected central stack.
3. Keep sources in the art for factual data. Move detailed explanation to a linked report or carousel.
4. Use the platform-map and specification file to choose a canvas. Check the actual uploader crop; interface overlays can change.
5. Export PNG/JPG for digital delivery. Keep the SVG as the editable record.

## Tokens and extensions
`tokens/tokens.json` is the simple CSS-oriented token map; `tokens/design-tokens.dtcg.json` is an interchange export. Complex CSS strings (shadows, easing, clamp) remain string tokens and may need mapping in design-tool importers. CSS is split by colors, typography, spacing, effects and social. Existing rwc token names are preserved. New success/info styles use blue, errors use red, warnings use ink and written labels; no new green/yellow palette is introduced.

New platforms should add dimensions, safe_rect_xywh, crop notes and a source in platform-specifications.json. Do not recolor another client's kit. The content family architecture is reusable; brand assets, tokens and typography are client-specific.

## Data and accessibility
Every chart includes title, subtitle, series labels, source/date and footnote slots. Schematic geometry is not data. Populate a verified dataset, calculate scales and labels, and keep an accessible table beside complex charts. Use line dashes, symbols and labels as well as color. Do not export bracketed values as campaign results.

Use 44px touch targets, visible focus, readable error messages, 16–18px minimum web body type and 12–14px captions. Normal text pairings have measured contrast in the reference. All user interface semantic statuses have text labels. Reduced-motion preference is honored. Components are specimens, not a certified production application.

## Ownership
Wesley Robertson is the brand guardian. Agency lead: Clint Sanchez, BlakSheep Creative. Record approvals of new taglines, identity masters, sponsor or beneficiary statements and public results. Review before each event and quarterly. This delivery sends no client communication and publishes nothing.
''')
put('guidelines/logo-production-spec.md','''# Logo production specification

Authority: assets/logos/red-white-and-clix-logo.png, 700×700 client-supplied artwork. Preserve stacked wording, star and memorial detail exactly. Do not extract the memorial element as decoration. The supplied PNG has transparency; use a clean black or dark backing when needed.

Needed production masters: faithful traced vector primary, approved horizontal arrangement, one-color dark/light, small-size simplified icon and favicon. These are not supplied as finished logos because approving altered identity artwork requires a separate decision. Use the supplied raster in all current templates. The SVG templates contain a raster image element and are not vector logo masters.

Clear space: 10% of actual mark width; minimum proposed full-mark digital width 120px. Social avatar is a padded full-logo master with circular-crop preview; at 32/64px the detailed mark loses legibility. Do not claim a finished small-size icon exists. Ask a vector artist to preserve actual outlines and compare side-by-side with the authority at multiple sizes.
''')
put('tools/requirements.txt','PyMuPDF==1.28.2\nplaywright==1.63.0\n')
put('guidelines/platform-sources.md','''# Platform source notes · September 21, 2026

LinkedIn company cover: 1512×256, updated from the supplied brief's legacy 1128×191. Primary source: https://www.linkedin.com/help/linkedin/answer/a563309. LinkedIn link image: 1200×627; shared landscape master is 1200×630, so choose a channel-specific size before delivery if required.

YouTube banner: 2560×1440. The official minimum canvas is 2048×1152 with a 1235×338 text/logo zone. The kit uses a conservatively rounded central 1544×422 zone on the recommended canvas. Primary source: https://support.google.com/youtube/answer/10456525.

Other dimensions follow the supplied universal/RWC briefs as editable production defaults, not verified current platform requirements. Facebook's official page at https://www.facebook.com/help/125379114252045 returned a login page. Safe zones are design guides, not guarantees about every device. Verify uploader crop and size limits before publication. Shared masters for optional platforms do not establish RWC account ownership.
''')
# Calculate text contrast; ratios are measurements, not aesthetic judgments.
def luminance(h):
 v=[int(h[i:i+2],16)/255 for i in [1,3,5]];v=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in v];return sum(a*b for a,b in zip(v,[.2126,.7152,.0722]))
def contrast(a,b):
 x,y=sorted([luminance(a),luminance(b)]);return (y+.05)/(x+.05)
contrasts=[{'foreground':a,'background':b,'ratio':round(contrast(a,b),2),'normal_text_AA':contrast(a,b)>=4.5} for a,b in [('#FFFFFF','#B91C1C'),('#FFFFFF','#0050B3'),('#111827','#FFFFFF'),('#111827','#F5F7FA'),('#FFFFFF','#FF0000'),('#FFFFFF','#0072FF')]]
js('tokens/contrast-report.json',contrasts)
# A manifest records actual shipped assets and their provenance.
js('_ds_manifest.json',{'name':'Red White and Clix Design System','version':'1.0.0','entry':'index.html','editor':'template-studio.html','styles':'styles.css','tokens':'tokens/tokens.json','components':[{'name':n,'sourcePath':f'components/{n}.html'} for n in C],'templates':[{'name':t['title'],'path':t['path']} for t in T],'brandFonts':[{'family':'Archivo Black','file':'assets/fonts/ArchivoBlack-Regular.ttf'},{'family':'Space Grotesk','file':'assets/fonts/SpaceGrotesk.ttf'}],'note':'Portable HTML/SVG kit. This manifest is an inventory, not a claim of compatibility with a proprietary import format.'})
# The reference is laid out as fixed US Letter sheets for predictable PDF output.
P=[]
def page(section,title,body,cls=''):
 P.append({'section':section,'title':title,'body':body,'class':cls})
def p(s):return '<p>'+s+'</p>'
def grid(*items):return '<div class="grid">'+''.join(items)+'</div>'
def panel(title,body):return '<div class="panel"><h3>'+title+'</h3>'+body+'</div>'
def table(headers,rows):return '<table><thead><tr>'+''.join('<th>'+str(x)+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(x)+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table>'
def note(s):return '<aside class="note">'+s+'</aside>'
def specimen(t,height=245):return '<figure class="specimen"><div class="art" style="height:'+str(height)+'px">'+t['svg']+'</div><figcaption>'+esc(t['title'])+'</figcaption></figure>'
def gett(id):return next(t for t in T if t['id']==id)
page('00 / The complete kit','A shared table.\nA clear identity.',f'<div class="cover-brand"><img src="{logo}" alt="Red White and Clix supplied logo"><div>RED WHITE AND CLIX<br><span>One Community. One Mission.</span></div></div><div class="cover-title">A shared table.<br>A clear identity.</div><p class="cover-intro">The complete brand, component and content system. Built for the people who organize, play, volunteer and support.</p><div class="cover-bottom"><strong>DESIGN SYSTEM / EDITION 1.0</strong><p>September 21, 2026<br>Prepared by BlakSheep Creative</p><span>Guidelines · Components · Templates · Tokens</span></div>','cover')
page('00 / Read me first','One kit. Every touchpoint.',p('Use this reference to make every Red White and Clix touchpoint feel related: from a registration card to an impact report, a social carousel to an event poster.')+grid(panel('Read and review',p('Open this HTML offline or use the supplied PDF. Print / Save PDF produces the same US Letter page sequence.')),panel('Make and export',p('Open template-studio.html. Choose a master, edit the text, preview the crop guide and download SVG, PNG or JPG.')))+table(['Included','What you can use'],[['Brand foundations','Identity, voice, messaging, typography and production rules'],[f'{len(C)} HTML components','Native reusable markup and shared CSS'],[f'{len(T)} editable templates','Social, charts, print collateral and presentation slides'],['Design tokens','CSS, JSON, DTCG-style export, contrast measurements'],['Source assets','Original logo, licensed fonts and 14 documentary photo references']])+note('Working system for review. The supplied identity is established; UI and creative extensions are proposed. Confirmation fields intentionally remain visible where source facts are unresolved.'))
page('00 / Contents','Find the right layer.',table(['Section','Contents'],[['01 / Brand foundation','Mission, positioning, audiences and brand promise'],['02 / Logo system','Supplied artwork, clear space, avatar and production gaps'],['03 / Color and type','Palette, accessible pairings, type hierarchy'],['04 / Layout and UI','Spacing, grids, buttons, forms, navigation and components'],['05 / Imagery','Documentary photos, icons and graphic treatments'],['06 / Voice and messaging','Language, headline bank, CTAs and audience messages'],['07 / Social and digital','Content families, masters, carousels and banners'],['08 / Data','22 chart structures, KPI and evidence rules'],['09 / Print and slides','US Letter applications, contact card and slide masters'],['10 / Production','Assets, exports, governance and confirmation register'],['11 / Tokens','CSS values, semantic aliases and implementation handoff']])+p('Every component and template has a corresponding editable file in the kit. The PDF is the visual reference; the HTML, SVG and token files are the working source.'))
page('01 / Brand foundation','Play brings people together.',panel('Mission',p('Bring people together through well-run tabletop gaming events that create camaraderie, raise awareness and support veteran-focused causes.'))+grid(panel('Positioning',p('The veteran-founded tabletop event community for players and supporters who want serious play, genuine connection and a clear way to support veteran causes.')),panel('Brand promise',p('A welcoming seat, a well-run event and an honest account of the mission your participation supports.')))+table(['Value','What it means in the work'],[['Belonging','Explain the next step; welcome new and returning players.'],['Play with purpose','Competent events and an understandable mission.'],['Service without spectacle','Respectful, human imagery and practical language.'],['Transparent impact','Publish confirmed results with sources and dates.'],['Camaraderie','Show people participating together as peers.']]))
page('01 / Brand foundation','Design for the next person in.',table(['Audience','Needs','Design response'],[['Competitive players','Format, rules, schedule, fee','Put logistics together; clear registration route.'],['Veterans and families','Respect and connection','Peer participation; no pity or clinical promises.'],['New or returning players','A manageable first step','Plain terms, helpful sequence, clear expectations.'],['Sponsors','Defined benefits and follow-through','Tier details, contact path and sourced results.'],['Donors and volunteers','Purpose and transparency','Specific next action, allocation and accountability.']])+grid(panel('Personality',p('Welcoming · organized · energetic · grounded · practical · respectful.')),panel('Focus',p('HeroClix-centered tabletop events, Indiana roots and a wider Midwest community.')))+note('Use RWC after the full name has appeared. Do not imply national programs, military endorsement or additional services that have not been established.'))
page('02 / Logo system','The supplied mark is the authority.',f'<div class="logo-stage"><img src="{logo}" alt="Official supplied Red White and Clix logo"></div>'+table(['Asset','Status'],[['Primary stacked raster','Supplied PNG · 700 × 700 · transparent PNG'],['Horizontal / one-color masters','Production specification supplied; artwork not yet commissioned'],['Simplified icon / favicon','Requires approved small-size design'],['Avatar','Padded full-logo master supplied; small-size limitations documented']])+note('Preserve the complete artwork, including the memorial detail. An SVG containing this PNG is an editable layout, not a vector logo.'))
page('02 / Logo system','Give the mark room.',f'<div class="clearspace"><img src="{logo}" alt="Logo with visible surrounding clear space"></div>'+grid(panel('Clear space',p('At least 10% of the artwork width on all sides. Keep type, photos and other logos outside this area.')),panel('Minimum size',p('Proposed full-mark minimum: 120 CSS pixels. At 300ppi, the 700px original supports about 2.33 inches at native resolution.')))+table(['Use','Avoid'],[['Black plate and preserved proportions','Recoloring, stretching, rotation or glow'],['Entire supplied mark','Rebuilding the wordmark from a typeface'],['Separate identity and photography','Putting it directly on a busy photograph'],['New vector artwork after review','Extracting the memorial detail as a pattern']]))
page('02 / Logo system','An honest avatar system.',grid(specimen(gett('avatar-primary'),310),panel('One supported variant',p('The primary artwork sits inside a black square with central padding. The circular crop protects the full mark; there is no invented monogram or isolated memorial symbol.')+p('Use the 800px master for upload. Test actual small previews before use.')))+'<div class="avatar-row">'+''.join(f'<div><img style="width:{s}px;height:{s}px;border-radius:50%" src="{logo}" alt="Logo legibility at {s}px"><span>{s}px</span></div>' for s in [32,64,128,256])+'</div>'+note('The current detailed logo loses legibility at 32px and 64px. A simplified icon and favicon remain a separate identity production task. These size previews are tests, not approved small-logo variants.'))
# Color tables contain RGB and mathematical CMYK approximations.
def cmyk(h):
 r,g,b=[int(h[i:i+2],16)/255 for i in [1,3,5]];k=1-max(r,g,b)
 return ' / '.join(str(round(x*100)) for x in ([0,0,0,1] if k==1 else [(1-r-k)/(1-k),(1-g-k)/(1-k),(1-b-k)/(1-k),k]))
for title,subset in [('Identity colors',list(colors.items())[:4]),('Interface colors',list(colors.items())[4:])]:
 sw='<div class="swatches">'+''.join(f'<div><div style="background:{v};border:1px solid #D1D5DB"></div><strong>{k}</strong><code>{v}</code></div>' for k,v in subset)+'</div>'
 rows=[[k,v,', '.join(str(int(v[i:i+2],16)) for i in [1,3,5]),cmyk(v)] for k,v in subset]
 page('03 / Color system',title+'.',sw+table(['Role','HEX','RGB','CMYK %*'],rows)+note('*CMYK is an approximate mathematical conversion, not a press specification. Use the printer’s ICC profile and proof. Bright logo colors remain in the artwork; darker action colors carry normal-size text.'))
page('03 / Color system','Pair color with evidence.',table(['Foreground','Background','Contrast','Normal text'],[[a['foreground'],a['background'],str(a['ratio'])+':1','AA pass' if a['normal_text_AA'] else 'Fails AA'] for a in contrasts])+grid(panel('Action and links',p('White on action red. White on action blue. Blue links on white with underlines. Ink on white or light surfaces.')),panel('Status and data',p('Success/info use blue; error uses red; warning uses ink. Pair each with a written label, icon, symbol or line style.')))+p('Recommended composition: 60% white/light, 20% ink/dark, 10% blue and 10% red. This guides balance across a composition; it is not a pixel quota.')+note('Quiet gray borders are for grouping and decoration. Input boundaries use ink so that an essential control is not defined by a faint divider alone.'))
page('03 / Typography','Bold display. Human details.','<div class="type-display">Archivo Black</div><p class="type-sample">One Community.<br>One Mission.</p><div class="type-body">Space Grotesk</div><p class="type-body-sample">Clear dates. Helpful directions. A welcoming place to play.</p>'+table(['Role','Family','Weight','Use'],[['Display','Archivo Black','400','Short headlines and chapter titles'],['Body','Space Grotesk','400 / 500','Reading copy and supporting content'],['UI / labels','Space Grotesk','600 / 700','Buttons, controls, metadata and tables']])+note('Both families are carried forward from the existing site. Bundled TTF files include their SIL Open Font Licenses and work offline. Do not use either font to reconstruct the logo.'))
page('03 / Typography','A hierarchy you can repeat.',table(['Role','Desktop','Mobile','Line height'],[['Display / H1','56–72px','36–48px','1.08–1.12'],['H2','36–48px','28–36px','1.12'],['H3','24–30px','21–26px','1.2'],['Body large','20px','18px','1.5–1.6'],['Body','16–18px','16–18px','1.6'],['Label / button','14–16px','14–16px','1.3'],['Caption / source','12–14px','12–14px','1.5']])+grid(panel('Writing in type',p('Sentence case. Short display headlines. Left-aligned reading copy. Uppercase only for brief eyebrows. Reading measure: up to 70ch.')),panel('Social scale',p('Typical 1080px canvas: headline 72–76px, body 30–32px, source 22–24px. The editor preserves text wrapping; review if copy length changes.')))+note('Slides use larger text at 1920×1080. When content is dense, use more slides or a linked document instead of shrinking the body.'))
page('04 / Layout','A measured, open grid.','<div class="spacing-demo">'+''.join(f'<div><span>{n}px</span><i style="width:{n*3}px"></i></div>' for n in [4,8,12,16,24,32,48,64,96])+'</div>'+table(['Rule','Value'],[['Spacing','8px main rhythm with 4px half steps'],['Content width','1200px maximum'],['Reading column','70ch maximum'],['Gutters','32px desktop / 16px mobile'],['Columns','12 desktop / 4 mobile conceptual grid'],['Section spacing','64px default; 96px for major breaks']])+p('Stack columns on small screens. Show event date, venue and registration details before long sponsor sections. Align labels, body copy and action edges.'))
page('04 / Layout','Shape supports the content.',grid(panel('Cards',p('White surface · 1px neutral border · 8px radius · 24px internal padding. Default flat; use a subtle shadow only to establish a real layer.')),panel('Controls',p('8px button and input radius. Minimum 44px target. Clear focus outline, a pressed color and an explicit disabled label.')))+table(['Token','Value'],[['Small shadow','0 2px 8px / ink at 8%'],['Medium shadow','0 8px 24px / ink at 12%'],['Large shadow','0 16px 48px / ink at 16%'],['Motion','120ms fast / 180ms standard'],['Easing','cubic-bezier(.2, 0, 0, 1)'],['Reduced motion','No animation or transitions']])+note('Hover changes color. Avoid jumpy scale effects, parallax, automatic movement, glass effects and excessive rounding.'))
# Every shipped UI component gets a visible specimen and description.
items=list(C.items())
for i in range(0,len(items),4):
 chunk=items[i:i+4]
 b='<div class="component-grid">'+''.join('<section class="component-spec"><h3>'+n+'</h3><div class="component-live">'+v['html']+'</div><p class="spec-desc">'+esc(v['description'])+'</p></section>' for n,v in chunk)+'</div>'
 page('04 / Component library',f'Components {i+1:02}–{min(i+4,len(items)):02}.',b)
page('05 / Photography','People, participating together.',p('Use documentary images of players at tables, welcoming interactions, organizers working and the event room. Keep natural color and honest context. Archive images do not establish the date of the next event.')+'<div class="photo-grid">'+''.join(f'<figure><img src="{datauri(p)}" alt="Documentary tabletop event reference"><figcaption>{esc(p.name[:20])}…<br>Context, credit and permission: confirm</figcaption></figure>' for p in [(K/'assets/photography'/n) for n in ['fb-a773fb13f49d.jpg','fb-b1e412d378a4.jpg','fb-7b11d485923b.jpg','fb-c12443d33e60.jpg']])+'</div>'+note('The 14 selected originals and their source manifest are included for internal reference. Public reuse requires context and permission review. No people are identified from image filenames.'))
page('05 / Graphic language','A little structure. Plenty of room.',grid(panel('Line icons','<div class="icon-grid">'+''.join('<div>'+icon(n)+'<small>'+n+'</small></div>' for n in icons)+'</div>'),panel('Graphic devices',p('Clean table-grid lines, lightly rounded rectangles and restrained red/blue edge accents. Use a single device per composition.')+p('No camouflage, distressed flags, neon esports effects, metallic gradients or repeating memorial symbols.')))+panel('Image treatments',p('Use framed, split or full-width photos with readable captions. Put copy on a solid panel next to the image. Product mockups stay labeled as mockups. Screenshots must come from a real interface.'))+note('No new mascot, fictional founder, AI attendee or military-themed illustration system is introduced.'))
page('06 / Voice','Sound like an organized host.',grid(panel('Welcoming',p('“There’s a seat at the table for you.” Invite participation without insider tests.')),panel('Practical',p('Lead with what, when, where and how. Explain the format before asking someone to register.')),panel('Grounded',p('Name the source and date. Say what is confirmed and what the organizer still needs to resolve.')),panel('Respectful',p('Treat veterans as people with agency and interests. Show camaraderie without pity or clinical promises.')))+table(['Use','Avoid'],[['Play, join, community, camaraderie','Partisan slogans and divisive framing'],['Support, participate, volunteer','“Save veterans” and medical guarantees'],['Confirmed results with dates','Invented totals, ratings or urgency'],['Clear beneficiary and allocation','“Every dollar goes directly” without records']]))
page('06 / Messaging','A consistent message bank.',panel('Organizational line','<h3>One Community. One Mission.</h3>')+panel('Core message',p('Tabletop play creates a place to belong and a practical way to stand with veterans.'))+grid(panel('Short description',p('Veteran-founded tabletop events where players compete, connect and support veteran-focused causes—together, at the same table.')),panel('Elevator pitch',p('Red White and Clix brings gamers, veterans, families and supporters together through organized tabletop events. Players get a welcoming, competitive experience. Partners get a practical way to participate in a veteran-focused mission rooted in Indiana.')))+note('“Play Together. Stand With Veterans.” is a proposed campaign line, pending brand-guardian approval. The templates default to the current organizational line.'))
page('06 / Messaging','One clear action at a time.',table(['Audience / purpose','Headline','CTA'],[['Player','Bring your best team—and your best sportsmanship.','View event details'],['Newcomer','New to HeroClix? Start here.','Read the event guide'],['Community','Camaraderie starts at a shared table.','Join the community'],['Sponsor','Stand behind a community that shows up.','Become a sponsor'],['Donor','Know what your gift supports.','Read the impact report'],['Volunteer','Help make the gathering possible.','Volunteer with RWC'],['Veteran resources','Looking for support? Start here.','View veteran resources']])+p('Registration is the primary event journey. Donation, sponsorship, volunteering and shopping are distinct actions. Keep one dominant action per asset.')+note('Use contractions naturally. Avoid long all-caps text, unexplained jargon and repeated exclamation marks. Emoji are optional and sparse in captions; do not substitute them for information or icons.'))
page('07 / Social and digital','One concept, recomposed.',grid(specimen(gett('save-date-square'),240),specimen(gett('save-date-portrait'),240),specimen(gett('save-date-landscape'),240),specimen(gett('save-date-story'),240))+p('Square puts the statement over the details. Portrait adds breathing room. Landscape splits the message and logistics. Story protects the central content from interface overlays.')+note('Every one of the 30 content families has square, portrait, story and landscape masters. Each format has its own layout, not a cropped copy of the first.'))
for i in range(0,len(F),4):
 chunk=F[i:i+4]
 page('07 / Social content families',f'Content families {i+1:02}–{min(i+4,len(F)):02}.',grid(*(specimen(gett(f['id']+'-square'),285) for f in chunk))+p('Editable square, portrait, vertical and landscape versions are supplied for each family shown. Replace confirmation fields before publishing.'))
for name,slides in carousels.items():
 page('07 / Carousel system',{'first-event':'Your first event.','mission-path':'From table to mission.','five-ways':'Five ways to take part.'}[name],'<div class="carousel-grid">'+''.join(specimen(gett(f'carousel-{name}-{i+1:02}'),180) for i in range(len(slides)))+'</div>'+note('Consistent ratio, safe area, branding and page numbers. One idea per slide. The mission sequence is a process template; confirm actual practice and report links before release.'))
page('07 / Operational templates','Useful updates, calmly delivered.',grid(*(specimen(gett('notice-'+s),230) for s in ['schedule-change','venue-change','weather-notice','cancellation']))+p('Additional masters cover registration closing and sold-out status. Countdown variants cover 30, 14, 7 and 3 days, tomorrow and today.')+note('Choose an update only when the status is verified. Every operational template requires a timestamp, authoritative link and contact route. A countdown master is not evidence that the event is nearly full.'))
page('07 / Video and long-form','Give the idea a clear frame.',grid(specimen(gett('thumbnail-new-player'),240),specimen(gett('thumbnail-photo-recap'),240),specimen(gett('infographic-education'),260),specimen(gett('infographic-impact'),260))+p('Eight dedicated thumbnail themes cover event announcement, FAQ/format, recap, founder, sponsor, beneficiary, new-player and update videos. Four tall infographic masters cover education, comparison, impact and new-player content.'))
page('07 / Banner system','Protect the center.', ''.join(specimen(gett('banner-'+s),150) for s in ['wide-banner','linkedin-cover','facebook-cover','youtube-banner'])+note('Banner layouts use dedicated central content zones. Guides in the editor are conservative design aids; inspect the real desktop and mobile uploader crops. Legacy LinkedIn and other shared banner masters are also included.'))
for i in range(0,len(spec),8):
 chunk=spec[i:i+8]
 page('07 / Platform configuration','Editable canvas specifications.',table(['Master','Canvas','Safe area (x, y, w, h)'],[[s['id'],f'{s["width"]} × {s["height"]}',', '.join(map(str,s['safe_rect_xywh']))] for s in chunk])+p('Canvas and safe-area values are stored in tokens/platform-specifications.json. Most follow the supplied brief as production defaults; they are not guarantees about a platform’s current uploader.')+p('Verified September 21, 2026: <a href="https://www.linkedin.com/help/linkedin/answer/a563309">LinkedIn company cover</a> is 1512 × 256. <a href="https://support.google.com/youtube/answer/10456525">YouTube banner</a> is 2560 × 1440; the center guide is conservatively scaled from its official minimum-size safe area.')+note('The brief’s 1128 × 191 LinkedIn cover remains as a labeled legacy master. Other channel variants can inherit a shared ratio; check exact upload dimensions and preview before release.'))
page('07 / Platform mapping','Start with the content family.',table(['Channel','Shared masters'],[[n,', '.join(v)] for n,v in platforms.items()])+note('Instagram, TikTok, LinkedIn, YouTube and other optional templates do not imply RWC owns verified accounts there. Add confirmed account links only when supplied.'))
page('08 / Data and evidence','Design the container. Verify the result.',grid(panel('Metric structure',p('Title → reporting period → value and unit → comparison context → source and date. Each value needs its own provenance.')),panel('Chart structure',p('Use clear axes, direct labels, written legends and non-color distinctions. Include a table or narrative for complex graphics.')))+C['KPIGrid']['html']+C['Citation']['html']+note('The following charts are schematic templates with bracketed fields. Their shapes are illustrative geometry, not sample RWC results. No invented numerical performance data is supplied.')+p('The source SVG can be edited in a vector tool. Populate verified data and recalculate geometry using your reporting or charting tool; these SVGs are not a data-driven dashboard.'))
for i in range(0,len(chart_names),4):
 chunk=chart_names[i:i+4]
 page('08 / Chart library',f'Chart structures {i+1:02}–{min(i+4,len(chart_names)):02}.',grid(*(specimen(gett('chart-'+n.lower().replace(' ','-')),270) for n in chunk))+p('Labels, titles and citation fields remain editable. Do not publish bracketed values or schematic geometry as a reported outcome.'))
for i in range(0,len(print_apps),4):
 chunk=print_apps[i:i+4]
 page('09 / Print applications',f'Print masters {i+1:02}–{min(i+4,len(print_apps)):02}.',grid(*(specimen(gett(a[0]),300) for a in chunk))+p('US Letter composition · editable SVG. The working copy comes from the client brief; unresolved operational fields stay visible.'))
page('09 / Contact and email','The everyday touchpoints.',specimen(gett('contact-card'),270)+specimen(gett('email-header'),270)+note('Contact card master: 3.5 × 2 inches at 300 canvas pixels per inch. Add the printer’s required bleed and color conversion before press. Email header uses the shared landscape layout.'))
for i in range(0,6,3):
 slides=[t for t in T if t['category']=='slides'][i:i+3]
 page('09 / Presentation system','A slide for each job.', ''.join(specimen(t,205) for t in slides)+p('1920 × 1080 / 16:9. Keep one message per slide. Use the data and quote masters only with verified records and approved attribution.'))
page('10 / Asset library','Everything has a place.',table(['Folder / file','Purpose'],[['index.html','Self-contained visual reference, printable offline'],['template-studio.html','Local text editor with SVG / PNG / JPG export'],['exports/','Matching PDF and template preview exports'],['tokens/','CSS layers, JSON, platform config and contrast report'],['components/','HTML specimens and component inventory'],['templates/','Social, chart, print and slide SVGs plus inventories'],['assets/logos/','Original supplied PNG; preserved bytes'],['assets/fonts/','Bundled TTF files and OFL license texts'],['assets/photography/','14 original reference photographs and source manifest'],['assets/icons/','16 editable SVG line icons'],['guidelines/','Brand rules, source notes and production handoff'],['tools/','Rebuild and export scripts']])+p('The numbered Markdown files mirror the master-brand-kit folder convention: read me, production prompt, guidelines, visual identity, voice, messaging, and context/prices.'))
page('10 / Production','From master to finished asset.',table(['Output','Use','Review'],[['SVG','Editable source in a vector editor','Install included fonts if the app ignores embedded font CSS.'],['PNG','Digital graphics and text-heavy art','Check exact canvas dimensions and actual upload crop.'],['JPG','Photo-heavy digital assets','Inspect compression and legibility.'],['PDF','Reference and review','US Letter, background graphics, no browser headers.'],['Print','Vendor-ready collateral after prepress','Add bleed, check image resolution, convert with printer profile.']])+panel('The supplied PDF',p('This is a visual system reference, not a press-certified PDF/X document. Editable print masters are supplied separately. Large printed logos require a faithful vector master.'))+panel('Source control',p('Keep the edited SVG with its final export, source facts and approval record. Update the content family and tokens rather than making untracked visual changes across many posts.')))
page('10 / Governance','Resolve the fact. Keep the field.',table(['Field','Required evidence / decision'],[['Event fee and checkout','Authoritative price, fee basis and registration URL'],['Schedule and access','Start/check-in times, parking and accessibility details'],['Beneficiary and allocation','Approved relationship, expenses and transfer terms'],['Sponsor material','Confirmed tiers, deliverables, availability and logo permission'],['Impact metrics','Verified record, reporting period and calculation method'],['Quotes and reviews','Exact source, date, attribution and permission'],['Photographs','Context, verified date, photographer and usage permission'],['Merchandise','Current product, price, availability and official store'],['Brand extensions','Campaign line, new logo masters and simplified icon']])+note('Wesley Robertson is the brand guardian; Clint Sanchez / BlakSheep Creative is the agency lead. Review quarterly and before each major event. This kit does not publish a site, send messages or change client accounts.'))
page('10 / Quality control','Ready to leave the studio?', '<div class="checklist">'+''.join('<p>□ '+x+'</p>' for x in ['Original logo, correct proportions and clear space','Brand palette and intended type roles','One clear message and one primary action','Date, venue, fee basis and destination checked','All CONFIRM and bracketed fields resolved','Sources and reporting dates on factual metrics','Photo context, rights and partner permissions checked','No invented impact, endorsement, rating or medical claim','Desktop, mobile and actual platform crops reviewed','Text remains readable at intended display size','Font rendering and final export dimensions checked','Editable source and final export saved together'])+'</div>'+note('The kit remains a working design extension until the brand guardian accepts it. Preserve confirmed identity assets and record changes.'))
# All actual CSS token values are visible in the reference, grouped and paginated.
for group,values in groups.items():
 rows=list(values.items())
 for i in range(0,len(rows),15):
  page('11 / Token reference',group.capitalize()+(' / continued' if i else '')+'.',table(['CSS variable','Value'],[[f'<code>--rwc-{k}</code>',f'<code>{esc(v)}</code>'] for k,v in rows[i:i+15]])+p(f'Source file: tokens/{group}.css. The rwc namespace carries existing project tokens forward. Semantic aliases keep UI meaning separate from the original logo hues.'))
page('11 / Developer handoff','A portable system.',panel('Use the CSS','<pre>&lt;link rel="stylesheet" href="styles.css"&gt;\n\n&lt;button class="rwc-btn" type="button"&gt;\n  View event details\n&lt;/button&gt;</pre>')+grid(panel('Change the system',p('Edit semantic values in tokens/*.css for consumption. For a reproducible full rebuild, update the matching token definitions in tools/build_kit.py and regenerate.')),panel('Extend a template',p('Duplicate the family and supply new content fields. Set canvas dimensions and safe zones in the platform configuration; recompose if the ratio changes.')))+p('JSON exports support tooling. DTCG-style output preserves complex CSS expressions as strings; an importer may need to map these. The component HTML has no framework dependency. Forms and buttons are specimens, with no backend services attached.')+note('HTML/SVG layouts stay editable. A raster photo or logo remains a raster asset inside the layout; the surrounding text, panels and geometry remain native elements.'))
page('12 / Closing','Built to bring people together.',f'<div class="closing-logo"><img src="{logo}" alt="Red White and Clix"></div><p class="closing-line">One Community.<br>One Mission.</p><p>Red White and Clix · Design System · Edition 1.0</p><p>Prepared by BlakSheep Creative<br>September 21, 2026</p>','closing')
reportcss='''
@page{size:Letter;margin:0}html{scroll-behavior:smooth}body{background:#D1D5DB;color:#111827;margin:0;font:15px/1.5 "Space Grotesk",Arial,sans-serif}*{box-sizing:border-box}.toolbar{position:sticky;top:0;z-index:30;background:#111827;color:white;padding:12px 24px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}.toolbar a,.toolbar button{color:white;background:#0050B3;border:0;border-radius:6px;padding:10px 16px;text-decoration:none;font:600 14px "Space Grotesk";cursor:pointer}.toolbar .brand{margin-right:auto}.sheet{width:816px;height:1056px;background:white;margin:24px auto;position:relative;padding:62px 48px 58px;break-after:page;overflow:hidden}.sheet:last-child{break-after:auto}.running{position:absolute;left:48px;right:48px;top:24px;display:flex;justify-content:space-between;font-size:8px;font-weight:700;letter-spacing:1.4px;text-transform:uppercase}.folio{position:absolute;bottom:24px;left:48px;right:48px;border-top:2px solid #0072FF;padding-top:10px;display:flex;justify-content:space-between;font-size:9px}.kicker{color:#0050B3;text-transform:uppercase;letter-spacing:2px;font-size:11px;font-weight:700;margin-bottom:14px}.sheet h1{font:400 40px/1.1 "Archivo Black";letter-spacing:-1.3px;margin:0 0 26px}.sheet h3{font:700 17px/1.25 "Space Grotesk";margin:0 0 10px}.sheet p{margin:12px 0}.grid,.component-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:18px 0}.panel{background:#F5F7FA;border:1px solid #D1D5DB;padding:20px;border-radius:8px}.panel p:first-of-type{margin-top:0}.panel p:last-child{margin-bottom:0}.note{border-left:4px solid #0050B3;padding:14px 18px;background:#F5F7FA;font-size:13px;margin-top:22px}.sheet table{width:100%;border-collapse:collapse;margin:18px 0;font-size:13px}.sheet th,.sheet td{text-align:left;vertical-align:top;border-bottom:1px solid #D1D5DB;padding:11px 10px}.sheet th{background:#111827;color:white;font-weight:600}.sheet td:first-child{font-weight:600}.sheet code{font:11px/1.4 monospace;overflow-wrap:anywhere}.sheet pre{font:13px/1.7 monospace;white-space:pre-wrap}.cover{background:#111827;color:white;padding-top:100px}.cover .kicker,.cover h1{display:none}.cover-brand{display:flex;gap:28px;align-items:center;font-weight:700;letter-spacing:2px;font-size:16px}.cover-brand img{width:180px;height:180px}.cover-brand span{font-weight:400;font-size:14px;letter-spacing:0}.cover-title{font:400 61px/1.06 "Archivo Black";letter-spacing:-2px;margin-top:92px}.cover-intro{font-size:20px;max-width:590px;line-height:1.6}.cover-bottom{margin-top:100px;font-size:14px}.cover-bottom strong{color:#FFFFFF;letter-spacing:2px}.cover .folio,.closing .folio{border-color:#0072FF}.cover .running,.closing .running{color:#FFFFFF}.logo-stage{background:#111827;display:flex;justify-content:center;padding:28px}.logo-stage img{width:290px;height:290px}.clearspace{background:repeating-linear-gradient(45deg,#F5F7FA,#F5F7FA 8px,#D1D5DB 8px,#D1D5DB 9px);padding:30px;width:360px;margin:0 auto 24px}.clearspace img{display:block;width:300px;height:300px}.avatar-row{display:flex;align-items:center;gap:20px;margin-top:28px}.avatar-row div{display:flex;flex-direction:column;gap:8px;align-items:center;font-size:12px}.swatches{display:flex;gap:12px;margin:24px 0}.swatches>div{flex:1;min-width:0}.swatches div div{height:130px;border-radius:6px}.swatches strong,.swatches code{display:block;font-size:12px;margin-top:8px}.type-display{font:400 38px "Archivo Black";margin-top:24px}.type-sample{font:400 55px/1.1 "Archivo Black";color:#0050B3}.type-body{font:700 28px "Space Grotesk";margin-top:35px}.type-body-sample{font-size:25px}.spacing-demo{display:grid;gap:12px}.spacing-demo>div{display:flex;gap:20px;align-items:center}.spacing-demo span{width:52px;font-size:13px}.spacing-demo i{display:block;height:18px;background:#0050B3}.component-grid{gap:22px}.component-spec{border-top:3px solid #0050B3;padding-top:12px;min-width:0}.component-live{font-size:13px;line-height:1.4;min-height:130px}.component-live .rwc-card{padding:16px}.component-live .rwc-card h3{font-size:18px}.component-live .rwc-btn{font-size:12px;padding:8px 10px;min-height:36px}.component-live .rwc-grid{gap:12px}.component-live .rwc-meta,.component-live .rwc-source,.component-live .rwc-badge{font-size:11px}.component-live .rwc-field{font-size:13px}.component-live .rwc-field small{font-size:11px}.component-live .rwc-table td,.component-live .rwc-table th{font-size:11px;padding:8px}.component-live .rwc-nav{padding:14px;gap:12px;flex-wrap:wrap}.component-live .rwc-cta{padding:18px}.component-live .rwc-photo{height:130px}.component-live .rwc-stat{font-size:30px}.component-live .rwc-skeleton{padding:18px}.spec-desc{font-size:12px;line-height:1.45}.photo-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}.photo-grid figure{margin:0}.photo-grid img{width:100%;height:220px;object-fit:cover}.photo-grid figcaption{font-size:11px}.icon-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}.icon-grid div{display:flex;align-items:center;flex-direction:column;gap:7px}.icon-grid small{font-size:9px}.specimen{margin:0;min-width:0}.art{display:flex;justify-content:center;align-items:center;background:#F5F7FA;padding:8px;border:1px solid #D1D5DB}.art>svg{display:block;width:100%;height:100%;object-fit:contain}.specimen figcaption{font-size:11px;font-weight:600;margin:7px 0 12px}.carousel-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.checklist p{border-bottom:1px solid #D1D5DB;padding:9px;font-size:15px}.closing{background:#111827;color:white;text-align:center}.closing .kicker,.closing h1{display:none}.closing-logo{margin:95px auto 50px}.closing-logo img{width:260px;height:260px}.closing-line{font:400 46px/1.15 "Archivo Black"}.sheet a{color:#0050B3}.sheet.cover a,.sheet.closing a{color:white}@media print{body{background:white}.toolbar{display:none}.sheet{margin:0;box-shadow:none}*{-webkit-print-color-adjust:exact;print-color-adjust:exact}}@media screen and (max-width:840px){.sheet{margin:16px 0;transform-origin:top left}.toolbar{position:relative}body{overflow-x:auto}}
'''
css=''.join((K/f'tokens/{x}.css').read_text() for x in ['colors','typography','spacing','effects','social'])+(K/'components/components.css').read_text()+reportcss
sheets=''.join(f'<article class="sheet {x["class"]}" id="page-{i+1}"><header class="running"><span>Red White and Clix / Comprehensive design system</span><span>BlakSheep Creative</span></header><div class="page-content"><div class="kicker">{x["section"]}</div><h1>{esc(x["title"])}</h1>{x["body"]}</div><footer class="folio"><span>Working brand system · September 2026</span><span>EDITION 1.0 / {i+1:02}</span></footer></article>' for i,x in enumerate(P))
put('index.html','<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Red White and Clix — Complete Design System</title><style>'+fonts+css+'</style></head><body><nav class="toolbar" aria-label="Document tools"><strong class="brand">Red White and Clix / Design system</strong><button onclick="window.print()">Print / Save PDF</button><a href="exports/Red White and Clix Design System.pdf" download>Download PDF</a><a href="template-studio.html">Open template editor</a></nav><main>'+sheets+'</main></body></html>')
js('exports/document-index.json',[{'page':i+1,'section':x['section'],'title':x['title']} for i,x in enumerate(P)])
print(f'Built reference: {len(P)} pages; {len(C)} components; {len(T)} templates; {len(flat)} tokens')
# The editor embeds its catalog and fonts, so file:// use requires no server or external requests.
studio_css='''*{box-sizing:border-box}body{margin:0;background:#F5F7FA;color:#111827;font:15px/1.5 "Space Grotesk",Arial}header{background:#111827;color:white;padding:20px 28px;display:flex;justify-content:space-between;align-items:center;gap:20px}header a{color:white}h1{font:400 24px "Archivo Black";margin:0}main{display:grid;grid-template-columns:320px 1fr;min-height:calc(100vh - 80px)}aside{background:white;border-right:1px solid #D1D5DB;padding:24px;max-height:calc(100vh - 80px);overflow:auto;position:sticky;top:0}label{display:grid;gap:6px;margin:12px 0;font-weight:600}select,input,textarea,button{font:inherit;min-height:44px;border:1px solid #111827;border-radius:6px;padding:10px;width:100%;background:white}button{background:#B91C1C;color:white;border:0;font-weight:700;cursor:pointer}.secondary{background:#0050B3}button:focus-visible,a:focus-visible,input:focus-visible,textarea:focus-visible,select:focus-visible{outline:3px solid #0050B3;outline-offset:3px}.exports{display:grid;grid-template-columns:1fr 1fr;gap:8px}section{padding:24px;min-width:0}.preview{background:#D1D5DB;padding:24px;display:flex;justify-content:center;min-height:480px}.preview svg{max-width:100%;height:auto;max-height:78vh;display:block}.help{font-size:13px;color:#111827}.notice{border-left:4px solid #0050B3;background:#F5F7FA;padding:12px;font-size:13px}.field-list label{font-size:12px}.field-list textarea{font-size:14px;min-height:72px}#status{font-weight:600;margin:12px 0}#guides-label{display:flex;align-items:center;gap:10px}#guides{width:20px;min-height:20px}#dirty{font-size:12px} @media(max-width:780px){main{grid-template-columns:1fr}aside{position:static;max-height:none;border-right:0}.preview svg{max-height:65vh}header{flex-wrap:wrap}}'''
studio_js=r'''
const catalog=CATALOG;
const fontCSS=FONT_CSS;
const family=document.getElementById('template');
const filter=document.getElementById('filter');
const preview=document.getElementById('preview');
const fields=document.getElementById('fields');
const status=document.getElementById('status');
let current,dirty=false;
const canvas=document.createElement('canvas'),ctx=canvas.getContext('2d');
function textOf(el){return [...el.querySelectorAll('tspan')].map(x=>x.textContent).join(' ')}
function fillOptions(){
 const q=filter.value.toLowerCase();family.innerHTML='';
 catalog.filter(t=>(t.title+' '+t.category+' '+t.format).toLowerCase().includes(q)).forEach(t=>{const o=document.createElement('option');o.value=t.id;o.textContent=t.title;family.append(o)});
 if(family.options.length)render(family.value);else{preview.textContent='No matching templates.';fields.innerHTML='';current=null;status.textContent='No matching templates.'}
}
function setDirty(v){dirty=v;document.getElementById('dirty').textContent=v?'Unsaved changes — download SVG before switching.':'Master loaded. Edits stay here until you download.'}
function render(id){
 current=catalog.find(t=>t.id===id);preview.innerHTML=current.svg;
 document.getElementById('template-title').textContent=current.title;
 const svg=preview.querySelector('svg');svg.querySelector('style').textContent=fontCSS;
 fields.innerHTML='';document.getElementById('guides').checked=false;
 svg.querySelectorAll('text[data-editable]').forEach((el,i)=>{
  const label=document.createElement('label');label.textContent=el.id.replaceAll('-',' ');
  const input=document.createElement('textarea');input.value=textOf(el);input.dataset.target=el.id;
  const x=el.getAttribute('x'),size=Number(el.getAttribute('font-size'));
  const width=Number(el.dataset.width||Math.min(Number(svg.getAttribute('width'))-Number(x)-64,900));
  const originalLines=el.querySelectorAll('tspan').length;
  input.addEventListener('input',()=>{
   const font=el.getAttribute('font-family');ctx.font=`${el.getAttribute('font-weight')} ${size}px "${font}"`;
   const words=input.value.trim().split(/\s+/);let rows=[],line='';
   for(const word of words){const candidate=line?line+' '+word:word;if(line&&ctx.measureText(candidate).width>width){rows.push(line);line=word}else{line=candidate}}rows.push(line);
   el.replaceChildren();rows.forEach((r,j)=>{const t=document.createElementNS('http://www.w3.org/2000/svg','tspan');t.setAttribute('x',x);t.setAttribute('dy',j?size*(font==='Archivo Black'?1.12:1.4):0);t.textContent=r;el.append(t)});
   setDirty(true);status.textContent=rows.length>originalLines?'Copy uses more lines than the master. Review nearby fields before exporting.':'Preview updated.';
  });label.append(input);fields.append(label);
 });
 setDirty(false);status.textContent='Canvas: '+svg.getAttribute('width')+' × '+svg.getAttribute('height')+' px';
}
function source(){const s=preview.querySelector('svg');if(!s)throw Error('Choose a template first.');const out=s.cloneNode(true);out.querySelector('#safe-guides')?.remove();out.querySelector('style').textContent=fontCSS;return new XMLSerializer().serializeToString(out)}
function download(blob,name){const u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(u),30000)}
filter.addEventListener('input',()=>{if(dirty){status.textContent='Save your SVG before filtering; changing the selection resets edits.'}fillOptions()});
family.addEventListener('change',()=>render(family.value));
document.getElementById('guides').addEventListener('change',e=>{const g=preview.querySelector('#safe-guides');if(g)g.style.display=e.target.checked?'block':'none';else status.textContent='This master has no crop overlay.'});
document.getElementById('reset').onclick=()=>render(current.id);
document.getElementById('svg-download').onclick=()=>{try{download(new Blob([source()],{type:'image/svg+xml'}),current.id+'-edited.svg');setDirty(false);status.textContent='Editable SVG downloaded.'}catch(e){status.textContent=e.message}};
async function raster(type){try{await document.fonts.ready;const svg=preview.querySelector('svg');const c=document.createElement('canvas');c.width=Number(svg.getAttribute('width'));c.height=Number(svg.getAttribute('height'));const context=c.getContext('2d');const img=new Image();const u=URL.createObjectURL(new Blob([source()],{type:'image/svg+xml'}));await new Promise((yes,no)=>{img.onload=yes;img.onerror=()=>no(new Error('The image could not be rendered.'));img.src=u});if(type==='jpeg'){context.fillStyle='white';context.fillRect(0,0,c.width,c.height)}context.drawImage(img,0,0);URL.revokeObjectURL(u);const b=await new Promise(r=>c.toBlob(r,'image/'+type,.94));if(!b)throw Error('Export failed.');download(b,current.id+'-edited.'+(type==='jpeg'?'jpg':'png'));status.textContent=`Downloaded ${c.width} × ${c.height} ${type.toUpperCase()}.`;}catch(e){status.textContent='Export error: '+e.message}}
document.getElementById('png-download').onclick=()=>raster('png');document.getElementById('jpg-download').onclick=()=>raster('jpeg');
document.getElementById('pdf-download').onclick=()=>{try{const s=preview.querySelector('svg'),w=s.getAttribute('width'),h=s.getAttribute('height'),win=window.open('','_blank');if(!win)throw Error('Allow the print window for this local file.');win.document.write('<!doctype html><html><head><title>'+current.title+'</title><style>'+fontCSS+'@page{size:'+w+'px '+h+'px;margin:0}body{margin:0}svg{display:block;width:100%;height:auto}*{print-color-adjust:exact;-webkit-print-color-adjust:exact}</style></head><body>'+source()+'</body></html>');win.document.close();win.document.fonts.ready.then(()=>setTimeout(()=>win.print(),700));}catch(e){status.textContent=e.message}};
window.addEventListener('beforeunload',e=>{if(dirty){e.preventDefault();e.returnValue=''}});
fillOptions();
'''.replace('CATALOG',json.dumps(T,ensure_ascii=False).replace('</',r'<\/')).replace('FONT_CSS',json.dumps(fonts))
# Fix raw-string regex: JavaScript needs a single slash escape in the regex literal.
studio_js=studio_js.replace(r'/\\s+/',r'/\s+/')
put('template-studio.html','<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>RWC Template Studio</title><style>'+fonts+studio_css+'</style></head><body><header><h1>Red White and Clix / Template studio</h1><a href="index.html">Open design system</a></header><main><aside><label>Filter templates<input id="filter" type="search" placeholder="Try sponsor, chart, story…"></label><label>Choose a master<select id="template"></select></label><p class="notice">Edit the fields below. Keep copy close to the master’s length and inspect the preview. Confirmation fields must be resolved before publication.</p><div class="exports"><button id="svg-download">Save SVG</button><button id="png-download">Save PNG</button><button id="jpg-download">Save JPG</button><button id="pdf-download">Print / PDF</button></div><p id="dirty"></p><label id="guides-label"><input id="guides" type="checkbox">Show safe-area guide</label><button id="reset" class="secondary">Reset to master</button><div id="fields" class="field-list"></div><p class="help">Fonts and logo are embedded. SVGs retain editable text and shapes. Charts are schematic; calculate geometry from verified data before using them as reports.</p></aside><section><h2 id="template-title"></h2><p id="status" role="status" aria-live="polite"></p><div id="preview" class="preview"></div><p class="help">Guide overlays are omitted from exports. Upload crop previews are the final check for a particular platform. Reopening or switching a master resets unsaved edits.</p></section></main><script>'+studio_js+'</script></body></html>')
