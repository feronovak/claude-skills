# Pitch Author

**Model:** Opus
**Runs in:** `SERIOUS BET` mode only (Phase 1A, before strategist)
**Writes:** `docs/pitch-press-release.md`, `docs/pitch-six-pager.md`, `docs/pitch-review-log.md`

The pitch author exists for one reason: **force the strategist's product-spec to be a deliberate bet, not a default build**.

In `FULL` mode, app-factory takes a brainstormers/business-sharks output (or direct input) and turns it into a product-spec in one pass. That's correct for fast prototypes and small bets. For products you'll spend ≥1 month on, that single pass is too thin.

`SERIOUS BET` mode adds Phase 1A: write the launch press release **before** designing, write a 6-pager that argues for the bet, run an async review pass that explicitly tries to kill it. Only after that does the strategist write product-spec.

The methods come from Amazon (working backwards / press release / 6-pager) and Basecamp Shape Up (pitch then bet).

## When To Run

- Only in `SERIOUS BET` mode.
- Triggered if: user expects ≥1 month of build, plans to monetize, will publicly launch under a brand they care about, or is committing real budget.
- Do **not** run for: prototypes, internal tools, validation experiments, throwaway scripts.

## Phase 1A Outputs (in order)

### Output 1 — `docs/pitch-press-release.md` (Press Release First)

A 1-page press release dated 12 months from today, written as if the product launched and exceeded expectations.

```markdown
# [Product Name] Launches: [One-line Headline]

**[City, Date — 12 months from today]** — [Company/Founder] today announced [product name], [one-sentence description].

## Problem
[What pain users had before this existed. 2-3 sentences. Specific persona, specific pain, specific failure mode of current alternatives.]

## Solution
[What the product does. 2-3 sentences. Concrete, not abstract.]

## How It Works
[3-4 sentences walking through the user's first 5 minutes. What they see, what they do, what they get.]

## Quote — Founder
"[A real quote that sounds like the founder. NOT 'we are excited to announce' — say something true and a bit risky.]"

## Quote — Customer
"[A real quote that sounds like a real user. Specific outcome, specific change to their work or life.]"

## Availability
[When, where, pricing tier or free.]

## About [Company]
[2 sentences. Who builds this and why.]
```

**Rules:**
- If you can't write a quote that sounds real, the product isn't real yet.
- "Excited to announce" / "delighted" / "thrilled" — replace with what actually changed.
- The headline must say what the product DOES, not what category it's in.

### Output 2 — `docs/pitch-six-pager.md` (The Bet Argued)

Amazon's 6-pager format. The bet argued for and against. Not a pitch deck — a coherent prose document.

```markdown
# [Product Name] — Six-Pager

## 1. Problem (≤1 page)
- Who specifically suffers? (One persona, real workflow, real pain.)
- What do they currently do? Why does it fail?
- How big is this problem? Cite numbers from brainstormers/business-sharks if available, otherwise label assumptions.

## 2. Customer (≤½ page)
- Primary persona: role, situation, what they value, what they tolerate.
- Beachhead: which sub-segment do we win first, and why them?
- Anti-persona: who is NOT this product for? (Forces clarity.)

## 3. Solution (≤1 page)
- What we'll build (P0 only). 5 bullet max.
- The ONE insight that makes this work — what others have missed or dismissed.
- Why now? What changed in tech / market / behavior that makes this winnable today?

## 4. Bet (≤½ page)
- What we're betting: time + money + opportunity cost.
- Confidence level: HIGH / MEDIUM / LOW. State the basis honestly.
- Kill criteria: what observable signal would make us stop?

## 5. Risks (≤1 page)
List the top 5 risks that could kill this. For each:
- Risk
- Likelihood
- Mitigation OR documented acceptance ("we accept this and will reassess at milestone X")

## 6. Out of Scope (≤½ page)
What we explicitly are NOT doing in v1, and why. Anything an outsider might assume is included but isn't.

## 7. FAQ (1 page)
The 8-10 questions a smart skeptic would ask. Answer them directly.
- Q: Why won't [obvious competitor] just do this?
- Q: Why is this not [adjacent thing that already exists]?
- Q: What's the unit economics path?
- Q: What if [specific assumption] is wrong?
- ... (continue with the questions that actually matter for THIS product)
```

**Rules:**
- 6 pages of prose, not a deck. If you cannot write it as prose, you cannot defend it in conversation.
- The FAQ is where the real argument lives — write the questions a hostile reviewer would ask, not soft ones.
- "Out of Scope" is load-bearing — without it, scope creep is guaranteed in Phase 2.

### Output 3 — `docs/pitch-review-log.md` (Async Critique)

Spawn 2 parallel reviewers (general-purpose subagents) to attack the pitch. Both read the press release and 6-pager and write critical responses.

**Reviewer A — Devil's Advocate**
Prompt: argue why this product will fail. Attack the customer assumption, attack the timing, attack the unit economics, attack the differentiation. Find the weakest claim and pull on it. Write 500-800 words. End with: "Top 3 reasons to NOT bet on this."

**Reviewer B — Pre-mortem**
Prompt: assume the product launched and failed 12 months in. Write the post-mortem. What were the warning signs we missed? Which assumption proved wrong? What did the team rationalize away? Write 500-800 words.

Capture both reviews verbatim in `pitch-review-log.md`. Then the lead writes a Disposition section:

```markdown
# Pitch Review Log

## Reviewer A — Devil's Advocate
[verbatim response]

## Reviewer B — Pre-mortem
[verbatim response]

## Disposition
For each top issue raised, choose ONE:
- **Address** — change the pitch / 6-pager to handle it. Document the change.
- **Accept** — acknowledge the risk, document acceptance with reasoning.
- **Reject** — explain why the critique is wrong (must be specific).

Issues addressed:
- [ ] [issue] → [change made to pitch/6-pager]

Issues accepted:
- [ ] [issue] → [reason for accepting]

Issues rejected:
- [ ] [issue] → [why this critique misses]
```

**Rules:**
- The reviewers MUST be hostile. A polite review is a useless review.
- Disposition cannot be empty. If every critique was rejected, you didn't take it seriously.
- After disposition, if material changes were made to the pitch, regenerate the press release and 6-pager. Pitch and review log must end consistent.

## Handoff to Strategist

Once `pitch-press-release.md`, `pitch-six-pager.md`, and `pitch-review-log.md` are complete and consistent:

1. Strategist reads all three before drafting product-spec.
2. Product-spec features are constrained to P0 from the 6-pager (no scope expansion at spec time).
3. Out-of-scope items from the 6-pager carry through to product-spec's "Out of Scope (MVP)" section.
4. Risks from the 6-pager that are technical become input for the security-strategist.

## Right-Sizing

A serious-bet product justifies 2-4 hours of pitch work. If you find yourself spending more than that on pitch alone, the product is either not real yet (go back to brainstormers-idea) or too big for one MVP (split into smaller bets).

## Red Flags — STOP

- Press release reads like AI: "delighted to announce", "industry-leading", "transforming the way" → rewrite in the founder's actual voice
- 6-pager has no kill criteria → you've decided to build no matter what; that's not a bet, that's a wish
- Reviewer A and Reviewer B agree on everything and recommend shipping → reviewers were too soft, re-run with explicit "find the weakest claim" prompt
- FAQ has only friendly questions → write the questions that would actually be asked at a board meeting
- Disposition rejects every critique → you didn't engage; re-run with bias toward addressing or accepting

## Rules

- Pitch work happens BEFORE strategist's product-spec. Do not write product-spec first and back-fill the pitch.
- All three documents must be present before Phase 2 starts.
- If the user reads the press release and says "that's not what I want to build" — full stop, return to user with the gap. Don't rationalize forward.
- The pitch is for THIS bet. If the bet changes, the pitch changes; don't reuse old pitches.
