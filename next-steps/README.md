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
