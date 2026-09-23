# Auth edge for the Instatic staging site.
#
# Railway has no native access control and its WAF is only "under attack"
# mode, so the admin is gated here instead. This service holds the public
# domain; the CMS itself is reachable only over the project's private network.
#
# Credentials come from environment variables — BASIC_AUTH_HASH is a bcrypt
# hash and never lands in this repository, which is public.
FROM caddy:2-alpine

COPY deploy/railway/edge/Caddyfile /etc/caddy/Caddyfile

EXPOSE 8080
CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]
