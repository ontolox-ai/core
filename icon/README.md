# Ontolox.ai — Weave mark

Geometry: 64-unit grid. Strands cross at 16 and 48, run 8 → 56, stroke 5.2 with round caps,
interlace break 7.8 (3.9 either side of a crossing), whole thing rotated 45°.
All eight tips land on one circle, r 28.3.

Interlace rule: every strand goes OVER at its first crossing and UNDER at its second.
Around the four corners, the over-strand alternates between the two directions.

## Colour
Fjord  #2E3440  strand 1, dark grounds
Slate  #5E81AC  strand 2, light-context accent
Ice    #88C0D0  strand 2 on dark grounds
Snow   #ECEFF4  strand 1 reversed

## Files
svg/ontolox-mark.svg              primary, two-tone, for light grounds
svg/ontolox-mark-mono.svg         single ink, inherits currentColor
svg/ontolox-mark-reversed.svg     Snow + Ice, for dark grounds
svg/ontolox-mark-simple.svg       interlace removed — use between 20 and 28 px
svg/ontolox-tile.svg              rounded-square app icon (mark at 70%)
svg/ontolox-avatar.svg            circular, social profiles (mark at 62%)
svg/ontolox-mark-favicon.svg      filled tile, two-tone
svg/ontolox-favicon-mono.svg      filled tile, one ink — best at 16 px
svg/ontolox-mark-animated.svg     self-drawing, SMIL, no JS
svg/ontolox-lockup-horizontal.svg mark + wordmark — outline the text before shipping
favicon.ico                       16 / 32 / 48
png/                              transparent raster exports, 16 → 1024

## Rules
Minimum size: 28 px for the primary. Below that use the simplified cut; below 20 px use the
favicon tile. Clear space: two "ticks" (a tick is 4.1 grid units, the stub past a crossing)
on all four sides. Don't recolour the strands outside the palette, don't add a third colour,
don't break the over/under alternation.
