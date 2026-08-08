# project-standard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `project-standard` skill and its stdlib-only Python checker, which validates and scaffolds project documentation, release flow and git hygiene across every repo under `~/projects/apps`.

**Architecture:** A vendored CLI owns the mechanical checks (deterministic, gates CI); a Claude Code skill owns the semantic checks and the interactive `setup`/`init` flows. The CLI is a package of small single-responsibility modules behind one `Finding` type, so each check is independently testable and the runner stays trivial.

**Tech Stack:** Python 3.10+, stdlib only (`argparse`, `json`, `re`, `subprocess`, `pathlib`, `unittest`). No third-party dependencies, ever — the tool is vendored into Next.js repos that must gain no dependency, and runs on `ubuntu-latest` with no setup step.

**Spec:** `docs/superpowers/specs/2026-08-04-project-standard-design.md` (1250 lines, 47 checks). The spec is authoritative; this plan implements it.

## Global Constraints

- **Stdlib only.** No PyYAML, no requests, no click. Python ≥ 3.10.
- **No YAML library exists in stdlib** — the contract block is parsed by a restricted-subset parser (Task 2) supporting exactly: `key: scalar`, `key:` followed by `  - item` list entries, and one level of nested `  reason:` under a key. Anything else is a parse error reported as a finding, never a crash.
- **Every git read goes through `gitio.py`.** No module shells out to git directly. This is what makes the whole suite testable against fixture repos.
- **Checks read `git ls-files`, never a filesystem walk** — except check 7, which by definition looks for tracked local-only paths.
- **Severity is data, not control flow.** A check returns findings; the runner decides the exit code. `error` → exit 1, `warn` → exit 0, `skipped` → exit 0 and reported distinctly.
- **`skipped` is a third outcome.** A check that did not run must never read as passed.
- **Determinism.** No timestamps, no `datetime`, no dict-order dependence in any generated output. `generate` output must be byte-identical across runs.
- **No Claude attribution in any commit** (`Co-Authored-By`, `Claude-Session:`, `Signed-off-by`, author identity). The global hooks enforce this; do not attempt to bypass them.
- Test command: `python3 -m unittest discover -s tool/tests -t tool -v`

---

## File Structure

```
~/projects/claude-skills/project-standard/
  SKILL.md                     orchestrator: modes, semantic checks, when to run what
  references/
    standard.md                artifacts, profiles, authoring contracts
    git-hygiene.md             the four attribution markers, local-only set
    release-flow.md            bump axis, three-way gate, channels
  templates/
    agent-contract.md.tmpl     includes the `## project-standard` yaml block
    PROJECT_MAP.md.tmpl  FEATURE_MAP.md.tmpl  NEXT_STEPS.md.tmpl
    DEVELOPMENT_FLOW.md.tmpl  NORTH_STAR.md.tmpl  API_REFERENCE.md.tmpl
    CHANGELOG.md.tmpl  prd.md.tmpl
  tool/
    project_standard/
      __init__.py              VERSION constant
      findings.py              Finding, Severity, Outcome
      gitio.py                 every git subprocess call, one place
      contract.py              restricted-subset yaml parser + Contract object
      detect.py                profile + http-api + channels detection
      artifacts.py             required-artifact matrix and presence checks
      docs.py                  stamps, TODO tokens, links, duplicate documents
      release.py               version source, tags, changelog, bump table
      hygiene.py               local-only paths, attribution markers, hooks
      api.py                   route enumeration, doc parsing, coverage
      docmap.py                DOCMAP.md generator
      runner.py                check registry, profiles (dev/ci), exit codes
      cli.py                   argparse surface
    tests/
      fixtures.py              builds throwaway git repos in temp dirs
      test_contract.py  test_detect.py  test_artifacts.py  test_docs.py
      test_release.py  test_hygiene.py  test_api.py  test_docmap.py
      test_runner.py  test_fleet_smoke.py
```

**Responsibility boundaries:** `gitio` is the only module that knows git exists. `findings` is the only shared vocabulary. Every checker module exports `check(ctx) -> list[Finding]` and imports nothing from its siblings. `runner` wires them; `cli` parses arguments. This is what lets a task be reviewed and rejected on its own.

---

### Task 1: Findings vocabulary and the git I/O layer

**Files:**
- Create: `tool/project_standard/__init__.py`, `tool/project_standard/findings.py`, `tool/project_standard/gitio.py`
- Test: `tool/tests/test_gitio.py`, `tool/tests/fixtures.py`

**Interfaces:**
- Produces: `Finding(check, severity, message, path=None, line=None)`; `Severity` = `"error" | "warn" | "skipped"`; `Git(repo)` with `ls_files()`, `log(n, fmt)`, `tags()`, `describe()`, `config(key)`, `commits_since(ref)`, `file_committed_at(path)`, `is_repo()`, `has_history()`.
- Consumes: nothing.

- [ ] **Step 1: Write `fixtures.py`** — a `TempRepo` context manager that `git init`s in a temp dir, sets `user.name`/`user.email`, writes files, and commits. Every later test builds on it. It must set `core.hooksPath` to an empty dir so the global guards never interfere with fixtures.

```python
class TempRepo:
    def __init__(self): self.dir = Path(tempfile.mkdtemp())
    def __enter__(self):
        self.git("init", "-q", "."); self.git("config", "user.name", "T")
        self.git("config", "user.email", "t@t.t")
        hooks = self.dir / ".nohooks"; hooks.mkdir()
        self.git("config", "core.hooksPath", str(hooks))
        return self
    def write(self, rel, content):
        p = self.dir / rel; p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content); return p
    def commit(self, msg="c", add="-A"):
        self.git("add", add); self.git("commit", "-q", "-m", msg)
    def git(self, *a):
        return subprocess.run(["git", "-C", str(self.dir), *a],
                              capture_output=True, text=True).stdout.strip()
    def __exit__(self, *e): shutil.rmtree(self.dir, ignore_errors=True)
```

- [ ] **Step 2: Write the failing test**

```python
def test_ls_files_returns_tracked_only(self):
    with TempRepo() as r:
        r.write("a.txt", "x"); r.write("b.txt", "y")
        r.commit()
        r.write("untracked.txt", "z")
        g = Git(r.dir)
        self.assertEqual(set(g.ls_files()), {"a.txt", "b.txt"})

def test_is_repo_false_outside_git(self):
    d = Path(tempfile.mkdtemp())
    self.assertFalse(Git(d).is_repo())
```

- [ ] **Step 3: Run to verify it fails** — `python3 -m unittest tool.tests.test_gitio -v`, expect `ModuleNotFoundError`.
- [ ] **Step 4: Implement `findings.py` and `gitio.py`.** `Git` wraps one `_run()` returning `stdout` or `None` on non-zero. `has_history()` returns whether `git rev-list --count HEAD` exceeds 1 and whether tags exist — the CI profile keys off it.
- [ ] **Step 5: Run tests, expect PASS.**
- [ ] **Step 6: Commit** — `feat(tool): findings vocabulary and the single git access point`

---

### Task 2: Contract parser

**Files:**
- Create: `tool/project_standard/contract.py`
- Test: `tool/tests/test_contract.py`

**Interfaces:**
- Consumes: `Finding` from Task 1.
- Produces: `Contract` with `.adopted`, `.profile`, `.http_api`, `.channels`, `.direction`, `.prds`, `.critical_paths`, `.baselines`, `.reasons`, `.path`, `.errors`; and `find_contract(repo, tracked) -> Path | None` returning `CLAUDE.md` or `AGENTS.md`.

- [ ] **Step 1: Write the failing tests** — cover the happy path, the missing-block case, a list value, a `reason` sub-key, and a malformed line.

```python
BLOCK = """## project-standard

```yaml
adopted: 4f3a91c
http-api: no
  reason: auth callbacks only
channels: [web, mobile]
critical-paths:
  - services/verdict/
  - services/scoring/
```
"""

def test_parses_scalars_lists_and_reasons(self):
    c = parse_contract(BLOCK)
    self.assertEqual(c.adopted, "4f3a91c")
    self.assertIs(c.http_api, False)
    self.assertEqual(c.reasons["http-api"], "auth callbacks only")
    self.assertEqual(c.channels, ["web", "mobile"])
    self.assertEqual(c.critical_paths, ["services/verdict/", "services/scoring/"])

def test_missing_block_is_an_error_not_a_crash(self):
    c = parse_contract("# Readme\n\nnothing here")
    self.assertIsNone(c.adopted)
    self.assertTrue(any("no `## project-standard` block" in e for e in c.errors))

def test_override_without_reason_is_recorded(self):
    c = parse_contract("## project-standard\n\n```yaml\nprofile: library\n```\n")
    self.assertEqual(c.profile, "library")
    self.assertIn("profile", c.missing_reasons)
```

- [ ] **Step 2: Run to verify it fails.**
- [ ] **Step 3: Implement the restricted parser.** Extract the first fenced block following a `## project-standard` heading. Parse line by line: `^(\S[\w-]*):\s*(.*)$` for keys, `^\s+-\s+(.+)$` for list items belonging to the last key, `^\s+(reason):\s*(.+)$` for the reason sub-key. Inline lists `[a, b]` split on commas. `yes/no/true/false` become booleans. Unparseable lines append to `.errors`; the parser never raises.
- [ ] **Step 4: Run tests, expect PASS.**
- [ ] **Step 5: Commit** — `feat(tool): parse the contract block without a yaml dependency`

---

### Task 3: Detection — profile, http-api, channels

**Files:**
- Create: `tool/project_standard/detect.py`
- Test: `tool/tests/test_detect.py`

**Interfaces:**
- Consumes: `Git`, `Contract`.
- Produces: `detect(repo, tracked) -> Detected(profile, http_api, channels, evidence)`; `resolve(detected, contract) -> Resolved(...)` applying overrides and returning a mismatch finding when the declaration contradicts detection.

- [ ] **Step 1: Write the failing tests** — one per profile and capability, including the exclusivity rule.

```python
def test_extension_suppresses_web(self):
    with TempRepo() as r:
        r.write("manifest.json", '{"manifest_version": 3}')
        r.write("src/app.ts", "export const x = 1")
        r.commit()
        d = detect(r.dir, Git(r.dir).ls_files())
        self.assertEqual(d.channels, ["extension"])

def test_nextjs_route_files_set_http_api(self):
    with TempRepo() as r:
        r.write("app/api/vet/route.ts", "export async function POST() {}")
        r.commit()
        self.assertTrue(detect(r.dir, Git(r.dir).ls_files()).http_api)

def test_declared_override_contradicting_detection_is_a_finding(self):
    ...
    self.assertTrue(any(f.check == "6" for f in findings))
```

- [ ] **Step 2: Run to verify it fails.**
- [ ] **Step 3: Implement.** Library signals: `publishConfig`/`bin` in `package.json`, or `[project.scripts]`/`build-backend` in `pyproject.toml`. Docs profile: no source files. Channels: `manifest_version` → `extension` (and suppress `web`); `android-native/` or `capacitor.config` → `mobile`; `src-tauri/` or an electron config → `desktop`; otherwise `web`.
- [ ] **Step 4: Run tests, expect PASS.**
- [ ] **Step 5: Commit** — `feat(tool): resolve profile and capabilities from code, not declaration`

---

### Task 4: Required artifacts and the presence matrix

**Files:**
- Create: `tool/project_standard/artifacts.py`
- Test: `tool/tests/test_artifacts.py`

**Interfaces:**
- Consumes: `Resolved`, `Contract`, tracked file list.
- Produces: `required_for(resolved, contract) -> list[Slot]` where `Slot(name, candidates, severity)`; `check(ctx) -> list[Finding]` implementing checks 1, 2, 30 and the slot aliases.

- [ ] **Step 1: Write the failing tests** — the alias slots are the subtle part and each needs its own case.

```python
def test_agent_contract_satisfied_by_either_filename(self):
    for name in ("CLAUDE.md", "AGENTS.md"):
        with self.subTest(name=name):
            ...
            self.assertFalse(any(f.check == "1" and "agent contract" in f.message
                                 for f in findings))

def test_releasing_md_satisfies_the_release_flow_slot(self):
    # library repo with RELEASING.md and no DEVELOPMENT_FLOW.md -> no finding
    ...

def test_direction_inherit_satisfies_check_30(self):
    # contract declares `direction: inherit` naming a parent -> no finding
    ...

def test_library_missing_direction_is_warn_not_error(self):
    self.assertEqual(sev_for(findings, "30"), "warn")
```

- [ ] **Step 2: Run to verify it fails.**
- [ ] **Step 3: Implement** the matrix from the spec's Required artifacts table, with slots rather than filenames: agent contract (`CLAUDE.md`|`AGENTS.md`), release flow (`docs/DEVELOPMENT_FLOW.md`|`RELEASING.md`), direction (contract's `direction:` key, `inherit`, or a `NORTH_STAR.md`/`MISSION.md`/`VISION.md` set).
- [ ] **Step 4: Run tests, expect PASS.**
- [ ] **Step 5: Commit** — `feat(tool): resolve required artifacts as slots, not filenames`

---

### Task 5: Docs checks — stamps, tokens, links, duplicates

**Files:**
- Create: `tool/project_standard/docs.py`
- Test: `tool/tests/test_docs.py`

**Interfaces:**
- Consumes: tracked list, `Contract`.
- Produces: `check(ctx) -> list[Finding]` implementing 4, 12, 13, 18, 19, 22, 23, 24, 25, 26, 27, 28, 36; plus `EXCLUDED` glob list.

- [ ] **Step 1: Write the failing tests.** The carve-outs are the whole point of this task — the review found check 26 firing on four real files.

```python
EXCLUDED_CASES = [
    ".github/ISSUE_TEMPLATE/todo.md",
    "implementation/archived/v3.2.0/NEXT_STEPS_PLAN.md",
    "project-management/archives/v5.10/NEXT_STEPS_ANALYSIS.md",
    "docs/done/ROADMAP.md",
]

def test_excluded_dirs_never_trigger_duplicate_backlog(self):
    for path in EXCLUDED_CASES:
        with self.subTest(path=path):
            with TempRepo() as r:
                r.write("docs/NEXT_STEPS.md", "# Next\n")
                r.write(path, "# Roadmap\n- [ ] thing\n")
                r.commit()
                self.assertEqual(
                    [f for f in run_docs(r.dir) if f.check == "26"], [])

def test_live_second_backlog_is_an_error(self):
    with TempRepo() as r:
        r.write("docs/NEXT_STEPS.md", "# Next\n")
        r.write("docs/ROADMAP.md", "# Roadmap\n")
        r.commit()
        self.assertEqual(sev_for(run_docs(r.dir), "26"), "error")

def test_todo_token_in_required_doc_is_error(self):
    ...  # "<!-- TODO(project-standard): fill this -->"

def test_scaffolded_plus_stamp_is_error(self):
    ...  # check 25

def test_relative_link_resolution(self):
    # docs/A.md linking ../README.md and ./B.md — one resolves, one does not
```

- [ ] **Step 2: Run to verify it fails.**
- [ ] **Step 3: Implement.** Link validation resolves relative to the containing file and only errors inside required docs (check 4); everything else is check 19 at warn. Stamp coverage counts `Last reviewed:` in the first 800 characters. Duplicate detection matches filename patterns **after** applying `EXCLUDED`.
- [ ] **Step 4: Run tests, expect PASS.**
- [ ] **Step 5: Commit** — `feat(tool): document checks, with carve-outs for history directories`

---

### Task 6: Release checks

**Files:**
- Create: `tool/project_standard/release.py`
- Test: `tool/tests/test_release.py`

**Interfaces:**
- Consumes: `Git`, `Contract`, `Resolved`.
- Produces: `version_source(repo, tags) -> (name, value)`; `check(ctx)` implementing 5, 15, 29, 37, 37b, 38.

- [ ] **Step 1: Write the failing tests.** Encode the two cases that broke earlier drafts.

```python
def test_polyglot_picks_the_source_the_tags_corroborate(self):
    with TempRepo() as r:
        r.write("package.json", '{"version": "5.0.0"}')
        r.write("VERSION", "0.13.2\n")
        r.write("f", "x"); r.commit(); r.git("tag", "v0.13.2")
        self.assertEqual(version_source(r.dir, Git(r.dir).tags()),
                         ("VERSION", "0.13.2"))

def test_regression_before_adopted_is_warn_after_is_error(self):
    # tags v2.2.0 then v1.7.0; adopted set before/after -> 15 vs 38
    ...

def test_channel_tags_gate_independently(self):
    # web/v1.7.4 and android/v1.7.5 both valid, no cross-channel regression
    ...

def test_prerelease_needs_no_changelog_section(self):
    # v1.5.0-pre-mobile with no [1.5.0] section -> no finding
    ...
```

- [ ] **Step 2: Run to verify it fails.**
- [ ] **Step 3: Implement.** Tag resolution via `git describe --tags --abbrev=0`, never sorting. Channel parsed from a `<channel>/` tag prefix, defaulting to `web`. Version source: candidates from `package.json`, `pyproject.toml`, `VERSION`; pick the one matching any tag; tie-break to the Python manifest when a `requirements.txt` or `pyproject.toml` exists.
- [ ] **Step 4: Run tests, expect PASS.**
- [ ] **Step 5: Commit** — `feat(tool): release gate with ancestry-based tag resolution`

---

### Task 7: Hygiene checks

**Files:**
- Create: `tool/project_standard/hygiene.py`
- Test: `tool/tests/test_hygiene.py`

**Interfaces:**
- Consumes: `Git`, `Contract`.
- Produces: `LOCAL_ONLY`, `LOCAL_ONLY_PATTERNS`, `ATTRIBUTION_PATTERNS`; `check(ctx)` implementing 7, 8a–8d, 9, 11, 11b, 14.

- [ ] **Step 1: Write the failing tests** — one per attribution marker, since the review found three of four unguarded.

```python
MARKERS = [
    ("8a", "Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"),
    ("8b", "Claude-Session: https://claude.ai/code/session_018abc"),
    ("8c", "Signed-off-by: Claude <noreply@anthropic.com>"),
]

def test_each_attribution_marker_after_adopted_is_an_error(self):
    for check_id, line in MARKERS:
        with self.subTest(check=check_id):
            ...
            self.assertEqual(sev_for(findings, check_id), "error")

def test_markers_before_adopted_are_warns(self):
    ...  # check 14

def test_exec_summary_pattern_is_warn_not_error(self):
    # docs/EXECUTIVE-SUMMARY.md tracked -> warn, not error
```

- [ ] **Step 2: Run to verify it fails.**
- [ ] **Step 3: Implement.** Attribution scans `git log --format=%H%x00%an%x00%ae%x00%B` from `adopted..HEAD` for errors and `..adopted` for warns; author identity checks `%an`/`%ae`. Hook reachability resolves `core.hooksPath` and tests both files for existence and the executable bit.
- [ ] **Step 4: Run tests, expect PASS.**
- [ ] **Step 5: Commit** — `feat(tool): hygiene checks covering all four attribution markers`

---

### Task 8: API surface — enumeration and coverage

**Files:**
- Create: `tool/project_standard/api.py`
- Test: `tool/tests/test_api.py`

**Interfaces:**
- Consumes: tracked list.
- Produces: `code_endpoints(repo, tracked) -> (set[(method, path)], list[str])` where the second value names unresolvable frameworks; `doc_endpoints(repo)`; `check(ctx)` implementing 10a–10d.

- [ ] **Step 1: Write the failing tests.** Both parser bugs the smoke run found get a regression test.

```python
def test_table_row_format_is_recognised(self):
    doc = "| POST | `/api/vet` | public | Vet one listing |\n"
    self.assertIn(("POST", "/api/vet"), parse_doc_endpoints(doc))

def test_combined_methods_expand(self):
    doc = "| GET·POST | `/api/me/hunts` | auth | List / create |\n"
    eps = parse_doc_endpoints(doc)
    self.assertIn(("GET", "/api/me/hunts"), eps)
    self.assertIn(("POST", "/api/me/hunts"), eps)

def test_flask_is_reported_unresolvable_not_guessed(self):
    with TempRepo() as r:
        r.write("app/__init__.py", "bp = Blueprint('x', __name__)\n"
                                   "@bp.route('/thing')\ndef t(): pass\n")
        r.write("app/reg.py", "app.register_blueprint(bp)\n")
        r.commit()
        eps, unresolved = code_endpoints(r.dir, Git(r.dir).ls_files())
        self.assertEqual(eps, set())
        self.assertTrue(any("flask" in u for u in unresolved))
        # and the finding is a warn, never a phantom-route error
```

- [ ] **Step 2: Run to verify it fails.**
- [ ] **Step 3: Implement.** Next.js: walk `app/api/**/route.ts` for exported method names. Manifest: read `docs/api/routes.json` when present and prefer it over heuristics. Flask/FastAPI without a manifest: return empty plus an `unresolved` entry → check 10d warn. Path normalisation collapses `<int:id>`, `[id]` and `:id` to `{}`.
- [ ] **Step 4: Run tests, expect PASS.**
- [ ] **Step 5: Commit** — `feat(tool): endpoint coverage that warns rather than inventing routes`

---

### Task 9: DOCMAP generator

**Files:**
- Create: `tool/project_standard/docmap.py`
- Test: `tool/tests/test_docmap.py`

**Interfaces:**
- Consumes: tracked list, stamp data from `docs.py`.
- Produces: `render(ctx) -> str`; `check(ctx)` implementing check 3 by regenerating and diffing.

- [ ] **Step 1: Write the failing test** — determinism is the requirement that matters.

```python
def test_output_is_byte_identical_across_runs(self):
    with TempRepo() as r:
        for n in ("A", "B", "C"):
            r.write(f"docs/{n}.md", f"# {n}\n\n**Last reviewed:** 2026-08-01\n")
        r.commit()
        self.assertEqual(render(ctx(r.dir)), render(ctx(r.dir)))
        self.assertNotIn("2026-08-05", render(ctx(r.dir)))  # no run date

def test_three_states_are_distinguished(self):
    # stamped / unstamped / scaffolded each appear with their own label
```

- [ ] **Step 2: Run to verify it fails.**
- [ ] **Step 3: Implement.** Sort every collection. Emit the tool version, never a date. Each doc row carries `stamped` / `unstamped` / `scaffolded`.
- [ ] **Step 4: Run tests, expect PASS.**
- [ ] **Step 5: Commit** — `feat(tool): deterministic DOCMAP generation`

---

### Task 10: Runner, profiles and CLI

**Files:**
- Create: `tool/project_standard/runner.py`, `tool/project_standard/cli.py`
- Test: `tool/tests/test_runner.py`

**Interfaces:**
- Consumes: every checker module.
- Produces: `run(repo, profile) -> Report(findings, skipped)`; CLI flags `--repo`, `--only`, `--fleet`, `--json`, `--profile`, and the `check` / `generate` / `routes` subcommands.

- [ ] **Step 1: Write the failing tests.**

```python
def test_ci_profile_skips_hook_and_history_checks(self):
    rep = run(repo, profile="ci", has_history=False)
    self.assertIn("11", rep.skipped)
    self.assertIn("5", rep.skipped)
    self.assertEqual(rep.exit_code, 0)   # skipped never fails

def test_error_sets_exit_1_and_warn_does_not(self):
    ...

def test_only_filter_narrows_findings(self):
    ...
```

- [ ] **Step 2: Run to verify it fails.**
- [ ] **Step 3: Implement.** A registry maps check id → callable + the profiles it runs in. Output is ranked error-first, then warn, then a skipped summary.
- [ ] **Step 4: Run tests, expect PASS.**
- [ ] **Step 5: Commit** — `feat(tool): runner with dev and ci profiles, and honest skip reporting`

---

### Task 11: Fleet smoke test

**Files:**
- Create: `tool/tests/test_fleet_smoke.py`

- [ ] **Step 1: Write the test.** It runs against the real repos when they exist and skips cleanly when they do not, so the suite stays portable.

```python
FLEET = Path.home() / "projects" / "apps"

@unittest.skipUnless(FLEET.is_dir(), "fleet not present")
def test_every_real_repo_runs_without_crashing(self):
    for repo in sorted(p for p in FLEET.iterdir() if (p / ".git").exists()):
        with self.subTest(repo=repo.name):
            rep = run(repo, profile="dev")
            self.assertIsInstance(rep.findings, list)
```

- [ ] **Step 2: Run it.** Every defect found during design came from real repos; this is the test that keeps that true.
- [ ] **Step 3: Commit** — `test(tool): smoke the whole fleet, since fixtures encode only what we believe`

---

### Task 12: Templates

**Files:**
- Create: everything under `templates/`

- [ ] **Step 1:** Write each template with `<!-- TODO(project-standard): ... -->` tokens for every unwritten field and **no plausible placeholder prose**. The agent-contract template includes the `## project-standard` block with `adopted`, `critical-paths` and the baselines.
- [ ] **Step 2:** Add a test asserting every template contains at least one token and no template contains a trust stamp (check 25 must not fire on a fresh scaffold).
- [ ] **Step 3: Commit** — `feat(templates): skeletons that admit what they do not know`

---

### Task 13: SKILL.md and references

**Files:**
- Create: `SKILL.md`, `references/*.md`

- [ ] **Step 1:** Write `SKILL.md`: frontmatter with a trigger description, the three modes, when to run the CLI versus the semantic checks, the five semantic checks, and the "I do now / you do" output contract.
- [ ] **Step 2:** Write the references, extracting from the spec rather than restating it.
- [ ] **Step 3:** Symlink into `~/.claude/skills/` and confirm it appears.
- [ ] **Step 4: Commit** — `feat(skill): project-standard orchestrator and references`

---

## Self-Review

**Spec coverage:** all 47 checks map to a task — 1/2/30 → Task 4; 3 → Task 9; 4/12/13/18/19/22–28/36 → Task 5; 5/15/29/37/37b/38 → Task 6; 6 → Task 3; 7/8a–8d/9/11/11b/14 → Task 7; 10a–10d → Task 8; 16/17/20/21/31–35 → Tasks 4–7 by owner module. The three modes and baselines are Tasks 10 and 13.

**Deferred, and stated rather than silently dropped:** `setup` and `init` write operations are Task 13's interactive flow and are driven by the skill, not the CLI — the CLI never mutates a repo in this plan. Per-workspace monorepo validation stays out of scope per the spec.

**Type consistency:** `check(ctx) -> list[Finding]` is uniform across all checker modules; `ctx` carries `repo`, `git`, `tracked`, `contract`, `resolved`. `Severity` strings are `"error" | "warn" | "skipped"` everywhere.
