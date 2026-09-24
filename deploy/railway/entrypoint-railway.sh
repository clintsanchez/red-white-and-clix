#!/bin/sh
# Railway entrypoint: make the volume usable, seed or re-seed it when asked,
# then hand off to Instatic's own entrypoint.
#
# Runs as ROOT because Railway mounts the volume root-owned while the image's
# app user is `bun` (uid 1000) — without a chown the first mkdir fails with
# EACCES. Privileges are dropped before the server starts, so Instatic itself
# never runs as root.
#
# SEEDING HAS TWO MODES, and the distinction matters because the volume is the
# live site's only copy of its content:
#
#   * First boot (no database on the volume) — seed if this image carries one.
#   * Content push — set SEED_VERSION to a new value. The volume records the
#     version it was last seeded at, so a matching value is a no-op. That makes
#     a push an explicit, one-time act instead of something a redeploy repeats.
#
# A content push REPLACES the database. Anything edited in the deployed admin
# since the last push is lost, which is why it needs a deliberate variable
# change rather than happening on every deploy.
set -e

VOL=/vol
APP_USER=bun
STAMP="$VOL/data/.seed-version"

mkdir -p "$VOL/data" "$VOL/uploads"

seed_now() {
  echo "[boot] seeding content (version: ${SEED_VERSION:-initial})"
  cp /seed/cms.db "$VOL/data/cms.db"
  # Remove any stale WAL/SHM beside the old database or SQLite will try to
  # replay them onto the new file and corrupt it.
  rm -f "$VOL/data/cms.db-wal" "$VOL/data/cms.db-shm"
  [ -d /seed/uploads ] && cp -a /seed/uploads/. "$VOL/uploads"/
  printf '%s' "${SEED_VERSION:-initial}" > "$STAMP"
}

if [ ! -f /seed/cms.db ]; then
  if [ -f "$VOL/data/cms.db" ]; then
    echo "[boot] no seed in image, database present on volume — untouched"
  else
    echo "[boot] ================================================================"
    echo "[boot] WARNING: the volume has no database and this image has no seed."
    echo "[boot] WARNING: Instatic is about to start EMPTY."
    echo "[boot] WARNING: If this is not a brand new environment, STOP and"
    echo "[boot] WARNING: restore a snapshot — see deploy/railway/README.md."
    echo "[boot] ================================================================"
  fi
elif [ ! -f "$VOL/data/cms.db" ]; then
  seed_now
elif [ -n "$SEED_VERSION" ] && [ "$(cat "$STAMP" 2>/dev/null)" != "$SEED_VERSION" ]; then
  echo "[boot] SEED_VERSION changed -> replacing the deployed content"
  seed_now
else
  echo "[boot] database present on volume — untouched"
fi

chown -R "$APP_USER:$APP_USER" "$VOL"

echo "[boot] dropping to $APP_USER and starting Instatic"
exec setpriv --reuid="$APP_USER" --regid="$APP_USER" --init-groups \
  /usr/local/bin/docker-entrypoint.sh "$@"
