---
name: equity-evaluation
description: How to evaluate domain equity and SEO history for aged domains - data sources, scoring logic, confidence levels
author: feronovak
---

# Domain Equity Evaluation

Used in Gate 6 (Toxic History), Gate 7 (Poisoned Link Profile), and Axis 6 (Domain Equity score).

Referenced by: SKILL.md § Data sourcing, SKILL.md § Scored axes

---

## Step 1: Classify the Domain

Run WHOIS first. Branch:

| WHOIS creation | archive.org snapshots | Classification |
|---|---|---|
| < 1yr | None | Fresh-reg - skip gates 6 & 7, equity = neutral |
| < 1yr | Snapshots exist | Expired and re-registered - run gates 6 & 7 |
| > 1yr | Any | Aged - run gates 6 & 7 |
| Redacted | Any | Unknown - note "WHOIS redacted, confidence: medium" |

**Always state classification in output header:** `Domain status: fresh-reg | aged since YYYY | expired-and-reclaimed`

---

## Step 2: Archive History Check (Gate 6)

Query archive.org CDX API:
```
https://web.archive.org/cdx/search/cdx?url=example.com&output=json&limit=50&fl=timestamp,statuscode,mimetype
```

What to look for:

| Finding | Action |
|---|---|
| No snapshots | Treat as fresh-reg |
| Clean content site (blog, product, etc.) | Gate 6 PASS |
| Snapshots show adult/pharma/casino/scam | Gate 6 FAIL |
| Snapshots show politically extreme content | Gate 6 FAIL |
| Content clearly different topic, but clean | Gate 6 PASS, note in equity section |
| 3yr+ gap with nothing | Note continuity break, minor equity deduction |

**Timeline rule:** A single toxic incident 5+ years ago with clean history since is a warning (⚠️), not an automatic FAIL. A toxic incident within 3 years = FAIL.

---

## Step 3: Link Profile Check (Gate 7)

**Only applicable for seo-primary or mixed profiles on aged domains.**

Soft-prompt the user once: "For accurate domain equity scoring in seo-primary mode, paste your Majestic or Ahrefs data for [domain]. Trust Flow, Citation Flow, referring domains, top anchors. Skip if you don't have it - I'll note medium confidence."

If user provides data, evaluate:

| Metric | Good | Caution | Fail |
|---|---|---|---|
| Majestic Trust Flow | > 20 | 10-20 | < 10 |
| TF/CF ratio | > 0.5 | 0.3-0.5 | < 0.3 (spam signal) |
| Referring domains | Diverse, real sites | Mix | PBN-heavy |
| Anchor text distribution | Branded/natural | Some keyword | Spammy exact-match |
| Top referring domains | Industry-relevant | Mixed | Casino/pharma/adult |

**No data rule:** If user declines, score domain equity at medium confidence. State clearly in output: "domain equity scored without Majestic data - confidence: medium"

---

## Step 4: Domain Equity Score (Axis 6)

Combine findings into a 1-10 score.

| Scenario | Score range | Notes |
|---|---|---|
| Fresh-reg, no history | 5 | Neutral. Brand-primary: exclude from weighted score |
| Aged, clean history, strong TF, topic match | 8-10 | Real asset |
| Aged, clean history, moderate TF | 6-7 | Modest equity |
| Aged, clean history, no SEO data | 5-6 | Can't value it |
| Aged, topic mismatch but clean | 4-5 | Equity doesn't transfer |
| History gaps, minor issues | 3-4 | Equity neutral to negative |
| Toxic history (should have failed Gate 6) | 1-2 | If user overrode gate, reflect here |

---

## Equity vs Brand-Primary Profile

In brand-primary mode, domain equity is still collected and reported - but it's **not included in the weighted score**. The weight table in SKILL.md shows 0% for brand-primary.

Why: A brand-primary buyer is building name recognition from scratch. SEO history on the domain is irrelevant noise for that goal. Report it informational ("this domain has TF 35, aged 8yr - fyi if you ever pivot to seo-heavy").

---

## Confidence Labeling

Always append a confidence marker to domain equity findings:

- `confidence: high` - WHOIS + archive + Majestic/Ahrefs all available
- `confidence: medium` - WHOIS + archive, no paid link data
- `confidence: low` - WHOIS redacted or archive empty, no link data
