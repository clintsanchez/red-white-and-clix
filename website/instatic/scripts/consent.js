(function () {
  'use strict';

  // Cookie consent banner.
  //
  // The Cookie Policy makes promises this file has to keep literally:
  //
  //   * Nothing is set until the visitor clicks Accept. Google Analytics is not
  //     on the page at all beforehand — not loaded-and-paused. Decline sends no
  //     request to Google and sets no cookie.
  //   * The answer is remembered in localStorage, NOT in a cookie, because
  //     storing "no" in the thing they said no to is self-defeating.
  //   * The banner never nags. One answer, remembered.
  //
  // It is built in JS rather than authored into the layout because a visitor
  // with JS disabled cannot run Google Analytics either, so for them there is
  // nothing to consent to and no banner is the correct outcome.
  //
  // GA_MEASUREMENT_ID is deliberately empty. Until a real property exists the
  // banner records a choice and loads nothing, which keeps the build order the
  // policies promise: banner and policy pages first, tracking afterwards.
  // Setting the ID is NOT sufficient on its own — the published pages carry
  // `script-src 'self'`, which blocks googletagmanager outright. See
  // website/legal/IMPLEMENTATION.md.

  var GA_MEASUREMENT_ID = '';
  var STORAGE_KEY = 'rwc-consent';
  var COOKIE_MAX_AGE = 33696000; // 13 months, matching the Cookie Policy table

  function read() {
    try { return window.localStorage.getItem(STORAGE_KEY); } catch (e) { return null; }
  }

  function write(value) {
    // Private mode and blocked site data both throw. Failing to remember the
    // answer is survivable — asking again is. Failing loudly is not.
    try { window.localStorage.setItem(STORAGE_KEY, value); } catch (e) {}
  }

  function loadAnalytics() {
    if (!GA_MEASUREMENT_ID) return;
    if (window.__rwcAnalyticsLoaded) return;
    window.__rwcAnalyticsLoaded = true;

    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(GA_MEASUREMENT_ID);
    document.head.appendChild(s);

    window.dataLayer = window.dataLayer || [];
    function gtag() { window.dataLayer.push(arguments); }
    window.gtag = gtag;
    gtag('js', new Date());
    gtag('config', GA_MEASUREMENT_ID, {
      anonymize_ip: true,
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
      cookie_expires: COOKIE_MAX_AGE
    });
  }

  function dismiss(banner, value) {
    write(value);
    if (value === 'granted') loadAnalytics();
    banner.parentNode && banner.parentNode.removeChild(banner);
    // Hand focus somewhere sensible rather than dropping it on <body>, which
    // sends a screen reader back to the top with no explanation.
    var main = document.querySelector('main') || document.body;
    if (main && main !== document.body) {
      main.setAttribute('tabindex', '-1');
      main.focus({ preventScroll: true });
    }
  }

  function build() {
    if (document.querySelector('.rwc-consent')) return; // idempotent

    var banner = document.createElement('section');
    banner.className = 'rwc-consent';
    banner.setAttribute('role', 'region');
    banner.setAttribute('aria-label', 'Cookie choice');

    var copy = document.createElement('div');
    copy.className = 'rwc-consent-copy';

    var text = document.createElement('p');
    text.className = 'rwc-consent-text';
    text.appendChild(document.createTextNode(
      'We would like to count visits so we can see which pages help people find ' +
      'an event. Nothing is stored unless you say yes, and we never use it for ' +
      'advertising. '));

    [['/cookie-policy', 'Cookie Policy'],
     ['/privacy-policy', 'Privacy Policy'],
     ['/terms-and-conditions', 'Terms']
    ].forEach(function (pair, i, all) {
      var a = document.createElement('a');
      a.className = 'rwc-consent-link';
      a.href = pair[0];
      a.textContent = pair[1];
      text.appendChild(a);
      if (i < all.length - 1) text.appendChild(document.createTextNode(' · '));
    });

    copy.appendChild(text);

    var actions = document.createElement('div');
    actions.className = 'rwc-consent-actions';

    // Decline is built first so it comes first in the tab order, and both
    // buttons carry the same class. Nothing here should nudge toward yes.
    [['Decline', 'denied'], ['Accept', 'granted']].forEach(function (pair) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'rwc-consent-btn';
      b.textContent = pair[0];
      b.addEventListener('click', function () { dismiss(banner, pair[1]); });
      actions.appendChild(b);
    });

    banner.appendChild(copy);
    banner.appendChild(actions);

    // First child of <body> so keyboard users reach it without tabbing the
    // whole page, even though it is painted at the bottom.
    document.body.insertBefore(banner, document.body.firstChild);
  }

  function init() {
    var choice = read();
    if (choice === 'granted') { loadAnalytics(); return; }
    if (choice === 'denied') return;
    build();
  }

  // Footer "Cookie settings" link: the Cookie Policy tells people they can
  // change their mind, so there has to be a way that is not "clear your
  // browser storage".
  function wireReopen() {
    document.querySelectorAll('[data-rwc-consent-reopen]').forEach(function (el) {
      el.addEventListener('click', function (ev) {
        ev.preventDefault();
        try { window.localStorage.removeItem(STORAGE_KEY); } catch (e) {}
        build();
        var first = document.querySelector('.rwc-consent-btn');
        if (first) first.focus();
      });
    });
  }

  function boot() { init(); wireReopen(); }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
