# Output format

Three artifacts per run: a file, an index row, a chat message. The structure is fixed
so that a human and a future agent both know where to look without opening anything
they do not need.

## 1. The file

Path: `<project-root>/docs/exec-summaries/<YYYY-MM-DD>-<topic-slug>.md`

- Flat directory, date-prefixed — sorts chronologically with no tooling.
- `<topic-slug>` is 2–4 kebab-case words naming the *subject*, not the scope:
  `jarvis-completion-ping`, not `session-summary`.
- Exact filename collision → suffix `-b`, then `-c`, continuing alphabetically.
  Never overwrite.

### Frontmatter

Every file opens with this block. It exists so the file can be triaged **without being
opened** — grepping `topics:` finds every summary on a subject in one pass.

```yaml
---
date: <YYYY-MM-DD>
scope: session            # session | today | week | since:<ref>
project: <repo or directory name>
title: <plain-language title, under 70 chars>
topics: [<3-6 kebab-case tags>]
status: shipped           # shipped | partial | blocked
headline: <one sentence, the single most important outcome>
evidence: [<commit hashes, short form>]
source: live              # live | record-only
---
```

Field rules:

- `status` is the **worst** state that matters, not the best: any blocked item →
  `blocked`; any unverified or partial item → `partial`; all Done → `shipped`.
- `headline` is the sentence you would say if given five seconds. It appears in the
  index, so it must stand alone. **It may state only Done outcomes.** If nothing
  reached Done, the headline says exactly that — `INDEX.md` is designed to be read
  without opening anything, so an unverified claim placed here propagates permanently.
- `evidence` holds hashes only. Empty list is valid and honest.
- `source: record-only` marks a run with no usable live conversation context.

### Body — fixed order, always these four sections

```markdown
# <title>

## Executive summary

### <workstream 1 — plain-language name>

**Why.** <1-2 sentences, business terms>

**What.** <outcomes, not activities — Done items only asserted as fact>

**How.** <one paragraph, no jargon>

**Value.** <one of: money / time saved / risk removed / capability gained,
with the quantification rule applied>

### <workstream 2 — omit this heading entirely if the run has only one>

<same four fields>

## Status

<N> items · <M> verified done

| Item | State | Evidence |
|---|---|---|
| <plain-language item> | Done | `a1b2c3d` |
| <plain-language item> | Partial | uncommitted in working tree |
| <plain-language item> | Claimed, unverified | no artifact found |
| <plain-language item> | Blocked | <blocker> |
| <plain-language item> | Out of scope | evidence lives in <where> |

## Next steps

**I do**
1. <step> — *<horizon>*

**You do**
1. <step> — *<horizon>*

## Evidence appendix

**Window.** <resolved window, and how it was resolved>

**Commits.**
- `a1b2c3d` <subject>

**Files changed.** <from git diff --stat>

**Checks run.** <command → result>

**Gaps.** <what could not be verified and why — never omit this>
```

One workstream block per distinct thread of work, ordered by importance, capped at
four. A single-workstream run drops the `###` headings and carries the four fields
directly. Beyond four, the run is too broad — narrow the scope or split by topic.

The Executive summary keeps the A-register: no repo names, no hashes, no tool names.
Everything technical waits for the appendix.

Cap the Executive summary at 250 words for one workstream, plus 150 for each
additional. If it runs longer, the work is being described rather than summarised.

The Status table stays a single table across all workstreams — the reader wants one
place to see how much was verified.

## 2. The index row

Path: `<project-root>/docs/exec-summaries/INDEX.md`

Create with this header when absent:

```markdown
# Executive summaries

One row per summary, newest first. Read this file alone to answer "what shipped".

| Date | Scope | Title | Topics | Status | Headline | File |
|---|---|---|---|---|---|---|
```

**Insert the new row on the line immediately after the header separator** (the
`|---|` line) so the newest sits on top, and touch no other line. Anchor the edit on
that separator — it is unique in the file. Never regenerate the table: the rows below
are the accumulated record and rewriting them loses history.

```markdown
| <YYYY-MM-DD> | week | JARVIS completion pings | jarvis, discord | shipped | Silent-failure class removed from both bots. | [link](<YYYY-MM-DD>-jarvis-completion-ping.md) |
```

Keep `Headline` under 90 characters so the table stays readable in a terminal.

## 3. The chat message

Under **1800 characters** — Discord truncates at 2000 and the path must survive.

Order:

1. One-sentence summary, plain prose, standing alone. Same constraint as `headline`:
   only Done outcomes may be asserted here.
2. Blank line.
3. Why / What / How / Value — trimmed to fit.
4. The Status count line: `<N> items · <M> verified done` plus any unverified item
   named explicitly. If something is unverified, it appears in chat — it is the part
   most likely to be repeated in a meeting.
5. Next steps, condensed to the top three.
6. The file path, on its own line, as a bare path.

If the content will not fit, cut *How* first, then *Next steps* to the top one. Never
cut the unverified items — they are the reason the message is worth reading.
