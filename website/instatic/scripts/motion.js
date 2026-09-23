/**
 * Scroll motion, driven by GSAP + ScrollTrigger.
 *
 * Why JS and not CSS: the stylesheet asks for `rwc-reveal`, `rwc-media-pan`
 * and `rwc-row-in` via `animation-name`, but those three @keyframes blocks
 * were never emitted by `site_apply_css` (a known silent-drop). Every
 * scroll reveal on this site has therefore been inert in every browser.
 * `animation-timeline: view()` would not have rescued it either — Firefox
 * still does not support it. GSAP runs everywhere, so it owns scroll motion
 * outright and those dead CSS rules are deliberately left undefined so
 * nothing animates twice.
 *
 * GSAP 3.13 is self-hosted under /uploads/vendor/gsap/ because the page CSP
 * is `script-src 'self'` — a CDN tag would be blocked.
 *
 * Three rules keep this from looking like stock template motion:
 *   1. Anything already on screen at load is never animated. Fading in
 *      content the visitor is already reading is the classic tell, and it
 *      would flash because this script runs after paint.
 *   2. Reveals are grouped per container so siblings stagger together
 *      rather than each firing on its own trigger.
 *   3. Reduced-motion exits before GSAP is even fetched, so those visitors
 *      pay no bytes for motion they will not see.
 */

const REVEAL_SELECTOR = [
  '.rwc-card',
  '.rwc-row',
  '.rwc-vals2-item',
  '.rwc-res-card',
  '.rwc-st-card',
  '.rwc-tier',
  '.rwc-tier-item',
  '.rwc-vol-box',
  '.rwc-band-quote',
  '.rwc-cta',
].join(', ')

const PARALLAX_SELECTOR = '.rwc-card-img'

const GSAP_BASE = '/uploads/vendor/gsap/'

/** Inject a classic script tag; same-origin, so the CSP allows it. */
function loadScript(src) {
  return new Promise((resolve, reject) => {
    const tag = document.createElement('script')
    tag.src = src
    tag.onload = () => resolve()
    tag.onerror = () => reject(new Error(`Failed to load ${src}`))
    document.head.appendChild(tag)
  })
}

/**
 * True when the element is already within the viewport at init. Those are
 * left alone — see rule 1 above.
 */
function alreadyOnScreen(element) {
  const rect = element.getBoundingClientRect()
  return rect.top < window.innerHeight && rect.bottom > 0
}

/** Group elements by their parent so siblings share one staggered trigger. */
function groupByParent(elements) {
  const groups = new Map()
  for (const element of elements) {
    const parent = element.parentElement
    if (!parent) continue
    if (!groups.has(parent)) groups.set(parent, [])
    groups.get(parent).push(element)
  }
  return groups
}

async function init() {
  // Exit before fetching 116KB of animation library.
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return

  try {
    await loadScript(`${GSAP_BASE}gsap.min.js`)
    await loadScript(`${GSAP_BASE}ScrollTrigger.min.js`)
  } catch (error) {
    // Content is already in its final state, so a failed load costs nothing
    // but the motion itself.
    console.warn('[rwc-motion]', error)
    return
  }

  const { gsap, ScrollTrigger } = window
  if (!gsap || !ScrollTrigger) return
  gsap.registerPlugin(ScrollTrigger)

  const candidates = Array.from(document.querySelectorAll(REVEAL_SELECTOR)).filter(
    (element) => !alreadyOnScreen(element),
  )

  // A `from` tween sets opacity 0 the moment it is created. If anything threw
  // after that point the content would stay invisible for good, which is far
  // worse than no animation — so failure clears every style GSAP applied.
  try {
    for (const [parent, elements] of groupByParent(candidates)) {
      gsap.from(elements, {
        opacity: 0,
        y: 28,
        duration: 0.7,
        ease: 'power2.out',
        stagger: elements.length > 1 ? 0.08 : 0,
        scrollTrigger: {
          trigger: parent,
          start: 'top 85%',
          once: true,
        },
      })
    }
  } catch (error) {
    console.warn('[rwc-motion] reveal setup failed, restoring content', error)
    gsap.killTweensOf(candidates)
    gsap.set(candidates, { clearProps: 'all' })
    return
  }

  // Transform-only parallax on card art. No opacity, so there is nothing to
  // flash even on an element that was visible at load.
  for (const image of document.querySelectorAll(PARALLAX_SELECTOR)) {
    const frame = image.parentElement
    if (!frame) continue
    // Overfill the frame first so the travel cannot expose an edge.
    gsap.set(image, { scale: 1.12, transformOrigin: 'center center' })
    gsap.fromTo(
      image,
      { yPercent: -4 },
      {
        yPercent: 4,
        ease: 'none',
        scrollTrigger: {
          trigger: frame,
          start: 'top bottom',
          end: 'bottom top',
          scrub: true,
        },
      },
    )
  }

  // Late-loading images change page height and would leave triggers at stale
  // offsets.
  window.addEventListener('load', () => ScrollTrigger.refresh())
}

init()
