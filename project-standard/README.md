# project-standard

One standard for how a project documents itself, releases, and records who
wrote it — plus a stdlib-only checker that enforces the half a machine can
decide.

## Contents

- [Why it is split](#why-it-is-split)
- [Install](#install)
- [Usage](#usage)
- [What is universal, and what is a house rule](#what-is-universal-and-what-is-a-house-rule)
- [Declining a slot](#declining-a-slot)
- [The judgement worklist](#the-judgement-worklist)
- [Profile detection](#profile-detection)
- [Severity](#severity)
- [CI](#ci)
- [Development](#development)
- [Layout](#layout)
- [Checks](#checks)
- [Secrets](#secrets)
- [Design](#design)

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

No dependencies, no install step. Put `bin/` on your PATH, or symlink the
wrapper:

```bash
ln -s "$PWD/bin/project-standard" ~/.local/bin/project-standard
project-standard check --repo /path/to/your-repo
```

Or call the module directly, with `tool/` on the path:

```bash
PYTHONPATH=/path/to/project-standard/tool \
  python3 -m project_standard.cli check --repo /path/to/your-repo
```

To gate a repo's CI, vendor the checker into it and add a job (see **CI**
below):

```bash
project-standard vendor --repo /path/to/your-repo
```

That writes `scripts/project_standard/` — an importable package name, with an
underscore. Commit it. Re-run `vendor` whenever this tool changes: check 17
compares the copy against canonical by content as well as by version, and
reports a copy that has fallen behind.

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
project-standard vendor                   # copy the checker in for CI
project-standard claims                   # the judgement worklist, with line numbers
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
| house | assistant scratch dirs; forbidding AI attribution | yes |

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

## Declining a slot

Policy is the repository's; structure is the standard's. Which paths are
local-only, whether AI attribution is forbidden, whether a given slot applies —
the repo decides, in its contract. Which documents exist and what they are
called does not vary per repo, because two conformant repositories that look
nothing alike mean the standard bought nothing.

A waivable slot is declined in the contract, and never silently:

```yaml
decisions: waived
  reason: a single script; there is no architecture to decide
```

`waived` with no `reason:` is an error. Same gate the profile overrides use,
for the same purpose — an escape hatch that costs nothing becomes the default.

## The judgement worklist

The mechanical half decides what a string comparison can. The other half needs
a model, and a model reading a document reports what it happened to notice.

Measured: five runs over one 40-row product map each verified a different
subset, none found every false row, and the run whose instruction demanded
thoroughness most forcefully scored worst — while opening with a claim that it
had checked every row. Recall follows sample size, not effort.

So `claims` prints the denominator:

```bash
project-standard claims                          # every unit, with line numbers
project-standard claims --doc docs/FEATURE_MAP.md
project-standard claims --json
```

Every document in the taxonomy has a countable unit, and what verifying one
means differs by slot — a product-map row is checked against the code, a PRD
never is, because a proposal already true of the implementation would not need
writing. A document with no countable unit is reported as having none, with the
reason, rather than going missing.

Working from the list is what raises coverage. Being told to try harder does
not, and measurably made it worse.

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

**The checker reads tracked files.** A document that exists on disk but has never
been `git add`ed is invisible to it — a freshly written `LICENSE` keeps failing the
broken-link check until it is staged. This is also why `generate` → commit →
`generate` is the documented order: the index cannot list what git cannot see.

**Trust stamps must be bold.** Check 12 matches `**Last reviewed:** YYYY-MM-DD`
(`docs.py`), and counts nothing else. A plain `Last reviewed: 2026-08-06` is not a
stamp and is reported as absent rather than as malformed — so a repo that stamps
every document the wrong way reads as a repo that stamps none.

**`skipped` is a third outcome on purpose.** A check that did not run must never
read as a check that passed.

Anything unfixable in one sitting is a warn by construction. A validator that
reports 150 failures on its first run does not survive the week.

## CI

```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 0        # required: eight checks need history and tags
- run: PYTHONPATH=scripts python3 -m project_standard.cli check --profile=ci
```

`PYTHONPATH=scripts` is what makes the vendored copy importable — the package
directory must be `scripts/project_standard/`, not a hyphenated name. Write it
with `project-standard vendor`, and re-run that whenever the tool changes: a
vendored copy is a fork the moment it stops matching, and CI then gates on
checks that are not the ones this documentation describes.

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

267 tests, stdlib `unittest`, no dependencies. Fixtures build throwaway git
repos in temp directories, with `core.hooksPath` pointed at an empty directory
so the global hygiene guards never interfere — otherwise a test that
deliberately commits an assistant trailer would be blocked by the very hook the
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
bin/project-standard         runnable wrapper — no install step
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
  baselines.py               the declared baselines, against what history recorded
  claims.py                  the enumerable unit in each document
  docmap.py                  the DOCMAP generator
  vendored.py                a vendored copy against the canonical tool
  runner.py                  the registry, profiles, exit codes
  cli.py                     argument surface
  routes.py                  writes docs/api/routes.json from a live app
```

Every checker module exports `check(ctx) -> list[Finding]` and imports nothing
from its siblings. `gitio` is the only module that knows git exists.

## Checks

48 checks are implemented. Six that the design describes are **not**, and are
listed here rather than left to be discovered:

| Not implemented | What it would do |
|---|---|
| 21 | the repo restates global agent tiering instead of pointing at it |
| 27 | a non-backlog document reads like an ordered backlog |
| 31 | a direction concept is stated in more than one file |
| 34 | a PRD marked shipped is not archived under that version |
| 35 | a draft PRD has no matching backlog entry |
| 39 | a major bump with no changelog entry describing a break |

Checks 27 and 31 need judgement rather than pattern matching and belong to the
skill's semantic half. The rest are mechanical and simply unwritten.

Check 17 (a vendored copy behind canonical) compares content as well as the
version string. The design specified a version comparison alone; measured on the
fleet, a vendored copy differed from canonical in nine modules while both still
declared the same version, so a version-only check would have called it current.

Five checks exist beyond the design: `5b` (version sources disagree — split out
because it needs no history and so must survive a shallow clone), `8e` (an
assistant generation notice in a commit message), `40` (no secret scanner
configured), `41` (a credential-shaped string in tracked documentation) and
`42` (a baseline was loosened).

Check 42 is what makes the baselines mean anything. The design states that a
baseline may never rise, but a baseline compared only against today's contract
enforces nothing: the commit that removes the documentation can edit the number
that would have caught it. So `42` compares each declared baseline against the
extreme the repository already recorded across the contract's own history —
the highest `api-coverage`, the lowest `scaffold`, the first resolvable
`adopted`. Moving `adopted` forward is an error because it grandfathers in
every attribution breach it steps over; moving it back is not, because that is
strictly stricter. It needs history, so a shallow clone reports it skipped
rather than passed.

## Secrets

**This tool recommends a scanner and ships none.** A partial pattern list
presented as a gate gives false confidence, which is worse than no gate. Use
gitleaks, detect-secrets or trufflehog and commit its config — check 40 goes
quiet once it sees one.

What the standard does assert is that secret *values* never belong in the agent
contract, a skill, a template or any tracked document; the machine-readable
block holds paths and references. Keep the real file gitignored and commit a
redacted mirror whose values read `REPLACE_ME`.

Check 41 reads tracked documentation only and warns on credential-shaped
strings. It is documentation hygiene, and it never reports a repository as
clean.

## Design

The full design, the rationale for each rule, and a log of every defect found
while building it live in the design document alongside this skill.
