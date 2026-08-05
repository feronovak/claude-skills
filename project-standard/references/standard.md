# The standard

Every artifact is a **slot** — a question the repo must answer. Several
filenames may answer it. Mandating one filename is how a standard tells its best
incumbent to rewrite itself for a parser's convenience.

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

## The document taxonomy

Five documents, five questions, five tenses. No overlap.

| Document | Answers | Tense |
|---|---|---|
| direction doc | why this exists, where it is going | timeless |
| `NEXT_STEPS.md` | what is open, in what order | future, one line each |
| `docs/prds/<feature>.md` | what one future feature must do, in depth | future, one per feature |
| `FEATURE_MAP.md` | what the product does today | present |
| `CHANGELOG.md` | what shipped, and when | past |

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
contract, they only ever ratchet down.

| Baseline | Effect |
|---|---|
| `adopted` | attribution errors apply to commits after it |
| `api-coverage` | endpoints documented at adoption; below it is a regression |
| `scaffold` | required docs still holding TODO tokens at adoption |

This is what lets a repo with 61 undocumented endpoints adopt today and pay the
debt down over weeks, rather than carrying a permanently red gate.
