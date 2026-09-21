# Claude Design Prompt — Red White and Clix Master Brand Design Kit

You are acting as a senior brand systems designer, creative director, information designer, accessibility specialist, copywriter, and production designer.

Create a complete, polished, editable **Red White and Clix master brand design kit** using the facts, rules, copy, and deliverables in this brief. This is a production system for a real nonprofit. It must be usable by staff, volunteers, designers, social-media managers, sponsors, and vendors.

Do not ask broad discovery questions before starting. Build the complete first version from this brief. If a required fact is unresolved, preserve an obvious editable placeholder labeled `CONFIRM BEFORE PUBLISHING` rather than inventing an answer.

---

# 1. Deliverable

Create a coherent design-kit document and editable component library covering:

1. Brand overview and strategy
2. Logo rules and production variants
3. Color and accessibility system
4. Typography and hierarchy
5. Layout, grid, spacing, cards, buttons, badges, and dividers
6. Photography, illustration, icon, pattern, and texture direction
7. Brand voice and writing rules
8. Complete messaging hierarchy and approved copy bank
9. Event, donation, sponsor, volunteer, impact, resource, merchandise, and contact applications
10. Social and digital system references
11. Print and presentation applications
12. Asset manifest and naming rules
13. Governance and quality-control checklist

Everything must remain editable. Use components, variants, named layers, variables/tokens, reusable styles, grids, and auto layout where supported. Do not flatten the master templates.

Organize the final system into clearly named pages or sections:

- `00 / Read Me First`
- `01 / Brand Foundation`
- `02 / Logo System`
- `03 / Color System`
- `04 / Typography`
- `05 / Layout and Components`
- `06 / Photography and Graphics`
- `07 / Voice and Messaging`
- `08 / Event Applications`
- `09 / Fundraising and Sponsor Applications`
- `10 / Social and Digital`
- `11 / Print and Presentation`
- `12 / Asset Library`
- `13 / Quality Control`

---

# 2. Brand facts

**Brand name:** Red White and Clix  
**Short form:** RWC, only after the full name appears  
**Legal name:** Red White and Clix Inc.  
**Website:** https://www.redwhiteandclix.org/  
**Email:** redwhiteandclix@gmail.com  
**Phone:** +1 574-265-9585  
**Primary market:** Lafayette and West Lafayette, Indiana; wider Midwest draw  
**Industry/category:** Veteran-serving nonprofit and veteran-founded tabletop event community  
**Primary game:** HeroClix  
**Founder and brand guardian:** Wesley Robertson  
**Agency:** BlakSheep Creative  
**Federal status:** IRS record supports 501(c)(3) status, a March 2026 ruling, and deductible contributions. Do not treat the ruling date as the founding date.

**Current annual event:** November 7–8, 2026, Lafayette National Guard Armory, 5218 Haggerty Lane, Lafayette, Indiana 47905.

Known event formats:

- RWC 300 Modern — November 7, 2026
- Team Sealed, 3v3 — November 8, 2026

**Important operational constraint:** Public sources currently conflict on event prices and purchase routes. Every price field, registration button, hotel rate, beneficiary allocation, attendance total, fundraising total, sponsor status, and Team Sealed fee basis must remain an editable `CONFIRM BEFORE PUBLISHING` field unless a newly supplied source resolves it.

The website/IRS mailing address and the event venue have different roles. Label addresses precisely. Never imply that the event venue is the permanent organization office.

---

# 3. Brand foundation

## Mission

Bring people together through well-run tabletop gaming events that create camaraderie, raise awareness, and support veteran-focused causes.

## Vision

Become the Midwest’s most trusted veteran-founded tabletop event community.

## Brand promise

A welcoming seat, a well-run event, and an honest account of the mission each person’s participation supports.

## Positioning

Red White and Clix is the veteran-founded tabletop event community for players and supporters who want serious play, genuine connection, and a clear way to support veteran causes.

## Values

### Belonging by design

Newcomers, regular players, veterans, and families should feel that there is a place for them. Inclusion is an operating standard.

### Play with purpose

The game must be enjoyable and competently run. The cause adds meaning; it does not excuse a weak event.

### Service without spectacle

Veterans are people with agency, humor, skill, and community. Avoid pity, trauma-centered imagery, partisan framing, and emotional manipulation.

### Transparent impact

Fees, beneficiaries, donation allocation, and outcomes should be understandable and supported by records.

### Camaraderie in action

Playing, volunteering, sponsoring, giving, and returning each year turn a room of participants into a durable community.

## Personality

Energetic, human, accessible, purposeful, bold, welcoming, organized, and respectful.

## Primary aspirational benchmark

Stack Up is the founder’s original model for what RWC could become. Learn from Stack Up’s gaming-native veteran mission, clear program architecture, multiple participation paths, and transparency. Do not copy its visual identity, tactical vocabulary, national scope, or program claims. Translate those strengths into an in-person, HeroClix-centered Midwest event system.

Other veteran-serving competitors are Operation Gratitude and Wounded Warrior Project. Do not classify general HeroClix tournaments or charities serving unrelated causes as direct competitors.

---

# 4. Audience

## Competitive tabletop player

Wants clear formats, credible rulings, worthwhile competition, accurate schedules, and a reason the trip is worth making.

## Veteran or military-family participant

Wants camaraderie and respect without being treated as a symbol, patient, or fundraising prop.

## New or returning player

Wants rules explained, expectations clarified, and a low-friction path into a community that will not exploit inexperience.

## Sponsor or community-partnership lead

Wants a credible local activation, clearly defined benefits, professional materials, and documented outcomes.

## Donor, volunteer, or community supporter

Wants to understand the mission, the beneficiary, the action available, and what the contribution made possible.

---

# 5. Logo system

The client-supplied raster logo is the current authority: `red-white-and-clix-logo.png`.

Preserve its stacked red, white, and blue wordmark, star, and battlefield-cross detail. Treat the military memorial symbolism with restraint. Never use it as a decorative texture.

Create or specify these production masters:

- Primary stacked lockup
- Horizontal lockup
- One-color dark version
- One-color light version
- Simplified small-size icon
- Favicon
- Social avatar master

If you cannot produce a faithful vector without redrawing the artwork inaccurately, create a vector-redraw specification and use the supplied raster logo in the layouts. Never ask generative AI to recreate the logo.

**Minimum digital size:** 120 CSS pixels for the full current mark.  
**Clear space:** at least 10% of the mark’s width on all sides.

Do not stretch, crop, recolor, rotate, outline, add shadows, add glow, rearrange elements, rebuild the wordmark with a font, or place the mark directly over visually busy photography.

---

# 6. Color system

## Established logo colors

| Token | HEX | RGB | Use |
|---|---|---|---|
| `logo.red` | `#FF0000` | 255, 0, 0 | Existing logo and large non-text accents |
| `logo.blue` | `#0072FF` | 0, 114, 255 | Existing logo and large non-text accents |
| `logo.white` | `#FFFFFF` | 255, 255, 255 | Existing logo and reversed surfaces |
| `logo.black` | `#000000` | 0, 0, 0 | Existing logo |

## Accessible interface colors

| Token | HEX | Use |
|---|---|---|
| `action.red` | `#B91C1C` | Primary buttons with white text |
| `action.blue` | `#0050B3` | Links, information, secondary actions |
| `ink.primary` | `#111827` | Body text and dark surfaces |
| `surface.light` | `#F5F7FA` | Light background |
| `surface.white` | `#FFFFFF` | Cards and open space |
| `border.neutral` | `#D1D5DB` | Dividers and quiet outlines |

The bright logo red and blue fail the 4.5:1 requirement against white for normal text. Use the darker interface colors for text, buttons, labels, and small controls. Preserve the bright values inside the logo.

Recommended visual ratio: 60% light/white surfaces, 20% ink/dark surfaces, 10% blue, 10% red. Red should indicate action or urgency and should not dominate every design.

Do not introduce unrelated patriotic colors, camouflage palettes, neon gaming palettes, metallic gradients, or flag textures.

---

# 7. Typography

**Display:** Archivo Black 400  
**Body/interface:** Space Grotesk 400, 500, 600, 700  
**Fallback:** Arial, sans-serif

Do not reconstruct the logo using these fonts.

| Role | Typeface | Weight | Suggested desktop | Suggested mobile | Use |
|---|---|---:|---:|---:|---|
| Display/H1 | Archivo Black | 400 | 56–72 px | 36–48 px | One short hero statement |
| H2 | Archivo Black | 400 | 36–48 px | 28–36 px | Major sections |
| H3 | Space Grotesk | 700 | 24–30 px | 21–26 px | Cards and subsections |
| Body large | Space Grotesk | 500 | 20 px | 18 px | Intros |
| Body | Space Grotesk | 400 | 16–18 px | 16–18 px | Reading copy |
| Label/button | Space Grotesk | 700 | 14–16 px | 14–16 px | Actions and metadata |
| Caption/source | Space Grotesk | 400 | 12–14 px | 12–14 px | Sources and notes |

Keep Archivo Black headlines short. Use sentence case. Avoid long all-caps paragraphs. Maintain at least 1.5 line height for body copy.

---

# 8. Layout and component direction

Use a disciplined 8-pixel spacing base. Suggested tokens: 4, 8, 12, 16, 24, 32, 48, 64, 96.

Use clean grids, generous space, bold concise headings, clear logistics, and subtle tabletop-grid geometry. Use square or lightly rounded cards, modest shadows, and firm borders. Avoid bubbly consumer-app styling, heavy glass effects, distressed military treatments, or dense patriotic decoration.

Create components for:

- Logo and lockups
- Primary, secondary, and text-link buttons
- Event date/location badge
- Format badge
- Registration status badge
- Sponsor tier badge
- Quote/testimonial card
- Impact statistic card
- Event detail card
- Schedule/timeline
- New-player explainer
- Beneficiary/partner card
- Donation allocation card
- CTA band
- Source/citation line
- Photo caption and consent/provenance label
- Alert for changed logistics
- `CONFIRM BEFORE PUBLISHING` production warning

Buttons should use clear actions: Register, View Event Details, Donate, Become a Sponsor, Volunteer, Read the Impact Report, and Get Veteran Resources.

---

# 9. Photography and graphic direction

Prioritize authentic photographs of:

- Players at real tables
- Welcoming interactions and rules explanations
- Wide event-room views
- Organizers working
- Group moments
- Prize or recognition moments
- Sponsors and beneficiaries in verified context
- Founder images when approved

Use natural color, eye-level viewpoints, honest documentary framing, and moderate contrast. Do not apply a heavy cinematic grade.

Label archive photographs accurately. Treat generated imagery and product mockups as illustration, never documentary evidence. Never imply that an AI-generated person is a veteran, attendee, beneficiary, or founder.

Avoid:

- Camouflage as decoration
- Explosions, weapons, battle scenes, or aggressive tactical imagery
- Excessive flags
- Pity-oriented veteran portraits
- Fake military uniforms or medals
- Unverified sponsor logos
- Generic esports neon
- AI text embedded into imagery

Use simple consistent line icons. Optional graphic devices may include clean grid lines, table/map geometry, measured red/blue edge accents, star points, and restrained game-token shapes. Do not extract the battlefield-cross element for decorative repetition.

---

# 10. Voice and writing system

## Voice summary

Sound like an organized host who welcomes every player, respects veterans, and makes the next step clear.

## Traits

- **Welcoming:** Invite people in without insider tests.
- **Grounded:** Tie claims to dates, records, partners, and results.
- **Energetic:** Celebrate play without empty hype.
- **Respectful:** Treat veteran stories as human stories.
- **Practical:** Lead with what, when, where, price, and how.

Use active voice, short paragraphs, concrete verbs, contractions where natural, and one main CTA per item. Define tournament terminology for newcomers.

Use words such as play, join, welcome, table, community, camaraderie, compete, participate, veterans, support, sponsor, volunteer, transparent, and together.

Avoid partisan slogans, pity, “real gamers,” “broken veterans,” combat metaphors for routine marketing, guaranteed impact, medical claims, official military endorsement, invented totals, and “every dollar goes directly” unless verified records support it.

---

# 11. Messaging hierarchy and copy bank

## Current organizational line

**One Community. One Mission.**

## Recommended campaign line

**Play Together. Stand With Veterans.**

Treat the recommended line as provisional until Wesley approves it as a replacement or campaign line.

## Core message

Tabletop play creates a place to belong and a practical way to stand with veterans.

## Value proposition

Red White and Clix brings players together for well-run tabletop events where competition, camaraderie, and veteran support share the same table.

## Short description

Veteran-founded tabletop events where players compete, connect, and support veteran-focused causes—together, at the same table.

## Fifty-word description

Red White and Clix brings gamers, veterans, families, and supporters together through organized tabletop events. Players get a welcoming, competitive experience. Partners get a practical way to participate in a veteran-focused mission rooted in Lafayette, Indiana, and built for the wider Midwest community.

## Elevator pitch

Red White and Clix is a veteran-founded nonprofit that uses organized HeroClix events to build community and support veteran-focused causes. The experience combines credible competition, welcoming camaraderie, and transparent participation. Players, veterans, families, volunteers, donors, and sponsors all have a practical way to take part.

## Message pillars

### A seat at the table

Welcoming events give experienced players and newcomers a clear way to participate.

Suggested headlines:

- There’s a seat at the table for you.
- New to HeroClix? Start here.
- Come for the game. Find your community.

### Competition with camaraderie

Strong formats and fair play make the event worth attending.

Suggested headlines:

- Serious play. A mission bigger than the standings.
- Bring your best team—and your best sportsmanship.
- Compete hard. Welcome generously.

### Purpose you can understand

RWC names its supported organizations and reports confirmed outcomes without exaggeration.

Suggested headlines:

- See what your participation supports.
- Clear purpose. Accountable impact.
- The event ends. The support continues.

### Veteran-founded and locally rooted

The mission comes from lived service and grows through Midwest relationships.

Suggested headlines:

- Built in Indiana. Open to the wider gaming community.
- Veteran-founded. Community-powered.
- Local tables. Shared purpose.

## Audience messages

**Competitive players:** A serious HeroClix weekend with clear formats, strong competition, and a mission bigger than the standings.

**Veterans and families:** A welcoming table built around camaraderie, respect, and participation.

**Newcomers:** You don’t need to know everyone—or everything—to take a seat.

**Sponsors:** Put your support into a visible community event with defined benefits and documented outcomes.

**Donors:** Understand the beneficiary, the purpose, and the confirmed result before you give.

## Calls to action

Primary: **Register for an Event**  
Secondary: **Donate**, **Become a Sponsor**, **Volunteer**, **Shop in Support**, **View Veteran Resources**

---

# 12. Required application templates

Create editable examples for:

- Brand overview page
- Event announcement poster
- Event schedule
- Registration card
- Format explainer
- New-player guide
- Venue/directions card
- Sponsor prospectus cover and tier page
- Sponsor thank-you
- Beneficiary spotlight
- Donation appeal
- Donation receipt/thank-you header
- Volunteer recruitment
- Impact report cover and statistic page
- Post-event results page
- Veteran-resource guide cover
- Merchandise promotion
- Email header
- Presentation title and content slides
- Letterhead
- One-page organization overview
- Business card or contact card
- Social avatar and profile banner reference

Use realistic RWC copy. For any unresolved fee, total, testimonial, sponsor, beneficiary term, or outcome, display an obvious editable placeholder. Never fabricate proof.

---

# 13. Accessibility

- Meet WCAG AA contrast for normal text.
- Maintain readable mobile type.
- Do not rely on red versus blue alone to communicate meaning.
- Give charts direct labels, symbols, or patterns.
- Define alt-text guidance for meaningful images.
- Keep essential text out of platform crop and interface zones.
- Make veteran-resource and crisis information plain, direct, and separate from promotional CTAs.

---

# 14. Quality control

Before finalizing, verify:

- Official supplied logo used without alteration
- Logo bright colors kept separate from accessible UI colors
- Archivo Black and Space Grotesk used correctly
- One clear content hierarchy
- Authentic imagery prioritized
- No partisan or militarized decorative framing
- No unsupported medical, financial, attendance, sponsor, or impact claims
- No unconfirmed event fee or registration route treated as final
- Event venue and mailing address labeled separately
- One primary CTA per asset
- Mobile and small-thumbnail readability checked
- Source/date component present where statistics appear
- Every template is editable and semantically named

Finish with a concise inventory of every created page, component, template, token, and unresolved approval item.

