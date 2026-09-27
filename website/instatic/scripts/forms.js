// Website forms -> /api/forms/<kind> (deploy/railway/forms) -> GoHighLevel.
//
// Every <form data-rwc-form="kind"> posts natively without JavaScript (the
// endpoint answers with a 303 back to the page plus ?form=sent|error#kind).
// This script upgrades that to an in-place submit with inline messages, adds
// the spam honeypot (Instatic strips tabindex/aria-hidden, so it is injected
// here), stamps the fill-time field, and pre-selects a sponsor tier from
// ?level= on the Support Us page.
//
// Error styling is inline on purpose: Instatic applies reusable classes above
// any state rule, so a `.rwc-input.is-invalid` rule would never win.
const RED = "#ff8a8a";

function status(form, text, ok) {
  const el = form.querySelector(".rwc-form-status");
  if (!el) return;
  el.textContent = text;
  el.style.color = ok ? "#b7f7c4" : RED;
  // The class hides it by default (its placeholder must not show without JS),
  // so an inline "block" is needed to override the class.
  el.style.display = text ? "block" : "none";
}

// Each form lands on its own confirmation page (noindex,nofollow), which is
// what GA4 counts as the conversion. The inline message is only a fallback.
const THANKS = { contact: "/thank-you/contact", sponsor: "/thank-you/sponsor", volunteer: "/thank-you/volunteer", newsletter: "/thank-you/newsletter" };

function sent(form) {
  const next = THANKS[form.dataset.rwcForm];
  if (next && !location.pathname.startsWith("/thank-you/")) { location.assign(next); return; }
  const msg = form.dataset.success || "Thanks. We got it.";
  [...form.children].forEach((c) => { if (!c.classList.contains("rwc-form-status")) c.style.display = "none"; });
  status(form, msg, true);
  form.querySelector(".rwc-form-status")?.focus?.();
}

function collect(form) {
  const out = {};
  for (const [k, v] of new FormData(form)) {
    if (k in out) out[k] = [].concat(out[k], v); else out[k] = v;
  }
  return out;
}

function markErrors(form, errors) {
  form.querySelectorAll("[aria-invalid]").forEach((el) => { el.removeAttribute("aria-invalid"); el.style.borderColor = ""; el.style.outline = ""; });
  let first = null;
  for (const name of Object.keys(errors)) {
    const el = form.querySelector(`[name="${name}"]`);
    if (!el) continue;
    el.setAttribute("aria-invalid", "true");
    el.style.borderColor = RED;
    el.style.outline = `2px solid ${RED}`;
    first = first || el;
  }
  first?.focus();
  status(form, Object.values(errors).join(". ") + ".", false);
}

function init(form) {
  const kind = form.dataset.rwcForm;
  const statusEl = form.querySelector(".rwc-form-status");
  if (statusEl) { statusEl.textContent = ""; statusEl.style.display = "none"; statusEl.setAttribute("tabindex", "-1"); }

  // Honeypot: off-screen, unreachable by keyboard, hidden from assistive tech.
  const trap = document.createElement("div");
  trap.setAttribute("aria-hidden", "true");
  trap.style.cssText = "position:absolute;left:-10000px;width:1px;height:1px;overflow:hidden";
  trap.innerHTML = '<label>Leave this empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label>';
  form.appendChild(trap);

  let t = form.querySelector('input[name="t"]');
  if (!t) { t = document.createElement("input"); t.type = "hidden"; t.name = "t"; form.appendChild(t); }
  t.value = String(Date.now());

  const qs = new URLSearchParams(location.search);
  if (location.hash === `#${kind}` && qs.get("form") === "sent") sent(form);   // legacy no-JS return
  if (location.hash === `#${kind}` && qs.get("form") === "error") status(form, "That didn't go through. Please check the form and try again.", false);
  const level = qs.get("level");
  if (level && kind === "sponsor") {
    const sel = form.querySelector('select[name="sponsor_level"]');
    if (sel && [...sel.options].some((o) => o.value === level)) sel.value = level;
  }

  // Capture phase + stopImmediatePropagation so no other form handler also
  // submits this form.
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    e.stopImmediatePropagation();
    const btn = form.querySelector('button[type="submit"]');
    const label = btn?.textContent;
    if (btn) { btn.disabled = true; btn.textContent = "Sending…"; }
    status(form, "", true);
    try {
      const r = await fetch(form.getAttribute("action"), {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(collect(form)),
      });
      const data = await r.json().catch(() => ({}));
      if (r.ok) return sent(form);
      if (r.status === 422 && data.errors) return markErrors(form, data.errors);
      status(form, data.error || "That didn't go through. Please try again, or email redwhiteandclix@gmail.com.", false);
    } catch {
      status(form, "We couldn't reach the server. Please try again, or email redwhiteandclix@gmail.com.", false);
    } finally {
      if (btn) { btn.disabled = false; btn.textContent = label; }
    }
  }, true);
}

document.querySelectorAll("form[data-rwc-form]").forEach(init);
