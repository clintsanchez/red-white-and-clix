// Rewrites the published Content-Security-Policy meta tag.
//
// Why a plugin at all: there is no CSP site setting. The publisher hardcodes
// `default-src 'self'; script-src 'self'` into every page, and that blocks
// googletagmanager outright — so GA loads, is refused by the browser, and
// silently records nothing. That failure is indistinguishable from "no
// traffic yet", which is why it gets its own visible plugin rather than being
// hidden inside the SEO one.
//
// Scope is deliberately narrow. Only script-src and connect-src change, and
// only by the exact hosts GA needs. 'unsafe-inline' is never added: consent.js
// is an external file and needs no inline execution.

const SCRIPT_SRC = ["https://www.googletagmanager.com"];
const CONNECT_SRC = [
  "https://www.google-analytics.com",
  "https://*.analytics.google.com",
  "https://*.google-analytics.com",
  "https://*.googletagmanager.com"
];

function addSources(policy, directive, sources, fallbackFrom) {
  const parts = policy.split(";").map((p) => p.trim()).filter(Boolean);
  const idx = parts.findIndex((p) => p.split(/\s+/)[0].toLowerCase() === directive);
  if (idx === -1) {
    // The directive is absent, so it currently inherits default-src. Spell it
    // out rather than loosening default-src, which would widen everything.
    const base = parts.find((p) => p.split(/\s+/)[0].toLowerCase() === fallbackFrom);
    const inherited = base ? base.split(/\s+/).slice(1).join(" ") : "'self'";
    parts.push(`${directive} ${inherited} ${sources.join(" ")}`.trim());
    return parts.join("; ") + ";";
  }
  const existing = parts[idx].split(/\s+/).slice(1);
  const merged = existing.concat(sources.filter((s) => !existing.includes(s)));
  parts[idx] = `${directive} ${merged.join(" ")}`;
  return parts.join("; ") + ";";
}

export default {
  async activate(api) {
    api.cms.hooks.filter("publish.html", async (html) => {
      if (api.cms.settings.get("allowAnalytics") === false) return html;

      const re = /(<meta[^>]*http-equiv=["']Content-Security-Policy["'][^>]*content=["'])([^"']*)(["'][^>]*>)/i;
      const m = html.match(re);
      if (!m) {
        // No meta to rewrite. Do not invent one: a CSP this plugin authored
        // from nothing could break a page it knows nothing about.
        api.plugin.log("[blaksheep.csp] no CSP meta tag found; left untouched");
        return html;
      }
      let policy = m[2];
      policy = addSources(policy, "script-src", SCRIPT_SRC, "default-src");
      policy = addSources(policy, "connect-src", CONNECT_SRC, "default-src");
      return html.replace(re, `$1${policy}$3`);
    });
    api.plugin.log("[blaksheep.csp] publish.html filter registered");
  }
};
