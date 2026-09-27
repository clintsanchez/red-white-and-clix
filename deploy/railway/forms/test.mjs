// Local test: mock GHL + the real server. `node test.mjs`
import http from "node:http";
import assert from "node:assert/strict";
const calls = [];
const mock = http.createServer((req, res) => {
  let b = ""; req.on("data", (c) => (b += c)); req.on("end", () => {
    calls.push({ m: req.method, p: req.url, b: b ? JSON.parse(b) : null, auth: req.headers.authorization });
    res.setHeader("Content-Type", "application/json");
    if (req.url.includes("/customFields")) return res.end(JSON.stringify({ customFields: [
      { id: "F1", fieldKey: "contact.your_feedback" }, { id: "F2", fieldKey: "contact.volunteer_interests", picklistOptions: ["Events", "Wherever needed"] },
      { id: "F3", fieldKey: "contact.sponsor_level", picklistOptions: ["Gold", "Silver"] }, { id: "F4", fieldKey: "contact.notes" },
      { id: "F5", fieldKey: "contact.volunteer_availability", picklistOptions: ["Weekends"] }, { id: "F6", fieldKey: "contact.guardian_required", picklistOptions: ["Yes", "No"] },
      { id: "F7", fieldKey: "contact.emergency_contact" }, { id: "F8", fieldKey: "contact.beneficiary_name" }, { id: "F9", fieldKey: "contact.relationship_to_nominator" },
      { id: "F10", fieldKey: "contact.shipping_address" }, { id: "F11", fieldKey: "contact.brief_description_of_your_situation" }] }));
    if (req.url === "/contacts/upsert") return res.end(JSON.stringify({ contact: { id: "C1" } }));
    res.end("{}");
  });
}).listen(18081);
process.env.GHL_BASE = "http://127.0.0.1:18081"; process.env.GHL_PIT = "test-pit"; process.env.GHL_LOCATION_ID = "LOC";
process.env.PORT = "18080";
const { server, e164 } = await import("./server.mjs");
server.listen(18080);
let ipn = 0; const post = (kind, body, headers = {}) => fetch(`http://127.0.0.1:18080/api/forms/${kind}`, { method: "POST", headers: { "Content-Type": "application/json", Origin: "https://www.redwhiteandclix.org", "X-Forwarded-For": `10.0.0.${++ipn}`, ...headers }, body: JSON.stringify(body) });
const old = Date.now() - 10000;

assert.equal(e164("(574) 265-9585"), "+15742659585"); assert.equal(e164("1-574-265-9585"), "+15742659585"); assert.equal(e164("12345"), "");
let r = await post("contact", { first_name: "Test", email: "t@example.com", message: "Hi", consent: "on", phone: "574 265 9585", t: old });
assert.equal(r.status, 200);
const up = calls.find((c) => c.p === "/contacts/upsert"); assert.equal(up.b.phone, "+15742659585"); assert.equal(up.b.customFields[0].id, "F1"); assert.equal(up.auth, "Bearer test-pit");
assert.ok(calls.some((c) => c.m === "DELETE" && c.p === "/contacts/C1/tags")); assert.deepEqual(calls.at(-1).b.tags, ["web-form-contact", "src-website"]);
r = await post("contact", { first_name: "Test", email: "bad", message: "", consent: "" , t: old}); assert.equal(r.status, 422); const e = (await r.json()).errors; assert.ok(e.email && e.message && e.consent);
calls.length = 0; r = await post("contact", { first_name: "Bot", email: "b@x.com", message: "spam", consent: "on", website: "http://spam" }); assert.equal(r.status, 200); assert.equal(calls.length, 0, "honeypot must not reach GHL");
r = await post("contact", { first_name: "Fast", email: "f@x.com", message: "x", consent: "on", t: Date.now() }); assert.equal(r.status, 200); assert.equal(calls.length, 0, "too-fast must not reach GHL");
r = await post("contact", { first_name: "x" }, { Origin: "https://evil.example" }); assert.equal(r.status, 403);
calls.length = 0; r = await post("volunteer", { first_name: "V", email: "v@x.com", phone: "5742659585", consent: "on", interests: ["Events", "Hacking"], t: old }); assert.equal(r.status, 200);
const vf = calls.find((c) => c.p === "/contacts/upsert").b.customFields.find((c) => c.id === "F2"); assert.deepEqual(vf.field_value, ["Events"], "unknown picklist values dropped");
r = await fetch("http://127.0.0.1:18080/api/forms/newsletter", { method: "POST", headers: { "X-Forwarded-For": "10.1.1.1", "Content-Type": "application/x-www-form-urlencoded", Origin: "https://www.redwhiteandclix.org", Referer: "https://www.redwhiteandclix.org/events" }, body: "email=n%40x.com&consent=on&t=" + old, redirect: "manual" });
assert.equal(r.status, 303); assert.match(r.headers.get("location"), /\/events\?form=sent#newsletter$/);
r = await post("nope", {}); assert.equal(r.status, 422);
let n = 0; for (let i = 0; i < 8; i++) { const x = await post("newsletter", { email: "r@x.com", consent: "on", t: old }, { "X-Forwarded-For": "9.9.9.9" }); if (x.status === 429) n++; } assert.ok(n >= 1, "rate limit");
console.log("all tests passed"); server.close(); mock.close();
