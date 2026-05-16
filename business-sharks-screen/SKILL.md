---
name: business-sharks-screen
description: Ultrafast single-idea pre-screen — a 2-3 minute go/no-go gate before committing to a full business-sharks validation. Use this skill when the user wants a quick triage on a raw idea, asks "is this worth a deep dive", "screen this idea", "fast check on this", "triage this idea", "should I bother researching X", "quick screen before full validation", or is sifting many candidate ideas (e.g. from Reddit) to decide which few deserve a real run. KILL-biased by design — most ideas should not survive.
version: "1.0"
authors: Fero Novak <https://feronovak.com>
---

Run an ultrafast triage screen on ONE business idea. The output is a single decision: is this idea worth the cost of a full `business-sharks` validation, or should it die now? Inline, no team, no subagents, hard cap of 6 web searches.

The idea to screen is: $ARGUMENTS

## What This Is — And Is NOT

**This IS:** a cheap, fast kill-or-promote gate. You sift many ideas through it and only a few survive. A screen that promotes most ideas is broken.

**This is NOT validation.** No TAM math, no financial model, no 13-dimension scorecard, no team of analysts. That is the `business-sharks` skill. The screen exists so you don't spend a full run on ideas that any honest 6-search look would have killed.

If the user wants depth, real numbers, or a GO/NO-GO verdict — that is `business-sharks`, not this skill. Say so and stop.

## Defensive Principles (non-negotiable)

These are carried from `business-sharks` and override all other behavior:

1. **NEVER ASSUME** — if the idea is vague on a dimension, flag "INSUFFICIENT SIGNAL" and score that dimension low. Do NOT fill gaps with optimism.
2. **RATE HONESTLY** — a 3/10 is a 3/10. The screen's whole value is killing weak ideas cheaply.
3. **NO CHEERLEADING** — your job is to find the reason this dies before the user wastes a full run on it.
4. **CITE SOURCES** — tag every factual claim: **FACT** (found in search), **INFERRED** (reasoned from comparables), **ASSUMPTION** (modeled, no data). The reader must always know which.
5. **KILL BIAS** — when the signal is genuinely ambiguous after 6 searches, that ambiguity is itself a finding. Lean MAYBE or KILL, never PROMOTE on hope.

## The Screen Procedure

Linear. Run it top to bottom. Do not parallelize, do not spawn agents.

### Step 1 — Frame the idea (0 searches)
Extract in 3-4 lines: what it is, the target customer, the business model, the core problem it claims to solve. If the idea is too vague to screen at all, ask the user ONE clarifying question, then proceed. Never ask more than one — this is a fast screen.

### Step 2 — Tarpit check (0 searches)
Match the idea against the condensed tarpit list in `references/screen-rubric.md`. A tarpit is an idea that generates enthusiasm but historically resists retention, monetization, or scale.
- If it matches a pattern, it must show a **structural escape** (new technology, behavioral shift, regulation, or a concrete proprietary-data flywheel). "We'll execute better" is not an escape.
- No escape → strong KILL signal. Matches 2+ patterns → "DOUBLE TARPIT" → KILL outright, you may stop here.

### Step 3 — Bounded research (HARD CAP: 6 searches, target 4-6)
Spend searches ONLY on the three decisive kill factors. Count every search. Suggested allocation:
- **1-2 — Already exists / saturation:** `"[idea] software"`, `"best [category] for [persona]"`, `"[competitor] alternatives"`
- **1-2 — Problem reality:** `"[problem] reddit"`, `"[problem] forum"`, complaints / Quora threads — looking for OBSERVED pain expressed unprompted
- **1 — Solved cheaply:** is there a free or near-free alternative that covers 80% of the pain?
- **1 — Adaptive:** spend on the single biggest remaining unknown

STOP at 6. If you are still unsure, that is a finding ("INSUFFICIENT SIGNAL"), not a license for a 7th search.

### Step 4 — Score the screen scorecard
Score the 5 dimensions in `references/screen-rubric.md`, 1-10 each. Apply the Defensive Principles to every score.

### Step 5 — Verdict
Apply the verdict thresholds in `references/screen-rubric.md`: **KILL / MAYBE / PROMOTE**.

### Step 6 — Output to the user
Print the verdict block using the exact format in `references/screen-rubric.md`.

### Step 7 — Append to the triage log
Append one row to `triage-log.md` in the current working directory (create the file with its header if it does not exist). Format in `references/screen-rubric.md`. This log is how the user compares ideas across many separate screens.

### Step 8 — Seed file (only if PROMOTE, or if the user asks)
Write `{idea-slug}-screen-seed.md` in the current working directory using the seed format in `references/screen-rubric.md`. This is the handoff into a full run — see below.

## Promoting to a Full Run

When the verdict is PROMOTE, tell the user plainly: *"Run `business-sharks` in this folder — it auto-detects the seed file and uses the screen findings as a warm start."*

The full `business-sharks` skill has an INPUT TRIAGE branch that detects `*-screen-seed.md`, uses it as the starting idea, and hands the screen's research to its analysts with the instruction to **challenge and extend** it — never to trust it. Six searches is a screen, not validation.

Do NOT invoke `business-sharks` yourself. The user runs it when they choose.

## Speed Rules (the point of this skill)

- **Inline only.** No team, no subagents, no Task tool. The team machinery is what makes the full skill slow.
- **Hard cap 6 searches.** Count them out loud in your reasoning. Do not rationalize a 7th — see Common Mistakes.
- **At most one file written** per run (the seed), plus the one-row log append. No project folder — `business-sharks` owns that.
- **No deep analysis.** No TAM math, no unit economics, no financial projections. If you catch yourself modeling LTV, stop — that is the full skill's job.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Doing a 7th, 8th search "just to be sure" | The cap is the feature. Ambiguity after 6 = MAYBE/KILL, that IS the answer. |
| Promoting because the idea "sounds cool" | PROMOTE is rare. If you're promoting more than ~1 in 4, your kill bias is broken. |
| Filling a vague idea with optimistic assumptions | Flag INSUFFICIENT SIGNAL, score low, move on. |
| Building a mini financial model | Out of scope. The screen judges *whether to bother*, not the economics. |
| Skipping the tarpit check because the idea "feels different" | Run it. Most ideas that "feel different" are textbook tarpits with a fresh coat of paint. |
| Spawning subagents to "do it properly" | That is the full skill. The screen is inline and fast on purpose. |
| Writing a project folder of files | One seed file max. The log gets one row. Nothing else. |
