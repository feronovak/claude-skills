---
name: weight-profiles
description: How to select the right weight profile and handle edge cases - brand-primary, seo-primary, mixed
author: feronovak
---

# Weight Profiles

Three profiles control how axis scores combine into the weighted final score.

Referenced by: SKILL.md § Weight profiles

---

## The Three Profiles

| Axis | brand-primary | seo-primary | mixed |
|---|---|---|---|
| Hallway test | 25% | 10% | 20% |
| Phone clarity | 20% | 10% | 15% |
| Brand fit | 30% | 15% | 25% |
| Distinctiveness | 15% | 10% | 12% |
| Extensibility | 10% | 5% | 8% |
| Domain equity | 0%* | 50% | 20% |

*brand-primary: domain equity collected and reported, but weight = 0. Weighted score total = 100% across other axes.

---

## Choosing the Right Profile

### brand-primary

Use when:
- Building a consumer brand or product from scratch
- Founder wants the domain to be the long-term company identity
- SEO is not the primary acquisition channel (or will be built from content, not domain authority)
- Domain is a fresh-reg

**Ask yourself:** "If this domain had zero backlinks and zero history, would it still be valuable?" If yes = brand-primary.

**Examples:**
- New SaaS product launch
- CEE startup targeting both EN and SK markets
- Personal brand (feronovak.com type)
- Children's product where brand safety matters more than SEO

---

### seo-primary

Use when:
- Buyer wants to acquire an aged domain specifically for its link equity
- The domain is an asset purchase, not a brand-first decision
- Organic search is the main growth channel
- Content or affiliate site

**Caution:** seo-primary + fresh-reg = domain equity axis scores neutral (5), which tanks the weighted score. That's correct behavior - a fresh domain is a poor seo-primary choice by definition.

**Examples:**
- Buying an aged domain to 301-redirect into an existing site
- Content site acquisition
- Affiliate project

---

### mixed

Use when:
- Building a brand AND organic search matters from early days
- E-commerce: brand credibility + product search traffic
- Media properties
- Can't clearly choose one axis

**Default:** If user doesn't specify and context doesn't make it obvious, suggest `mixed` and explain the trade-off. Let them confirm.

---

## Profile Selection Edge Cases

### "I want brand AND SEO"

Default to `mixed`. If the user is evaluating an aged domain specifically for its equity, you can run both `brand-primary` and `seo-primary` scorecards side by side and show how the verdict changes.

### Profile conflicts with domain type

- Fresh-reg + seo-primary → proceed, but note: "seo-primary on a fresh-reg: domain equity scores 5 (neutral), which reduces your weighted score by design. If you're open to aged domains, that changes the calculus."
- Aged domain with toxic history + any profile → gates 6/7 should reject before scoring. If user overrode: proceed but note the override in output.

### Brand-contextual mode

When pulling brand context from project memory, infer the profile:
- Context shows heavy content/SEO strategy → suggest seo-primary or mixed
- Context shows product launch / consumer brand → suggest brand-primary
- Unclear → ask directly

---

## Verdict Thresholds (same across all profiles)

| Score | Verdict |
|---|---|
| Gate fail | REJECT |
| >= 7.5 | STRONG GO |
| 6.0 - 7.4 | GO with notes |
| 4.5 - 5.9 | CONDITIONAL (specific fixes identified) |
| < 4.5 | PASS |

**CONDITIONAL** means: "Could work if X." X must be specific - not "improve brand fit" but "if you drop the `-ify` suffix and use a coined word, brand fit goes from 5 to 7+."
