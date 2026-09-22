from pathlib import Path
import asyncio,json
from urllib.parse import unquote,urlparse
from playwright.async_api import async_playwright
P=Path(__file__).resolve().parents[1]
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(channel='chrome');page=await b.new_page();errors=[];results=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  for width in [1440,768,390,320]:
   await page.set_viewport_size({'width':width,'height':1000})
   for file in ['index.html','events.html','about.html','donate.html','review.html']:
    await page.goto((P/file).as_uri());await page.evaluate('document.fonts.ready')
    result=await page.evaluate('''()=>({width:innerWidth,bodyWidth:document.documentElement.scrollWidth,h1:document.querySelectorAll('h1').length,brokenImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src),fonts:[...document.fonts].map(f=>({family:f.family,status:f.status})),links:[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href'))})''')
    assert result['bodyWidth']<=width,(file,width,result['bodyWidth'])
    assert result['h1']==1;assert not result['brokenImages']
    for link in result.pop('links'):
     if link.startswith(('https:','mailto:','tel:')):continue
     route,_,anchor=link.partition('#');target=P/route if route else P/file
     assert target.exists(),(file,link)
     if anchor:
      assert f'id="{anchor}"' in target.read_text(),(file,link)
    results.append({'page':file,**result})
    if width in [1440,390]:await page.screenshot(path=str(P/f'review/{file[:-5]}-{width}.png'),full_page=True)
   if width==390:
    await page.locator('.mobile-menu summary').click();assert await page.locator('.mobile-menu nav').is_visible()
    await page.locator('.mobile-menu nav a[href="events.html"]').click();assert page.url.endswith('events.html')
    assert await page.get_by_role('button',name='Registration link pending').count()==2
    assert await page.get_by_role('button',name='Registration link pending').first.is_disabled()
    await page.locator('.faq summary').first.click();assert await page.locator('.faq details').first.get_attribute('open') is not None
    await page.goto((P/'donate.html').as_uri());assert await page.get_by_role('button',name='Donation link pending').is_disabled()
  await page.set_viewport_size({'width':1440,'height':1000});await page.goto((P/'index.html').as_uri())
  await page.keyboard.press('Tab');assert await page.locator('.skip').evaluate('(el)=>el===document.activeElement')
  assert not errors,errors
  report={'checks':results,'browserErrors':errors,'localLinksAndAnchors':'passed','mobileMenu':'passed','faq':'passed','checkoutControls':'disabled as intended','keyboardSkipLink':'passed'}
  (P/'review/check-results.json').write_text(json.dumps(report,indent=2));print('PASS: 5 pages at 4 widths; local links/anchors, images, mobile navigation, FAQs, disabled checkout and keyboard skip link.')
  await b.close()
asyncio.run(main())
