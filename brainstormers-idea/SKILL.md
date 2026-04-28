---
name: brainstormers-idea
description: Creative idea research team — takes a raw idea, interviews for context, researches market/competition/timing/revenue in parallel, then synthesizes into a refined idea with strategy. Use this skill when the user wants to explore a business idea, brainstorm a product concept, research whether something is worth building, shape a raw idea into something concrete, or get creative research on a new venture. Triggers on phrases like 'brainstorm this idea', 'research this concept', 'help me shape this idea', 'explore this opportunity', 'is this idea any good'.
version: "2.1"
authors: Fero Novak <https://feronovak.com>
---

Creative idea research and shaping. Four phases: folder setup, discovery interview, parallel research sprint, and interactive presentation. 5 teammates research market, competition, timing, revenue, and synthesize into a refined idea.

The raw idea is: $ARGUMENTS

## Reference Files

This skill uses bundled reference files. Load them as follows:

- **Every teammate** gets: `references/creative-principles.md` (principles, citation rules, section format, file rules)
- **market-explorer** gets: `references/market-explorer.md`
- **competition-scout** gets: `references/competition-scout.md`
- **window-validator** gets: `references/window-validator.md`
- **revenue-architect** gets: `references/revenue-architect.md`
- **idea-architect** gets: `references/idea-architect.md`
- **Team lead** reads: `references/update-protocol.md` (for update/amendment runs)

When spawning a teammate, include ONLY creative-principles + their role-specific file. This reduces context consumption per teammate.

---

## PHASE 0: PROJECT SETUP (Interactive)

Before creating the team or launching any research, set up a dedicated project folder:

1. Generate a suggested folder name from the raw idea:
   - Use lowercase kebab-case (e.g., "ai-writing-coach", "local-food-marketplace")
   - Keep it short (2-4 words) and descriptive of the core concept

2. Present the suggested folder name to the user using AskUserQuestion:
   - Provide the suggested name as the recommended option
   - Let the user confirm, modify, or provide their own name
   - Do NOT proceed until the user confirms

3. Once confirmed, create the project folder structure:
   - Create `{project-folder}/` in the current working directory
   - Create `{project-folder}/docs/` subdirectory

4. Store the confirmed project folder path. ALL subsequent file operations by ALL teammates use `{project-folder}/docs/` as the output directory.

### File Structure

```
{project-folder}/docs/
  00-idea-brief.md            # Team lead creates from interview (Phase 1)
  01-market-landscape.md      # market-explorer
  02-competition-map.md       # competition-scout
  03-timing-window.md         # window-validator
  04-revenue-models.md        # revenue-architect
  05-refined-idea.md          # idea-architect
  06-strategy-brief.md        # idea-architect
```

### Phase 0 Rules
- Phase 0 MUST complete before creating the team or launching any teammates.
- The folder is created in the CURRENT WORKING DIRECTORY.
- If the folder already exists, warn the user and ask whether to reuse or pick a new name.

---

## EXECUTION MODE

After confirming the project folder, ask the user which mode to use.

**Mode inheritance:** If the user previously ran another pipeline skill (business-sharks, app-factory) in this session and already chose a mode, default to the same mode. Mention it: "You used STANDARD for the previous step — I'll default to STANDARD here too. Change?" This prevents asking the same question 3 times across the pipeline.

**STANDARD** (default): Full depth research with the best models.
- Phase 2: 4 agents (Opus x2 for market-explorer + revenue-architect, Sonnet x2 for competition-scout + window-validator)
- Phase 3: idea-architect runs as Opus
- Best for ideas you're seriously considering pursuing
- Token cost: highest

**QUICK** (faster, cheaper): Good for early-stage exploration when you want a fast read.
- Phase 2: 4 agents, ALL Sonnet — faster and cheaper
- Phase 3: idea-architect still runs as Opus (synthesis quality matters)
- Shorter interview: 3-5 questions instead of 5-8
- Target section lengths reduced by ~30%
- Best for quick gut-checks or when exploring multiple ideas
- Token savings: ~40% vs Standard

Default to STANDARD if user says "go" or doesn't specify. If the user explicitly asks for speed or says something like "quick pass" or "just a rough look", use QUICK.

The selected mode determines model assignments in the Teammate Assignments table (Phase 2). In QUICK mode, override all researcher models to Sonnet.

---

## PHASE 1: IDEA DISCOVERY (Interactive — team lead interviews user)

The team lead acts as the interviewer. No separate teammate needed.

### Interview Approach

Ask 5-8 focused questions to understand the idea deeply. Use AskUserQuestion with multiple-choice options where possible to keep it fast.

Cover these dimensions (adapt to the specific idea — not every question applies):

1. **The Problem**: What specific problem does this solve? Who has it? How painful is it?
2. **Target Audience**: Who is the ideal first user? Be specific — job title, situation, context.
3. **Vision & Scope**: What's the dream version? What's the minimum viable version?
4. **Existing Assets**: Domain expertise, existing audience, technical skills, partnerships?
5. **Constraints**: Budget, timeline, solo vs team, technical limitations, geographic focus?
6. **Why Now**: What triggered this idea? Is there a trend, event, or personal experience?
7. **Revenue Intuition**: Initial sense of how this makes money?
8. **Existing Landscape**: Any known competitors? What's missing from them?

### Interview Rules
- Ask 2-3 questions at a time maximum. Do NOT dump all 8 at once.
- Use AskUserQuestion with concrete options where possible.
- Listen for signals — if the user reveals something important, follow up before moving on.
- Keep it conversational, not interrogative. You're a curious co-founder, not a form.
- 5-8 questions total across 2-4 rounds of interaction.

### Writing the Idea Brief

After the interview, write `{project-folder}/docs/00-idea-brief.md` with this structure:

```markdown
# Idea Brief

## The Idea
[1-2 paragraph synthesis of what this is]

## Problem Statement
[What problem does this solve? For whom? How painful is it?]

## Target Audience
[Primary audience description — specific persona(s)]

## Vision
- **Dream version:** [what success looks like at scale]
- **Minimum viable version:** [smallest useful version]

## Founder Assets & Constraints
- **Assets:** [domain expertise, audience, skills, partnerships]
- **Constraints:** [budget, timeline, team size, technical limits]

## Why Now
[What makes this timely?]

## Revenue Intuition
[Any initial thoughts on monetization — or "To be explored"]

## Known Landscape
[Any competitors mentioned — or "To be researched"]

## Research Questions
[Specific questions derived from the interview]
```

### Phase 1 Rules
- Present the completed brief to the user for confirmation before proceeding.
- The user may request changes — iterate until they confirm.
- Once confirmed, proceed to Phase 2.

---

## PHASE 2: RESEARCH SPRINT (Fully autonomous — 4 teammates in parallel)

All 4 research teammates launch simultaneously. Each reads `00-idea-brief.md` and researches their angle. For each teammate's responsibilities and output structure, read their reference file.

### Teammate Assignments

| Teammate | Model | Writes | Reference |
|----------|-------|--------|-----------|
| market-explorer | Opus | `01-market-landscape.md` | `references/market-explorer.md` |
| competition-scout | Sonnet | `02-competition-map.md` | `references/competition-scout.md` |
| window-validator | Sonnet | `03-timing-window.md` | `references/window-validator.md` |
| revenue-architect | Opus | `04-revenue-models.md` | `references/revenue-architect.md` |

### Phase 2 Rules
- All 4 researchers start simultaneously and work in parallel.
- Each researcher reads ONLY `00-idea-brief.md` — they do NOT cross-read each other's output.
- Apply Creative Advisory Principles (from `references/creative-principles.md`) to every section.
- Phase 2 completes when all 4 researchers have written their section files.
- Do NOT present anything to the user during Phase 2.

### Agent Failure Recovery

- After launching Phase 2, verify each teammate's expected file exists before proceeding to Phase 3.
- If a teammate goes idle WITHOUT writing their file: send them a message to resume. Include: "You were assigned [section file]. Please complete it now."
- If a teammate fails twice after nudging: shut them down and spawn a FRESH replacement agent for the same role. Provide the same context.
- Do NOT block the entire phase for one stalled agent. If 3 of 4 complete, start nudging the 4th immediately.
- Log any agent failures so the user is informed during Phase 4.

---

## PHASE 3: IDEA SYNTHESIS (Fully autonomous — 1 teammate)

idea-architect starts ONLY after all 4 Phase 2 teammates complete.

For idea-architect's full responsibilities, output structures, and reality check rules, read `references/idea-architect.md`.

### Phase 3 Rules
- idea-architect reads ALL files thoroughly before writing.
- When Phase 3 is complete, SHUT DOWN all 4 Phase 2 teammates. Then proceed to Phase 4.

---

## PHASE 4: PRESENTATION (Interactive)

When Phase 3 completes, the team lead presents to the user:

1. **Reality Check Verdict** — PROMISING / PIVOT RECOMMENDED / RECONSIDER (from `05-refined-idea.md`). Lead with this.
2. **The Refined Idea** — How the idea evolved, and why (from `05-refined-idea.md`)
3. **Revenue Strategy** — Top 3 revenue models ranked, with recommended pricing (from `06-strategy-brief.md`)
4. **Market Highlights** — Key market size, best audience segment, strongest demand signals (from `01-market-landscape.md`)
5. **Competitive Positioning** — Where the white space is, how to differentiate (from `02-competition-map.md`)
6. **Timing Assessment** — Early / On Time / Late verdict with key factors (from `03-timing-window.md`)
7. **Critical Assumptions** — Top 5 things to validate (from `06-strategy-brief.md`)
8. **Recommended Next Steps** — What to do now (from `06-strategy-brief.md`)

Then STOP and WAIT for user response.

### Phase 4 Interaction

The user may:

- **Ask questions** — Answer from research findings. If not covered, say "This was not covered in our research" and offer to spin up a fresh researcher.
- **Provide new information** — Spin up a FRESH researcher with `00-idea-brief.md` + their existing section file. Researcher OVERWRITES their file. Then idea-architect updates `05` and `06`.
- **Request deeper dive** — Spin up a FRESH researcher with existing file as context. Researcher OVERWRITES with expanded research. Then idea-architect re-synthesizes.
- **Adjust direction** — Update `00-idea-brief.md` with the new direction. Selectively re-run affected researchers and idea-architect.
- **Say "final"** — Lock the research. Shut down idea-architect and clean up.

### Phase 4 Rules
- No limit on interaction rounds. Keep iterating until "final".
- Phase 2 agents are SHUT DOWN after Phase 3. Only idea-architect remains during Phase 4.
- For re-research, spin up FRESH agents. Provide `00-idea-brief.md` + existing section file + new information.

---

## GLOBAL COORDINATION RULES

- Phase 0 (folder setup) MUST complete before any other phase
- Phase 1 (interview) MUST complete and brief MUST be confirmed before Phase 2
- All teammates write ALL files inside `{project-folder}/docs/`
- Create 2-3 tasks per teammate for progress tracking
- Phase 2: all 4 researchers work in PARALLEL
- Phase 3: idea-architect is BLOCKED until all 4 Phase 2 outputs exist
- Phase 3 completion: SHUT DOWN all Phase 2 agents
- Phase 4: presentation happens ONLY after idea-architect completes
- Phases 0 and 1 are interactive, Phases 2 and 3 are autonomous, Phase 4 is interactive
- When "final", shut down all remaining teammates and clean up

### Prompt Efficiency

When spawning teammates, include ONLY the instructions relevant to their role:
- Each researcher gets: `references/creative-principles.md` + their own reference file
- idea-architect gets: `references/creative-principles.md` + `references/idea-architect.md`
- No teammate needs Phase 4 details or other teammates' responsibilities

### Update & Amendment Protocol

For updating existing brainstorms rather than creating new ones, read `references/update-protocol.md`. This covers three update types (BRIEF-ONLY, SECTION-SPECIFIC, DIRECTION CHANGE) and handles resuming incomplete brainstorms.
