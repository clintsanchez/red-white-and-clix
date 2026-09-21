import requests, json, hashlib, re, io
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from PIL import Image
import xml.etree.ElementTree as ET

ROOT=Path('/Users/clintsanchez/Documents/Claude/Projects/Red-White-and-Clix')
REF=ROOT/'99-Reference/site-snapshot'
OUT=Path('/Users/clintsanchez/pCloud Drive/Documents/BlakSheep Creative/Clients/Red White and Clix/05-Photos/site-pull')
REF.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
base='https://www.redwhiteandclix.org/'
xml=Path('/private/tmp/rwc-onboarding/sitemap.xml').read_text()
tree=ET.fromstring(xml);ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','i':'http://www.google.com/schemas/sitemap-image/1.1'}
urls=[n.text for n in tree.findall('s:url/s:loc',ns)]
assets={};pages=[]
def add(u,page,alt=''):
    u=urljoin(base,u)
    if 'images.squarespace-cdn.com/' not in u and 'static1.squarespace.com/' not in u:return
    u=u.split('?')[0]
    v=assets.setdefault(u,{'source_url':u,'pages':[],'alt_text':[],'provenance':'SITE-DERIVED'})
    if page not in v['pages']:v['pages'].append(page)
    if alt and alt not in v['alt_text']:v['alt_text'].append(alt)
for el in tree.findall('s:url',ns):
    page=el.find('s:loc',ns).text
    for n in el.findall('i:image/i:loc',ns):add(n.text,page)
def read(url):
    try:
        r=requests.get(url,timeout=35);r.raise_for_status();s=BeautifulSoup(r.text,'html.parser')
        slug=re.sub('[^a-zA-Z0-9_-]+','-',urlsplit(url).path.strip('/')) or 'home'
        links=sorted(set(urljoin(url,a['href']) for a in s.select('a[href]')))
        imgs=[(i.get('data-src') or i.get('src'),i.get('alt','')) for i in s.select('img')]
        for n in s.select('script,style,noscript'):n.decompose()
        text=s.get_text('\n',strip=True)
        (REF/(slug+'.txt')).write_text(text)
        return {'url':url,'title':s.title.get_text() if s.title else '', 'snapshot':slug+'.txt','links':links,'images':imgs,'status':r.status_code}
    except Exception as e:return {'url':url,'error':str(e)}
with ThreadPoolExecutor(max_workers=5) as pool:
    for p in pool.map(read,urls):
        for u,alt in p.pop('images',[]):
            if u:add(u,p['url'],alt)
        pages.append(p)
(REF/'pages.json').write_text(json.dumps(pages,indent=2))
def download(item):
    u,meta=item
    try:
        r=requests.get(u,timeout=45);r.raise_for_status();im=Image.open(io.BytesIO(r.content));im.load()
        name=hashlib.sha256(u.encode()).hexdigest()[:10]+'-'+re.sub('[^a-zA-Z0-9._-]+','-',unquote(urlsplit(u).path.rsplit('/',1)[-1]))[:140]
        (OUT/name).write_bytes(r.content)
        return dict(meta,file=name,bytes=len(r.content),width=im.width,height=im.height,sha256=hashlib.sha256(r.content).hexdigest(),status='downloaded')
    except Exception as e:return dict(meta,status='failed',error=str(e))
with ThreadPoolExecutor(max_workers=5) as pool:manifest=list(pool.map(download,assets.items()))
(OUT/'MANIFEST.json').write_text(json.dumps({'retrieved':'2026-09-21','assets':manifest},indent=2))
(ROOT/'06-Reports/site-assets-manifest.json').write_text(json.dumps({'retrieved':'2026-09-21','asset_root':str(OUT),'assets':manifest},indent=2))
print(json.dumps({'pages':len(pages),'assets':len(manifest),'downloaded':sum(a['status']=='downloaded' for a in manifest),'total_bytes':sum(a.get('bytes',0) for a in manifest),'links':sorted(set(l for p in pages for l in p.get('links',[]) if any(t in l for t in ['facebook','instagram','linkedin','youtube','tiktok','twitter','hcunits','printify'])))}))
