---
name: domain-validator
description: This skill should be used when the user asks to "check a domain", "validate a domain name", "score a domain", "rank domain candidates", "is X.com a good domain", "should I buy X.com", "evaluate domain for brand", "pre ktorú doménu by som išiel", "oplatí sa kúpiť X.com", or provides a list of domains to compare. Evaluates writing/spelling risk, phone-dictation clarity, brand fit, distinctiveness, extensibility, and optional domain equity (SEO history) across EN and Slovak markets.
---

# domain-validator

Rubric-based evaluation of domain name candidates. Three invocation shapes, three weight profiles, optional brand context.

## Required inputs

Before scoring, ensure the invocation provides:

- **Domain(s)** to evaluate
- **Language scope** (EN, SK, EN+SK, other) - if absent, ask
- **Profile** (brand-primary, seo-primary, mixed) - if absent, ask

Batch missing inputs into one clarifying message, not multiple rounds.

## Invocation shapes

1. **Single domain** - "Check AlchemyComics.com. Language: EN+SK. Profile: brand-primary." -> full scorecard.
2. **List comparison** - "Rank these 5: X, Y, Z. Language: EN. Profile: brand-primary." -> ranked table + top-2 scorecards + recommendation.
3. **Brand-contextual** - "Score X for <project-name>." -> read project context from `~/.claude/projects/*/memory/`, `CLAUDE.md` sections, project folder; infer language+profile if present in context, ask if not.

## Rubric

### Gates (any fail = REJECT, no scoring)

1. **Spelling trap** - ambiguous letters for target language(s); SK/EN phonetic clashes (`y`/`i`, `c`/`k`, `s`/`z`).
2. **Homophone collision** - sounds like existing brand or common word in target language.
3. **Character hostility** - hyphens, digits, non-letter punctuation. Dies in dictation.
4. **Pejorative meaning** - best-effort scan EN/SK/CZ/PL/DE/HU. Flag as non-exhaustive.
5. **Trademark/category collision** - consumer-confusion or lawsuit-bait signal.
6. **Toxic history** - archive.org shows prior porn/scam/malware/politically-toxic content. Skip if fresh-reg.
7. **Poisoned link profile** - PBN/spam-dominant backlinks (Majestic/Ahrefs data required). Skip if fresh-reg or no paid data.

User can override a gate explicitly ("proceed anyway, I want the hyphen"). Note override in output.

### Scored axes (1-10, only if all active gates pass)

1. **Hallway test** - repeat-back, guess-purpose, remember-tomorrow after one hallway mention.
2. **Phone clarity** - how much spelling explanation required over bad phone line.
3. **Brand fit** - CEO lens (supports business 3 years out) + CMO lens (works in headline/logo/tagline). In brand-contextual mode, evaluate against pulled project context.
4. **Distinctiveness** - differs from generic category pattern.
5. **Extensibility** - room to grow vs pigeonhole.
6. **Domain equity** - WHOIS age, Majestic TF/CF, referring-domain quality, archive.org continuity, topic relevance, residual traffic. Scored as neutral/1 for fresh-reg.

### Weight profiles

| Axis | brand-primary | seo-primary | mixed |
|---|---|---|---|
| Hallway | 25% | 10% | 20% |
| Phone clarity | 20% | 10% | 15% |
| Brand fit | 30% | 15% | 25% |
| Distinctiveness | 15% | 10% | 12% |
| Extensibility | 10% | 5% | 8% |
| Domain equity | 0%* | 50% | 20% |

*brand-primary: domain equity reported but not weighted.

### Verdict thresholds

- Any active gate fails -> **REJECT**
- Weighted >=7.5 -> **STRONG GO**
- 6.0-7.4 -> **GO with notes**
- 4.5-5.9 -> **CONDITIONAL** (specific fixes identified)
- <4.5 -> **PASS**

## Data sourcing

1. Run WHOIS first -> detect fresh-reg (<1yr + no archive.org history) vs aged branch.
2. **Fresh-reg:** skip gates 6 and 7 (mark N/A), domain equity = neutral/1 informational, no paid-data prompts.
3. **Aged:** run archive.org CDX check for history gate. In seo-primary/mixed profile, soft-prompt user to paste Majestic/Ahrefs data for link-quality gate. Soft = score anyway with gap flagged if user declines.
4. Never invent data. Gaps explicit in output ("domain equity scored without Majestic data - confidence: medium").

## Output format

Produce structured markdown in Fero's voice: direct, no corporate filler, short dashes not em dashes, no motivational closers.

### Single-domain shape

```markdown
# Domain verdict: <domain>

**Verdict: <VERDICT>** (weighted <score>/10, profile: <profile>, lang: <languages>)
**Domain status:** <fresh-reg | aged since YYYY | expired-and-reclaimed>

## Gates
- ✅/❌/⚠️/N/A <gate name> - <one-line finding>
(all 7 gates; ⚠️ = passed with caveat; N/A = skipped)

## Scored axes
| Axis | Score | Notes |
|---|---|---|
(skip rows where domain equity N/A in brand-primary)

## Notes
- <strategic observation>
- <risk or confirmation action>
```

### List shape

Ranked table + rejected-with-reason + top-2 detailed scorecards + recommendation. If >20 candidates: rank-only first pass, offer top-5 detailed on request.

### Brand-contextual shape

Add header block showing what was pulled from project context so user can catch misreads:

```markdown
**Brand context used (<project>):**
  - Audience: <pulled>
  - Markets: <pulled>
  - Voice / positioning: <pulled>
  - Constraints: <any relevant rules>
```

## Edge cases

- **Malformed domain** -> validate first, ask to correct. Don't score garbage.
- **Archive.org empty** -> treat as fresh-reg branch.
- **WHOIS redacted** -> skip age-based scoring, note medium confidence.
- **Registered but not available to buy** -> note status, still score if user wants competitive study.
- **Brand context named but no memory/project exists** -> ask user directly for audience/tone/markets/deal-breakers.
- **Pejorative check is best-effort** -> always flag "non-exhaustive scan; confirm with native speakers before launch."

## Additional Resources

_(These reference, script, and example files are populated by later Phase 1 tasks. If absent, skip - core rubric above is sufficient to produce a verdict.)_

Detailed content in:
- `references/rubric-details.md` - per-gate/axis deep dive with failure examples
- `references/phonetic-traps.md` - SK/EN/CZ/PL/DE/HU pitfall lookup lists
- `references/weight-profiles.md` - profile selection edge cases
- `references/output-templates.md` - full output templates
- `references/brand-context-reading.md` - how to pull brand info from memory/project files

Scripts:
- `scripts/check-whois.sh` - WHOIS creation date + registrar + status
- `scripts/fetch-archive-snapshots.sh` - archive.org CDX API query
- `scripts/domain-sanity.sh` - domain string validation

Examples:
- `examples/single-domain.md` - worked Shape 1
- `examples/list-comparison.md` - worked Shape 2
- `examples/brand-contextual.md` - worked Shape 3
