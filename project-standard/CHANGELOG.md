# Changelog

The checker under `tool/` is shipped software — a console entry point with its
own version — so it releases like any other. Tags are
`project-standard/v<semver>`, the multi-channel form the standard defines, so
they never collide with the skill collection's own `vX.Y.Z` tags.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- **`critical-paths` entries may name the reference that must be read before
  editing that path.** A bare path says *be careful here*; it does not say where
  the knowledge lives, and that half is the one a newcomer or an agent cannot
  guess — a project's reference lookups are discoverable only once you already
  know they exist, so the reader most likely to miss one is editing exactly the
  code that needed it.

  ```yaml
  critical-paths:
    - services/scoring/                        # unchanged
    - path: src/integrations/
      reference: docs/reference/FIELD_MAP.md
  ```

  Additive and backward compatible: bare strings parse as before, `critical_paths`
  still yields plain paths, and a contract that declares no reference is never
  flagged. New checks `20a` (the reference does not exist, so the promise points
  at nothing) and `20b` (it carries neither a `Last reviewed:` stamp nor a
  generated-file marker, so a reader cannot tell whether to trust it). A generated
  reference is accepted without a stamp deliberately — demanding a review date for
  a file whose header says *do not hand-edit* teaches the habit the stamp exists
  to detect.

  The list-item mapping form is gated on a closed key allow-list (`path`,
  `reference`) rather than on "contains a colon", so a value that happens to hold
  one keeps parsing exactly as before. This parser is deliberately not YAML, and
  widening it by shape rather than by name is how a simple parser starts silently
  reinterpreting old contracts.

### Fixed — documentation

Documentation fixes only — no behaviour change. Every item came from retrofitting
one real repository (a React/TypeScript product with 35 living docs) and hitting
the guidance where it was wrong or silent.

### Fixed

- **The incumbent table contradicted check 30.** It listed `NORTH_STAR.md` /
  `MISSION.md` / `VISION.md` as "leave it, name it in the contract", which reads
  as though the direction slot accepts any path. Check 30 matches the *filename*.
  Following the table, a retrofit merged three direction docs into `STRATEGY.md`,
  passed its own review, and then failed the check — costing a rename and eleven
  files of link repointing after the work was done.
- **`git-hygiene.md` contradicted itself on attribution.** The opening said a repo
  may declare `ai-attribution: allow`; the scope table said the rule holds
  "every repo, unconditionally". The override is implemented, so the table was
  the wrong half.

### Added

- **The hook and the checker disagree by design, and now say so.** `check` reads
  the contract and honours `ai-attribution: allow`; the `commit-msg` hook greps
  flat and never parses a contract, so it blocks the trailer in a repo that
  declared `allow`. A repo that wants the attribution must both declare it and
  stop installing the hook, or commits fail with no finding to explain why.
- **The checker reads tracked files.** A `LICENSE` written but not `git add`ed
  stays invisible and its broken-link finding persists. This is also the reason
  behind the `generate` → commit → `generate` order.
- **Trust stamps must be bold.** Check 12 matches `**Last reviewed:**` and counts
  nothing else; a plain `Last reviewed:` is reported as absent rather than
  malformed, so a repo stamping every document the wrong way reads as one
  stamping none.
- **Repointing inbound links is not a string replacement.** Warned in setup, with
  the failure seen: a blind substitution put the same entry twice in a golden path
  and left an index row labelled with the merged document's old name.
- **Rewriting commit history needs a clean tree**, and `git stash` is blocked
  outright on setups carrying a destructive-git guard. The file-copy plus
  `git show HEAD:<path>` workaround is documented.

## [0.2.0] - 2026-08-06

The first release with a version anyone can act on. Every defect below was
found by measurement against real repositories or by an adversarial review of
the finished skill — none came from a fixture.

### Added

- `claims` — enumerates the checkable unit in every standard document, so a
  judgement pass has a denominator instead of an impression. Measured across
  five runs over one 40-row product map, each verified a different subset and
  none found every false row; the run whose instruction demanded thoroughness
  most forcefully scored worst while claiming to have checked everything.
- `vendor` — copies the checker into a repository for CI. The copy step used to
  be a paragraph of README prose, which is how one repository came to run nine
  stale modules in its gate.
- Check 17 — a vendored copy that no longer matches canonical. Compares content
  as well as the version string, because the drift found in the field carried
  nine differing modules at an identical version.
- Check 42 — a declared baseline may never loosen. Compared against the extreme
  the repository already recorded across its contract's history, not against
  the value sitting in the contract today, which the same commit could edit.
- A `decisions` slot, satisfied by `docs/DECISIONS.md` or a directory of
  records. The taxonomy had no home for why a choice was made and what it cost.
- Slots may be declined with `<slot>: waived` and a written `reason:`. Waiving
  without one is an error.

### Changed

- Every check reads tracked git state. Presence used to be answered from the
  working tree in the profile classifier and the version-source resolver, so a
  gitignored `package.json` rewrote which documents a repository owed — the
  same commit reported three errors on a clean clone and nine on the machine
  with the stray file.
- The judgement half must report coverage and name what it did not check, the
  rule the mechanical half already followed by reporting a check skipped rather
  than passed.

### Fixed

- Invocation from a subdirectory reported false missing documents. `git -C
  <subdir> ls-files` scopes to the subtree, so every root-level document read
  as absent. `generate` and `routes` wrote their output into the subdirectory
  for the same reason.
- The contract grammar is closed. A typo'd key parsed clean and the override
  silently never took effect.
- Detection and enumeration share one route pattern. They had drifted, so a
  repository whose only surface was a root-level `app/route.ts` never resolved
  as serving HTTP and the entire endpoint-coverage check never ran.
- `next-steps` and `release-flow` are admissible keys. Closing the grammar
  rejected them, because the key list was derived by grepping for a literal
  accessor and both are read through a lookup table.

## [0.1.0] - 2026-08-05

Initial release. One standard for how a project documents itself, releases and
records who wrote it: a stdlib-only checker for what a machine can decide, and
a skill for what it cannot.

[0.2.0]: https://github.com/feronovak/claude-skills/releases/tag/project-standard%2Fv0.2.0
[0.1.0]: https://github.com/feronovak/claude-skills/releases/tag/project-standard%2Fv0.1.0
