# Performance Rules

## Cumulative Layout Shift (CLS)

- `<img>` needs explicit `width` and `height` attributes.
- Web fonts need `font-display: swap` or `font-display: optional`.
- No injecting content above existing content after load.

## Largest Contentful Paint (LCP)

- Above-fold hero images: `fetchpriority="high"` or framework `priority` prop.
- Critical fonts: `<link rel="preload" as="font" crossorigin>`.
- Add `<link rel="preconnect">` for CDN/asset domains.
- Target: hero LCP under 2.5s.

## Lazy Loading

- Below-fold images: `loading="lazy"`.
- Never lazy-load above-fold images.

## Rendering

- Large lists (50+ items): virtualize or use `content-visibility: auto`.
- No layout reads in render path (`getBoundingClientRect`, `offsetHeight`, `offsetWidth`, `scrollTop`).
- Batch DOM reads and writes. Never interleave.
- Prefer uncontrolled inputs. Controlled inputs must be cheap per keystroke.

## Assets

- Images served as WebP or AVIF with fallback.
- Responsive `srcset` on images with multiple sizes.
- SVGs inlined or sprited for icons, not raster.
