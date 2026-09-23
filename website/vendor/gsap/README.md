# GSAP 3.13.0 (vendored)

Self-hosted because the published pages run under `script-src 'self'` — a CDN
tag is blocked by CSP. Served from the Instatic uploads volume at
`/uploads/vendor/gsap/`, which is where `src/scripts/motion.js` loads it from.

To restore after a fresh deploy (the uploads volume is not in this repo):

```bash
docker exec -u root <container> mkdir -p /app/uploads/vendor/gsap
docker cp gsap.min.js          <container>:/app/uploads/vendor/gsap/
docker cp ScrollTrigger.min.js <container>:/app/uploads/vendor/gsap/
docker exec -u root <container> chown -R bun:bun /app/uploads/vendor
```

GSAP 3.13 is free for this use under the GreenSock standard license; every
plugin, ScrollTrigger included, became free in 2025.
Source: https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/
