# Screen Rubric

All formats, thresholds, and the tarpit list for `business-sharks-screen`. SKILL.md is the procedure; this file is the reference.

---

## Condensed Tarpit List

A tarpit is an idea that generates enthusiasm but historically resists retention, monetization, or scale. The problem is often real — the *business* is not. Match the idea against these patterns in Step 2.

| Pattern | Why it fails | Possible structural escape |
|---|---|---|
| **"LinkedIn / social network for [niche]"** | Network effects need critical mass; a niche can't reach it | An existing captive community migrating in bulk |
| **Discovery / recommendation app** ("find the best [X]") | Discovered once, no retention; Google is free | Proprietary data or a repeat-use trigger |
| **"Uber for [X]"** (on-demand non-urgent service) | Supply economics break; low frequency kills unit economics | Genuinely high-frequency, high-density demand |
| **Habit / mood / activity tracker** | Users quit in 2-4 weeks; low WTP for tracking alone | Tracking is a side effect of a job users already do |
| **Content-creation tool** ("make it easy to create [X]") | Oversaturated; free tools; creators don't pay until they earn | A wedge into a creator workflow with real lock-in |
| **Local two-sided marketplace** | Cold-start in every city; economics don't scale geographically | A single dense geography with a supply lock |
| **AI wrapper for [vertical]** ("AI for [industry]") | Thin layer over commodity LLM APIs; incumbents copy in months | A concrete, specific proprietary-data flywheel — not "we'll collect data" |
| **Aggregator / comparison platform** ("compare [providers]") | Suppliers resist listing, data goes stale, users compare once | Exclusive supply data or a transactional cut |
| **B2B-wrapped consumer tarpit** (sell a churny consumer feature to businesses) | The underlying churn / low-WTP / engagement decay doesn't disappear behind B2B billing | The business buyer has a hard compliance or cost reason to keep paying |

**Rules:**
- Matches a pattern + no credible structural escape → strong KILL signal.
- Matches 2+ patterns → **DOUBLE TARPIT** → KILL outright; you may stop the screen here.
- "We'll execute better" / "better UX" is never a structural escape.

> **Sync note:** this list is a condensed copy of the canonical tarpit table in `business-sharks/references/market-researcher.md`. If one changes, update the other.

---

## The Screen Scorecard (5 dimensions, 1-10 each)

Score each dimension. Apply the Defensive Principles — unknowns score low and get flagged, never assumed up.

| # | Dimension | 1-3 (weak) | 4-6 (mixed) | 7-10 (strong) |
|---|---|---|---|---|
| 1 | **Problem Reality** — painkiller vs vitamin | Nice-to-have, no urgency, INFERRED only | Real but mild or infrequent pain | Urgent, frequent, OBSERVED pain expressed unprompted |
| 2 | **Demand Signal** — is anyone actively looking | No searches, no threads, silence | Some forum chatter, weak search intent | Clear search demand and/or repeated unprompted complaints |
| 3 | **Competitive Space** — room to enter | Saturated, or solved free/cheaply by an incumbent | A few players, no obvious white space | Real gap incumbents ignore or do badly |
| 4 | **Tarpit Risk** — inverted (10 = clean) | Textbook tarpit, no escape | Tarpit-adjacent, weak escape | Not a tarpit pattern at all |
| 5 | **Wedge** — a credible reason this gets a first foothold | "Me-too", no angle | A plausible but unproven angle | A specific non-obvious wedge (distribution, niche, insight) |

**Screen Score = average of the 5 dimensions, to one decimal.**

Moat, financials, and TAM are deliberately absent — they need a full run. The Wedge dimension is a fast proxy for "could this even get started", not a moat assessment.

---

## Verdict Thresholds

Apply in order — the first matching rule wins:

1. **KILL** if ANY of:
   - DOUBLE TARPIT, or a single tarpit match with no structural escape
   - Problem Reality ≤ 3 (it's a vitamin)
   - Screen Score < 4.5
2. **PROMOTE** if ALL of:
   - Screen Score ≥ 6.5
   - No dimension ≤ 3
   - Not an unescaped tarpit
3. **MAYBE** — everything else (Screen Score 4.5-6.4, or high score dragged by one weak dimension).

PROMOTE is meant to be rare. If you are promoting more than roughly 1 idea in 4, re-check your kill bias.

---

## Chat Output Format (Step 6)

Print exactly this block:

```
🦈 SCREEN — <idea in one line>
Verdict: <KILL | MAYBE | PROMOTE>   ·   Score: <X.X>/10   ·   Searches used: <N>/6

| Dimension          | Score | Note |
|--------------------|-------|------|
| Problem Reality    | X/10  | <one line> |
| Demand Signal      | X/10  | <one line> |
| Competitive Space  | X/10  | <one line> |
| Tarpit Risk        | X/10  | <one line> |
| Wedge              | X/10  | <one line> |

Why this verdict:
- <reason 1>
- <reason 2>
- <reason 3 — optional>

Biggest kill risk: <the single thing most likely to sink this>

What a full run must verify: <1-2 bullets — omit entirely if KILL>

<If PROMOTE: "Seed written: <path>. Run business-sharks here for the full validation.">
<If KILL: one blunt line on whether a pivot is even worth thinking about.>
```

Keep notes terse. Tag claims FACT / INFERRED / ASSUMPTION where it matters.

---

## Triage Log Format (Step 7)

File: `triage-log.md` in the current working directory. If it does not exist, create it with this header:

```
# Idea Triage Log

Screened with business-sharks-screen. One row per screen.

| Date | Idea | Verdict | Score | Killer / Note | Promoted |
|------|------|---------|-------|---------------|----------|
```

Then append exactly one row per screen:

```
| 2026-05-16 | <idea, short> | KILL | 3.2 | textbook "Uber for X" tarpit, no escape | — |
| 2026-05-16 | <idea, short> | PROMOTE | 7.1 | real OBSERVED pain, thin competition | ✅ |
```

Append only — never rewrite existing rows.

---

## Seed File Format (Step 8)

File: `{idea-slug}-screen-seed.md` in the current working directory. `{idea-slug}` is lowercase kebab-case, 2-4 words. Written only on PROMOTE (or on user request).

```markdown
# Screen Seed: <idea title>
**Source:** business-sharks-screen v1.0  ·  **Screened:** <date>
**Screen verdict:** PROMOTE (<X.X>/10)

## Idea
<the full idea text as framed in Step 1 — what it is, customer, model, core problem>

## Screen Scorecard
<the 5-dimension table from the chat output>

## Research Done (<N> searches)
- **FACT:** <finding + source>
- **OBSERVED:** <signal + where>
- **INFERRED:** <reasoning>
- **ASSUMPTION:** <modeled gap — unverified>

## Tarpit Assessment
<which pattern(s) matched or "no tarpit pattern matched"; structural escape if any>

## What a Full Run Must Verify
- <open question 1>
- <open question 2>

---
*Pass this to `business-sharks`. Its analysts must CHALLENGE and EXTEND these findings, never trust them — this is 6 searches, not validation. Verify every FACT, re-derive every INFERRED, treat every ASSUMPTION as unknown.*
```
