#!/bin/sh
# Seed the Railway volume on first boot, then hand off to Instatic's own
# entrypoint. Railway volumes start empty, and the CMS keeps everything that
# matters — pages, plugins, media — in SQLite plus the uploads directory.
#
# Seeding is one-shot and guarded: a redeploy must never overwrite content the
# client has edited in the deployed admin.
#
# This runs as ROOT because Railway mounts the volume root-owned while the
# image's app user is `bun` (uid 1000) — without a chown the very first mkdir
# fails with EACCES. Privileges are dropped again before the app starts, so
# the server itself never runs as root.
set -e

VOL=/vol
APP_USER=bun

mkdir -p "$VOL/data" "$VOL/uploads"

if [ ! -f "$VOL/data/cms.db" ]; then
  echo "[seed] no database in volume — copying snapshot"
  cp /seed/cms.db "$VOL/data/cms.db"
else
  echo "[seed] database already present — leaving it alone"
fi

if [ ! -f "$VOL/uploads/.seeded" ]; then
  echo "[seed] copying uploads"
  cp -a /seed/uploads/. "$VOL/uploads"/
  touch "$VOL/uploads/.seeded"
else
  echo "[seed] uploads already present — leaving them alone"
fi

chown -R "$APP_USER:$APP_USER" "$VOL"

echo "[seed] dropping to $APP_USER and starting Instatic"
exec setpriv --reuid="$APP_USER" --regid="$APP_USER" --init-groups \
  /usr/local/bin/docker-entrypoint.sh "$@"
