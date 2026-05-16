# business-sharks-screen

Ultrafast idea triage. One idea, 2-3 minutes, one decision: **KILL / MAYBE / PROMOTE**.

## Why this exists

A full `business-sharks` run is thorough — and not free. When you're sifting many raw ideas (Reddit threads, shower thoughts, a notes file), you don't want to spend a full run on each. You want a cheap gate that kills the obvious losers fast and flags the few worth real research.

`business-sharks-screen` is that gate. It runs **inline** — no team, no subagents — with a **hard cap of 6 web searches**, aimed only at the three things that actually kill ideas: it's a known **tarpit**, the **problem isn't real**, or it's **already solved cheaply**. Same defensive rigor as the full skill, scoped to the decisive 20%.

## Invoke

Triggers on quick-triage language:

- "Quick screen this idea: an AI tool that summarizes city council meetings"
- "Is this worth a deep dive — a marketplace for used lab equipment?"
- "Triage this before I do a full validation: ..."

## What you get

- A **verdict** — KILL / MAYBE / PROMOTE — with a 5-dimension screen scorecard, the reasons, and the single biggest kill risk.
- A row appended to **`triage-log.md`** in your working directory, so you can compare every idea you've screened and pick winners.
- On PROMOTE: a **`*-screen-seed.md`** file that `business-sharks` auto-detects and uses as a warm start — the full run stress-tests the screen's findings instead of redoing them.

## Heads up

- **This is not validation.** No TAM math, no financials, no GO/NO-GO. The screen decides *whether to bother* — `business-sharks` does the real work.
- **KILL-biased on purpose.** Most ideas should not survive a screen. If most do, something is wrong.
- **Pairs with the pipeline:** `business-sharks-screen` → `business-sharks` → `app-factory`.

Full procedure: see `SKILL.md` and `references/screen-rubric.md`.

---

Built by [Fero Novak](https://feronovak.com). Part of [feronovak/claude-skills](https://github.com/feronovak/claude-skills).
