# Interaction Rules

## Forms

- Inputs need `autocomplete` and meaningful `name`.
- Use correct `type` (`email`, `tel`, `url`, `number`) and `inputmode`.
- Never block paste on any input.
- Labels clickable via `for`/`htmlFor` or wrapping the control.
- Disable spellcheck on emails, codes, usernames.
- Checkboxes/radios: label + control share single hit target. No dead zones between label and input.
- Submit button stays enabled until request starts. Show spinner during request.
- Errors inline next to fields. Focus first error on submit.
- Placeholders show example pattern and end with `...` or `_`.
- Warn before navigation with unsaved changes (`beforeunload` or router guard).

## Touch

- Touch target sizes: see `rules/layout.md` Touch Targets section (canonical thresholds).
- `touch-action: manipulation` to prevent double-tap zoom delay.
- Set `-webkit-tap-highlight-color` intentionally.
- `overscroll-behavior: contain` in modals, drawers, sheets.
- During drag: disable text selection, `inert` on dragged elements.

## Animation

- Honor `prefers-reduced-motion` (reduced variant or disable).
- Animate only `transform` and `opacity` (compositor-friendly).
- Never `transition: all`. List properties explicitly.
- Set correct `transform-origin`.
- Animations interruptible. Respond to user input mid-animation.

## Hover & Interactive States

- All buttons and links need `hover:` state with visual feedback.
- Interactive states increase contrast: hover/active/focus more prominent than rest.
- Hover styles must not be the only indicator of interactivity (mobile has no hover).

## Dropdowns & Hover Menus

- No physical gap between trigger and dropdown. A gap in the DOM means the mouse leaves the trigger's `:hover` zone before reaching the dropdown, causing it to close. Fix: use `padding-top` on the dropdown element itself (not `top: calc(100% + gap)`), or an invisible bridge element.
- Dropdown must remain open while mouse moves from trigger into dropdown content.
- Dropdown must close on mouse leave from the entire trigger+dropdown area, not just the trigger.
- Keyboard: dropdown must open on Enter/Space, close on Escape, support arrow-key navigation inside.

## Link Target Consistency

- Internal links (`/path`, `#anchor`, same-domain) must open in the same tab. Never `target="_blank"` for same-site navigation.
- External links (different domain) may open in new tab with `target="_blank" rel="noopener noreferrer"`.
- All links of the same type should behave consistently. If "Bundle" links to `/bundle` in the nav without `_blank`, the hero CTA linking to `/bundle` must also not use `_blank`.
- FAIL if `target="_blank"` is hardcoded on a component that handles both internal and external URLs.

## Navigation & State

- URL reflects state. Filters, tabs, pagination, expanded panels in query params.
- Links use `<a>` (support Cmd/Ctrl+click, middle-click).
- Destructive actions need confirmation modal or undo window. Never immediate.
- `autoFocus` sparingly. Desktop only, single primary input. Avoid on mobile.
