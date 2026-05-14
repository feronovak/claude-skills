# DevOps (Operational Readiness)

**Owned by:** engineer
**Verified by:** deployment-readiness-reviewer (Phase 3)
**Mandatory in:** FULL and SERIOUS BET modes. Skipped in BUILD ONLY (with explicit one-line rationale).

The pipeline is not finished when code builds and tests pass. It's finished when the product can run in production, you can see what it's doing, you can find the secret to rotate, and you can roll back when it breaks.

This file defines what the engineer ships beyond `src/` so the deployment-readiness-reviewer in Phase 3 has something to verify.

## What "operationally ready" means

A senior team won't approve a service that is missing any of these. Skip none — note "N/A" with one-line rationale per item only when it genuinely doesn't apply (e.g., observability for a CLI tool: structured logging still applies, error tracker may not).

| Pillar | What ships |
|---|---|
| Deploy | One-command deploy, environment promotion path, rollback procedure |
| Observability | Structured logs, error tracking, health checks, metrics, distributed tracing (tier 2) |
| Secrets | Per-environment secret manager, never in repo, never in image |
| Environments | dev, staging, prod (or documented why staging is skipped for v1) |
| Data | Migrations with rollback, tested backup/restore drill, seed data, declared RTO/RPO |
| Documentation | README, .env.example, architecture diagram, runbook |
| Incident Response | Severity matrix, comms template, postmortem requirement, on-call expectations |

## 1. Deploy

### Choose a host. Keep it boring.
For a solo or small team, pick one of:
- **Vercel** (Next.js / SvelteKit / Astro / static)
- **Fly.io** (Docker, multi-region, Postgres included)
- **Railway** (Docker, Postgres, Redis included)
- **Render** (Docker, Postgres, Redis included)
- **Self-hosted** (Caddy + Docker on a VPS — only if user explicitly chose this)

Pick at Phase 1 (strategist's Technical Requirements → Hosting topology). Do not defer to Phase 2.

### Deliverables
- `Dockerfile` (or framework-native config) — multi-stage build, non-root user, no secrets baked in
- `.dockerignore` — minimum: `.env*`, `.git`, `node_modules`, `dist`, `*.log`
- One-command deploy: either platform-native (`vercel`, `fly deploy`, `railway up`) or scripted (`scripts/deploy.sh`)
- CI workflow (`.github/workflows/deploy.yml` or platform equivalent) — at minimum: install → typecheck → lint → unit tests → build → deploy on `main`. Branch deploys for PRs if the platform supports it.
- Documented rollback path in README:
  - **Platform-native**: `vercel rollback`, `fly releases rollback`, `railway up --rollback`, etc.
  - **Self-hosted**: previous Docker image tagged, `docker compose up -d --image <prev-tag>` documented.

### Environment promotion
- `dev` (developer machine, `.env.local`)
- `staging` (deployed branch or separate project; mirrors prod config but with non-prod data and lower-tier resources)
- `prod` (deployed `main`)

For SERIOUS BET: staging is mandatory. Smoke tests run against staging before promotion to prod.

For FULL: staging is recommended, can be skipped for v1 with a one-line rationale and a note to add it before second meaningful release.

For BUILD ONLY: dev only. Note that this means "not for paying users."

## 2. Observability

### Structured logging
- JSON logs by default. One log per request with: `request_id`, `user_id` (if auth), `route`, `method`, `status`, `duration_ms`, `error` if any.
- Library suggestion (pick one): `pino` (Node), `structlog` (Python), `zerolog` (Go).
- Never log: passwords, full request bodies on auth/payment endpoints, credit card data, full names, emails (hash if needed for correlation), phone numbers, full IPs (truncate last octet for EU users), API keys, session tokens.
- Log destination: stdout/stderr — let the platform aggregate (Vercel logs, Fly logs, Railway logs). For self-hosted: ship to a sink (Grafana Loki, Better Stack, Datadog free tier).

### Error tracking
- Wire one of: **Sentry** (free tier), **Rollbar**, **Bugsnag**, or platform-native (Vercel Errors). Sentry is the safe default.
- Initialize in app entrypoint with environment, release version (git SHA), and PII scrubbing enabled.
- Confirm a test error appears in the dashboard before considering this done.

### Health checks
- `GET /healthz` — returns 200 if process is alive (no DB or external check). Liveness probe.
- `GET /readyz` — returns 200 if process can serve traffic (DB connection ok, critical external services reachable). Readiness probe.
- Wire to platform's health check config (Fly: `[[services.tcp_checks]]` and `[[services.http_checks]]`; Vercel: not applicable; Railway: built-in).

### Metrics (light tier — don't over-invest)
For v1, structured logs + error tracker is enough. Add metrics only when there's something to chart:
- LLM-backed product → daily token/$ counter (already required by Safety Guards)
- High-volume endpoint → request rate + p95 latency (use platform's built-in metrics first)
- Background jobs → success/failure counters + last-success-at gauge

If you cannot answer "is the service up and serving correctly?" in under 30 seconds from observability tooling, add what's missing.

### Distributed Tracing (Tier 2 — required in SERIOUS BET, recommended in FULL)

For products with ≥2 services, ≥1 third-party dependency in the request path, or ≥100 req/min target, structured logs are not enough — you need to follow a request across hops.

**OpenTelemetry is the default.** Reasons: vendor-neutral SDK, supported by every major backend (Honeycomb, Grafana Tempo, Datadog, New Relic, Jaeger).

#### Minimum viable wiring
- OTel SDK initialized at app entrypoint with: `service.name`, `service.version` (git SHA), `deployment.environment` (dev/staging/prod).
- Auto-instrumentation enabled for: HTTP server, HTTP client, database driver. (Most languages have a `@opentelemetry/auto-instrumentations-node` or equivalent meta-package.)
- Trace context propagation across third-party calls (LLM provider, payment provider, email).
- Sampling: head-based 10% in prod by default; 100% in staging; tail-based "errors always" if backend supports.
- Exporter:
  - Cheap default: **Grafana Tempo + Grafana Cloud free tier** or **Honeycomb free tier**
  - Self-hosted: Jaeger + OTel Collector
  - Avoid: writing your own backend, adding a paid Datadog tier on day one

#### What to verify before claiming "tracing is wired"
- One real user request produces a span tree visible in your trace backend
- DB queries appear as child spans of the API span
- LLM calls appear as child spans with token-count attributes
- Errors are tagged on spans (not just in logs)

#### Minimum SLOs
For SERIOUS BET, declare at least these three:

| SLO | Default target | Error budget |
|---|---|---|
| Availability (homepage) | 99.5% over 30d | 3h 36m / month |
| Critical-flow latency p95 (e.g., checkout, primary CTA) | ≤ 1s over 30d | 5% of requests slower than 1s |
| Critical-flow success rate | ≥ 99% over 30d | 1% failed requests |

Burn-rate alerts (page if you'll exhaust the monthly budget in <24h at current rate) are the single most useful alert pattern. Wire one per SLO.

For FULL: declare at least the availability SLO. Latency/success SLOs recommended.

For BUILD ONLY: skip.

Document SLOs in `docs/runbook.md` § "Observability targets."

### Alerting
Pick a default channel and document it in README. Order of preference:
1. **Email + console** (cheapest default, always available) — Sentry can email on first error in prod.
2. **Slack webhook** (one channel `#prod-alerts`) — Sentry, Better Stack, Uptime Kuma all support it.
3. **PagerDuty / Opsgenie** (only if user is actually on-call).

Alerts to wire from day one:
- Error rate spike (Sentry default works)
- Health check failure (platform-native or Uptime Kuma)
- Daily $ cap hit (80% warn, 100% kill — implementation in Safety Guards)
- Disk/memory > 90% on self-hosted

## 3. Secrets management

`.env` in repo root is for local dev only. Production secrets go through one of:

| Host | Secret store |
|---|---|
| Vercel | Vercel env vars (per-environment: dev / preview / production) |
| Fly.io | `fly secrets set` |
| Railway | Railway env vars (per-environment) |
| Render | Render env vars |
| Self-hosted | Doppler, 1Password CLI, AWS Secrets Manager, or `.env` on the VPS owned by deploy user with `chmod 600` (acceptable for solo/small) |

### Rules
- `.env` is gitignored; `.env.example` is committed with all required keys and comments (no values).
- Production secrets are rotated at least once before launch (proves rotation actually works).
- The CI/CD pipeline pulls secrets from the secret store at deploy time — never echoes or logs them.
- Secret rotation procedure documented in README (one paragraph: "to rotate X, run Y, redeploy, verify Z").
- No secrets in Dockerfiles, no secrets in `docker compose.yml` committed values, no secrets in image layers.

## 4. Database (if applicable)

### Migrations
- Tooling: framework-native (Prisma migrate, Drizzle migrate, Alembic, Rails migrations). Never raw SQL files run by hand in production.
- Each migration file has a header comment with one of:
  - `safe-additive` — additive only, backwards-compatible, no rollback needed
  - `requires-coordination` — schema change requires deploy ordering or feature flag; document in PR description
  - `destructive` — drops or renames; backup taken first, rollback path documented
- Migrations run in CI before deploy completes. Failed migration aborts the deploy.

### Backups
- Managed Postgres (Fly, Railway, Render, Supabase, Neon) → enable point-in-time recovery (PITR) or daily snapshots. Document retention.
- Self-hosted Postgres → `pg_dump` daily, ship to object storage with ≥30-day retention.
- **Tested restore drill required** — once before launch, restore the latest backup to a scratch instance, verify it loads. Document the procedure with the timestamps in README. Untested backups don't count.

### Seed data
- `scripts/seed.ts` (or equivalent) — produces a dev/staging-quality dataset. Idempotent.
- Never seed prod with this script. Production starts empty or imports a documented dataset.

## 5. Documentation deliverables

Engineer writes these as part of Phase 2. Reviewer checks they exist and are accurate.

### `README.md` (project root)
Minimum sections:
1. **What this is** (2 lines)
2. **Tech stack** (one line per layer)
3. **Local setup** (clone, install, env, db, run — 5-10 commands max)
4. **Environment variables** (table: name, required?, example, description)
5. **Deploy** (one paragraph, link to platform docs for details)
6. **Rollback** (specific commands)
7. **Run tests** (unit, e2e, load — copy-paste commands)
8. **Architecture** (one ASCII diagram or one paragraph: components and data flow)
9. **Runbook links** (where to look when X breaks)

### `.env.example`
Every key required to run locally. Comment what each does. No values.

### `docs/adr/NNN-title.md` (one per major decision)
Required ADRs:
- `001-tech-stack.md` — what was chosen and why (cite strategist's options)
- `002-auth.md` — auth approach (sessions vs JWT vs magic link vs OAuth provider)
- `003-data-store.md` — DB + ORM choices
- `004-ai-provider.md` — if LLM features (provider, fallback, why)
- Optional: `005-hosting.md`, `006-payments.md` (if applicable)

Each ADR is one page max:
```markdown
# ADR NNN: Title

**Status:** accepted | superseded by NNN | deprecated
**Date:** YYYY-MM-DD

## Context
[2-3 sentences: what problem, what constraints]

## Decision
[1-2 sentences: what we chose]

## Consequences
[3-5 bullets: what this enables, what this costs, what we're giving up]

## Alternatives considered
[1 line each]
```

### `docs/runbook.md`
A list of "if X happens, do Y." Start with at least:
- **Deploy failed in CI** — how to investigate, where logs are
- **Error rate spiked** — how to find the cause in error tracker
- **DB connection errors** — pooler limits, connection check, restart procedure
- **LLM costs spiking** — kill switch, how to disable feature
- **Need to roll back** — exact command + verification steps

Three runbook entries with real commands beats ten vague ones.

## 6. Incident Response (SERIOUS BET mandatory; FULL recommended)

When prod breaks, the team needs a script. The runbook tells you what to do for known issues. IR tells you how to operate when something unknown is on fire.

### Severity Matrix

| Sev | Definition | Response time | Comms |
|---|---|---|---|
| **SEV1** | User-facing outage; data loss imminent or in progress; security breach | < 15 min ack, all-hands | Public status update within 30 min; user comms if data implicated |
| **SEV2** | Major feature broken; significant subset of users affected; revenue impact | < 1 hour ack | Internal channel + status page if user-facing |
| **SEV3** | Minor feature broken; workaround exists; no revenue impact | Next business day | Internal channel only |
| **SEV4** | Cosmetic or low-impact bug | Backlog | Ticket only |

For solo / very-small teams, SEV1 = "drop everything"; SEV2 = "today"; SEV3 = "this week."

### On-Call Expectations

- **Solo founder mode** — the founder is on-call by default. Document this honestly: "I am the on-call. SLA is 15 min during business hours, best-effort outside." Set realistic user expectations.
- **Small team mode** — primary + secondary, weekly rotation, 24/7 only if SLA promises 24/7. Use platform native (PagerDuty, Opsgenie, Better Uptime) or a Slack channel + phone.
- Hand-off: weekly on-call review covers open incidents, runbook updates needed, alert noise.

### Comms Template (for SEV1-2)

```
[STATUS] [SEV1/2] <one-line summary>
Started: <UTC timestamp>
Impact: <who is affected, what they see>
Status: investigating | identified | mitigating | monitoring | resolved
Next update: <time>
```

Post in `#prod-alerts` (or status page) at every state change. Resolution post includes one-line cause and link to postmortem (when written).

### Postmortem Requirement

Every SEV1 and SEV2 gets a postmortem within 5 days. Blameless template stored at `docs/postmortems/TEMPLATE.md`:

```markdown
# Postmortem: <incident title>
**Date:** YYYY-MM-DD | **Severity:** SEV1/2 | **Duration:** Xh Ym | **Author:** <name>

## What happened
[Plain-language summary, 3-5 sentences]

## Impact
[Users affected, revenue, data, reputation]

## Timeline (UTC)
- HH:MM — first signal (alert / user report)
- HH:MM — engineer engaged
- HH:MM — root cause identified
- HH:MM — mitigation applied
- HH:MM — verified resolved

## Root cause
[The one thing that, if different, would have prevented this — not the trigger]

## What worked
[Detection time, comms, mitigations that helped]

## What didn't
[Detection gaps, runbook gaps, ownership confusion]

## Action items
| Action | Owner | Due | Type |
|---|---|---|---|
| ... | ... | YYYY-MM-DD | prevent / detect / mitigate |
```

Completed postmortems live at `docs/postmortems/YYYY-MM-DD-title.md`.

### Disaster Recovery (RTO / RPO)

RTO and RPO are declared in `docs/product-spec.md` (Technical Requirements). The IR process ensures they're achievable.

- **RTO** (Recovery Time Objective) — how long to restore service after a disaster. Test by restoring backup to scratch + spinning up service from scratch in staging. Measure actual time.
- **RPO** (Recovery Point Objective) — how much data loss is acceptable. If RPO is 1h, backups must run at least hourly.
- Test once before launch. Re-test annually or on infrastructure changes.

### Tabletop Drill (SERIOUS BET, before launch)

One pretend-incident dry-run before launch, with the on-call walking the IR process out loud:
1. Pick a plausible incident (DB connection storm, third-party API outage, prod cost spike).
2. Walk through: detection → ack → comms → triage → mitigate → resolve → postmortem.
3. Document gaps found (missing alert, runbook entry, comms channel) and fix them.
4. Log the drill timestamp in `docs/runbook.md`.

Untested IR = no IR. The first real incident is not the time to find out the comms channel doesn't work.

## 7. Build sequence integration

The engineer's existing build sequence (in `engineer.md`) ends at step 8 (build check). Add step 9:

**9. Operational readiness** — produce all DevOps deliverables before declaring Phase 2 complete. The deployment-readiness-reviewer in Phase 3 will verify each one. If any are missing, qa-reviewer creates a fix task back to engineer before Phase 3 begins.

## Right-Sizing By Mode

| Mode | DevOps depth |
|---|---|
| BUILD ONLY | Skipped. README has "this is a prototype, not deployable as-is." |
| FULL | All sections. Staging optional with rationale. Tested backup drill mandatory. |
| SERIOUS BET | All sections. Staging mandatory. Backup drill + rollback drill (deploy old image, verify, redeploy current). ADRs all five. |

## Red Flags — STOP

- "We'll add observability after launch" → first incident, you'll have nothing to debug with. Wire it before launch.
- "Sentry is overkill for v1" → free tier, 10 minutes to set up, catches errors you'd otherwise miss for weeks.
- "Production .env on the VPS is fine" → as long as the file is `chmod 600`, owned by the deploy user, never copied to repo, and rotation is documented. Otherwise upgrade to a secret manager.
- "We don't need staging for v1" → only acceptable if FULL mode and rationale is documented. Not acceptable for SERIOUS BET.
- "Backups happen automatically with the managed DB" → maybe. Run a tested restore once before claiming this. Untested = nonexistent.
- "Rollback is just `git revert`" → no, it's redeploying a known-good image without rebuilding. Document the actual command.

## Rules

- DevOps deliverables ship at the same time as `src/`, not after.
- The deployment-readiness-reviewer reads this file as its rubric. Cross-references `docs/security-acceptance-criteria.md` for any security-driven ops requirements (alerts, audit logs).
- "Documented" means in `README.md` or `docs/runbook.md`, not in commit messages or chat.
- Rollback must be tested at least once on staging (FULL/SERIOUS BET). Note the timestamp.
- If a section is genuinely N/A (e.g., no DB), write `## Database — N/A (no persistent storage)` in README. Silent omissions = future incidents.
