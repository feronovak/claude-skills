# Typography Presets by Content Type

Reference file. Load when you need to evaluate whether typography choices match the content type, or when recommending improvements.

## Quick Reference

| Property | Editorial | Marketing | E-commerce | Docs | Dashboard |
|----------|-----------|-----------|------------|------|-----------|
| Base size | 18-21px | 16-18px | 14-16px | 16px | 13-14px |
| Scale ratio | 1.250 | 1.333-1.414 | 1.200 | 1.250 | 1.125-1.200 |
| Body line-height | 1.6-1.8 | 1.5-1.6 | 1.4-1.5 | 1.5-1.7 | 1.3-1.4 |
| Line length | 60-75ch | 45-65ch | 30-50ch cards | 70-80ch | N/A (tables) |
| Max heading levels | 3 | 2-3 | 3 | 5-6 | 3 |
| Font approach | Serif body | Sans dominant | Sans throughout | Sans + mono | Sans + mono |

## Editorial / Long-form

Optimized for sustained reading. Medium uses 21px, NYT 17px serif, Substack 18px.

```
Body:      18-21px, serif, line-height 1.7, max-width 65ch
h1:        39-48px, line-height 1.1
h2:        25-30px, margin-top 2.5em, margin-bottom 0.75em
h3:        20-24px, margin-top 2em, margin-bottom 0.5em
Paragraph: margin-bottom 1.2em
```

Special: `hyphens: auto`, `text-rendering: optimizeLegibility`, generous margins. Serif body reads better for 2000+ word pieces.

## Marketing / Landing

Visual impact. Short text blocks. CTA-focused. Stripe, Linear, Vercel patterns.

```
Eyebrow:   12-14px, uppercase, 500 weight, letter-spacing 0.08em, accent color
Hero h1:   48-72px, 700-800 weight, line-height 1.1
Sub-hero:  18-20px, 400 weight, muted color, max-width 540px
Section h2: 36-48px, 600-700 weight
Body:      16-18px, 400 weight
CTA:       15-16px, 600 weight
```

Special: large whitespace between sections (80-120px). Weight contrast (300-800) matters more than size.

## E-commerce / Catalog

Dense information. Shopify Dawn uses 15-16px, Apple Store 17px.

```
Product title:  18-20px, 600 weight
Product desc:   14-15px, 400 weight, line-clamp 2-3 on cards
Price:          18px, 700 weight, tabular-nums
Price original: 16px, 400 weight, line-through, muted color
Price sale:     18px, 700 weight, error/accent color
Card text:      14px, line-height 1.4
```

Special: `font-variant-numeric: tabular-nums` on all prices. Right-align numbers in tables. Truncate card titles at 2 lines.

## Documentation / Technical

Scannable. Deep hierarchy. Stripe Docs, MDN, Tailwind Docs patterns.

```
Body:       16px, sans-serif, line-height 1.7, max-width 75ch
Code block: 14-15px, monospace, line-height 1.5, padding 16-20px
Inline code: 0.875em, background rgba(0,0,0,0.05), padding 2px 6px, radius 3px
h1:         32px (page title)
h2:         24px (major section)
h3:         20px (subsection)
h4:         16px bold (detail - same size as body)
h5:         14px bold (sub-detail)
```

Special: `scroll-margin-top` for anchored headings. 3-column layout (nav 240px, content, TOC). Admonitions 14-15px with colored left border.

## Dashboard / Data

Maximum density. Vercel, Linear, Grafana patterns.

```
Body:          14px, sans-serif, line-height 1.35
Table header:  12px, 500 weight, uppercase, letter-spacing 0.04em, muted
Table cell:    13-14px, 400 weight
Cell numbers:  tabular-nums, right-aligned
Cell mono:     12-13px (IDs, hashes)
KPI number:    24-36px, 600 weight
Status badge:  11-12px, uppercase, letter-spacing 0.04em, 500 weight
Row height:    36-44px
```

Special: `tabular-nums` everywhere numbers appear. No serif fonts. Truncate with `text-overflow: ellipsis` in cells.

## Dark Mode Adjustments (all types)

- Reduce font-weight slightly (white-on-dark appears bolder due to halation)
- Use `-webkit-font-smoothing: antialiased` to compensate
- Body text L = 0.87-0.93, not pure white
- Surface L = 0.13-0.17, not pure black
- Reduce chroma 20-30% on all chromatic text
