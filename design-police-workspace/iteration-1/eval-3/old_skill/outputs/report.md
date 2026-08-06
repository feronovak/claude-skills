## VERDICT: PASS (0 failures)

Scope: http://127.0.0.1:8811/clean/ (source: /home/fnovak/.claude/skills/design-police-workspace/fixtures/clean/index.html)

## index.html (CODE)

PASS - no anti-pattern matches.

- Spacing scale: --s1..--s8 = 4/8/12/16/24/32/48/64, every step >=25% over the last, all values on the accepted 4px-base scale.
- Type scale: --t-body 16 / --t-lead+h3 20 / --t-h2 25 / --t-h1 39 = 16 * 1.25^n at n=0,1,2,4. h1 (39px) is 2.44x body - clears the 1.5x minimum. Headings strictly decrease h1>h2>h3.
- 1 font family (system-ui stack) - well under the 3-family cap, no pairing-harmony issue.
- Palette: 7 distinct swatches (ink, ink-2, accent, white, surface-2, rule, accent-hover) - 1 chromatic hue (blue), 2 hues total. Under the 3/5/12 limits.
- Text color hierarchy: 2 non-semantic roles (ink = primary, ink-2 = secondary), headings and body share ink - matches the "headings use body color" rule.
- Single --radius (8px) and single --shadow-1 used consistently - no one-off radius/shadow values.
- Semantic HTML throughout: header/nav/main/section/article/footer, heading levels don't skip (h1->h2->h3).
- <img> has explicit width="1120" height="420" and descriptive alt text (CLS/a11y covered).
- :focus-visible outline defined (no outline: none trap).
- No target="_blank" anywhere; all links same-tab, consistent.
- Transitions list explicit properties (color, background-color), no transition: all.
- Viewport meta has no user-scalable=no / maximum-scale=1.
- No inline styles, no !important, no placeholder/lorem-ipsum copy, no console.log.

## / at 375px (COMPUTED)

PASS

- No horizontal scroll (scrollWidth == innerWidth == 375).
- 0 margin/padding/gap values off the spacing scale.
- Touch targets: smallest is "Docs" at 55x50px - all links/buttons clear 44x44px.
- Line length: lead/feature paragraphs measured 31-37 characters via Range.getClientRects() - well inside 45-75ch, nowhere near the 80ch fail line.
- Body font size 16px (>=14px mobile floor).

## / at 768px (COMPUTED)

PASS

- No horizontal scroll.
- 0 non-scale spacing values.
- Touch targets unchanged from mobile, all >=50px.
- Feature grid naturally reflows to 2 columns (auto-fit, minmax(260px, 1fr)) - no overlap, no fixed-width breakage.

## / at 1440px (COMPUTED)

PASS

- No horizontal scroll (scrollWidth == innerWidth == 1440); the only "off-scale" values my sweep caught were the 160px auto-centering margins on .wrap (max-width:1120px; margin:0 auto on a 1440px viewport) - that's arithmetic from centering, not a chosen spacing token, so it doesn't count against the scale.
- Font sizes on page: {16, 20, 25, 39}px - all four are exact scale steps, 0 stray sizes.
- Heading proximity (measured as actual visual gap above vs. below each heading, not just the element's own margin-top, since page-level and card-level headings get their "above" space from section/card padding rather than their own margin):
  - h1: 145px above (header + hero padding) vs 16px below -> page-level heading, matches the explicit "0/48px top" exception in the rules.
  - h2: 113px above (hero padding-bottom + features padding-top) vs 32px below -> 3.5:1, clears the 3.3:1 minimum.
  - h3 (x3): 24px above (card padding) vs 8px below -> matches the Card Typography spec exactly (8px heading->description, 16-24px card padding).
- Touch targets: all >=50x50 at desktop, non-issue at this viewport anyway.
- Contrast (APCA, full soft-clamp formula, not the simplified WCAG-ratio shortcut): body-on-white Lc 102.5, nav/lead ink-2-on-white Lc 88.2, button white-on-accent Lc -87.1 - all clear their thresholds. One value worth flagging as a soft note below.

## / at 375/768/1440px (VISUAL)

PASS - screenshots attached (screenshot-375.png, screenshot-768.png, screenshot-1440.png).

- Clear visual hierarchy: bold black h1 > grey lead paragraph > solid blue CTA > light-grey feature cards. Figure-ground works - the blue button is the only saturated color on the page, so it reads as the one action.
- No broken images, no overlapping elements, no placeholder content.
- Feature grid reflows cleanly 3->2->1 columns across viewports with no orphaned/floating sections.
- Nav row holds at 375px without wrapping or needing a hamburger - 3 short links fit.

## Soft note (not a failure)

.feature p (card description text, color --ink-2 on --surface-2 background) measures APCA Lc ~83 at 16px/400. The color.md table's target for 16px/400 is Lc90; the anti-patterns.md instant-fail floor for the same combination is Lc75. 83 clears the hard floor with margin but sits under the aspirational target - flagging for visibility, not counting it as a failure, since the anti-patterns list is what the skill treats as automatic-FAIL and this doesn't match it. If you want headroom, darkening --ink-2 by ~2-3 OKLCH-L points on --surface-2 specifically would close the gap to Lc90 without touching its use on white.

---

**What now?**
1. Acknowledge
2. Audit different scope (specify which)
3. Write something else (free text)
