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

Canonical, version-controlled, in `~/.claude/git-hooks/`, reached by
`core.hooksPath`. A hook vendored into a repo's own `.git/hooks` never fires
when `core.hooksPath` is set — and it is set globally here, so the vendored
approach would install one dead file per repo while the check that confirmed
the file existed reported green.

A local `core.hooksPath` override pointing at a directory without the guards
disables every hook silently. That is check 11b, and it has happened twice.

## Scope: the two rules differ

| Rule | Scope | Why |
|---|---|---|
| No Claude attribution | every repo, unconditionally | personal policy, true everywhere |
| Local-only paths stay untracked | only repos that opted in | `logs/` and `test_results/` are legitimately tracked in some repos, including employer work |

A repo opts in by carrying `# project-standard: local-only` in `.gitignore` or
the vendored checker in `scripts/project-standard/`. Blocking `logs/` everywhere
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
in service of tidiness rather than a leak. Secrets are a different matter and
belong to `secrets-audit`.
