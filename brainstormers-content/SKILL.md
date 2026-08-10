---
name: brainstormers-content
description: "Content research and recommendation team. Finds hot topics, analyzes audience demand and competitive landscape, scores for authenticity/timeliness/differentiation, recommends content with platform assignments. Use when the user wants content ideas, topic research, content strategy for LinkedIn/blog/newsletter, or trending topics. Triggers on 'what should I write about', 'content brainstorm', 'find me content ideas', 'what's trending in X'. Do NOT trigger for: copy-editing drafts (use humanizer), single-topic article writing, or generic brainstorming without research need."
version: "3.0"
authors: Fero Novak <https://feronovak.com>
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

The skill needs to know WHO is publishing. Authenticity scoring, platform
assignment and the voice of every angle all hang off it. A profile resolved to
the wrong person produces a content plan that is confident, specific, and about
somebody else.

**Resolve exactly one identity. Never merge two.**

Search in this order, and report every path you checked:

1. **Project-local** — `./CLAUDE.md`, `./AGENTS.md`, `./.claude/`, or a persona file the project names. Scoped to the project root; do not walk up the tree.
2. **Persona file** — `./content-persona.md`, then `~/.agents/personas/content-creator.md`. Where several exist, ask which one is publishing. If one is found: "I found your saved profile. Should I use it, or do you want to update anything?"
3. **Global config** — `~/.claude/CLAUDE.md` or the runtime's equivalent. **Never use this silently.** A global config describes whoever owns the machine, who is frequently not the person this project publishes as. Name the identity you found there and ask whether they are the author before using a line of it.
4. **Interview** — no profile found, so ask (4 questions via AskUserQuestion):
   - **Role:** "What's your role?" (e.g., "CTO at a fintech startup", "MD of a media company")
   - **Expertise domains:** "What topics can you speak about from real experience?" (e.g., "product management, AI in media, scaling teams, CEE market"). Push for specifics — "marketing" is too broad, "B2B SaaS content marketing for dev tools" is useful.
   - **Audience:** "Who reads your content?" (e.g., "other startup founders, mostly technical", "CEE media industry professionals")
   - **Channels:** "Where do you publish?" with options: LinkedIn, Blog/website, Newsletter, X/Twitter, Internal comms, Other
5. **Save for next time** — after an interview, ask: "Want me to save this profile so you don't have to answer these questions next time?" If yes, write it to `~/.agents/personas/content-creator.md` using the persona format below.

**The identity guard.** Where two sources name different people — a project
profile and a global config, two persona files, a profile that disagrees with
what the user just said — **stop and ask which one is publishing.** Do not merge
them. Do not prefer the more detailed one. Blending two identities attributes
one person's experience to another, and every Authenticity score downstream
inherits that error without showing it.

State the resolved identity by name in `00-brief.md` and again when presenting
in Phase 3, so the wrong person is visible in the first line rather than buried
in the recommendations.

Where the guard fires, **write no brief and launch no research.** A brief whose
identity is unresolved has nothing to put in the field every subagent reads
first. Ask the question, wait, then start Phase 0 again from the top.

### Voice Source

The profile says what the user has **done**. It says nothing about how they
**write** — yet the strategist is asked to produce angles in their voice and to
run a voice check before finalizing. With no voice source, that check can only
strip generic badness. It can never confirm a match, and an output that implies
otherwise is asserting something nobody verified.

Resolve one, in this order:

1. **A voice skill.** Where a skill available in this session governs how this specific person writes — a personal voice, persona, or brand-voice skill — **that skill owns voice for this run.** Name it in the brief. Do not restate or second-guess its rules; it is the authority and this skill defers to it.
2. **Writing samples.** 3-5 existing posts, a bio document, a past draft, an interview transcript. Ask for a path or a paste, and record where they came from.
3. **Neither.** Ask once. If the user has nothing to point at, proceed — and carry `VOICE: UNGROUNDED` through to the output.

Where `humanizer` is available, it owns the de-AI pass on any copy drafted in
Phase 3. It is not a substitute for a voice source: it removes what reads as
machine-written, which is a different thing from sounding like a named person.

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
**Publishing as:** [name — the one identity resolved in Profile Discovery]
**Resolved from:** [which source, and every path checked]
**Role:** [role]
**Expertise:** [domains they can speak about authentically]
**Audience:** [who reads their content]
**Channels:** [where they publish]
**Voice source:** [skill name / samples at <path> / UNGROUNDED]
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
- **One identity, never merged.** Two sources naming different people is a question for the user, not a conflict to resolve silently.
- **The voice source is resolved before Phase 1, not improvised in Phase 3.** `UNGROUNDED` is a valid answer; a fabricated match is not.
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

1. **Header line**: "Publishing as [name] · voice: [source, or UNGROUNDED]". This
   goes first, before the count. A plan built for the wrong person, or written
   in a voice nobody verified, should be visible in the first line the user
   reads — not discovered three recommendations in.

2. **Summary line**: "[N] content opportunities in [area]. Top recommendations:"

3. **Each recommendation** (ranked by composite score):
   - Headline/topic
   - Platform + why (1 line)
   - Angle (1-2 lines)
   - Key points (bullets)
   - Why now + effort estimate
   - Authenticity / Timeliness / Differentiation scores, and the quoted profile line the Authenticity score rests on

4. **Quick research stats**:
   - Hottest trending topic (from 01)
   - Biggest audience gap (from 02)
   - Most overdone topic to avoid (from 03)

5. **Parking lot** — every topic capped as INFERRED, each with its inference as a one-line question. These are the topics the user can unlock by confirming an experience the profile never recorded, and they are worth more of the user's attention than the stats above.

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
