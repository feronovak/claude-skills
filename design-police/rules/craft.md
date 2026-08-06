# Craft — the pass that thresholds cannot do

Every rule in the other files is a number. A page can satisfy all of them and
still be bad, because the numbers check whether elements are *legal*, not
whether the composition *works*. This file is the part of the audit that only
happens by looking.

Run this from the screenshots, after the computed pass, at every viewport.

## Why this exists

The failure it prevents: a page returns PASS — spacing on-scale, contrast above
floor, no anti-patterns — and the person who asked still looks at it and sees
something obviously amateur. If that happens, the audit was worthless to them,
however many checks it ran. A verdict nobody believes is worse than no verdict.

## The questions

Answer each one from the screenshot. Each has a defect condition — something
observably wrong, not a preference. Cite what you saw.

**1. Focal point.** Squint at the screenshot until detail disappears. What is
still legible? That is the focal point. Does it match the one thing this page
exists to do?
→ *Defect:* nothing survives the squint (everything is the same weight), or the
loudest element is not the important one.

**2. Hierarchy vs. importance.** Rank the elements by visual prominence, then by
actual importance to the reader. Do the two orders match?
→ *Defect:* the ordering is inverted — decoration outranks the action, or a
utility link is heavier than the headline.

**3. Grouping.** Related things should sit closer together than unrelated
things. Measure the gaps if you're unsure.
→ *Defect:* the gap *inside* a group is >= the gap *between* groups, so the
reader cannot tell what belongs with what.

**4. Alignment.** Count the distinct left edges down the page.
→ *Defect:* edges that are close but not equal (a 4px stagger reads as a
mistake; a 40px indent reads as a decision).

**5. Density.** Is anything cramped against a boundary, or marooned in space
with no relationship to its neighbours?
→ *Defect:* text touching a container edge, or an element floating alone in a
region with no alignment to anything.

**6. Orphans and awkward wraps.** A heading breaking one word onto its own
line, a widow, a lone item on a final row.
→ *Defect:* only when it is **stranded**, not merely uneven. An uneven last row
is the ordinary arithmetic of a responsive grid — 3 cards in a 2-column
reflow leaves one on its own at some width, on almost every site ever built,
and calling that a failure destroys trust in the whole report. It is a defect
when the orphan is *visibly wrong*: stretched full-width so it reads as a
different component, leaving a hole mid-layout, or a headline whose last word
drops alone under a wide empty line.

**7. Consistency.** Two controls that do the same kind of job should look the
same. Two that do different jobs should look different.
→ *Defect:* same job, different treatment — or worse, different job, identical
treatment, so the destructive action looks like the safe one.

**8. Designed or defaulted?** Unstyled `<select>`s, default-blue links next to a
custom palette, one browser-default focus ring among custom ones, three
different border radii.
→ *Defect:* the page mixes styled and unstyled treatments of the same element
type, so it reads as unfinished rather than deliberate.

## Reporting

A craft finding is either a **BLOCKER** or a **POLISH** note. There is no
middle band, deliberately: "a bit off, worth a DEFECT" is where invented
problems live, and a nitpick promoted to a failure costs more credibility than
it buys. Ask one question — *is the composition actually broken?* If yes it is a
blocker; if it is anything less, it is polish, and polish never changes the
verdict.

Hold yourself to a higher bar here than on the numeric checks, because this is
the one place where you could invent a problem:

- **Name the element and the evidence.** "The three feature cards use 24px
  internal padding but 12px between cards, so they read as one block" — not
  "spacing feels off".
- **Defect, not preference.** If a competent designer could have chosen it on
  purpose, it is not a failure. Serif body copy is a choice; 4px of stagger
  between two left edges is a mistake.
- **At most 3 craft blockers per page.** If you believe there are more, you are
  describing a redesign, not auditing a build — report the worst 3 and say so.
- **A page that is merely plain is not failing.** Restraint is a legitimate
  design choice. Reserve blockers for composition that is broken, and put every
  "I'd have done it differently" under Polish where it belongs.

## The closing note

After the verdict, whether PASS or FAIL, answer one more question and report it
under **Polish** as a single non-blocking line:

> If everything here passed, what is the one thing an art director would still
> change?

This is not a failure and must never affect the verdict. It exists because
"technically compliant and slightly lifeless" is a real state, and the person
reading the report would rather hear it than not.
