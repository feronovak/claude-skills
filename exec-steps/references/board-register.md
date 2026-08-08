# Board register — how to write the summary

The reader is intelligent, busy, and does not know the codebase. They will not ask a
follow-up question. Everything they need to act is on the page or it does not reach
them.

## The binding rule, before anything else

**The narrative may assert as fact only what reached Done.**

Partial items are written as explicitly in progress. Claimed-unverified and Blocked
items never appear as achieved outcomes anywhere in the Executive Summary — not in
*What*, not in *Value*, not in the headline.

This is the rule that makes the rest of the document worth writing. A Status table
reading "Claimed, unverified" above a *What* section reading "failures are now visible
the moment they happen" is a dishonest document, and the board reads the prose, not
the table.

Write one Why / What / How / Value block per workstream, not one per run.

## Why

The problem or opportunity, in business terms. One or two sentences.

- **Good:** "Two automated systems were failing silently — work appeared to complete
  while producing nothing, with no signal that anything was wrong."
- **Bad:** "The completion ping wasn't firing on channel-root answers."

The second sentence describes a symptom in implementation vocabulary. The first
describes why anyone outside the room should care. *Why* answers "what was at stake",
never "what was broken in the code".

## What

What now exists that did not before. Outcomes, not activities.

- **Good:** "Failures are now visible the moment they happen rather than discovered days later."
- **Bad:** "Added a status report library and moved three scheduled jobs onto it."

Activities describe motion. Outcomes describe a changed state of the world. If a line
could appear on a timesheet, it is an activity — rewrite it.

## How

The approach, one paragraph, no jargon. Enough that the reader can picture the shape
of the solution and answer "was this a sensible way to do it?" — not enough to
reimplement it. Name a technology only when the choice itself was the decision.

## Value

Exactly **one** of four types. Pick the one that dominates; do not list all four.

| Type | Reads like |
|---|---|
| Money | Cost removed or revenue enabled, with the figure's source. |
| Time saved | Hours removed from someone's week, and whose. |
| Risk removed | A specific failure that is now prevented, or now caught. |
| Capability gained | Something now possible that was not. |

### The quantification rule

**Never invent a figure, and never smuggle one in as a magnitude claim.**

No number, ratio, multiplier, or comparative magnitude appears unless it was actually
measured in the evidence. That covers the obvious cases and these evasions, all of
which read as compliant and are not:

- **Vague quantifiers** — "roughly halved", "~2x", "an order of magnitude faster",
  "several hours a week". A hedge word does not make an unmeasured number honest.
- **Bare comparatives** — "markedly faster than before", "substantially more reliable",
  with no measurement anywhere. If nothing was measured, there is no comparison.
- **Laundered estimates** — a figure the user guessed aloud, then printed as board
  fact. Permitted only with its source attached inline: *(owner's estimate, unmeasured)*.
- **Activity counts dressed as impact** — "40 files changed", "12 commits". That is
  motion, not value. It never appears in the Value line.

When there is no honest figure, write exactly this shape:

> **Value:** Risk removed — silent failures are now surfaced rather than discovered by
> accident. *Unquantified; would need failure-frequency data from the last quarter to size.*

That construction does two things a fabricated metric cannot: it stays credible under
challenge, and it tells the reader what to measure next. A made-up percentage in a
board pack is worse than an acknowledged gap — it is the sentence that destroys trust
in every other line on the page.

## Next steps

Each step carries an **owner** and a **horizon**: now / this week / this month. Order
by what should happen first, not by size. Split into two groups:

- **I do** — steps the assistant can execute.
- **You do** — steps requiring the user's decision, access, or authority.

A next step with no owner is a wish. A next step with no horizon never happens.

## Banned vocabulary

These words signal a machine wrote the text and drain it of meaning. None appears in
the output:

leverage · robust · streamline · seamless · synergy · best-in-class · cutting-edge ·
game-changer · unlock · empower · holistic · delve · landscape (figurative) ·
journey (figurative) · in today's fast-paced · it's worth noting that ·
comprehensive solution · significantly enhance

Also banned: **em-dash-heavy triads** ("faster, cleaner, smarter"), sentences opening
with "By leveraging", and any claim of transformation not backed by an artifact.

## Register discipline

The Executive Summary contains **no repo names, no commit hashes, no file paths, no
tool names**. A board reader never meets the word `systemd`, `cron`, or `rsync`. All
of it lives in the Evidence Appendix, which is where a technical reader goes and
where a challenge gets answered.

Write short sentences. Prefer the concrete noun to the abstract one. When a sentence
can lose a clause and keep its meaning, drop the clause.
