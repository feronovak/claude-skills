---
name: project-standard
description: Use when validating or setting up a project's documentation, release flow and git hygiene — checking whether CLAUDE.md/AGENTS.md actually describes the project, whether the code map and product map are current, whether every endpoint is documented, whether releases agree with their tags and changelog, whether local-only files leaked into git, or whether an AI assistant was marked as a contributor. Also use when starting a new repo that should follow the standard from commit 1, when retrofitting an existing repo, or when the user asks "is this project set up right", "check my docs", "scaffold the docs", or "make this repo consistent with the others".
version: "0.2.0"
authors: Fero Novak <https://feronovak.com>
license: MIT
allowed-tools: Bash(project-standard *) Bash(${CLAUDE_SKILL_DIR}/bin/project-standard *)
---

# project-standard

One standard for how a project documents itself, releases, and records who
wrote it — with a CLI for what a machine can decide and this skill for what it
cannot.

## The split, and why it matters

**Mechanical** — does the file exist, do its links resolve, is the endpoint
documented, does the tag match the version, is a local-only path tracked. The
CLI answers these in well under a second per repository, with no model
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
project-standard check --repo <path>     # one repo
project-standard check --fleet           # every repo under the fleet root
project-standard check --only version    # one concern everywhere
project-standard check --json            # machine-readable
```

If `project-standard` is not on PATH, the wrapper is `bin/project-standard`
inside this skill directory; it needs no install.

Then get the worklist, and work it:

```bash
project-standard claims --repo <path>          # every unit, with line numbers
project-standard claims --doc docs/FEATURE_MAP.md   # one document
```

**Do not read a document and report what you noticed.** That is a spot-check,
and its recall is proportional to how much of the document you happened to
sample. Measured across five runs over one 40-row product map: each verified a
different subset, none found every false row, and the run told most forcefully
to be thorough scored worst — while opening with a claim that it had checked
every row. Working from the enumerated list is what makes the difference; being
told to try harder is not.

For each unit: verify it, or mark it unchecked. Then report both.

### The five semantic checks

1. **Does the agent contract describe this project?** Real modules, real
   commands — or boilerplate that would fit any repo of the same framework?
2. **Is every `claim` unit true of the code today?** Open the implementation
   the row names — the function, its inputs, its call site. A commit message,
   a test name and a sibling document are all evidence about what someone
   believed, not about what the code does. Highest hit rate of the five.
3. **Does every `mapping` unit hold?** The CLI verifies the paths resolve; you
   verify the responsibility described is what lives there.
4. **Is a profile or capability override genuine**, or a way to dodge a check?
5. **Is a trust stamp plausible** given what has landed since it was applied?

`prd-header` and `prd-section` units are never checked against the code — a
PRD is intent, and a proposal already true of the code would not need writing.
Check that it is owned, linked and decided.

### Report coverage, always

Close every judgement pass with the denominator:

```
Verified 34 of 41 units in docs/FEATURE_MAP.md.
Not checked: lines 88, 91, 104-108 (admin sub-panels — needs a running instance).
```

A pass that names no denominator reads as an audit while being a sample. That
is the same dishonesty the trust stamps exist to prevent, and the mechanical
half already refuses it by reporting a check as skipped rather than passed.
Where you cannot verify a unit, say which and why — never let it go silent.

## setup — retrofitting

**Reconcile before you create.** Most repos already have a document doing a
slot's job under another name. Creating `FEATURE_MAP.md` beside an existing
`NORTH_STAR.md` leaves two documents asserting what the product does, which is
the disease this skill treats, arrived at from the other direction.

| Incumbent | Slot |
|---|---|
| `ROADMAP.md`, `TODO.md`, `IMPLEMENTATION_ROADMAP.md` | `docs/NEXT_STEPS.md` |
| `NORTH_STAR.md` | direction — already the slot; leave it where it is |
| `MISSION.md`, `VISION.md`, `STRATEGY.md` | direction — **rename to `NORTH_STAR.md`**; check 30 matches the filename, not a contract pointer |
| `RELEASING.md` | release flow — satisfies the slot, do not add a second |
| `API_REFERENCE.md` in prose | api reference — diff it against the routes, do not replace it |
| `PRDs/`, `docs/prd/` | `docs/prds/` |
| `ADR/`, `docs/adr/`, `docs/decisions/`, `ARCHITECTURE_DECISIONS.md` | decisions — a directory of records satisfies the slot, leave it |

Rename or merge. Only create when no incumbent exists. Ask when it is ambiguous.

**Repointing inbound links is not a string replacement.** A merged doc is usually
referenced from an index, where the link text and the surrounding row carry meaning
a blind substitution destroys — a golden-path list ends up with the same entry
twice, or a row still labelled with the old document's name pointing at the new one.
Grep the inbound references first, rewrite them, then **re-read every index that
changed** and fix its structure by hand.

**Rewriting commit history needs a clean working tree.** `git filter-branch` and
friends refuse to run with unstaged changes, and the obvious escape — `git stash` —
is blocked outright on some setups by a destructive-git guard. Copy the dirty files
aside, restore the committed content with `git show HEAD:<path> > <path>`, rewrite,
then copy back. No git state is destroyed and no guard fires.

**Never introduce a file named for an assistant the project does not use.**
Read the repository first: an existing `AGENTS.md`, a `.codex/`, `.agents/`,
`.cursor/rules/` or `.github/copilot-instructions.md` all say which assistant
this project is written with. Extend what is there and match it. Creating a
`CLAUDE.md` in a repository built with something else is a foreign artifact,
and in a public repository it reads as one vendor planting a flag. When nothing
indicates a preference, `AGENTS.md` is the neutral choice.

**Then generate the index.** `docs/DOCMAP.md` is a required slot with no
template, and only the generator produces one the freshness check accepts:

```bash
project-standard generate --repo <path>   # writes docs/DOCMAP.md
```

Run it, commit, then run it once more — the map indexes itself, so the first
output is stale the moment it is tracked. Hand-writing this file instead leaves
the repo permanently failing its own freshness check.

**If the repo already generates its own index, do not run `generate`** — it
would overwrite a working repo-native file with this tool's format. Declare
`docmap: own` in the contract instead. Check 3 then answers freshness by
ancestry rather than by byte comparison, so the check still runs and the repo
keeps its generator.

**Then set the baselines.** Adoption is what makes a red repo green without
anyone pretending the work is done:

```yaml
adopted: <the current commit>   # attribution errors start here
api-coverage: 12                # endpoints documented today; fewer is a regression
scaffold: 7                     # required docs still holding TODO tokens
```

**Count `scaffold` honestly and set it exactly.** It is the number of required
documents that still carry a `TODO(project-standard)` token right now. At or
under it, an unwritten document is reported as debt; above it, as an error.
Setting it high to buy silence defeats the mechanism.

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
finding like any other. A declaration that merely agrees with detection is not
an override and costs nothing.

Then scaffold from `templates/`, and finish as setup does: run
`project-standard generate`, commit, generate again.

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
| **`DECISIONS.md`** | **why a choice was made, and what it cost** | **no — the reasoning was in someone's head, not the diff** |

For the two marked no: scaffold a list of *candidates* marked `unverified`,
never a list of claims, and work through them with the user.

**Retrofitting a changelog does not invent history.** Where tags do not reach
back far enough, the file starts at the current version and says so.

## House rules are defaults, not universals

This skill is meant to be pointed at other people's repositories. Before
reporting a house rule as a violation, check whether the repo declared
otherwise:

```yaml
local-only:            # extend the default set
  - scratch/
track-anyway:          # keep tracking something the default would flag
  - logs/
ai-attribution: allow  # this repo wants the Co-Authored-By trailers
decisions: waived      # this repo owes no decision log
  reason: a single script; there is no architecture to decide
```

**A slot may be waived, never silently.** `decisions: waived` with no `reason:`
is an error. Policy is the repo's — which paths are local-only, whether
attribution is forbidden, whether a slot applies. Structure is the standard's:
which documents exist and what they are called does not vary per repo, or two
conformant repositories look nothing alike and the standard has bought
nothing.

`ai-attribution` defaults to `forbid` because the tooling appends those markers
unless told otherwise — silence produces the marker rather than its absence.
A repo that declares `allow` is not in breach, and the checks stand down.

## Reference

- `references/standard.md` — every artifact, its slot, and what it asserts
- `references/git-hygiene.md` — the five attribution markers and the local-only set
- `references/release-flow.md` — the bump axis, the three-way gate, channels
- `README.md` — the CLI surface, severity model, CI setup, and the list of
  designed-but-unimplemented checks

## Secrets

The standard recommends a dedicated scanner and ships none — a partial pattern
list posing as a gate gives false confidence. Check 40 warns when no scanner is
configured and goes quiet once one is.

What it does enforce is that secret *values* never appear in the agent
contract, a skill, a template or any tracked document. The machine-readable
block holds paths and references, never values. The pattern is a gitignored
real file plus a redacted mirror whose values read `REPLACE_ME`.

Check 41 reads tracked documentation only. When you report it, say what it is:
documentation hygiene, not a scan, and never evidence that a repository is
clean.

## Two things the CLI cannot do

**Pull request bodies.** Git hooks never see them, so the
assistant generation notice in a PR body has no mechanical guard anywhere. Check it
by eye when a PR is opened. Do not claim a guard that does not exist.

**Anything in a repo with no git.** The checker refuses rather than reporting a
repo as conformant on checks that never ran. Offer `git init`.

## Six checks the design describes and the code does not

21, 27, 31, 34, 35, 39 — listed in `README.md`. Do not report them as
passing; they never ran. 27 and 31 are judgement calls, so cover them yourself
when the repo warrants it: a document that reads like a second backlog, and a
direction concept restated in more than one place.
