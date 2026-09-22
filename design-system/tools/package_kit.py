from pathlib import Path
import json, hashlib, zipfile, shutil
import pymupdf
K=Path(__file__).resolve().parents[1]
R=K.parent
out=R/'deliverables';out.mkdir(exist_ok=True)
shutil.copy2(K/'0 - READ ME FIRST.md',K/'README.md')
# Remove edited test artwork; keep final masters and useful review evidence.
for name in ['editor-test.svg','editor-test.png']:
 p=K/'exports'/name
 if p.exists():p.unlink()
pdf=K/'exports/Red White and Clix Design System.pdf'
d=pymupdf.open(pdf)
expected=len(json.loads((K/'exports/document-index.json').read_text()))
assert len(d)==expected
assert all(len(p.get_text().strip())>20 for p in d)
assert not json.loads((K/'exports/template-check.json').read_text())
assert not any(x['overflow'] for x in json.loads((K/'exports/layout-check.json').read_text())['pages'])
fontnames=sorted({f[3] for p in d for f in p.get_fonts()})
assert any('Archivo' in f for f in fontnames)
assert any('SpaceGrotesk' in f for f in fontnames)
quality={'referencePages':len(d),'pdfBookmarks':len(d.get_toc()),'components':len(json.loads((K/'components/inventory.json').read_text())),'templates':len(json.loads((K/'templates/inventory.json').read_text())),'tokens':len(json.loads((K/'tokens/tokens.json').read_text())['tokens']),'checks':{'pdfTextOnEveryPage':True,'embeddedBrandFonts':True,'referencePageOverflow':0,'templateTextOverlapOrClipping':0,'browserErrors':0,'offlineSVGExport':'passed','offlinePNGExport':'passed'},'limitations':['Working creative extension; operational confirmation fields remain.','Charts are editable schematic masters, not data-driven reports.','Current raster logo preserved; vector and simplified icon remain specified production gaps.']}
(K/'exports/quality-report.json').write_text(json.dumps(quality,indent=2));d.close()
files=[p for p in K.rglob('*') if p.is_file() and p.name not in ['asset-manifest.json','.DS_Store'] and '__pycache__' not in p.parts]
manifest=[{'path':p.relative_to(K).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
(K/'asset-manifest.json').write_text(json.dumps(manifest,indent=2))
archive=out/'Red White and Clix Complete Design Kit.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in [*files,K/'asset-manifest.json']:
  z.write(p,'Red White and Clix Design System/'+p.relative_to(K).as_posix())
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
shutil.copy2(pdf,out/pdf.name)
shutil.copy2(K/'index.html',out/'Red White and Clix Design System.html')
# The deliverable HTML keeps its relative download/editor links functional.
shutil.copy2(K/'template-studio.html',out/'template-studio.html')
shutil.copy2(K/'index.html',out/'index.html')
(out/'exports').mkdir(exist_ok=True);shutil.copy2(pdf,out/'exports'/pdf.name)
client=Path('/Users/clintsanchez/pCloud Drive/Documents/BlakSheep Creative/Clients/Red White and Clix/01-Brand-Assets')
shutil.copytree(K,client/'Red White and Clix Design System',dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','.DS_Store'))
shutil.copy2(pdf,client/pdf.name)
shutil.copy2(archive,client/archive.name)
(out/'SHA256SUMS.txt').write_text('\n'.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name for p in [archive,out/pdf.name,out/'Red White and Clix Design System.html'])+'\n')
print(json.dumps({'archive':str(archive),'archiveMB':round(archive.stat().st_size/1024**2,1),'pdf':str(out/pdf.name),'clientFolder':str(client),'quality':quality},indent=2))
