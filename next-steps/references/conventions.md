# The project's priority scale

The skill writes its verdict in the vocabulary the project already uses. It
never imports one. Two projects that both ran a round should each still read
like themselves.

## Finding the scale

Two questions, in this order. The second is the one that gets skipped.

### Is there a repeated marker?

1. **A legend line.** A line near the top of the backlog beginning `Priority:`,
   `Legend:` or similar, naming the bands. This is the most reliable signal and
   the one to trust.
2. **The rows themselves.** A prefix repeated across rows — `P0`/`P1`/`P2`,
   `[high]`/`[med]`/`[low]`, `**Must**`, `🔴`/`🟡`/`⚪`, `!!!`/`!!`/`!`. Three
   bands is the common shape; two or four are both fine.
3. **Nothing.** The rows carry no marker at all — bare bullets or checkboxes.

### Is that marker a priority scale?

**A repeated prefix is not automatically a priority scale.** Projects band their
rows by severity, size, effort, confidence or area using exactly the same shape.
`P0`/`P1`/`P2` is the ambiguous one: it is as often severity as priority, and
the two are indistinguishable from the shape alone. Never decide from the shape.

The tell is what a band *asserts about a row*:

| The band answers | It is | Example wording |
|---|---|---|
| when this ships | priority | "near-term", "this release", "later", "until-trigger" |
| how bad it is if left undone | severity | "a buyer is shown something wrong" |
| how big it is | size / effort | "under a day", "multi-week" |
| how sure we are | confidence | "confirmed", "suspected" |
| what it touches | area | "billing", "auth" |

Read the legend's own words, and the band headers where the file groups rows
under them. A band that describes a *consequence* is severity, not priority —
the row's consequence does not change when the schedule does.

Where the file says so outright — *"the `P0`–`P5` bands are SEVERITY, not release
scope"* — that is the answer, and no inference is needed. Files that carry that
sentence usually carry the corollary too: *never move a row between bands to
record that it is in or out of a release.* Honour it.

### When the marker is not a priority scale

**Never write into it.** Rewriting a severity band to record release scope makes
the file assert something false — that the consequence of leaving a row undone
has changed, when only its schedule did. It also destroys the severity reading,
which nothing else in the file records.

Instead:

1. **Look for the release-scope layer that already exists.** A file that bands
   by severity usually scopes releases somewhere else: a `## Release 0.19.0`
   section, a per-row `*0.19.0 — Batch 2.*` line, a milestone column. Where one
   exists, that is where this round writes, in whatever form it already uses.
2. **Where none exists, treat the file as having no priority scale.** Step 4
   asks before adopting one, and the markers it settles on are written
   *alongside* the existing ones, never over them.

Report the non-priority marker by name either way, so the user can see the round
read it and left it alone.

### Reporting

Report which outcome you found, what the bands are, and — where a marker exists
— whether it is a priority scale or something else. A misread scale corrupts
every row the round writes.

## Mapping onto it

Fit the four letters to the bands the project has:

| Bands | Must | Should | Could | Won't — this release |
|---|---|---|---|---|
| Two | top | top | lower | lower |
| Three | top | middle | lowest | lowest |
| Four | top | second | third | fourth |
| More than four | top | second | third | fourth |

Where the project's bands carry their own meaning, honour it. A band labelled
"until-trigger" is a lowest band, not a middle one, whatever its position.

**Beyond four bands, the letters reach only the top four.** Rows sitting below
the fourth band keep their marker untouched — say which bands those are and how
many rows they hold, so the omission is visible rather than silent. A five-or-
more-band scale is also the strongest hint that the bands are not priorities at
all; re-run the test above before mapping anything.

## When there is no scale

This covers both shapes: a file with no marker at all, and a file whose only
marker turned out not to be a priority scale and which carries no release-scope
layer either.

**Ask before adopting one.** Offer the project a choice — MoSCoW words
(`**Must**`, `**Should**`, `**Could**`) are the safe default because they need
no legend to be understood, but the user may prefer their own.

Once chosen, **write a legend line at the top of the backlog** so later rounds
read the choice back instead of asking again:

    Priority: **Must** ships this release · **Should** if it fits · **Could** if there is room

Never adopt a scale silently. Introducing a symbol vocabulary into someone
else's repository without asking is the same failure as re-ordering their
backlog without asking.

## Worked examples

### A priority scale

A file whose legend reads:

    Priority: 🟥 near-term · 🟧 scheduled · ⬜ backlog / until-trigger

Every band answers *when this ships*, so it is a priority scale. Three bands:
Must writes 🟥, Should writes 🟧, and both Could and Won't-this-release write ⬜.

### A marker that is not one

A file whose bands read:

    P0 — a buyer is shown something wrong
    P1 — a buyer is blocked
    P2 — nothing breaks and nobody is misled

Same `P0`/`P1`/`P2` shape, and it is **not** a priority scale: every band names a
consequence, not a schedule. Nothing here is written. The round looks for the
file's own release layer — a `## Release 0.19.0` section, a `*0.19.0 — Batch 2.*`
line under a row — and writes there instead, reporting that the `P0`–`P2` bands
are severity and were left untouched.

Two files can carry an identical marker and take opposite treatment. The shape
never decides it; the band's own words do.

Nothing about this changes how the round is conducted. The letters are the
round's language; the bands are the file's. A project with no scale is still
reasoned about in MUST/SHOULD/COULD — the only open question is what those
letters become on disk.
