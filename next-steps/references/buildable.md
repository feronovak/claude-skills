# What counts as a next step

A next step is work that can be **built** — code, config, docs, a deploy. A
backlog also collects things only its owner can do, and those are not next
steps for development. Mixing the two is how a release plan ends up holding
work nobody on the delivery side can start.

## The test

A row is **buildable** if all of it can be done by someone with the repository,
the credentials already in place, and a terminal.

A row is **yours** if any of it needs:

| Needs | Example |
|---|---|
| Money | a paid tier, a subscription, a spend decision |
| A credential action | rotating a key, creating an account, granting access |
| A third party | a support ticket, a contract, another team |
| A physical act | plugging in a cable, re-terminating one, moving hardware |
| A product or policy call | which vendor, whether to spend, what the rule is |
| A console only the owner reaches | a SaaS admin UI, a bank, a registrar |

The line is **capability, not effort**. A twenty-hour migration is buildable. A
two-minute credential rotation is not.

Where a tool is deliberately withheld from the assistant — a user-only CLI, a
blocked hook — the work is the owner's by construction, whatever it looks like.

## Where they go

Non-buildable rows move to a `## Yours` section at the end of the backlog,
under a one-line note saying what the section is for. They carry **no priority
band**: the scale scopes a release, and these are not in one. Order them
most-consequential first, and say what each one unblocks.

Never delete a row to get it out of the way. Moving it is the point — the work
still matters, it is just not development's to schedule.

## Mixed rows

A row that is mostly buildable but waits on the owner stays **one row**, in
place, and is scoped normally. The build order marks it `blocked by you` and
names what is needed. Splitting it would scatter one piece of work across two
sections.

Judge by where the substance sits. If the buildable part is the work and the
human part is a gate, it is a mixed row. If the human part *is* the work, it
belongs under `## Yours`.

When the buildable part is trivial and the gate is substantive, ask which one a
reader would call *the work*. If removing the human decision leaves a task not
worth a backlog row on its own, the row is theirs. A config flip behind a spend
decision belongs under `## Yours`; a week of migration behind a five-minute
access grant is a mixed row.
