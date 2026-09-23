# Railway deploy — staging copy of the Instatic site

Runs the same `ghcr.io/corebunch/instatic:latest` image as local, with a
first-boot seed step so a fresh Railway volume comes up with the site in it.

- Project: `red-white-and-clix` / service `cms` / environment `production`
- Volume `cms-volume` mounted at `/vol`
- URL: https://cms-production-8370.up.railway.app

## Why a custom Dockerfile

Railway volumes start empty and there is no upload path for one. The image
copies a database snapshot and the uploads directory to `/seed`, and
`entrypoint-seed.sh` moves them into `/vol` **only when the volume has no
database yet**. A redeploy therefore never overwrites content edited in the
deployed admin.

`DATABASE_URL` and `UPLOADS_DIR` both point into `/vol`, so all state lives on
the volume rather than the container filesystem.

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

`railway up` honours the repository `.gitignore`, which excludes `seed/` — so
deploying from this directory silently ships an empty build context and the
build fails on `COPY seed/uploads`. Deploy from a copy **outside the repo**:

```bash
CTX=/private/tmp/rwc-railway-ctx
rm -rf "$CTX" && mkdir -p "$CTX"
cp Dockerfile entrypoint-seed.sh "$CTX"/
cp -a seed "$CTX/seed"
cd "$CTX"
railway link --project 315ba717-17bd-4396-8121-7e3ed1bd8fd2 --service cms --environment production
railway up --detach
```

## Volume ownership

Railway mounts the volume **root-owned**, while the image's app user is `bun`
(uid 1000). A container that starts as `bun` cannot even `mkdir /vol/data` —
the first deploy died in a restart loop on `Permission denied`. So the image
keeps `USER root` and `entrypoint-seed.sh` chowns `/vol` before dropping back
to `bun` with `setpriv` to exec the server. Instatic itself never runs as root.

## Variables

| Variable | Value | Why |
| --- | --- | --- |
| `DATABASE_URL` | `sqlite:/vol/data/cms.db` | On the volume, not the container |
| `UPLOADS_DIR` | `/vol/uploads` | Same |
| `STATIC_DIR` | `/app/dist` | Ships in the image |
| `PORT` | `3001` | Matches the image's `EXPOSE` |
| `PUBLIC_ORIGIN` | the Railway URL | Origin checks reject requests otherwise |
| `INSTATIC_SECRET_KEY` | copied from local | Reused so the seeded database's sessions and any encrypted plugin settings stay valid. Rotate it and those are invalidated. |

## Before this is anything but staging

- The admin at `/admin` is publicly reachable. It is protected only by the
  account password carried over in the snapshot.
- The policy pages have not had legal review (RWC-26, P0).
- Four SAMPLE event records are still present (RWC-16).
- The donation, volunteer and registration forms are not wired to anything
  (RWC-18 / RWC-20 / RWC-21).
- Canonical tags point at `https://www.redwhiteandclix.org`, so search engines
  should prefer the real site over this copy — but that is a hint, not a block.
  Add robots rules (RWC-27) before sharing the URL widely.
