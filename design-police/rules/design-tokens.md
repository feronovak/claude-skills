# Design Tokens (Core System Rules)

Everything in a well-designed UI comes from a constrained set of pre-defined values. If a value isn't on the scale, it's a violation.

## Spacing Scale

All margin, padding, and gap values must be from a 4px-base scale.

**Accepted values (px):** 0, 1, 2, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96

- 1px, 2px only for borders and fine separators.
- All other spacing must be multiples of 4px.
- Each step should increase by ~25%+ from previous (no linear scales like 4, 8, 12, 16, 20, 24, 28...).

**Measurement:** Extract all computed margin, padding, gap values via Playwright. Calculate compliance:
- **> 90% on scale** = PASS
- **70-90%** = FAIL (needs cleanup)
- **< 70%** = FAIL (no consistent scale)

## Type Scale

All font sizes must follow a modular scale: `size = base * ratio^n`.

**Recommended ratios by use case:**
- Dense UI / many heading levels: 1.200 (Minor Third) or 1.250 (Major Third)
- Standard web: 1.250 (Major Third) or 1.333 (Perfect Fourth)
- Marketing / few levels: 1.333-1.500

**Base size:** 16px (1rem). Never below 14px anywhere.

**Validation:** For each text element, compute which scale step it's closest to. If it deviates more than **5%** from any step in the scale, FAIL.

**Example scale (base 16px, ratio 1.250):**
- 10.24, 12.80, 16.00, 20.00, 25.00, 31.25, 39.06, 48.83, 61.04

**Max heading size:** h1 should not exceed 4.5x body size (72px for 16px base).

## Color Palette

**Palette structure:**
- Greys: 8-10 shades (most-used set)
- Primary: 1-2 hues, 9 shades each (100-900)
- Accents: 3-5 hues, ~5 shades each (semantic: error, warning, success, info + brand)
- Total: 40-65 distinct values max

**Palette constraints (measurable):**
- Max **3 chromatic hues** (excluding semantic colors) on a single screen
- Max **5 total hues** (including semantic) on a single screen
- Max **12 distinct colors** (deltaEOK > 0.05 apart) on a single screen
- Neutral palette must stay within **15 degrees hue range** in OKLCH
- No one-off colors. Every color on the page must match a palette value.

**Shade consistency (OKLCH):**
- Colors at the same "step" across hues: OKLCH L within **+/-0.02**
- Lightness steps between shades: delta-L uniform within **+/-0.015**
- Chroma jump between adjacent steps: max **0.05**

## Shadow Scale

5 levels. Each shadow uses two layers (tight + diffused). Bigger shadow = more elevation.

| Level | Use case |
|-------|----------|
| sm | Buttons, subtle depth |
| md | Cards, slight lift |
| lg | Dropdowns, popovers |
| xl | Floating panels |
| 2xl | Modals, dialogs |

**Rule:** All shadows on the page must come from a pre-defined scale. No one-off `box-shadow` values.

## Border Radius

Constrain to 3-5 named sizes. Small = professional, large = playful. Pick a personality and be consistent.

**Rule:** All `border-radius` values must match one of the defined tokens. Flag one-off values.

## Discovering the Site's Palette

Before checking palette membership, you need to know what the palette IS. Discover it in this priority order:

1. **CSS custom properties:** Look for `--color-*`, `--c-*`, `--theme-*` variables on `:root` or `html`. This is the most reliable source.
2. **Tailwind config:** Check `tailwind.config.*` for `theme.extend.colors`. Extract all defined color values.
3. **Design tokens file:** Look for `tokens.json`, `design-tokens.*`, or `theme.*` in the project.
4. **Extract and cluster:** If none of the above exist, extract all unique computed color values from the page, convert to OKLCH, cluster by deltaEOK < 0.05, and treat the clusters as the de facto palette. Flag if there are more than 12 clusters - the site likely has no intentional palette.

If discovery fails entirely, skip palette membership checks but still enforce hue count limits and contrast rules.

## Validation Script Approach

Run via `page.evaluate()` in Playwright:

```js
// Extract all spacing values
document.querySelectorAll('*').forEach(el => {
  const s = getComputedStyle(el);
  // Check margin, padding, gap against scale
});

// Extract all font sizes
// Check each against base * ratio^n within 5%

// Extract all colors
// Group by deltaEOK, count distinct, check palette membership
```
