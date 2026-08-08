# exec-steps — design

**Date:** 2026-07-25
**Status:** approved, implemented
**Author:** Fero Novak

## Problem

At the end of a working session there is no reliable answer to two questions: what
actually got done, and what happens next. The conversation holds intent but
overstates completion — "deployed and working" is said before the artifact exists.
Git holds artifacts but no intent. Neither is readable by a board.

Three failure modes this addresses:

1. **Unverified claims propagate.** Work described as finished in a session gets
   repeated to stakeholders without anyone checking a commit exists. The claim is
   challenged in a room and cannot be backed.
2. **Technical output is unreadable upward.** "Added a systemd timer" carries no
   decision value for a non-technical reader.
3. **No accumulating record.** Answering "what shipped in Q3" means re-reading
   sessions that no longer exist.

## Solution

A Claude Code skill, `exec-steps`, that reads the live conversation as the spine,
verifies every completion claim against repository evidence, and emits a board-ready
Why / What / How / Value summary plus a dated, indexed markdown artifact.

The verification step is the point. Without it this is a formatting exercise.

## Scope

`$ARGUMENTS` carries an optional scope:

| Argument | Evidence window |
|---|---|
| *(none)* / `session` | Since the current session's first message |
| `today` | Since local midnight |
| `week` | Last 7 days |
| `since <ref>` | Since a git ref, tag, or ISO date |

Single project only — always the current working directory's repository. Cross-project
runs are explicitly out of scope: separate repos and separate session notes stop the
evidence from forming one coherent story.

Cold sessions (no relevant live context) are supported and degrade to record-only,
which is declared in the output rather than hidden.

## Pipeline

1. **Resolve scope** — window start, git root, whether live context applies.
2. **Live context inventory** — every completion claim and every stated intent from
   the conversation. Intent exists nowhere else and is the only source for *Why*.
3. **Evidence gathering** — `git log`, `git diff --stat`, `git status`, session notes
   in window, named TODO/Trello items.
4. **Validation** — each claim assigned one of four states against an evidence
   standard. States never upgrade for presentational reasons.
5. **Board translation** — Why / What / How / Value per workstream.
6. **Emit** — chat summary (under Discord's limit) + file + index row.

## Validation states

| State | Requirement |
|---|---|
| **Done** | A named artifact proves it: commit hash, existing file path, responding service, or test output. |
| **Partial** | Started; evidence incomplete or uncommitted. |
| **Claimed, unverified** | Conversation asserts completion; no artifact found. Stated as such. |
| **Blocked** | Not done, with the blocker named. |

## Output

**Register:** dual. Executive summary in non-technical language; evidence appendix
retains repo names, hashes, and paths. Always English regardless of session language.

**Value rule:** exactly one of money, time, risk removed, or capability gained. When
not measurable, the output reads `Unquantified` and names what measurement would
close the gap. Inventing a figure is prohibited — a fabricated metric in a board pack
is worse than an acknowledged gap.

**File:** `docs/exec-summaries/YYYY-MM-DD-<topic-slug>.md`, flat, date-prefixed.
YAML frontmatter (`date`, `scope`, `project`, `title`, `topics`, `status`, `headline`,
`evidence`, `source`) makes each file triageable without opening it.

**Index:** `docs/exec-summaries/INDEX.md`, one table, newest first, one row appended
per run. Reading the index alone answers "what shipped this quarter".

**Body order is fixed:** Executive Summary → Status → Next Steps → Evidence Appendix.
A fixed order means both a human and a future agent know where to look.

## Non-goals

Cross-project runs. Charts. Invented metrics. Any write into an operational doc —
these are dated artifacts confined to their own directory.

## Delivery

Phase A (this spec): skill only, at `~/projects/claude-skills/exec-steps/`, symlinked
into `~/.claude/skills/`.

Phase B (on approval of A): thin `!exesteps [scope]` front door in JARVIS `index.ts`
that rewrites to a skill invocation, plus a `!help` line. The skill stays the single
source of logic.
