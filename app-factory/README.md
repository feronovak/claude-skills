# app-factory

Take a validated idea and build it. End-to-end app development with parallel product validation.

## Why this exists

You've validated an idea (via `business-sharks` or your own conviction). Now you need to actually ship something — a product spec, design, engineering, QA, and a parallel track that keeps testing assumptions while you build. `app-factory` orchestrates that workflow. Five teammates, three phases, a human gate after the business analysis so you don't sleepwalk into building the wrong thing.

Designed for small bets that need to ship fast, not enterprise platforms.

## Invoke

The skill triggers on build language:

- "Build this app: a Next.js app for kids' story illustration with AI"
- "Create this product: a Tauri desktop tool for personal finance with AI categorization"
- "Develop this: a Slack bot that summarizes daily standups"
- "Make this into an MVP: ..."

Or pass the output of `business-sharks` directly — `app-factory` reads the validation context and skips re-asking.

## What you get

A project folder under your CWD with phase-numbered outputs:

- **Phase 1 — Business Analysis** → product spec, persona, scope, success metrics. **HUMAN GATE** here: review before building.
- **Phase 2 — Design** → UI specs, component tree, design system tokens.
- **Phase 3 — Engineering + QA + Validation** → code, tests, parallel product validation that pings users while build progresses.

Final state: a shipped MVP plus a validation log that captures what you learned during the build.

## Heads up

- **The human gate after Phase 1 is non-skippable.** It's there because the most expensive mistake in software is building the right thing wrong, and the second is building the wrong thing right. Review the spec.
- **This is for small bets.** Solo or small-team apps, not multi-team platforms. If you're building something with 4+ subsystems, decompose first and run `app-factory` per subsystem.
- **Pairs with `brainstormers-idea` and `business-sharks`** — chain the three for a brainstorm → validate → build pipeline. Or run standalone.

Full orchestration logic: see `SKILL.md` and `references/`.

---

Built by [Fero Novak](https://feronovak.com). Part of [feronovak/claude-skills](https://github.com/feronovak/claude-skills).
