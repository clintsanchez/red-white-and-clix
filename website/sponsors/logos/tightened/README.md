# Tightened logos — cleaned from the live site

For sponsors whose own site publishes nothing better, these are the live
Squarespace assets pulled at `?format=original` and cleaned up with
`../../tighten.py`. Two operations:

1. **Background knocked out.** A global "replace white" would punch holes
   through white letter interiors, so the script floods inward from the image
   border and clears only pixels CONNECTED to the edge. Edge pixels get partial
   alpha scaled by their distance from the background colour, so anti-aliased
   type does not turn into a jagged cut.
2. **Trimmed to content**, so no logo carries its own padding and the wall
   controls spacing. Then capped at 800px on the long edge — a wall slot is
   ~200px, so 800 covers 2x with headroom. 6.4MB to 2.8MB across the set;
   Instatic then generates WebP variants for delivery.

## The wall has to use light tiles

Checked by rendering the set on the dark page and on white tiles. On dark,
**Valvoline's navy wordmark, Wyrd's black type and PIP's "Print" all but
disappear**, and Gen Con's dark lockup fights the background. On white tiles
every one of the thirteen reads correctly. That is not a preference — a dark
sponsor wall would make several of these illegible.

## Two that needed different handling

- **Mission: Breakout** is white type on black: the black IS the lockup.
  Knocking it out hollowed the letters into outlines, so this one is trimmed
  only, black box intact.
- **DeFouw Automotive** was **discarded**. Its file is not a logo but a
  presentation mockup — black mark on a grey gradient with a drop shadow baked
  in. Cleaning that up would only launder a mockup into something that looks
  like a real asset. Ask DeFouw for their file.

## Deliberately NOT cleaned

`Blue Moon Comics` and `GamerMats` are AI-generated artwork (see
`06-Reports/sponsor-logo-audit.md`). Tightening a fabricated logo just makes
the fabrication look more convincing. They need real files from the businesses.

## Flag: the Sticker Ninja mark reads ".com.au"

The logo on the live site is for **StickerNinja.com.au**, an Australian
business. `stickerninja.com` is a different company. Before this goes live,
confirm with Wesley which one is the sponsor — this may be the wrong company's
logo entirely.
