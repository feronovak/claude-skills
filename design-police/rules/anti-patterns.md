# Anti-Patterns (Instant FAIL)

Any match = automatic FAIL. No exceptions.

## Design System Violations

- Spacing scale compliance below 70% (see design-tokens.md for measurement)
- Font size not matching any step in type scale (5% tolerance)
- Color not in defined palette (deltaEOK > 0.05 from nearest palette color)
- One-off `box-shadow` not from shadow scale
- One-off `border-radius` not from radius tokens

## Typography Violations

- Body text line-length > 80 characters
- Font size below 14px anywhere
- Font weight below 400 in UI text
- All-caps text with default letter-spacing (0)
- Body line-height below 1.3

## Color Violations

- More than 5 distinct hues on a single screen
- More than 12 distinct colors on a single screen (count structural roles + brand accent only; semantic/category colors are separate - see color.md)
- APCA Lc below 75 for 16px/400 body text
- APCA Lc below 45 for non-text UI elements (icons, borders)
- Accent color exceeds 15% pixel coverage
- Pure white (#fff) body text in dark mode

## Layout Violations

- Horizontal scrollbar at any viewport
- Content exceeding viewport width
- Text overflowing its container
- Touch targets below 44x44px on mobile
- Page margins below 16px on mobile
- Max content width exceeding 1600px
- No `max-width` on text containers

## Interaction Violations

- Dropdown with physical gap between trigger and menu (`top: calc(100% + gap)` without bridge element)
- `target="_blank"` on internal/same-site links
- Inconsistent link behavior: same destination opens in new tab in one place, same tab in another

## Code-Level Violations

- `<div>` or `<span>` with click handlers instead of `<button>` or `<a>`
- `outline: none` without `:focus-visible` replacement
- Images without `alt` attribute
- Images without `width` and `height` attributes
- `transition: all` (must list properties)
- `user-scalable=no` or `maximum-scale=1` in viewport meta
- Hardcoded date/number formats instead of `Intl.*`
- `console.log` in production code
- Inline styles overriding the design system
- `!important` used to fix specificity

## Visual Violations (screenshot)

- Broken images (missing/404)
- Placeholder content ("Lorem ipsum", "TODO")
- Overlapping elements that aren't intentional layering
- No clear visual hierarchy (everything equal weight)
- Flash of unstyled content (FOUC)
