// Website form endpoint for redwhiteandclix.org -> GoHighLevel.
//
// The site's own forms POST here (via the Caddy edge at /api/forms/<kind>).
// This service validates, filters spam, normalises the phone number, upserts
// the contact into the RWC GHL sub-account and re-applies a `web-form-<kind>`
// tag. That tag is the trigger on the matching GHL "Form - ..." workflow, so a
// website submission runs exactly the same automation as a native GHL form.
//
// The GHL key lives only in Railway variables (GHL_PIT, GHL_LOCATION_ID). This
// repository is public: never put a token in this file.
//
// No dependencies; Node 20+.
import http from "node:http";

const PORT = Number(process.env.PORT || 8080);
const GHL = process.env.GHL_BASE || "https://services.leadconnectorhq.com";
const PIT = (process.env.GHL_PIT || "").trim();
const LOC = (process.env.GHL_LOCATION_ID || "").trim();
const ORIGINS = (process.env.ALLOWED_ORIGINS || "https://www.redwhiteandclix.org,https://redwhiteandclix.org")
  .split(",").map((s) => s.trim()).filter(Boolean);
const MIN_FILL_MS = 3000;          // bots submit instantly; people do not
const RATE = { max: 6, windowMs: 10 * 60 * 1000 };

// Field map per form. `key` = GHL contact custom field key (contact.<key>).
// Standard fields are handled separately. `multi` fields accept several values.
const FORMS = {
  contact: {
    tag: "web-form-contact", required: ["first_name", "email", "message"],
    custom: { message: { key: "your_feedback" } },
  },
  sponsor: {
    tag: "web-form-sponsor", required: ["first_name", "email", "organization"],
    custom: { sponsor_level: { key: "sponsor_level", label: "Sponsorship level" }, notes: { key: "notes" } },
  },
  newsletter: { tag: "web-form-newsletter", required: ["email"], custom: {} },
  volunteer: {
    tag: "web-form-volunteer", required: ["first_name", "email", "phone"],
    custom: {
      interests: { key: "volunteer_interests", multi: true, label: "Would like to help with" },
      availability: { key: "volunteer_availability", multi: true, label: "Availability" },
      under_18: { key: "guardian_required", label: "Under 18" },
      emergency_contact: { key: "emergency_contact" },
    },
  },
  nominate: {
    tag: "web-form-nominate", required: ["first_name", "email", "beneficiary_name"],
    custom: {
      beneficiary_name: { key: "beneficiary_name" },
      relationship: { key: "relationship_to_nominator" },
      address: { key: "shipping_address" },
      story: { key: "brief_description_of_your_situation" },
    },
  },
};

const hits = new Map();
function limited(ip) {
  const now = Date.now();
  const recent = (hits.get(ip) || []).filter((t) => now - t < RATE.windowMs);
  recent.push(now);
  hits.set(ip, recent);
  return recent.length > RATE.max;
}

export function e164(raw) {
  const s = String(raw || "").trim();
  if (!s) return "";
  const digits = s.replace(/\D/g, "");
  if (s.startsWith("+")) return digits.length >= 8 ? "+" + digits : "";
  if (digits.length === 10) return "+1" + digits;
  if (digits.length === 11 && digits.startsWith("1")) return "+" + digits;
  return "";
}

const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const clip = (v, n = 2000) => String(v ?? "").replace(/\u0000/g, "").trim().slice(0, n);

export function validate(kind, body) {
  const spec = FORMS[kind];
  if (!spec) return { error: "unknown form" };
  const errors = {};
  for (const f of spec.required) if (!clip(body[f])) errors[f] = "Required";
  if (body.email && !EMAIL.test(clip(body.email, 254))) errors.email = "Enter a valid email address";
  if (body.phone && !e164(body.phone)) errors.phone = "Enter a valid phone number";
  if (!body.consent) errors.consent = "Please tick the box so we can reply";
  return Object.keys(errors).length ? { errors } : { ok: true };
}

let fieldCache = null;
async function fields() {
  if (fieldCache) return fieldCache;
  const r = await ghl("GET", `/locations/${LOC}/customFields`);
  fieldCache = Object.fromEntries((r.customFields || []).map((f) => [f.fieldKey.replace(/^contact\./, ""), f]));
  return fieldCache;
}

async function ghl(method, path, body) {
  const r = await fetch(GHL + path, {
    method,
    headers: { Authorization: `Bearer ${PIT}`, Version: "2021-07-28", Accept: "application/json", "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await r.text();
  if (!r.ok) throw new Error(`GHL ${method} ${path.split("?")[0]} -> ${r.status} ${text.slice(0, 200)}`);
  return text ? JSON.parse(text) : {};
}

export async function submit(kind, body) {
  const spec = FORMS[kind];
  const fmap = await fields();
  const customFields = [];
  // A choice the site offers but the GHL picklist does not know yet is kept
  // as a line in Notes rather than dropped, so nothing the visitor chose is lost.
  const unmatched = [];
  for (const [input, def] of Object.entries(spec.custom)) {
    let v = body[input];
    if (v == null || v === "") continue;
    const f = fmap[def.key];
    if (!f) throw new Error(`custom field missing in GHL: ${def.key}`);
    const allowed = f.picklistOptions ? new Set(f.picklistOptions) : null;
    if (def.multi) {
      const all = (Array.isArray(v) ? v : [v]).map((x) => clip(x, 200)).filter(Boolean);
      v = allowed ? all.filter((x) => allowed.has(x)) : all;
      const extra = allowed ? all.filter((x) => !allowed.has(x)) : [];
      if (extra.length) unmatched.push(`${def.label || def.key}: ${extra.join(", ")}`);
      if (!v.length) continue;
    } else {
      v = clip(v);
      if (allowed && !allowed.has(v)) { unmatched.push(`${def.label || def.key}: ${v}`); continue; }
    }
    customFields.push({ id: f.id, field_value: v });
  }
  if (unmatched.length && fmap.notes) {
    const i = customFields.findIndex((c) => c.id === fmap.notes.id);
    const prefix = unmatched.join(" | ");
    if (i >= 0) customFields[i].field_value = clip(`${prefix} | ${customFields[i].field_value}`);
    else customFields.push({ id: fmap.notes.id, field_value: clip(prefix) });
  }
  const contact = {
    locationId: LOC,
    firstName: clip(body.first_name, 100) || undefined,
    lastName: clip(body.last_name, 100) || undefined,
    email: clip(body.email, 254).toLowerCase(),
    phone: e164(body.phone) || undefined,
    companyName: clip(body.organization, 200) || undefined,
    source: `Website - ${kind}`,
    customFields,
  };
  const up = await ghl("POST", "/contacts/upsert", contact);
  const id = up.contact?.id;
  if (!id) throw new Error("upsert returned no contact id");
  // Remove then re-add: a tag trigger fires on "added", so a returning contact
  // who already carries the tag would otherwise never re-enter the workflow.
  await ghl("DELETE", `/contacts/${id}/tags`, { tags: [spec.tag] }).catch(() => {});
  await ghl("POST", `/contacts/${id}/tags`, { tags: [spec.tag, "src-website"] });
  return id;
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let size = 0; const chunks = [];
    req.on("data", (c) => { size += c.length; if (size > 32 * 1024) { reject(new Error("too large")); req.destroy(); } else chunks.push(c); });
    req.on("end", () => resolve(Buffer.concat(chunks).toString("utf8")));
    req.on("error", reject);
  });
}

function parse(raw, type) {
  if ((type || "").includes("application/json")) return JSON.parse(raw || "{}");
  const out = {};
  for (const [k, v] of new URLSearchParams(raw)) {
    if (k in out) out[k] = [].concat(out[k], v); else out[k] = v;
  }
  return out;
}

function send(res, status, obj, extra = {}) {
  res.writeHead(status, { "Content-Type": "application/json", "Cache-Control": "no-store", ...extra });
  res.end(JSON.stringify(obj));
}

export const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, "http://x");
  if (url.pathname === "/api/forms/health") return send(res, 200, { ok: true, configured: Boolean(PIT && LOC) });
  const m = url.pathname.match(/^\/api\/forms\/([a-z]+)\/?$/);
  if (!m || req.method !== "POST") return send(res, 404, { error: "not found" });
  const kind = m[1];
  const origin = req.headers.origin || "";
  if (origin && !ORIGINS.includes(origin)) return send(res, 403, { error: "origin not allowed" });
  // Railway's edge supplies the visitor address; without one, skip the limit
  // rather than lumping every visitor into a single bucket.
  const ip = String(req.headers["x-real-ip"] || req.headers["x-forwarded-for"] || "").split(",")[0].trim();
  if (ip && limited(ip)) return send(res, 429, { error: "Too many submissions. Please try again later." });

  let body;
  try { body = parse(await readBody(req), req.headers["content-type"]); }
  catch { return send(res, 400, { error: "bad request" }); }

  const html = !(req.headers["content-type"] || "").includes("application/json");
  const back = (ok) => {
    const ref = req.headers.referer && ORIGINS.some((o) => req.headers.referer.startsWith(o)) ? new URL(req.headers.referer) : new URL(ORIGINS[0]);
    ref.searchParams.set("form", ok ? "sent" : "error"); ref.hash = kind;
    res.writeHead(303, { Location: ref.toString(), "Cache-Control": "no-store" }); res.end();
  };

  // Spam: honeypot filled, or submitted faster than a person could. Answer as
  // if it worked so bots get no signal to adapt to.
  const started = Number(body.t || 0);
  if (clip(body.website) || (started && Date.now() - started < MIN_FILL_MS)) {
    console.log(JSON.stringify({ kind, result: "spam-dropped" }));
    return html ? back(true) : send(res, 200, { ok: true });
  }

  const v = validate(kind, body);
  if (!v.ok) return html ? back(false) : send(res, 422, v.error ? { error: v.error } : { errors: v.errors });
  if (!PIT || !LOC) {
    console.error(JSON.stringify({ kind, result: "not-configured" }));
    return html ? back(false) : send(res, 503, { error: "We could not send that just now. Please email redwhiteandclix@gmail.com or call (574) 265-9585." });
  }

  try {
    await submit(kind, body);
    console.log(JSON.stringify({ kind, result: "ok" }));
    return html ? back(true) : send(res, 200, { ok: true });
  } catch (e) {
    console.error(JSON.stringify({ kind, result: "error", message: String(e.message).slice(0, 300) }));
    return html ? back(false) : send(res, 502, { error: "We could not send that just now. Please email redwhiteandclix@gmail.com." });
  }
});

if (process.argv[1] && import.meta.url === new URL(`file://${process.argv[1]}`).href) {
  server.listen(PORT, () => console.log(`forms listening on ${PORT} (configured: ${Boolean(PIT && LOC)})`));
}
