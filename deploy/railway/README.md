# Railway deploy — staging copy of the Instatic site

Runs the same `ghcr.io/corebunch/instatic:latest` image as local, with a
first-boot seed step so a fresh Railway volume comes up with the site in it.

- Project: `red-white-and-clix` / service `cms` / environment `production`
- Volume `cms-volume` mounted at `/vol`
- Public URL: https://site-production-0334.up.railway.app (the `site` edge)
- The `cms` service has NO public domain — private network only

## How deploys work

Both services are connected to GitHub: pushes to `instatic-site-build` build
and deploy automatically. Each service's Dockerfile path is set on the service
itself (`serviceInstanceUpdate { dockerfilePath }`) rather than in a
`railway.json` — config-as-code is deprecated, and the API refuses to set
`railwayConfigFile`. The build context is the repository root for both.

| Service | Dockerfile | Role |
| --- | --- | --- |
| `site` | `deploy/railway/edge/Dockerfile` | Caddy; holds the public domain, gates the admin |
| `cms` | `deploy/railway/Dockerfile` | Instatic; private network only |
| `forms` | `deploy/railway/forms/Dockerfile` | Website form endpoint → GoHighLevel; private network only, reached by the edge at `/api/forms/*` |

**The image is stateless.** All content — pages, plugins, media, the SEO
records — lives on the Railway volume at `/vol`, because `DATABASE_URL` and
`UPLOADS_DIR` point there. `entrypoint-railway.sh` only touches the volume
when it is empty, so a redeploy never overwrites anything edited in the
deployed admin.

This is why GitHub builds carry no database snapshot: the snapshot holds admin
user rows and **this repository is public**, so it is deliberately untracked.
A normal deploy does not need it — the volume already has the data.

## Rebuilding the seed

`seed/` is deliberately untracked — the snapshot contains admin user rows.
Recreate it from a running local container, checkpointing the WAL first or you
copy a shell while the real data sits in `cms.db-wal`:

```bash
docker exec <container> bun -e "const {Database}=require('bun:sqlite'); \
  const db=new Database('/app/data/cms.db'); db.exec('PRAGMA wal_checkpoint(TRUNCATE)')"
docker cp <container>:/app/data/cms.db  deploy/railway/seed/cms.db
docker cp <container>:/app/uploads      deploy/railway/seed/uploads
```

## Deploying

Normally: `git push`. Railway builds the branch it is connected to.

### Pushing content to the deployed site

The volume is the deployed site's only copy of its content, so a normal
redeploy never touches it. Pushing new content is therefore deliberate:

1. Rebuild `seed/` from the local container (below).
2. Bump `SEED_VERSION` on the `cms` service to a new value.
3. Run a local build carrying the snapshot (below).

The volume records the version it was last seeded at, so the replace happens
exactly once — a later redeploy with the same value is a no-op.

**Do not `git push` in the middle of a content push.** Both services deploy
from GitHub, so a push starts a build of the *stateless* image that races the
one carrying the snapshot, and whichever finishes last is the one running. Let
any in-flight deploy reach SUCCESS first:

```bash
until ! railway deployment list | sed -n '2p' | grep -qE 'BUILDING|DEPLOYING|QUEUED'; do sleep 15; done
```

**The content-push Dockerfile has to live at `deploy/railway/Dockerfile`
inside the context**, because that is the path set on the service
(`serviceInstanceUpdate { dockerfilePath }`). A Dockerfile at the context root
fails the build with `couldn't locate the dockerfile at path
deploy/railway/Dockerfile`. **A push
REPLACES the database**, so anything edited in the deployed admin since the
last push is lost. That is the trade for having it be a single explicit act.

### Bootstrapping an empty volume

Only needed for a brand new environment, or after losing a volume. The boot
log shouts when it happens — an empty volume with no seed starts a blank site,
which otherwise looks like a fresh install rather than data loss.

Build a context **outside the repository** (`railway up` honours the repo
`.gitignore`, which excludes `seed/`, so deploying from inside it would ship no
snapshot) and add a `COPY seed /seed` line for that one build:

```bash
CTX=/private/tmp/rwc-railway-ctx
rm -rf "$CTX" && mkdir -p "$CTX/deploy/railway"
cp deploy/railway/entrypoint-railway.sh "$CTX/deploy/railway/"
cp -a deploy/railway/seed "$CTX/seed"
cd "$CTX"
# Write a Dockerfile that adds `COPY seed /seed` to the repo one. Do NOT
# generate it with sed on `USER root` — the file has two such lines and you
# get the COPY twice.
railway link --project 315ba717-17bd-4396-8121-7e3ed1bd8fd2 --service cms --environment production
railway up --detach
```

## Volume ownership

Railway mounts the volume **root-owned**, while the image's app user is `bun`
(uid 1000). A container that starts as `bun` cannot even `mkdir /vol/data` —
the first deploy died in a restart loop on `Permission denied`. So the image
keeps `USER root` and `entrypoint-railway.sh` chowns `/vol` before dropping
back to `bun` with `setpriv` to exec the server. Instatic never runs as root.

## Variables

| Variable | Value | Why |
| --- | --- | --- |
| `DATABASE_URL` | `sqlite:/vol/data/cms.db` | On the volume, not the container |
| `UPLOADS_DIR` | `/vol/uploads` | Same |
| `STATIC_DIR` | `/app/dist` | Ships in the image |
| `PORT` | `3001` | Matches the image's `EXPOSE` |
| `PUBLIC_ORIGIN` | the Railway URL | Origin checks reject requests otherwise |
| `INSTATIC_SECRET_KEY` | copied from local | Reused so the seeded database's sessions and any encrypted plugin settings stay valid. Rotate it and those are invalidated. |

## The admin gate

Railway has no native access control (its WAF is only "under attack" mode), so
`/admin*` and `/_instatic/mcp*` sit behind HTTP basic auth at the `site` edge.
Everything a visitor needs — pages, `/_instatic/assets` and `/_instatic/css`,
the loop endpoint, form posts, uploaded media — stays public.

The CMS has no public domain at all; the edge reaches it at
`cms.railway.internal:3001`. Credentials are in the gitignored
`CREDENTIALS.local.md`; the bcrypt hash lives in the `BASIC_AUTH_HASH`
variable on the `site` service and never in this public repository.

Instatic's own login also locks out after 5 failed attempts, doubling from 15
minutes up to 24 hours.

## Before this is anything but staging
- The policy pages have not had legal review (RWC-26, P0).
- Four SAMPLE event records are still present (RWC-16).
- The donation, volunteer and registration forms are not wired to anything
  (RWC-18 / RWC-20 / RWC-21).
- Canonical tags point at `https://www.redwhiteandclix.org`, so search engines
  should prefer the real site over this copy — but that is a hint, not a block.
  Add robots rules (RWC-27) before sharing the URL widely.

## PUBLIC_ORIGIN — changed 2026-09-27

`cms` now carries `PUBLIC_ORIGIN=https://www.redwhiteandclix.org`. It was
still the staging URL after the domain cutover, which made Instatic reject
anything posted from the real domain with **"Forbidden: invalid origin"** —
admin login on `www`, and any future contact form.

**The check flips both ways.** Admin writes are now accepted only from
`www.redwhiteandclix.org`. The staging URL still serves and still reads, but
saving there fails with the same error. All admin work belongs on `www` now;
that is the point.

Two things that wasted time and are worth knowing:

- Setting the variable triggers a rebuild, and the **old container keeps
  serving until it finishes**. Testing the origin immediately after the CLI
  returns shows the old behaviour and looks like the change failed. Watch
  `railway deployment list --service cms` for SUCCESS before testing.
- Distinguish the two failures by status: **403 `invalid origin`** means the
  host check rejected it; **401** means it reached authentication and the
  credentials were wrong. Going from 403 to 401 is the fix working.

## Website forms (`forms` service)

The site's own forms POST to `/api/forms/<kind>` (contact, sponsor,
newsletter, volunteer, nominate). The edge proxies that path to
`forms.railway.internal:8080` (override with `FORMS_UPSTREAM` on `site`).
`deploy/railway/forms/server.mjs` validates, drops spam (honeypot + a 3-second
minimum fill time + 6 submissions per IP per 10 minutes), normalises phone
numbers to E.164, upserts the contact into the RWC GoHighLevel sub-account and
removes-then-adds a `web-form-<kind>` tag. That tag triggers the matching
"Form - ..." workflow in GHL, so website and native GHL submissions run the
same automation.

| Variable (on `forms`) | Value |
| --- | --- |
| `GHL_PIT` | RWC Private Integration token — Railway only, never in git |
| `GHL_LOCATION_ID` | `yNbQAVmIAdetff2yf45O` |
| `PORT` | `8080` |
| `ALLOWED_ORIGINS` | optional; defaults to the two redwhiteandclix.org origins |

Without `GHL_PIT` the service answers 503 and the site shows its fallback
message. Test locally with `node deploy/railway/forms/test.mjs` (mock GHL).
