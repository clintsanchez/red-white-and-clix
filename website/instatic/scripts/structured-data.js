(function () {
  'use strict';

  // Emits JSON-LD. Instatic strips <script> from HTML imports, so schema
  // cannot be authored into a template — it has to be built at runtime. The
  // better home is a publish.html plugin filter, which would put it in the
  // static HTML; move it there if the plugin route is ever proven out.
  //
  // Everything here is READ FROM THE PAGE rather than restated. A second copy
  // of the dates or the address is a second thing to forget to update, and a
  // schema that disagrees with the visible page is worse than no schema.

  var ORIGIN = 'https://www.redwhiteandclix.org';

  function meta(sel, attr) {
    var el = document.querySelector(sel);
    return el ? (el.getAttribute(attr || 'content') || '').trim() : '';
  }

  function emit(obj) {
    var s = document.createElement('script');
    s.type = 'application/ld+json';
    s.textContent = JSON.stringify(obj);
    document.head.appendChild(s);
  }

  function organisation() {
    return {
      '@context': 'https://schema.org',
      '@type': 'NGO',
      name: 'Red, White, and Clix',
      url: ORIGIN + '/',
      logo: ORIGIN + '/uploads/rwc/logo.png',
      email: 'redwhiteandclix@gmail.com',
      telephone: '+1-574-265-9585',
      description: 'A veteran-founded nonprofit running tabletop gaming events that raise awareness and support for veteran-focused causes.'
    };
  }

  function event() {
    var el = document.querySelector('[data-rwc-event]');
    if (!el) return null;

    var start = el.getAttribute('data-start');
    var end = el.getAttribute('data-end');
    var title = el.getAttribute('data-title');
    var venue = el.getAttribute('data-venue');
    var rawAddress = el.getAttribute('data-address') || '';
    var address = rawAddress.replace(/\s+/g, ' ').trim();
    if (!start || !title) return null;

    // The dates are authored without an offset. Lafayette is Eastern, and the
    // event falls after DST ends, so it is EST. Leaving this off makes Google
    // read the times as UTC and show them five hours out.
    function withOffset(d) { return /[Z+-]\d\d:?\d\d$/.test(d) ? d : d + '-05:00'; }

    // The attribute is authored over two lines:
    //   5218 Haggerty Lane
    //   Lafayette, IN 47905
    // That line break is the only reliable street/city boundary — collapsing
    // it first makes "5218" the street and "Haggerty Lane Lafayette" the city,
    // because no regex can tell a two-word street from a two-word town.
    var street = address, city = '', region = '', postal = '';
    var lines = rawAddress.split(/\r?\n/).map(function (l) { return l.trim(); }).filter(Boolean);
    var tail = (lines.length > 1 ? lines[lines.length - 1] : address);
    var mm = tail.match(/^([A-Za-z .'-]+),\s*([A-Z]{2})\s*(\d{5})$/);
    if (mm && lines.length > 1) {
      street = lines.slice(0, -1).join(' ');
      city = mm[1]; region = mm[2]; postal = mm[3];
    } else {
      mm = null;
    }

    var place = { '@type': 'Place', name: venue || undefined };
    if (mm) {
      place.address = {
        '@type': 'PostalAddress',
        streetAddress: street,
        addressLocality: city,
        addressRegion: region,
        postalCode: postal,
        addressCountry: 'US'
      };
    } else if (address) {
      place.address = address;
    }

    var ev = {
      '@context': 'https://schema.org',
      '@type': 'Event',
      name: title,
      startDate: withOffset(start),
      eventStatus: 'https://schema.org/EventScheduled',
      eventAttendanceMode: 'https://schema.org/OfflineEventAttendanceMode',
      location: place,
      organizer: { '@type': 'NGO', name: 'Red, White, and Clix', url: ORIGIN + '/' },
      url: meta('link[rel="canonical"]', 'href') || location.href
    };
    if (end) ev.endDate = withOffset(end);

    var desc = meta('meta[name="description"]');
    if (desc) ev.description = desc;

    var img = meta('meta[property="og:image"]');
    if (img) ev.image = img;

    // Entry fees run from $10 (Learn to Play) upward and vary by event, so
    // only the floor is asserted. Claiming a single price would be wrong.
    ev.offers = {
      '@type': 'AggregateOffer',
      priceCurrency: 'USD',
      lowPrice: '10',
      availability: 'https://schema.org/InStock',
      url: ORIGIN + '/register'
    };

    return ev;
  }

  function init() {
    try {
      emit(organisation());
      var ev = event();
      if (ev) emit(ev);
    } catch (e) {
      // Never let a schema problem break a page.
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
