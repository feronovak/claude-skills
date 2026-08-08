# MoSCoW, scoped to a release

## Why the boundary matters

MoSCoW is a commitment scale measured against a fixed scope boundary. Without
one, every item drifts to Must and the letters stop carrying information. The
boundary is **the next release** — never a calendar window. "Two weeks" is not
a release; it is a guess about how long one takes.

**Versioned repo** — the boundary is the next version bump. Read it from the
manifest (`package.json`, `pyproject.toml`, `Cargo.toml`, a `VERSION` file).

**Unversioned repo** — there is no bump to point at, so the boundary is "the
next block of work". Say this out loud in the round. A soft cut-off is still
usable, but the user must not be left thinking the round carries discipline it
does not.

## The four letters

| Letter | Means |
|---|---|
| **Must** | The release does not ship without it. |
| **Should** | Goes in if it fits. Its absence is a disappointment, not a failure. |
| **Could** | Only if everything above lands with room to spare. |
| **Won't** | Explicitly out. Two flavours — see below. |

**Where the boundary is soft**, "the release does not ship without it" has no
ship event to test against. Use consequence-of-omission instead: if this is
still undone when the block of work ends, does something stay broken, unsafe,
or blocked for somebody? That is a Must. If the honest answer is that it would
merely have been good to have, it is a Should.

**Won't has two flavours and they are not interchangeable:**

- **Won't — this release.** Still wanted, just not now. Stays in the backlog.
- **Won't — ever.** Dead. The row is deleted.

Never collapse the second into the first to avoid a deletion. An item nobody
will ever do, left in the backlog, costs a re-read every future round.

**Could and Won't-this-release are the pair that blur.** The test: a Could is
something you would genuinely pick up if the release ran light. A
Won't-this-release is something you would not start even with room to spare,
because its time has not come. If spare capacity would not tempt you, it is
Won't.

## Writing the verdict back

| Verdict | Effect on the backlog |
|---|---|
| Must | the project's top band |
| Should | its middle band |
| Could | its lowest band |
| Won't — this release | its lowest band, demoted if the row currently sits higher |
| Won't — ever | row **deleted**, one explicit confirmation for that row |
| Already done | row **deleted**, same per-row confirmation |

Bands are whatever the project already uses — see `references/conventions.md`.
In a file whose legend reads `Priority: 🟥 near-term · 🟧 scheduled · ⬜ backlog`,
the top band is 🟥 and the lowest is ⬜.

**Already done is not a proposal-time verdict.** Every item gets one of the four
letters at Step 1. Already-done surfaces only at Step 2, when a correction turns
out to mean the work already shipped.

The letters themselves do not persist. They are the round's verdict; their only
effect is to move the standing marker. One scale survives in the file, so there
is no second column to maintain and nothing that can disagree with itself.

**Could and Won't-this-release both land in the lowest band.** A three-band
scale cannot carry four letters. The collapse is accepted, not solved — the
standing scale is deliberately coarser than the round's verdict. Where the
difference matters, the inline comment carries it:

    *Could: if the release has room after the ACL lands.*

Do not invent an extra band. That would add a symbol to every backlog in the
fleet to record a state that lasts one round.

**A row reported as already shipped is deleted, not marked done.** A roadmap
holds future work only; completed items leave rather than moving to a
done-section.

## The 60% guard

Where the backlog carries effort estimates (`~1 hr`, `2–3 hr`), sum them. The
denominator is the work going **into** the release — Must plus Should plus
Could. Won't rows are out of scope and are not counted. Could rows count here
even though `release-plan.md` leaves them out of the build order. That is
deliberate: the guard asks what share of the release's work is mandatory, and a
Could is work you have said you would take if there is room. Normalise mixed
units to hours before summing. If the Musts exceed **roughly 60%** of that
total, say so, name the rows you summed, and say what should drop.

This is the only mechanical defence against everything becoming Must, and it is
the reason to read the estimates rather than skim past them.

**Where estimates are absent, say the guard cannot be checked.** Do not
estimate the items yourself to make the arithmetic possible. A percentage
derived from invented figures looks exactly like a percentage derived from real
ones, and that is the failure this instruction exists to prevent.

**Where only some rows carry estimates, the guard cannot be checked either.** Say
so, and say how many rows are unestimated. A sum over the rows that happen to
carry numbers is a percentage of the wrong denominator, and it looks exactly like
a real one.

## Comments

Comments land inline under the row they belong to, in the present tense:

    - 🟧 **OpenClaw as non-root** (2–3 hr). Turns the allowlist from a
      speed-bump into a real boundary.
      *Held: not before the off-site backup lands.*

Never a dated narrative. "Held, and why" is current state. "Deprioritised on
2026-08-08" is changelog, belongs in a history file, and will trip the
`doc-state-guard.py` hook.
