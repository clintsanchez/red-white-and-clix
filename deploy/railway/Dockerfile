# Instatic for Railway.
#
# The upstream image is used as-is; this only adds a first-boot seed step so a
# fresh Railway volume comes up with the site already in it. DATABASE_URL and
# UPLOADS_DIR are pointed into the volume at /vol by the service variables, so
# a redeploy never loses content.
FROM ghcr.io/corebunch/instatic:latest

USER root
COPY seed/cms.db /seed/cms.db
COPY seed/uploads /seed/uploads
COPY entrypoint-seed.sh /usr/local/bin/entrypoint-seed.sh
RUN chmod +x /usr/local/bin/entrypoint-seed.sh \
 && chown -R bun:bun /seed
USER bun

ENTRYPOINT ["/usr/local/bin/entrypoint-seed.sh"]
CMD ["bun", "run", "server/index.ts"]
