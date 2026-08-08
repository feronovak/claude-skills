# Color Rules

## APCA Contrast (replaces WCAG 2.x ratio)

APCA (Advanced Perceptual Contrast Algorithm) is more accurate than WCAG's
simple ratio. It accounts for font size, weight, and polarity.

**Do not hand-compute this. `scripts/probe.js` returns `Lc`, `floor` and
`target` for every text element on the page.** The formula has two polarity
branches, a soft-clamp for near-black values, and a ±0.027 offset; retyping it
from memory drops one of those and silently mis-scores every light-text-on-dark
element — which is every primary button you will ever audit.

### Two thresholds, and they are not the same thing

Conflating these is the single most common way this audit produces a wrong
answer. A legible white-on-blue CTA at Lc 80 is *fine*; failing it because a
table somewhere says "90" burns the developer's trust in every other line of
the report.

| | what it means | what you do |
|---|---|---|
| **floor** | below this, the text is genuinely hard to read | **FAIL** |
| **target** (floor + 15) | the bar you'd hit with a free hand | note it, never fail it |

**Floors** (compare `|Lc|` — polarity is already handled inside the algorithm):

| condition | floor |
|---|---|
| >= 36px, or >= 24px and bold | 45 |
| >= 24px, or >= 18px and bold | 55 |
| >= 18px | 60 |
| >= 16px | 68 |
| 14–15px | 75 |

Weight 700 subtracts 5; weight 600 subtracts 3 — heavier strokes stay readable
at lower contrast.

**Non-text** (icons, borders, focus rings): floor Lc 45.
**Genuinely disabled/placeholder controls:** floor Lc 30. Do not use this as an
excuse for low-contrast body copy.

These floors are anchored on APCA's own published levels: Lc 90 preferred for
body text, 75 the minimum for columns of body text, 60 for spot reading and
headlines, 45 for large or bold text and non-text elements.

## 60-30-10 Color Proportion

Pixel coverage on each viewport:

| Role | Target | Acceptable |
|------|--------|-----------|
| Dominant (backgrounds) | 60% | 55-70% |
| Secondary (surfaces, cards) | 30% | 20-35% |
| Accent (CTAs, highlights) | 10% | 3-12% |

**FAIL if accent exceeds 15%.** If everything is accented, nothing is.

**Measurement:** Screenshot, quantize to palette colors (group within deltaEOK < 0.05), count pixel coverage. Mask `<img>` elements before measuring.

## Palette Limits (per screen)

- Max 3 chromatic hues (excluding semantic error/warning/success/info)
- Max 5 total hues (including semantic)
- Max 12 distinct colors (deltaEOK > 0.05 apart)
- Neutral hues within 15 degree range in OKLCH
- No one-off colors outside the defined palette

**Counting text colors:** When counting distinct text colors, separate into categories:
- **Structural roles** (primary, secondary, muted, disabled, on-dark variants) — max 4 per surface context (light surface, dark surface)
- **Semantic colors** (niche/category tags, error, success, warning) — don't count against the 10-max text color limit
- **Brand accent** (link color, CTA text) — counts as 1 regardless of hover/active variants

A site with 4 light-surface text roles + 4 dark-surface text roles + 1 brand accent + 3 semantic category colors = 12 computed colors but is well-structured. Report the breakdown, not just the raw count. FAIL only if non-semantic, non-role colors appear (one-off values with no systematic purpose).

## OKLCH Palette Quality

For sites that define a design system palette:

- **Cross-hue lightness:** Same step across hues: OKLCH L within +/-0.02
- **Step spacing:** delta-L between consecutive steps uniform within +/-0.015
- **Chroma smoothness:** max 0.05 jump between adjacent steps
- **Gamut:** all colors within sRGB (0-255 per channel)

## Dark Mode

If the site supports dark mode, toggle `prefers-color-scheme: dark` in Playwright and re-check:

**Surface colors:**
- Base surface: OKLCH L = 0.13-0.17 (not pure black)
- Each elevation level: L increases by 0.015-0.03
- No colored surface above L = 0.50

**Text:**
- Body text: OKLCH L = 0.87-0.93 (not pure white L=1.0 - causes glare)
- Secondary text: L = 0.65-0.75

**Chroma:**
- All chromatic colors: reduce chroma 20-30% vs light mode
- Saturated colors on dark backgrounds cause visual vibration

**Elevation:**
- Don't use shadows for elevation in dark mode (invisible)
- Use surface tint + lightness increase instead

## On Colored Backgrounds

Don't overlay grey text on colored backgrounds. Use:
- White text with adjusted opacity, or
- A color from the same hue family at appropriate lightness
