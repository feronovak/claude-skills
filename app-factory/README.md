# app-factory

End-to-end app development. Idea or validated spec → shipped product. Multi-agent pipeline with security, ops, and review built in.

## Why this exists

You've validated an idea (via `business-sharks` or your own conviction) and now you need a real, deployable product — not just code that compiles. `app-factory` orchestrates the full pipeline: pitch → spec → security threat model → design → engineer → QA → 7 parallel reviewers, with ops and observability baked into the engineer's job. Solo founders shipping consumer/SMB SaaS in EU jurisdictions get the most leverage from this.

The pipeline has hardware-rated escape hatches: a fast prototype mode for throwaways, a default mode for paid product MVPs, and a serious-bet mode that adds press-release-first pitch + tabletop incident drill before launch.

## Invoke

The skill triggers on full-product-build language. Examples:

- "Build this app: a Next.js app for kids' AI bedtime stories"
- "Create this product: a Tauri desktop tool for personal finance with AI categorization"
- "Develop this: a Slack bot that summarizes daily standups using Claude"
- "Turn this into an MVP: ..."
- "ship me a habit tracker for solo founders, iOS via Expo, two weeks"

Or pass the output of `business-sharks` directly — `app-factory` reads the validation context and skips re-asking.

Does NOT trigger for: adding features to existing apps (use `feature-dev`), single scripts, debugging, code review, or pure deployment.

## Modes

| Mode | When | Phase 1A | Security | Phase 3 reviewers | DevOps deliverables |
|---|---|---|---|---|---|
| **BUILD ONLY** | Prototype, throwaway, validation experiment | – | – | – | minimal |
| **FULL** (default) | Paid product MVP, real users | – | STRIDE + Data Lifecycle | 7 reviewers | full (deploy, observability, README, ADRs, runbook, SBOM) |
| **SERIOUS BET** | ≥1 month build, real money, brand stake | press release + 6-pager + hostile review | full STRIDE + supply-chain + data classification | 7 reviewers | full + tracing + SLOs + IR runbook + tabletop drill |

## What you get

A project folder under your CWD with phase-numbered outputs:

| Phase | Files | Owner |
|---|---|---|
| **0** | project setup | team-lead |
| **1A** (SERIOUS BET) | `pitch-press-release.md`, `pitch-six-pager.md`, `pitch-review-log.md` | pitch-author |
| **1** | `product-spec.md` (with threat model + Data Lifecycle), `security-acceptance-criteria.md` | strategist + security-strategist |
| **2** | `design-system.md`, `component-specs.md`, `ux-flows.md`, `src/`, `Dockerfile`, `README.md`, `.env.example`, `docs/adr/*.md`, `docs/runbook.md`, tests in 3 layers | designer + engineer + qa-reviewer |
| **3** | 7 review files + unified `product-review.md` scorecard | parallel reviewers |

**Human gates:** Phase 0 (setup), Phase 1A (pitch confirmation, SERIOUS BET only), Phase 1 (spec + tech stack approval). Phases 2-3 are autonomous within those gates.

**Final scorecard:** 11 dimensions × 1-10 (visual polish, design system, visual regression, UX, accessibility, technical SEO, content SEO, code quality, security, deploy readiness, feature completeness, product quality).

## Heads up

- **The Phase 1 gate is non-skippable.** Most expensive mistake in software is building the right thing wrong; second is building the wrong thing right. Review the spec.
- **Cost varies by mode + project size.** Rough estimates: BUILD ONLY ~$3-6, FULL ~$10-16, SERIOUS BET ~$13-20 per medium-SaaS build (with current Opus + Sonnet model mix).
- **EU-friendly defaults.** GDPR Data Lifecycle (export, erasure, consent log) is mandatory in FULL/SERIOUS BET. Brevo/Stripe Tax for EU stack.
- **Pairs with `brainstormers-idea` and `business-sharks`** — chain the three for a brainstorm → validate → build pipeline. Or run standalone.
- **Designed for small bets.** Solo or small-team apps, not multi-team platforms. If you're building something with 4+ subsystems, decompose first and run `app-factory` per subsystem.

Full orchestration: see `SKILL.md` and `references/`.

---

Built by [Fero Novak](https://feronovak.com). Part of [feronovak/claude-skills](https://github.com/feronovak/claude-skills).
