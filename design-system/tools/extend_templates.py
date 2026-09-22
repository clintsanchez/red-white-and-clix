"""Extends the RWC template library with channel-specific canvases, reel covers and
profile images, reusing the repository's own generator (build_kit.py) so every new
master shares its layout engine, tokens, fonts and logo handling."""
import json, re
from pathlib import Path

G = Path(__file__).resolve().parents[2]  # repository root
KIT = G / 'design-system' / 'tools' / 'build_kit.py'
src = KIT.read_text().split('\n')
cut = next(i for i, l in enumerate(src) if l.startswith('T=[]'))
ns = {'__file__': str(KIT), '__name__': 'build_kit_prefix'}
exec('\n'.join(src[:cut]), ns)
g = ns
formats, spec, F, colors, logo, fonts = g['formats'], g['spec'], g['F'], g['colors'], g['logo'], g['fonts']
txt, rect, svgdoc, make_social, esc = g['txt'], g['rect'], g['svgdoc'], g['make_social'], g['esc']

OUT = G / 'design-system'
NEW = []  # inventory rows


def fam(i):
    return dict(next(f for f in F if f['id'] == i))


def save(id, title, fmt, svg):
    p = OUT / 'templates' / 'social' / f'{id}.svg'
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(svg.replace('<style>', '<style>' + fonts, 1))
    NEW.append({'id': id, 'title': title, 'category': 'social', 'format': fmt,
                'path': f'templates/social/{id}.svg', 'fields': []})


def resize(svg, w, h):
    """Output a composition at a channel size that shares the design canvas's ratio."""
    return re.sub(r'width="\d+" height="\d+" viewBox', f'width="{w}" height="{h}" viewBox', svg, count=1)


# 1. Channel canvases --------------------------------------------------------------
# (id, width, height, design master or None=compose natively, note)
channels = [
    ('instagram-landscape', 1080, 566, None, 'Instagram feed landscape (1.91:1).'),
    ('linkedin-landscape', 1200, 627, None, 'LinkedIn landscape post and link preview.'),
    ('x-landscape', 1280, 720, None, 'X landscape image (16:9).'),
    ('linkedin-square', 1200, 1200, 'square', 'LinkedIn square post; square composition output at 1200.'),
    ('linkedin-portrait', 720, 900, 'portrait', 'LinkedIn portrait post (4:5); portrait composition output at 720.'),
    ('x-portrait', 720, 1280, 'story', 'X portrait image (9:16); story composition output at 720.'),
    ('pinterest-square', 1000, 1000, 'square', 'Pinterest square pin; square composition output at 1000.'),
    ('pinterest-landscape', 800, 450, 'x-landscape', 'Pinterest landscape cover (16:9); composed at 1280 x 720.'),
    ('youtube-podcast', 1280, 1280, 'square', 'YouTube podcast / playlist thumbnail (1:1).'),
]
families = ['save-date', 'event-update', 'mission', 'impact', 'new-player', 'sponsor']
dark = {'mission'}
new_specs = []
for cid, w, h, master, note in channels:
    if master is None:
        formats[cid] = (w, h)
        spec.append({'id': cid, 'width': w, 'height': h, 'ratio': round(w / h, 3),
                     'safe_rect_xywh': [64, 64, w - 128, h - 128]})
    base = next(s for s in spec if s['id'] == (master or cid))
    k = w / base['width']
    safe = [round(v * k) for v in base['safe_rect_xywh']]
    new_specs.append({'id': cid, 'width': w, 'height': h, 'ratio': round(w / h, 3), 'safe_rect_xywh': safe,
                      'status': 'Editable production default; check platform preview before upload',
                      'source': 'Universal social template brief (channel list)', 'checked': None,
                      'crop': note + ' Keep text inside guide; verify mobile and desktop uploader crops.',
                      'design_master': master or cid})
    for fid in families:
        f = fam(fid)
        svg = make_social(f, master or cid, 'dark' if fid in dark else 'light')
        if master:
            svg = resize(svg, w, h)
        save(f'{fid}-{cid}', f'{f["title"]} / {cid}', cid, svg)

# 2. Reel / short-video covers -------------------------------------------------------
# One shared 1080 x 1920 master whose safe area clears the interface of Instagram Reels,
# Facebook Reels, TikTok and YouTube Shorts together, and stays inside the 3:4 profile-grid crop.
RW, RH = 1080, 1920
REEL_SAFE = [64, 250, 826, 1190]  # x, y, w, h  -> right edge 890 (190 px rail), bottom 1440 (480 px caption zone)
ui_zones = {  # conservative editable guides, drawn only in the guide layer
    'Top bar (account, close, audio)': [0, 0, 1080, 250],
    'Caption, audio and navigation': [0, 1440, 1080, 480],
    'Action rail (like, comment, share)': [890, 250, 190, 1190],
}
new_specs.append({'id': 'reel-cover', 'width': RW, 'height': RH, 'ratio': round(RW / RH, 3), 'safe_rect_xywh': REEL_SAFE,
                  'status': 'Editable production default; check platform preview before upload',
                  'source': 'Universal social template brief (video cover system)', 'checked': None,
                  'crop': 'Shared cover for Instagram Reels, Facebook Reels, TikTok and YouTube Shorts. Top 250 px, bottom 480 px and right 190 px are interface zones; the profile grid shows the centre 1080 x 1440 (3:4). Verify in each app before posting.',
                  'design_master': 'reel-cover', 'ui_zones': ui_zones})


def reel(f, theme='dark'):
    d = theme == 'dark'
    bg, ink = (colors['ink'], '#FFFFFF') if d else ('#FFFFFF', colors['ink'])
    x, y0, sw, sh = REEL_SAFE
    a = [rect(0, 0, RW, RH, bg), rect(0, 0, 16, RH, colors['logo-blue']), rect(16, 0, 8, RH, colors['logo-red'])]
    a.append(f'<image x="{x}" y="{y0 + 8}" width="150" height="150" href="{logo}"/>')
    a.append(txt('RED WHITE AND CLIX', x + 174, y0 + 92, 24, '#F5F7FA' if d else colors['ink'], sw - 174)[0])
    fh = g['fh']
    size = 112
    while size > 56 and max(fh.text_length(wd, fontsize=size) for wd in f['headline'].split()) > sw:
        size -= 4
    rows = g['lines'](f['headline'], sw, size, True)
    hh0 = len(rows) * size * 1.12
    bsz = 40
    brows = g['lines'](f['body'], sw, bsz) if f['body'] else []
    block = hh0 + (24 + len(brows) * bsz * 1.4 if brows else 0)
    top = y0 + 190 + max(0, (sh - 190 - 120 - block) / 2) + size
    head, hh = txt(f['headline'], x, top, size, ink, sw, True, 'headline', maxlines=6)
    a.append(head)
    if brows:
        body, bh = txt(f['body'], x, top - size + hh + 24 + bsz, bsz, ink, sw, False, 'body', maxlines=5)
        a.append(body)
    a.append(rect(x, y0 + sh - 64, 220, 12, colors['action'], None, 6))  # short action bar, not a button
    a.append(txt('redwhiteandclix.org', x, y0 + sh - 8, 30, ink, sw, id='website')[0])
    guides = ''.join(f'<rect x="{r[0]}" y="{r[1]}" width="{r[2]}" height="{r[3]}" fill="#B91C1C" fill-opacity="0.18"/>'
                     f'<text x="{r[0] + 24}" y="{r[1] + 44}" fill="{ink}" font-family="Space Grotesk" font-size="26">{esc(n)}</text>'
                     for n, r in ui_zones.items())
    guides += f'<rect x="{x}" y="{y0}" width="{sw}" height="{sh}" fill="none" stroke="#B91C1C" stroke-width="3" stroke-dasharray="14 10"/>'
    guides += f'<rect x="0" y="240" width="1080" height="1440" fill="none" stroke="#0072FF" stroke-width="3" stroke-dasharray="6 8"/>'
    a.append(f'<g id="safe-guides" style="display:none">{guides}</g>')
    return svgdoc(RW, RH, ''.join(a), 'Video cover / ' + f['title'])


reels = ['save-date', 'new-player', 'photo-recap', 'competition', 'event-update', 'founder']
for fid in reels:
    f = fam(fid)
    save(f'reel-cover-{fid}', f'Video cover / {f["title"]}', 'reel-cover', reel(f, 'light' if fid in ('event-update',) else 'dark'))
# guide specimen with the interface zones visible
guide = reel(fam('save-date')).replace('style="display:none"', '')
save('reel-cover-guide', 'Video cover / interface safe zones (guide)', 'reel-cover', guide)

# 3. Profile images -----------------------------------------------------------------
avatar = svgdoc(800, 800, rect(0, 0, 800, 800, '#000000') + f'<image x="144" y="144" width="512" height="512" href="{logo}"/>', 'Avatar primary')
profiles = [('instagram', 320), ('tiktok', 200), ('x', 400), ('linkedin', 400), ('pinterest', 280), ('youtube', 800), ('facebook', 320)]
for p, s in profiles:
    save(f'avatar-{p}', f'Avatar / {p} {s} px', 'avatar', resize(avatar, s, s))
    new_specs.append({'id': f'avatar-{p}', 'width': s, 'height': s, 'ratio': 1.0,
                      'safe_rect_xywh': [round(144 * s / 800)] * 2 + [round(512 * s / 800)] * 2,
                      'status': 'Editable production default; check platform preview before upload',
                      'source': 'Universal social template brief (profile images)', 'checked': None,
                      'crop': 'Circular crop on most platforms; the mark stays inside the central safe circle.',
                      'design_master': 'avatar'})

# avatar legibility sheet: square and circular crop at 256/128/64/32
W, H = 1200, 900
b = rect(0, 0, W, H, '#FFFFFF') + rect(0, 0, 16, H, colors['logo-blue']) + rect(16, 0, 8, H, colors['logo-red'])
b += txt('Avatar sizes and circular crop', 64, 84, 40, colors['ink'], 1000, True)[0]
b += '<defs>' + ''.join(f'<clipPath id="c{s}"><circle cx="{s / 2}" cy="{s / 2}" r="{s / 2}"/></clipPath>' for s in (256, 128, 64, 32)) + '</defs>'
def mark(s, x, y, clip):
    c = f' clip-path="url(#c{s})"' if clip else ''
    return f'<g transform="translate({x},{y})"><g{c}><rect width="{s}" height="{s}" fill="#000000"/><image x="{s * .18}" y="{s * .18}" width="{s * .64}" height="{s * .64}" href="{logo}"/></g></g>'
b += txt('Square', 64, 150, 24, colors['ink'], 300)[0] + txt('Circle crop', 64, 510, 24, colors['ink'], 300)[0]
xx = 64
for s in (256, 128, 64, 32):
    b += txt(f'{s} px', xx, 184 - 0, 20, colors['ink'], 200)[0]
    b += mark(s, xx, 196, False) + mark(s, xx, 540, True)
    xx += s + 64
b += txt('The full mark loses legibility at 32–64 px. A simplified small icon needs separate design and approval.', 64, 856, 22, colors['ink'], 1080)[0]
save('avatar-size-preview', 'Avatar / size and circle-crop preview', 'avatar-preview', svgdoc(W, H, b, 'Avatar size preview'))

# 4. Configuration updates ----------------------------------------------------------
repo = G / 'design-system'
specs = json.loads((repo / 'tokens' / 'platform-specifications.json').read_text())
known = {s['id'] for s in specs}
specs += [s for s in new_specs if s['id'] not in known]
(OUT / 'tokens').mkdir(parents=True, exist_ok=True)
(OUT / 'tokens' / 'platform-specifications.json').write_text(json.dumps(specs, indent=2, ensure_ascii=False))
pm = json.loads((repo / 'templates' / 'platform-map.json').read_text())
add = {'Instagram': ['instagram-landscape', 'reel-cover', 'avatar-instagram'],
       'Facebook': ['reel-cover', 'avatar-facebook'],
       'LinkedIn': ['linkedin-landscape', 'linkedin-square', 'linkedin-portrait', 'avatar-linkedin'],
       'X': ['x-landscape', 'x-portrait', 'avatar-x'],
       'TikTok': ['reel-cover', 'avatar-tiktok'],
       'YouTube': ['reel-cover', 'youtube-podcast', 'avatar-youtube'],
       'Pinterest': ['pinterest-square', 'pinterest-landscape', 'avatar-pinterest']}
for k, v in add.items():
    pm['platforms'][k] = pm['platforms'].get(k, []) + [x for x in v if x not in pm['platforms'].get(k, [])]
(OUT / 'templates').mkdir(parents=True, exist_ok=True)
(OUT / 'templates' / 'platform-map.json').write_text(json.dumps(pm, indent=2, ensure_ascii=False))
inv = json.loads((repo / 'templates' / 'inventory.json').read_text())
ids = {x['id'] for x in inv}
inv += [x for x in NEW if x['id'] not in ids]
(OUT / 'templates' / 'inventory.json').write_text(json.dumps(inv, indent=2, ensure_ascii=False))
print(len(NEW), 'new templates;', len(specs), 'specs')
