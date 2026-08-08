# Typography Rules

Typography is the most important design layer - users read, not watch. Every rule here is measurable via computed styles.

## Font Pairing

**Max 3 font families.** Ideal is 2. Each must have a clear role:

| Role | Used for | Min weights required |
|------|----------|---------------------|
| Display / Heading | 20px+ sizes | 1 (the one you use), 3+ preferred |
| Body / Text | 15-21px running text | 4 minimum: 400, 400i, 700, 700i |
| Monospace | Code, tabular data only | 2: 400, 700 |

**FAIL if:**
- More than 3 font families loaded
- Body font missing Regular, Italic, Bold, or Bold Italic
- Display font used below 20px
- Monospace used outside `code`, `pre`, `kbd`, `samp` or tabular context
- Two fonts from the same sub-classification paired (two geometric sans, two transitional serifs)
- Decorative/script font used for body text
- Font weight below 400 for body text

**Pairing harmony:** x-height ratio between paired fonts must be within 10% when rendered at the same size. Superfamilies (Roboto+Roboto Slab, Source Sans+Source Serif, IBM Plex) auto-pass this check.

## Type Scale

All font sizes must follow a modular scale: `size = base * ratio^n` within 5% tolerance.

| Content type | Base | Ratio | Why |
|-------------|------|-------|-----|
| Editorial / long-form | 18-21px | 1.250 | Sustained reading needs larger text |
| Marketing / landing | 16-18px | 1.333-1.414 | Big jumps for visual impact |
| E-commerce / catalog | 14-16px | 1.200 | Dense info, many size levels |
| Documentation | 16px | 1.250 | Deep heading hierarchy |
| Dashboard / data | 13-14px | 1.125-1.200 | Maximum density |

**Size minimums:**
- Body text: **16px** (Butterick: 15-25px for screen)
- UI elements (buttons, nav): **14px**
- Captions, small text: **12px** absolute floor
- h1 must be >= **1.5x** body size
- Each heading level strictly larger than the one below: h1 > h2 > h3 > h4

## Line Length

- Body text: **45-75 characters**. Ideal: 65ch.
- FAIL if > **80 characters**.
- Marketing hero text can be wider (1-2 lines only).
- Constrain with `max-width` in `ch` units or px equivalent.

**Measurement:** Do NOT use `element.offsetWidth / (fontSize * 0.5)` - this measures the container, not the text, and overestimates by 20-40%. Instead use `Range.getClientRects()` to measure actual rendered line widths:
```js
const range = document.createRange();
range.selectNodeContents(el);
const maxLineWidth = Math.max(...[...range.getClientRects()].map(r => r.width));
const approxChars = Math.round(maxLineWidth / (fontSize * 0.55));
```
The 0.55 multiplier is more accurate for proportional sans-serif fonts (Inter, system-ui). For monospace, use 0.6. For serif body, use 0.5.

## Line Height

Inversely proportional to font size:

| Text type | Font size | Line height |
|-----------|-----------|-------------|
| Body copy | 14-18px | 1.5-1.7 |
| Subheadings | 20-24px | 1.25-1.35 |
| Headings | 30-48px | 1.1-1.25 |
| Display / hero | 48px+ | 1.0-1.15 |

**FAIL if:** body line-height < 1.4 (WCAG 1.4.12), heading line-height > 1.4, any line-height < 1.0.

## Heading Proximity

A heading belongs to the content BELOW it, not above. Space above must be larger than space below.

| Level | margin-top | margin-bottom | Ratio (min 2:1) |
|-------|-----------|---------------|-----------------|
| h1 | 0 (page-level) or 48px | 16px | 3:1 |
| h2 | 40px | 12px | 3.3:1 |
| h3 | 32px | 8px | 4:1 |
| h4 | 24px | 8px | 3:1 |

**FAIL if:** any heading has margin-top <= margin-bottom. The heading is visually equidistant from content above and below - breaking Proximity.

## Paragraph Spacing

- Standard: **1em** (16px for 16px body). Butterick: 50-100% of body size.
- First-line indent OR paragraph spacing. **Never both.**
- First paragraph after heading: no indent, no extra spacing.

**Spacing hierarchy (must be distinct steps):**
- Between lines: line-height (24px at 16px/1.5)
- Between paragraphs: 1em (16px)
- Between subsections: 2em (32px)
- Between sections: 3-5em (48-80px)
- Between major regions: 6-8em (96-128px)

## Text Color Hierarchy

**Max 4 non-semantic text colors** (primary, secondary, muted, disabled):

| Role | Light mode OKLCH L | Dark mode OKLCH L |
|------|-------------------|-------------------|
| Primary (headings, body) | 0.15-0.25 | 0.87-0.93 |
| Secondary (descriptions) | 0.40-0.50 | 0.65-0.75 |
| Muted (captions, timestamps) | 0.55-0.65 | 0.50-0.60 |
| Disabled | 0.65-0.75 | 0.40-0.50 |

**FAIL if:**
- More than 6 non-semantic text colors on a page
- Two text roles with OKLCH L difference < 0.10 (indistinguishable - merge them)
- Primary-to-secondary L difference < 0.18
- Grey text (chroma < 0.01) on colored background (chroma > 0.03) - use white with opacity or same-hue lighter color instead
- Pure white (#fff) body text in dark mode - use L 0.87-0.93
- Heading color hue differs > 15 degrees from body text (h2-h6)

**Headings and body use the same color.** Hierarchy comes from size and weight, not color. Exception: h1/hero heading may use a brand accent.

## Link Colors

Links must be distinguishable by more than color alone:
- **Underlined links:** can match body text color
- **Non-underlined links:** must have 3:1 contrast ratio (WCAG) / APCA Lc >= 25 vs body text, plus underline or other visual cue on hover/focus

## All-Caps Text

- `letter-spacing` must be **0.05-0.12em** when `text-transform: uppercase`
- FAIL if all-caps text has default letter-spacing

## Fluid Type

If using `clamp()`:
- Body never below **16px** at any viewport
- Body never above **24px** at any viewport
- No font size decreases as viewport increases
- Adjacent scale steps differ by at least **2px** at any viewport

## Content Rules

- `font-variant-numeric: tabular-nums` on number columns, prices, statistics
- `text-wrap: balance` on headings (prevents orphans)
- Active voice: "Install the CLI" not "The CLI will be installed"
- Specific button labels: "Save API Key" not "Submit"
- Error messages include fix or next step
- Numerals for counts: "8 deployments" not "eight"

## Card Typography

Inside cards, spacing is 50-75% of page-level:
- Heading to description: **8px**
- Description to metadata: **12-16px**
- Card padding: **16-24px**
- Image to heading: **12-16px**

## i18n

- Dates/times: `Intl.DateTimeFormat`, never hardcoded
- Numbers/currency: `Intl.NumberFormat`, never hardcoded
