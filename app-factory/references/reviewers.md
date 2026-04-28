# Phase 3 Reviewers

5 specialist reviewers run in parallel after QA completes. Each is independent — they don't read each other's output.

## Visual Design Reviewer
**Model:** Sonnet
**Reads:** `docs/design-system.md`, `docs/component-specs.md`, all source code (CSS, components)
**Writes:** `docs/review-visual-design.md`
**Enhanced by:** `interface-design:audit` + `interface-design:critique` — if available, you MUST run these skills as your PRIMARY audit. They catch violations and craft issues the built-in methodology will miss. Run the built-in checks below ONLY to supplement gaps.

### System Compliance Audit (built-in, always runs)
1. **Token adherence** — grep source code for raw color values (hex, rgb, hsl not from tokens), hardcoded spacing (px values not from scale), raw font sizes. Every visual value should trace back to design-system.md.
2. **Spacing consistency** — all spacing values are multiples of the base unit defined in design-system.md. No magic numbers.
3. **Depth strategy compliance** — design-system.md declares a depth strategy (borders-only, shadows, surface shifts, etc.). Check that ONE strategy is used throughout. Mixed approaches = system violation.
4. **Color palette compliance** — every color in source traces to the token architecture (foreground, background, border, brand, semantic). No ad-hoc hex values.
5. **Component fidelity** — compare each implemented component against component-specs.md: all variants built? All states handled? Props match spec?
6. **Responsive consistency** — spot-check at mobile (390px), tablet (768px), desktop (1280px). Layouts break? Touch targets below 44px on mobile?

### Craft Critique (built-in, always runs)
Go beyond "does it match the spec" — evaluate whether the design feels intentional.

1. **Swap Test** — mentally swap the typeface for Inter/system default, or swap layout for a standard Bootstrap-style template. Would anyone notice the difference? If not, the design defaulted to generic.
2. **Squint Test** — blur your eyes at each page. Can you perceive clear hierarchy? Is the primary action obvious? Does anything jump out inappropriately? Craft whispers, doesn't shout.
3. **Signature Test** — the design-system.md should declare a signature element. Can you find it in 5+ specific places in the implementation? Not "overall feel" — actual components.
4. **Token Test** — read the CSS variable names. Do they sound like they belong to THIS product, or could they belong to any project? (`--ink` and `--parchment` vs `--gray-700`)
5. **Visual hierarchy** — each page has a clear primary action, logical eye flow, intentional whitespace (not leftover space)
6. **Typography hierarchy** — all 4 text levels (primary, secondary, tertiary, muted) used consistently. Font weights create clear distinction.
7. **Depth & motion** — elevation creates consistent layering. Transitions are smooth, purposeful, not decorative.

### Anti-Pattern Detection
Flag these if found — they indicate design defaulting:
- System/generic fonts (Inter, Roboto, Arial) without justification
- Purple gradients on white backgrounds
- Symmetric card grids with no hierarchy variation
- Sidebar with different background color than canvas (fragments the interface)
- Harsh borders (should barely be visible, not demand attention)
- Pure white cards on colored backgrounds
- Multiple accent colors (dilutes focus)
- Shadow and border mixing (pick one depth strategy)

- **Rate:** Visual Polish (1-10), Design System Adherence (1-10)

## UX & Accessibility Reviewer
**Model:** Sonnet
**Reads:** `docs/product-spec.md`, `docs/ux-flows.md`, all source code
**Writes:** `docs/review-ux-a11y.md`

### UX Audit Methodology
1. **Flow completeness** — walk through each P0 user flow from ux-flows.md. Can a user complete it end-to-end? Are there dead ends?
2. **Error handling** — what happens when things go wrong? Form validation errors are clear and helpful? Network failures show useful messages?
3. **Empty states** — first-time user sees helpful onboarding, not blank screens. Empty lists have illustration + action.
4. **Loading states** — data-dependent views show skeletons or spinners, not layout shifts.
5. **Navigation clarity** — user always knows where they are (active nav state, breadcrumbs). Back navigation works as expected.

### Accessibility Audit (WCAG AA)
1. **Keyboard navigation** — tab through every interactive element. Focus order is logical (top-left to bottom-right, not jumping around). All functionality is reachable without a mouse.
2. **Focus indicators** — every focused element has a visible ring/outline. Focus-visible is used (shows on keyboard, not mouse click).
3. **Semantic HTML** — check for: landmarks (header, nav, main, aside, footer), heading hierarchy (h1 → h2 → h3, no skips), form labels (visible, connected via htmlFor/for), lists (ul/ol for list content, not divs).
4. **ARIA usage** — check for: aria-label on icon-only buttons, aria-describedby on inputs with help text, aria-expanded on toggles/dropdowns, aria-live on dynamic content, role attributes only where semantic HTML isn't sufficient.
5. **Screen reader** — images have meaningful alt text (or aria-hidden for decorative), links/buttons describe their destination/action, status messages are announced.
6. **Skip links** — "Skip to main content" link as first focusable element.
7. **Reduced motion** — check for prefers-reduced-motion media query on animations.

- **Rate:** UX Quality (1-10), Accessibility (1-10)

## SEO Reviewer (conditional)
**Model:** Sonnet
**Reads:** `docs/product-spec.md`, all source code
**Writes:** `docs/review-seo.md`
**Enhanced by:** `seo-technical-optimization` skills — if available, you MUST run them as your PRIMARY audit for structured data, keyword density, and snippet optimization. Run the built-in checks below ONLY to supplement gaps.

**Skip this reviewer if** the product is: desktop app (Tauri/Electron), internal tool, CLI, or any non-web-facing product.

### Technical SEO Audit (built-in, always runs)
1. **Meta tags** — each page has unique title (50-60 chars) and description (150-160 chars). Titles follow pattern: "Page Name | Brand"
2. **OpenGraph / Twitter Cards** — og:title, og:description, og:image, og:type set on key pages. Twitter card meta present.
3. **Structured data** — JSON-LD where applicable (Organization, Product, FAQ, BreadcrumbList). Validate against schema.org.
4. **Heading structure** — one h1 per page, logical h2-h6 hierarchy matching content outline.
5. **URL structure** — clean, readable URLs. No query params for main content. Consistent trailing slash behavior.
6. **Performance signals** — image optimization (WebP/AVIF, lazy loading, width/height attributes), font loading strategy (display:swap), bundle splitting.
7. **Canonical URLs** — self-referencing canonicals on all pages.
8. **Robots** — appropriate meta robots tags, robots.txt if applicable.

### Content SEO Audit
1. **Content structure** — scannable with headings, short paragraphs, lists where appropriate
2. **Internal linking** — pages link to related content, navigation covers key pages
3. **Semantic HTML** — article, section, nav, aside used appropriately for content
4. **Image alt text** — descriptive, keyword-relevant where natural

- **Rate:** Technical SEO (1-10), Content SEO (1-10)

## Code Quality Reviewer
**Model:** Sonnet
**Reads:** All source code, package.json/config, build config, tests
**Writes:** `docs/review-code-quality.md`
**Enhanced by:** `security-scanning:security-sast` — if available, you MUST run SAST analysis as your PRIMARY security audit. It catches vulnerabilities the manual checklist below will miss. Run the built-in checks ONLY to supplement gaps.

### Code Quality Audit (built-in, always runs)
1. **Organization** — logical file/folder structure, consistent naming convention (camelCase, PascalCase, kebab-case used purposefully), small focused files (under 200 lines preferred).
2. **Naming** — variables/functions describe what they do, not how. No single-letter names outside loops. Boolean names read as questions (isLoading, hasError).
3. **Modularity** — components have single responsibility. Shared logic extracted to utilities/hooks/composables. No copy-paste code blocks.
4. **Error handling** — async operations have try/catch or .catch(). Errors surface to the user meaningfully. No swallowed errors.
5. **Type safety** — if TypeScript: strict mode, no `any` escape hatches, interfaces for data shapes. If JS: PropTypes or JSDoc for key interfaces.

### Security Audit (OWASP Top 10 Relevant Items)
1. **XSS prevention** — user input is sanitized before rendering. No unsafe innerHTML injection (React, Vue, or raw DOM). Content Security Policy headers if applicable.
2. **Injection** — no string concatenation in queries/commands. Parameterized queries for any database access. No dynamic code execution with user input.
3. **Sensitive data** — no API keys, tokens, or secrets in source code. Environment variables for configuration. .env in .gitignore.
4. **Dependencies** — check for known vulnerabilities (outdated packages with CVEs). No unnecessary dependencies.
5. **Authentication** — if auth exists: tokens stored securely (httpOnly cookies preferred over localStorage), passwords never logged or exposed, session management is sound.
6. **Input validation** — form inputs validated on both client and server (if applicable). File uploads restricted by type/size.

### Performance Audit
1. **Bundle size** — no massive unused imports. Tree-shaking works. Dynamic imports for heavy modules.
2. **Render performance** — no unnecessary re-renders (React: memoization where needed). Lists use keys. Heavy computations memoized.
3. **Images/assets** — optimized formats, appropriate sizes, lazy loading for below-fold content.

- **Rate:** Code Quality (1-10), Security (1-10)

## Product Fit Reviewer
**Model:** Opus
**Reads:** `docs/product-spec.md`, all source code
**Writes:** `docs/review-product-fit.md`

- Validate ALL P0 features from product-spec are implemented
- Check feature completeness against RICE list
- Verify success metrics can be tracked
- Note spec deviations and assess justification
- **Rate:** Feature Completeness (1-10), Product Quality (1-10)

## Review Output Format

Every reviewer uses the same structure:

```markdown
# [Review Name]

### Ratings
| Dimension | Rating | Summary |
|---|---|---|
| [name] | X/10 | ... |

### Strengths
[What was done well]

### Issues
[Each: CRITICAL/MODERATE/MINOR with file path, what's wrong, how to fix]

### Recommendations
[Prioritized list]
```
