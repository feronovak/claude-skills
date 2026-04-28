# domain-validator

Score and rank domain candidates. Writing risk, dictation clarity, brand fit, distinctiveness — for both EN and Slovak markets.

## Why this exists

Picking a domain is one of those decisions founders agonize over for hours and then second-guess for years. Most "domain checkers" tell you if it's available. They don't tell you if it's *good*. `domain-validator` evaluates candidates against a rubric: can a human spell it on the first try, can you dictate it cleanly over a phone, does it carry brand signal in your target language, is it extensible to product lines and subdomains, does it have SEO history baggage.

EN + SK are first-class. Built specifically because picking a domain that works in Bratislava but doesn't translate to English (or vice versa) is a real CEE founder problem.

## Invoke

The skill triggers on domain evaluation language. Examples:

- "Is talealbum.com a good domain?"
- "Should I buy storybook.io or makemystory.app?"
- "Score these domains: a.com vs b.io vs c.app"
- "Pre ktorú doménu by som išiel — kniezka.sk alebo storybook.sk?"
- "Oplatí sa kúpiť tento domain?"

## What you get

A scored rubric per candidate, plus a ranked recommendation. Each candidate gets:

| Dimension | What it checks |
|---|---|
| Writing risk | Can someone spell it correctly hearing it once? |
| Phone dictation | Does it survive being read aloud over a bad phone line? |
| Brand fit | Does it carry the right vibe (premium / playful / utility / B2B)? |
| Distinctiveness | Does it stand out, or could it be confused with 5 other things? |
| Extensibility | Can it stretch to product lines, subdomains, internationalization? |
| Domain equity (optional) | If a domain has SEO history, is that history helpful or harmful? |

Output: a rubric table with scores per dimension per candidate, plus a final ranked list with reasoning. Trade-offs called out explicitly — no "they're all great, you decide" dodging.

## Heads up

- **EN + SK first-class.** Other languages work but the rubric is tuned for English-and-Slovak speaking audiences. If you're picking a domain for a Polish or German market, mention that — the skill adapts.
- **Doesn't check availability.** Use Namecheap / Cloudflare for that. This skill assumes you've already shortlisted available candidates.
- **Doesn't replace gut feel.** The rubric helps surface things you'd otherwise miss (like phone-dictation risk). It doesn't override your taste.

Full rubric and weighting logic: see `SKILL.md`. Examples and edge cases: `examples/` and `references/`.

---

Built by [Fero Novak](https://feronovak.com). Part of [feronovak/claude-skills](https://github.com/feronovak/claude-skills).
