from pathlib import Path
from PIL import Image
import vtracer,xml.etree.ElementTree as ET,json,shutil
K=Path(__file__).resolve().parents[1];R=K.parents[1]
for d in ['svg','png','pdf','source','review']:(K/d).mkdir(exist_ok=True)
src=R/'brand/red-white-and-clix-logo.png'
if not src.exists(): src=K/'source/original-logo.png'
im=Image.open(src).convert('RGBA');w,h=im.size
if src.resolve() != (K/'source/original-logo.png').resolve(): shutil.copy2(src,K/'source/original-logo.png')
palette=[(0,0,0),(255,0,0),(255,255,255),(0,114,255)]
pixels=list(im.getdata());groups=[];solid=[]
for r,g,b,a in pixels:
 solid.append(a>=128)
 groups.append(-1 if a<128 else (1 if r>100 and r>g*1.8 and r>b*1.8 else (3 if b>100 and b>r*1.8 and b>g*1.3 else (2 if (r+g+b)/3>127 else 0))))
NS='http://www.w3.org/2000/svg'
def trace(name,bits):
 mask=Image.new('L',(w,h));mask.putdata([0 if b else 255 for b in bits]);mask.save(K/'source'/f'{name}-mask.png')
 target=K/'source'/f'{name}-trace.svg'
 vtracer.convert_image_to_svg_py(str(K/'source'/f'{name}-mask.png'),str(target),colormode='binary',mode='spline',filter_speckle=2,corner_threshold=60,length_threshold=2.5,max_iterations=15,splice_threshold=45,path_precision=3)
 root=ET.parse(target).getroot();paths=[]
 for el in root:
  if el.tag.endswith('path'):
   attr=' '.join(f'{k}="{v}"' for k,v in el.attrib.items() if k!='fill')
   paths.append('<path '+attr+'/>')
 return ''.join(paths)
shape=trace('silhouette',solid)
red=trace('red',[x==1 for x in groups]);white=trace('white',[x==2 for x in groups]);blue=trace('blue',[x==3 for x in groups])
# A single-ink dial uses the colored/white word shapes as knockouts.
letter_bits=[x in [1,2,3] for x in groups]
letter=trace('all-letterforms',letter_bits)
ink=trace('single-ink',[a and not b for a,b in zip(solid,letter_bits)])
def group(id,color,body):return f'<g id="{id}" fill="{color}">{body}</g>'
full=group('dial','#000000',shape)+group('red-word','#FF0000',red)+group('white-word-and-ampersand','#FFFFFF',white)+group('clix-word','#0072FF',blue)
def svg(body,title,vb='0 0 700 700'):
 ww,hh=vb.split()[2:];return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{ww}" height="{hh}" role="img" aria-label="{title}"><title>{title}</title><desc>Vector paths traced from the supplied 700px Red White and Clix logo. No embedded raster image and no font dependency. Working artwork for review.</desc>{body}</svg>'
V={}
def add(name,title,body,vb='0 0 700 700',bg='white'):
 s=svg(body,title,vb);(K/'svg'/f'{name}.svg').write_text(s);V[name]={'title':title,'file':f'svg/{name}.svg','background':bg}
add('rwc-primary-full-color','Primary / full color',full)
add('rwc-primary-white-outline','Primary / white outline',f'<g fill="none" stroke="#FFFFFF" stroke-width="12" stroke-linejoin="round">{shape}</g>'+full,'-10 -10 720 720','#111827')
add('rwc-primary-black-outline','Primary / black outline',f'<g fill="none" stroke="#000000" stroke-width="10" stroke-linejoin="round">{shape}</g>'+full,'-10 -10 720 720')
add('rwc-single-color-black','Single color / black',group('dial-and-memorial','#000000',ink))
add('rwc-single-color-white','Single color / white',group('dial-and-memorial','#FFFFFF',ink),bg='#111827')
add('rwc-letterforms-black','Letterforms only / black — proposed',group('letterforms','#000000',letter))
add('rwc-letterforms-white','Letterforms only / white — proposed',group('letterforms','#FFFFFF',letter),bg='#111827')
# Wide arrangement uses the actual traced letterforms, not replacement typography.
# Preserve internal letter angles and memorial shape; separate only the three source rows.
rows=[]
for name,color,lo,hi in [('red','#FF0000',40,238),('white','#111827',260,488),('clix','#0072FF',475,665)]:
 bits=[grp=={'red':1,'white':2,'clix':3}[name] and lo<=i//w<=hi for i,grp in enumerate(groups)]
 rows.append(trace('wide-'+name,bits))
wide=group('red-word','#FF0000',f'<g transform="translate(-95,-38)">{rows[0]}</g>')+group('white-word-and-ampersand','#111827',f'<g transform="translate(420,-248)">{rows[1]}</g>')+group('clix-word','#0072FF',f'<g transform="translate(930,-472)">{rows[2]}</g>')
# Width fits the original row extents after their translations.
add('rwc-wide-wordmark','Wide wordmark — proposed arrangement',wide,'0 0 1510 260')
widewhite=wide.replace('fill="#111827"','fill="#FFFFFF"')
add('rwc-wide-wordmark-on-dark','Wide wordmark / on dark — proposed',widewhite,'0 0 1510 260','#111827')
(K/'manifest.json').write_text(json.dumps({'source':'source/original-logo.png','method':'Fixed-palette classification and spline tracing; all delivered SVG artwork consists of path geometry.','variants':V},indent=2))
print('Created',len(V),'vector variants; primary path count:',full.count('<path'))
