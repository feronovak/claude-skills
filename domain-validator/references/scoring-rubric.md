---
name: scoring-rubric
description: Detailed scoring guide for the six evaluated axes - what each score level looks like, how to apply it, worked examples
author: feronovak
---

# Scoring Rubric

Six axes, each scored 1-10. Applies only after all active gates pass.

Referenced by: SKILL.md § Scored axes, SKILL.md § Weight profiles

---

## Axis 1 - Hallway Test (writing risk)

**What it measures:** If someone hears the domain once in a hallway conversation, can they (a) repeat it back, (b) guess roughly what the product does, (c) remember it tomorrow?

| Score | Meaning |
|---|---|
| 9-10 | One-shot recall, purpose guessable, sticky |
| 7-8 | Easy recall, purpose partially guessable |
| 5-6 | Recalls with effort, purpose opaque |
| 3-4 | Recalls only with spelling, purpose alien |
| 1-2 | Won't be recalled without writing it down |

**Examples:**
- `talealbum.com` - 7: both words clear, "tale" + "album" hints at stories/memories
- `ithinktoday.com` - 5: phrase is clear but purpose is opaque, could be anything
- `xqzt.io` - 1: unrecallable

**SK-market note:** Score separately for SK audience if language scope includes SK. A 9 in EN can be a 5 in SK if the words don't land.

---

## Axis 2 - Phone Clarity

**What it measures:** How much spelling explanation is required when reading this domain over a bad phone line to a non-tech person.

| Score | Meaning |
|---|---|
| 9-10 | No spelling needed. Say it, they get it. |
| 7-8 | One clarification max ("that's K not C") |
| 5-6 | 2-3 clarifications, but workable |
| 3-4 | Must spell it out fully |
| 1-2 | Even after spelling, confusion likely |

**High-risk patterns:**
- `ck` vs `k` vs `c` endings
- `ph` vs `f`
- `ei` vs `ie`
- Silent letters
- Unusual TLDs: `.io`, `.ai` score lower than `.com`/`.sk` with non-tech audiences

---

## Axis 3 - Brand Fit

**What it measures:** Does this domain support the business 3 years out?
- CEO lens: Is this still a credible company address when you're 10x bigger?
- CMO lens: Does it work in a headline, a logo, a tagline, a billboard?

**In brand-contextual mode:** Pull project context and evaluate against it explicitly. State what context was used.

| Score | Meaning |
|---|---|
| 9-10 | Scales, premium, works across all formats |
| 7-8 | Good fit, minor limitations in 1 format |
| 5-6 | Works today, might constrain at scale |
| 3-4 | Already constraining, category-specific |
| 1-2 | Pigeonholes from day one |

**Examples:**
- `stripe.com` - 10: scales from payments to full financial OS
- `shoestore.com` - 2: exactly what it says, nowhere to grow
- `kraboo.com` - 8: invented word, premium feel, no category lock

---

## Axis 4 - Distinctiveness

**What it measures:** Does it stand out from the generic category pattern, or does it blend into a sea of `[adjective]+[noun].com` names?

| Score | Meaning |
|---|---|
| 9-10 | Completely distinctive, nothing like it in category |
| 7-8 | Stands out clearly with minor genre markers |
| 5-6 | Distinctive within a crowded subtype |
| 3-4 | Sounds like the category, not a specific brand |
| 1-2 | Indistinguishable from 20 similar names |

**Pattern deductions:** `-ly`, `-ify`, `-hub`, `-HQ`, `My-`, `Get-`, `Smart-` prefixes/suffixes all signal low distinctiveness. Subtract 1-2 points each.

---

## Axis 5 - Extensibility

**What it measures:** Room to grow vs. room to be pigeonholed.

Questions to ask:
- Can this work as `blog.domain.com`, `shop.domain.com`, `api.domain.com` without absurdity?
- If the product pivots category, does the name survive?
- Does it work in English AND Slovak without one language making it awkward?

| Score | Meaning |
|---|---|
| 9-10 | Extends naturally to any product direction |
| 7-8 | Works in 2-3 directions with minor awkwardness |
| 5-6 | OK in current direction, constrained elsewhere |
| 3-4 | Already constraining the product |
| 1-2 | Can't pivot without a rebrand |

---

## Axis 6 - Domain Equity

**What it measures:** If the domain is aged (not fresh-reg), does its SEO and link history add value or add risk?

**Fresh-reg:** Score 5 (neutral), label "informational - no data". Weight override: brand-primary profiles exclude this axis from weighted score regardless.

**Data points to collect:**
- WHOIS creation date and registrar
- archive.org snapshot count and continuity (no 3yr+ gaps)
- Majestic TF/CF (if available)
- Referring domain count and quality (if available)
- Topic alignment between historical content and intended new use

| Score | Meaning |
|---|---|
| 9-10 | Strong TF, relevant history, continuous use |
| 7-8 | Decent TF, mostly relevant, minor gaps |
| 5-6 | Neutral (fresh-reg or unrelated but clean history) |
| 3-4 | Thin history, or topic mismatch |
| 1-2 | Toxic/spammy history, should fail gate 6/7 first |

**Always note confidence level:** "domain equity scored without Majestic data - confidence: medium"
