---
name: next-steps
description: Scopes the next release out of an existing backlog using MoSCoW, then produces the build order for what it scoped. Use this skill when the user types "nextsteps" or "!nextsteps", or asks to "scope the next release", "what goes in the next release", "triage the backlog", "prioritise these", "what should I do next", "run MoSCoW on this", or wants a list of open work cut into what ships next and what waits. Writes the verdict back into the project's one backlog file as priority markers plus inline comments. Do NOT use for generating new ideas (free-think-day, free-dev-day), designing one feature (brainstorming), planning how to build one feature (writing-plans), reporting what already shipped (exec-steps), or validating documentation (project-standard).
version: "1.1"
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

Four things, in this order. Report all four back before proposing anything.

**Source.** One of:

| Source | Where the candidates come from |
|---|---|
| session | Follow-ups from the work done in this session |
| backlog | The rows already in the backlog file |
| handoff | The tail of `exec-steps`, `free-think-day`, or `project-standard` |

Default to `backlog` when the argument does not say and a backlog file exists.
An argument that names no source — empty, or a bare path — does not say.
Use `session` when there is no backlog file, or when the user's phrasing points
at what was just done.

**The backlog file.** Look for every one of `NEXT_STEPS.md`, `ROADMAP.md`,
`TODO.md`, `BACKLOG.md`, `PLAN.md` and `IMPLEMENTATION_ROADMAP.md` — all six,
every time, matched by filename anywhere in the tree rather than at the root
alone. This is not a first-match chain: the refusal below can only fire if you
checked them all. Where exactly one exists, that is the backlog; where the
canonical slot must be named, it is `docs/NEXT_STEPS.md`.

Those six are the names the `project-standard` checker treats as backlogs,
where a project uses it. That is a default, not a requirement: if the user
names a different file, use theirs. A name this skill does not look for is a
second backlog it will silently ratify.

- **More than one match — refuse to write, and stop.** Name every file found.
  Do not triage the items anyway and offer to write afterwards; the refusal
  comes before the round. Choosing one silently is how a second backlog is born:
  two lists of open work that disagree, with no way to tell which is current.
- **No match, source is `session`** — offer to create `docs/NEXT_STEPS.md` and
  seed it with the session's follow-ups.
- **No match, any other source** — say there is nothing to triage. Do not scan
  the repo to manufacture candidates.

**The priority scale.** Read `references/conventions.md`. Find the scale the
backlog already uses — from its legend, from its rows, or find that it has
none. Name the bands you found. Where there is none, do not adopt one here;
Step 5 asks first.

**The release.** Read the version from a manifest — `package.json`,
`pyproject.toml`, `Cargo.toml`, a `VERSION` file.

- **Found** — the boundary is the next bump from that version. Name it. Where
  nothing indicates whether the bump is patch, minor or major, say which you
  assumed in one clause. Never pick one silently.
- **Not found** — the boundary is "the next block of work". **Say the cut-off is
  soft**, so the round is not mistaken for carrying more discipline than it does.
  Do not invent a version number.

## Step 1 — Propose

**Classify before you letter.** Read `references/buildable.md` now. A row only
the owner can do is not a next step for development: it never receives a
letter, never enters the release, and moves to `## Yours`. Report those
separately, with what each needs.

Read `references/moscow.md` now.

Assign a letter to **every buildable** item. Nothing is left blank, and nothing
is handed to the user that could have been reasoned about first.

Reason from the release boundary and the dependencies first; compare against the
standing marker only afterwards, to decide whether the reason must be shown.

Where the proposed letter **differs** from the item's standing marker, a reason
is mandatory. Where it agrees, a bare `—` is enough.

The test reads a marker, and the lowest band carries both Could and Won't. So
for any row currently sitting in the lowest band the test cannot resolve, and
the reason is always mandatory.

Propose against the release boundary and against dependencies between items —
never against the existing markers. A pre-fill that mirrors the current markers
back is worthless: the user would be approving their own past self, and the
round would have added nothing.

Print one table:

This example's project uses `🟥 / 🟧 / ⬜`; yours writes whatever bands yours has.

```
#  Item                              Now  Proposed             Why
1  Expire share links after 30 days  🟥   MUST                 —
2  Revoke links on password reset    🟧   MUST                 links outlive the
                                                               credential they
                                                               were issued under
3  Legacy XML importer               ⬜   WON'T (ever)         no tenant has used
                                                               it in a year
```

Propose Won't with its flavour — `WON'T (this release)` or `WON'T (ever)`. A
bare `WON'T` leaves the destructive case invisible in the table until Step 2.

Then apply the 60% guard from `references/moscow.md` and report the result —
including reporting that it could not be computed, when no estimates exist. If
the guard trips, state it and carry the question into Step 2. Do not stop and
wait here; Step 2 is the one place the round blocks for input.

## Step 2 — Correct

Ask for free-text corrections. Not per-item prompts: the round's value is seeing
the whole cut at once, and batched multi-select hides the shape while the user
is inside it.

Accept forms like `flip 4 to Must, kill 5, hold 2 until 1 lands`. Restate what
changed, then ask again. **Loop until the user stops correcting.**

`kill` is ambiguous on its own — it may mean Won't-ever or already-done, and both
delete the row. Ask which, once, per row.

Any row **you** proposed as `WON'T (ever)` needs its own explicit confirmation
here, one row at a time, before it reaches the diff. The diff is not the
confirmation: a user who replies "looks good" to the table has not agreed to
delete anything.

## Step 3 — Plan

Read `references/release-plan.md` now.

Emit the build order for the Musts and Shoulds. Name any Must that needs a spec,
with the reason it is judged non-trivial. Offer `brainstorming` for those; never
invoke it without agreement. Name any Should that drops out because something
outside the release blocks it — dropping one silently is the failure this step
guards against.

Mark any row that waits on the owner as `blocked by you` and say what is
needed; it stays in the release, but it cannot start until they act.

## Step 4 — Diff

Show every line that will change, before writing anything:

Again in the example project's bands — substitute the ones you found in Step 0.

```
docs/NEXT_STEPS.md

~ 🟧 → 🟥  Revoke links on password reset
+          *Held: not before link expiry lands.*
- ⬜       Legacy XML importer                    (Won't — ever, confirmed)
+ ⬜       Retire the v1 webhook                  (ADDED from session)
→ Yours     Rotate the billing provider key         (user-only CLI)
```

Session follow-ups are the **only** rows this skill ever adds, and they appear as
`ADDED` here before they are written.

The example above shows one; a round whose source is `backlog` has no such row.

A `→ Yours` line moves a row into that section. It is a move, never a delete —
the row keeps its text and its history, and nothing is lost.

**The inline comment records what a later reader needs to know about where the
row now stands** — a Could's condition, a Should's blocker, a Must's dependency.
Where Step 1's Why already says it, reuse it in the present tense. A row whose
Why was a bare `—` gets no comment.

## Step 5 — Apply

Write the file. Then:

- Bump a `Last reviewed:` stamp **only** if the file already carries one and
  the round checked rows against the code or infrastructure they describe.
  Re-ordering is not verification, and a file without a stamp does not gain one
  here.
- Report what changed in one short paragraph. No summary table — the diff was
  step 4.

---

## Guardrails

- **Never invent backlog items.** Session follow-ups are the one addition, and
  they are shown as `ADDED` in the diff first.
- **Never write a PRD.** A non-trivial Must without one is named as a gap, with
  the reason, and handed to `brainstorming` only on agreement.
- **Never validate.** Checking that a project's documents are correct is a
  different job. Where `project-standard` is in use it owns that, including the
  one-backlog rule this skill writes into.
- **Never delete in a batch.** Won't-ever and already-done each need their own
  confirmation. This is the only destructive act in the skill.
- **Never invent a band the project does not have.** Where its scale has fewer
  bands than the four letters, they collapse — `references/moscow.md` says how.
  Where it has four or more, each letter maps to its own and nothing collapses.
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
