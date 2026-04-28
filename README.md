# claude-skills

Opinionated [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skills for product validation, idea brainstorming, end-to-end app development, and brand-specific workflows.

Built from running consumer products at Ringier Slovakia (Aktuality.sk, Azet.sk, Pokec) and a decade of side projects at Kontemi. These are the questions I ask before betting on something — turned into skills you can run.

Not generic tooling. Not framework-of-the-week. Each skill is rigorous enough to use on a real decision.

## What's inside

| Skill | What it does |
|---|---|
| `/brainstormers-idea` | Takes a raw idea and shapes it: market, competition, timing, revenue. Asks the right questions before research starts. |
| `/business-sharks` | Rigorous startup validation — market research, competitive intel, SEO/GEO, financials, and a YC-style shark panel. Honest verdicts: GO / CONDITIONAL / NO-GO with WWNBT and pivot suggestions. |
| `/app-factory` | End-to-end app development from a validated idea: spec, design, engineering, QA, and parallel product validation. |
| `/domain-validator` | Score and rank domain candidates: writing risk, dictation clarity, brand fit, distinctiveness. EN + Slovak markets. |

The first three form a complete pipeline: brainstorm → validate → build. Each runs independently or chains into the next.

## Install

```bash
git clone https://github.com/feronovak/claude-skills.git ~/projects/claude-skills
cd ~/projects/claude-skills
./setup.sh
```

`setup.sh` symlinks each skill directory into `~/.claude/skills/`. Pulls work without re-running setup — symlinks pick up changes instantly.

## Update

```bash
cd ~/projects/claude-skills && git pull
```

## Use

```
/brainstormers-idea A subscription product for indie podcast hosts
/business-sharks A B2B SaaS that automates compliance reporting for fintech
/app-factory A Next.js app for kids' story illustration with AI
/domain-validator talealbum.com vs storybook.app vs makemystory.io
```

## Philosophy

- **Honest over polite.** A skill that tells you your idea is great when it isn't wastes more time than a skill that tells you the truth. These default to skeptical.
- **Specific over generic.** "Test the market" is not a GTM strategy. "Cold email 50 mid-market podcast networks" is. Skills push for the specific.
- **Defensible over comprehensive.** Every claim should cite evidence. Where evidence is missing, the skill says so explicitly — `INSUFFICIENT DATA` is a valid output.
- **Multi-phase over one-shot.** Real validation isn't a single LLM call. The team-based skills run parallel research, cross-read each other, and synthesize.

## Who built this

[Fero Novak](https://feronovak.com), Managing Director. 12+ years running consumer products at scale — Aktuality.sk (#1 news in SK), Azet.sk, Pokec. Builder background: Kontemi (car marketplaces, dating products, travel services since 2010).

These skills started as personal tooling for evaluating side-project ideas without falling for my own hype. Sharing them in case they're useful to anyone else doing the same.

## License

MIT. Use them, fork them, build on them. No warranty.

## Contributing

Issues and PRs welcome. Voice rule: skills should be direct and specific. No buzzwords, no fluff, no engagement bait.
