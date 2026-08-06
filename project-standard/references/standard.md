# The standard

Every artifact is a **slot** — a question the repo must answer. Several
filenames may answer it. Mandating one filename is how a standard tells its best
incumbent to rewrite itself for a parser's convenience.

## Contents

- [Profile and capabilities](#profile-and-capabilities)
- [Required slots](#required-slots)
- [The document taxonomy](#the-document-taxonomy)
- [The API surface](#the-api-surface)
- [Enumerable units — how each document must be written](#enumerable-units--how-each-document-must-be-written)
- [Trust stamps](#trust-stamps)
- [Baselines](#baselines)

## Profile and capabilities

Detected from code, because a declaration is a hand-maintained assertion and
those are what this tool distrusts.

| Profile | Detection |
|---|---|
| `library` | a manifest declaring distribution — `bin`/`exports`/`publishConfig`, `[project.scripts]`, `[lib]` |
| `product` | any package manifest, or a conventional source root (`src`, `app`, `lib`, `cmd`, `pages`, …) |
| `docs` | neither |

By packaging convention, not by absence of code and not by a markdown ratio: an
infrastructure repo holds shell scripts, and a documentation-heavy product can
be 41% markdown.

Capabilities: **`http-api`** (Flask/FastAPI/Django app object, `app/api/**/route.ts`,
`pages/api/`, Express `listen`) and **`channels`** (`web` · `extension` ·
`mobile` · `desktop`).

`extension` is exclusive — an extension's source looks exactly like a web app's,
and a phantom `web` channel arms a release gate that can never pass.

House rules — the local-only set and whether AI attribution is forbidden — are
defaults, not universals. `local-only:` extends the set, `local-only: [replace,
…]` swaps it, `track-anyway:` keeps a default path tracked, and
`ai-attribution: allow` stands the attribution checks down.

An override in the contract must state a `reason:`. An escape hatch that costs
nothing becomes the default.

## Required slots

| Slot | product | library | docs | Satisfied by |
|---|:-:|:-:|:-:|---|
| agent contract | ✅ | ✅ | ✅ | `CLAUDE.md` or `AGENTS.md` |
| readme | ✅ | ✅ | ✅ | `README.md` |
| docmap | ✅ | ✅ | ✅ | `docs/DOCMAP.md` — generated |
| code map | ✅ | ✅ | — | `docs/PROJECT_MAP.md` |
| product map | ✅ | ✅ | — | `docs/FEATURE_MAP.md` |
| roadmap | ✅ | ✅ | — | `docs/NEXT_STEPS.md` |
| release flow | ✅ | ✅ | — | `docs/DEVELOPMENT_FLOW.md` or `RELEASING.md` |
| changelog | ✅ | ✅ | — | `CHANGELOG.md` |
| direction | ✅ | warn | — | `NORTH_STAR.md` / `MISSION.md` / `VISION.md`, or `direction: inherit` |
| api reference | if `http-api` | if `http-api` | — | `docs/API_REFERENCE.md` |
| contribution surface | — | ✅ | — | `CONTRIBUTING.md`, `SECURITY.md` |
| decisions | warn | warn | warn | `docs/DECISIONS.md`, or `docs/adr/**` |

## The document taxonomy

Six documents, six questions. Five partition by tense; the sixth answers a
question none of the others can.

| Document | Answers | Tense |
|---|---|---|
| direction doc | why this exists, where it is going | timeless |
| `NEXT_STEPS.md` | what is open, in what order | future, one line each |
| `docs/prds/<feature>.md` | what one future feature must do, in depth | future, one per feature |
| `FEATURE_MAP.md` | what the product does today | present |
| `CHANGELOG.md` | what shipped, and when | past |
| `DECISIONS.md` | why this and not the obvious alternative | at the moment of choosing |

**The decision log is not a sixth tense, and that is the point.** The other five
split cleanly on time; a decision is fixed to the moment it was made and stays
true afterwards even when the code moves on. Direction says where the product
is going, the product map what it does today, the changelog what shipped, a PRD
what is proposed — none of them records a choice or what it cost. A project
without this document relitigates the same argument every time somebody new
reads the code.

**A decision is superseded, never edited.** Editing an entry destroys the
record of what was believed when the choice was made, which is the only thing
the document is for. A decision that no longer holds gets a later entry saying
so, linking back.

**The slot is waivable, with a written reason.** Not every repository has
architecture to decide. `decisions: waived` plus a `reason:` declines it; the
same reason gate the profile overrides use, for the same purpose — an escape
hatch that costs nothing becomes the default.

A backlog line graduates into a PRD when someone starts designing it. A PRD
never graduates into the product map — the map is written from the code that
shipped, not from the document that proposed it.

**Exactly one file holds open work.** A repo may carry any number of
complementary documents — vision, specs, architecture — but only one may answer
"what is next". Two roadmaps disagreeing is worse than none.

**A repo may inherit direction from a parent product** via `direction: inherit`.
A companion repo carries what describes itself and points at the parent for what
the product answers once.

## The API surface

**Coverage is mandatory; OpenAPI is not.** The requirement is that every
endpoint is understandable by a person and by a model reading the repo cold.

Enumeration comes from the framework, never from scraping decorators. A Flask
route's path is relative to its blueprint, blueprints nest, and the real path is
composed at registration across modules — regex over decorators produced 107
phantom routes against a document correctly describing 55. Flask and FastAPI
write `docs/api/routes.json` at dev time via `project-standard routes`; Next.js
resolves statically. Where enumeration is impossible, the checker **warns** and
says so rather than inventing findings.

The document format accepts what good documentation already looks like: table
rows with the method and path in separate cells, inline `GET /path`, headings,
and combined methods (`GET·POST`).

## Enumerable units — how each document must be written

Every document in the taxonomy has a **countable unit**, and the shape of the
document is what makes it countable. This is not a formatting preference. A
judgement pass over a document reports what it happened to read; over a
worklist it reports coverage against a denominator, and can say what it
skipped.

The measurement behind the rule: five runs over one product map of ~40 rows
each verified a different subset, none found every false row, and the run whose
instruction most forcefully demanded thoroughness scored worst — while opening
with a claim that it had checked every row. Recall follows sample size, not
effort. So the standard makes the sample enumerable.

| Document | Unit | Written as | Verifying one means |
|---|---|---|---|
| product map | a claim | one table row per feature | read the implementation it names; is it true today |
| code map | a mapping | one table row per path | the path exists, and holds the responsibility described |
| api reference | an endpoint | one table row, or `GET /path` inline | the route exists; the handler matches the description |
| `NEXT_STEPS.md` | a backlog item | one list item per item, one line each | it is still open |
| PRD | a header and a section | `**Status:**` / `**Backlog:**` / `**Owner:**`, then `##` sections | it is decided, linked and owned — **never** whether it is true of the code |
| `CHANGELOG.md` | a release | `## [x.y.z] - date` | a tag exists, and the entry describes what shipped |
| release flow | a bump rule | one table row per bump | it names a real consumer and a real consequence |
| decisions | a decision | one `##` entry per choice, newest first | it still governs the code — if not, supersede it |
| direction doc | — | prose | nothing to count; direction is judgement |

`project-standard claims` prints this worklist. `--doc` narrows it to one file,
`--json` makes it machine-readable.

**A PRD is intent and is never checked against the code.** It is the one slot
where "is this true of the implementation" is the wrong question — a proposal
that were already true of the code would not need writing. What is checkable
is that it is owned, linked to a backlog item, and carries a decided status.
Conflating the two turns a checklist into a demand that proposals be facts.

**A document with no countable unit says so rather than going missing.** The
direction doc and the README hold no unit; both are reported as having none,
with the reason. A document absent from the worklist must never read as a
document with nothing to check — the same rule the mechanical half follows
when it reports a check as skipped rather than passed.

**Writing a document so it cannot be enumerated is a way of avoiding the
check.** A product map written as paragraphs yields no rows, and a backlog
written as prose yields no items. Where the shape does not match the slot, the
worklist says the unit count is zero and names the document, so the gap is
visible rather than silent.

## Trust stamps

`**Last reviewed:** YYYY-MM-DD · **As of:** vX.Y.Z`

A stamp means one thing: someone read this document against the code at that
version. Never applied in bulk. Three states exist and are never blurred —
`stamped`, `unstamped`, `scaffolded`.

**An unstamped document is a metric, never a failure.** A repo with 150
documents and no stamps would report 150 errors on its first run and the gate
would be switched off within a day.

## Baselines

Adoption is gated by baselines, not by finishing the work. Declared in the
contract, they only ever ratchet down — and check 42 enforces that against
what the repository already recorded, not against the value sitting in the
contract today. A baseline that could be edited in the same commit as the
regression it excuses would gate nothing.

| Baseline | Effect |
|---|---|
| `adopted` | attribution errors apply to commits after it |
| `api-coverage` | endpoints documented at adoption; below it is a regression |
| `scaffold` | required docs still holding TODO tokens at adoption |

This is what lets a repo with 61 undocumented endpoints adopt today and pay the
debt down over weeks, rather than carrying a permanently red gate.
