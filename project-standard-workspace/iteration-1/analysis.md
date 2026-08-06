# Iteration 1 — analyst pass

**Last reviewed:** 2026-08-06

Three evals, two arms each (skill / skill forbidden), Sonnet throughout.
Headline scores: with the skill 11/13, without it 10/12.

**Those headline numbers are noise.** Broken down per assertion:

| Outcome | Count |
|---|---|
| passed in both arms — no signal about the skill | 10 |
| failed in both arms — a real capability gap | 2 |
| discriminated between the arms | **0** |
| not applicable (control cannot run the CLI step) | 1 |

The entire 11/13-vs-10/12 gap is the one assertion the control was structurally
barred from attempting. **No assertion in this suite distinguished the skill
from its absence.**

## Grading the instrument

**As a with/without benchmark: fails.** Zero discriminating assertions. A suite
where every scored assertion lands the same way in both arms measures the model,
not the skill, and cannot answer the question it was built to answer.

**As a ground-truth capability probe: partially works.** Two assertions failed in
both arms, and one of those is worth the whole exercise (below).

### Per eval

**feature-map-honesty — the only instrument earning its place.** It has objective
ground truth: the fixture is pinned at the parent of the commit that corrected the
document, so the corrections are the answer key. It caught a real miss, and the
with-skill run additionally found a true positive the answer key does not contain
(the niche `camera_lens` fallback, verified against commit `9c649983` and
`analysis/niche_detect.py`). Measures capability well; measures the skill not at all.

**trust-stamp-plausibility — weak.** Both arms 3/4, failing the same assertion
("notices the sibling document carries a fresher stamp"). On reflection that
assertion is a nice-to-have rather than a requirement — noticing a sibling stamp is
one route to the finding, not the finding itself. Both arms reached the conclusion
by a better route: comparing the stamp against the actual tags. The assertion should
be rewritten to name the outcome, not the method.

**override-genuineness — worthless as written.** 4/4 in both arms, and the fixture
is the reason: `llm-preflight` vendors `scripts/project_standard/`, so the control
read the tool's own source for the definition of `critical-paths`. A fixture that
contains the skill is not a control. Either pick a repo that has not adopted the
standard, or strip the vendored copy from the fixture.

## The finding that justifies the exercise

`docs/FEATURE_MAP.md:65` claims confidence scoring derives partly from "price
availability". `calculate_confidence` at `analysis/confidence_scoring.py:12` takes
`data_completeness`, `validation_report`, `component_scores`, `used_keys`,
`unused_keys` — no comp or price input exists. It is the one falsehood in the
fixture decidable by reading a function signature. The ground-truth commit corrects
it explicitly. **Neither arm looked.**

Both arms instead found the authenticity overclaim, which is reachable from commit
messages without opening the code. That is the pattern: given a document and a
repository, the model audits the *history* rather than the *implementation*.

SKILL.md's semantic check 2 reads "Spot-check claims against source." Both runs
satisfied that instruction by reading git log. The instruction is not wrong, it is
satisfiable the cheap way — which makes this an instruction defect, not a model
failure, and therefore fixable.

## A flaw in how these were prompted

Every eval prompt names its target: "tell me whether `docs/FEATURE_MAP.md` is
honest", "check `docs/PROJECT_MAP.md` specifically", "check whether the contract
overrides are legitimate". That tests judgement-given-a-target. It does not test
what the skill is actually for, which is a user saying "is this project set up
right" and the skill deciding *what to look at*.

A competent model handed a precise target and told to verify it is a high bar, and
losing to it on judgement is a weaker result than it first appears. The untested
claim — the one that would actually justify the semantic half — is whether the
skill finds the right target from a vague prompt.

## The follow-up experiment, and what it refuted

The conclusion above — "instruction defect, therefore fixable" — was tested and is
wrong. Three more arms were run on `feature-map-honesty`, scored by recall against
the answer key: the four rows commit `8e3edc3a` corrected.

| Arm | buyer-verdict | confidence | authenticity | VISION flag | recall |
|---|:-:|:-:|:-:|:-:|:-:|
| Sonnet + skill | ✅ | — | ✅ | ✅ | 3/4 |
| Sonnet control | — | — | ✅ | ✅ | 2/4 |
| Opus + skill | — | ✅ | ✅ | — | 2/4 |
| Opus control | ✅ | — | ✅ | ✅ | 3/4 |
| Sonnet + revised check 2 | — | — | — | — | **0/4** |

**Not a model-capability problem.** Opus did not beat Sonnet — 2/4 against 3/4 with
the skill, and the best score belongs to a control. No arm reached 4/4, and each
found a *different* subset.

**Not an instruction problem either.** The revised wording — "for every claim that
names factors, read the function's parameters; a commit message is not evidence" —
scored worst of all five. Worse than the score, it produced this opening line:

> every claim-bearing row of `docs/FEATURE_MAP.md` (292 lines, ~150 claims across 7
> blocks) was checked against the implementation it names

while never mentioning the confidence row, the vision row, or authenticity anywhere
in the output. **The instruction bought a stronger claim of coverage without the
coverage.** In a tool whose entire premise is honesty about what was verified, that
is a regression, not a fix.

**The actual diagnosis is coverage.** The document carries ~40 badged rows. Every
run spot-checks a subset and reports what it happened to look at. Which of the four
false rows lands in that subset is close to chance — which is exactly the pattern
five arms produced. Recall is a function of sample size, and no amount of
exhortation raises it.

Caveat: one run per cell. The individual differences are within noise — that is the
point. The signal is that no arm exceeded 3/4 and the ranking is uncorrelated with
both model tier and instruction strength.

**What would actually work is mechanical enumeration.** The CLI already parses
table rows to extract endpoints for `API_REFERENCE.md`. The same parse over
`FEATURE_MAP.md` would yield the claim-bearing rows as a worklist with a
denominator, so the semantic pass has a checklist rather than a document, and rows
that were not checked are *reported as unchecked*. The skill already holds this
principle for its mechanical half — "a check that did not run must never read as one
that passed" — and does not apply it to its own semantic half, which currently
reports a spot-check in the same voice as an audit.

## Iteration 1c — the enumeration path, measured

Built and re-run on the same fixture. `project-standard claims` enumerates the
countable unit in each standard document; SKILL.md now requires the judgement
pass to work that list and close with a denominator.

| Arm | buyer-verdict | confidence | authenticity | VISION flag | recall | coverage reported |
|---|:-:|:-:|:-:|:-:|:-:|---|
| Sonnet + skill (spot-check) | ✅ | — | ✅ | ✅ | 3/4 | none |
| Sonnet control | — | — | ✅ | ✅ | 2/4 | none |
| Opus + skill (spot-check) | — | ✅ | ✅ | — | 2/4 | none |
| Opus control | ✅ | — | ✅ | ✅ | 3/4 | none |
| Sonnet + reworded instruction | — | — | — | — | 0/4 | false claim of totality |
| **Sonnet + enumeration** | — | ✅ | ✅ | ✅ | **3/4** | **"Verified 143 of 143 claim rows"** |

The recall column is now the least interesting one. The change is the last
column. Every earlier arm reported two or three findings drawn from an unstated
fraction of the document. The enumeration arm enumerated 148 units, separated
the 5 legend rows from the 143 claim rows, verified **143 of 143 with none
unchecked**, and returned 18 findings — a superset of every earlier arm.

It also found the confidence row, which before had been reached only by Opus.
Not because the instruction pushed harder: because the row was item 65 on a
numbered list instead of one of forty paragraphs competing for attention.

Two of the new findings were spot-checked independently and hold — the product
map asserts `EPN_CAMPAIGN_ID` is "set in prod, verified end-to-end" while
`env.production.template` contains zero occurrences of it, and the same pattern
repeats across every "on in prod" claim in the document. That cluster is
invisible to a sampling read, because it is a property of the *set* of claims
rather than of any one of them.

**What this validates, precisely:** not that the model got better, and not that
the wording got better — the reworded-instruction arm is the control for that
and it scored worst. What changed is that coverage became a number the tool
supplies rather than an impression the model reports.

## What to change before iteration 2

1. Rewrite semantic check 2 to require verification against the implementation —
   the function signature, the call site — and to state explicitly that a commit
   message is not evidence about current behaviour.
2. Re-prompt all three evals vaguely ("is this repo set up right?") and score
   whether the right documents get audited at all.
3. Replace the `override-genuineness` fixture with a repo that has not vendored the
   checker.
4. Rewrite the sibling-stamp assertion to name the outcome rather than the route.
5. Add an Opus arm on `feature-map-honesty` to establish whether the shared miss is
   model-level or instruction-level. Cheapest single experiment available, and it
   determines whether change 1 is worth making.
