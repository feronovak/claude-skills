# Release flow

## The version source

One per repo, chosen by ecosystem — never a `VERSION` file added beside a
manifest that already states a version, which would create the second source of
truth this standard exists to remove.

| Ecosystem | Source |
|---|---|
| npm only | `package.json` `version` |
| Python only | `pyproject.toml` `[project] version` |
| polyglot | the source the release tags corroborate; ties break to the backend |
| neither | `VERSION` at root |

The polyglot rule is not hypothetical. A Flask-plus-npm repo reads 5.0.0 in
`package.json` and 0.13.2 in `VERSION`, with every tag saying 0.13.2. A flat
"npm wins" rule picks the one number nothing agrees with.

## What a bump means

The standard fixes the axis; each product names its consumer.

| Profile | The consumer | major is |
|---|---|---|
| `library` | code that imports it | a change requiring callers to adapt |
| `product` with an HTTP API | callers of the API | a request or response contract change |
| `product`, no API | the user | the product's promise changes |

- **minor** — new capability, or a change to what the consumer is told, that
  does not require them to adapt.
- **patch** — fixes and internals the consumer cannot observe.

Below 1.0, minor absorbs breaking changes; `0.9 → 0.10` skips no gate. 1.0 is a
quality milestone, declared once and never spent to make a launch sound larger.

## Tags

Resolution is by **ancestry** — `git describe --tags --abbrev=0` — never by
sorting. One repo renumbered downward and carries v2.2.0 above its current
v1.7.x line; sorting reads the wrong tag as latest and invents a three-major
discrepancy that does not exist.

| Shape | Meaning |
|---|---|
| `v1.7.4` | single-channel release |
| `web/v1.7.4`, `android/v1.7.5` | multi-channel; each gates independently |
| `v1.5.0-pre-mobile` | a cut of 1.5.0; needs no changelog section, released nothing |
| `HEAD` untagged | the gate is not evaluated — the normal state between releases |

## The three-way gate

The three are the tag, the version source and the changelog. When `HEAD`
carries a `v<semver>` tag: the version source reads `X.Y.Z`, and `CHANGELOG.md`
has an `X.Y.Z` section. Checkable in a second, no model involved.

## The changelog stays hand-written

Keep a Changelog, `## [Unreleased]` accumulating as work lands. This is the one
place the standard rejects generation: a changelog cannot drift the way a
product map can — it is append-only and version-scoped, so an entry describing
1.7.5 stays true regardless of what the code does next. Generating from commits
would turn "keys dropped when typing fast" into "fix(input): handleKey closure".
