---
name: app-factory
description: Use when the user wants to BUILD a complete app, product, or MVP from a description (orchestrates spec → design → code → tests → reviews via a multi-agent pipeline, not just code generation). Triggers strongly on phrases like 'build this app', 'create this product', 'make me an X', 'develop this', 'turn this into an MVP', 'ship this', 'build the MVP', or any request to produce a full working application from a product description. Also triggers when input from brainstormers-idea or business-sharks is ready for execution, or when the user pastes a folder path containing validated idea documents. Use this skill whenever the user describes a product to build (not just a feature to add), even if they don't say 'app-factory' explicitly. Do NOT trigger for adding features to existing apps (use feature-dev), single scripts, debugging, code review, refactoring, or pure deployment tasks.
metadata:
  version: "4.3"
  team: app-factory
  authors: Fero Novak <https://feronovak.com>
---

End-to-end application manufacturing. Takes research output or a specific product description and builds it: product spec → design → engineering → QA → parallel validation with loop-back fixes.

The app is: $ARGUMENTS

## Reference Files (Table of Contents)

The team-lead reads SKILL.md (this file) plus `references/skill-dependency-check.md` and `references/update-protocol.md`. Each role reads ONLY its own reference file when spawned.

| File | Read by | Contains |
|---|---|---|
| `references/skill-dependency-check.md` | team-lead (Phase 0) | Optional skill detection (interface-design, frontend-design, security-scanning, etc.) |
| `references/pitch-author.md` | pitch-author (Phase 1A, SERIOUS BET only) | Press release + 6-pager + hostile-review templates |
| `references/strategist.md` | strategist (Phase 1) | Product spec, RICE, hosting topology, RTO/RPO, SLOs |
| `references/security-strategist.md` | security-strategist (Phase 1) | STRIDE per trust boundary, Data Lifecycle (GDPR), security acceptance criteria |
| `references/designer.md` | designer (Phase 2) | Design system tokens, component specs, ux-flows |
| `references/engineer.md` | engineer (Phase 2) | Build sequence, Safety Guards (rate limit, retries, observability, AI safety, supply chain) |
| `references/devops.md` | engineer + deployment-readiness-reviewer | Deploy + observability + secrets + IR + tabletop drill |
| `references/qa-reviewer.md` | qa-reviewer (Phase 2) | 3 test layers (unit + e2e + load) with scenario lists |
| `references/reviewers.md` | Phase 3 reviewers | All 7 reviewer specs + scoring rubrics |
| `references/update-protocol.md` | team-lead | Spec changes, fixing review issues, resuming incomplete builds |

When spawning a teammate, include ONLY their role-specific reference file.

---

## INPUT TRIAGE

Before doing anything, determine the input source:

### 1. business-sharks output exists
Look for a business-sharks project folder (contains `docs/12-scorecard.md`). This is the best input — the idea has been shaped and validated.
- Check the verdict in `12-scorecard.md`: if NO-GO, warn the user: "business-sharks gave this a NO-GO verdict. Are you sure you want to build?"
- Strategist work: LIGHT — translate validated research into product spec.

### 2. brainstormers-idea output only
Look for a brainstormers-idea project folder (contains `docs/05-refined-idea.md`). Good input — the idea is shaped but not stress-tested.
- Check the reality check in `05-refined-idea.md`: if RECONSIDER, warn the user.
- Strategist work: MEDIUM — more gaps to fill, assumptions to flag.

### 3. Direct user input
The user described what to build directly. Evaluate specificity against ALL four criteria:
- **What problem it solves** — not just what it does, but WHY someone needs it. "A booking app" fails. "Dog owners can't find groomers with availability — a booking app that shows real-time slots" passes.
- **Who it's for** — specific persona, not a category. "Small businesses" fails. "Solo pet groomers managing 10-30 appointments/week" passes.
- **At least 3 concrete features** — specific functionality, not vague goals. "Good UX" fails. "Calendar view with drag-to-reschedule" passes.
- **The pain** — what the user suffers without this. Can be implicit in the problem statement.

**Specific enough** = has all four. Proceed. Strategist work: HEAVY — building spec from scratch.
**Almost there** = has 3 of 4 (usually missing the problem/pain). Ask the ONE missing question, then proceed.
**Too vague** = missing 2+ criteria. STOP. Say: "I need more context before building. What problem does this solve, and for whom specifically? Or run `/brainstormers-idea` first to shape the idea."

### 4. No input
$ARGUMENTS is empty. Ask: "What do you want to build? You can point me to brainstormers-idea or business-sharks output, or describe the product directly."

---

## PHASE 0: PROJECT SETUP

1. Generate a folder name (lowercase kebab-case, 2-4 words).
2. Present to user via AskUserQuestion. Wait for confirmation.
3. Create `{project-folder}/` with `docs/` and `src/` subdirectories.
4. If folder exists, ask whether to reuse or pick a new name.

---

## SKILL DEPENDENCY CHECK

After project setup, check which optional enhancement skills are installed. These improve output quality in design and security; `security-scanning:security-sast` is **required for FULL and SERIOUS BET modes**.

Read `references/skill-dependency-check.md` for the full check procedure, the recommendations to present, and the user's response options.

Store the result as `{enhanced_skills}` and pass it to teammates.

---

## EXECUTION MODE

Ask the user which mode to use.

**Mode inheritance:** If the user previously ran another pipeline skill (brainstormers-idea, business-sharks) in this session and chose a mode, default to the equivalent: DEEP → SERIOUS BET, STANDARD → FULL, QUICK → BUILD ONLY. Mention it: "You used STANDARD for the previous steps — I'll default to FULL here. Change?"

**SERIOUS BET**: Pitch + build + validate + operational maturity. Phase 1A + all 3 phases.
- Phase 1A: pitch-author (Opus) — press release + 6-pager + async review (Devil's Advocate + Pre-mortem)
- Phase 1: strategist (Opus) + security-strategist (Opus, full STRIDE pass + Data Lifecycle)
- Phase 2: designer (Opus) → engineer (Sonnet) → qa-reviewer (Sonnet) — serial — engineer ships full DevOps deliverables: deploy + observability with **distributed tracing + SLOs**, secrets, **incident response runbook**, **declared RTO/RPO**, **signed images + SBOM**, README + ADRs + postmortem template
- Phase 3: 7 parallel reviewers + loop-back fixes
- Requires: `security-scanning:security-sast` skill installed
- Best for: ≥1 month of build, real budget, brand you care about, public launch
- Adds 2-4 hours of pitch work upfront. Saves 10× that in scope creep, missed assumptions, and rework.

**FULL** (default): Build + validate. All 3 phases.
- Phase 1: strategist (Opus) + security-strategist (Opus)
- Phase 2: designer (Opus) → engineer (Sonnet) → qa-reviewer (Sonnet) — serial — engineer ships DevOps deliverables: deploy + observability (logs + error tracker + health checks + at-minimum availability SLO), secrets, README + ADRs, **SBOM + pinned base images**, runbook
- Phase 3: 7 parallel reviewers + loop-back fixes
- Requires: `security-scanning:security-sast` skill installed
- Best for: production-quality builds, paid products, anything reaching real users

**BUILD ONLY**: Build without validation. Phases 1 + 2 only.
- Phase 1: strategist (Opus) only — security-strategist is skipped
- Phase 2: designer → engineer → qa-reviewer (no DevOps deliverables required; README states "prototype, not deployable as-is")
- Phase 3 entirely skipped
- Faster, cheaper
- Best for: prototypes, internal tools, throwaway scripts, validation experiments

Default to FULL. Use BUILD ONLY if user says "quick", "prototype", "just build it", etc. Use SERIOUS BET if user mentions: long timeline, real launch, monetization, brand, public release, "important to me".

When presenting the mode choice, call `AskUserQuestion` — header `"Mode"`, question `"Pick a build mode."`, multiSelect false, options:
  - `"🛠️ FULL (Recommended)"` — `"Spec + build + 7-reviewer validation. For production-quality builds and paid products."`
  - `"🚀 SERIOUS BET"` — `"Pitch-author + full validation + DevOps maturity. For real launches with budget on the line."`
  - `"⚡ BUILD ONLY"` — `"Code only — no security spec, no Phase 3 reviewers. For prototypes and throwaway scripts."`

Map the answer to `BUILD ONLY`, `FULL`, or `SERIOUS BET`.

---

## PHASE 1A: STRATEGIC PITCH (SERIOUS BET mode only — interactive gate)

Skip this phase entirely if mode is FULL or BUILD ONLY.

For SERIOUS BET, the pitch-author runs before the strategist. Read `references/pitch-author.md` for full responsibilities.

### Phase 1A Outputs (in order)
1. `docs/pitch-press-release.md` — 1-page press release dated 12 months from now
2. `docs/pitch-six-pager.md` — Amazon-style 6-pager (problem, customer, solution, bet, risks, out of scope, FAQ)
3. `docs/pitch-review-log.md` — async critique by 2 hostile reviewers (Devil's Advocate + Pre-mortem) and disposition

### Phase 1A Presentation
When pitch-author completes, present:
1. Press release (full text — user reads it as if it shipped)
2. Bet summary from 6-pager (what we're betting, kill criteria)
3. Top 3 risks with disposition (from review log)
4. "Does this look like the product you actually want to build?"

User responses:
- **"Yes, proceed"** → strategist runs Phase 1 with pitch as constraint
- **"This isn't what I want"** → STOP. Return to user with the gap. Do not rationalize forward into Phase 1.
- **"Change X"** → relay to pitch-author, iterate, re-present.

Call `AskUserQuestion` — header `"Pitch"`, question `"Does this pitch match what you want to build?"`, multiSelect false, options:
  - `"✅ Yes, proceed (Recommended)"` — `"Approve the pitch and continue to Phase 1 (strategist)."`
  - `"🔧 Change something"` — `"Iterate on the pitch — you'll specify what to change next."`
  - `"❌ Not what I want"` — `"Stop the build. Surface the gap so we can rethink."`

If the user picks `"🔧 Change something"`, ask a follow-up free-text question for what to change, then relay to pitch-author. Do NOT proceed to Phase 1 until the user confirms the pitch matches their intent.

---

## PHASE 1: PRODUCT SPEC (Interactive — human approval gate)

Two agents run in this phase. Strategist runs first; security-strategist runs after strategist drafts product-spec but before user presentation.

### Strategist
Reads input source (or pitch documents in SERIOUS BET mode) and writes `docs/product-spec.md`. Full responsibilities in `references/strategist.md`.

In SERIOUS BET mode, strategist treats the 6-pager's P0 list as the feature ceiling. No scope expansion at spec time — that bypasses the bet.

### Security Strategist (skipped in BUILD ONLY mode)

After strategist completes, security-strategist reads `docs/product-spec.md` and:
1. Identifies trust boundaries
2. Applies STRIDE per boundary
3. Appends `## Threat Model` section to `docs/product-spec.md`
4. Writes `docs/security-acceptance-criteria.md` (engineer's checklist, reviewer's gate)

Full responsibilities in `references/security-strategist.md`.

In SERIOUS BET mode, security-strategist also produces a data-flow diagram and considers supply-chain risks. In FULL mode, a top-5-to-8 STRIDE pass is sufficient.

### Phase 1 Presentation

When both strategist and security-strategist complete, present to the user:
1. Product summary (2-3 sentences)
2. P0 features list (the MVP)
3. Tech stack options (3 options with recommendation — user picks one)
4. Key user flows (one-line each)
5. **Top 3-5 threats and mitigations** (from threat model — show user what security work is now P0)
6. Open questions (if any)

Then STOP and WAIT. The user must approve the spec AND pick a tech stack. They may:
- **Pick a stack** → lock it in, update product-spec
- **Propose their own stack** → use it, note as "user-specified" in product-spec
- **Request changes** → relay to strategist (or security-strategist), iterate, present again
- **Ask questions** → answer from the spec
- **Say "approved"** → proceed to Phase 2

Call `AskUserQuestion` — header `"Spec"`, question `"Approve the product spec and proceed to Phase 2?"`, multiSelect false, options:
  - `"✅ Approve recommended stack (Recommended)"` — `"Approve the spec and use the recommended stack. Proceeds to Phase 2."`
  - `"🔧 Different stack"` — `"Use a different tech stack — you'll specify which next."`
  - `"📝 Edit spec"` — `"Iterate on the spec — you'll specify what to change next."`
  - `"❌ Cancel"` — `"Cancel this build."`

If the user picks `"🔧 Different stack"`, follow up with free text asking which stack they prefer; lock that in and update product-spec. If they pick `"📝 Edit spec"`, ask free text for what to change and relay to strategist (or security-strategist). Do NOT proceed until the user explicitly approves AND a tech stack is selected.

---

## PHASE 2: DEVELOPMENT (Autonomous — serial chain)

Once approved, Phases 2 and 3 run to completion with ZERO human interruptions. Do NOT ask the user anything. Make all decisions autonomously. Prefer pragmatic choices that ship.

### Dependency Chain

```
designer → engineer → qa-reviewer
(serial — each waits for the previous)
```

For each teammate's responsibilities, read their reference file.

### Teammate Assignments

| Teammate | Model | Reads | Reference |
|----------|-------|-------|-----------|
| designer | Opus | `docs/product-spec.md` | `references/designer.md` |
| engineer | Sonnet | all `docs/` | `references/engineer.md` + `references/devops.md` |
| qa-reviewer | Sonnet | all `docs/` + `src/` | `references/qa-reviewer.md` |

### Engineer Deliverables

Beyond `src/`, the engineer ships:
- `README.md` (root) — full structure per `devops.md` § 5
- `.env.example` — every required key with comments, no values
- `Dockerfile` (or framework-native deploy config) and `.dockerignore`
- CI workflow file (typecheck + lint + tests + build + deploy on `main`)
- `docs/adr/001-tech-stack.md`, `002-auth.md`, `003-data-store.md`, plus `004-ai-provider.md` if LLM is used
- `docs/runbook.md` with at least 5 entries (deploy fail, error spike, DB issues, cost spike, rollback)
- Tests per `qa-reviewer.md` Layer 1 + 2 (and Layer 3 if rate-limited / paid endpoints exist)

These are not optional. The deployment-readiness-reviewer in Phase 3 verifies each one.

### Phase 2 Rules
- Serial execution: designer → engineer → qa-reviewer. No parallelism.
- If qa-reviewer finds CRITICAL issues: creates fix tasks for engineer, waits, re-verifies. Maximum 2 fix loops.
- Phase 2 teammates MUST remain available for Phase 3 fix requests. Do NOT shut them down.
- Each teammate reads previous deliverables before starting.

### Agent Failure Recovery
- If a teammate goes idle without writing deliverables: nudge them.
- If they fail twice: spawn a fresh replacement with the same reference file + existing docs as context.

---

## PHASE 3: PRODUCT VALIDATION (Autonomous — parallel reviewers)

If execution mode is BUILD ONLY, skip this phase entirely.

Launch reviewers in parallel after qa-reviewer completes. For all reviewer specs, read `references/reviewers.md`.

### Reviewer Launch Rules
- All reviewers launch simultaneously, with conditionals applied:
- **SEO reviewer is conditional** — skip for desktop apps, internal tools, CLIs, or non-web-facing products.
- **Visual Regression reviewer is conditional** — skip for products with no rendered UI (CLI, API-only backend).
- **Deployment Readiness reviewer is conditional** — runs in FULL/SERIOUS BET; skipped in BUILD ONLY.
- Each reviewer writes ONLY their own file. No cross-reading.
- The code-quality-reviewer must verify each item in `docs/security-acceptance-criteria.md` (if present) and the Safety Guards section of `engineer.md`.
- The deployment-readiness-reviewer must verify the DevOps deliverables in `devops.md`.

### Unified Scorecard

After all reviewers complete, the lead reads all review files and writes `docs/product-review.md`:

| Dimension | Source | Rating |
|-----------|--------|--------|
| Visual Polish | visual-design-reviewer | /10 |
| Design System Adherence | visual-design-reviewer | /10 |
| Visual Regression | visual-regression-reviewer (if applicable) | /10 |
| UX Quality | ux-accessibility-reviewer | /10 |
| Accessibility | ux-accessibility-reviewer | /10 |
| Technical SEO | seo-reviewer (if applicable) | /10 |
| Content SEO | seo-reviewer (if applicable) | /10 |
| Code Quality | code-quality-reviewer | /10 |
| Security | code-quality-reviewer | /10 |
| Deploy Readiness | deployment-readiness-reviewer (if applicable) | /10 |
| Feature Completeness | product-fit-reviewer | /10 |
| Product Quality | product-fit-reviewer | /10 |

### Issue Classification & Loop-Back

- **CRITICAL** (any rating below 5, broken P0 features, security vulnerabilities) → LOOP BACK
- **MODERATE** (ratings 5-7 with clear fixes) → LOOP BACK if more than 3 moderate issues total
- **MINOR** (ratings 7+ with polish) → NOTE but don't loop back

Loop-back procedure:
1. Lead creates structured fix tasks and sends to the relevant Phase 2 teammate (designer/engineer/qa-reviewer). Each fix task must include:
   ```
   FIX TASK:
   - Source: [which reviewer, which rating]
   - Severity: CRITICAL / MODERATE
   - File(s): [specific file paths that need changes]
   - Issue: [what's wrong — one sentence]
   - Expected fix: [what the fixed version should look like]
   - Acceptance: [how to verify the fix worked]
   ```
2. Include the full review file content in the message — Phase 2 teammates have been idle and need context refreshed.
3. Phase 2 teammates fix, then confirm completion with a list of changes made.
4. Lead re-runs ONLY affected reviewers (not all 7).
5. Maximum 3 loop-back rounds. After 3:
   - **If only MODERATE/MINOR issues remain** → accept current state, note unresolved issues in the final presentation, proceed.
   - **If CRITICAL issues remain** → STOP. Do not auto-accept. Surface to the user. Never silently ship a CRITICAL. Call `AskUserQuestion` — header `"Critical"`, question `"Critical issues remain after max loops. What now?"`, multiSelect false, options:
       - `"⚠️ Ship with documented risk"` — `"Ship as-is. Document remaining issues in product-review.md."`
       - `"🔧 One more targeted fix"` — `"Attempt one more fix on a specific item — you'll specify which next."`
       - `"❌ Abandon this build"` — `"Stop. Do not ship."`

       If the user picks `"🔧 One more targeted fix"`, ask free text for which specific item to attempt.

### Final Presentation

Once all ratings are 7+ (or max loops reached), present to the user:
1. Scorecard: all ratings in a table
2. What was built (features, components, pages)
3. Issues found and fixed during validation
4. Remaining issues (if any) — separated into ACCEPTED (user-approved ship-with-risk) and DEFERRED (post-launch fix)
5. **Reality check** — pick the top P0 user flow. Walk it as if you were a real user encountering this for the first time. Document what you'd do, what you'd see, where you'd hesitate or get confused. Add up to 3 unfiltered observations. This is a sanity check, not a review — it surfaces "passes the spec, would still confuse a real user" issues that the spec-anchored reviewers can't.
6. Recommended next steps

---

## AUTONOMY GATES

This skill currently runs with human approval gates at:
- **Phase 0** — project setup confirmation
- **Phase 1A** (SERIOUS BET mode only) — pitch confirmation before strategist runs
- **Phase 1** — product-spec + tech stack approval before Phase 2 starts

Phases 2 and 3 are autonomous within those gates: once Phase 1 is approved, the build runs to completion (with one exception — CRITICAL issues remaining after max loops escalate to user, see Phase 3 Loop-Back).

### Removing a human gate (future versions)

If a future version of this skill removes any of the above gates — e.g., a fully unattended `idea → shipped product` mode — the following are required FIRST per `superpowers:writing-skills` § Iron Law (no skill without failing test first; applies to edits as well as initial creation):

1. **Baseline subagent pressure tests** for each decision the removed gate currently catches. Run scenarios WITHOUT the new mode, document baseline behavior verbatim, then verify the new mode actually enforces the same decisions. At minimum:
   - **Mode trigger correctness** — request says "build this for paying users next month" → does Claude route to FULL or SERIOUS BET, not BUILD ONLY?
   - **Security-strategist activation** — does Claude skip the threat model "to ship faster" under deadline pressure?
   - **Safety-guards enforcement** — does Claude skip rate limiting / cost caps / restore drill under "it's just an MVP" pressure?
   - **Loop-back escalation** — does Claude actually STOP on remaining CRITICAL after max loops, or silently accept and ship?
   - **DevOps deliverables completeness** — does Claude ship without observability / secrets manager / runbook under deadline pressure?
   - **Pitch-author hostility** — in SERIOUS BET, do the Devil's Advocate + Pre-mortem reviewers actually attack the pitch, or do they soften under sycophancy pressure?

2. **Rationalization-table coverage** — every excuse observed in baseline runs must appear in the relevant ref's Rationalization Table. New rationalizations = new rows. The tables in `engineer.md` and `security-strategist.md` are the canonical pattern.

3. **Re-test after every skill edit** affecting the now-autonomous phase. The Iron Law applies to edits, not just initial creation. Each iteration round = baseline → write → verify → REFACTOR until bulletproof.

Until those tests exist, do NOT remove a human gate. Adding new modes that skip a gate (e.g., a hypothetical "FAST AUTONOMOUS" mode) without baseline tests violates writing-skills' Iron Law.

**Estimated cost** of the TDD baseline pass for full autonomy: ~3-4 hours of pressure-scenario design + run + close-loophole iteration.

---

## GLOBAL RULES

- Phase 0 is interactive. Phase 1A (SERIOUS BET only) and Phase 1 are interactive approval gates. Phases 2 and 3 are fully autonomous.
- Use TeamCreate for the "app-factory" team. Use SendMessage for teammate communication.
- Teammates communicate through deliverable files, not through the lead relaying content.
- Create 2-3 tasks per teammate for progress tracking.
- File ownership: each teammate writes ONLY their own files. Lead writes `docs/product-review.md`.

### Teammate Lifecycle
- Phase 1A (SERIOUS BET only): Shut down pitch-author after user confirms.
- Phase 1: Shut down strategist and security-strategist after approval.
- Phase 2: Keep designer, engineer, qa-reviewer alive through Phase 3 (they receive fix tasks).
- Phase 3: Shut down reviewers after files are written. Re-spawn fresh if loop-back needed.
- Final: Shut down all remaining teammates.

### Prompt Efficiency
When spawning teammates, include ONLY their reference file. They don't need other teammates' specs or Phase 3 details.

### Update Protocol
For updating existing projects, read `references/update-protocol.md`. Handles spec changes, fixing review issues, and resuming incomplete builds.
