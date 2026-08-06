# Layout Rules

## Max Content Width

- Content area: **1200-1440px** max. Absolute ceiling: 1600px.
- Text blocks specifically: **45-75ch** (roughly 640-900px for body text).
- FAIL if any text block exceeds 80ch.

## Page Margins

| Viewport | Minimum margin (each side) |
|----------|---------------------------|
| < 600px (mobile) | 16px |
| 600-904px (tablet) | 24px |
| >= 905px (desktop) | 24px (or auto with max-width) |

## Grid System

| Viewport | Columns | Gutter |
|----------|---------|--------|
| < 600px | 4 | 8-16px |
| 600-904px | 8 | 12-16px |
| >= 905px | 12 | 16-24px |

- Gutter must be from spacing scale (multiple of 4 or 8).
- Gutter consistent within a row.

## Responsive Breakpoints

Test at: **320, 480, 768, 1024, 1280, 1440, 1920px**.

At every breakpoint, check:
1. `document.body.scrollWidth <= window.innerWidth` (no horizontal scroll)
2. All elements: `computedWidth <= viewportWidth`
3. Body font size >= 14px (mobile), >= 16px (desktop)
4. Body text line-length 45-75ch
5. No overlapping elements (check via `getBoundingClientRect` intersections)
6. Images: `max-width: 100%` or equivalent, not overflowing

**Signs of breaking (FAIL):**
- Horizontal scrollbar
- Text overflows container
- Elements overlap unintentionally
- Touch targets < 44x44px on mobile
- Fixed-width elements that don't resize
- Nav items disappear without hamburger alternative
- Font size below 14px

**Signs of adapting (PASS):**
- Multi-column to single-column
- Navigation collapses to hamburger/drawer
- Font sizes adjust but stay in readable range
- Grid columns reduce (12 -> 8 -> 4)
- Spacing reduces proportionally but stays on scale

## Aspect Ratios

Standard ratios: 1:1, 4:3, 3:2, 16:9, 21:9, 2:3, 3:4

- All images within the same component type: same aspect ratio (+/-5%)
- Video containers: 16:9 (+/-2%)
- Flag any image/container not within 5% of a standard ratio

## Density & Whitespace

| Page type | Whitespace ratio |
|-----------|-----------------|
| Dashboard / data table | 30-40% |
| Standard page | 40-60% |
| Editorial / reading | 50-70% |
| Landing page | 60-75% |

FAIL if < 30% (cramped) or > 80% (empty).

## Component Spacing

| Element | Vertical padding | Horizontal padding |
|---------|-----------------|-------------------|
| Buttons | 8-16px | 16-24px |
| Cards | 16-24px | 16-24px |
| Input fields | 8-12px | 12-16px |
| Modals | 24-32px | 24-32px |

All must be from spacing scale.

**Section spacing:** 48-128px between major sections (3x-8x base spacing unit).

## Container-Content Fit

- Image containers must fit their content. If a container (gallery, lightbox, card frame) is visually larger than the image inside it, the empty space reads as broken. The container should match the image aspect ratio, or the image should fill the container (`object-fit: cover` or `width: 100%`).
- Card action rows (buttons at card bottom) need the same horizontal padding as the card body. If the body has 20px padding but the action row has 0px, buttons appear to float at the card edge.
- Same component on different pages must have consistent spacing. If a card has 20px body padding on the homepage, it must have 20px on every page. Check by comparing the component's computed padding across routes.

## Floating Sections

A section with only 1-2 small elements (a price + a button) in a large vertical space looks "lost" - visually disconnected from the content above and below. This violates Proximity.

**FAIL if:** A section's content height is less than 25% of its total height (including padding). The content is drowning in whitespace. Fix by: reducing padding, adding a background/border to give the section visual weight, or merging it into the adjacent section.

## Touch Targets

- Minimum: **44x44px** on mobile viewports
- Recommended: **48x48px**
- Spacing between targets: minimum **8px**
- Measure via `getBoundingClientRect()` on all interactive elements at mobile viewport

**Measurement:** Use `Math.round()` before comparing - subpixel rendering can produce 43.99px for a 44px element. Compare with `Math.round(rect.width) < 44 || Math.round(rect.height) < 44`. Elements at exactly 44px PASS.

## Intrinsic Layout Rules

Prefer intrinsic values over magic numbers:
- `max-width: 65ch` over `max-width: 743px`
- `gap: var(--space-m)` over `margin-left: 23px`
- `flex-basis: 20rem` over `width: 320px`

Flag any pixel literal in padding/margin/gap/width that isn't on the spacing scale.

## Safe Areas

- Full-bleed layouts: `env(safe-area-inset-*)` for notched devices
- Modals/drawers: backdrop covers full viewport, content doesn't overflow behind it
