# next-steps Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a skill that cuts an existing backlog into the next release using MoSCoW, then emits the build order for what it scoped.

**Architecture:** A markdown-only skill in the established `claude-skills` shape — `SKILL.md` holds the round and the guardrails, two `references/` files hold the decision rules that would otherwise bloat the always-loaded body, and `evals/` holds four fixture backlogs each discriminating against a specific failure mode. No code ships, so correctness is established by running the skill against the fixtures and comparing against declared expectations rather than by a unit suite.

**Tech Stack:** Markdown only. No Python, no third-party dependencies, no build step. Installation is `setup.sh`, which symlinks each directory containing a `SKILL.md` into `~/.claude/skills/`.

## Global Constraints

- Repo: `~/projects/claude-skills`, branch `feat/next-steps-skill` (already created, based on `fix/skill-validation-tdd`).
- One directory per skill; the directory name is the skill name — so the directory MUST be exactly `next-steps/`.
- `SKILL.md` carries YAML frontmatter with `name`, `description`, `version: "1.0"`, `authors: Fero Novak <https://feronovak.com>`.
- The `description` is written to trigger on what a user would actually say, and MUST carry a `Do NOT use for` clause naming the neighbouring skills.
- Long reference material goes in `references/`, never in `SKILL.md` — the body loads on every trigger, references only when read.
- Skills that ship code keep it under `<skill>/tool/`. **This skill ships no code**; do not create `tool/`.
- No AI assistant is recorded as a contributor: no `Co-Authored-By` trailer, no session reference, no generation notice. A commit-msg hook enforces this and will reject the commit.
- MoSCoW is scoped to **the next release**, never a calendar window. The words "two weeks", "this quarter", "sprint" must not appear as the scope boundary in any deliverable.
- The three standing markers are exactly `🟥` (near-term), `🟧` (scheduled), `⬜` (backlog). No fourth marker may be introduced.
- Inline comments are present tense. No dated narrative anywhere in a written-back backlog row — the global `doc-state-guard.py` hook warns on it.

---

## File Structure

| File | Responsibility |
|---|---|
| `next-steps/SKILL.md` | The six-step round, the guardrails, the handoffs. Always loaded. |
| `next-steps/references/moscow.md` | Letter definitions against the release boundary, marker mapping, Won't's two flavours, already-done, the 60% guard, the Could/Won't collapse. Read at step 1. |
| `next-steps/references/release-plan.md` | The three readiness states, the ordering rules, the `needs spec` judgment, the output format. Read at step 3. |
| `next-steps/README.md` | What it is, why it exists, where it sits in the chain. Not loaded by the skill. |
| `next-steps/evals/evals.json` | Four evals, each naming the failure mode it discriminates against. |
| `next-steps/evals/fixtures/*/` | Four fixture repos. Plain directories, not git clones — the skill must not require git. |
| `exec-steps/SKILL.md` | Modified: description narrowed so it stops competing for this skill's prompts. |

Task order puts the fixtures and their expectations before the skill body, so the skill is written against declared behaviour rather than the fixtures being fitted to whatever got written.

---

### Task 1: Fix the exec-steps triggering collision

Independent of everything else and reviewable on its own. Do it first so the collision never exists in the tree alongside the new skill.

**Files:**
- Modify: `exec-steps/SKILL.md:3` (the `description` line in the frontmatter)

**Interfaces:**
- Consumes: nothing
- Produces: nothing consumed by later tasks. This is a standalone triggering fix.

- [ ] **Step 1: Read the current description to confirm the exact string**

Run: `sed -n '3p' exec-steps/SKILL.md`

Expected: a single long `description:` line containing both the phrase `"what did we do and what's next"` and the clause `Do NOT use for writing a git commit message, a changelog, a session recap buffer, or a technical design doc.`

If either substring is absent, STOP — the file has changed since this plan was written; report it rather than guessing at a replacement.

- [ ] **Step 2: Replace the description line**

Replace line 3 of `exec-steps/SKILL.md` in full with:

```
description: Validates what actually got done in a work session against real evidence, then writes a board-ready executive summary — Why, What, How, Value — plus ranked next steps. Use this skill when the user types "exesteps" or "!exesteps", or asks for an executive summary of the session, a board summary, a status write-up for leadership, "what did we get done", "summarise this session for the board", "wrap this up for exec", or a weekly/daily summary of shipped work. Every completion claim is verified against commits, files, and tests before it is reported as done. Do NOT use for writing a git commit message, a changelog, a session recap buffer, a technical design doc, or for prioritising a backlog and scoping the next release (next-steps).
```

Two changes, and only two: `"what did we do and what's next"` becomes `"what did we get done"`, and the exclusion list gains `, or for prioritising a backlog and scoping the next release (next-steps)`.

- [ ] **Step 3: Verify the forward-looking trigger is gone and the exclusion landed**

Run: `grep -c "what's next" exec-steps/SKILL.md`
Expected: `0`

Run: `grep -c "next-steps" exec-steps/SKILL.md`
Expected: `1`

Run: `sed -n '1,6p' exec-steps/SKILL.md`
Expected: frontmatter still opens with `---`, still carries `name: exec-steps`, `version: "1.0"`, `authors:`, and closes with `---`. Only line 3 changed.

- [ ] **Step 4: Commit**

```bash
git add exec-steps/SKILL.md
git commit -m "fix(exec-steps): stop competing for backlog-prioritisation prompts

The description claimed \"what did we do and what's next\", which reaches
for work that belongs to next-steps. Narrowed to the retrospective half
and added next-steps to the exclusion list. No behaviour change."
```

---

### Task 2: Fixtures and declared expectations

The tests come before the skill. Each fixture exists to discriminate against one specific failure mode; a fixture every implementation passes teaches nothing.

**Files:**
- Create: `next-steps/evals/fixtures/versioned-product/package.json`
- Create: `next-steps/evals/fixtures/versioned-product/docs/NEXT_STEPS.md`
- Create: `next-steps/evals/fixtures/unversioned-docs/docs/NEXT_STEPS.md`
- Create: `next-steps/evals/fixtures/two-backlogs/docs/NEXT_STEPS.md`
- Create: `next-steps/evals/fixtures/two-backlogs/ROADMAP.md`
- Create: `next-steps/evals/fixtures/no-estimates/docs/NEXT_STEPS.md`
- Create: `next-steps/evals/evals.json`

**Interfaces:**
- Consumes: nothing
- Produces: four fixture paths under `next-steps/evals/fixtures/`, referenced by name (`versioned-product`, `unversioned-docs`, `two-backlogs`, `no-estimates`) in `evals.json` and in Task 6's verification steps.

- [ ] **Step 1: Create the versioned-product fixture**

Create `next-steps/evals/fixtures/versioned-product/package.json`:

```json
{
  "name": "fixture-versioned-product",
  "version": "1.4.0",
  "private": true
}
```

Create `next-steps/evals/fixtures/versioned-product/docs/NEXT_STEPS.md`:

```markdown
# Fixture Product — Next Steps

Future work only. Completed work lives in git history.

**Last reviewed:** 2026-07-30.

Priority: 🟥 near-term · 🟧 scheduled · ⬜ backlog / until-trigger

---

## Auth

- 🟥 **Session expiry on the magic-link flow** (~2 hr). Links currently never
  expire once issued.
- 🟧 **Rate-limit the login endpoint** (~1 hr). Depends on session expiry
  landing first.
- ⬜ **Passkey support** (~8 hr). No user has asked; the magic link works.

## Billing

- 🟧 **Invoice PDF generation** (~6 hr). Customers ask for it monthly.
- ⬜ **Proration on plan change** (~4 hr).

## Platform

- 🟧 **Move image processing off the request path** (~5 hr). Uploads over 4 MB
  time out.
- ⬜ **Multi-region read replicas** (~20 hr).
- ⬜ **Replace the CSV exporter** (~3 hr).
```

Eight items, estimates on every row, one real dependency (rate-limit → session expiry), total 49 hours. This is the fixture where the 60% guard can actually compute.

- [ ] **Step 2: Create the unversioned-docs fixture**

Create `next-steps/evals/fixtures/unversioned-docs/docs/NEXT_STEPS.md`:

```markdown
# Fixture Docs Repo — Next Steps

**Last reviewed:** 2026-07-30.

Priority: 🟥 near-term · 🟧 scheduled · ⬜ backlog / until-trigger

---

## Infrastructure

- 🟥 **Off-site backup** (~1 hr). Single disk, no copy leaves the building.
- 🟧 **Rotate the exposed API credentials** (~30 min).
- ⬜ **Log rotation on the bot container** (~15 min).
```

No manifest anywhere in this fixture — no `package.json`, no `pyproject.toml`, no `Cargo.toml`. This is what makes it unversioned, and the skill must notice and say the cut-off is soft rather than inventing a version.

- [ ] **Step 3: Create the two-backlogs fixture**

Create `next-steps/evals/fixtures/two-backlogs/docs/NEXT_STEPS.md`:

```markdown
# Fixture — Next Steps

**Last reviewed:** 2026-07-30.

- 🟥 **Ship the onboarding email** (~2 hr).
- ⬜ **Dark mode** (~6 hr).
```

Create `next-steps/evals/fixtures/two-backlogs/ROADMAP.md`:

```markdown
# Fixture — Roadmap

- Ship the onboarding email
- Dark mode
- Rewrite the settings page
```

Two files both answering "what is open". The skill must refuse to write and say which two it found.

- [ ] **Step 4: Create the no-estimates fixture**

Create `next-steps/evals/fixtures/no-estimates/docs/NEXT_STEPS.md`:

```markdown
# Fixture — Next Steps

**Last reviewed:** 2026-07-30.

Priority: 🟥 near-term · 🟧 scheduled · ⬜ backlog / until-trigger

---

## Editor

- 🟥 **Autosave drafts**. Users lose work on refresh.
- 🟧 **Markdown paste handling**.
- 🟧 **Inline image upload**.
- ⬜ **Collaborative cursors**.
- ⬜ **Version history**.
```

Not one hour figure on any row. The 60% guard cannot be computed here and the skill must say so rather than producing a number.

- [ ] **Step 5: Write the eval declarations**

Create `next-steps/evals/evals.json`:

```json
{
  "skill_name": "next-steps",
  "notes": "This skill ships no code, so there is no unit suite. Each fixture is a plain directory, not a git clone, because the skill must work without git. Every eval names the failure mode it discriminates against — an eval that every run passes teaches nothing.",
  "evals": [
    {
      "id": 1,
      "name": "release-boundary-is-a-version",
      "prompt": "nextsteps",
      "fixture": "versioned-product",
      "expected_output": "Names the next release as a version bump from 1.4.0, proposes a MoSCoW letter for all eight items, and reports that the Musts exceed roughly 60% of the 49-hour total if they do.",
      "failure_mode": "Scoping to a calendar window ('the next two weeks') instead of a release. The package.json declares 1.4.0; a run that never mentions a version has ignored the one signal that makes MoSCoW meaningful here.",
      "expectations": [
        "Reads package.json and names the release as a bump from 1.4.0",
        "Assigns a letter to all eight items, none left blank",
        "Gives a reason on every item whose proposed letter differs from its standing marker",
        "Notices that rate-limit the login endpoint depends on session expiry and orders them accordingly",
        "Computes the 60% guard against the 49-hour total rather than asserting it without arithmetic"
      ]
    },
    {
      "id": 2,
      "name": "soft-cutoff-is-declared",
      "prompt": "nextsteps",
      "fixture": "unversioned-docs",
      "expected_output": "States that the repo carries no version, that 'the next release' therefore means the next block of work, and that the cut-off is soft.",
      "failure_mode": "Silently proceeding as though a hard release boundary exists, which overstates how much discipline the round carries. Inventing a version number is the same failure in a louder form.",
      "expectations": [
        "Says explicitly that no version was found",
        "Declares the cut-off soft rather than implying a firm boundary",
        "Still completes the round — a soft boundary is a caveat, not a refusal"
      ]
    },
    {
      "id": 3,
      "name": "refuses-two-backlogs",
      "prompt": "nextsteps",
      "fixture": "two-backlogs",
      "expected_output": "Refuses to write, naming both docs/NEXT_STEPS.md and ROADMAP.md.",
      "failure_mode": "Picking docs/NEXT_STEPS.md because it is first in the search order and writing to it. That silently ratifies a second backlog, the exact condition project-standard check 26 exists to prevent.",
      "expectations": [
        "Refuses to write to either file",
        "Names both files it found",
        "Does not triage the items anyway and offer to write later — the refusal comes before the round, not after"
      ]
    },
    {
      "id": 4,
      "name": "declines-the-uncomputable-guard",
      "prompt": "nextsteps",
      "fixture": "no-estimates",
      "expected_output": "Runs the round and states that the 60% guard cannot be checked because no item carries an effort estimate.",
      "failure_mode": "Producing a percentage anyway from invented effort figures. A fabricated number here is worse than no number, because it looks like the guard ran.",
      "expectations": [
        "Assigns a letter to all five items",
        "States that no effort estimates are present",
        "Produces no percentage and no invented hour figures"
      ]
    }
  ]
}
```

- [ ] **Step 6: Verify the fixtures are well-formed and the evals parse**

Run: `python3 -c "import json,pathlib; d=json.loads(pathlib.Path('next-steps/evals/evals.json').read_text()); print(len(d['evals']), 'evals'); [print(e['id'], e['name'], e['fixture']) for e in d['evals']]"`

Expected:
```
4 evals
1 release-boundary-is-a-version versioned-product
2 soft-cutoff-is-declared unversioned-docs
3 refuses-two-backlogs two-backlogs
4 declines-the-uncomputable-guard no-estimates
```

Run: `for f in versioned-product unversioned-docs two-backlogs no-estimates; do test -d "next-steps/evals/fixtures/$f" && echo "ok $f" || echo "MISSING $f"; done`

Expected: four `ok` lines.

Run: `test -f next-steps/evals/fixtures/versioned-product/package.json && echo "versioned has manifest"; test -f next-steps/evals/fixtures/unversioned-docs/package.json && echo "BUG: unversioned has a manifest" || echo "ok unversioned has none"`

Expected:
```
versioned has manifest
ok unversioned has none
```

- [ ] **Step 7: Commit**

```bash
git add next-steps/evals
git commit -m "test(next-steps): four fixtures, each discriminating one failure mode

Versioned product exercises the release boundary and the 60% guard.
Unversioned docs must declare its cut-off soft. Two backlogs must be
refused before the round, not after. No-estimates must decline the
guard rather than invent a percentage.

Fixtures are plain directories, not clones - the skill must not
require git."
```

---

### Task 3: The MoSCoW reference

The decision rules, kept out of `SKILL.md` because they are read once per round rather than on every trigger.

**Files:**
- Create: `next-steps/references/moscow.md`

**Interfaces:**
- Consumes: nothing
- Produces: the file `references/moscow.md`, which `SKILL.md` step 1 instructs the model to read. Section headings referenced by name from `SKILL.md`: `## The four letters`, `## Writing the verdict back`, `## The 60% guard`.

- [ ] **Step 1: Write the reference**

Create `next-steps/references/moscow.md`:

```markdown
# MoSCoW, scoped to a release

## Why the boundary matters

MoSCoW is a commitment scale measured against a fixed scope boundary. Without
one, every item drifts to Must and the letters stop carrying information. The
boundary is **the next release** — never a calendar window. "Two weeks" is not
a release; it is a guess about how long one takes.

**Versioned repo** — the boundary is the next version bump. Read it from the
manifest (`package.json`, `pyproject.toml`, `Cargo.toml`, a `VERSION` file).

**Unversioned repo** — there is no bump to point at, so the boundary is "the
next block of work". Say this out loud in the round. A soft cut-off is still
usable, but the user must not be left thinking the round carries discipline it
does not.

## The four letters

| Letter | Means |
|---|---|
| **Must** | The release does not ship without it. |
| **Should** | Goes in if it fits. Its absence is a disappointment, not a failure. |
| **Could** | Only if everything above lands with room to spare. |
| **Won't** | Explicitly out. Two flavours — see below. |

**Won't has two flavours and they are not interchangeable:**

- **Won't — this release.** Still wanted, just not now. Stays in the backlog.
- **Won't — ever.** Dead. The row is deleted.

Never collapse the second into the first to avoid a deletion. An item nobody
will ever do, left in the backlog, costs a re-read every future round.

## Writing the verdict back

| Verdict | Effect on the backlog |
|---|---|
| Must | `🟥` |
| Should | `🟧` |
| Could | `⬜` |
| Won't — this release | `⬜` — demote it if it currently reads `🟥` or `🟧` |
| Won't — ever | row **deleted**, one explicit confirmation for that row |
| Already done | row **deleted**, one explicit confirmation for that row |

The letters themselves do not persist. They are the round's verdict; their only
effect is to move the standing marker. One scale survives in the file, so there
is no second column to maintain and nothing that can disagree with itself.

**Could and Won't-this-release both land on `⬜`.** Three markers cannot carry
four letters. The collapse is accepted, not solved — the standing scale is
deliberately coarser than the round's verdict. Where the difference matters,
the inline comment carries it:

    *Could: if the release has room after the ACL lands.*

Do not invent a fourth marker. That would add a symbol to every backlog in the
fleet to record a state that lasts one round.

**A row reported as already shipped is deleted, not marked done.** A roadmap
holds future work only; completed items leave rather than moving to a
done-section.

## The 60% guard

Where the backlog carries effort estimates (`~1 hr`, `2–3 hr`), sum them. If
the Musts exceed **roughly 60% of the release's total estimated effort**, say
so and ask what drops.

This is the only mechanical defence against everything becoming Must, and it is
the reason to read the estimates rather than skim past them.

**Where estimates are absent, say the guard cannot be checked.** Do not
estimate the items yourself to make the arithmetic possible. A percentage
derived from invented figures looks exactly like a percentage derived from real
ones, and that is the failure this instruction exists to prevent.

## Comments

Comments land inline under the row they belong to, in the present tense:

    - 🟧 **OpenClaw as non-root** (2–3 hr). Turns the allowlist from a
      speed-bump into a real boundary.
      *Held: not before the off-site backup lands.*

Never a dated narrative. "Held, and why" is current state. "Deprioritised on
2026-08-08" is changelog, belongs in a history file, and will trip the
`doc-state-guard.py` hook.
```

- [ ] **Step 2: Verify the anchors SKILL.md will reference exist, and no calendar language leaked in**

Run: `grep -n '^## ' next-steps/references/moscow.md`

Expected to include, among others:
```
## The four letters
## Writing the verdict back
## The 60% guard
```

Run: `grep -niE 'two.week|this quarter|sprint|fortnight' next-steps/references/moscow.md | grep -v 'not a release' | grep -v 'is not a release'`

Expected: no output other than the line that explicitly rejects "two weeks" as a boundary. Any other hit means calendar framing leaked into the rules.

- [ ] **Step 3: Commit**

```bash
git add next-steps/references/moscow.md
git commit -m "feat(next-steps): MoSCoW rules scoped to a release

Four letters against a release boundary, the marker mapping, Won't's
two flavours, and the 60% guard - including the instruction to decline
the guard rather than invent estimates to satisfy it."
```

---

### Task 4: The release-plan reference

**Files:**
- Create: `next-steps/references/release-plan.md`

**Interfaces:**
- Consumes: the marker vocabulary defined in `references/moscow.md` (`🟥` `🟧` `⬜`)
- Produces: the file `references/release-plan.md`, read by `SKILL.md` step 3. Defines the three readiness states `ready`, `blocked by <n>`, `needs spec`, used verbatim in the step 3 output table.

- [ ] **Step 1: Write the reference**

Create `next-steps/references/release-plan.md`:

```markdown
# The release plan

Produced at step 3, for the **Musts and Shoulds only**. Coulds are not ordered
— by definition nothing depends on them.

## The three readiness states

| State | Means |
|---|---|
| `ready` | Can start now. Nothing blocks it and nothing needs designing first. |
| `blocked by <n>` | Depends on another item **in this release**, named by its row number. |
| `needs spec` | Non-trivial, and no `docs/prds/<name>.md` exists for it. |

An item blocked by something **outside** this release is not `blocked by` — it
is a Must that cannot ship, which means either the blocker belongs in the
release or this item does not. Say so rather than recording an unsatisfiable
dependency.

## Output format

```
Release 1.5.0 — build order

1. Session expiry on the magic-link flow    ready
2. Rate-limit the login endpoint            blocked by 1
3. Move image processing off request path   needs spec
4. Invoice PDF generation                   ready · parallel with 1

Gaps: 1 Must has no PRD (item 3).
```

Order is dependency order, not importance order — importance was already
settled by the letter. Where two items are independent, say so with
`· parallel with <n>`; a reader who does not know they can be done at once will
serialise them for no reason.

## The `needs spec` judgment

This is the weakest call in the skill, and it must behave like it knows that.

An item needs a spec when it is non-trivial **and** has no PRD. "Non-trivial"
means the work has open design questions — not merely that it is large. A
20-hour migration with one obvious path needs no spec; a 3-hour change to how
pricing is calculated does.

Three rules:

1. **State the reason.** Never just `needs spec` — say what is undecided.
2. **It is overruled in the same free-text pass as everything else.** The user
   saying "3 is fine, just build it" ends the matter without argument.
3. **Never hand off without agreement.** `brainstorming` is offered, never
   invoked on the user's behalf. Routing work to a design session the user did
   not ask for is the failure mode this rule prevents.

## What this is not

This is not an implementation plan. It says *which items, in what order, and
which cannot start yet*. How to build any one of them is `writing-plans`, at a
different altitude, invoked separately and per item.
```

- [ ] **Step 2: Verify the readiness vocabulary matches what SKILL.md will emit**

Run: `grep -c 'needs spec' next-steps/references/release-plan.md`
Expected: a count of `4` or greater (table row, output example, section heading, and the rules).

Run: `grep -n 'blocked by' next-steps/references/release-plan.md | head -3`
Expected: at least the table row and the worked example, both using the exact lowercase form `blocked by`.

- [ ] **Step 3: Commit**

```bash
git add next-steps/references/release-plan.md
git commit -m "feat(next-steps): release build-order rules

Three readiness states, dependency ordering rather than importance
ordering, and the needs-spec judgment with its three guards - state the
reason, overrulable in free text, never hand off without agreement."
```

---

### Task 5: The skill body

**Files:**
- Create: `next-steps/SKILL.md`

**Interfaces:**
- Consumes: `references/moscow.md` (read at step 1), `references/release-plan.md` (read at step 3), and the fixture names from Task 2 for Task 6's verification.
- Produces: the skill itself. Directory name `next-steps/` and frontmatter `name: next-steps` must match, or `setup.sh` links a skill whose internal name disagrees with its trigger.

- [ ] **Step 1: Write the skill body**

Create `next-steps/SKILL.md`:

````markdown
---
name: next-steps
description: Scopes the next release out of an existing backlog using MoSCoW, then produces the build order for what it scoped. Use this skill when the user types "nextsteps" or "!nextsteps", or asks to "scope the next release", "what goes in the next release", "triage the backlog", "prioritise these", "what should I do next", "run MoSCoW on this", or wants a list of open work cut into what ships next and what waits. Writes the verdict back into the project's one backlog file as priority markers plus inline comments. Do NOT use for generating new ideas (free-think-day, free-dev-day), designing one feature (brainstorming), planning how to build one feature (writing-plans), reporting what already shipped (exec-steps), or validating documentation (project-standard).
version: "1.0"
authors: Fero Novak <https://feronovak.com>
---

Cut an existing backlog into the next release, then say in what order to build it.

Optional argument, taken from the text following the trigger word and possibly
empty (when invoked as a slash command it arrives here): $ARGUMENTS

This skill **consumes** candidates. It never goes hunting for them. If the
backlog is thin, that is a finding to report, not a licence to scan the repo and
invent work.

---

## Step 0 — Resolve

Three things, in this order. Report all three back before proposing anything.

**Source.** One of:

| Source | Where the candidates come from |
|---|---|
| session | Follow-ups from the work done in this session |
| backlog | The rows already in the backlog file |
| handoff | The tail of `exec-steps`, `free-think-day`, or `project-standard` |

Default to `backlog` when the argument does not say and a backlog file exists.
Use `session` when there is no backlog file, or when the user's phrasing points
at what was just done.

**The backlog file.** Search in this order: `docs/NEXT_STEPS.md`, then
`ROADMAP.md`, then `TODO.md`.

- **More than one match — refuse to write, and stop.** Name every file found.
  Do not triage the items anyway and offer to write afterwards; the refusal
  comes before the round. Choosing one silently is how a second backlog is born,
  which is the condition `project-standard` check 26 exists to prevent.
- **No match, source is `session`** — offer to create `docs/NEXT_STEPS.md` and
  seed it with the session's follow-ups.
- **No match, any other source** — say there is nothing to triage. Do not scan
  the repo to manufacture candidates.

**The release.** Read the version from a manifest — `package.json`,
`pyproject.toml`, `Cargo.toml`, a `VERSION` file.

- **Found** — the boundary is the next bump from that version. Name it.
- **Not found** — the boundary is "the next block of work". **Say the cut-off is
  soft**, so the round is not mistaken for carrying more discipline than it does.
  Do not invent a version number.

## Step 1 — Propose

Read `references/moscow.md` now.

Assign a letter to **every** item. Nothing is left blank, and nothing is handed
to the user that could have been reasoned about first.

Where the proposed letter **differs** from the item's standing marker, a reason
is mandatory. Where it agrees, one line is enough.

Propose against the release boundary and against dependencies between items —
never against the existing markers. A pre-fill that mirrors the current markers
back is worthless: the user would be approving their own past self, and the
round would have added nothing.

Print one table:

```
#  Item                              Now  Proposed  Why
1  Session expiry on magic links     🟥   MUST      —
2  Rate-limit the login endpoint     🟧   MUST      auth hole is only half
                                                    closed without it
3  Passkey support                   ⬜   WON'T     nobody has asked
```

Then apply the 60% guard from `references/moscow.md` and report the result —
including reporting that it could not be computed, when no estimates exist.

## Step 2 — Correct

Ask for free-text corrections. Not per-item prompts: the round's value is seeing
the whole cut at once, and batched multi-select hides the shape while the user
is inside it.

Accept forms like `flip 4 to Must, kill 5, hold 2 until 1 lands`. Restate what
changed, then ask again. **Loop until the user stops correcting.**

`kill` is ambiguous on its own — it may mean Won't-ever or already-done, and both
delete the row. Ask which, once, per row.

## Step 3 — Plan

Read `references/release-plan.md` now.

Emit the build order for the Musts and Shoulds. Name any Must that needs a spec,
with the reason it is judged non-trivial. Offer `brainstorming` for those; never
invoke it without agreement.

## Step 4 — Diff

Show every line that will change, before writing anything:

```
docs/NEXT_STEPS.md

~ 🟧 → 🟥  Rate-limit the login endpoint
+          *Held: not before session expiry lands.*
- ⬜       Passkey support                        (Won't — ever, confirmed)
+ ⬜       Retire the CSV exporter                (ADDED from session)
```

Session follow-ups are the **only** rows this skill ever adds, and they appear as
`ADDED` here before they are written.

## Step 5 — Apply

Write the file. Then:

- Bump `Last reviewed:` **only** if the round checked rows against the code or
  infrastructure they describe. Re-ordering is not verification; a round that
  only re-ordered leaves the stamp where it was.
- Report what changed in one short paragraph. No summary table — the diff was
  step 4.

---

## Guardrails

- **Never invent backlog items.** Session follow-ups are the one addition, and
  they are shown as `ADDED` in the diff first.
- **Never write a PRD.** A non-trivial Must without one is named as a gap, with
  the reason, and handed to `brainstorming` only on agreement.
- **Never validate.** `project-standard` owns that, including the one-backlog
  rule this skill writes into. Do not re-implement its checks.
- **Never delete in a batch.** Won't-ever and already-done each need their own
  confirmation. This is the only destructive act in the skill.
- **Never introduce a fourth marker.** Three markers, four letters, and the
  collapse is documented in `references/moscow.md`.
- **Never write a dated narrative into a backlog row.** Present tense only.

## Where this sits

| Stage | Skill |
|---|---|
| Shape a raw idea | `brainstormers-idea` |
| Decide if it is worth building | `business-sharks` |
| Generate candidates | `free-think-day`, `free-dev-day` |
| **Scope the next release** | **this skill** |
| Design one feature | `brainstorming` |
| Plan one feature's build | `writing-plans` |
| Execute | `executing-plans` |
| Report what shipped | `exec-steps` |
| Check the docs agree | `project-standard` |
````

- [ ] **Step 2: Verify frontmatter, name/directory agreement, and reference wiring**

Run: `head -1 next-steps/SKILL.md`
Expected: `---`

Run: `grep -m1 '^name:' next-steps/SKILL.md`
Expected: `name: next-steps` — and it must equal the directory name `next-steps`.

Run: `grep -c 'Do NOT use for' next-steps/SKILL.md`
Expected: `1`

Run: `grep -o 'references/[a-z-]*\.md' next-steps/SKILL.md | sort -u`
Expected:
```
references/moscow.md
references/release-plan.md
```

Run: `for f in $(grep -o 'references/[a-z-]*\.md' next-steps/SKILL.md | sort -u); do test -f "next-steps/$f" && echo "ok $f" || echo "MISSING $f"; done`
Expected: two `ok` lines. A reference named in the body but absent on disk is a dead instruction.

Run: `test -d next-steps/tool && echo "BUG: tool/ must not exist" || echo "ok no tool dir"`
Expected: `ok no tool dir`

- [ ] **Step 3: Commit**

```bash
git add next-steps/SKILL.md
git commit -m "feat(next-steps): the round

Six steps - resolve, propose, correct, plan, diff, apply. Refuses to
write when two backlog files exist, declares a soft cut-off when the
repo carries no version, and adds rows only from the session source.

References carry the decision rules so the always-loaded body stays
short."
```

---

### Task 6: README, install, and end-to-end verification against all four fixtures

**Files:**
- Create: `next-steps/README.md`
- Modify: none — `setup.sh` already picks up any directory containing a `SKILL.md`

**Interfaces:**
- Consumes: everything from Tasks 1–5.
- Produces: the installed skill at `~/.claude/skills/next-steps`, and a verified pass against the four evals.

- [ ] **Step 1: Write the README**

Create `next-steps/README.md`:

```markdown
# next-steps

Cuts an existing backlog into the next release using MoSCoW, then produces the
build order for what it scoped.

## Why it exists

The skill chain had a hole in it:

| Stage | Skill |
|---|---|
| Shape a raw idea | `brainstormers-idea` |
| Decide if it is worth building | `business-sharks` |
| Generate candidates | `free-think-day`, `free-dev-day` |
| **Scope the next release** | **— nothing —** |
| Design one feature | `brainstorming` |
| Plan one feature's build | `writing-plans` |
| Execute | `executing-plans` |
| Report what shipped | `exec-steps` |
| Check the docs agree | `project-standard` |

`writing-plans` plans one spec. `RELEASING.md` describes the release *process*.
Neither decides what goes into the next release. A backlog with 25 open rows and
no cut is a list, not a plan.

## What it does not do

- **Does not generate candidates.** It triages what exists.
- **Does not write PRDs.** It names where one is missing.
- **Does not validate.** `project-standard` does that.
- **Is not `writing-plans`.** This decides which items and in what order;
  `writing-plans` decides how to build one of them.

## Usage

```
nextsteps
nextsteps session
```

The round: resolve the source, the backlog file and the release → propose a
MoSCoW letter for every item → take free-text corrections until you stop → emit
the build order → show the diff → write.

## How the verdict lands

MoSCoW letters do not persist. They move the standing marker and the round is
over:

| Verdict | Effect |
|---|---|
| Must | `🟥` |
| Should | `🟧` |
| Could | `⬜` |
| Won't — this release | `⬜` |
| Won't — ever | row deleted, confirmed individually |
| Already done | row deleted, confirmed individually |

Reasoning lands inline under the row, in the present tense.

## Evals

`evals/evals.json` declares four, each naming the failure mode it discriminates
against. Fixtures are plain directories under `evals/fixtures/` — the skill must
work without git.

The two judgment calls — the `needs spec` determination and the Must/Should
boundary — are not covered by any fixture and will sometimes be wrong. Fixtures
catch mechanics, not taste.
```

- [ ] **Step 2: Install and confirm the symlink resolves**

Run: `bash setup.sh 2>&1 | grep -E 'next-steps|skipped'`
Expected: a line reading `linked: next-steps` (or `refreshed: next-steps` on a re-run). If it reads `skipped: next-steps`, a real directory is shadowing the symlink at `~/.claude/skills/next-steps` and must be removed by hand.

Run: `readlink -f ~/.claude/skills/next-steps`
Expected: `/home/fnovak/projects/claude-skills/next-steps`

Run: `test -f ~/.claude/skills/next-steps/references/moscow.md && echo "ok references reachable through the symlink"`
Expected: `ok references reachable through the symlink`

- [ ] **Step 3: Run eval 3 first — the refusal**

Eval 3 is first because it is the only one with a binary, unmistakable outcome, and a skill that writes when it should refuse has a defect no later eval will surface.

Copy the fixture to scratch so the round cannot dirty the repo:

```bash
rm -rf /tmp/claude-1000/ns-eval && mkdir -p /tmp/claude-1000/ns-eval
cp -r next-steps/evals/fixtures/two-backlogs /tmp/claude-1000/ns-eval/
```

In a fresh session, `cd /tmp/claude-1000/ns-eval/two-backlogs` and invoke `nextsteps`.

Expected: refuses to write, names **both** `docs/NEXT_STEPS.md` and `ROADMAP.md`, and does not triage the two items anyway.

Then confirm nothing was written:

```bash
diff -r next-steps/evals/fixtures/two-backlogs /tmp/claude-1000/ns-eval/two-backlogs && echo "ok nothing written"
```
Expected: `ok nothing written`

- [ ] **Step 4: Run evals 1, 2 and 4**

For each of `versioned-product`, `unversioned-docs`, `no-estimates`: copy to `/tmp/claude-1000/ns-eval/`, `cd` into the copy, invoke `nextsteps`, and check the run against that eval's `expectations` array in `evals.json`.

The three findings that most often fail, and what each proves:

| Fixture | Must appear | Proves |
|---|---|---|
| `versioned-product` | a version bump from `1.4.0`, and item 2 ordered after item 1 | the boundary is a release, and dependencies were actually read |
| `unversioned-docs` | "no version found" and an explicit soft cut-off | absence was noticed rather than papered over |
| `no-estimates` | "cannot check the 60% guard", and no percentage anywhere | the guard declined instead of fabricating |

Record each result in the eval's entry as a `result` field — pass, or what was
observed instead. An eval whose outcome is not written down did not run.

- [ ] **Step 5: Commit**

```bash
git add next-steps/README.md next-steps/evals/evals.json
git commit -m "docs(next-steps): README and recorded eval results

Four evals run against their fixtures with outcomes recorded. The
refusal case is verified by diffing the scratch copy against the
fixture - a skill that writes when it should refuse fails silently
otherwise."
```

- [ ] **Step 6: Refresh DOCMAP and verify the repo still passes its own standard**

```bash
./project-standard/bin/project-standard generate --repo .
./project-standard/bin/project-standard check --repo .
```

Expected: no **new** errors attributable to `next-steps/`. The repo's pre-existing findings are not this plan's to fix.

Note: running the tool rewrites tracked `__pycache__/*.pyc` files. Leave them dirty. Do **not** `git checkout --` them — the destructive-git hook blocks it, correctly.

```bash
git add docs/DOCMAP.md
git commit -m "docs: index next-steps in DOCMAP"
```

---

## Self-Review

**Spec coverage.** Every section of `2026-08-08-next-steps-design.md` maps to a task:

| Spec section | Task |
|---|---|
| Identity, triggers | 5 |
| The exec-steps collision | 1 |
| Inputs, backlog location, no-backlog case | 5 (step 0) |
| The release, versioned vs unversioned | 5 (step 0), 2 (fixtures 1–2) |
| Step 1 Propose, the 60% guard | 5, 3, 2 (fixture 4) |
| Step 2 Correct | 5 |
| Step 3 Plan, needs-spec judgment | 5, 4 |
| Write-back table, Could/Won't collapse, already-done | 3 |
| Comments, present tense | 3 |
| Last reviewed stamp rule | 5 (step 5) |
| Guardrails | 5 |
| Files | 3, 4, 5, 6 |
| Testing, four fixtures | 2, 6 |

No gaps.

**Placeholder scan.** No `TBD`, no "add error handling", no "similar to Task N".
Every file's full content is written out in the step that creates it. Every
verification step names the command and its expected output.

**Type consistency.** The vocabulary is consistent across tasks: markers are
`🟥` `🟧` `⬜` everywhere; readiness states are `ready`, `blocked by <n>`,
`needs spec` in both `references/release-plan.md` (Task 4) and `SKILL.md` step 3
(Task 5); the four fixture directory names introduced in Task 2 are the same
four used in Task 6 and in `evals.json`; `references/moscow.md` and
`references/release-plan.md` are named identically in Tasks 3, 4, 5 and the
Task 5 wiring check.

One deliberate asymmetry worth naming: Task 1 modifies `exec-steps` and has no
dependency on Tasks 2–6, so it can be reviewed and merged independently if the
rest is rejected.
