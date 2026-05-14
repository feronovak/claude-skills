---
name: scripts-todo
description: Planned shell scripts and examples not yet created - intent and specs for future implementation
author: feronovak
---

# Scripts and Examples - To Be Created

These files are referenced in SKILL.md but not yet implemented. The core rubric in SKILL.md and the references/ files are sufficient for manual evaluation. These would add automation.

---

## Shell Scripts

### scripts/check-whois.sh

**Purpose:** Query WHOIS for a domain and extract: creation date, registrar, status (registered/expired/available).

**Expected output:**
```
Domain: example.com
Created: 2015-03-12
Registrar: Namecheap
Status: clientTransferProhibited
Age: 9yr 2mo
Classification: aged
```

**Implementation notes:**
- Use `whois` CLI, parse `Creation Date` or `created` field (registrar-dependent format)
- Fall back to `jwhois` or `python-whois` if `whois` output is garbled
- Output plain text + exit code 0 = aged, 1 = fresh-reg, 2 = not found/redacted

---

### scripts/fetch-archive-snapshots.sh

**Purpose:** Query the archive.org CDX API and return a summary of snapshot history.

**Expected output:**
```
Domain: example.com
Total snapshots: 347
First snapshot: 2014-08-01
Last snapshot: 2024-11-30
Gaps > 1yr: none
Sample URLs: [3 representative paths]
```

**Implementation notes:**
- CDX API: `https://web.archive.org/cdx/search/cdx?url=<domain>&output=json&limit=100&fl=timestamp,statuscode`
- Detect gaps by sorting timestamps and looking for > 365-day intervals
- No auth required, but rate-limit: don't hammer the API

---

### scripts/domain-sanity.sh

**Purpose:** Validate that a domain string is a legal domain name before running any evaluation.

**Checks:**
- Valid characters only (letters, digits, hyphens - no hyphens at start/end)
- No consecutive hyphens (except `xn--` punycode)
- TLD exists (against IANA list or basic regex)
- Not a subdomain (count dots)
- Length <= 253 chars, label <= 63 chars

**Exit codes:** 0 = valid, 1 = invalid with error message

---

## Example Files

### examples/single-domain.md

Worked example of Shape 1 (single domain evaluation). Should show:
- Domain: a real-ish domain candidate
- Full gates section with mixed pass/fail/NA
- Full scored axes table
- Verdict with reasoning
- Fero's voice throughout

---

### examples/list-comparison.md

Worked example of Shape 2 (ranked list of 3-5 candidates). Should show:
- Ranked table as primary output
- Two detailed scorecards for top candidates
- Rejected candidates with one-line reason each
- Clear recommendation with rationale

---

### examples/brand-contextual.md

Worked example of Shape 3 (brand-contextual evaluation). Should show:
- Brand context header block (what was pulled from memory/project)
- How brand fit axis score changes based on context vs. without it
- SK + EN bilingual evaluation in one run
