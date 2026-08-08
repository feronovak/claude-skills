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
invoke it without agreement. Name any Should that drops out because something
outside the release blocks it — dropping one silently is the failure this step
guards against.

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
