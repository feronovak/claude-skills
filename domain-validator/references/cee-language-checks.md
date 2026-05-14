---
name: cee-language-checks
description: Pejorative scans, phonetic pitfalls, and false friends for domain strings across EN/SK/CZ/PL/DE/HU
author: feronovak
---

# CEE Language Checks

Used in Gate 1 (Spelling Trap) and Gate 4 (Pejorative Meaning).

Always add disclaimer: "Pejorative scan is best-effort and non-exhaustive. Confirm with native speakers before launch."

---

## Phonetic Pitfall Patterns by Language

### Slovak (SK)

| Pattern | Risk | Example |
|---|---|---|
| `y` / `i` | Interchangeable sound in SK; EN speakers expect `y` = /j/ or /aɪ/ | `byznys` looks SK, `biznis` looks EN |
| `c` | In SK = /ts/; EN readers expect /k/ or /s/ | `Cena.sk` = "price" in SK but feels like `Sena` to EN ear |
| `ch` | SK = /x/ guttural; EN = various | `Chalupa` fine in SK, confusing in EN |
| `š`, `č`, `ž`, `ľ`, `ň` | Diacritics don't work in domain names; romanization varies | `Capek` vs `Čapek` |
| `á`, `é`, `í`, `ó`, `ú` | Long vowels; drop in domain → spelling ambiguity | `Kupnoviny` vs `Kupnoviny` |

### Czech (CZ)

| Pattern | Risk | Example |
|---|---|---|
| `ř` | Unique sound; romanized as `r` but `rz` in Polish | Confusion across borders |
| `v` + consonant clusters | Tongue-twister for EN speakers | `vstr` clusters |

### Polish (PL)

| Pattern | Risk | Example |
|---|---|---|
| `w` | Pronounced /v/ in PL; EN reads as /w/ | `Wawa` = Warsaw in PL, sounds different |
| `ó` → `u` romanization | Inconsistent; creates two spellings | |
| `sz` / `cz` / `szcz` | Digraphs confusing to EN speakers | |
| `j` | Pronounced /j/ in PL, /dʒ/ expectation in EN | |

### German (DE)

| Pattern | Risk | Example |
|---|---|---|
| `v` | Pronounced /f/ in DE | `Vogel` = "foh-gel" |
| `w` | Pronounced /v/ in DE | Swaps with `v` |
| `ie` vs `ei` | /ee/ vs /eye/ - easy confusion | `Kiel` vs `Keil` |
| `ß` | Not usable in domains; becomes `ss` | `strasse` vs `straße` |
| `ü`, `ä`, `ö` | Drop diacritics → `ue`, `ae`, `oe` or just drop → ambiguity | |

### Hungarian (HU)

| Pattern | Risk | Example |
|---|---|---|
| `cs` | Pronounced /tʃ/ | Looks like `c` + `s` to non-HU |
| `gy` | Pronounced /dj/ | Opaque to everyone else |
| `sz` | Pronounced /s/ in HU (vs /ʃ/ in PL) | Cross-market confusion |
| `zs` | Pronounced /ʒ/ | |

---

## Common Pejorative / False Friend Lookups

Partial list of words that appear innocent in one language but are problematic in another. Not exhaustive.

| String | Language issue | Notes |
|---|---|---|
| `kunt` | EN - vulgar | Any domain containing this substring |
| `fick` | DE - vulgar ("fuck") | Check substrings |
| `merde` | FR - vulgar | If FR is in scope |
| `puta` | ES - vulgar | If ES in scope |
| `piča` | SK/CZ - vulgar | |
| `hovado` | SK - vulgar (bovine insult) | |
| `suka` | SK/CZ/PL/RU - vulgar (bitch) | Common word in SL = "bitch" |
| `bič` | SK - "whip" (not vulgar but odd) | |
| `anal` | Universal - sexual | Any substring match |
| `ass` | EN - vulgar | Substring: `class`, `brass` are fine; `basshole` not |
| `sex` | Most markets - flaggable | Not always a reject, context-dependent |
| `shit` | EN - vulgar | Substring check |
| `fag` | EN - slur | |
| `cum` | EN - sexual | Substring: `document`, `accumulate` are fine |

**Substring check rule:** For Gate 4, always check for embedded profanity in compound domains. Run the domain string through the list above looking for substrings, not just whole-word matches.

---

## SK-Specific False Friends (EN brands that read badly in Slovak)

| Domain | Reads as in SK | Issue |
|---|---|---|
| `kupa.com` | "kúpa" = "bath" or "buying" | Odd for non-retail |
| `vata.com` | "vata" = "cotton wool" / "BS" (colloquial) | "That's vata" = meaningless |
| `nos.sk` | "nos" = "nose" | Fine if intentional |
| `psa.sk` | "psa" = "of a dog" (genitive) | Unintentionally funny |

---

## Process Note

When running Gate 4:
1. Check the full domain string as one word (e.g. `speedassist` → check for `ass`)
2. Check any obvious component words split at natural word boundaries
3. Check across EN, SK, CZ, PL, DE, HU
4. If domain targets specific non-listed markets, flag: "pejorative check not run for [language] - verify manually"
