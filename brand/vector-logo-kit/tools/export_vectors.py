from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image
import asyncio,json,base64,re,xml.etree.ElementTree as ET
K=Path(__file__).resolve().parents[1]
M=json.loads((K/'manifest.json').read_text());V=M['variants']
def inline(n):return (K/V[n]['file']).read_text()
def card(n):
 v=V[n];return f'<figure><div class="art" style="background:{v["background"]}">{inline(n)}</div><figcaption>{v["title"]}<br><a href="{v["file"]}" download>SVG</a> · <a href="pdf/{n}.pdf" download>PDF</a> · <a href="png/{n}-2400.png" download>PNG</a></figcaption></figure>'
orig=base64.b64encode((K/'source/original-logo.png').read_bytes()).decode()
css='''@page{size:Letter;margin:0}*{box-sizing:border-box}body{margin:0;background:#e5e7eb;color:#111827;font:15px/1.5 Arial,sans-serif}nav{padding:16px 24px;background:#111827;color:white;display:flex;justify-content:space-between;align-items:center}nav button{padding:10px 16px;background:#0050B3;color:white;border:0;border-radius:6px;cursor:pointer}.page{width:816px;height:1056px;margin:24px auto;padding:48px;background:white;position:relative;break-after:page}.page:last-child{break-after:auto}h1{font-size:40px;letter-spacing:-1.3px;line-height:1.1;margin:16px 0 20px}h2{font-size:26px;margin:0 0 20px}.eyebrow{font-size:11px;letter-spacing:2px;color:#0050B3;font-weight:bold;text-transform:uppercase}.grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0}.art{height:195px;display:flex;align-items:center;justify-content:center;padding:20px;border:1px solid #D1D5DB}.art svg,.art img{width:100%;height:100%;object-fit:contain}figcaption{font-size:12px;margin:8px 0 20px}a{color:#0050B3}footer{position:absolute;bottom:26px;left:48px;right:48px;border-top:2px solid #0072FF;padding-top:10px;font-size:10px;display:flex;justify-content:space-between}.large .art{height:340px}.wide .art{height:150px}.note{border-left:4px solid #0050B3;padding:16px;background:#F5F7FA;margin:22px 0;font-size:14px}table{width:100%;border-collapse:collapse;font-size:13px}td,th{padding:10px;text-align:left;border-bottom:1px solid #D1D5DB}th{background:#111827;color:white}@media print{nav{display:none}.page{margin:0}body{background:white}*{print-color-adjust:exact;-webkit-print-color-adjust:exact}}
'''
content=f'''<section class="page"><div class="eyebrow">Red White and Clix / Vector identity</div><h1>The original mark.<br>Now scalable.</h1><p>Faithful path tracing of the supplied 700 × 700 artwork, with clearly labeled production and layout variants.</p><div class="grid large"><figure><div class="art"><img src="data:image/png;base64,{orig}" alt="Supplied raster logo"></div><figcaption>Original client-supplied PNG</figcaption></figure>{card('rwc-primary-full-color')}</div><div class="note">Every delivered SVG uses editable vector paths. There are no embedded raster images and no font dependencies. Fine memorial details are traced from the original; vectorization preserves the source’s existing irregularities.</div><table><tr><th>File type</th><th>Use</th></tr><tr><td>SVG</td><td>Editable master for web and vector-design software.</td></tr><tr><td>PDF</td><td>Vector artwork for placement in print layouts.</td></tr><tr><td>PNG</td><td>Transparent 2400px export for everyday use.</td></tr></table><footer><span>BlakSheep Creative · September 21, 2026</span><span>01 / Working artwork</span></footer></section>'''
content+='<section class="page"><div class="eyebrow">Production variants</div><h1>Light. Dark. Single ink.</h1><div class="grid">'+''.join(card(n) for n in ['rwc-primary-white-outline','rwc-primary-black-outline','rwc-single-color-black','rwc-single-color-white','rwc-letterforms-black','rwc-letterforms-white'])+'</div><footer><span>Background panels are preview aids, not part of transparent artwork.</span><span>02 / Variants for review</span></footer></section>'
content+='<section class="page wide"><div class="eyebrow">Alternative arrangement</div><h1>A wider signature.</h1><p>The existing traced word shapes are arranged horizontally. The original letter angles and memorial cutout remain intact. These are proposed lockups, not replacements for the primary badge.</p>'+card('rwc-wide-wordmark')+card('rwc-wide-wordmark-on-dark')+'<div class="note">White artwork is transparent and may look blank against a white PDF viewer. Place it on a dark background in your design application. The gray/dark panels in this preview are not included in the SVG or transparent PNG files.</div><table><tr><th>Rule</th><th>Application</th></tr><tr><td>Primary identity</td><td>Use the full-color badge as the faithful source-matched version.</td></tr><tr><td>Clear space</td><td>Keep at least 10% of the mark width clear on every side.</td></tr><tr><td>Small use</td><td>Fine detail still needs size-specific review; no simplified favicon is claimed here.</td></tr><tr><td>Production</td><td>Approve variants before rollout. Confirm minimum line/detail sizes with print or embroidery vendors.</td></tr></table><footer><span>SVG source · Vector PDF · Transparent PNG</span><span>03 / Proposed wide lockups</span></footer></section>'
(K/'preview.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Red White and Clix — Vector Logo Variants</title><style>'+css+'</style><nav><strong>Red White and Clix / Logo variants</strong><button onclick="print()">Print / Save PDF</button></nav>'+content+'</html>')
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(channel='chrome');page=await b.new_page(viewport={'width':700,'height':700})
  for n,v in V.items():
   s=inline(n);root=ET.fromstring(s);vw=float(root.attrib['viewBox'].split()[2]);vh=float(root.attrib['viewBox'].split()[3]);height=round(2400*vh/vw)
   assert not any(el.tag.endswith(('image','text','foreignObject')) for el in root.iter())
   await page.set_content(f'<html><head><style>@page{{size:{vw}px {vh}px;margin:0}}body{{margin:0;background:transparent}}svg{{display:block;width:100vw;height:100vh}}*{{print-color-adjust:exact;-webkit-print-color-adjust:exact}}</style></head><body>{s}</body></html>')
   await page.set_viewport_size({'width':2400,'height':height})
   await page.screenshot(path=str(K/'png'/f'{n}-2400.png'),omit_background=True)
   await page.pdf(path=str(K/'pdf'/f'{n}.pdf'),print_background=True,prefer_css_page_size=True)
   if n=='rwc-primary-full-color':
    await page.set_viewport_size({'width':700,'height':700});await page.screenshot(path=str(K/'review/primary-render-700.png'),omit_background=True)
  await page.set_viewport_size({'width':1000,'height':1150})
  await page.goto((K/'preview.html').as_uri())
  for i in range(3):await page.locator('.page').nth(i).screenshot(path=str(K/f'review/preview-{i+1}.png'))
  await page.pdf(path=str(K/'Red White and Clix Logo Variants.pdf'),print_background=True,prefer_css_page_size=True)
  await b.close()
 # Render comparison at original resolution against a common white ground.
 a=Image.open(K/'source/original-logo.png').convert('RGBA');z=Image.open(K/'review/primary-render-700.png').convert('RGBA')
 def classify(px):
  r,g,b,alpha=px
  if alpha<128:return -1
  return 1 if r>100 and r>g*1.8 and r>b*1.8 else (3 if b>100 and b>r*1.8 and b>g*1.3 else (2 if (r+g+b)/3>127 else 0))
 ap=list(a.getdata());zp=list(z.getdata());different=sum(classify(x)!=classify(y) for x,y in zip(ap,zp))
 report={'variants':len(V),'vectorOnlySVGs':True,'classificationAgreementPercent':round(100*(1-different/(700*700)),3),'comparison':'Original versus vector render at 700px, brand-hue classification and alpha threshold 128. Boundary antialiasing differences count as mismatches.'}
 (K/'review/quality-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
asyncio.run(main())
