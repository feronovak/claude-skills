---
name: exec-steps
description: Validates what actually got done in a work session against real evidence, then writes a board-ready executive summary — Why, What, How, Value — plus ranked next steps. Use this skill when the user types "exesteps" or "!exesteps", or asks for an executive summary of the session, a board summary, a status write-up for leadership, "what did we do and what's next", "summarise this session for the board", "wrap this up for exec", or a weekly/daily summary of shipped work. Every completion claim is verified against commits, files, and tests before it is reported as done. Do NOT use for writing a git commit message, a changelog, a session recap buffer, or a technical design doc.
version: "1.0"
authors: Fero Novak <https://feronovak.com>
---

Produce an executive summary of work done in this session — validated against evidence,
written for a board, and saved as a dated, indexed artifact.

Optional argument, taken from the text following the trigger word and possibly empty
(when invoked as a slash command it arrives here): $ARGUMENTS

Two things separate this from a status update. First, **every completion claim is
verified against something real** before it is reported as done — a conversation
saying "deployed and working" is not evidence that it deployed. Second, the output is
written for someone who does not know the codebase and will not ask a follow-up
question.

Output is **always English**, regardless of the language of the session.

---

## Step 0 — Resolve scope and location

Parse the argument into a scope. Accepted forms:

| Argument | Evidence window |
|---|---|
| *(empty)* or `session` | Since this session's first message |
| `today` | Since local midnight |
| `week` | Last 7 days |
| `since <ref>` | Since a git ref, tag, or ISO date (e.g. `since v2.1`, `since <YYYY-MM-DD>`) |

Anything unrecognised: treat as `session` and say so in one line at the top of the
chat output. Never fail on a bad argument.

**Resolve the session start** (for `session` scope) from this session's transcript:

```bash
ls -1t ~/.claude/projects/*/${CLAUDE_CODE_SESSION_ID}.jsonl 2>/dev/null | head -1
```

Take the **first timestamp that exists** in the file — the opening lines are often
metadata records with no timestamp field, so reading only line 1 is not enough:

```bash
grep -m1 -o '"timestamp":"[^"]*"' <transcript>
```

Do not read the whole transcript — it is large and you already hold the conversation
in context.

Two failure modes to handle explicitly:

- **No file, or no timestamp anywhere** → fall back to `--since="12 hours ago"` and
  record the fallback in the Evidence Appendix.
- **Timestamp older than 24 hours** → this is a resumed session, so the window now
  reaches back before today's work. Use it, but state in the Evidence Appendix that
  the window may include work from earlier sittings.

**Resolve the project root:**

```bash
git rev-parse --show-toplevel 2>/dev/null || pwd
```

If this is not a git repository, continue — but every claim that would need a commit
to prove it drops to *Claimed, unverified*, and the Evidence Appendix states that the
directory is not under version control.

---

## Step 1 — Inventory the live claims

From the conversation in context, list every distinct piece of work. For each one
capture two things:

- **The claim** — what was said to be done, in one line.
- **The why** — the problem it addresses or the reason it was undertaken.

The *why* is the part that exists nowhere except this conversation. Git will never
tell you it. Capture it now, before you start looking at evidence, or the summary
will end up describing activity instead of purpose.

If the conversation contains no relevant work (a cold session, or `week` scope over
sessions that are gone), mark the run `source: record-only` and **build the item list
in Step 2 instead** — one item per commit or session-note entry in the window,
grouped where several commits serve one purpose.

In record-only mode two rules bind. Items can reach no higher than Done-by-commit,
since there is no conversation asserting anything further. And *Why* is written only
from what the evidence itself states — a commit subject, a session note, a linked
ticket. Do not infer intent to fill the gap: record-only output has thinner *Why*
sections and should look that way.

---

## Step 2 — Gather evidence

Keep output small; you need facts, not dumps.

**First resolve the base**, because `git diff` has no `--since` and `git log --since`
does not accept a ref. The two scope families need different commands:

```bash
# Time scopes (session / today / week)
base=$(git rev-list -1 --before="<window-start>" HEAD)   # empty => use root commit
git log --since="<window-start>" --pretty=format:'%h|%an|%ad|%s' --date=short
git diff --stat "$base"..HEAD

# Ref scope (since <ref>)
git log <ref>..HEAD --pretty=format:'%h|%an|%ad|%s' --date=short
git diff --stat <ref>..HEAD
```

For `since <x>`, disambiguate ref from date by trying `git rev-parse --verify <x>`
first; if that fails, treat `<x>` as a date and use the time-scope commands.

Then:

```bash
git status --short     # uncommitted work is NOT done
```

Working-tree dirt only counts as evidence when it plausibly relates to an inventoried
claim — on `today` and `week` scopes it is often unrelated leftovers.

**Filter by authorship.** `git log` returns everything in the window, including
teammates' commits and merged upstream work. Commits not attributable to this
session's work are listed in the appendix as *in window, not ours* and never enter the
summary. Reporting someone else's commit as your output is overstatement by absorption.

Then, as applicable:

- **Session notes** — `session-notes/YYYY-MM.md` in the project, entries inside the window.
- **Named tickets** — any Trello card or TODO item referenced in the conversation.
- **Existence checks** — for each claimed file, `test -f`. A path that does not exist
  is decisive.
- **Health checks** — only where the conversation claims a service is live or a test
  passes, and only if the check is cheap and read-only. A claimed passing test that
  can be run in seconds **must** be re-run, or the claim stays below Done. Test output
  pasted earlier in the conversation is not a substitute: it may be stale, since later
  edits can break what passed an hour ago.

Do not run destructive commands, deploys, or anything that changes state. This skill
reports; it does not act.

---

## Step 3 — Validate

Read `references/validation-rubric.md` and assign every item from Step 1 exactly one
of four states.

| State | Requirement |
|---|---|
| **Done** | A named artifact proves it — commit hash, existing file path, responding service, or test output. |
| **Partial** | Started; evidence incomplete, or the change is uncommitted. |
| **Claimed, unverified** | The conversation asserts completion; no artifact was found. |
| **Blocked** | Not done, with the blocker named. |

**A state is never upgraded to make the summary read better.** If the honest answer is
that three of five items are unverified, the summary says three of five are unverified.
That specific discipline is the entire reason this skill exists: an unverified claim
repeated to a board is the one that gets challenged and cannot be backed.

---

## Step 4 — Translate to board register

Read `references/board-register.md` before writing a word of the summary. It carries
the Why / What / How / Value rules, the value-quantification rule, and the banned
vocabulary list.

**The narrative is bound to the validation states.** The Executive Summary may assert
as fact only what reached **Done**. Partial items appear explicitly as in progress.
Claimed-unverified and Blocked items never appear as achieved outcomes anywhere in the
Executive Summary. Without this binding the Status table can say "unverified" while
the prose above it says "failures are now visible" — and the board reads the prose.

**One Why/What/How/Value block per workstream.** A `week` scope usually spans several
unrelated threads of work; collapsing them into one narrative produces a muddle that
serves no reader. Group by workstream, order by importance, and cap at four — beyond
that, the run is too broad and should be split by scope or by topic.

The four sections, in order:

- **Why** — the problem or opportunity, in business terms. One or two sentences.
- **What** — what now exists that did not before. Outcomes, not activities.
- **How** — the approach, one paragraph, no jargon.
- **Value** — exactly one of: money, time saved, risk removed, capability gained.
  If it is not measurable, write `Unquantified` and name the measurement that would
  close the gap. **Never invent a figure.**

Then **Next steps** — each with an owner and a horizon (now / this week / this month),
ordered by what should happen first. Split into *"I do"* and *"you do"*.

---

## Step 5 — Emit

Read `references/output-format.md` for the exact file template and index row format.

Three outputs, in this order:

1. **Write the file** — `docs/exec-summaries/YYYY-MM-DD-<topic-slug>.md` under the
   project root. Create the directory if absent. If that exact filename exists,
   suffix `-b`, then `-c`. Never overwrite.
2. **Update the index** — append one row to `docs/exec-summaries/INDEX.md`, newest
   first. Create the file with its header if absent. Append only — never regenerate
   the table, or history is lost.
3. **Print to chat** — the executive summary, under 1800 characters so it survives
   Discord's message limit, ending with the file path.

---

## Hard rules

- **No invented numbers, and no magnitude claims either.** No number, ratio,
  multiplier, or comparative magnitude — "halved", "roughly", "~", "order of
  magnitude", "significantly faster", "several hours a week" — appears in the
  Executive Summary unless it was actually measured in evidence. A figure the user
  stated carries its source inline: *(owner's estimate, unmeasured)*. Counts of
  commits or files changed are activity, never Value. Absent a measurement, the word
  is `Unquantified`.
- **Evidence before assertion.** "Done" requires an artifact you actually looked at.
- **No repo names, hashes, or tool names in the Executive Summary.** They belong in
  the Evidence Appendix. A board reader should not meet the word `systemd`.
- **Read-only.** Never deploy, never commit the summary automatically, never modify
  project code.
- **Never write into an operational doc.** These are dated artifacts and stay inside
  `docs/exec-summaries/`.
- **Report the gaps.** If evidence was unavailable — no git, missing session notes, a
  check you could not run — say so in the Evidence Appendix. A summary that hides its
  own blind spots is worse than no summary.
