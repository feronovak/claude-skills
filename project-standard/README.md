# project-standard

One standard for how a project documents itself, releases, and keeps Claude out
of its git history — plus a stdlib-only checker that enforces the half a machine
can decide.

## Why it is split

Checks fall into two kinds, and conflating them produces either a slow validator
or one that cannot run in CI.

**Mechanical** — does the file exist, do its links resolve, is the endpoint
documented, does the tag match the version, is a local-only path tracked.
Decidable by string comparison; the same answer every run. 542 ms across eight
repos, no model, no tokens. Runs from CI, a hook, cron, or a shell.

**Semantic** — does the contract describe *this* project or a generic framework,
does the product map claim something the code no longer does, is a trust stamp
plausible. Nothing decides these but judgement. That half is the skill.

A validator that only exists inside a model runs when someone remembers it.
That is how nine repos ended up with nine different structures.

## Install

The tool takes no dependencies and needs no install step. Run it from anywhere:

```bash
python3 -m project_standard.cli check --repo ~/projects/apps/llm-preflight
```

To gate a repo's CI, vendor `tool/project_standard/` to
`scripts/project-standard/` and add a job (see **CI** below).

## Usage

```bash
project-standard check                    # this repo, every check
project-standard check --repo NAME        # one repo, by path or by name under ~/projects/apps
project-standard check --only version     # one concern, repeatable
project-standard check --fleet            # every git repo under ~/projects/apps
project-standard check --json             # machine-readable
project-standard check --profile=ci       # skip what a runner cannot answer

project-standard generate                 # write docs/DOCMAP.md
project-standard routes --app app:create_app   # write docs/api/routes.json
```

Exit code is non-zero on error-severity findings, so no wrapper is needed to
gate CI, a pre-push hook, or a cron.

`--only` is what makes a rule change cheap to assess: change a rule, ask one
question of every repo, ignore everything else.

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

106 tests, stdlib `unittest`, no dependencies. Fixtures build throwaway git
repos in temp directories, with `core.hooksPath` pointed at an empty directory
so the global hygiene guards never interfere — otherwise a test that
deliberately commits a Claude trailer would be blocked by the very hook the
checker is being tested for.

`test_fleet_smoke.py` runs against the real repositories and skips cleanly when
they are absent. It is the test that keeps the suite honest: every defect found
while designing this standard came from a real repo, and not one came from a
fixture. Fixtures encode what the author already believes.

## Layout

```
SKILL.md                     the orchestrator — modes, semantic checks
references/
  standard.md                artifacts, slots, taxonomy, baselines
  git-hygiene.md             the five attribution markers, the local-only set
  release-flow.md            version source, bump axis, tags, the three-way gate
templates/                   skeletons carrying TODO tokens, never plausible prose
tool/project_standard/
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

## Design

Full design, all 47 checks, and a log of every defect with what found it:
`docs/superpowers/specs/2026-08-04-project-standard-design.md`.
