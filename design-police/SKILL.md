---
name: design-police
description: Use when reviewing any web UI for quality - after building web pages, web apps, components, or layouts. Triggers: "review UI", "check design", "audit page", "validate frontend", "design police", "does this look good", "check my site". Also use proactively after building or modifying any web interface, even if not explicitly asked. Inspects source code AND live pages via Playwright at multiple viewports. Binary pass/fail - any anti-pattern = FAIL.
---

# Design Police

Binary pass/fail audit of web interfaces. Reads source files AND inspects live pages via Playwright (computed styles, screenshots). Any anti-pattern is a failure.

## How to Run

### 1. Determine Scope

`$ARGUMENTS` = files, directories, or URLs to review. If empty, review all files changed in current branch vs main.

### 2. Code Audit

Read each source file. Check against code-level rules. Every violation is a FAIL item.

### 3. Live Audit (Playwright)

For each distinct page/route, at 3 viewports (375px, 768px, 1440px):

**A. Extract computed styles** via `page.evaluate()`:
- All margin, padding, gap values (check spacing scale compliance)
- All font sizes, line heights, font weights (check type scale)
- All text element widths in characters (check line length)
- All colors: text color + background color pairs (check APCA contrast)
- All interactive element dimensions (check touch targets)

**Measurement pitfalls (avoid these):**
- **Line length:** Do NOT use `element.offsetWidth / (fontSize * 0.5)` — this measures the container, not the text, and overestimates by 20-40%. Use `Range.getClientRects()` to measure actual rendered line widths. See `rules/typography.md` for the correct snippet.
- **Touch targets:** Use `Math.round(rect.width)` and `Math.round(rect.height)` before comparing to 44px. Subpixel rendering produces values like 43.99 for elements that are actually 44px. Elements at exactly 44px PASS.
- **Text colors:** Count structural roles (primary, secondary, muted per surface context) + brand accent. Semantic/category colors (niche tags, error/success states) are separate and don't count against the limit. Report the breakdown, not just the raw count. See `rules/color.md`.

**B. Take screenshots** for visual checks that can't be computed:
- Overall visual hierarchy and balance
- Broken images, placeholder content
- Layout breakage, overlapping elements

### 4. Verdict

```
PASS - 0 failures found
FAIL - N failures found
```

No warnings. No suggestions. Pass or fail.

**If Playwright is unavailable:** Run code-audit only. Note in the verdict that COMPUTED and VISUAL checks were skipped due to no browser access.

### 5. Post-Verdict Gate

After the verdict, present BOTH a numbered list (for terminal users) AND a `jarvis-gate` block (Discord buttons in JARVIS; hidden noise in terminal).

**On PASS:**

```
**What now?**
1. ✅ Acknowledge
2. 📋 Audit different scope (specify which)
3. ✏️  Write something else (free text)
```

Then append the gate block:

````
```jarvis-gate
{"options":[
  {"id":"acknowledge","label":"✅ Acknowledge","style":"success","response":"acknowledged"},
  {"id":"different_scope","label":"📋 Audit different scope","ask":"Which files, directories, or URLs should we audit next?"}
]}
```
````

**On FAIL:** prioritize fixing. Default option is to fix critical anti-patterns inline.

```
**What now?**
1. 🔧 Fix critical now
2. 🎯 Fix specific items (cite line numbers or rule tags)
3. 🔁 Re-audit the same scope
4. 📝 Note for later (write to docs/design-debt.md)
5. ⚠️  Acknowledge — won't fix, continue
6. ✏️  Write something else (free text)
```

Then append the gate block:

````
```jarvis-gate
{"options":[
  {"id":"fix_critical","label":"🔧 Fix critical now","style":"success","response":"fix all critical anti-pattern failures from the verdict above; leave moderate/cosmetic items for later"},
  {"id":"fix_specific","label":"🎯 Fix specific items","ask":"Which specific failures should we fix? (cite line numbers or rule tags)"},
  {"id":"reaudit","label":"🔁 Re-audit","response":"re-run the audit on the same scope and produce a new verdict"},
  {"id":"defer","label":"📝 Note for later","response":"note all failures in docs/design-debt.md (create if missing) and continue without fixing now"},
  {"id":"acknowledge_wontfix","label":"⚠️ Acknowledge (won't fix)","style":"danger","response":"acknowledged — will not fix; continue"}
]}
```
````

Terminal users reply with the number or free text. Discord users tap a button or type a reply.

## Output Format

```
## VERDICT: FAIL (7 failures)

## src/pages/index.astro (CODE)

FAIL src/pages/index.astro:42 - img missing width/height
FAIL src/pages/index.astro:55 - heading jumps h1 to h3

## / at 375px (COMPUTED)

FAIL [Repetition] body line-length 94 chars (max 75)
FAIL [Repetition] spacing: 23px margin not on 4px scale
FAIL [Proximity] nav link touch target 32x28px (min 44x44)

## / at 1440px (COMPUTED)

FAIL [Repetition] type scale: h2 is 28px, expected 30px (scale: 16 * 1.25^4 = 30.5)
FAIL [Contrast] APCA: #888 on #fff = Lc 63 (min 75 for 14px/400)

## / at 375px (VISUAL)

FAIL [Alignment] horizontal scrollbar visible - content breaks grid

## / at 1440px (VISUAL)

PASS
```

Principle tags: `[Contrast]`, `[Repetition]`, `[Alignment]`, `[Proximity]`. These tell the developer which fundamental principle is violated, not just which threshold was missed.

## Rules

Load all rule files for every audit:
- `rules/principles.md` - **READ FIRST.** CRAP + Gestalt - the WHY behind every rule. Use this to explain failures.
- `rules/design-tokens.md` - Spacing scale, type scale, color palette, shadows (THE CORE - enforces Repetition)
- `rules/typography.md` - Font pairing, type scale, line length/height, heading proximity, text color hierarchy, spacing
- `rules/typography-presets.md` - Content-type presets: editorial, marketing, e-commerce, docs, dashboard (load when recommending improvements)
- `rules/color.md` - APCA contrast, palette limits, 60-30-10, dark mode (enforces Contrast + Figure-Ground)
- `rules/layout.md` - Grid, max-width, margins, density, responsive, aspect ratios (enforces Alignment + Proximity)
- `rules/interaction.md` - Forms, touch, animation, hover, navigation
- `rules/accessibility.md` - Semantic HTML, ARIA, keyboard, focus (lower priority)
- `rules/performance.md` - CLS, LCP, lazy loading, virtualization
- `rules/anti-patterns.md` - Instant-fail patterns (the blocklist)

Priority order: principles > design-tokens > typography > color > layout > interaction > performance > accessibility.

When reporting failures, cite which principle is violated (Contrast, Repetition, Alignment, Proximity) alongside the specific threshold. This helps the developer understand not just what's wrong but why it matters.

Any match in `rules/anti-patterns.md` = automatic FAIL regardless of context.
