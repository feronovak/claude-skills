# project-standard

One standard for how a project documents itself, releases, and records who
wrote it — plus a stdlib-only checker that enforces the half a machine can
decide.

## Why it is split

Checks fall into two kinds, and conflating them produces either a slow validator
or one that cannot run in CI.

**Mechanical** — does the file exist, do its links resolve, is the endpoint
documented, does the tag match the version, is a local-only path tracked.
Decidable by string comparison; the same answer every run. Well under a second
per repository, no model, no tokens. Runs from CI, a hook, cron, or a shell.

**Semantic** — does the contract describe *this* project or a generic framework,
does the product map claim something the code no longer does, is a trust stamp
plausible. Nothing decides these but judgement. That half is the skill.

A validator that only exists inside a model runs when someone remembers it.
That is how a set of related repos ends up with as many different structures
as it has repos.

## Install

The tool takes no dependencies and needs no install step. Run it from anywhere:

```bash
python3 -m project_standard.cli check --repo /path/to/your-repo
```

To gate a repo's CI, vendor `tool/project_standard/` to
`scripts/project-standard/` and add a job (see **CI** below).

To install the authorship guards:

```bash
project-standard install-hooks            # this repository
project-standard install-hooks --global   # every repository
```

This sets `core.hooksPath`, which **replaces** any other hooks directory — if
you already have one, merge its hooks into the new location.

## Usage

```bash
project-standard check                    # this repo, every check
project-standard check --repo NAME        # one repo, by path or by name under the fleet root
project-standard check --only version     # one concern, repeatable
project-standard check --fleet            # every git repo under the fleet root
project-standard check --json             # machine-readable
project-standard check --profile=ci       # skip what a runner cannot answer

project-standard install-hooks            # install the authorship guards
project-standard generate                 # write docs/DOCMAP.md
project-standard routes --app app:create_app   # write docs/api/routes.json
```

Exit code is non-zero on error-severity findings, so no wrapper is needed to
gate CI, a pre-push hook, or a cron.

`--only` is what makes a rule change cheap to assess: change a rule, ask one
question of every repo, ignore everything else.

The fleet root is `$PROJECT_STANDARD_FLEET`, falling back to the parent of the
current repository — the common "all my projects sit side by side" layout.

## What is universal, and what is a house rule

The tool is meant to be pointed at someone else's repositories, so anything
tuned to one setup is declarable in the contract rather than baked in.

| Level | Example | Overridable |
|---|---|---|
| universal | a package manifest means shipped software | no |
| common | `logs/`, `coverage/`, `.pytest_cache/` are machine-local | yes |
| house | agent and editor scratch dirs; forbidding AI attribution | yes |

```yaml
local-only:            # extend the default set
  - scratch/
track-anyway:          # keep tracking something the default would flag
  - logs/
ai-attribution: allow  # this repo wants the Co-Authored-By trailers
```

`local-only: [replace, ...]` swaps the set entirely. `ai-attribution` defaults
to `forbid` because the tooling appends those markers unless told otherwise —
silence produces the marker rather than its absence — but a team that wants the
attribution says so and the checks stand down.

## Profile detection

| Profile | Signal |
|---|---|
| `library` | a manifest declaring distribution — `bin`/`exports`/`publishConfig`, `[project.scripts]`, `[lib]` |
| `product` | any package manifest, or a conventional source root (`src`, `app`, `lib`, `cmd`, `pages`, …) |
| `docs` | neither |

Detection is by packaging convention, not by absence of code and not by a
markdown ratio. An infrastructure repo holds shell scripts, and a
documentation-heavy product can be 41% markdown — both break the naive tests.

## Severity

| Level | Exit | Meaning |
|---|---|---|
| `error` | 1 | broken, or self-contradictory |
| `warn` | 0 | worth knowing, not a defect — a gradual retrofit, or a fact about the repo |
| `skipped` | 0 | the check could not run here, and says so |

**`skipped` is a third outcome on purpose.** A check that did not run must never
read as a check that passed.

Anything unfixable in one sitting is a warn by construction. A validator that
reports 150 failures on its first run does not survive the week.

## CI

```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 0        # required: eight checks need history and tags
- run: python3 -m project_standard.cli check --profile=ci
```

`fetch-depth: 0` is not optional. GitHub Actions clones one commit with no tags
by default, which makes every history-dependent check unanswerable — they are
skipped and reported as skipped, never silently passed.

`--profile=ci` also skips the hook checks: a runner has no developer hooks
directory, and that check asks about a workstation.

## Development

```bash
cd tool
PYTHONPATH=.:tests python3 -m unittest discover -s tests -t . -v
```

134 tests, stdlib `unittest`, no dependencies. Fixtures build throwaway git
repos in temp directories, with `core.hooksPath` pointed at an empty directory
so the global hygiene guards never interfere — otherwise a test that
deliberately commits a Claude trailer would be blocked by the very hook the
checker is being tested for.

`test_fleet_smoke.py` runs against whatever real repositories are present and
skips cleanly when there are none. It is the test that keeps the suite honest: every defect found
while designing this standard came from a real repo, and not one came from a
fixture. Fixtures encode what the author already believes.

## Layout

```
SKILL.md                     the orchestrator — modes, semantic checks
references/
  standard.md                artifacts, slots, taxonomy, baselines
  git-hygiene.md             the five attribution markers, the local-only set
  release-flow.md            version source, bump axis, tags, the three-way gate
hooks/                       the authorship guards, installed by install-hooks
templates/                   skeletons carrying TODO tokens, never plausible prose
tool/project_standard/
  defaults.py                universal / common / house, and the overrides
  findings.py                the one shared vocabulary
  gitio.py                   every git read, in one place
  contract.py                the restricted-subset parser for the contract block
  detect.py                  profile and capabilities, from code
  artifacts.py               slots and presence
  docs.py                    stamps, tokens, links, duplicates
  release.py                 version source, tags, changelog
  hygiene.py                 local-only paths, attribution, hooks
  api.py                     route enumeration and endpoint coverage
  docmap.py                  the DOCMAP generator
  runner.py                  the registry, profiles, exit codes
  cli.py                     argument surface
```

Every checker module exports `check(ctx) -> list[Finding]` and imports nothing
from its siblings. `gitio` is the only module that knows git exists.

## Checks

44 checks are implemented. Seven that the design describes are **not**, and are
listed here rather than left to be discovered:

| Not implemented | What it would do |
|---|---|
| 17 | vendored copy is behind the canonical version |
| 21 | the repo restates global agent tiering instead of pointing at it |
| 27 | a non-backlog document reads like an ordered backlog |
| 31 | a direction concept is stated in more than one file |
| 34 | a PRD marked shipped is not archived under that version |
| 35 | a draft PRD has no matching backlog entry |
| 39 | a major bump with no changelog entry describing a break |

Checks 27 and 31 need judgement rather than pattern matching and belong to the
skill's semantic half. The rest are mechanical and simply unwritten.

Two checks exist beyond the design: `5b` (version sources disagree — split out
because it needs no history and so must survive a shallow clone) and `8e` (an
assistant generation notice in a commit message).

## Design

The full design, the rationale for each rule, and a log of every defect found
while building it live in the design document alongside this skill.
