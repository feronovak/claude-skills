# Design Police Audit — Account Settings

**Scope:** `http://127.0.0.1:8811/app/` (source: `fixtures/app/index.html`)
**Method:** source read + Playwright live inspection (computed styles, APCA contrast, touch targets) at 375px / 768px / 1440px, plus full-page screenshots at each.

## VERDICT: FAIL (27 failures)

---

## fixtures/app/index.html (CODE)

FAIL fixtures/app/index.html:18 - `.shell` padding `23px 13px` — neither value on the 4px spacing scale (nearest: 24, 12)
FAIL fixtures/app/index.html:23 - `h1` margin-bottom `23px` — not on spacing scale (nearest: 24)
FAIL fixtures/app/index.html:30 - `.card` padding `21px` — not on spacing scale (nearest: 20)
FAIL fixtures/app/index.html:31 - `.card` margin-bottom `13px` — not on spacing scale (nearest: 12)
FAIL fixtures/app/index.html:32 - `.card` `transition: all 0.2s ease` — must list properties explicitly, not `all`
FAIL fixtures/app/index.html:37 - `.card h2` margin-bottom `14px` — not on spacing scale (nearest: 12 or 16)
FAIL fixtures/app/index.html:38 - `.card h2` `text-transform: uppercase` with default `letter-spacing` (0) — needs 0.05–0.12em
FAIL fixtures/app/index.html:46 - `.row` padding `9px 0` — not on spacing scale (nearest: 8)
FAIL fixtures/app/index.html:61-62 - `.icon-btn` is `28x28px` — below the 44x44px minimum touch target on every button used for Weekly digest / Deploy alerts / Billing receipts
FAIL fixtures/app/index.html:66 - `.icon-btn` `font-size: 13px` — below the 14px absolute floor
FAIL fixtures/app/index.html:68 - `.icon-btn` `outline: none` with no `:focus-visible` replacement — keyboard users lose all focus indication
FAIL fixtures/app/index.html:87 - `.save` padding `12px 26px` — 26px not on spacing scale (nearest: 24)
FAIL fixtures/app/index.html:90 - `.save` `outline: none` with no `:focus-visible` replacement
FAIL fixtures/app/index.html:93-103 - `.badge` `font-size: 11px` — below the 14px absolute floor
FAIL fixtures/app/index.html:101 - `.badge` padding `3px 7px` — not on spacing scale (nearest: 4/8)
FAIL fixtures/app/index.html:94-96 - `.badge` `position: absolute; top: 10px; left: 18px` inside `.save-wrap` places the "PRO" badge on top of the button label instead of at a corner — confirmed broken in the live screenshots (see VISUAL below): renders as "PROchanges"
FAIL fixtures/app/index.html:105-111 - `.danger` `font-size: 13px` — below the 14px absolute floor, used on a destructive action label
FAIL fixtures/app/index.html:122 - `<img class="avatar">` has no `width`/`height` attributes (and `.avatar` sets none in CSS either) — CLS risk; also the image 404s in the live app (`/avatars/fnovak.png` — confirmed via console)
FAIL fixtures/app/index.html:51-58 - `.value` (`width: 140px; overflow: hidden; white-space: nowrap`) has no `text-overflow: ellipsis` and no `title` attribute — Email and Workspace values are silently truncated mid-word with no way to read the full value (confirmed in screenshots: "frantisek.novak.long…", "Ringier Slovakia Pro…")
FAIL fixtures/app/index.html:160 - inline `style="margin-top: 23px"` — inline style overriding the design system, and 23px is itself off-scale
FAIL fixtures/app/index.html:161 - `<div class="danger" onclick="deleteAccount()">` — click handler on a `<div>` instead of a `<button>`; not keyboard-reachable, no semantic role
FAIL fixtures/app/index.html:161-168 - "Delete this account permanently" fires `deleteAccount()` immediately (currently just a `console.log`) with no confirmation modal or undo — destructive action needs a confirmation step
FAIL fixtures/app/index.html:167 - `console.log()` left in production code

## / at 375px, 768px, 1440px (COMPUTED)

Layout doesn't adapt between breakpoints (single column throughout, `.shell` just centers via `max-width: 720px`), so every computed value below is identical at all three viewports — reported once.

FAIL [Repetition] Spacing scale compliance: **1 of 10** distinct declared spacing values (only `12px`) is on the 4px scale — 23, 13, 21, 14, 9, 26, 7, 5, 3px are all off-scale. Well under the 70% compliance floor — this page has no spacing system.
FAIL [Repetition] Type scale: 6 distinct font sizes in use (11, 13, 14, 15, 16, 22px) — not a modular scale, reads as a linear micro-scale (13→14→15→16) explicitly called out as a violation, not systematic sizing.
FAIL [Contrast] APCA: `.value` (Email/Workspace) `#9aa1ad` on `#fff`, 14px/400 → **Lc ≈ 48** (min Lc 100 required at 14px/400). Account email and workspace name are borderline illegible.
FAIL [Contrast] APCA: `.danger` "Delete this account permanently" `#d92d20` on `#f7f8fa`, 13px/400 → **Lc ≈ 66** — under threshold, and on an undersized (13px) destructive-action label.
FAIL [Contrast] APCA: `.card h2` section labels (PROFILE / NOTIFICATIONS) `#6b7280` on `#fff`, 15px/700 → **Lc ≈ 70** (min ≈72-75 required) — borderline fail.
FAIL [Contrast] APCA: `.badge` "PRO" `#3a2f00` on `#ffcc00`, 11px/700 → **Lc ≈ 71** — undersized text at a contrast level that doesn't clear the bar for that size.
FAIL [Contrast] APCA: `.save` button label `#fff` on `#2f5cff`, 15px/400 → **Lc ≈ 77** (min ≈95 required at 15px/400) — the primary CTA's own label is under-contrast against its fill color.
FAIL [Proximity] Touch targets: `.icon-btn` (Weekly digest / Deploy alerts / Billing receipts toggles) measure **28×28px**, `.save` button measures **147×41px** (height under 44), `.danger` delete row measures **214×25px** — all below the 44×44px minimum interactive target size.

PASS - no horizontal scroll at any viewport (`scrollWidth == viewportWidth` at 375/768/1440)

## / at 375px, 768px, 1440px (VISUAL)

FAIL [Alignment] Avatar image renders as a blank box — `/avatars/fnovak.png` 404s (confirmed via browser console), and with no `width`/`height` set it collapses to nothing rather than showing a placeholder.
FAIL [Proximity] Email ("frantisek.novak.long…") and Workspace ("Ringier Slovakia Pro…") values are visibly cut off mid-word at every viewport, with no ellipsis or truncation affordance — user cannot tell the value is incomplete or recover the full text.
FAIL [Figure-Ground] The "PRO" badge sits directly on top of the "Save changes" button label — the button visibly reads "PROchanges" at all three viewports. This is a broken/overlapping element, not intentional layering.
FAIL [Contrast] The Weekly digest / Deploy alerts (on) and Billing receipts (off) toggle buttons are styled identically regardless of state — no color, fill, or weight difference distinguishes "on" from "off." State is conveyed by the text alone, so at a glance all three toggles look the same.

---

## Screenshots

- `screenshot-1440.png` — desktop, full page
- `screenshot-768.png` — tablet, full page
- `screenshot-375.png` — mobile, full page

All three show the same three visual bugs: broken avatar, truncated Email/Workspace values, and the PRO badge overlapping "Save changes."

---

## What now?

1. 🔧 Fix critical now
2. 🎯 Fix specific items (cite line numbers or rule tags)
3. 🔁 Re-audit the same scope
4. 📝 Note for later (write to docs/design-debt.md)
5. ⚠️ Acknowledge — won't fix, continue
6. ✏️ Write something else (free text)

```jarvis-gate
{"options":[
  {"id":"fix_critical","label":"🔧 Fix critical now","style":"success","response":"fix all critical anti-pattern failures from the verdict above; leave moderate/cosmetic items for later"},
  {"id":"fix_specific","label":"🎯 Fix specific items","ask":"Which specific failures should we fix? (cite line numbers or rule tags)"},
  {"id":"reaudit","label":"🔁 Re-audit","response":"re-run the audit on the same scope and produce a new verdict"},
  {"id":"defer","label":"📝 Note for later","response":"note all failures in docs/design-debt.md (create if missing) and continue without fixing now"},
  {"id":"acknowledge_wontfix","label":"⚠️ Acknowledge (won't fix)","style":"danger","response":"acknowledged — will not fix; continue"}
]}
```
