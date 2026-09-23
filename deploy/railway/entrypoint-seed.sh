#!/bin/sh
# Seed the Railway volume on first boot, then hand off to Instatic's own
# entrypoint. Railway volumes start empty, and the CMS keeps everything that
# matters — pages, plugins, media — in SQLite plus the uploads directory.
#
# Seeding is one-shot and guarded: a redeploy must never overwrite content the
# client has edited in the deployed admin.
set -e

DATA_DIR=/vol/data
UPLOADS_DIR_TARGET=/vol/uploads

mkdir -p "$DATA_DIR" "$UPLOADS_DIR_TARGET"

if [ ! -f "$DATA_DIR/cms.db" ]; then
  echo "[seed] no database in volume — copying snapshot"
  cp /seed/cms.db "$DATA_DIR/cms.db"
else
  echo "[seed] database already present — leaving it alone"
fi

if [ ! -f "$UPLOADS_DIR_TARGET/.seeded" ]; then
  echo "[seed] copying uploads"
  cp -a /seed/uploads/. "$UPLOADS_DIR_TARGET"/
  touch "$UPLOADS_DIR_TARGET/.seeded"
else
  echo "[seed] uploads already present — leaving them alone"
fi

exec /usr/local/bin/docker-entrypoint.sh "$@"
