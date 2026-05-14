# Phase 3 Reviewers

7 specialist reviewers run in parallel after QA completes. Each is independent — they don't read each other's output.

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
**Model:** Opus
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

### Performance Audit (with explicit budgets)

Soft assessment is not enough — the build must meet declared budgets or document the gap.

| Metric | Default budget (web app) | How to measure |
|---|---|---|
| LCP (Largest Contentful Paint) | ≤ 2.5s on 3G fast | Lighthouse CI / Chrome DevTools |
| TTI (Time To Interactive) | ≤ 3.8s on 3G fast | Lighthouse CI |
| CLS (Cumulative Layout Shift) | ≤ 0.1 | Lighthouse CI |
| INP (Interaction to Next Paint) | ≤ 200ms | Lighthouse CI / web-vitals lib |
| First-load JS bundle | ≤ 200KB gzip | bundle analyzer (`@next/bundle-analyzer`, `vite-plugin-bundle-visualizer`) |
| p95 server response time on critical endpoints | ≤ 500ms | platform metrics / k6 load test |

For non-web products (CLI, desktop), pick budgets that fit (CLI: startup time, memory ceiling; desktop: bundle size, cold start).

For products explicitly outside the web (API-only, batch jobs): document N/A with the relevant alternative budgets.

Audit:
1. **Bundle size** — no massive unused imports. Tree-shaking works. Dynamic imports for heavy modules. Bundle is under the budget.
2. **Render performance** — no unnecessary re-renders (React: memoization where needed). Lists use keys. Heavy computations memoized. Vitals are within budget.
3. **Images/assets** — optimized formats (WebP/AVIF), appropriate sizes, lazy loading for below-fold content, `width`/`height` attributes to avoid CLS.
4. **Server-side** — p95 latency on top 5 endpoints meets budget. Slow queries identified (the database has indexes for the queries actually run).

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

## Deployment Readiness Reviewer
**Model:** Sonnet
**Reads:** `references/devops.md`, `README.md`, `Dockerfile` (if present), CI workflow files, `.env.example`, `docs/runbook.md`, `docs/adr/*.md`, `docs/security-acceptance-criteria.md` (if present)
**Writes:** `docs/review-deploy-readiness.md`

**Skip this reviewer if** mode is BUILD ONLY. (Note "skipped — BUILD ONLY mode, prototype tier" in the review file.)

The deployment-readiness-reviewer verifies the pipeline produced a deployable service, not just code that builds. Uses `references/devops.md` as the rubric.

### Audit Sections

For each pillar in `devops.md`, mark each item: ✅ implemented | ⚠️ partial | ❌ missing | N/A (with rationale).

#### 1. Deploy
- [ ] Host chosen and documented in README
- [ ] `Dockerfile` (or framework-native config) — multi-stage, non-root user, no secrets in image
- [ ] `.dockerignore` excludes `.env*`, `.git`, `node_modules`, `dist`, logs
- [ ] One-command deploy works (run it; capture output)
- [ ] CI workflow runs typecheck + lint + tests + build + deploy on `main`
- [ ] Rollback path documented with specific commands

#### 2. Environments
- [ ] dev / staging / prod separation per mode requirements (FULL: staging optional with rationale; SERIOUS BET: staging mandatory)
- [ ] Smoke subset of e2e tests runs against staging (if staging exists)
- [ ] Per-environment secrets, no cross-environment leakage

#### 3. Observability
- [ ] Structured logging (JSON, request_id, etc.) — verify by sampling 5 log lines
- [ ] Error tracker wired (Sentry or equivalent); send a test error and confirm receipt
- [ ] `GET /healthz` and `GET /readyz` exist and return correctly
- [ ] Alerting channel chosen and documented; day-one alerts wired (error rate, health failure, $ cap, disk/memory)
- [ ] **(SERIOUS BET) Distributed tracing wired** — OpenTelemetry SDK with auto-instrumentation; one real request produces a span tree visible in trace backend; LLM/DB calls appear as child spans; sampling configured per environment
- [ ] **(SERIOUS BET) SLOs declared** — at least availability, critical-flow latency p95, critical-flow success rate; documented in `docs/runbook.md`; burn-rate alerts wired
- [ ] **(FULL) Availability SLO declared** — at minimum, with a target and measurement method

#### 4. Secrets
- [ ] Production secrets in a host secret manager (or VPS `.env` with `chmod 600` for self-hosted)
- [ ] `.env.example` complete and committed
- [ ] No secrets in repo history (`gitleaks` or grep check)
- [ ] No secrets in Docker image layers (extract image, grep)
- [ ] Rotation procedure documented in README; one rotation performed before launch

#### 5. Database (if applicable)
- [ ] Migrations versioned and run in CI before deploy
- [ ] Each migration marked `safe-additive` / `requires-coordination` / `destructive`
- [ ] Backups configured; **restore drill performed** with timestamp in runbook
- [ ] Seed script exists for dev/staging; not run against prod
- [ ] RTO/RPO declared in `docs/product-spec.md` Technical Requirements; backup frequency aligns with RPO; restore drill measured time aligns with RTO target

#### 6. Documentation
- [ ] `README.md` has all 9 sections from `devops.md` § 5
- [ ] `.env.example` complete with comments
- [ ] Required ADRs present (`001-tech-stack.md`, `002-auth.md`, `003-data-store.md`, `004-ai-provider.md` if LLM)
- [ ] `docs/runbook.md` has at least 5 entries with real commands

#### 7. Incident Response (SERIOUS BET mandatory; FULL recommended)
- [ ] Severity matrix (SEV1-4) documented in `docs/runbook.md`
- [ ] Comms template defined for SEV1-2
- [ ] On-call expectations stated honestly (solo / small team / 24/7)
- [ ] Postmortem template at `docs/postmortems/TEMPLATE.md` (or equivalent)
- [ ] At least one tabletop walk-through documented before launch (pretend-incident dry-run)

#### 8. Supply Chain (FULL and SERIOUS BET)
- [ ] SBOM generated on release builds
- [ ] Dockerfile `FROM` lines pinned to digests
- [ ] (SERIOUS BET) Release images signed with `cosign` or platform attestation

### Anti-Patterns to Flag

- README that just says "see commands above" without commands
- Rollback documented as "git revert and redeploy" (that's a code change, not a rollback)
- Sentry or logging library installed but never initialized
- Secrets present in `docker-compose.yml` committed values
- "We'll add staging later" without rationale (FULL mode) or at all (SERIOUS BET)
- `chmod 644` `.env` on VPS, world-readable
- Health check returns 200 by checking nothing
- Alerts that go nowhere (Sentry installed but no email/Slack configured)
- ADRs that say "we picked X because we like X"
- Backups configured but never restored — document restore-drill timestamp or it doesn't count

### Output Format

Standard reviewer output. The Issues section is structured by pillar:

```markdown
# Deployment Readiness Review

### Ratings
| Dimension | Rating | Summary |
|---|---|---|
| Deploy Readiness | X/10 | [one-line summary, e.g., "deploy works, rollback untested"] |

### Pillar Status
| Pillar | Status | Notes |
|---|---|---|
| Deploy | ✅ / ⚠️ / ❌ | [...] |
| Environments | ... | ... |
| Observability | ... | ... |
| Secrets | ... | ... |
| Database | ... | ... |
| Documentation | ... | ... |

### Strengths
[What's solid]

### Issues
[Each: CRITICAL/MODERATE/MINOR with file path / pillar, what's wrong, how to fix]

### Recommendations
[Prioritized list — what to fix before launch]
```

- **Rate:** Deploy Readiness (1-10) — 10 = could ship to prod today; 7 = ship-ready with one or two minor gaps; 5 = significant gaps but core deploy works; <5 = not deployable, must loop back to engineer.

## Visual Regression Reviewer
**Model:** Sonnet
**Reads:** `docs/component-specs.md`, all source code, `tests/visual/baseline/` if present
**Writes:** `docs/review-visual-regression.md`, `tests/visual/baseline/*.png` (on first run), `tests/visual/diffs/*.png` (on subsequent runs if regressions)

**Skip this reviewer if** the product has no rendered UI (CLI, API-only backend).

The visual regression reviewer guards against the most common silent failure in AI-assisted builds: a component's layout breaks, every other test passes, and no one notices until a user complains.

### Setup

Wire Playwright with screenshot diffing. The reviewer is responsible for the test config, not the engineer. Use the chosen stack's test runner (Playwright Test for most cases; for non-web stacks adapt to the platform's screenshot tooling).

```ts
// tests/visual/visual.spec.ts (template — adapt to product structure)
import { test, expect } from '@playwright/test';

const VIEWPORTS = [
  { name: 'mobile', width: 390, height: 844 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'desktop', width: 1280, height: 800 },
];

const ROUTES = [
  // Pulled from ux-flows.md: every primary route + key states
  { path: '/', name: 'home' },
  // ... add per product-spec
];

for (const viewport of VIEWPORTS) {
  for (const route of ROUTES) {
    test(`${route.name} @ ${viewport.name}`, async ({ page }) => {
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      await page.goto(route.path);
      await page.waitForLoadState('networkidle');
      await expect(page).toHaveScreenshot(`${route.name}-${viewport.name}.png`, {
        maxDiffPixels: 100, // small anti-aliasing tolerance
        fullPage: true,
      });
    });
  }
}
```

### Methodology

1. **Determine if baseline exists.**
   - If `tests/visual/baseline/` is empty → first run. Generate baselines, mark all as accepted, write a one-line note in the review: "Baseline created (N screenshots × M viewports)."
   - If baseline exists → run diff.
2. **Run Playwright in headed mode if available, otherwise headless** with the diff threshold above. Capture diffs.
3. **For each diff above threshold:**
   - Open the diff image, inspect.
   - Classify: **intentional** (engineer changed the component on purpose, baseline should update) or **regression** (unintended layout/spacing/color change).
4. **Intentional changes** → re-baseline that screenshot, note in the review which were updated and why (cite commit or component-specs change).
5. **Regressions** → flag as MODERATE issue with file path and screenshot reference; engineer fixes.

### Coverage Targets

- Every P0 page/route has at least desktop + mobile screenshots
- Every component with multiple variants (button, card, modal) has one screenshot per variant
- States that matter (loading, empty, error) have screenshots if they're reachable in the test environment

### Common Issues to Catch

- **Layout shift** — a component grew or shrank, pushing other content
- **Z-index conflicts** — overlay or modal renders behind/in front of unintended layer
- **Responsive break** — a layout works at desktop but breaks at tablet
- **Token drift** — a color or spacing value changed without design-system.md updating
- **Font fallback** — webfont didn't load, system font is rendering, layout looks "almost right"
- **Hover-only craft** — element looks unfinished without hover; baseline catches the resting state

### Output Format

```markdown
# Visual Regression Review

## Setup
- Playwright screenshot tests in `tests/visual/`
- Baseline location: `tests/visual/baseline/`
- Threshold: 100 px diff per screenshot

## Run Result
- Total screenshots: 24 (8 routes × 3 viewports)
- Baselined: 24
- Regressions: 2
- Intentional changes: 1 (re-baselined)

## Regressions Found
[Each: CRITICAL/MODERATE/MINOR with file path, screenshot path, what changed, suggested fix]

## Intentional Updates
- `home-desktop.png` — re-baselined; component-specs changed hero spacing per spec section X
```

- **Rate:** Visual Regression (1-10) — 10 = no regressions, full coverage. 7 = minor unflagged drift but no broken layouts. <5 = visible layout breaks not caught by other reviewers.

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
