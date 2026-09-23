# Red, White and Clix — Instatic

Local CMS: http://localhost:3022/admin

On the first visit, enter **Red, White and Clix** as the site name and create your administrator account.

This independent Docker Compose project leaves the WordPress site intact. The upstream production and SQLite Compose files are adapted with a unique project/container name, localhost port 3022, public origins, and an explicit AMD64 platform for the current upstream image on Apple Silicon.

## Start

From this directory:

```sh
INSTATIC_IMAGE=ghcr.io/corebunch/instatic:latest docker compose -f compose.prod.yml -f compose.sqlite.yml up -d
```

## Stop

```sh
docker compose -f compose.prod.yml -f compose.sqlite.yml stop
```

## Storage and secrets

- Container: `red-white-and-clix`
- SQLite volume: `red-white-and-clix_data` at `/app/data`
- Media volume: `red-white-and-clix_uploads` at `/app/uploads`
- `.env` contains the generated encryption key, is Git-ignored, and has owner-only permissions. Preserve this key with backups.
- Back up the SQLite database and uploads together. Removing containers preserves volumes; `down -v` deletes them.
- The server listens only on this Mac. Public hosting and domain setup are separate steps.

Source: https://github.com/CoreBunch/Instatic/tree/main/docs/deployment
