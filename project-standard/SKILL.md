---
name: project-standard
description: Use when validating or setting up a project's documentation, release flow and git hygiene — checking whether CLAUDE.md/AGENTS.md actually describes the project, whether the code map and product map are current, whether every endpoint is documented, whether releases agree with their tags and changelog, whether local-only files leaked into git, or whether Claude was marked as a contributor. Also use when starting a new repo that should follow the standard from commit 1, when retrofitting an existing repo, or when the user asks "is this project set up right", "check my docs", "scaffold the docs", or "make this repo consistent with the others".
---

# project-standard

One standard for how a project documents itself, releases, and keeps Claude out
of its git history — with a CLI for what a machine can decide and this skill for
what it cannot.

## The split, and why it matters

**Mechanical** — does the file exist, do its links resolve, is the endpoint
documented, does the tag match the version, is a local-only path tracked. The
CLI answers these in about half a second across eight repos, with no model
involved. Never re-derive them by reading files yourself.

**Semantic** — does the contract describe *this* project or a generic framework,
does the product map claim something the code no longer does, is a trust stamp
plausible. No amount of string comparison decides these. This is your half.

Always run the CLI first. Then judge only what it could not.

## Modes

| Mode | When | What it does |
|---|---|---|
| **validate** (default) | "check this repo", "is this set up right" | run `check`, add semantic judgement, report. Changes nothing. |
| **setup** | "scaffold the docs", retrofitting an existing repo | reconcile incumbents, then create what is genuinely missing |
| **init** | a new repo, before the first line of code | ask three questions, scaffold, so the rules apply from commit 1 |

## validate

```bash
python3 -m project_standard.cli check --repo <path>          # one repo
python3 -m project_standard.cli check --fleet                # all of ~/projects/apps
python3 -m project_standard.cli check --only version         # one concern everywhere
python3 -m project_standard.cli check --json                 # machine-readable
```

Then apply the five semantic checks below, and report findings ranked
most-severe first, closing with an "I do now / you do" split and an ordering —
never a bare list.

### The five semantic checks

1. **Does the agent contract describe this project?** Real modules, real
   commands — or boilerplate that would fit any repo of the same framework?
2. **Does `FEATURE_MAP.md` claim anything the code no longer does?** Spot-check
   claims against source. This is the check with the highest hit rate.
3. **Does `PROJECT_MAP.md` match the actual tree?** The CLI verifies the paths
   resolve; you verify the responsibilities are true.
4. **Is a profile or capability override genuine**, or a way to dodge a check?
5. **Is a trust stamp plausible** given what has landed since it was applied?

## setup — retrofitting

**Reconcile before you create.** Most repos already have a document doing a
slot's job under another name. Creating `FEATURE_MAP.md` beside an existing
`NORTH_STAR.md` leaves two documents asserting what the product does, which is
the disease this skill treats, arrived at from the other direction.

| Incumbent | Slot |
|---|---|
| `ROADMAP.md`, `TODO.md`, `IMPLEMENTATION_ROADMAP.md` | `docs/NEXT_STEPS.md` |
| `NORTH_STAR.md`, `MISSION.md`, `VISION.md` | direction — leave it, name it in the contract |
| `RELEASING.md` | release flow — satisfies the slot, do not add a second |
| `API_REFERENCE.md` in prose | api reference — diff it against the routes, do not replace it |
| `PRDs/`, `docs/prd/` | `docs/prds/` |

Rename or merge. Only create when no incumbent exists. Ask when it is ambiguous.

**Then set the baselines.** Adoption is what makes a red repo green without
anyone pretending the work is done:

```yaml
adopted: <the current commit>       # attribution errors start here
api-coverage: 12/61                 # documented today; below this is a regression
scaffold: 4                         # required docs still holding TODO tokens
```

A baseline only ever ratchets down. This is what lets a repo with 61
undocumented endpoints adopt the standard today and pay the debt down over
weeks, instead of carrying a permanently red gate that gets switched off.

**Say plainly that setup does not make the repo green.** It converts unknown
gaps into an ordered worklist with the mechanical parts pre-filled. Claiming
otherwise would be the dishonesty the trust stamps exist to prevent.

## init — a new repo

Detection needs code to read, and a new repo has none. So ask:

1. Is this a **product**, a **library**, or a **docs** repo?
2. Does it expose an **HTTP API**?
3. Which **channels** does it ship on — web, extension, mobile, desktop?

Record the answers as declarations in the contract block; later runs verify them
against the code as it appears, and a declaration the code contradicts becomes a
finding like any other. Then scaffold from `templates/`.

Greenfield is where this standard costs least and pays most: the gitignore and
the hygiene rules are in place at commit 1, so the expensive retrofit step —
un-tracking files that should never have been committed, which history keeps
anyway — never happens.

## Authoring: what may be drafted, and what may not

**Scaffolding never fabricates.** Templates carry
`<!-- TODO(project-standard): ... -->` tokens rather than plausible prose,
because a convincing skeleton that passes the presence check and gets indexed
by DOCMAP is worse than a missing file.

| Artifact | Where content comes from | Draftable |
|---|---|---|
| `PROJECT_MAP.md` | the tree, entry points, package scripts | mostly |
| `API_REFERENCE.md` | routes for the skeleton; the handler for each endpoint's substance | skeleton only |
| `CHANGELOG.md` | `git log` since the earliest tag, as a seed to edit down | seed only |
| agent contract | run/test/build from package scripts; the rest asked | partly |
| `DEVELOPMENT_FLOW.md` | boilerplate; who the consumer is must be asked | partly |
| `NEXT_STEPS.md` | merged from existing backlogs; direction is not asked here | merge only |
| **`FEATURE_MAP.md`** | **what the product does today** | **no** |
| **direction doc** | **mission, vision, north star** | **no — ask, never draft** |

For the two marked no: scaffold a list of *candidates* marked `unverified`,
never a list of claims, and work through them with the user.

**Retrofitting a changelog does not invent history.** Where tags do not reach
back far enough, the file starts at the current version and says so.

## Reference

- `references/standard.md` — every artifact, its slot, and what it asserts
- `references/git-hygiene.md` — the five attribution markers and the local-only set
- `references/release-flow.md` — the bump axis, the three-way gate, channels
- Full design and the defect log: `docs/superpowers/specs/2026-08-04-project-standard-design.md`

## Two things the CLI cannot do

**Pull request bodies.** Git hooks never see them, so the
`🤖 Generated with Claude Code` rule has no mechanical guard anywhere. Check it
by eye when a PR is opened. Do not claim a guard that does not exist.

**Anything in a repo with no git.** The checker refuses rather than reporting a
repo as conformant on checks that never ran. Offer `git init`.
