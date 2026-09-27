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
//
// THE TRAP, learned the hard way: the policy value contains single quotes
// ('self'), so a content=["']([^"']*)["'] pattern captures only "default-src "
// and mangles everything after it. A mangled policy is worse than no plugin —
// a duplicated directive means the browser honours the FIRST one, so a broken
// script-src silently blocks the site's own JavaScript. Match the double-quoted
// attribute only, and verify the result before returning it.

const SCRIPT_SRC = ["https://www.googletagmanager.com"];
const CONNECT_SRC = [
  "https://www.google-analytics.com",
  "https://*.analytics.google.com",
  "https://*.google-analytics.com",
  "https://*.googletagmanager.com"
];

const CSP_META = /(<meta[^>]*http-equiv="Content-Security-Policy"[^>]*content=")([^"]*)("[^>]*>)/i;

function parse(policy) {
  return policy.split(";").map((p) => p.trim()).filter(Boolean).map((p) => {
    const bits = p.split(/\s+/);
    return { name: bits[0].toLowerCase(), sources: bits.slice(1) };
  });
}

function serialise(parts) {
  return parts.map((p) => [p.name].concat(p.sources).join(" ")).join("; ") + ";";
}

function addSources(parts, name, sources) {
  const found = parts.find((p) => p.name === name);
  if (found) {
    sources.forEach((s) => { if (!found.sources.includes(s)) found.sources.push(s); });
    return parts;
  }
  // Absent, so it currently inherits default-src. Spell it out rather than
  // widening default-src, which would loosen every other fetch type too.
  const base = parts.find((p) => p.name === "default-src");
  const inherited = base && base.sources.length ? base.sources.slice() : ["'self'"];
  parts.push({ name, sources: inherited.concat(sources) });
  return parts;
}

// Refuse to emit anything that is not obviously safe. Any of these means the
// parse went wrong, and the original policy is always the safer answer.
function isSane(parts) {
  if (!parts.length) return false;
  const names = parts.map((p) => p.name);
  if (new Set(names).size !== names.length) return false;      // duplicate directive
  if (parts.some((p) => p.sources.length === 0)) return false;  // empty directive
  if (!names.includes("default-src")) return false;
  return true;
}

function rewritePolicy(policy) {
  const parts = parse(policy);
  if (!isSane(parts)) return null;
  addSources(parts, "script-src", SCRIPT_SRC);
  addSources(parts, "connect-src", CONNECT_SRC);
  if (!isSane(parts)) return null;
  return serialise(parts);
}

export default {
  async activate(api) {
    api.cms.hooks.filter("publish.html", async (html) => {
      const allow = api.cms.settings.get("allowAnalytics");
      if (allow === false || allow === "false" || allow === "off" || allow === 0) return html;

      const m = html.match(CSP_META);
      if (!m) {
        api.plugin.log("[blaksheep.csp] no CSP meta tag found; left untouched");
        return html;
      }
      const next = rewritePolicy(m[2]);
      if (!next) {
        api.plugin.log("[blaksheep.csp] policy failed sanity check; left untouched:", m[2]);
        return html;
      }
      return html.replace(CSP_META, `$1${next}$3`);
    });
    api.plugin.log("[blaksheep.csp] publish.html filter registered");
  }
};
