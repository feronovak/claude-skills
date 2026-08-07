# next-steps — design

**Status:** approved
**Date:** 2026-08-08
**Author:** Fero Novak

A skill that scopes the next release out of an existing backlog, using MoSCoW,
and produces the build order for what it scoped.

## Why it exists

The skill chain has a hole in it:

| Stage | Skill |
|---|---|
| Shape a raw idea | `brainstormers-idea` |
| Decide if it's worth building | `business-sharks` |
| Generate candidates | `free-think-day`, `free-dev-day` |
| **Scope the next release** | **— nothing —** |
| Design one feature | `brainstorming` → spec |
| Plan one feature's build | `writing-plans` |
| Execute | `executing-plans` |
| Report what shipped | `exec-steps` |
| Check the docs agree | `project-standard` |

`writing-plans` plans one spec. `RELEASING.md` describes the release *process*.
Neither decides what goes into the next release. A backlog with 25 open rows and
no cut is a list, not a plan.

## What it is not

- **Not a generator.** It triages what exists. `free-think-day` and
  `free-dev-day` produce candidates; this consumes them.
- **Not a PRD writer.** A non-trivial Must with no `docs/prds/<feature>.md` is
  named as a gap and handed to `brainstorming` — never filled silently.
- **Not a validator.** `project-standard` validates, and owns the one-backlog
  rule this skill writes into.
- **Not `writing-plans`.** Different altitude: this decides *which items and in
  what order*; `writing-plans` decides *how to build one of them*.

## Identity

Directory `next-steps/`, symlinked into `~/.claude/skills/` by `setup.sh`.

Triggers: `nextsteps`, `!nextsteps`, "scope the next release", "what's in the
next release", "triage the backlog", "prioritise these", "MoSCoW".

Explicitly excluded from the description: generating candidates, designing one
feature, planning one feature's build, reporting what shipped.

### The exec-steps collision

`exec-steps`' description contains the phrase **"what did we do and what's
next"**, which reaches directly for this skill's work. Two skills competing for
one prompt is a triggering defect, not a preference.

Fix, as part of this work: narrow that phrase in `exec-steps` to the
retrospective half, and add `next-steps` to its "Do NOT use for" list. No
behaviour change to `exec-steps` beyond triggering.

## Inputs

Source is one of three. Never a cold scan of the repo.

1. **This session's work** — follow-ups from what was just done
2. **The backlog file** — re-triage what is already written
3. **Another skill's output** — the tail of `exec-steps`, `free-think-day`, or
   `project-standard`

The backlog is located, not hardcoded: `docs/NEXT_STEPS.md`, else `ROADMAP.md`,
else `TODO.md`. **If more than one candidate exists the skill refuses to
write** — choosing one silently is how a second backlog is born, which is the
condition `project-standard` check 26 exists to prevent.

If **no** backlog file exists, behaviour depends on the source. With the session
source, the round offers to create the file at the canonical slot
(`docs/NEXT_STEPS.md`) and seed it with the session's follow-ups. With any other
source there is nothing to triage, and the skill says so instead of scanning the
repo to manufacture candidates.

## The release

MoSCoW is a commitment scale against a fixed scope boundary. Without one, every
item drifts to Must and the letters mean nothing. The boundary here is **the
next release**, never a calendar window.

- **Versioned repo** — the next version bump.
- **Unversioned repo** (`project-standard` profile `docs`, `version=—`) — the
  next block of work. The skill states out loud that the cut-off is soft here,
  so the round is not mistaken for carrying more discipline than it does.

## The round

```
0  Resolve   source · backlog file · release identity
1  Propose   MoSCoW for every item
2  Correct   free text, loops until the user stops
3  Plan      build order for Musts and Shoulds
4  Diff      every line that will change
5  Apply     write
```

### Step 1 — Propose

Every item gets a letter. Nothing is left blank, and nothing is deferred to the
user that the skill could have reasoned about.

Where the proposed letter **differs** from the item's standing marker, a reason
is mandatory. Where it agrees, one line. The difference column is the output;
the rest is confirmation.

A pre-fill that mirrors the existing markers back is worthless — the user would
be approving their own past self. The proposal is made against the release
boundary and against dependencies between items, not against the current
markers.

### The 60% guard

The backlog carries rough effort estimates (`~1 hr`, `2–3 hr`). Where they
exist, if the Musts exceed **~60% of the release's estimated effort**, the round
says so and asks what drops. This is the only mechanical defence against
everything becoming Must.

Where estimates are absent, the skill says it cannot check rather than
pretending it did.

### Step 2 — Correct

Free text, not per-item prompts. `flip 4 to Must, kill 5, hold 2 until 1 lands`.
Loops until the user stops correcting.

Rejected alternative: batched interactive multi-select, ~7 round-trips for 25
items. More rigorous per vote, but it hides the shape of the round while the
user is inside it, and the round's value is seeing the whole cut at once.

### Step 3 — Plan

For the Musts and Shoulds only, in order:

| State | Meaning |
|---|---|
| `ready` | can start now |
| `blocked by <n>` | depends on another item in this release |
| `needs spec` | non-trivial and has no PRD |

The `needs spec` call is the weakest judgment in the skill. It states its
reason and is overruled in the same free-text pass as everything else. It never
routes anything to `brainstorming` without agreement.

## Write-back

| Verdict | Effect |
|---|---|
| Must | 🟥 |
| Should | 🟧 |
| Could | ⬜ |
| Won't — this release | ⬜ (demoted if it currently reads 🟥 or 🟧) |
| Won't — ever | row **deleted**, one explicit confirmation per row |
| Already done | row **deleted**, same per-row confirmation |

MoSCoW letters do not persist in the file. They are the round's verdict; their
effect is to move the standing marker. One scale survives, so there is no second
column to maintain and nothing that can disagree with itself.

**Could and Won't-this-release both land on ⬜.** Three markers cannot carry four
letters, and the collapse is accepted rather than solved: the standing scale is
deliberately coarser than the round's verdict. Where the difference matters, the
inline comment carries it — `*Could: if the release has room after the ACL.*`
Inventing a fourth marker to preserve the distinction would add a symbol to
every backlog in the fleet to record a state that lasts one round.

A row the user reports as already shipped is deleted, not marked done. That
follows the standing rule that a roadmap holds future work only, and that
completed items leave rather than moving to a done-section.

Comments land inline under the row, present tense:

```markdown
- 🟧 **OpenClaw as non-root** (2–3 hr). Turns the allowlist from a speed-bump
  into a real boundary.
  *Held: not before the off-site backup lands.*
```

Never a dated narrative. "Held, and why" is current state; "deprioritised on
2026-08-08" is changelog, and the global `doc-state-guard.py` hook warns on it
correctly.

The `Last reviewed:` stamp bumps **only** if the round checked the rows against
the code or the infrastructure they describe. Re-ordering rows is not
verification, and a round that only re-ordered leaves the stamp where it was —
the same rule that applies to any other document under the standard.

## Guardrails

- Never invents backlog items. Session follow-ups are the one addition and are
  shown as `ADDED` in the diff before anything is written.
- Never writes a PRD.
- Never validates; defers to `project-standard`.
- Refuses to write when more than one backlog file is found.
- Shows the diff before every write.
- Deleting a row is the only destructive act, requires per-row confirmation, and
  never happens in a batch. This covers both Won't-ever and already-done.

## Files

```
next-steps/
├── SKILL.md                    the round, the guardrails, the handoffs
├── README.md                   what it is, why it exists
└── references/
    ├── moscow.md               letter definitions, the 60% guard,
    │                           Won't's two flavours
    └── release-plan.md         ordering + readiness output format
```

No code, so no `tool/` directory and no unit suite.

## Testing

Fixtures plus dry runs:

1. A versioned product repo — real release boundary
2. An unversioned docs repo — soft cut-off, must be declared as such
3. A repo with two backlog files — must refuse to write
4. A backlog with no effort estimates — must decline the 60% check rather than
   fake it

Fixtures catch mechanics, not taste. The two judgment calls — the `needs spec`
determination and the Must/Should boundary — are not covered by any fixture and
will sometimes be wrong. This is the same limit measured in the `design-police`
eval work, and it is stated rather than designed around.

## Rejected options

**Extending `exec-steps` with a triage phase.** Cheapest build, one trigger to
remember. Rejected: `exec-steps` is an evidence-validated retrospective written
for a board, one-shot, side-effect-free apart from its own dated file. This is
forward-looking, written for one reader, interactive, and mutates the backlog. A
skill that edits the canonical backlog must be invoked deliberately, never ride
along inside a summary command.

**Adding general backlog stewardship** (killing stale rows, merging duplicates,
enforcing future-only). Rejected as unbounded — it grows into a second
`project-standard`, and those rules already live in `CLAUDE.md` and that
checker.

**Writing a durable release-scope document.** Rejected for now: "what is in the
release before it ships" has no slot in `project-standard`'s taxonomy, and
inventing one means every conformant repo inherits it. That is a change to the
standard, not to this skill. Additive later if the need proves real.

**Multi-person voting via a shared artifact.** Out of scope — this is solo
triage. Would require artifact runtime capabilities and persistent shared
state, a materially larger build.

**A visual MoSCoW board artifact.** Dropped in favour of the terminal table.
The board shows the shape of the round but costs a second surface for a
single-reader skill.
