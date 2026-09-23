# Instatic for Railway.
#
# Build context is the REPOSITORY ROOT so this works for GitHub-triggered
# builds (see railway.json at the root, which points Railway at this file).
# The image is stateless: all content lives on the Railway volume at /vol,
# and `entrypoint-railway.sh` only bootstraps that volume when it is empty.
#
# A local bootstrap deploy can additionally drop a snapshot at /seed — see
# deploy/railway/README.md. GitHub builds never carry one, because the
# snapshot contains admin user rows and this repository is public.
FROM ghcr.io/corebunch/instatic:latest

USER root
COPY deploy/railway/entrypoint-railway.sh /usr/local/bin/entrypoint-railway.sh
RUN chmod +x /usr/local/bin/entrypoint-railway.sh

# Stays root on purpose: Railway mounts the volume root-owned, so the boot
# step has to chown it. entrypoint-railway.sh drops back to `bun` via setpriv
# before exec'ing the server, so Instatic never runs as root.
USER root

ENTRYPOINT ["/usr/local/bin/entrypoint-railway.sh"]
CMD ["bun", "run", "server/index.ts"]
