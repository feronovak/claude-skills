## VERDICT: FAIL (11 failures)

Coverage: `/article/` audited — source (`fixtures/article/index.html`, confirmed byte-identical to what the server returns) and live render at 375px, 768px, 1440px via Playwright, using `scripts/probe.js` for computed-style measurement. This is a single-template fixture with one route in scope; nothing was skipped.

### BLOCKER

FAIL [Visual] `/article/` all viewports - hero image 404s (`/img/hero-datacenter.jpg`, HTTP 404 confirmed). Renders as a ~700–950px tall empty grey box with only the alt text ("Racks in a data centre") visible in the corner — the single largest element on the page is broken, on every viewport.

FAIL [Visual] `/article/` - Lorem ipsum paragraph is live in the article body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt..." — placeholder copy shipped as the second real paragraph of the article.

FAIL [Visual] `/article/` - editorial note is live on the page: `<p class="tag">TODO: add author bio + newsletter CTA here before publish</p>` renders as visible text at the bottom of the article, not a code comment.

FAIL [Contrast] `/article/` - 3 elements use `var(--meta)` (`#b4b4b4` / `rgb(180,180,180)`) grey-on-white text below the APCA readability floor for their size: byline ("Fero Novak · 6 August 2026 · 9 min read", 14px/400, Lc 40.5, floor 75), the TODO tag line (13px/400, Lc 40.5, floor 75), and the footer copyright line (18px/400, Lc 40.5, floor 60 — see the DEFECT below on why it's 18px, not the intended 14px). All three are meaningfully below their floor, not just under target — genuinely hard to read.

FAIL [Layout] `/article/` 375px - all 4 nav links ("Home" 44×31, "Archive" 56×31, "About" 44×31, "RSS" 29×31) are 31px tall, below the 44px mobile touch-target minimum; RSS is also under 44px wide. Every primary nav control on the page fails the touch-target floor on mobile.

### DEFECT

FAIL [Repetition] `/article/` - spacing compliance 65% (below the 90% pass bar): 3 distinct off-scale values — 10px, 14px, 18px — used for `nav padding-bottom`, `nav row/column-gap`, `h2 margin-bottom`, and every paragraph's `margin-bottom`. None are on the 4px-base scale.

FAIL [Contrast] `/article/` - h1 (21px) vs h2 (19px) is a 1.10x size ratio, and h1 vs body text (18px) is 1.17x — both below the 1.2x minimum the Contrast principle requires between distinguishable levels, and h1 is well under the 1.5x-of-body floor typography.md sets for a top-level heading. Confirmed visually: in the 1440px screenshot the headline ("The Quiet Case for Boring Infrastructure") is barely distinguishable in size from the two h2 subheads ("What boring actually buys you", "The cost nobody prices in") — only the bold weight tells them apart.

FAIL [Alignment] `/article/` - no `max-width` on the text container (`.wrap` has only 24px side padding, no cap). Real rendered line length hits 166–168 characters at 1440px and 83–87 characters at 768px, both over the 80ch ceiling — more than double the ideal at desktop width.

FAIL `/article/` - CSS cascade bug on the footer copyright line: `<p>© 2026 Field Notes. All rights reserved.</p>` sits inside `<footer>`, which sets `font-size: 14px; color: var(--meta)`. The generic `p { font-size: 18px }` rule applies directly to that `<p>` and wins over the inherited 14px (a direct rule on an element always beats an inherited value), while `color` — which `p` never sets — is correctly inherited as grey. Net effect: the copyright line renders at body-text size (18px) instead of the small caption size the footer was clearly written to produce, compounding the contrast failure above.

FAIL [Repetition] `/article/` - `.tag` (the TODO line) is 13px, below the 14px absolute floor for any text on the page.

FAIL `/article/` - hero `<img>` has no `width`/`height` attributes, so the browser can't reserve layout space before it loads (CLS risk); also a straight anti-pattern-list violation independent of the broken-image issue.

### POLISH (not counted)

- The byline sits above the h1, not below it — an unconventional editorial order, but a legitimate stylistic choice, not a defect.
- The entire page is black/grey/white with zero accent color — no hue anywhere for links, the brand, or a highlight. Nothing gives the eye a figure-ground anchor; it reads as unfinished-plain rather than deliberately restrained. (Art director's note.)
- Once the hero image is fixed, give it a reserved aspect-ratio (not just a placeholder background) so layout doesn't jump between broken and loaded states.

---

**What now?**
1. 🔧 Fix blockers now
2. 🎯 Fix specific items (cite line numbers or rule tags)
3. 🔁 Re-audit the same scope
4. 📝 Note for later (write to docs/design-debt.md)
5. ⚠️  Acknowledge — won't fix, continue
6. ✏️  Write something else (free text)

```jarvis-gate
{"options":[
  {"id":"fix_critical","label":"🔧 Fix blockers now","style":"success","response":"fix every BLOCKER from the verdict above; leave DEFECT and POLISH items for later"},
  {"id":"fix_specific","label":"🎯 Fix specific items","ask":"Which specific failures should we fix? (cite line numbers or rule tags)"},
  {"id":"reaudit","label":"🔁 Re-audit","response":"re-run the audit on the same scope and produce a new verdict"},
  {"id":"defer","label":"📝 Note for later","response":"note all failures in docs/design-debt.md (create if missing) and continue without fixing now"},
  {"id":"acknowledge_wontfix","label":"⚠️ Acknowledge (won't fix)","style":"danger","response":"acknowledged — will not fix; continue"}
]}
```
