# Claude Design Prompt — Red White and Clix Social Media Template System

You are acting as a senior social-media designer, brand-systems architect, campaign art director, information designer, accessibility specialist, and production copywriter.

Create a complete, reusable, editable social-media and digital-content template system for **Red White and Clix**. Use the brand rules and copy in this brief as the source of truth. Build a real system with components, variants, named text/image layers, safe zones, variables, and responsive recomposition—not isolated sample posts.

Do not pause for general discovery. Produce the complete first version. If a fee, registration link, beneficiary allocation, attendance number, fundraising result, sponsor relationship, hotel price, quote, or testimonial is unresolved, use a visible editable field labeled `CONFIRM BEFORE PUBLISHING`. Never invent facts.

---

# 1. Brand system to inherit

**Brand:** Red White and Clix  
**Category:** Veteran-serving nonprofit and veteran-founded tabletop event community  
**Primary market:** Lafayette/West Lafayette, Indiana and the Midwest  
**Primary game:** HeroClix  
**Website:** redwhiteandclix.org  
**Email:** redwhiteandclix@gmail.com  
**Phone:** 574-265-9585

**Mission:** Bring people together through well-run tabletop gaming events that create camaraderie, raise awareness, and support veteran-focused causes.

**Positioning:** The veteran-founded tabletop event community for players and supporters who want serious play, genuine connection, and a clear way to support veteran causes.

**Current organizational line:** One Community. One Mission.  
**Recommended campaign line:** Play Together. Stand With Veterans. — provisional pending approval.

**Voice:** An organized host who welcomes every player, respects veterans, and makes the next step clear.

**Personality:** Energetic, human, accessible, purposeful, bold, welcoming, organized, respectful.

**Primary CTA:** Register for an Event  
**Secondary CTAs:** Donate, Become a Sponsor, Volunteer, Shop in Support, View Veteran Resources

---

# 2. Visual tokens

## Logo

Use the supplied `red-white-and-clix-logo.png`. Preserve proportions. Minimum proposed full-mark size: 120 CSS pixels. Clear space: 10% of logo width. Never redraw, crop, stretch, recolor, outline, shadow, glow, rotate, or reconstruct the logo.

Do not extract the battlefield-cross detail as a repeating decorative motif.

## Colors

| Token | Value | Use |
|---|---|---|
| `logo.red` | `#FF0000` | Logo and large non-text accents |
| `logo.blue` | `#0072FF` | Logo and large non-text accents |
| `logo.white` | `#FFFFFF` | Logo and light surfaces |
| `logo.black` | `#000000` | Logo |
| `action.red` | `#B91C1C` | Accessible red buttons/labels |
| `action.blue` | `#0050B3` | Accessible blue links/information |
| `ink.primary` | `#111827` | Text and dark surfaces |
| `surface.light` | `#F5F7FA` | Light background |
| `border.neutral` | `#D1D5DB` | Dividers |

Do not place normal-size white text on `#FF0000` or `#0072FF`; use the darker action colors.

## Typography

- Display headlines: Archivo Black 400
- Body, labels, UI, captions: Space Grotesk 400/500/600/700
- Fallback: Arial, sans-serif
- Use sentence case
- Keep display copy short
- Maintain mobile readability

## Visual direction

Use real event tables, players interacting, rules explanations, room-wide views, organizers, groups, prizes, sponsors, and beneficiary context when verified. Use natural color and documentary framing. Separate archival, generated, mockup, and documentary images.

Avoid camouflage, distressed flags, explosions, weapons, trauma-centered veteran imagery, fake uniforms, unverified logos, excessive patriotism, generic esports neon, and AI-generated people presented as real participants.

Use clean grids, generous space, direct logistics, strong editorial hierarchy, subtle tabletop/map geometry, and restrained red/blue edge accents.

---

# 3. Architecture

Use this dependency model:

`RWC Brand Tokens → Social Components → Content Family → Platform Format → Final Asset`

Build reusable components for:

- Logo lockup
- Eyebrow/category label
- Headline
- Body copy
- Event date badge
- Venue/location line
- Format badge
- Registration-status badge
- CTA button
- Website footer
- Source/date line
- Photo caption
- Sponsor logo rail
- Partner/beneficiary card
- Impact statistic
- Quote/testimonial
- Carousel page number
- Swipe indicator
- Alert/update banner
- `CONFIRM BEFORE PUBLISHING` warning

Use variants instead of duplicate components.

---

# 4. Master sizes

Create responsive master families and recompose intelligently:

- Square: 1080 × 1080
- Portrait feed: 1080 × 1350
- Vertical/story/reel: 1080 × 1920
- Landscape/link preview: 1200 × 630
- Widescreen/video: 1920 × 1080
- YouTube thumbnail: 1280 × 720
- Facebook cover: 851 × 315
- Facebook event cover: current editable platform specification
- YouTube banner: 2560 × 1440 with critical content in the central safe zone
- LinkedIn company cover: 1128 × 191
- X header: 1500 × 500
- Google Business Profile square and landscape masters

Maintain a central `Platform Specifications` page with width, height, ratio, safe zone, crop behavior, date checked, and notes. Platform dimensions must be editable configuration values.

Do not merely resize one composition. Recompose hierarchy for each ratio.

---

# 5. Required platform families

Create templates for:

## Facebook

- Square, portrait, landscape, story, reel cover
- Page cover, event cover, profile image
- Link preview
- Event, update, offer, fundraiser, sponsor, volunteer, photo recap

## Instagram

- Square and portrait feed
- Story and reel cover
- Square and portrait carousel
- Profile image

## LinkedIn

- Landscape, square, portrait
- Company cover and logo
- Carousel
- Sponsor/partner announcement
- Impact and annual-report graphics

## YouTube

- Channel banner and avatar
- Long-form thumbnail
- Shorts cover/reference frame
- Playlist cover
- Community square and portrait

## Google Business Profile

- Update, event, announcement, photo, offer, sponsor, review, and cover-style image
- Prioritize small-display legibility

## Optional shared masters

Create adaptable versions for TikTok, X, Threads, Bluesky, Pinterest, Reddit, and email/link previews. Do not imply RWC owns an account on any platform unless a verified account is supplied.

---

# 6. Content families and exact sample text

Create every family below in square, portrait, vertical, and landscape where appropriate. Use the supplied text as editable sample content.

## A. Brand/mission statement

**Headline:** Play Together. Stand With Veterans.  
**Body:** Red White and Clix brings players together for well-run tabletop events where competition, camaraderie, and veteran support share the same table.  
**CTA:** Learn About the Mission

Alternative:

**Headline:** One Community. One Mission.  
**Body:** Veteran-founded tabletop events rooted in Lafayette, Indiana, and built for the wider Midwest gaming community.

## B. Save the date

**Eyebrow:** Save the Date  
**Headline:** Red White and Clix 2026  
**Date:** November 7–8, 2026  
**Location:** Lafayette National Guard Armory · Lafayette, Indiana  
**CTA:** Event details at redwhiteandclix.org

## C. 300 Modern event

**Eyebrow:** Saturday Event  
**Headline:** RWC 300 Modern  
**Date:** November 7, 2026  
**Venue:** Lafayette National Guard Armory  
**Price:** CONFIRM BEFORE PUBLISHING  
**Registration URL:** CONFIRM BEFORE PUBLISHING  
**CTA:** Register for 300 Modern

## D. Team Sealed event

**Eyebrow:** Sunday Event  
**Headline:** Team Sealed · 3v3  
**Date:** November 8, 2026  
**Venue:** Lafayette National Guard Armory  
**Price and whether per team:** CONFIRM BEFORE PUBLISHING  
**Registration URL:** CONFIRM BEFORE PUBLISHING  
**CTA:** View Team Sealed Details

## E. Event logistics/update

**Headline:** Event Update  
**Body template:** `[DETAIL] has changed. The current information is [CONFIRMED DETAIL]. Please use [AUTHORITATIVE LINK] for registration and updates.`  
**CTA:** View Current Details

Design this to feel direct and calm, not alarming.

## F. New-player welcome

**Headline:** New to HeroClix? There’s a seat for you.  
**Body:** You don’t need to know everyone—or everything—to take part. Review the format, bring your questions, and join a community that values fair play and helpful competition.  
**CTA:** Read the New-Player Guide

Do not promise coaching, loaners, or beginner divisions unless operationally confirmed.

## G. Competition message

**Headline:** Serious play. A mission bigger than the standings.  
**Body:** Clear formats, fair competition, real camaraderie, and a veteran-focused purpose.  
**CTA:** See the Event Schedule

## H. Veteran/family message

**Headline:** Camaraderie starts with a shared table.  
**Body:** RWC creates a welcoming activity where veterans, families, gamers, and supporters can participate as peers.  
**CTA:** Join the Community

Avoid clinical outcome claims.

## I. Donation appeal

**Headline:** Help put purpose behind every table.  
**Body:** Your gift supports Red White and Clix and its veteran-focused mission. Review the current beneficiary and allocation details before you donate.  
**Beneficiary:** CONFIRM BEFORE PUBLISHING  
**Allocation:** CONFIRM BEFORE PUBLISHING  
**CTA:** Donate

## J. Donation transparency

**Headline:** Know what your gift supports.  
**Fields:** Beneficiary · Event expenses · Program support · Amount transferred · Reporting date  
Every result remains `CONFIRM BEFORE PUBLISHING` until verified.

## K. Sponsor recruitment

**Headline:** Put your brand behind a community that shows up.  
**Body:** Support a veteran-founded tabletop event with defined sponsor benefits, an engaged in-person audience, and documented follow-through.  
**CTA:** Become a Sponsor

## L. Sponsor spotlight

**Eyebrow:** Community Partner  
**Headline:** Thank you, [APPROVED SPONSOR NAME]  
**Body:** Your support helps make the Red White and Clix event possible.  
**Permission status:** CONFIRM BEFORE PUBLISHING  
**CTA:** Meet Our Partners

## M. Volunteer recruitment

**Headline:** Help us run a table worth returning to.  
**Body:** Volunteers support check-in, logistics, hospitality, setup, teardown, and the participant experience.  
**Available roles/date:** CONFIRM BEFORE PUBLISHING  
**CTA:** Volunteer With RWC

## N. Beneficiary spotlight

**Eyebrow:** Supported Organization  
**Headline:** [CONFIRMED BENEFICIARY NAME]  
**Body:** `[Approved description of the organization and the relationship.]`  
**CTA:** Learn Where the Support Goes

Do not imply endorsement or use a logo without permission.

## O. Impact statistic

Create layouts for one, two, three, and four metrics.

Permitted labels:

- Confirmed registrations
- Event attendance
- Volunteers
- Sponsors
- Funds raised
- Funds transferred
- Returning participants
- Resource-guide visits

Every number needs a source and date. Use `[VERIFIED NUMBER]` placeholders in the master examples.

## P. Post-event results

**Headline:** What We Accomplished Together  
**Body:** Thank you to every player, volunteer, sponsor, and supporter who took a seat and stood with veterans.  
**Metrics:** VERIFIED ATTENDANCE · VERIFIED FUNDS · CONFIRMED BENEFICIARY · REPORTING DATE  
**CTA:** Read the Impact Report

## Q. Founder/story

**Headline:** Veteran-founded. Community-powered.  
**Body:** Wesley Robertson created Red White and Clix to connect the camaraderie of tabletop gaming with a practical commitment to veteran support.  
**CTA:** Read the RWC Story

Use further service, health, memorial, or family details only when the supplied copy has explicit approval.

## R. Resource post

**Headline:** Looking for veteran support? Start here.  
**Body:** Find qualified local, state, and national resources in the RWC Veteran Resource Guide.  
**CTA:** View Veteran Resources

Keep crisis resources direct and separate from fundraising CTAs.

## S. Merchandise

**Headline:** Wear the mission. Support the community.  
**Body:** Shop current Red White and Clix merchandise through the official store.  
**Store URL and product availability:** CONFIRM BEFORE PUBLISHING  
**CTA:** Shop RWC

## T. FAQ

Create a single-question card and carousel system for:

- When and where is the next event?
- Which HeroClix formats are offered?
- How do I register?
- Is Red White and Clix a nonprofit?
- Which veteran organization does this event support?
- How can my business sponsor the event?
- Can I volunteer?
- Is the event welcoming to newer players?

Answers involving price, allocation, exact registration process, beginner support, or beneficiary terms must remain `CONFIRM BEFORE PUBLISHING` until verified.

## U. Quote/testimonial

Create quote, review, and testimonial variants with name, role/context, date, source, and permission status. Use `[APPROVED TESTIMONIAL]` in the master. Never invent a quote or star rating.

## V. Educational carousel

Create these complete sequences:

### Your first RWC event

1. Cover: Your First Red White and Clix Event
2. Check the current format and registration link
3. Review the schedule and venue details
4. Bring required game materials
5. Ask questions and practice good sportsmanship
6. Meet the community and learn what the event supports
7. CTA: View the Current Event Guide

### How participation supports the mission

1. Cover: From the Table to the Mission
2. Players register for a confirmed event
3. Sponsors and volunteers help make the gathering possible
4. RWC documents expenses and beneficiary terms
5. Confirmed support is transferred or delivered
6. Results are reported with sources and dates
7. CTA: Read the Latest Impact Report

### Five ways to take part

1. Register
2. Sponsor
3. Volunteer
4. Donate
5. Share verified event information
6. CTA: Choose Your Next Step

## W. Countdown

Create 30-day, 14-day, 7-day, 3-day, tomorrow, and today variants. Countdown templates must include current event, date, venue, registration status, and link fields. Do not use false urgency or claim low availability without evidence.

## X. Weather/change/cancellation

Create calm operational templates for schedule changes, venue changes, registration closing, sold-out status, weather notices, and cancellation. Every template must include timestamp, authoritative link, and contact method.

## Y. Photo recap

**Headline options:** Around the Tables · The Community in Play · Thank You for Showing Up  
Include event/date caption, photographer credit, consent status, and optional CTA to view results.

---

# 7. Carousel architecture

Create cover, context, content, summary, and CTA slide components. Include page numbering, optional swipe indicator, persistent small branding, consistent safe areas, and source/date components.

Create variants for:

- Event details
- New-player guide
- Format explainer
- Sponsor prospectus
- Beneficiary transparency
- Impact results
- FAQ
- Checklist
- Myth/fact
- Founder story
- Veteran-resource guide

---

# 8. Video and thumbnail system

Create vertical covers for Reels, Stories, TikTok, and Shorts reference frames with protected center content and interface-safe areas.

Create YouTube thumbnails for:

- Event announcement
- Format explanation
- Event recap
- Founder story
- Sponsor spotlight
- Beneficiary interview
- New-player guide
- Rules/update video

Rules: one idea, short headline, one dominant image, strong facial or tabletop focal point, minimal small text, and clear RWC recognition. Do not create clickbait expressions or unverified claims.

---

# 9. Chart and data system

Create accessible bar, stacked bar, line, donut, progress, KPI, timeline, and comparison components using approved brand-derived tokens. Include title, subtitle, direct values, legend, annotation, source, reporting period, and footnote.

Possible RWC metrics:

- Registrations by event
- Attendance by year
- Participant geography
- Referral source
- New versus returning players
- Sponsor support
- Volunteer hours
- Funds raised and transferred
- Website-to-registration conversion

Do not include sample numerical results. Use clearly labeled placeholders.

---

# 10. Footer, citation, and CTA rules

Footer variants:

- Compact: logo + website
- Standard: logo + website + one CTA
- Evidence: logo + source + reporting date
- Carousel: logo + page number + website

Citation formats:

- `Source: Organization, Year`
- `Source: Organization · Report title · Date`
- `Source: Red White and Clix registration records · Updated [DATE]`

Never fabricate a source.

Use one primary CTA per asset. Do not stack Register, Donate, Sponsor, Volunteer, and Shop with equal visual weight in one post.

---

# 11. Naming

Use semantic names such as:

- `Social / Feed / Portrait / Event Announcement`
- `Social / Feed / Square / Mission Statement`
- `Social / Story / Countdown`
- `Social / Carousel / New Player / Cover`
- `Social / Carousel / New Player / Content`
- `Social / Carousel / CTA`
- `Video / Thumbnail / Event Recap`
- `Banner / Facebook / Event`
- `Data / KPI / Three Metric`
- `Component / Event Details`
- `Component / Source and Date`
- `Component / Confirm Before Publishing`

---

# 12. Accessibility and quality control

Verify every template for:

- Correct RWC logo and proportions
- Approved colors and accessible contrast
- Archivo Black and Space Grotesk only
- Small-screen legibility
- Platform crop/safe-zone protection
- One clear headline and CTA
- Authentic imagery classification
- No partisan or trauma-centered framing
- No fabricated numbers, quotes, sponsors, prices, beneficiaries, or availability
- Accurate date and venue fields
- Source/date on every factual statistic
- Editable layers and reusable components
- No Lorem Ipsum
- No generic AI-brand styling

At completion, provide:

1. A platform specification page
2. A token/component inventory
3. A template inventory grouped by platform and content family
4. A list of every `CONFIRM BEFORE PUBLISHING` field
5. Export guidance for PNG, JPG, PDF, and video-cover use
6. A concise handoff guide explaining how staff should duplicate and edit templates safely

