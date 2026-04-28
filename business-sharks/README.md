# business-sharks

Rigorous startup validation. Honest verdicts: GO / CONDITIONAL / NO-GO.

## Why this exists

Founders evaluate their own ideas by talking to friends who tell them what they want to hear. `business-sharks` runs five adversarial analysts — market researcher, competitive intel, digital scout, financial modeler, and chief shark — through three phases (parallel research, synthesis, a YC-style shark panel). Output: the conversation you'd have with someone who's seen 1,000 ideas and isn't trying to spare your feelings.

## Invoke

The skill triggers on validation language. Examples:

- "Is this idea worth pursuing: a B2B SaaS for compliance reporting in fintech?"
- "Should I build a subscription product for indie podcast hosts?"
- "Shark tank this: an AI photo organizer for parents"

## What you get

A project folder created in your CWD with numbered files:

| File | Owner |
|---|---|
| `00-business-idea.md` | your input |
| `01-07` | analyst outputs (problem, market, competition, moat, SEO/GEO, unit econ, projections) |
| `08-15` | chief-shark synthesis (GTM, risk, scalability, YC eval, scorecard, exec summary) |
| `16-pivot.md` | pivot suggestions — only if NO-GO or weak CONDITIONAL with adjacent opportunities |

Final scorecard: **13 dimensions × 1–10**, dual lens (Venture vs Bootstrap, higher score drives the average), and a verdict with WWNBT (what would need to be true) for any CONDITIONAL.

## Heads up

- **This is desk research.** Strongest signal still comes from real customer conversations the founder runs. Sharks can score market sizing but can't validate that customers actually want it.
- **Three modes:** STANDARD (full 5-agent team), HYBRID (background subagents, ~40% cheaper), QUICK (single-pass Sonnet, ~60% cheaper).
- **Re-runnable.** Re-running on the same idea folder triggers update mode — analysts overwrite their files; chief-shark re-synthesizes. Not destructive.
- **Pairs with the pipeline:** chain `brainstormers-idea` → `business-sharks` → `app-factory` for a complete brainstorm → validate → build flow.

Full orchestration: see `SKILL.md` and `references/`.

---

Built by [Fero Novak](https://feronovak.com). Part of [feronovak/claude-skills](https://github.com/feronovak/claude-skills).
