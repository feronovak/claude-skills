---
name: brainstormers-content
description: Content research and recommendation team — finds hot topics, analyzes audience demand and competitive landscape, scores for authenticity/timeliness/differentiation, and recommends content with platform assignments. Use this skill when the user wants content ideas, topic research, help deciding what to write or post about, content strategy for LinkedIn/blog/newsletter, or needs to find trending topics in their space. Triggers on phrases like 'what should I write about', 'find me content ideas', 'research topics for my blog', 'content brainstorm', 'what's trending in [area]'.
version: "2.4"
authors: kraboo-labs
---

Content research and recommendation. Three phases: briefing with profile discovery, parallel research sprint (trends + audience + competitive), and strategy synthesis with scored recommendations.

The content area is: $ARGUMENTS

## Reference Files

This skill uses bundled reference files. Load them as follows:

- **Every subagent** gets: `references/content-principles.md` (principles, citation rules, file rules)
- **trend-scanner** gets: `references/trend-scanner.md`
- **audience-researcher** gets: `references/audience-researcher.md`
- **content-scout** gets: `references/content-scout.md`
- **content-strategist** gets: `references/content-strategist.md`
- **Team lead** reads: `references/update-protocol.md` (for update/amendment runs)

When spawning a subagent, include ONLY content-principles + their role-specific file. This reduces context consumption per subagent.

---

## PHASE 0: BRIEFING (Interactive)

### Profile Discovery

The skill needs to know WHO the user is to score authenticity and assign platforms. Check for existing profile information in this order:

1. **Saved persona file** — check for `~/.agents/personas/content-creator.md`. If it exists, read it and confirm: "I found your saved profile. Should I use it, or do you want to update anything?"
2. **CLAUDE.md / project context** — if a user profile exists (role, expertise, channels), use it. Confirm with the user: "I found your profile in the project config. Should I use it, or do you want to update anything?"
3. **If no profile found** — run a discovery interview (4 questions via AskUserQuestion):
   - **Role:** "What's your role?" (e.g., "CTO at a fintech startup", "MD of a media company")
   - **Expertise domains:** "What topics can you speak about from real experience?" (e.g., "product management, AI in media, scaling teams, CEE market"). Push for specifics — "marketing" is too broad, "B2B SaaS content marketing for dev tools" is useful.
   - **Audience:** "Who reads your content?" (e.g., "other startup founders, mostly technical", "CEE media industry professionals")
   - **Channels:** "Where do you publish?" with options: LinkedIn, Blog/website, Newsletter, X/Twitter, Internal comms, Other
4. **Save for next time** — after the first interview, ask: "Want me to save this profile so you don't have to answer these questions next time?" If yes, write the profile to `~/.agents/personas/content-creator.md` using the persona format below.

### Content Area Confirmation

1. If $ARGUMENTS is empty or vague, ask:
   - "What content area should we research?" (e.g., "AI in media", "leadership", "product management")
   - Do NOT proceed until the user answers.

2. If $ARGUMENTS is provided, confirm:
   - "Any specific angle or constraint? Or should I go broad on '{content-area}'?"
   - Optional — proceed if user says "go" or similar.

### Output Setup

Create the output directory and brief:
- Create folder: `./content-briefs/YYYY-MM-DD-{title}/`
- {title} = kebab-case slug of the content area
- If that folder already exists, append a counter: `-2`, `-3`, etc.
- Store the full path as {output-dir}

Write `{output-dir}/00-brief.md`:
```markdown
# Content Research Brief
**Date:** [date]
**Area:** [content area]
**Angle/Context:** [any additional context, or "Broad research"]
**Mode:** [STANDARD/QUICK]

## User Profile
**Role:** [role]
**Expertise:** [domains they can speak about authentically]
**Audience:** [who reads their content]
**Channels:** [where they publish]
```

### Persona File Format

When saving a persona to `~/.agents/personas/content-creator.md`:

```markdown
---
name: [user's name]
updated: [date]
---

# Content Creator Persona

## Role
[role and title, company if shared]

## Expertise
[Domains they can speak about from real experience — bullet list, be specific]

## Audience
[Who reads their content — specific personas, not just "professionals"]

## Channels
[Where they publish — list of platforms]
```

The persona file lives outside the skill in `~/.agents/personas/` so it persists across projects. Multiple personas can coexist (e.g., `content-creator.md`, `content-creator-company-blog.md`) — ask the user which to use if multiple exist.

### Phase 0 Rules
- Phase 0 MUST complete before launching any research.
- The profile in 00-brief.md is the single source of truth for all subagents.
- Persona file is a convenience for skipping the interview — it gets copied into 00-brief.md each run, not read directly by subagents.
- Proceed immediately to execution mode selection, then Phase 1.

---

## EXECUTION MODE

Ask the user which mode to use.

**Mode inheritance:** If the user previously ran another pipeline skill in this session and already chose a mode, default to the equivalent mode. Mention it: "You used STANDARD for the previous step — I'll default to STANDARD here too. Change?"

**STANDARD** (default): Deep research with the best models.
- Phase 1: 3 subagents (Opus for trend-scanner, Sonnet for audience-researcher + content-scout)
- Phase 2: content-strategist always runs as Opus
- Best for serious content planning
- Token cost: higher

**QUICK** (faster, cheaper): Good for quick inspiration or weekly topic checks.
- Phase 1: 3 subagents, ALL Sonnet — faster and cheaper
- Phase 2: content-strategist still runs as Opus (synthesis quality matters)
- Fewer search queries per researcher (4-6 instead of 6-8)
- Best for regular cadence checks or when exploring multiple areas
- Token savings: ~40% vs Standard

Default to STANDARD if user says "go" or doesn't specify. Use QUICK if the user asks for speed or says "quick pass", "just a rough look", etc.

When asking the user to choose a mode, call `AskUserQuestion` — header `"Mode"`, question `"Pick a research mode."`, multiSelect false, options:
  - `"📚 STANDARD (Recommended)"` — `"Deep research, best models. For serious content planning."`
  - `"⚡ QUICK"` — `"All Sonnet, fewer queries. For weekly topic checks or rough exploration."`

Map the answer to `STANDARD` or `QUICK`.

---

## PHASE 1: PARALLEL RESEARCH (Autonomous — 3 background subagents)

Launch 3 background subagents simultaneously using the Agent tool with `run_in_background=true`. Each reads `00-brief.md` and writes their output file. All researchers are independent — they do NOT communicate with each other.

### Subagent Assignments

| Subagent | Model (STANDARD) | Model (QUICK) | Writes | Reference |
|----------|-------------------|---------------|--------|-----------|
| trend-scanner | Opus | Sonnet | `01-trending-topics.md` | `references/trend-scanner.md` |
| audience-researcher | Sonnet | Sonnet | `02-audience-demand.md` | `references/audience-researcher.md` |
| content-scout | Sonnet | Sonnet | `03-competitive-content.md` | `references/content-scout.md` |

Subagent type: `general-purpose` for all researchers.

### Phase 1 Rules
- All 3 subagents launch simultaneously as background agents.
- Each writes ONLY their own file.
- Wait for all 3 to complete before proceeding to Phase 2.
- Do NOT present anything to the user during Phase 1.

### Agent Failure Recovery
- After launching Phase 1, verify each subagent's expected file exists before proceeding to Phase 2.
- If a subagent fails or goes idle without writing their file: spawn a fresh replacement with the same prompt.
- Do NOT block the entire phase for one stalled agent. If 2 of 3 complete, nudge the 3rd immediately.
- Log any agent failures so the user is informed during Phase 3.

---

## PHASE 2: CONTENT STRATEGY SYNTHESIS (Autonomous — 1 subagent)

Launch 1 subagent after all Phase 1 outputs exist. Always Opus, even in QUICK mode — synthesis quality determines the value of the entire output.

Subagent type: `general-purpose`.

### Subagent Assignment

| Subagent | Model | Reads | Writes | Reference |
|----------|-------|-------|--------|-----------|
| content-strategist | Opus (always) | `00` through `03` | `04-recommendations.md` | `references/content-strategist.md` |

For the content-strategist's full scoring system, synthesis method, and output format, read `references/content-strategist.md`.

### Phase 2 Rules
- Content-strategist starts ONLY after all 3 Phase 1 files exist.
- Do NOT present to user during Phase 2.

---

## PHASE 3: PRESENTATION (Interactive)

When Phase 2 completes, read `04-recommendations.md` and present to the user:

1. **Summary line**: "[N] content opportunities in [area]. Top recommendations:"

2. **Each recommendation** (ranked by composite score):
   - Headline/topic
   - Platform + why (1 line)
   - Angle (1-2 lines)
   - Key points (bullets)
   - Why now + effort estimate
   - Authenticity / Timeliness / Differentiation scores

3. **Quick research stats**:
   - Hottest trending topic (from 01)
   - Biggest audience gap (from 02)
   - Most overdone topic to avoid (from 03)

4. **Parking lot** (briefly — topics that could work if the user has experience the research didn't detect)

Then STOP and WAIT for user response. Call `AskUserQuestion` — header `"What now"`, question `"What would you like to do?"`, multiSelect false, options (4 max — "Other" is auto-added for free text, do NOT add it manually). Build options dynamically from the top recommendations, putting the topic headline in `description`:

- `"✍️ Draft #1 (Recommended)"` — description: `"<topic-1-headline-full>"`
- `"✍️ Draft #2"` — description: `"<topic-2-headline-full>"` (skip if fewer than 2 recommendations)
- `"✍️ Draft #3"` — description: `"<topic-3-headline-full>"` (skip if fewer than 3 recommendations)
- `"✅ Done"` — `"End the session."`

If fewer than 3 recommendations, fill the remaining slot(s) with `"📋 Show more"` (`"Surface lower-ranked recommendations from the research."`) and/or `"🔄 Different area"` (`"Research a different content area or topic — you'll specify next."`). Always include `"✅ Done"`.

When the user picks `"🔄 Different area"`, ask a follow-up via free text or a second `AskUserQuestion` for the new area. When the user picks `"Other"`, interpret the free text — common intents are `"show more"`, `"different area: X"`, or asking a question about the research.

### Phase 3 Interaction

The user may:

- **Pick a topic** — Offer to draft it immediately using the channel/voice guidelines from 00-brief.md.
- **Ask for more detail** — Pull from research files and elaborate.
- **Request different angle** — Adjust the recommendation and re-score.
- **Say "more"** — Surface lower-ranked recommendations from research.
- **Say "different area"** — Start over from Phase 0 with new brief.
- **Say "done"** — End session.

---

## GLOBAL RULES

- Phase 0 is interactive. Phases 1-2 are fully autonomous. Phase 3 is interactive.
- All subagents are background agents (`run_in_background=true`), NOT team members. No TeamCreate needed.
- Each subagent writes ONLY their own file. No file conflicts.
- If a subagent fails, spawn a fresh replacement. Do not block the whole pipeline.
- The team lead (main conversation) coordinates everything and presents to the user.
- When presenting, match the language of the user's request.

### Prompt Efficiency

When spawning subagents, include ONLY the instructions relevant to their role:
- Each researcher gets: `references/content-principles.md` + their own reference file
- content-strategist gets: `references/content-principles.md` + `references/content-strategist.md`
- No subagent needs Phase 3 details or other subagents' responsibilities

### Update & Amendment Protocol

For updating existing content research rather than starting fresh, read `references/update-protocol.md`. This covers three update types (ANGLE SHIFT, NEW INFORMATION, REFRESH) and handles resuming incomplete research.
