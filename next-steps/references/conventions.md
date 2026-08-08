# The project's priority scale

The skill writes its verdict in the vocabulary the project already uses. It
never imports one. Two projects that both ran a round should each still read
like themselves.

## Finding the scale

In this order:

1. **A legend line.** A line near the top of the backlog beginning `Priority:`,
   `Legend:` or similar, naming the bands. This is the most reliable signal and
   the one to trust.
2. **The rows themselves.** A prefix repeated across rows — `P0`/`P1`/`P2`,
   `[high]`/`[med]`/`[low]`, `**Must**`, `🔴`/`🟡`/`⚪`, `!!!`/`!!`/`!`. Three
   bands is the common shape; two or four are both fine.
3. **Nothing.** The rows carry no priority signal at all — bare bullets or
   checkboxes.

Report which of the three you found, and what the bands are, as part of Step 0.
A misread scale corrupts every row the round writes.

## Mapping onto it

Fit the four letters to the bands the project has:

| Bands | Must | Should | Could | Won't — this release |
|---|---|---|---|---|
| Three | top | middle | lowest | lowest |
| Two | top | top | lower | lower |
| Four | top | second | third | fourth |

Where the project's bands carry their own meaning, honour it. A band labelled
"until-trigger" is a lowest band, not a middle one, whatever its position.

## When there is no scale

**Ask before adopting one.** Offer the project a choice — MoSCoW words
(`**Must**`, `**Should**`, `**Could**`) are the safe default because they need
no legend to be understood, but the user may prefer their own.

Once chosen, **write a legend line at the top of the backlog** so later rounds
read the choice back instead of asking again:

    Priority: **Must** ships this release · **Should** if it fits · **Could** if there is room

Never adopt a scale silently. Introducing a symbol vocabulary into someone
else's repository without asking is the same failure as re-ordering their
backlog without asking.

## Worked example

A file whose legend reads:

    Priority: 🟥 near-term · 🟧 scheduled · ⬜ backlog / until-trigger

has three bands, so Must writes 🟥, Should writes 🟧, and both Could and
Won't-this-release write ⬜. A file using `P0`/`P1`/`P2` gets exactly the same
verdicts written as `P0`/`P1`/`P2`. The round is identical; only the vocabulary
changes.
