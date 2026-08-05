# Git hygiene

## Attribution — five markers, not one

**This is a house rule with a default, not a universal truth.** It is on by
default because the tooling appends these markers unless told otherwise, so a
silent repo gets the marker rather than its absence. A repo that wants the
attribution declares `ai-attribution: allow` and every check below stands down.

The harness appends several independently. Guarding only the trailer leaves the
rule half-enforced, and the session line is the one that actually got through:
one repo carries three in its last 200 commits, in messages with no trailer.

| Marker | Where | Guard |
|---|---|---|
| `Co-Authored-By: Claude …` | commit message | `commit-msg` |
| `Claude-Session: https://claude.ai/code/…` | commit message, separate from the trailer | `commit-msg` |
| `Signed-off-by:` naming Claude or Anthropic | commit message | `commit-msg` |
| author / committer identity | commit metadata, invisible to `commit-msg` | `pre-commit`, via `git var` |
| `🤖 Generated with Claude Code` | pull request body | **none — git hooks never see PR bodies** |

The last row has no mechanical enforcement anywhere. It is checked by eye. A
guard that does not exist is never claimed to.

## Where the guards live

Install them with `project-standard install-hooks`, which copies both guards
into a directory and points `core.hooksPath` at it.

A hook placed in a repo's own `.git/hooks` never fires when `core.hooksPath` is
set elsewhere. Any setup that assumes otherwise installs one dead file per repo
while a naive "the file exists" check reports green.

A local `core.hooksPath` override pointing at a directory without the guards
disables every hook silently — that is check 11b, and it is easy to create by
accident when a repository is renamed or moved.

## Scope: the two rules differ

| Rule | Scope | Why |
|---|---|---|
| No Claude attribution | every repo, unconditionally | personal policy, true everywhere |
| Local-only paths stay untracked | only repos that opted in | `logs/` and `test_results/` are legitimately tracked in some repos, including employer work |

A repo opts in by carrying `# project-standard: local-only` in `.gitignore` or
the vendored checker in `scripts/project_standard/`. Blocking `logs/` everywhere
would stop a legitimate commit, and a guard that does that gets disabled
wholesale — taking the secret scan with it.

## The local-only set

Split by how universal it is. `local-only:` in the contract extends the set,
`local-only: [replace, ...]` swaps it, and `track-anyway:` keeps a default path
tracked — some repos track `logs/` on purpose, and being told that is wrong is
how a guard gets disabled wholesale.

```
docs/exec-summaries/   session-notes/   logs/   test_results/
.agenthub/   .playwright-mcp/   .interface-design/   .cursor/   .ruff_cache/
.claude/settings.local.json   .claude/worktrees/   .claude/scheduled_tasks.lock
```

Plus filename patterns (`*EXEC*SUMMAR*`, `*-exec-summary*`, `*SESSION-NOTES*`)
as **warns**, because exact paths miss a summary written outside the convention
and a filename is a hint rather than proof.

Tracked: `docs/superpowers/`, `think-day-*/`, `dev-day-*/`, `.claude/agents/`,
`.claude/skills/`.

## History is not rewritten

A currently tracked local-only file is an error — un-tracking needs no rewrite.
A marker in history before the `adopted` baseline is a warn. Rewriting history
across the fleet to remove executive summaries is a large, disruptive operation
in service of tidiness rather than a leak.

## Secrets

**This standard does not scan for secrets, on purpose.** A partial pattern list
presented as a gate gives false confidence, which is worse than no gate, and
secret scanning has mature dedicated tools. Configure one — gitleaks,
detect-secrets, trufflehog — and commit its config; check 40 recommends one and
goes quiet as soon as it sees any of them.

What the standard does assert is where secret *values* may live:

| | |
|---|---|
| never | the agent contract, a skill, a template, or any tracked document |
| never | the machine-readable block — it holds paths and references, not values |
| the pattern | keep the real file gitignored, commit a redacted mirror whose values read `REPLACE_ME` |

Check 41 backs the first row and nothing more: it reads tracked documentation
and warns when a string is shaped like a live credential. It is documentation
hygiene, not a scan, and it never reports a repository as clean.

Out of scope, stated rather than implied: assistant configuration and memory
held outside the repository, and any file the checker cannot see.
