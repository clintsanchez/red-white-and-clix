#!/bin/sh
# Railway entrypoint: make the volume usable, bootstrap it if this image
# happens to carry a seed, then hand off to Instatic's own entrypoint.
#
# Runs as ROOT because Railway mounts the volume root-owned while the image's
# app user is `bun` (uid 1000) — without a chown the first mkdir fails with
# EACCES. Privileges are dropped before the server starts, so Instatic itself
# never runs as root.
#
# The seed is OPTIONAL by design. Builds from GitHub cannot carry it: the
# snapshot holds admin user rows and is deliberately untracked, and the repo
# is public. The volume is the source of truth, so a normal redeploy simply
# finds a database already there and leaves it alone. Only a first bootstrap
# needs the snapshot, which is what `railway up` from a local context is for.
set -e

VOL=/vol
APP_USER=bun

mkdir -p "$VOL/data" "$VOL/uploads"

if [ -f "$VOL/data/cms.db" ]; then
  echo "[boot] database present on volume — untouched"
elif [ -f /seed/cms.db ]; then
  echo "[boot] empty volume, image carries a seed — restoring snapshot"
  cp /seed/cms.db "$VOL/data/cms.db"
  if [ -d /seed/uploads ]; then
    cp -a /seed/uploads/. "$VOL/uploads"/
  fi
else
  # Loud, because the alternative is a silently blank site that looks like a
  # fresh install rather than a lost volume.
  echo "[boot] ================================================================"
  echo "[boot] WARNING: the volume has no database and this image has no seed."
  echo "[boot] WARNING: Instatic is about to start EMPTY."
  echo "[boot] WARNING: If this is not a brand new environment, STOP and"
  echo "[boot] WARNING: restore a snapshot — see deploy/railway/README.md."
  echo "[boot] ================================================================"
fi

chown -R "$APP_USER:$APP_USER" "$VOL"

echo "[boot] dropping to $APP_USER and starting Instatic"
exec setpriv --reuid="$APP_USER" --regid="$APP_USER" --init-groups \
  /usr/local/bin/docker-entrypoint.sh "$@"
