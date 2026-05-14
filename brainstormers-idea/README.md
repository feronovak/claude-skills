# brainstormers-idea

Take a raw idea and shape it into something concrete enough to validate.

## Why this exists

You have an idea but it's vague — a phrase, a hunch, a one-liner. Before running it through `business-sharks` (which is rigorous and expensive), you need to *shape* it: who's it for, what's the angle, why now, what's the revenue model. `brainstormers-idea` interviews you for context, then runs four parallel research streams (market landscape, competition map, timing window, revenue models) and synthesizes a refined version of the idea you can take into validation.

Creative, not skeptical. The skeptical pass is what `business-sharks` is for.

## Invoke

The skill triggers on idea-shaping language:

- "Brainstorm this idea: a tool for indie podcasters to monetize without ads"
- "Help me shape this: AI-powered Slovak language tutoring"
- "Research this concept: a community for first-time freelance designers"
- "Is this idea any good: ..."

## What you get

A project folder under your CWD with seven numbered files:

| File | Content |
|---|---|
| `00-idea-brief.md` | your input + interview answers, compiled by the team lead |
| `01-market-landscape.md` | who's the audience, where do they spend time, what alternatives exist |
| `02-competition-map.md` | direct/indirect competitors, gaps, positioning |
| `03-timing-window.md` | why now, what's enabling/blocking, market readiness |
| `04-revenue-models.md` | how this could make money — pricing, channels, unit shape |
| `05-refined-idea.md` | the synthesis: a tighter version of your original idea, with strategic angle |
| `06-strategy-brief.md` | critical assumptions, next steps, recommended actions |

`05-refined-idea.md` is the file you'd hand to `business-sharks` next. The skill emits it in a format that sharks can ingest as Phase 0 input — analysts will challenge and extend rather than re-research from scratch.

## Heads up

- **This is creative, not adversarial.** It explores possibilities. If you want someone to break your idea, run it through `business-sharks` after.
- **The interview is real.** First exchange is questions about you, your audience, your constraints. Skipping it produces shallower research.
- **Pairs naturally with `business-sharks`** — sharks detects brainstormers output and uses it as starting context. No re-typing your idea.

Full pipeline orchestration: see `SKILL.md` and `references/`.

---

Built by [Fero Novak](https://feronovak.com). Part of [feronovak/claude-skills](https://github.com/feronovak/claude-skills).
