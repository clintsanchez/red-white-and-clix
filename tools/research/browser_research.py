import json
from pathlib import Path
from playwright.sync_api import sync_playwright

out=Path('/private/tmp/rwc-onboarding/browser');out.mkdir(exist_ok=True)
targets={
 'facebook':'https://www.facebook.com/p/Red-White-and-Clix-61570114731358/',
 'google-business':'https://share.google/Zggq1t2iJ2iMra02T',
 'candid':'https://app.candid.org/profile/16594633/red-white-and-clix-inc-41-4723161',
 'printify':'https://red-white-and-clix.printify.me/products',
}
with sync_playwright() as p:
 b=p.chromium.launch(headless=True)
 context=b.new_context(viewport={'width':1440,'height':1050})
 for name,url in targets.items():
  page=context.new_page()
  try:
   page.goto(url,wait_until='domcontentloaded',timeout=35000)
   page.wait_for_timeout(2000)
   text=page.locator('body').inner_text(timeout=10000)
   links=page.locator('a[href]').evaluate_all('(els)=>els.map(e=>({text:e.innerText,url:e.href}))')
   images=page.locator('img').evaluate_all('(els)=>els.map(e=>({url:e.currentSrc||e.src,alt:e.alt,width:e.naturalWidth,height:e.naturalHeight}))')
   (out/(name+'.json')).write_text(json.dumps({'url':page.url,'text':text,'links':links,'images':images},indent=2))
   page.screenshot(path=str(out/(name+'.png')))
   print(name,page.url,text[:11000],flush=True)
  except Exception as e:print(name,'ERROR',str(e),flush=True)
  page.close()
 b.close()
