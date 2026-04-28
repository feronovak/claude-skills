---
name: app-factory
description: End-to-end application development — takes a product idea (from brainstormers-idea, business-sharks, or direct input), creates a product spec, then builds it with design, engineering, QA, and parallel product validation. Use this skill when the user wants to build an app, create a product, develop a web application, or turn an idea into working code. Triggers on phrases like 'build this app', 'create this product', 'develop this', 'make this into an app', 'build the MVP'.
version: "3.0"
authors: Fero Novak <https://feronovak.com>
---

End-to-end application manufacturing. Takes research output or a specific product description and builds it: product spec → design → engineering → QA → parallel validation with loop-back fixes.

The app is: $ARGUMENTS

## Reference Files

This skill uses bundled reference files. Load them as follows:

- **strategist** gets: `references/strategist.md`
- **designer** gets: `references/designer.md`
- **engineer** gets: `references/engineer.md`
- **qa-reviewer** gets: `references/qa-reviewer.md`
- **Phase 3 reviewers** — read `references/reviewers.md` for all 5 reviewer specs
- **Team lead** reads: `references/update-protocol.md` (for updates to existing projects)

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

After project setup, check which optional enhancement skills the user has installed. These skills significantly improve output quality in their domains — the built-in methodology is solid but the specialized skills are deeper.

### How to Check

Look for these skills in the available skills list:

| Skill | Used By | Enhancement |
|-------|---------|-------------|
| `interface-design:init` | designer | Design system creation with production-grade tokens and patterns |
| `interface-design:audit` | visual-design-reviewer | Deep visual audit with design system violation detection |
| `interface-design:critique` | visual-design-reviewer | Design craft critique — catches "looks default" problems |
| `frontend-design` | designer | Component design with distinctive, non-generic visual identity |
| `seo-technical-optimization` | seo-reviewer | Technical SEO analysis (meta, structured data, Core Web Vitals) |
| `security-scanning:security-sast` | code-quality-reviewer | Static analysis security scanning beyond checklist review |

### Present to User

Report what was found, with recommendations for missing critical skills:

```
Skill check:
  ✅ interface-design — installed (designer + visual reviewer will use it)
  ❌ frontend-design — not installed
  ✅ security-scanning — installed (code reviewer will use it)
  ❌ seo-technical-optimization — not installed
```

### Critical Skill Recommendations

If either of these two skills is missing, strongly recommend installation. They cover design capabilities that the built-in methodology cannot fully replicate.

**`interface-design`** (HIGH impact — design system + visual review)
> This skill transforms how the designer creates your design system. Without it, the designer follows a solid checklist — picks colors, sets typography, defines spacing. With it, the designer explores your product's domain, rejects generic defaults explicitly, builds a token architecture where every visual value traces to intent, and runs 4 craft tests (Swap, Squint, Signature, Token) before delivering. The visual reviewer also uses it to catch design system violations and "looks default" problems that a checklist audit will miss. The difference is a design system that looks *intentional* vs one that looks *professional but templated*.
>
> Install: `claude install-skill anthropic/interface-design`

**`frontend-design`** (HIGH impact — component distinctiveness)
> This skill pushes components from "well-structured" to "memorable." Without it, the designer specs components with correct anatomy, variants, and states — functional and clean. With it, the designer commits to a bold aesthetic direction, uses distinctive typography instead of safe defaults, applies spatial composition (asymmetry, negative space, density variation), and designs motion that reinforces the product's personality. The difference is components that could belong to any app vs components someone would screenshot and share.
>
> Install: `claude install-skill anthropic/frontend-design`

Present the recommendation like this:

```
⚠️  Two skills are missing that significantly affect design quality:

1. interface-design — makes design systems intentional, not templated
   Install: claude install-skill anthropic/interface-design

2. frontend-design — makes components distinctive, not generic
   Install: claude install-skill anthropic/frontend-design

Without them, the build will use solid built-in methodology (covers
design principles, anti-patterns, craft tests) but the output won't
match what these specialized skills produce.

Options:
  a) Install now (recommended — takes ~30 seconds each)
  b) Proceed without — built-in methodology will be used
  c) Skip all external skills — built-in only
```

The user may:
- **Install recommended skills** → wait, then re-check
- **Proceed as-is** → use whatever is available, built-in for the rest
- **Skip all external skills** → use only built-in methodology

Store the result as `{enhanced_skills}` — pass this to teammates so they know which path to take.

---

## EXECUTION MODE

Ask the user which mode to use.

**Mode inheritance:** If the user previously ran another pipeline skill (brainstormers-idea, business-sharks) in this session and chose a mode, default to the equivalent: STANDARD → FULL, QUICK → BUILD ONLY. Mention it: "You used STANDARD for the previous steps — I'll default to FULL here. Change?"

**FULL** (default): Build + validate. All 3 phases.
- Phase 1: strategist (Opus)
- Phase 2: designer → engineer → qa-reviewer (serial, Sonnet)
- Phase 3: 5 parallel reviewers + loop-back fixes
- Best for production-quality builds

**BUILD ONLY**: Build without validation. Phases 1 + 2 only.
- Skips Phase 3 entirely
- Faster, cheaper
- Best for prototypes, internal tools, or quick MVPs

Default to FULL. Use BUILD ONLY if user says "quick", "prototype", "just build it", etc.

---

## PHASE 1: PRODUCT SPEC (Interactive — human approval gate)

Strategist reads the input source and writes `docs/product-spec.md`. For the strategist's full responsibilities and output format, read `references/strategist.md`.

### Phase 1 Presentation

When strategist completes, present to the user:
1. Product summary (2-3 sentences)
2. P0 features list (the MVP)
3. Tech stack options (3 options with recommendation — user picks one)
4. Key user flows (one-line each)
5. Open questions (if any)

Then STOP and WAIT. The user must approve the spec AND pick a tech stack. They may:
- **Pick a stack** → lock it in, update product-spec
- **Propose their own stack** → use it, note as "user-specified" in product-spec
- **Request changes** → relay to strategist, iterate, present again
- **Ask questions** → answer from the spec
- **Say "approved"** → proceed to Phase 2

Do NOT proceed until the user explicitly approves AND a tech stack is selected.

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
| designer | Sonnet | `docs/product-spec.md` | `references/designer.md` |
| engineer | Sonnet | all `docs/` | `references/engineer.md` |
| qa-reviewer | Sonnet | all `docs/` + `src/` | `references/qa-reviewer.md` |

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
- All reviewers except SEO launch simultaneously.
- **SEO reviewer is conditional** — skip for desktop apps, internal tools, CLIs, or non-web-facing products.
- Each reviewer writes ONLY their own file. No cross-reading.

### Unified Scorecard

After all reviewers complete, the lead reads all review files and writes `docs/product-review.md`:

| Dimension | Source | Rating |
|-----------|--------|--------|
| Visual Polish | visual-design-reviewer | /10 |
| Design System Adherence | visual-design-reviewer | /10 |
| UX Quality | ux-accessibility-reviewer | /10 |
| Accessibility | ux-accessibility-reviewer | /10 |
| Technical SEO | seo-reviewer (if applicable) | /10 |
| Content SEO | seo-reviewer (if applicable) | /10 |
| Code Quality | code-quality-reviewer | /10 |
| Security | code-quality-reviewer | /10 |
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
4. Lead re-runs ONLY affected reviewers (not all 5).
5. Maximum 3 loop-back rounds. After 3, accept current state and note unresolved issues in the final presentation.

### Final Presentation

Once all ratings are 7+ (or max loops reached), present to the user:
1. Scorecard: all ratings in a table
2. What was built (features, components, pages)
3. Issues found and fixed during validation
4. Remaining issues (if any)
5. Recommended next steps

---

## GLOBAL RULES

- Phase 0 is interactive. Phase 1 is interactive (approval gate). Phases 2 and 3 are fully autonomous.
- Use TeamCreate for the "app-factory" team. Use SendMessage for teammate communication.
- Teammates communicate through deliverable files, not through the lead relaying content.
- Create 2-3 tasks per teammate for progress tracking.
- File ownership: each teammate writes ONLY their own files. Lead writes `docs/product-review.md`.

### Teammate Lifecycle
- Phase 1: Shut down strategist after approval.
- Phase 2: Keep designer, engineer, qa-reviewer alive through Phase 3 (they receive fix tasks).
- Phase 3: Shut down reviewers after files are written. Re-spawn fresh if loop-back needed.
- Final: Shut down all remaining teammates.

### Prompt Efficiency
When spawning teammates, include ONLY their reference file. They don't need other teammates' specs or Phase 3 details.

### Update Protocol
For updating existing projects, read `references/update-protocol.md`. Handles spec changes, fixing review issues, and resuming incomplete builds.
