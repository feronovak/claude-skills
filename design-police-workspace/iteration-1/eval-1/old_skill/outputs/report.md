## VERDICT: FAIL (19 failures)

Scope: `/home/fnovak/.claude/skills/design-police-workspace/fixtures/article/index.html`, live at `http://127.0.0.1:8811/article/`. Code audit + Playwright live audit (computed styles + screenshots) at 375px, 768px, 1440px.

## fixtures/article/index.html (CODE)

FAIL index.html:97 - `<img class="hero" src="/img/hero-datacenter.jpg">` has no `width`/`height` attributes - CLS risk, and this is an instant-fail anti-pattern regardless of context.

FAIL index.html:92 - `<a href="https://example.com/feed" target="_blank">RSS</a>` opens a new tab without `rel="noopener noreferrer"`. External links may use `target="_blank"`, but must ship the `rel` pair (tabnabbing risk + missing perf isolation).

FAIL index.html:47 - `h1 { font-size: 21px }` against `p { font-size: 18px }` body text. h1 must be >=1.5x body (27px minimum). 21px is only 1.17x. [Contrast]

FAIL index.html:47,53 - h1 (21px) vs h2 (19px): a 1.1x gap. Two heading levels that are supposed to signal different importance render almost indistinguishable at reading distance. [Contrast]

FAIL index.html - Type scale is not modular. Sizes in use: 13, 14, 15, 16, 18, 19, 21px. Against an editorial base of 18px / ratio 1.25 (steps: 11.52, 14.4, 18, 22.5), only 14px and 18px land within 5% tolerance; 13, 15, 19, 21 all miss every step. This isn't a scale, it's arbitrary per-element picks. [Repetition]

FAIL index.html:60 - `p { margin: 0 0 18px }` - 18px is not on the 4px spacing scale (nearest valid: 16 or 20). [Repetition]

FAIL index.html:26 - `header nav { gap: 18px }` - 18px off-scale. [Repetition]

FAIL index.html:27 - `header nav { padding-bottom: 14px }` - 14px off-scale. [Repetition]

FAIL index.html:55 - `h2 { margin: 28px 0 10px }` - neither 28px nor 10px is on the spacing scale (nearest: 24/32 and 8/12). [Repetition]

FAIL index.html:109-112 - A full paragraph of `Lorem ipsum dolor sit amet...` is shipped inline between real paragraphs. Instant-fail placeholder content, and it renders live on the page - not a comment, not stripped before "finished."

FAIL index.html:129 - `<p class="tag">TODO: add author bio + newsletter CTA here before publish</p>` ships as visible, styled, live content. Instant-fail placeholder content.

FAIL index.html - No `max-width` anywhere on `.wrap`, `article`, or `p`. The text column is fully unconstrained and grows with the viewport (confirmed live, see 1440px below). [Alignment]

## / at 375px (COMPUTED)

FAIL [Repetition] spacing scale compliance 60% (18/30 checked values on-scale) - below the 70% floor. Off-scale values: nav gap 18px, nav padding-bottom 14px, every `p` margin-bottom 18px, both `h2` margin-top 28px / margin-bottom 10px.

FAIL [Proximity] nav touch targets all fail height: Home 44x31px, Archive 56x31px, About 44x31px, RSS 29x31px. Every nav link is under the 44x44px minimum; RSS fails both axes.

FAIL [Contrast] byline `.byline` - `rgb(180,180,180)` (#b4b4b4) on white, 14px/400. Computed APCA Lc ~ 41, required Lc >= 100. Less than half the required contrast.

FAIL [Contrast] `.tag` (TODO line) - same #b4b4b4 on white at 13px/400. Lc ~ 41 against an even stricter small-text threshold. Effectively unreadable at arm's length.

## / at 768px (COMPUTED)

FAIL [Repetition] spacing scale compliance 62% (18/29) - same broken-scale values reproduced at this viewport.

Note: body line-length measured 80 characters exactly here (the hard ceiling) with zero max-width margin - confirms the container has no safety constraint (see 1440px, where this breaks outright).

## / at 1440px (COMPUTED)

FAIL [Alignment][Repetition] body text line-length 154 characters - nearly double the 80-char hard limit (target 45-75ch). Caused directly by the missing `max-width` noted in the code audit: `article` renders at the full 1392px content width with no reading-measure constraint.

FAIL [Repetition] spacing scale compliance 62% (18/29) - same off-scale values as other viewports.

## / at 375px, 768px, 1440px (VISUAL)

FAIL [Visual anti-pattern] Hero image is broken at every viewport: `GET /img/hero-datacenter.jpg` 404s (confirmed via console + `naturalWidth: 0`). Renders as an empty grey box with the alt text exposed in the top-left corner across all three screenshots.

FAIL [Visual anti-pattern] Placeholder content renders live on the page, not just in source: the Lorem ipsum paragraph sits between two real paragraphs mid-article, and "TODO: add author bio + newsletter CTA here before publish" is styled and visible right above the footer rule - reads as an unfinished draft shipped as final.

FAIL [Alignment] At 1440px the body copy stretches edge-to-edge across the full 1392px content width with no visual column - confirms the line-length failure above; the eye can't track a line back to its start.

No horizontal scroll at any viewport. Heading hierarchy has no skipped levels (h1 -> h2 -> h2). Both `<h2>`s present, no h3/h4 gaps. Images (the one that loads) carry descriptive `alt` text. Viewport meta doesn't block pinch-zoom.

---

**What now?**
1. Fix critical now
2. Fix specific items (cite line numbers or rule tags)
3. Re-audit the same scope
4. Note for later (write to docs/design-debt.md)
5. Acknowledge - won't fix, continue
6. Write something else (free text)
