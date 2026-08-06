# Accessibility Rules

## Semantic HTML

- `<button>` for actions, `<a>` for navigation. Never `<div onClick>` or `<span onClick>`.
- Use `<nav>`, `<main>`, `<header>`, `<footer>`, `<section>`, `<article>` before ARIA roles.
- Headings hierarchical `<h1>` through `<h6>`. No skipping levels.
- Include skip-to-main-content link.
- `scroll-margin-top` on heading anchors.

## ARIA

- Icon-only buttons need `aria-label`.
- Form controls need `<label>` or `aria-label`.
- Decorative icons need `aria-hidden="true"`.
- Async updates (toasts, validation errors) need `aria-live="polite"`.
- Don't duplicate native semantics with ARIA (`<button role="button">`).

## Keyboard

- All interactive elements reachable via Tab.
- Interactive elements need keyboard handlers (`onKeyDown`/`onKeyUp` or native element).
- Escape closes modals/dropdowns.
- Focus trapped inside open modals.

## Focus States

- All interactive elements need visible focus indicator.
- Never `outline: none` or `outline-none` without a replacement focus style.
- Use `:focus-visible` over `:focus` (no focus ring on mouse click).
- `:focus-within` for compound controls (search bar with button, etc).

## Images

- `<img>` needs `alt` text. Decorative images get `alt=""`.
- `alt` text describes function, not appearance ("Submit form" not "blue button").

## Color

- Contrast: defer to `rules/color.md` APCA thresholds (supersedes WCAG 2.x ratio for this skill).
- Information never conveyed by color alone (add icon, pattern, or text).
