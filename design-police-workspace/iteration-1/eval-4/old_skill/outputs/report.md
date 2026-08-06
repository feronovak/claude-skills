# Design Police Audit — Account Settings (relay-console)

**Scope:** `/home/fnovak/.claude/skills/design-police-workspace/fixtures/project-noserver`, route `/settings/` (`public/settings/index.html`)
**Method:** Source read + live audit via Playwright at 375px, 768px, 1440px (`npm run dev`, served on `http://127.0.0.1:8899/settings/`)

## VERDICT: FAIL (25 failures)

## public/settings/index.html (CODE)

FAIL index.html:2 - `maximum-scale=1` in viewport meta blocks pinch-zoom [Anti-pattern]
FAIL index.html:32 - `.card { transition: all 0.2s ease }` - must list properties explicitly, not `all` [Anti-pattern]
FAIL index.html:68 - `.icon-btn { outline: none }` with no `:focus-visible` replacement anywhere in the stylesheet [Anti-pattern / Contrast]
FAIL index.html:90 - `.save { outline: none }` with no `:focus-visible` replacement [Anti-pattern / Contrast]
FAIL index.html:38 - `.card h2 { text-transform: uppercase }` with default (0) letter-spacing - needs 0.05-0.12em [Anti-pattern / Repetition]
FAIL index.html:122 - `<img class="avatar">` missing `width`/`height` attributes [Anti-pattern / CLS]
FAIL index.html:161 - `<div class="danger" onclick="deleteAccount()">` - click handler on a `<div>`, not a `<button>` [Anti-pattern]; also the account-deletion control has zero confirmation step (interaction.md: destructive actions need a confirm modal or undo window)
FAIL index.html:167 - `console.log("delete account clicked")` left in production code [Anti-pattern]
FAIL index.html:18,23,30-31,37,46,79,87,101-102,110,160 - spacing values 23px, 13px, 21px, 14px, 9px, 26px, 3px, 7px, 5px used throughout - 9 of ~11 distinct spacing values are off the 4px scale, compliance far under the 70% floor [Repetition]
FAIL index.html:66,99,107 - font-size 13px (`.icon-btn`), 11px (`.badge`), 13px (`.danger`) - all below the 14px absolute floor [Anti-pattern]
FAIL index.html (whole `<style>` block) - no `line-height` declared anywhere; every text block falls back to the browser default (~1.14x), below the 1.4 minimum for body text [Repetition]
FAIL index.html:51-58 - `.value { overflow: hidden; white-space: nowrap }` with no `text-overflow: ellipsis` - content is silently clipped, not just visually tight [Anti-pattern]
FAIL index.html (whole document) - zero semantic landmarks (`<main>`, `<header>`, `<nav>`); the entire page is a single `<div class="shell">` [accessibility.md]
FAIL index.html (whole `<style>` block) - no `:hover` rule for `.icon-btn`, `.save`, or `.danger` - none of the interactive elements give visual feedback on hover [interaction.md]
FAIL index.html:61-62 - `.icon-btn` hardcoded to `28px x 28px`, fixed and non-responsive - below the 44x44 touch-target minimum on every viewport

## /settings/ at 375px / 768px / 1440px (COMPUTED)

*The stylesheet has no `@media` query, so the layout does not change across breakpoints - every computed failure below reproduces identically at all three widths.*

FAIL [Repetition] spacing: computed margin/padding pulled 11 distinct off-scale values (23, 21, 14, 13, 9, 7, 5, 3, 26px...) - scale compliance well under 70%
FAIL [Repetition] type scale: sizes in use are 22/15/15/14/13/13/11px with no modular ratio; three of them (13, 13, 11px) sit below the 14px floor
FAIL [Proximity] touch targets: `.icon-btn` measures 28x28px (x3 - weekly digest, deploy alerts, billing receipts), `.save` measures 147x41px (4px short of 44), `.danger` measures 214x25px - all below the 44x44 minimum
FAIL [Contrast] APCA: `.value` text `#9aa1ad` on `#fff`, 14px/400, computes to Lc ~ 53 - requires Lc >= 100. The account **email** and **workspace name** - the two most identity-critical fields on the page - are the lowest-contrast text on it
FAIL [Repetition] line-height: computed row-label box-height / font-size ratio = 1.14 - below the 1.4 floor for body text
FAIL text overflow confirmed: `.value` `scrollWidth` (339px for the email, 273px for the workspace name) exceeds `clientWidth` (140px) for both rows - text is being cut, not just visually snug
FAIL avatar: `naturalWidth`/`naturalHeight` = 0, rendered box = 0x0px - the broken image doesn't just fail to load, it reserves no layout space at all

## /settings/ at 375px / 768px / 1440px (VISUAL)

FAIL [Alignment / Figure-Ground] the yellow "PRO" badge (`position: absolute; top:10px; left:18px` relative to `.save-wrap`) sits directly on top of the "Save changes" button and covers the word "Save" - the page's primary CTA visibly reads as "[PRO] changes" at all three viewports
FAIL [Figure-Ground] Avatar row renders empty - broken image (404 on `/avatars/fnovak.png`), no fallback initials/placeholder, nothing visible next to the "Avatar" label
FAIL Email and Workspace values are visibly truncated mid-character ("frantisek.novak.long...", "Ringier Slovakia Pro...") with no ellipsis or other affordance that more text exists behind the cut

No horizontal scrollbar at any tested width - that specific check passes.

---

## Screenshots

- `settings-375.png` - mobile (375px) - badge/button overlap and clipped values clearly visible
- `settings-768.png` - tablet (768px) - identical bugs, layout unchanged
- `settings-1440.png` - desktop (1440px) - identical bugs; fixed-width value column truncates even with abundant free space

## Console (live page load)

- `404` on `http://127.0.0.1:8899/avatars/fnovak.png` (the broken avatar above)
- `404` on `/favicon.ico` (cosmetic, not scored)

---

## What now?

1. Fix critical now
2. Fix specific items (cite line numbers or rule tags)
3. Re-audit the same scope
4. Note for later (write to docs/design-debt.md)
5. Acknowledge - won't fix, continue
6. Write something else (free text)

```jarvis-gate
{"options":[
  {"id":"fix_critical","label":"Fix critical now","style":"success","response":"fix all critical anti-pattern failures from the verdict above; leave moderate/cosmetic items for later"},
  {"id":"fix_specific","label":"Fix specific items","ask":"Which specific failures should we fix? (cite line numbers or rule tags)"},
  {"id":"reaudit","label":"Re-audit","response":"re-run the audit on the same scope and produce a new verdict"},
  {"id":"defer","label":"Note for later","response":"note all failures in docs/design-debt.md (create if missing) and continue without fixing now"},
  {"id":"acknowledge_wontfix","label":"Acknowledge (won't fix)","style":"danger","response":"acknowledged - will not fix; continue"}
]}
```
