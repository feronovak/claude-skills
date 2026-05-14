---
name: gates-and-tests
description: Per-gate test conditions, failure examples, and override rules for the domain-validator gates step
author: feronovak
---

# Gates and Tests

Seven gates. Any fail = REJECT before scoring. Gate overrides must be explicit from the user.

Referenced by: SKILL.md § Gates

---

## Gate 1 - Spelling Trap

**Test:** Ask: "If someone hears this domain spoken once, what spellings might they try?"

**Fail conditions:**
- Two or more plausible spellings exist with no clear default
- SK/EN phonetic clashes: `y` vs `i` (Slovak: y=i sound), `c` vs `k`, `s` vs `z`, `ph` vs `f`
- Silent letters that aren't obvious from category (e.g. `gnocchi` would fail)
- Ambiguous doubled consonants: `travell.com` vs `travel.com`

**Examples:**
- FAIL: `Sirup.com` - SK speaker types `sirup`, EN speaker might try `syrup`
- FAIL: `Phixer.com` - f/ph ambiguity, also `fixer` already exists
- PASS: `Kraboo.com` - one plausible spelling, phonetically unambiguous in both EN and SK

**Override:** User explicitly accepts the spelling risk (e.g. "I know, the double-meaning is intentional").

---

## Gate 2 - Homophone Collision

**Test:** Speak the domain aloud. Does it sound identical to an existing brand, product, or common word in target languages?

**Fail conditions:**
- Sounds identical to a known brand (consumer confusion)
- Sounds identical to a common SK/EN word that creates unintended meaning
- Phonetic similarity close enough to confuse over a phone (70%+ syllable match)

**Examples:**
- FAIL: `Wix.com` clone attempts - sounds like Wix
- FAIL: `Kúp.sk` - sounds like "buy" in Slovak (imperative), confusing as a brand name
- PASS: `Talealbum.com` - distinct sound, no obvious collision

---

## Gate 3 - Character Hostility

**Test:** Can you dictate this domain to someone on a bad phone call without spelling it out character by character?

**Fail conditions:**
- Contains a hyphen (must say "dash" every time)
- Contains digits (which number? "two" or "2"?)
- Contains any non-letter character: `_`, `+`, `.` (in the name, not TLD)

**Note:** Subdomains with hyphens (e.g. `my-account.brand.com`) are fine - this gate is about the registerable domain itself.

**Override:** Hyphen intentional for SEO or trademark reasons - user must state this.

---

## Gate 4 - Pejorative Meaning

**Test:** Cross-check the domain string against pejorative, vulgar, or embarrassing meanings in EN/SK/CZ/PL/DE/HU.

**Fail conditions:**
- Slang or vulgar meaning in any of the 6 languages
- Sexual, bodily, or derogatory meaning when read as a word
- Meaning that's embarrassing in the brand's target market even if not vulgar

**Process:** See `references/cee-language-checks.md` for specific lookup lists and false-friend tables.

**Always flag:** "Pejorative scan is best-effort and non-exhaustive. Confirm with native speakers before launch, especially for PL and HU."

**Override:** None - if it's genuinely vulgar in a target market, REJECT. User can re-invoke with a different candidate.

---

## Gate 5 - Trademark / Category Collision

**Test:** Does the domain string or its obvious reading match or closely approximate a registered trademark in the domain's intended operating category?

**Fail conditions:**
- Near-identical to a trademark in the same goods/services class
- Generic descriptor that could create false impression of official status (e.g. `AppleStore.com`)
- Name of a public figure without consent

**Note:** Not a legal opinion. Flag "consult trademark counsel before purchase" whenever this gate triggers.

---

## Gate 6 - Toxic History (skip for fresh-reg)

**Test:** archive.org CDX API query for the domain. Check 3+ years of snapshots.

**Fail conditions:**
- Majority of snapshots show: adult content, scam/phishing, malware delivery, politically toxic content
- Single high-profile toxic event in recent years (< 3yr) even if now clean

**Fresh-reg bypass:** If WHOIS creation date < 1yr AND archive.org shows no snapshots -> mark N/A.

**Aged bypass:** If WHOIS shows < 1yr but archive.org shows prior history -> run the gate.

---

## Gate 7 - Poisoned Link Profile (skip for fresh-reg or no paid data)

**Test:** Requires Majestic or Ahrefs data pasted by user. Examine referring domain quality.

**Fail conditions:**
- >60% of referring domains are known PBN networks or link farms
- Dominant anchor text is pharmaceutical, casino, or adult spam
- Trust Flow < 10 with Citation Flow > 30 (Majestic metric = spam signal)

**Soft-prompt rule:** In seo-primary or mixed profile on an aged domain, ask user once to paste Majestic/Ahrefs data. If they decline, score domain equity at medium confidence and note the gap. Don't ask again.
