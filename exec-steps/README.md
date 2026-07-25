# exec-steps

Validates what actually got done in a work session, then writes a board-ready
executive summary — Why, What, How, Value — plus ranked next steps.

## Why it exists

At the end of a session there is no reliable answer to two questions: what actually
got done, and what happens next.

The conversation holds intent but overstates completion — "deployed and working" gets
said before the artifact exists. Git holds artifacts but no intent. Neither is
readable by someone outside the room.

The verification step is the point. Without it, this is a formatting exercise.

## Use

```
exesteps                      # this session
exesteps today
exesteps week
exesteps since v2.1
exesteps since <YYYY-MM-DD>
```

Runs against the current working directory's repository. Output is always English,
whatever language the session was in.

## What it does

1. Reads the live conversation for completion claims **and intent** — intent exists
   nowhere else and is the only source for *Why*.
2. Gathers evidence: `git log`, `git diff --stat`, `git status`, session notes,
   named tickets, file-existence checks, cheap read-only health checks.
3. Assigns each claim one of four states — **Done**, **Partial**,
   **Claimed, unverified**, **Blocked** — against a fixed evidence standard.
4. Translates to Why / What / How / Value with an owner and horizon on every next step.
5. Emits a chat summary, a dated file, and an index row.

States never upgrade for presentational reasons. A summary reporting three done and
two unverified is more useful than one reporting five done, because the reader knows
which two claims not to repeat in a meeting.

## Output

```
docs/exec-summaries/
  INDEX.md
  <YYYY-MM-DD>-jarvis-completion-ping.md
  <YYYY-MM-DD>-hal9000-context-wall.md
```

Every file opens with YAML frontmatter (`date`, `scope`, `project`, `title`, `topics`,
`status`, `headline`, `evidence`, `source`), so a file can be triaged without being
opened — grepping `topics:` finds every summary on a subject in one pass. Reading
`INDEX.md` alone answers "what shipped this quarter".

Body order is fixed: Executive Summary → Status → Next Steps → Evidence Appendix.

## Rules it will not break

- **No invented numbers.** No percentage, currency figure, or time saving appears
  unless traceable to evidence or stated by the user. Otherwise the word is
  `Unquantified`, plus what measurement would close the gap.
- **No jargon above the fold.** The executive summary contains no repo names, hashes,
  file paths, or tool names. Those live in the evidence appendix.
- **Read-only.** It never deploys, commits, or modifies project code.
- **Gaps are reported.** Evidence it could not gather is stated, not hidden.

## Files

| File | Holds |
|---|---|
| `SKILL.md` | The six-step pipeline |
| `references/validation-rubric.md` | The four states, evidence standards, edge cases |
| `references/board-register.md` | Why/What/How/Value rules, quantification rule, banned vocabulary |
| `references/output-format.md` | File template, frontmatter, index row, chat message |
