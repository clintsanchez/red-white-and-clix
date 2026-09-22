from pathlib import Path
import json, asyncio, re, sys
import pymupdf
from playwright.async_api import async_playwright
K=Path(__file__).resolve().parents[1]
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(channel='chrome',headless=True)
  page=await browser.new_page(viewport={'width':1100,'height':1200},device_scale_factor=1)
  errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  await page.goto((K/'index.html').as_uri(),wait_until='load')
  await page.evaluate('document.fonts.ready')
  report=await page.evaluate('''() => [...document.querySelectorAll('.sheet')].map((p,i)=>{const r=p.getBoundingClientRect(),c=p.querySelector('.page-content').getBoundingClientRect();return {page:i+1,title:p.querySelector('h1').textContent,bottom:c.bottom-r.top,overflow:c.bottom>r.bottom-48}})''')
  overflow=[r for r in report if r['overflow']]
  print('Reference overflow:',json.dumps(overflow),flush=True)
  (K/'exports/layout-check.json').write_text(json.dumps({'pages':report,'errors':errors},indent=2))
  for n in [1,4,7,10,14,17,25,32,43,49,57,66,77]:
   await page.locator('.sheet').nth(n-1).screenshot(path=str(K/f'exports/page-{n:02}.png'))
  await page.pdf(path=str(K/'exports/Red White and Clix Design System.pdf'),print_background=True,prefer_css_page_size=True)
  pdf_path=K/'exports/Red White and Clix Design System.pdf'
  d=pymupdf.open(pdf_path)
  index=json.loads((K/'exports/document-index.json').read_text())
  d.set_toc([[1,x['section']+' — '+x['title'],x['page']] for x in index])
  d.set_metadata({'title':'Red White and Clix — Complete Design System','author':'BlakSheep Creative','subject':'Brand foundations, components, social templates and design tokens','keywords':'Red White and Clix, brand kit, design system'})
  d.saveIncr();d.close()
  if '--reference-only' in sys.argv:
   await browser.close();return
  # Exercise local-file editor and actual downloadable exports.
  await page.goto((K/'template-studio.html').as_uri(),wait_until='load')
  await page.evaluate('document.fonts.ready')
  await page.locator('#template').select_option('save-date-square')
  field=page.locator('#fields textarea').first
  await field.fill('A place to play together.')
  await page.locator('#guides').check()
  async with page.expect_download() as dl:
   await page.locator('#svg-download').click()
  d=await dl.value;await d.save_as(str(K/'exports/editor-test.svg'))
  async with page.expect_download() as dl:
   await page.locator('#png-download').click()
  d=await dl.value;await d.save_as(str(K/'exports/editor-test.png'))
  await page.screenshot(path=str(K/'exports/template-studio-preview.png'),full_page=False)
  print('Editor export verified',flush=True)
  await page.set_viewport_size({'width':390,'height':844})
  await page.screenshot(path=str(K/'exports/template-studio-mobile.png'),full_page=False)
  # Verify all SVG text is inside each canvas and no text fields overlap.
  inv=json.loads((K/'templates/inventory.json').read_text())
  findings=[]
  out=K/'exports/template-previews';out.mkdir(exist_ok=True)
  for i,t in enumerate(inv):
   raw=(K/t['path']).read_text()
   await page.set_content('<!doctype html><html><head><style>body{margin:0}svg{display:block}</style></head><body>'+raw+'</body></html>')
   await page.evaluate('document.fonts.ready')
   results=await page.evaluate('''() => {const s=document.querySelector('svg'),w=s.viewBox.baseVal.width,h=s.viewBox.baseVal.height;const a=[...s.querySelectorAll('text')].map(e=>({id:e.id,text:e.textContent.slice(0,70),r:e.getBBox()})).map(e=>({...e,r:{x:e.r.x,y:e.r.y,w:e.r.width,h:e.r.height}}));let issues=[];for(const e of a){if(e.r.x<0||e.r.y<0||e.r.x+e.r.w>w+1||e.r.y+e.r.h>h+1)issues.push({kind:'outside',...e})}for(let i=0;i<a.length;i++)for(let j=i+1;j<a.length;j++){const u=a[i],v=a[j],x=Math.min(u.r.x+u.r.w,v.r.x+v.r.w)-Math.max(u.r.x,v.r.x),y=Math.min(u.r.y+u.r.h,v.r.y+v.r.h)-Math.max(u.r.y,v.r.y);if(x>2&&y>3)issues.push({kind:'text-overlap',a:u.text,b:v.text,x,y})}return {w,h,issues}}''')
   if results['issues']:findings.append({'id':t['id'],'issues':results['issues']})
   # Native-dimension PNG previews of all templates are included for convenience.
   await page.set_viewport_size({'width':int(results['w']),'height':int(results['h'])})
   await page.screenshot(path=str(out/(t['id']+'.png')),full_page=True)
   if i%40==0:print(f'Templates checked/exported: {i+1}/{len(inv)}',flush=True)
  (K/'exports/template-check.json').write_text(json.dumps(findings,indent=2))
  print('Template findings:',len(findings),'Browser errors:',errors,flush=True)
  await browser.close()
asyncio.run(main())
