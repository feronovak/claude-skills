# project-standard — design

**Date:** 2026-08-04
**Status:** approved, not implemented
**Author:** Fero Novak

## Problem

Nine projects under `~/projects/apps/` have nine different structures. A survey on
2026-08-04:

| Repo | agent contract | docs shape | changelog | version source | API reference |
|---|---|---|---|---|---|
| isitgood-auction | CLAUDE.md | `architecture/ features/ prds/ superpowers/` | none | `VERSION` **and** `package.json` | prose, unverified |
| photoinput | CLAUDE.md | `plans/ audit/ done/ superpowers/` + 4 root SCREAMING_CASE | none | `package.json` | none |
| ithinktoday | CLAUDE.md | `product/ platform/ analysis/ reference/` | none | none | none |
| pyramid-wordle | CLAUDE.md | `history/ superpowers/` | yes | `package.json` | none |
| llm-preflight | AGENTS.md | `guides/ operations/ reference/ product/` | yes | `pyproject.toml` | none |
| talealbum | none | flat SCREAMING_CASE | none | `package.json` | none |
| iplaytoday | none | flat + `sharks/` | none | `package.json` | none |
| car-trip-automation | AGENTS.md | `discovery/ prd/` | none | `package.json` | none |
| isitgood-auction-extension | none | one file | none | `package.json` | none |

Four consequences:

1. **An agent entering a repo cannot rely on anything.** Where the code map lives,
   whether the product map is current, whether an API surface is documented at all —
   each answer is per-repo folklore. Three of nine — talealbum, iplaytoday and
   isitgood-auction-extension — have no agent contract file at all, and of the six
   that do, two use `AGENTS.md` rather than `CLAUDE.md`.
2. **Documentation asserts things nobody has verified.** Only isitgood-auction
   distinguishes "a human read this against the code at vX" from "this file exists".
   Everywhere else, a doc's presence is mistaken for its accuracy.
3. **Releases have no contract.** pyramid-wordle sits at `package.json` 1.7.5 with its
   nearest reachable tag at v1.7.4 — and also carries v2.0.0, v2.1.0 and v2.2.0 tags
   from February, above the line it is now on. isitgood-auction carries two disagreeing
   version numbers. Nothing detects either.
4. **Local-only artifacts leak into GitHub by default.** Executive summaries land in
   `docs/`, which is tracked. isitgood-auction un-tracked its own by hand after the
   fact; infra's `docs/exec-summaries/` is untracked today with nothing preventing the
   next `git add -A`.

A fifth constraint is not drift but policy: **Claude must never appear as a contributor
in git.** This one is violated by *default behavior* — Claude Code's harness instructs
the agent to append `Co-Authored-By: Claude ...` to commit messages and
`🤖 Generated with Claude Code` to pull request bodies. A repo that stays silent on
attribution gets the wrong outcome automatically.

## Solution

A Claude Code skill, `project-standard`, that resolves a repo's profile from its code,
validates it against one canonical standard, and — on explicit request — scaffolds
what is missing.

The standard is harvested from isitgood-auction, which has been living roughly 80% of
it in daily use: a generated `DOCMAP.md` with per-doc trust stamps, `PROJECT_MAP.md`,
`FEATURE_MAP.md`, `DEVELOPMENT_FLOW.md`, and `scripts/ci-local.sh`. Three gaps in that
implementation are closed *in the standard itself* rather than blessed: its API surface
documents its routes in prose that nothing verifies against the code, it has no
changelog, and its local-only rule is manual.

### Why a checker and a skill, not one or the other

The checks split into two irreducibly different kinds.

**Mechanical** — does the file exist, do its links resolve, is the spec older than the
routes, is a local-only path tracked, does the tag match the version. Decidable by
string comparison, identical answer every run. Running these through a model is slow,
expensive, and occasionally inconsistent — and a validator that only exists inside a
model cannot gate CI, so it runs only when someone remembers it. That is how nine
structures happened.

**Semantic** — does the agent contract describe *this* project or a generic framework,
does the product map claim a feature that was removed, is a trust stamp plausible given
what has landed since. No amount of string comparison decides these. isitgood-auction's
trust stamps exist precisely because this call cannot be automated.

So: a vendored Python checker owns the mechanical half and can gate CI; the skill owns
the semantic half and the profile definitions.

## Architecture

```
~/projects/claude-skills/project-standard/
  SKILL.md                      orchestrator — modes, decision flow, semantic checks
  references/
    standard.md                 every artifact, what it asserts, who owns it
    profiles.md                 profile + capability detection, override syntax
    git-hygiene.md              attribution + local-only rules
    release-flow.md             version / tag / changelog contract
  templates/                    skeletons carrying TODO(project-standard) tokens,
                                never plausible-looking placeholder content
  tool/
    project_standard.py         `generate` + `check`, stdlib-only Python 3
    routes.py                   dev-time route manifest generator
    test_project_standard.py
```

Symlinked into `~/.claude/skills/` like the other skills in this repo.

The tool is **vendored** into each target repo at `scripts/project-standard/` during
setup, matching isitgood-auction's existing `scripts/docmap.py` convention. Stdlib-only
Python 3 so a Next.js repo gains no dependency and GitHub Actions' `ubuntu-latest` needs
no setup step.

Vendoring means N copies, which drift. The mitigation is the standard one: the tool
stamps its own version into everything it emits, and the skill compares that against its
canonical version and offers an update when the copy is stale.

### How the two halves are actually used

They are not one workflow run at one cadence. The fast half should run constantly and
the expensive half rarely.

| | Mechanical (`check`) | Semantic (skill) |
|---|---|---|
| Cost | 56 ms one repo, 542 ms across eight | a session, tokens |
| Needs a model | no | yes |
| Runs from | CI, a hook, cron, a shell, ad hoc | a Claude session |
| Cadence | every commit / every push | at retrofit, or when judgment is wanted |

Measured on the eight real git repos, including 500-commit log scans. Something that costs a
third of a second across the whole fleet can be pinned in CI and run on a whim; the
judgment layer cannot, and should not pretend to.

### Invocation surface

```
project-standard check                    # this repo, all checks
project-standard check --repo=NAME        # one repo by name
project-standard check --only=version     # one concern, repeatable
project-standard check --fleet            # every repo under ~/projects/apps
project-standard check --json             # machine-readable
project-standard check --profile=ci       # skip developer-machine checks, report skips
project-standard routes                   # write docs/api/routes.json from the live app
```

Exit code is non-zero on error-severity findings, so no wrapper is needed to gate CI, a
pre-push hook, or a cron.

`--only` is what makes a rule change cheap to assess: change a rule, ask one question of
every repo, ignore everything else. Asking the fleet only about version sources returns
isitgood-auction's `package.json=5.0.0` against `VERSION=0.13.2` and pyramid-wordle's
stray v2.x tags, and nothing else.

**Fleet mode is why a canonical copy exists alongside the vendored ones.** The vendored
copy validates its own repo and is what CI runs, self-contained. The canonical copy in
the skill sweeps every repo from devbox — which is how the smoke runs that found four of
this spec's defects were done.

### Two commands

- **`generate`** — writes `docs/DOCMAP.md` from the files themselves. Its output must be
  byte-deterministic: sorted, and carrying no timestamp or run date. A single
  "Generated on" line makes check 3 permanently red. isitgood-auction's `docmap.py`
  already satisfies this — verified: no `datetime`/`strftime`, seven `sorted()` calls. This is
  isitgood-auction's `docmap.py`, generalized. Without a shipped generator, the
  "generated index" requirement would be aspirational in every repo but one.
- **`check`** — mechanical validation. Exits non-zero on **error**-severity findings so
  CI can gate; warns are reported and exit zero. See [Severity](#severity).

### Three modes

- **validate** (default) — read-only. Run `check`, then apply the semantic judgment.
  Reports findings; changes nothing.
- **setup** — retrofit an existing repo. Interactive, explicit request only. Resolve
  profile → print what was detected and why → **reconcile incumbents** → show the
  complete list of files it would create, rename or merge → wait for approval → write →
  re-run `check` and show what remains.
- **init** — scaffold a new repo, before the first line of code.

### Why `init` is a mode and not a branch inside `setup`

Setup's two central mechanisms both assume a repo with history, and neither works on an
empty one.

**Detection needs code to read.** Profile and capability resolution looks for a FastAPI
app object, a `manifest.json`, a `publishConfig` block. A new repo has none, so
resolution returns nothing. `init` therefore **asks** the three questions — profile,
`http-api`, channels — and records the answers as declarations. Later `validate` runs
verify those declarations against the code as it appears, and a declaration the code
contradicts becomes check 6 like any other.

**Reconciliation is meaningless with no incumbents.** What replaces it is ordering: the
agent contract, the maps and the gitignore exist at commit 1. The local-only rule is
never retroactive, so setup's most expensive step — un-tracking files that should never
have been committed, which cannot be undone in history — simply never happens.

Greenfield is where this standard costs least and pays most.

### Reconciliation is a required setup step, not an optional one

Most repos already have documents doing a standard slot's job under another name.
photoinput carries `NORTH_STAR.md`, `IMPLEMENTATION_ROADMAP.md` and `PHASES_DETAILED.md`
at root; talealbum carries `ROADMAP.md`, `TODO.md` and `EXECUTIVE-SUMMARY.md`.

Creating `FEATURE_MAP.md` alongside `NORTH_STAR.md` leaves two documents asserting what
the product does. That is the disease this skill exists to treat, arrived at by a
different route. So setup **maps incumbents onto slots and renames or merges them**, and
only creates a file when no incumbent exists. Where reconciliation is ambiguous it asks
rather than guessing.

The checker backs this with a warn when more than one document appears to assert product
truth — matched by filename convention and by leading-heading text.

## Profiles and capabilities

A declared profile is a hand-maintained assertion, and hand-maintained assertions are
the thing this skill distrusts. So the profile is **detected from code**, with an escape
hatch that costs something.

**Profile** — one of:

| Profile | Meaning | Detection |
|---|---|---|
| `product` | shipped to users | a source tree with an entry point or deploy config |
| `library` | published to developers | `publishConfig`/`files`/`bin` in package.json, or `[project.scripts]` / build backend in pyproject.toml |
| `docs` | no product code | no source tree, predominantly markdown |

**Capabilities** — detected independently, and only these two change what is required:

- **`http-api`** — FastAPI/Flask/Django app object, `app/api/**/route.ts`,
  `pages/api/`, or Express `app.listen`. The only thing that requires an API reference —
  and the same enumeration is what endpoint coverage is diffed against.
- **`channels`** — `web` (default) · `extension` (`manifest.json` with
  `manifest_version`) · `mobile` (`android-native/`, Capacitor config) · `desktop`
  (`src-tauri/`, Electron config).

  **`extension` is exclusive; `mobile` and `desktop` compose with `web`.** Precedence is
  explicit: if `extension` is detected, `web` is suppressed even when a `src/` tree is
  present — an extension's source looks exactly like a web app's.
 A browser
  extension has a source tree that looks like a web app but ships through a store as one
  artifact, so detecting it as `web+extension` would arm two release gates where only one
  release exists — and the phantom gate can never pass. pyramid-wordle genuinely is
  `web+mobile+desktop` and genuinely needs three.

Resolved for the current fleet:

| Repo | profile | http-api | channels |
|---|---|---|---|
| isitgood-auction | product | yes | web |
| talealbum | product | yes | web |
| photoinput | product | no | web |
| pyramid-wordle | product | no | web, mobile, desktop |
| iplaytoday | product | not surveyed | web |
| ithinktoday | product | not surveyed | web |
| car-trip-automation | product | not surveyed | web |
| isitgood-auction-extension | product | no | extension |
| llm-preflight | library | no | — |
| infra | docs | no | — |

**Override.** An agent contract may pin a profile or capability, and **must state why**:

```
profile: product
http-api: no — the app/api/ directory is Auth.js callbacks only, no public surface
```

The checker reports both detected and declared values and raises a mismatch as a
finding rather than deferring silently. Requiring a written reason is what keeps the
escape hatch from becoming the default.

**Rejected: a single profile name doing both jobs.** An earlier draft used five profile
names (`webapp`/`service`/`client`/`library`/`docs`). It filed photoinput and
pyramid-wordle — two shipped consumer web products — under `client` alongside a browser
extension, purely because none of them serve HTTP. Splitting "what is this" from "what
does it expose" is both simpler and accurate.

## Required artifacts

| Artifact | product | library | docs | What it asserts |
|---|:-:|:-:|:-:|---|
| agent contract | ✅ | ✅ | ✅ | what this repo is, how to run it, its rules |
| `README.md` | ✅ | ✅ | ✅ | human entry point |
| `docs/DOCMAP.md` | ✅ | ✅ | ✅ | **generated** index of every doc + trust stamps |
| `docs/PROJECT_MAP.md` | ✅ | ✅ | — | map of code — where things live |
| `docs/FEATURE_MAP.md` | ✅ | ✅ | — | map of product; for a library, its public interface |
| `docs/API_REFERENCE.md` | if `http-api` | if `http-api` | — | every endpoint, understandable cold by a person or a model |
| direction doc | ✅ | warn | — | mission, vision, north star — why it exists and where it is going |
| `docs/NEXT_STEPS.md` | ✅ | ✅ | — | the single roadmap — what is open and what is next |
| `docs/DEVELOPMENT_FLOW.md` | ✅ | ✅ | — | how work becomes a release, for this product |
| `CHANGELOG.md` | ✅ | ✅ | — | Keep a Changelog, hand-written |
| gitignore local-only block | ✅ | ✅ | ✅ | supporting files stay off GitHub |
| local-only opt-in marker | ✅ | ✅ | ✅ | arms the global guard for this repo |
| `CONTRIBUTING.md` `SECURITY.md` | — | ✅ | — | third-party contribution surface |

**Agent contract** — satisfied by `CLAUDE.md` **or** `AGENTS.md`, same content rules
either way. llm-preflight and car-trip-automation use `AGENTS.md` deliberately;
llm-preflight also carries `.agents/` and `.codex/`, so hardcoding `CLAUDE.md` would
break a repo that is tool-neutral on purpose. If both files exist, one must be a pointer
to the other. Required sections: what the repo is; how to run, test and build it; the
git-hygiene rules stated explicitly; a pointer to `DOCMAP.md`.

**`RELEASING.md` satisfies the release-flow slot.** An earlier draft required both it and
`DEVELOPMENT_FLOW.md` for libraries — two mandated documents answering one question, which
is the disease this skill treats. llm-preflight's `RELEASING.md` already *is* a
step-by-step account of how work becomes a release. The slot is the concept; either
filename satisfies it, and a repo carrying both must make one a pointer.

### Contract grammar

Everything a check must read out of the agent contract lives in **one fenced `yaml` block
under a `## project-standard` heading**. Prose is for humans; this block is the machine
interface, and it is the only part the checker parses.

````markdown
## project-standard

```yaml
adopted: 4f3a91c              # baseline commit; attribution errors start here
profile: product              # omit unless overriding detection
http-api: no                  # omit unless overriding detection
  reason: app/api/ is Auth.js callbacks only, no public surface
channels: [web, mobile]       # omit unless overriding detection
direction: docs/NORTH_STAR.md # which file holds mission/vision/north star
prds: docs/prds/              # or `local` for a public repo keeping them out of git
critical-paths:               # may be empty, may not be absent
  - services/verdict/
  - services/scoring/
```
````

Without this, checks 2, 6, 8, 20, 30, 32 and 37 have nothing deterministic to read — an
earlier draft left the encoding unstated and scattered YAML-ish fragments through prose,
which made the entire contract-reading half of the checker unimplementable. Any override
key carrying a `reason` requires it to be non-empty.

The rule for what goes in the block: **if a check reads it, it is a key.** If only a human
reads it, it stays prose.

### Direction: mission, vision, north star

Three concepts, one slot, flexible filenames:

| Concept | Answers |
|---|---|
| **mission** | why this exists, and who for |
| **vision** | where it is going — the state being built toward |
| **north star** | the one metric or principle a decision is judged against |

**Satisfied by `docs/NORTH_STAR.md` carrying all three, or by separate files
(`MISSION.md`, `VISION.md`, `NORTH_STAR.md`) — any split is fine, but each concept is
stated in exactly one place.** photoinput already has a `NORTH_STAR.md`; the slot is named
for the concept, not the filename, exactly as the agent contract accepts `CLAUDE.md` or
`AGENTS.md`.

**The boundary against `README.md` matters, or this becomes duplication.** The README says
what the project is and how to run it — the operational entry point. The direction doc
says why it deserves to exist and what it is becoming. A README that already carries a
mission paragraph should have it moved, not copied.

**Required for `product`, a warn for `library`.** A published tool's README usually
carries its purpose adequately, and demanding a vision statement for a CLI would produce
ceremony rather than clarity. A product without a stated north star is a different
problem: every scoping argument reopens from scratch.

Nothing derives this. It is the purest judgment artifact in the standard, so `setup` asks
and never drafts. Which file holds the slot is named by `direction:` in the contract, so
the check reads a key rather than guessing across an open set of filenames.

**A repo may inherit direction from a parent product.** isitgood-auction-extension is a
companion to isitgood-auction and has no separate mission; demanding its own vision
statement would manufacture ceremony and, worse, a second place where the product's
direction is stated. The contract declares `direction: ../isitgood-auction/docs/NORTH_STAR.md`
or `direction: inherit` with the parent named, and check 30 is satisfied.

This is the standard's answer to proportionality generally: a companion repo carries the
artifacts describing *itself* — its code map, its API surface, its changelog — and points
at the parent for everything the product answers once.

### `NEXT_STEPS.md` is the single roadmap

**Exactly one file holds open work.** A repo may carry as many complementary documents as
it likes — vision, strategy, specs, PRDs, architecture — but only one may answer "what is
next". Two roadmaps disagreeing is worse than none, because both look authoritative and
nobody can tell which is current.

The fleet shows why the rule is needed: photoinput carries three forward documents
(`docs/NEXT_STEPS.md`, `IMPLEMENTATION_ROADMAP.md`, `NORTH_STAR.md`) and talealbum two
(`docs/ROADMAP.md`, `docs/TODO.md`).

| Kind | Role | Allowed alongside? |
|---|---|---|
| `docs/NEXT_STEPS.md` | the ordered open backlog | **the only one** |
| direction doc (`NORTH_STAR.md`, …) | why the product exists, where it is going | ✅ — and it **owns** direction |
| specs, PRDs, architecture | what a thing is and how it works | ✅ |
| `ROADMAP.md`, `TODO.md`, `BACKLOG.md`, `PLAN.md`, `IMPLEMENTATION_ROADMAP.md` | a second ordered open backlog | ❌ — merge into `NEXT_STEPS.md` |

The boundary is whether the document carries an **ordered list of open work**. A vision
doc saying "we are going after resale sellers next year" is direction and stays. A file
listing the next six things to build is a roadmap and must be the one roadmap.

**Direction moves out.** With a direction document in the standard, `NEXT_STEPS.md` holds
the ordered open backlog and links to it rather than restating it. Two files describing
where the product is going is the same duplication this rule exists to stop — the
direction slot wins because a north star outlives any particular backlog.
isitgood-auction's file currently carries both and reconciles by keeping the backlog and
pointing at direction.

**Future-only.** Completed work lives in `CHANGELOG.md` and git history. Done rows are
deleted, not struck through and kept — a roadmap that accumulates finished items is a
changelog in disguise, and it drifts the moment the two disagree. isitgood-auction's file
already states the rule in its own header: *"nothing that's already done."*

### PRDs: intent for features that do not exist yet

A PRD is the depth behind one future feature. It is not the backlog, and it is not state.

**The taxonomy this completes** — five documents, five questions, no overlap:

| Document | Answers | Tense |
|---|---|---|
| direction doc | why this exists, where it is going | timeless |
| `docs/NEXT_STEPS.md` | what is open, in what order | future, one line each |
| `docs/prds/<feature>.md` | what one future feature must do, in depth | future, one per feature |
| `docs/FEATURE_MAP.md` | what the product does today | present |
| `CHANGELOG.md` | what shipped, and when | past |

A backlog line graduates into a PRD when someone starts designing it. The PRD never
graduates into `FEATURE_MAP.md` — the map is written from the code that shipped, not
from the document that proposed it.

**Structure:**

```
docs/prds/
  README.md                index — one line per PRD with its status
  <feature-slug>.md        one PRD per feature, kebab-case
  archived/v<X.Y.Z>/       shipped or dropped, moved here on release
```

`docs/prds/` is canonical. isitgood-auction's root `PRDs/` and car-trip-automation's
`docs/prd/` both rename into it; the version-archive idea is isitgood-auction's and is
kept, because it answers "what did we intend at 2.6" without cluttering what is live.

**Required header:**

```
**Status:** draft | accepted | building | shipped v1.2.0 | dropped
**Backlog:** <link to the NEXT_STEPS item>
**Owner:** <who decides>
```

**Required sections:** Problem (who hurts, and the evidence) · Outcome (what changes for
the user, and how it is measured) · Scope (in, and explicitly out) · Behaviour (the
feature as the user experiences it) · Constraints and risks · Open questions.

**A PRD is intent, never state.** `FEATURE_MAP.md` is the only authority on what exists,
and every PRD header says so. car-trip-automation's `docs/prd/implementation-status.md` is
exactly this confusion — a state document living among intent documents, where it will be
read as current and will drift. It merges into `FEATURE_MAP.md`.

**Shipped PRDs are kept, not deleted.** This is the opposite of the roadmap rule, and
deliberately: a backlog row that is done is noise, but a PRD records *why* a feature is
the shape it is, which stays useful long after it ships. On release it moves to
`archived/v<version>/`.

**Tracked by default; local-only is a declarable choice.** A public repository may keep
PRDs out of git — llm-preflight gitignores `PRD-*.md` because publishing internal product
plans alongside an open-source tool serves nobody. That choice is stated in the agent
contract with its reason, exactly like a profile override, so it reads as a decision
rather than an omission.

**The same applies to the backlog.** llm-preflight also gitignores a 28 KB `ROADMAP.md`,
and the reasoning is identical: an open-source tool's public repo is not where internal
prioritisation belongs. `NEXT_STEPS.md` may therefore be declared local for a public
repo. It is still required to exist — the checker verifies it on the developer's machine
and skips it under `--profile=ci`, the same way it treats anything a runner cannot see.

**PRDs are not a required artifact.** A repo may legitimately have none. The structure is
enforced when PRDs exist, not conjured as an empty directory.

### Agent rules

Model tiering is global policy and stays in exactly one place — `~/.claude/agents/`,
which today holds:

| Agent | Model | Role |
|---|---|---|
| `scout` | haiku | a single known fact, in a file already known |
| `explorer` | sonnet | read-only breadth across many files |
| `builder` | sonnet | mechanical implementation, tests, fixtures, docs |
| `reviewer` | opus | adversarial pre-merge review, once per batch |
| `consultant` | fable | the hard kernel — one dispatch |

The main session stays Opus. **The standard does not copy this into any repo.** Nine
copies of a tiering table is the duplicate-source-of-truth failure the skill exists to
prevent, arrived at from the other direction.

What each repo declares instead is the one thing that genuinely varies: **its
correctness-critical paths** — where a wrong call ships a fabricated result. This
declaration lives in the agent contract and is what arms the fable review:

```
critical-paths:
  - services/verdict/        a wrong gate tells a buyer a bad listing is clean
  - services/scoring/        every downstream number derives from these
```

**The fable trigger is risk, not size.** A size threshold — files or lines changed —
would summon the premium tier for a large mechanical rename, and fable is reserved for
roughly 5% of work. A diff touching a declared critical path is what warrants it. Size
may act as a secondary trigger only with a high floor.

A repo declaring no critical paths is a legitimate answer, not a gap: pyramid-wordle
guesses words, and no path in it can fabricate a result a person will act on.

### `.claude/` is split, not wholesale ignored

| Path | Disposition | Why |
|---|---|---|
| `.claude/agents/` | tracked | project-specific agents are project knowledge |
| `.claude/skills/` | tracked | pyramid-wordle already tracks two, correctly |
| `.claude/settings.local.json` | local-only | machine-local state — photoinput's is 20KB |
| `.claude/worktrees/` | local-only | ephemeral checkouts |
| `.claude/scheduled_tasks.lock` | local-only | runtime lock |

Today `.claude/` is untracked everywhere except pyramid-wordle's two skills — by luck
rather than by rule, so the useful half is lost along with the noise.

### The API surface: coverage is mandatory, OpenAPI is not

**The requirement is that every endpoint is understandable — by a person and by a model
reading the repo cold. It is not that the file is OpenAPI.**

An earlier draft mandated `docs/api/openapi.yaml`. That confused a format with an
outcome, and the format is expensive in exactly the place it matters: isitgood-auction
is **Flask 3.1.3**, which has no native emitter, so a spec there means adding
`flask-smorest`/`apispec` and annotating a live API, or hand-maintaining YAML. Meanwhile
isitgood-auction already has `docs/API_REFERENCE.md` describing its routes in prose —
which the OpenAPI mandate classed as a gap, when it is in fact the thing the requirement
was asking for.

**Required:** `docs/API_REFERENCE.md`, covering every route the code exposes. Per
endpoint:

| Field | Why |
|---|---|
| `METHOD /path` | the canonical identifier, and what coverage is matched on |
| purpose | one line — what a caller uses it for |
| parameters | name, type, required or not |
| auth | what a caller must present, or none |
| response shape | what comes back on success |
| errors | the failure modes a caller must handle |

**The format rule accepts what good documentation already looks like.** An endpoint may
be declared as inline text (`GET /api/me`), as a markdown table row with the method and
path in separate cells (`| GET·POST | \`/api/me/hunts\` | …`), or as a heading. Combined
methods (`GET·POST`, `PATCH·DELETE`) count as one entry per method, and backticks are
stripped before matching.

An earlier draft required a literal adjacent `METHOD /path`. isitgood-auction's
`API_REFERENCE.md` — a table carrying method, path, auth, purpose and response shape for
55 endpoints, the best API document in the fleet — fails that rule outright, and would
have been told to rewrite itself into a worse format to satisfy a parser. A standard that
does that to its best incumbent is wrong about the standard, not about the incumbent.

**OpenAPI is an accepted, encouraged way to satisfy this — never a second document.**
Where the framework emits it free (FastAPI natively, a Next.js route tree by walking),
generate it and render `API_REFERENCE.md` from it; a generated spec cannot drift. Where
it does not (Flask, Express), write the reference directly. A repo that has both must
generate one from the other, never maintain two.

### Coverage, not presence

Requiring the file only proves a file exists. The failure that actually happens is an
endpoint shipping undocumented, so the check enumerates routes from the code and diffs
them against the documented set.

**Enumeration must come from the framework, not from scraping decorators.**

| Stack | Source of truth | Reliable statically? |
|---|---|---|
| Next.js | filesystem walk of `app/api/**/route.ts` + exported method names | **yes** |
| Flask | `app.url_map` at dev time, committed as a route manifest | no — see below |
| FastAPI | `app.routes` / the generated spec, committed | no |
| Express | `app.get(...)` / `router.post(...)` literals | partially |

A Flask decorator's path is relative to its blueprint, and blueprints nest — the real
path is composed at `register_blueprint` time, across modules. isitgood-auction registers
seven sub-blueprints under an admin blueprint alone. Regex over decorators produced 107
phantom routes there, against a document that correctly describes 55; that is a validator
crying wolf, and it would be switched off within a day.

So Flask and FastAPI enumerate at dev time from the live app object and commit the
result, exactly as generated specs do. CI diffs the document against the committed
manifest and never re-derives it.

**The manifest is concrete, not a hand-wave.** `docs/api/routes.json`, written by
`project-standard routes` — which imports the app the way the project's own entrypoint
does, walks `app.url_map` (Flask) or `app.routes` (FastAPI), and emits sorted JSON:

```json
{"generated_by": "project-standard 0.1.0",
 "routes": [{"method": "POST", "path": "/api/vet"}, {"method": "GET", "path": "/api/me"}]}
```

Sorted and version-stamped so it diffs cleanly, and committed. Check 10c compares its
last-commit timestamp against the route files'. Without naming the file, the format and
the command, check 10c depends on an artifact nothing produces.

**Where enumeration cannot be resolved, warn — never error.** A checker that cannot
enumerate must say so and report the documented count, rather than inventing findings
from a partial parse.

| Finding | Severity |
| a route in the enumeration with no entry in the reference | **error** |
| an entry in the reference matching no enumerated route | **error** — it documents something that no longer exists |
| enumeration unavailable for this stack | warn, with the documented count |
| coverage summary (`N/M` endpoints documented) | reported always |

This is deterministic, needs no model, and is a far stronger guarantee than the presence
check it replaces. talealbum has 36 endpoints and no API document at all; car-trip-automation 61,
iplaytoday 7.
Under presence-checking both are one file away from green while every endpoint stays
undocumented.

Where a generated spec exists, freshness is additionally checked against **last-commit
timestamps**, never mtimes:

```
git log -1 --format=%ct -- docs/api/openapi.yaml   vs   the same for each route file
```

Git does not store mtimes. A fresh clone stamps every file with the checkout time, so
an mtime comparison in CI passes or fails at random depending on filesystem write order.
This applies anywhere the standard compares document age to code age.

**Trust stamps.** Every file under `docs/` carries:

```
**Last reviewed:** YYYY-MM-DD · **As of:** vX.Y.Z
```

A stamp means one thing: someone read this document against the code at that version.
It is never applied in bulk. `DOCMAP.md` reports an unstamped doc as `unstamped` rather
than filling in something plausible. This is isitgood-auction's rule, kept verbatim.
Infra's existing `Last reviewed:` convention is the same idea and stays compatible.

**An unstamped doc is a metric, never a failure.** isitgood-auction has ~150 documents
and virtually none carry a stamp today. If missing stamps failed the build, its first CI
run would report 150 errors and the gate would be switched off within a day — and
stamping 150 docs would become a precondition for adopting the standard at all instead
of something that happens as each doc is next read. The checker reports the stamped
fraction and exits zero.

## Authoring: how a missing artifact gets written

Detection is the cheap half. Everything above decides whether a document is *missing*;
this section decides what gets written in its place, and it is the half that determines
whether the standard produces documentation or just files.

**The governing rule: scaffolding never fabricates.** A template that drops a
plausible-looking `FEATURE_MAP.md` into a repo produces a document that passes the
presence check, gets indexed by `DOCMAP.md`, and asserts nothing true — which is strictly
worse than the missing file, because a reader coming in cold now believes it. That is the
same failure the whole skill exists to prevent, manufactured by the tool meant to prevent
it.

So every artifact has an authoring contract: what it asserts, where its content legally
comes from, what `setup` must ask when the answer is judgment rather than code, and what
distinguishes finished from skeletal.

### Derivation sources

| Artifact | Content comes from | Auto-draftable |
|---|---|---|
| `PROJECT_MAP.md` | directory tree, entry points, package scripts | mostly |
| `API_REFERENCE.md` | route enumeration for the skeleton; the handler for each endpoint's substance | skeleton only |
| `CHANGELOG.md` | `git log` since the earliest tag, as a seed to edit down | seed only |
| agent contract | run/test/build from package scripts or Makefile; the rest asked | partly |
| `DEVELOPMENT_FLOW.md` | standard boilerplate; this product's bump and milestone meanings asked | partly |
| `FEATURE_MAP.md` | what the product does today | **no** |

### Per-artifact contracts

**`PROJECT_MAP.md`** — asserts where each kind of code lives and what each area is
responsible for. Drafted from the tree; every top-level source directory gets a purpose
line. Done when no line names a path that does not resolve — which is mechanically
checkable, and therefore is a check.

**`FEATURE_MAP.md`** — asserts what the product does today and the state of each feature.
**Nothing derives this.** Routes, UI entry points and test names suggest *candidates*;
whether a candidate is live, partial or abandoned is judgment that requires reading the
code. `setup` scaffolds a list of candidates each marked `unverified`, never a list of
claims, and works through them with the user. Done when every claim traces to code
someone read, and nothing listed is unreachable.

**`API_REFERENCE.md`** — skeleton generated from the route enumeration, one row per
endpoint, all six fields empty. Purpose, auth, parameters, response shape and errors come
from reading each handler. Done when coverage is 100% and no field is blank. For
talealbum's 36 endpoints and car-trip-automation's 61, the skeleton is free and the substance
is the work.

**Direction doc** — asserts why the product exists, where it is going, and what a
decision is judged against. Nothing derives it; `setup` asks the three questions and
writes what it is told, never a draft. Done when a reader can say what this product is
for without reading any code, and no other file restates it.

**PRDs** — assert what one future feature must do. Not derivable; a PRD is a product
decision. `setup` does not write PRDs, it only normalises existing ones into
`docs/prds/`, adds the missing `Status:` headers, and reports which sections are absent.
Done when every PRD carries a status and no PRD asserts current behaviour.

**`NEXT_STEPS.md`** — asserts what is open, as an ordered backlog, opening with a link to
the direction doc rather than restating it. Not derivable: open work is intent, and no
amount of reading code produces it. `setup` seeds it by merging any existing roadmap, TODO
or backlog file. It does **not** ask for direction here — that belongs to the direction
slot, and asking twice is how the duplication check 31 exists to catch gets written by the
tool itself. Done when it carries no completed items and no second backlog file survives
beside it.

**`DEVELOPMENT_FLOW.md`** — mostly boilerplate; the bump axis comes from the standard.
What must be asked: **who this product's consumer is** and what breaking them looks like,
what its milestone versions mean, and its release channels. Done when the bump table names
a real consumer rather than restating generic semver.

**Agent contract** — run, test and build commands derive from package scripts or the
Makefile. What must be asked: what this repo is in a paragraph, its `critical-paths`, and
the reason for any profile override. Done when it names real modules and real commands and
carries no generic framework prose.

**`CHANGELOG.md`** — seeded from `git log` grouped by tag, then edited to reader-facing
lines. **Retrofit does not invent history.** Where tags do not reach back far enough, the
file starts at the current version and says so; it never reconstructs releases that were
never cut. pyramid-wordle and llm-preflight already show the target quality.

### Scaffolded is a distinct state, and it is not green

Templates mark every unwritten field with one literal token:

```
<!-- TODO(project-standard): <what is needed here> -->
```

- A required document containing that token is an **error**. Without this, `setup` can
  take a repo from six errors to zero while nothing true has been written, and the whole
  standard degrades into box-ticking.
- A scaffolded document carries `**Status:** scaffolded` in place of a trust stamp. It is
  never stamped by the tool that created it.
- `DOCMAP.md` reports three distinct states — `stamped`, `unstamped`, `scaffolded` — and
  never lets the third pass for the second.

**`setup` therefore does not make a repo green, and says so when it finishes.** It
converts unknown gaps into an explicit, ordered worklist with the mechanical parts already
filled in. Claiming otherwise would be the same dishonesty the trust stamps exist to
prevent.

## Release flow

**One version source per repo, chosen by ecosystem** — not a `VERSION` file:

| Ecosystem | Source |
|---|---|
| npm only | `package.json` `version` |
| Python only | `pyproject.toml` `[project] version` |
| **polyglot** | the source the release tags agree with; ties broken by the backend |
| neither | a `VERSION` file at root |

**Polyglot repos need the tie-break, and the motivating example is one.** isitgood-auction
is Flask plus an npm frontend: `package.json` reads 5.0.0, `VERSION` and every tag read
0.13.2. A flat "npm wins" rule deterministically selects 5.0.0 — the number that agrees
with nothing — and would report the product as four majors ahead of its own releases. The
version source is whichever file the tags corroborate; where nothing corroborates, the
backend's manifest wins and the frontend's `version` field is declared decorative in the
contract.

An earlier draft mandated a `VERSION` file everywhere. That is wrong: in an npm or PyPI
project it *creates* a second source of truth, which is the drift the skill exists to
kill. isitgood-auction demonstrates the failure today — `VERSION`/tag say 0.13.2 while
`package.json` says 5.0.0. Under this standard that disagreement is a finding it must
resolve.

### What a bump means

**The standard fixes the axis; each product names its consumer.** Semver only asks one
question — *does this break whoever depends on us* — and the answer depends entirely on
who that is. That is the part a project must state, and the only part.

| Profile | The consumer | A **major** bump is |
|---|---|---|
| `library` | code that imports it | a signature or behaviour change requiring callers to adapt |
| `product` with `http-api` | callers of the API | a request or response contract change |
| `product`, no API | the user | the product's promise changes — what it tells them, or what it is for |

- **major** — the consumer above must adapt.
- **minor** — new capability, or a change to what the consumer is told, that does not
  require them to adapt.
- **patch** — fixes and internals the consumer cannot observe.

isitgood-auction already states exactly this shape ("the verdict contract changes in a way
a caller must adapt to, or the product's promise changes"), and it is generalised here
rather than invented.

**Pre-1.0.** Below 1.0, minor absorbs breaking changes — `0.9 → 0.10` is a normal bump
and skips no gate. 1.0 is a **quality** milestone, declared once in `DEVELOPMENT_FLOW.md`
and not spent early. Milestone meanings are stated once and honoured; a version is never
bumped to make a launch sound larger.

**Versions never go backwards on a channel.** pyramid-wordle carries v2.0.0–v2.2.0 from
February and a current v1.7.x line, which is why tag resolution is by ancestry — but the
underlying renumbering is itself the failure this rule names.

**Multi-channel lines move independently, and a tag says which channel it is.** A fix
shipping to web as 1.7.4 and to Android as 1.7.5 is normal, not drift. Single-channel
repos tag `v<semver>`; multi-channel repos tag `<channel>/v<semver>`:

```
v1.7.4                 single channel
web/v1.7.4             multi-channel
android/v1.7.5
```

Without a convention, "per channel" gating and "lower than an earlier release on the same
channel" are both undecidable — an earlier draft specified both while leaving tags with no
channel at all.

**A repo with `channels` declared but untagged-by-channel is a warn, not an error.**
pyramid-wordle is exactly this today, and retagging released history is not something a
validator should demand. New tags adopt the convention; old ones are read as `web`.

**Pre-release suffixes** (`v1.5.0-pre-mobile`) are cuts of the same base version. The
version source must agree on the base; no changelog section is required, because nothing
was released.

**The three-way gate.** The three are the tag, the version source and the changelog.
When `HEAD` carries a tag matching `v<semver>` (or `<channel>/v<semver>`):

1. the version source reads `X.Y.Z`, **and**
2. `CHANGELOG.md` has an `X.Y.Z` section

Checkable in a second, no model involved. It catches the failure that actually happens —
a release tagged with no changelog entry, or a version bumped without a tag.

**Tag resolution is by ancestry, never by sorting.** "The latest tag" means
`git describe --tags --abbrev=0` — the nearest tag reachable from `HEAD`. It does not
mean the highest semver in `refs/tags`.

pyramid-wordle is why. It carries v2.0.0, v2.1.0 and v2.2.0 created 2026-02-17, then
renumbered downward to the v1.7.x line in July; `package.json` reads 1.7.5 and the
nearest reachable tag is v1.7.4. A checker resolving "latest" by sorting reads v2.2.0
and reports a three-major-version discrepancy that does not exist. Resolving by
ancestry reads v1.7.4 and is right.

Because that trap will bite other tooling too, a tag sorting above the current version
is reported as a **warn**, not silently ignored.

**Tag shapes the gate does not evaluate:**

| Situation | Behavior |
|---|---|
| `HEAD` carries no tag | gate not evaluated — the normal state between releases |
| tag does not match `v<semver>` | ignored for the gate |
| pre-release suffix, e.g. `v1.5.0-pre-mobile` | recognized as a release of `1.5.0`; version source must agree, changelog section **not** required |

photoinput's only tag is `v1.5.0-pre-mobile`, so without the third row the gate would
demand a changelog section for a pre-release cut.

**Multi-channel repos gate per channel.** pyramid-wordle ships web, Android and desktop,
and its changelog opens with "Android release carrying the input fix that shipped to web
on 2026-07-29 under 1.7.4." A single-number release contract cannot describe that.
Multi-channel repos state per-channel version in `DEVELOPMENT_FLOW.md` and each channel
is gated separately.

**Changelog stays hand-written.** Keep a Changelog, `## [Unreleased]` accumulating as
work lands. This is the one place the standard rejects generation. A changelog cannot
drift the way a product map can: it is append-only and version-scoped, so a 2026-07
entry describing 1.7.5 stays true regardless of what the code does next — the anti-drift
argument that justifies generating `DOCMAP.md` simply does not apply. Generating from
conventional commits would turn pyramid-wordle's "keys dropped when typing fast" into
"fix(input): handleKey closure", and would emit every `chore:` as product news. What
closes the real gap is the three-way gate above, not generation.

## Git hygiene

Both rules are violated by default behavior, not by carelessness. Neither can be
enforced by silence.

**The two rules have different scopes, and conflating them over-reaches.**

| Rule | Scope | Why |
|---|---|---|
| No Claude attribution | every repo, unconditionally | personal policy, true everywhere, no repo has a legitimate reason to want the trailer |
| Local-only paths stay untracked | only repos that opted in | `logs/` and `test_results/` are legitimately tracked in some repos, including employer work |

Opt-in is detected, not declared: the repo carries the local-only gitignore block, or
the vendored checker. A guard that blocks `logs/` in every repo the user touches will be
disabled wholesale the first time it blocks a legitimate commit, taking the attribution
rule down with it.

**No Claude attribution — and there are four markers, not one.** Claude Code's harness
appends several independently, so blocking the trailer alone leaves the rule half-enforced.

| Marker | Where | Guard |
|---|---|---|
| `Co-Authored-By: Claude …` | commit message | `commit-msg` |
| `Claude-Session: https://claude.ai/code/…` | commit message, **separate from the trailer** | `commit-msg` |
| `Signed-off-by:` naming Claude or Anthropic | commit message | `commit-msg` |
| author / committer identity | commit metadata — **invisible to `commit-msg`** | `pre-commit`, via `git var` |
| `🤖 Generated with Claude Code` | **pull request body** | **no git-side guard exists** |

The session line is the one that actually got through: photoinput carries three in its
last 200 commits, and a message stripped of its trailer but keeping that line still names
Claude. Identity has to be checked in `pre-commit` because `commit-msg` receives only the
message file.

**The PR-body rule has no mechanical enforcement and the spec does not pretend otherwise.**
Git hooks never see pull request bodies. It is a semantic check when the skill runs, and
a convention otherwise. Claiming a guard that does not exist would be the failure mode
this whole standard is built against.

### The guards ship with the tool and are installed, never assumed

An earlier draft vendored a `pre-commit` hook into each repo. That mechanism cannot fire
here: `core.hooksPath` is set globally, and when it is set git ignores every repo's own
`.git/hooks` entirely. The design would have installed one dead file per repo, and the
check that confirmed the file existed would have reported green.

| | Where | Scope |
|---|---|---|
| `commit-msg` | shipped in the tool, installed by `install-hooks` | attribution |
| `pre-commit` | same | author and committer identity |

**The guards do not scan for secrets.** Secret scanning is a separate concern
with mature dedicated tools, and a half-hearted pattern list inside this hook
would give false confidence. An earlier draft bundled one; shipping it would
have implied a guarantee the tool cannot make.

**Attribution must be `commit-msg`, not `pre-commit`.** The commit message does not exist
when `pre-commit` runs, and the trailer lives in the message. A pre-commit implementation
of this rule cannot work at all, regardless of where it is installed.

The guards are version controlled with the tool, so an edit is diffable and
revertible, and they are installed by an explicit command rather than assumed
to exist. A check that demands guards a user has no way to obtain fails every
first run.

**A repo opts into the local-only guard**, by carrying `# project-standard: local-only`
in its `.gitignore` or the vendored checker in `scripts/project-standard/`. The
attribution guard is not opt-in.

**Local-only supporting files.** These are gitignored and hook-blocked:

```
docs/exec-summaries/   session-notes/   logs/   test_results/
.agenthub/   .playwright-mcp/   .interface-design/   .cursor/   .ruff_cache/
.claude/settings.local.json   .claude/worktrees/   .claude/scheduled_tasks.lock
```

**Plus content patterns, because exact paths miss the case that actually happens.**
talealbum tracks `docs/EXECUTIVE-SUMMARY.md` today — an executive summary on GitHub,
matching no path in the list, while the problem statement names exactly that failure.
Exact paths catch the directory convention; a summary written outside it needs a pattern:

```
**/EXEC*SUMMAR*      **/*-exec-summary*      **/SESSION-NOTES*
```

Pattern matches are **warns**, not errors: a filename resembling an executive summary is
a strong hint, not proof. Reconciliation moves genuine ones into `docs/exec-summaries/`.

These stay **tracked**: `docs/superpowers/` (specs and retrospectives are real
documentation), the dated `think-day-*/` and `dev-day-*/` directories (deliberate
historical snapshots, already committed in three repos), and `.claude/agents/` plus
`.claude/skills/` (project knowledge — see [`.claude/` is split](#claude-is-split-not-wholesale-ignored)).

**Auditing what already happened — and why attribution needs a baseline.**

A smoke run across the seven git repos under `~/projects/apps` on 2026-08-04:

```
photoinput 441 · isitgood-auction 405 · talealbum 231 · pyramid-wordle 141 · iplaytoday 44
```

1,262 Claude trailers, all in commits reachable from `HEAD`. An earlier draft called any
trailer in a tracked commit an error while also placing history rewriting out of scope —
which left six of eight repos permanently red with no action inside the standard able
to change it. A gate nobody can pass is a gate that gets switched off.

So adoption sets a **baseline**: the commit at which the repo adopted the standard,
recorded in the agent contract.

| Situation | Severity |
|---|---|
| trailer in a commit after the baseline | **error** |
| trailer in a commit before the baseline | warn, with a count |
| trailer only in unreachable history | warn |
| tracked local-only path, any time | **error** — fixable by un-tracking, no rewrite needed |

The rule then binds going forward, which is what it was for. Un-tracking a file does not
erase it from history, and rewriting history across eight repos to remove executive
summaries and trailers is a large, disruptive operation in service of tidiness rather
than a leak. Secrets are a different matter and belong to `secrets-audit`, not to this
skill.

**A repo with no git at all is refused, not passed.** `ithinktoday` has no `.git`, so
every git-derived check is inapplicable. The checker exits with a clear message and offers
`git init` rather than reporting a repo as conformant on checks that never ran.

## Checks

### Severity

Two levels, because a validator that fails on everything gets switched off.

- **error** — exits non-zero, gates CI. Something is broken or contradicts itself.
- **warn** — reported, exits zero. Something is worth knowing and is not a defect: a
  gradual retrofit in progress, or a fact about the repo the reader should have.

**Adoption is gated by baselines, not by finishing the work.** An earlier draft promised
a green `check` "in one sitting" while making undocumented endpoints, unresolved TODO
tokens and a missing north star all errors — judgment work measured in days. Both could
not be true. For talealbum (36 endpoints), car-trip-automation (61) and photoinput, the
honest estimate is 2–4 days each; for llm-preflight, the easiest, 5–8 hours.

So the promise is narrower and actually keepable: **a repo reaches green in one sitting
once its baselines are declared, and the baselines only ever ratchet down.**

| Baseline | Declared in | Effect |
|---|---|---|
| `adopted` | contract | attribution errors apply to commits after it |
| `api-coverage` | contract | endpoints documented at adoption; below it is an error, above is progress |
| `scaffold` | contract | required docs still holding TODO tokens at adoption |

A baseline may never rise. Documenting six more endpoints lowers the coverage debt
permanently; a later commit that drops back below the recorded figure is an error. This is
the same mechanism the attribution rule already used, generalised — and it is what lets a
repo adopt the standard on day one and pay the documentation debt down over weeks without
a permanently red gate.

Everything that cannot be fixed in one sitting and has no baseline — stamping 150
documents, rewriting history — stays a warn. Without this, isitgood-auction's first run
reports ~150 failures and the gate does not survive the week.

**Link validation is scoped, not blanket.** Only links *inside* the standard-required
documents are errors. Links anywhere else under `docs/` are warns until the repo opts
into full link enforcement in its agent contract.

The unscoped version would sink adoption by the same mechanism the severity split
prevents elsewhere. isitgood-auction has had link tooling for months; nobody else has
ever run one. A first run against talealbum that returns forty broken links in documents
the standard did not ask for is a red gate on day one, and a red gate that is not
actionable in a sitting gets switched off.

### What the checks look at

Two scoping rules, both previously unstated, and both of which change results on the real
fleet.

**Tracked, not the filesystem.** Every file-pattern check reads `git ls-files`, never a
directory walk. A file that is not in git is not part of the repository's documentation,
whatever it is called. This is what makes the blessed local-only cases work: llm-preflight
gitignores `PRD-*.md` and `ROADMAP.md`, and under a filesystem walk checks 26 and 32 would
error on the exact arrangement the standard explicitly permits.

The one exception is check 7, which by definition looks for local-only paths that *are*
tracked.

**Historical and template directories are excluded** from the duplicate-document checks
(18, 26, 27, 32, 36):

```
archived/**   docs/done/**   history/**   .github/**   **/v[0-9]*/**
think-day-*/**   dev-day-*/**   docs/superpowers/**
```

Without carve-outs, check 26 errors on isitgood-auction's
`.github/ISSUE_TEMPLATE/todo.md`, `implementation/archived/v3.2.0/NEXT_STEPS_PLAN.md` and
`project-management/archives/v5.10/NEXT_STEPS_ANALYSIS.md`, and on photoinput's
`docs/done/ROADMAP.md` — all verified present, none of them a second live roadmap. The
spec elsewhere blesses these directories as legitimately tracked history; the duplicate
checks must agree.

### Mechanical — `project_standard.py check`

| # | Check | Severity |
|---|---|---|
| 1 | Required artifacts present for the resolved profile and capabilities | error |
| 2 | Agent contract contains its required sections | error |
| 3 | `DOCMAP.md` freshness — regenerate to a temp file, diff against the committed one | error |
| 4 | Link validation **within standard-required docs** (isitgood-auction's `validate-links.ps1`, ported off PowerShell) | error |
| 5 | Release agreement — version source, resolved tag, changelog section, per channel | error |
| 6 | Declared profile or capability contradicts what was detected | error |
| 7 | `git ls-files` finds a currently tracked local-only path | error |
| 8a | A commit after `adopted` carries a Claude `Co-Authored-By` trailer | error |
| 8b | A commit after `adopted` carries a `Claude-Session:` line or session URL | error |
| 8c | A commit after `adopted` carries `Signed-off-by` naming Claude or Anthropic | error |
| 8d | A commit after `adopted` has Claude as author or committer identity | error |
| 9 | gitignore carries the local-only block | error |
| 10a | An enumerated route has no entry in `API_REFERENCE.md` | error |
| 10b | An entry in `API_REFERENCE.md` matches no enumerated route | error |
| 10c | A generated spec or route manifest last committed before the routes it documents | error |
| 10d | Route enumeration unavailable for this stack | warn |
| 11 | `core.hooksPath` resolves to an existing dir holding both guards | error |
| 11b | A local `core.hooksPath` override points somewhere without them | error |
| 12 | Stamp coverage — the stamped fraction of `docs/**.md` | warn |
| 13 | Stamp staleness — `As of` behind current version, as *unverified since vX* | warn |
| 14 | Claude trailers before the baseline, or only in unreachable history | warn |
| 15 | A tag sorting above the current version, or a version regression **before `adopted`** | warn |
| 16 | Workspaces detected but not validated | warn |
| 17 | Vendored tool version behind the skill's canonical version | warn |
| 18 | More than one document appears to assert product truth | warn |
| 19 | Broken link outside the standard-required docs | warn |
| 20 | A declared `critical-paths` entry no longer resolves to a real path | warn |
| 21 | The repo restates the global model tiering instead of pointing at it | warn |
| 22 | `.claude/agents/` or `.claude/skills/` present but untracked | warn |
| 23 | A required document still contains a `TODO(project-standard)` token | error |
| 24 | `PROJECT_MAP.md` names a path that does not resolve | warn |
| 25 | A document carries both `Status: scaffolded` and a trust stamp | error |
| 26 | A second backlog file exists beside `NEXT_STEPS.md` (by filename) | error |
| 27 | A non-backlog doc reads like an ordered open backlog | warn |
| 28 | `NEXT_STEPS.md` appears to carry completed items | warn |
| 29 | Commits since the last tag, but no `[Unreleased]` changelog section | warn |
| 30 | No direction doc — mission, vision and north star all unstated | error (product) / warn (library) |
| 31 | A direction concept is stated in more than one file | warn |
| 32 | A PRD-shaped file lives outside `docs/prds/` | error |
| 33 | A PRD carries no `Status:` header | error |
| 34 | A PRD marked `shipped vX.Y.Z` is not archived under that version | warn |
| 35 | A `draft`/`accepted` PRD has no matching `NEXT_STEPS.md` entry | warn |
| 36 | A state-asserting document lives inside `docs/prds/` | warn |
| 37 | `DEVELOPMENT_FLOW.md` has no bump table with rows for major, minor and patch | error |
| 37b | The bump table restates generic semver instead of naming a real consumer | warn (semantic) |
| 38 | A release tag **after `adopted`** is lower than an earlier release on the same channel | error |
| 39 | A major bump with no changelog entry describing a break | warn |

Checks 3, 4, 5, 8 and 13 are the ones that justify the split — none needs a model, and
all are work a model would otherwise be paid to eyeball.

Checks 27 and 28 are warns because they cannot be decided by pattern matching. A loose
matcher for completed items (`[x]`, `~~`, "done", "shipped") returns 15 hits against
isitgood-auction's `NEXT_STEPS.md`, and prose like "once done" or "ships when complete"
accounts for most of them. Erroring on that would train everyone to ignore the check. The
mechanical half flags the candidates; the semantic half decides.

### Semantic — the skill, after `check` returns

1. Does the agent contract describe *this* project — real modules, real commands — or
   framework boilerplate?
2. Does `FEATURE_MAP.md` claim anything the code no longer does?
3. Does `PROJECT_MAP.md` match the actual tree?
4. Is a profile-override reason genuine, or a way to dodge a check?
5. Is a trust stamp plausible given what has landed since it was applied?

### Output

Findings ranked most-severe first, each as `path:line — what is wrong — the fix`,
closing with an "I do now / you do" split and an ordering. Never a bare list of findings.

## Monorepos

photoinput is an npm workspaces monorepo (root plus `content-site`). v1 validates the
repo root and **reports** `N workspaces detected, validating root only` rather than
passing silently. Per-workspace validation is a later increment. A bounded scope that
announces itself is honest; one that stays quiet reads as full coverage.

## CI

`setup` offers a `project-standard` job running `check`. It offers rather than imposes —
a repo can adopt the standard without adopting the gate.

**Not every check can run in CI, and pretending otherwise makes the gate red forever.**

| Requirement | Why | Consequence if unmet |
|---|---|---|
| `fetch-depth: 0` | checks 5, 8a–8d, 10c, 13, 14, 15, 38 need full history and tags | those checks are skipped and reported as skipped |
| `--profile=ci` | `~/.claude/git-hooks` does not exist on a runner, and there is no global git config | check 11 is skipped, not failed |

GitHub Actions defaults to `fetch-depth: 1` with no tags, so a naive job would fail every
history-dependent check on a shallow clone. And check 11 asks whether a developer's
machine has the guards installed — a question a runner cannot answer and should not try.

**Skipped is a third outcome, reported distinctly from pass and fail.** A check that did
not run must never read as a check that passed; that is the same dishonesty the trust
stamps exist to prevent. `check --profile=ci` prints the skipped set and why.

The developer-machine profile runs everything.

## Testing

`unittest`, stdlib-only. Fixture repos built in temp directories: one per profile, one
per capability combination, each asserting the exact findings it should produce.

Plus a read-only smoke run across the fleet. That run is not optional, and its record so
far is the argument. Seven defects were corrected during design; **every one came from
checking the standard against real repositories, and not one would have been caught by a
fixture-only suite** — fixtures encode what the author already believes.

| Found by | Defect |
|---|---|
| survey | the `VERSION` file mandate created a second source of truth |
| survey | one profile name conflated "what is this" with "what does it expose" |
| survey | `CLAUDE.md` hardcoded, breaking `AGENTS.md` repos |
| config audit | `core.hooksPath` is global — a vendored hook can never fire |
| config audit | tag resolution by sorting misreads pyramid-wordle's downward renumbering |
| smoke run | attribution-as-error locked 5 of 7 repos permanently red |
| smoke run | isitgood-auction is Flask, not FastAPI — which exposed that the requirement was a format, not an outcome |
| smoke run | the `METHOD /path` format rule failed the fleet's best API document, a 55-endpoint table |
| smoke run | regex over Flask decorators cannot resolve nested blueprint prefixes — 107 phantom routes |
| adversarial review | no grammar for the agent contract — seven checks unimplementable |
| adversarial review | the "green in one sitting" promise contradicted its own severity table |
| adversarial review | `Claude-Session:` lines evaded the attribution rule; photoinput carries three |
| adversarial review | checks 15 and 38 filed one fact pattern as both warn and error |
| adversarial review | check 11 is red on every CI runner; shallow clones break eight history checks |
| adversarial review | the npm-wins version rule selects the number no tag agrees with |
| adversarial review | check 26 errors on `.github/ISSUE_TEMPLATE/todo.md` and `docs/done/ROADMAP.md` |
| adversarial review | `RELEASING.md` and `DEVELOPMENT_FLOW.md` both mandated for one question |
| adversarial review | talealbum's tracked `EXECUTIVE-SUMMARY.md` matched no local-only path |
| implementing | attribution cannot be a `pre-commit` rule — the message does not exist yet |
| implementing | the secret scan's bare `eyJ` matched npm lockfile integrity hashes |
| implementing | its env rule blocked `.env.example`, contradicting the redacted-mirror convention |
| implementing | the scanner matched its own pattern list, so the guard could never be committed |

## Rollout

Ship the skill only. Retrofit happens manually, project by project, when each repo is
next worked in.

**First retrofit is `llm-preflight`, not isitgood-auction.** The smoke run reversed that
choice. Scored across the seven git repos:

| Repo | Errors | What makes it easy or hard |
|---|---|---|
| **llm-preflight** | **3** | version source agrees with its tag, changelog current, no HTTP surface to document, no tracked leaks |
| pyramid-wordle | 4 | clean except docs; stray v2.x tags to retire |
| isitgood-auction-extension | 4 | tiny, but needs a contract from scratch |
| iplaytoday | 5 | no contract; 7 endpoints need documenting |
| car-trip-automation | 4 | `AGENTS.md` missing all three required sections; 61 endpoints, the fleet's largest gap |
| photoinput | 5 | 190 docs; tracks `docs/exec-summaries/`; monorepo |
| talealbum | 6 | no contract at all, and 36 undocumented endpoints |
| isitgood-auction | 6 | two disagreeing version sources, three tracked local-only dirs; API reference exists but has never been diffed against the routes |

isitgood-auction was the natural first target only while the standard was assumed to fit
it for free. It is now the worst first choice on error count — though dropping the
OpenAPI mandate removed the multi-day item that made it forbidding, since its existing
`API_REFERENCE.md` satisfies the slot and needs reconciling against the routes rather
than replacing. llm-preflight is still the model the others should be measured against —
it is the only repo whose release gate already passes.

**Known cost of shipping without an end-to-end run:** the mechanical half has now been
validated against every git repo in the fleet, but the semantic half has never run at
all. The first retrofit is still the first real test of the judgment layer.

**One project is still not a git repository.** `ithinktoday` has no `.git`, so it is out
of the standard's reach until it has one — and it is deployed, so it currently has no
history and no rollback path, independent of anything this skill does.
`car-trip-automation` was brought under version control on 2026-08-04 and enters the
fleet mid-pack: 4 errors, an `AGENTS.md` missing all three required sections, and 61
undocumented endpoints — the largest API gap in the fleet.

## Out of scope

- Rewriting git history to remove already-committed local-only files or Claude trailers
- Secret scanning and rotation — `secrets-audit` owns this
- Per-workspace monorepo validation
- Enforcing the standard on repos outside `~/projects/`
