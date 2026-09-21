"""Public-page Playwright photo pull. Fresh context; no cookie/profile imports.
Only follows photo links exposed by the page. Stops at access challenges.
"""
import json,io,hashlib,re
from pathlib import Path
from urllib.parse import urlsplit,parse_qs
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path('/Users/clintsanchez/Documents/Claude/Projects/Red-White-and-Clix')
OUT=Path('/Users/clintsanchez/pCloud Drive/Documents/BlakSheep Creative/Clients/Red White and Clix/05-Photos/facebook-pull')
OUT.mkdir(parents=True,exist_ok=True)
source='https://www.facebook.com/p/Red-White-and-Clix-61570114731358/'
manifest=[];snapshots=[];seen=set();bodies={}
with sync_playwright() as p:
 b=p.chromium.launch(headless=True)
 context=b.new_context(viewport={'width':1440,'height':1100})
 page=context.new_page()
 def response(r):
  if 'scontent' in r.url and 'fbcdn.net' in r.url:
   try:
    if r.ok:bodies[r.url]=r.body()
   except Exception:pass
 # Fetch only image URLs observed in the rendered DOM using this browser context.
 def capture(url):
  try:
   page.goto(url,wait_until='domcontentloaded',timeout=30000)
   page.wait_for_timeout(3000)
   text=page.locator('body').inner_text(timeout=15000)
   snapshots.append({'url':page.url,'text':text})
   images=page.locator('img').evaluate_all('(els)=>els.map(e=>({url:e.currentSrc||e.src,alt:e.alt,width:e.naturalWidth,height:e.naturalHeight}))')
   for i in images:
    if 'scontent' not in i['url'] or max(i['width'],i['height'])<600:continue
    raw=bodies.get(i['url'])
    if not raw:
     try:
      r=context.request.get(i['url'],timeout=15000)
      if r.ok:raw=r.body()
     except Exception:pass
    if not raw:continue
    sha=hashlib.sha256(raw).hexdigest()
    if sha in seen:continue
    im=Image.open(io.BytesIO(raw));im.load();ext='png' if im.format=='PNG' else 'jpg' if im.format=='JPEG' else 'webp'
    name='fb-'+sha[:12]+'.'+ext;(OUT/name).write_bytes(raw);seen.add(sha)
    manifest.append({'file':name,'source_page':url,'source_url':i['url'],'alt_text':i['alt'],'width':im.width,'height':im.height,'bytes':len(raw),'sha256':sha,'provenance':'FACEBOOK-PUBLIC-DERIVED','rights':'Client page source; confirm reuse permissions for people and third-party artwork.'})
   links=page.locator('a[href]').evaluate_all('(els)=>els.map(e=>e.href)')
   print('CAPTURE',url,'assets',len(manifest),'text',text[:100],flush=True)
   return links,text
  except Exception as e:
   snapshots.append({'url':url,'error':str(e)});return [],''
 links,text=capture(source)
 if not links:
  prior=json.loads(Path('/private/tmp/rwc-onboarding/browser/facebook.json').read_text())
  links=[x['url'] for x in prior['links']]
 photos=next((u for u in links if 'sk=photos' in u),None)
 if photos:
  more,t=capture(photos)
  links+=more
  # Scroll only a publicly rendered photo grid; never dismiss a login gate.
  if 'photo/?fbid=' in '\n'.join(more):
   for _ in range(3):
    page.mouse.wheel(0,850);page.wait_for_timeout(1200)
    links+=page.locator('a[href]').evaluate_all('(els)=>els.map(e=>e.href)')
 urls={}
 for u in links:
  if '/photo/' in u and 'fbid=' in u:urls.setdefault(parse_qs(urlsplit(u).query)['fbid'][0],u)
 for u in list(urls.values())[:35]:
  _,text=capture(u)
  if 'temporarily blocked' in text.lower() or 'confirm you' in text.lower():break
 about=next((u for u in links if 'sk=about' in u),None)
 if about:capture(about)
 b.close()
(OUT/'MANIFEST.json').write_text(json.dumps({'retrieved':'2026-09-21','method':'Fresh public Playwright context; response bytes of publicly rendered images only','assets':manifest},indent=2))
(ROOT/'06-Reports/facebook-assets-manifest.json').write_text(json.dumps({'asset_root':str(OUT),'assets':manifest},indent=2))
(ROOT/'99-Reference/facebook-public-snapshots.json').write_text(json.dumps(snapshots,indent=2))
print('DONE',len(manifest),'assets')
