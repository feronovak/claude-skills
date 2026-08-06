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
