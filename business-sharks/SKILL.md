---
name: business-sharks
description: Rigorous startup/business idea validation — market research, competitive intel, SEO/GEO, financials, and structured multi-analyst stress-test with GO/NO-GO verdict. Use this skill when the user wants to evaluate a startup idea, validate a business concept, assess whether to build something, do due diligence on a product idea, analyze market opportunity, or get a GO/NO-GO verdict on a new venture. Triggers on phrases like 'is this idea worth pursuing', 'should I build this', 'analyze this business', 'evaluate my startup', 'shark tank this idea', 'due diligence'.
version: "4.3"
team: business-sharks
authors: Fero Novak <https://feronovak.com>
---

Create an agent team called "business-sharks" for rigorous startup/business idea validation. Five specialized analysts — each applying their own framework — synthesized into a structured GO/NO-GO verdict. Four phases with gated interaction at Phase 0 (folder setup) and Phase 3 (interactive review) only. 5 teammates.

Note on framing: the "shark tank" trigger phrases are idiomatic shorthand users search for. What's actually delivered is analyst-driven: distinct frameworks per role, not character personas debating. The chief-shark synthesizes across all analysts and delivers the verdict — that's where the judgment lives.

The business idea is: $ARGUMENTS

## Reference Files

This skill uses bundled reference files. Load them as follows:

- **Every teammate** gets: `references/defensive-principles.md` (principles, section format, length limits)
- **market-researcher** gets: `references/market-researcher.md`
- **competitive-intel** gets: `references/competitive-intel.md`
- **digital-scout** gets: `references/digital-scout.md`
- **financial-modeler** gets: `references/financial-modeler.md`
- **chief-shark** gets: `references/chief-shark.md`
- **Team lead** reads: `references/update-protocol.md` (for update/amendment runs)

When spawning a teammate, include ONLY the defensive-principles file + their role-specific file. This reduces context consumption by ~40% per teammate.

---

## INPUT TRIAGE

Before setting up a project, check whether brainstormers-idea output exists:

### 1. brainstormers-idea output detected
The user points to a brainstormers-idea folder, or $ARGUMENTS references one. Confirm by checking for `docs/05-refined-idea.md`.

If found:
- Store the brainstormers-idea folder path as `{prior-research-path}`
- Read `05-refined-idea.md` — use the "Refined Idea" section as the business idea for `00-business-idea.md` (instead of raw user input)
- The prior research files (`01-market-landscape.md`, `02-competition-map.md`, `03-timing-window.md`, `04-revenue-models.md`) will be passed to relevant analysts as starting context. They CHALLENGE and EXTEND this research, not repeat it.
- Tell the user: "I found brainstormers-idea output. I'll use the refined idea as the starting point and give your prior research to the analysts to stress-test."

### 2. No prior research
Proceed normally — user provides the business idea directly in $ARGUMENTS.

### Mapping Prior Research to Analysts

When brainstormers-idea output exists, each analyst receives their prior research file alongside `00-business-idea.md`:

| Analyst | Receives prior research file | Instruction |
|---------|------------------------------|-------------|
| market-researcher | `01-market-landscape.md` | Challenge the market sizing. Validate or dispute demand signals. Dig deeper into problem intensity — brainstormers was creative, you are critical. |
| competitive-intel | `02-competition-map.md` | Stress-test the competitive gaps. Are the "opportunities" real or wishful thinking? Check for competitors brainstormers missed. Assess moat honestly. |
| digital-scout | (none) | No equivalent in brainstormers-idea. Research from scratch. |
| financial-modeler | `04-revenue-models.md` | Take the proposed revenue models and run the actual numbers. Challenge the pricing assumptions. Build unit economics that brainstormers didn't. |

Analysts must NOT simply summarize the prior research. Their job is to apply Defensive AI Principles — challenge, verify, and extend. Prior research is a starting point, not a conclusion. If prior research was wrong, say so.

---

## PHASE 0: PROJECT SETUP (Interactive — before anything else)

Before creating the team or launching any research, set up a dedicated project folder:

1. Generate a suggested folder name from the business idea:
   - Use lowercase kebab-case (e.g., "ai-pet-insurance", "saas-crm-tool")
   - Keep it short (2-4 words) and descriptive of the core idea

2. Present the suggested folder name to the user using AskUserQuestion:
   - Provide the suggested name as the recommended option
   - Let the user confirm, modify, or provide their own name
   - Do NOT proceed until the user confirms

3. Once confirmed, create the project folder structure:
   - Create `{project-folder}/` in the current working directory
   - Create `{project-folder}/docs/` subdirectory

4. Create the business idea file:
   - If brainstormers-idea input: write `00-business-idea.md` using the refined idea from `05-refined-idea.md`. Add a note at the top: `**Source:** brainstormers-idea output from {prior-research-path}`
   - If direct input: write `00-business-idea.md` with the user's business idea text
   - Add `**Analysis Date:** [date]`
   - This file is the single source of truth — all teammates read it

5. Store the confirmed project folder path. ALL subsequent file operations use `{project-folder}/docs/`.

### File Structure

```
{project-folder}/docs/
  00-business-idea.md           # team lead creates in Phase 0
  01-problem-validation.md      # market-researcher
  02-market-size-timing.md      # market-researcher
  03-competitive-landscape.md   # competitive-intel
  04-defensibility-moat.md      # competitive-intel
  05-digital-seo-geo.md         # digital-scout
  06-unit-economics.md          # financial-modeler
  07-financial-projections.md   # financial-modeler
  08-gtm-strategy.md            # chief-shark
  09-risk-matrix.md             # chief-shark
  10-scalability.md             # chief-shark
  11-yc-evaluation.md           # chief-shark
  12-scorecard.md               # chief-shark
  13-executive-summary.md       # chief-shark
  14-cross-reference.md         # chief-shark
  15-questions.md               # chief-shark
  16-pivot.md                   # chief-shark (conditional)
```

### File Ownership Rules
- Each file has ONE owner. Only the owner writes to that file.
- No teammate ever writes to another teammate's file.
- When a section is updated, the owner OVERWRITES with new content. No appending, no version suffixes.

### Phase 0 Rules
- Phase 0 MUST complete before creating the team or launching teammates.
- The folder is created in the CURRENT WORKING DIRECTORY.
- If the folder already exists, warn the user and ask whether to reuse or pick a new name.

---

## EXECUTION MODE

Before creating the team, ask the user which mode to use.

**Mode inheritance:** If the user previously ran another pipeline skill (brainstormers-idea, app-factory) in this session and already chose a mode, default to the equivalent mode. Mention it: "You used STANDARD for brainstormers-idea — I'll default to STANDARD here too. Change?" This prevents asking the same question repeatedly across the pipeline.

**STANDARD** (default): Full team for all phases.
- Phase 1: 4 team members (Opus x2, Sonnet x2) running in parallel
- Phase 2-3: chief-shark as team member (interactive)
- Supports Phase 3 deep dives with original analysts
- Token cost: highest

**HYBRID** (recommended for cost-conscious runs):
- Phase 1: 4 background subagents via Task tool (run_in_background=true). Each writes their section files and auto-terminates.
- Phase 2-3: Create team with ONLY chief-shark. Reads all section files.
- Phase 3 deep dives: spawn fresh subagents as needed
- Token savings: ~40% vs Standard

**QUICK** (fastest, cheapest):
- Phase 1: 4 background subagents, ALL Sonnet model, single pass (skip Pass 1 drafts)
- Phase 2: 1 Opus subagent for synthesis (not a team member)
- Phase 3: Team lead presents findings directly. No interactive follow-up.
- Token savings: ~60% vs Standard

When asking the user to choose a mode, call `AskUserQuestion` — header `"Mode"`, question `"Pick a validation mode."`, multiSelect false, options:
  - `"💰 HYBRID (Recommended)"` — `"Balanced. Background subagents for Phase 1, chief-shark team for Phases 2-3. ~40% token savings."`
  - `"🦈 STANDARD"` — `"Full team for all phases. Best for high-stakes validation."`
  - `"⚡ QUICK"` — `"All Sonnet, single pass, no Phase 3 follow-up. Fastest, cheapest. ~60% token savings."`

Map the answer to `QUICK`, `HYBRID`, or `STANDARD`.

---

## PHASE 1: TWO-PASS PARALLEL RESEARCH (Fully autonomous)

Phase 1 has two passes. Both are fully autonomous — do NOT ask the user anything.

### Pass 1: Research & Draft Key Findings (parallel)

All 4 research teammates launch simultaneously. Each reads `{project-folder}/docs/00-business-idea.md`, conducts research, and writes ONLY their Key Findings block (not the full section) to their section files.

After Pass 1, each section file contains only the header, rating, and Key Findings block (~10-15 lines). Detailed analysis is NOT written yet.

### Pass 2: Cross-Read & Write Full Sections (parallel)

Once all Key Findings drafts exist, each teammate:
1. Reads the OTHER 3 teammates' Key Findings blocks
2. OVERWRITES their own section files with the FULL analysis (Key Findings + detailed content + Questions for Founder)

This cross-read ensures each analyst knows the broader context before writing, eliminating contradictions and redundancy at the source.

### Teammate Assignments

| Teammate | Model | Reads | Prior Research (if available) | Writes |
|---|---|---|---|---|
| market-researcher | Opus | 00 | brainstormers `01-market-landscape.md` | 01, 02 |
| competitive-intel | Opus | 00 | brainstormers `02-competition-map.md` | 03, 04 |
| digital-scout | Sonnet | 00 | (none) | 05 |
| financial-modeler | Sonnet | 00 | brainstormers `04-revenue-models.md` | 06, 07 |

For each teammate's analytical framework and responsibilities, read their reference file in `references/`.

When prior research exists, include it in the teammate's prompt with the instruction: "Prior creative research is attached. Your job is to CHALLENGE and EXTEND it, not summarize it. Apply Defensive AI Principles. If the prior research was optimistic, find what it missed. If it was accurate, go deeper."

### Phase 1 Rules
- Pass 1: All 4 researchers start simultaneously. Each writes ONLY Key Findings drafts.
- Pass 2: Once all Key Findings exist, each researcher cross-reads then OVERWRITES with full analysis.
- NO-REPEAT RULE: Reference other sections by file number: "The free-tier pricing pressure (see 03) makes CAC estimation challenging." Never re-explain what another section covers.
- If a teammate identifies missing critical information, add questions under `### Questions for Founder`.
- Do NOT soften findings. Apply Defensive AI Principles rigorously.
- Phase 1 completes when all 4 researchers have written full sections (Pass 2 done).
- Do NOT present anything to the user during Phase 1.

### Agent Failure Recovery (Phase 1)

Agents may go idle, get interrupted, or fail to write their files:
- After launching Pass 1 or Pass 2, verify each teammate's expected files exist before proceeding.
- If a teammate goes idle WITHOUT writing files: send them a message to resume. Include: "You were assigned [section files]. Please complete them now."
- If a teammate fails twice after nudging: shut them down and spawn a FRESH replacement agent for the same role. Provide the same context.
- Do NOT block the entire phase for one stalled agent. If 3 of 4 complete, start nudging the 4th immediately.
- Log any agent failures so the user is informed during Phase 3.

---

## PHASE 2: SHARK SYNTHESIS (Fully autonomous)

Chief-shark starts ONLY after all 4 Phase 1 teammates complete (both passes).

Chief-shark reads ALL files `00` through `07` (Key Findings first for overview, then detail as needed) and writes files `08` through `15`, conditionally `16`.

For chief-shark's full responsibilities, analytical frameworks, scorecard rules, WWNBT framework, and pivot rules, read `references/chief-shark.md`.

### Phase 2 Rules
- Chief-shark scores dimensions 7-13 independently based on synthesis — do not simply average Phase 1 scores.
- If Phase 1 analysts flagged "INSUFFICIENT DATA", chief-shark preserves those flags AND reduces scores accordingly.
- NO-REPEAT RULE applies: reference Phase 1 findings by file number.
- Do NOT present to the user during Phase 2.
- When Phase 2 is complete, SHUT DOWN all 4 Phase 1 teammates. Then proceed to Phase 3.

### Agent Failure Recovery (Phase 2)

Chief-shark writes 9 files (08-16). If it stalls mid-synthesis:
- Check which files have been written and which are missing.
- If chief-shark goes idle with files remaining: send a message listing the missing files and instruct it to continue.
- If chief-shark fails twice after nudging: shut it down and spawn a FRESH chief-shark. Provide `references/chief-shark.md` + `references/defensive-principles.md` + all existing section files as context. Instruct it to write only the missing files.
- Do NOT re-run Phase 1. The Phase 1 output files are the input.

---

## PHASE 3: SHARK TANK (Interactive with human)

When Phase 2 completes, the team lead presents to the user:

1. **The Verdict** — GO / CONDITIONAL / NO-GO with average score and strategy lens used
2. **Scorecard table** — all 13 dimensions with scores and one-line findings (from `12-scorecard.md`)
3. **WWNBT** — if CONDITIONAL: key assumptions to validate with test methods and timeline
4. **Executive Summary** — 3-sentence pitch, top 3 strengths, top 3 weaknesses, hardest question (from `13-executive-summary.md`)
5. **Key Contradictions** — tensions between analysts (from `14-cross-reference.md`)
6. **Questions for Founder** — unanswered questions (from `15-questions.md`)
7. **The single most important thing** the founder needs to hear

Then STOP and WAIT for user response. Adapt the first option's label to match the verdict (GO → "🚀 Build it"; CONDITIONAL → "🔁 Iterate"; NO-GO → "🧭 Pivot"). Call `AskUserQuestion` — header `"Next step"`, question `"What's next?"`, multiSelect false, options (4 max — "Other" is auto-added for free text, do NOT add it manually):

- **First option, verdict-dependent:**
  - GO → `"🚀 Build it (Recommended)"` — `"Chain to app-factory using this folder as input."`
  - CONDITIONAL → `"🔁 Iterate (Recommended)"` — `"Re-test the WWNBT assumptions before building."`
  - NO-GO → `"🧭 Pivot (Recommended)"` — `"Explore pivot suggestions and write `16-pivot.md`."`
- `"🔍 Refine"` — `"Deeper dive on a section OR challenge a rating with new info. You'll specify which next."`
- `"🧭 Explore pivot path"` — `"Write `16-pivot.md` with pivot suggestions."` (skip this option if verdict is NO-GO — it's already absorbed into the first option)
- `"✅ Final"` — `"Lock the report and stop."`

If the user picks `"🔍 Refine"`, follow up with a second `AskUserQuestion` — header `"Refine"`, question `"What kind?"`, options: `"Deeper dive on a section"`, `"Challenge a rating with new info"`. Then ask the user to specify which section or which rating + the new info as free text.

### Phase 3 Interaction Rules

The user may:

- **Ask questions** — Answer from the report. If not covered, say so and offer to spin up a fresh analyst.
- **Provide additional information** — Spin up a FRESH researcher with `00-business-idea.md` + their existing section file(s). Researcher OVERWRITES their files. Then chief-shark re-scores.
- **Challenge a rating** — Chief-shark defends with evidence. Only adjust if founder provides compelling NEW information. NEVER adjust just because the founder disagrees.
- **Request deeper dive** — Spin up a FRESH analyst with their existing file. Analyst OVERWRITES with expanded version. Chief-shark re-synthesizes.
- **Say "final"** — Lock the report. Shut down chief-shark and clean up the team.

### Phase 3 Rules
- No limit on interaction rounds. Keep iterating until "final".
- Phase 1 agents are SHUT DOWN after Phase 2. Only chief-shark remains.
- For re-analysis, spin up FRESH agents with `00-business-idea.md` + existing section file + new information.
- When "final", shut down all remaining teammates and clean up.

---

## GLOBAL COORDINATION RULES

- Phase 0 (folder setup) MUST complete before any other phase
- All teammates write ALL files inside `{project-folder}/docs/`
- Create 3-5 tasks per teammate for granular progress tracking
- Phase 1 Pass 1: all 4 researchers write Key Findings drafts in PARALLEL
- Phase 1 Pass 2: all 4 researchers cross-read then write full sections in PARALLEL
- Phase 2: chief-shark is BLOCKED until all Phase 1 Pass 2 outputs are complete
- Phase 2 completion: SHUT DOWN all Phase 1 agents
- Phase 3: user presentation ONLY after chief-shark completes
- ONE FILE PER SECTION — each teammate writes only their own numbered files
- When re-analyzing: OVERWRITE. Never append versions.
- NO-REPEAT RULE: Reference by file number, don't re-describe
- Apply Defensive AI Principles to every section — non-negotiable
- Phase 0 is interactive, Phases 1-2 are autonomous, Phase 3 is interactive

### Skill & Tool Access
This workflow is SELF-CONTAINED. All analysis uses web research + built-in analytical frameworks. Teammates do NOT depend on external skills or plugins.

### Update & Amendment Protocol
For updating existing analyses rather than creating new ones, read `references/update-protocol.md`.
