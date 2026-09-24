"""
Clean up sponsor logos taken from the live site.

Two operations, in order:

1. Knock out the background. A plain global "replace all white" would punch
   holes through white letter interiors and enclosed shapes, so this walks the
   background inward from the image border instead and only clears pixels that
   are CONNECTED to the edge. Interior whites survive.

2. Trim to the remaining content, so every logo arrives with no padding of its
   own and the wall controls the spacing.

Edge pixels get partial alpha scaled by how far they are from the background
colour, which keeps anti-aliased type from turning into a hard jagged cut.
"""
import sys, os
from collections import deque
from PIL import Image

def dist(a, b):
    return max(abs(a[0]-b[0]), abs(a[1]-b[1]), abs(a[2]-b[2]))

def tighten(src, dst, tol=None, feather_hi=None):
    im = Image.open(src).convert('RGBA')
    w, h = im.size
    px = im.load()

    # Background colour = the agreed corner colour. If the corners disagree the
    # image has no flat background and only trimming is safe.
    corners = [px[0,0], px[w-1,0], px[0,h-1], px[w-1,h-1]]
    bg = corners[0][:3]
    if max(dist(c[:3], bg) for c in corners) > 24:
        im.save(dst); return f'{os.path.basename(dst)}: corners disagree, left as-is'

    if tol is None:
        tol = 34 if src.lower().endswith(('.jpg','.jpeg')) else 16
    if feather_hi is None:
        feather_hi = tol * 2.4

    # Flood from every border pixel that matches the background.
    seen = bytearray(w*h)
    q = deque()
    for x in range(w):
        for y in (0, h-1):
            if dist(px[x,y][:3], bg) <= tol and not seen[y*w+x]:
                seen[y*w+x] = 1; q.append((x,y))
    for y in range(h):
        for x in (0, w-1):
            if dist(px[x,y][:3], bg) <= tol and not seen[y*w+x]:
                seen[y*w+x] = 1; q.append((x,y))
    while q:
        x, y = q.popleft()
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = x+dx, y+dy
            if 0 <= nx < w and 0 <= ny < h and not seen[ny*w+nx]:
                if dist(px[nx,ny][:3], bg) <= tol:
                    seen[ny*w+nx] = 1; q.append((nx,ny))

    for i in range(w*h):
        if seen[i]:
            x, y = i % w, i // w
            px[x,y] = (px[x,y][0], px[x,y][1], px[x,y][2], 0)

    # Soften the boundary: anything still opaque but sitting against a cleared
    # pixel gets alpha proportional to its distance from the background.
    softened = 0
    for i in range(w*h):
        if seen[i]: continue
        x, y = i % w, i // w
        touching = False
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = x+dx, y+dy
            if 0 <= nx < w and 0 <= ny < h and seen[ny*w+nx]:
                touching = True; break
        if touching:
            d = dist(px[x,y][:3], bg)
            if d < feather_hi:
                a = int(max(0, min(255, 255 * d / feather_hi)))
                r, g, b, _ = px[x,y]
                px[x,y] = (r, g, b, a); softened += 1

    bbox = im.getbbox()
    if bbox: im = im.crop(bbox)
    im.save(dst, optimize=True)
    return f'{os.path.basename(dst)}: bg{bg} tol={tol} -> {im.size[0]}x{im.size[1]} ({softened} edge px softened)'

if __name__ == '__main__':
    for name in sys.argv[1:]:
        src = f'/private/tmp/rwc-tighten/in/{name}'
        stem = os.path.splitext(name)[0]
        dst = f'/private/tmp/rwc-tighten/out/{stem}.png'
        try:
            print(tighten(src, dst))
        except Exception as e:
            print(f'{name}: FAILED {e}')
