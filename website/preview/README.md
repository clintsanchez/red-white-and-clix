# Red White and Clix — website preview

Open `index.html` in a browser. The four core pages, fonts, styles and photographs are local and work without a build step or web server. `review.html` explains unresolved facts and the intended review sequence.

Included: Home, Events, Our story, Give, and an internal review page. Registration and donation controls are disabled until authoritative destinations and fees are supplied. Email/phone links open the user's chosen apps; resource and shop links lead to the existing external site. No form submission, payment, analytics, backend or production deployment is configured.

The original primary logo is used. The alternate vector lockups remain separate review options. Imagery is taken from the documented client archive; publication requires context/permission review. `assets/images/provenance.json` preserves the source records.

Platform, budget, scope, launch date and maintenance owner remain unresolved. This preview is framework-free and does not choose a migration path. All pages are marked noindex/nofollow for review; that metadata is not authentication and does not make a public upload private.

Rebuild HTML with `python3 tools/build.py` in the original agency repository. Edit shared styling in `site.css`. The exported preview folder itself has no Python dependency.
