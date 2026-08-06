# Design Police Audit — Ledger landing page

Target: http://127.0.0.1:8811/clean/
Source: /home/fnovak/.claude/skills/design-police-workspace/fixtures/clean/index.html

## VERDICT: PASS - 0 failures found
Coverage: single route audited (the source is one static `index.html` with no
router and no other pages — this landing page is the entire site). Audited via
source read + live Playwright inspection at 375px, 768px, and 1440px. Computed-
style probe (`scripts/probe.js`) run at all three; full-page screenshots taken
at all three for the craft pass.

## Code audit

Checked against `anti-patterns.md`, `design-tokens.md`, `typography.md`,
`color.md`, `layout.md`:

- **Spacing** — every margin/padding/gap comes from the declared 4px-base
  scale (`--s1`…`--s8`: 4/8/12/16/24/32/48/64px). Probe confirms 100%
  compliance at all three viewports, 0 off-scale values.
- **Type scale** — 16 / 20 / 25 / 39px, all on the declared `16 x 1.25^n`
  scale. H1 (39px) is 2.4x body — well clear of the 1.2x contrast minimum.
- **Color** — 6-value palette (`--ink`, `--ink-2`, `--accent`, `--surface`,
  `--surface-2`, `--rule`) plus white button text and a computed hover shade;
  used consistently for the same roles everywhere. Well under the 12-color cap.
- **Contrast** — 0 APCA failures below floor at any viewport, for any
  text/background pair (nav links, body copy, CTA white-on-blue, footer
  copyright).
- No `transition: all` — properties are listed explicitly (`color 0.15s ease`,
  `background-color 0.15s ease`).
- No `outline: none` without a `:focus-visible` replacement — a custom focus
  ring is defined and applied.
- `<img>` has both `alt` and explicit `width`/`height`.
- No `<div>`/`<span>` with click handlers — every interactive element is a
  real `<a>`.
- No `!important`, no inline style overrides, no `target="_blank"` on internal
  links, no all-caps text, no `console.log`.
- Viewport meta doesn't disable pinch-zoom.
- Line-length constraints (`max-width: 18ch` on h1, `58ch`/`60ch` on body
  copy) keep every text block well under the 80ch cap.

No anti-pattern matches. No DEFECT-tier findings either — no off-scale
spacing, no missing image dimensions, no `transition: all`.

## Live audit — all three viewports (375 / 768 / 1440px)

Probe returned zero on every measurable check, at every viewport:

- 0 contrast failures (below floor)
- 0 off-scale spacing values
- 0 touch-target failures (nav links and CTA all clear 44px at mobile width)
- 0 clipped text, 0 occluded text
- 0 broken images, 0 missing image dimensions
- 0 placeholder copy ("lorem ipsum" / "TODO" pattern)
- 0 horizontal scroll at any width
- 0 line-length failures

I also opened all three screenshots directly to check the one thing the probe
can't see: whether the hero image (`shot.png`) actually matches its alt text
("The Ledger dashboard showing a month of categorised transactions"). It
does — a populated transaction table with real vendor names (Figma, CSOB
poplatok, Alza.sk, Booking.com, Anthropic, Slovnaft, Martinus), colour-coded
category chips, and formatted amounts. Nothing broken or misleading there.

## Craft pass (from the screenshots, craft.md questions 1-8)

1. **Focal point** — squinting at each screenshot, the headline and the blue
   "Start a free month" button are what survive. Matches the page's actual
   goal. Pass.
2. **Hierarchy vs. importance** — h1 > lead > CTA > product screenshot > "Three
   things it does properly" > feature cards > nav > footer. Visual weight
   tracks actual importance at every step. Pass.
3. **Grouping** — hero content sits at 16-32px internal gaps against a much
   larger 48-64px gap to the next section; the three feature cards read as a
   distinct group, separated from the hero by a rule + large padding. Pass.
4. **Alignment** — the logo, h1, lead, CTA, screenshot, "Three things it does
   properly," and the card grid all share one `.wrap` left edge at every
   viewport. Pass.
5. **Density** — nothing touches a container edge; nothing floats unrelated
   to its neighbours. Pass.
6. **Orphans** — at 768px the feature grid drops to 2-then-1 columns; the lone
   third card sits at the same width as its column (not stretched, no hole in
   the layout) — ordinary responsive arithmetic, not a defect per the skill's
   own guidance. The headline wraps cleanly with no stranded single word at
   any width. Pass.
7. **Consistency** — the three feature cards share identical treatment; nav
   links share identical treatment; the CTA — the one thing that should look
   different — does. Pass.
8. **Designed vs. defaulted** — one consistent 8px border-radius throughout,
   one shadow token used only on the hero image, no default-blue links, no
   unstyled form controls, a custom focus ring. Reads as deliberate, not
   defaulted. Pass.

No craft blockers.

### POLISH (not counted, does not affect verdict)

- The accent blue (`#1a44d6`) does double duty as both the CTA fill and the
  nav/footer link color. It doesn't cause confusion (button vs. link shape
  disambiguates them), but a hover underline on nav links would give the
  accent a second, more specific "job" instead of one flat use everywhere.
- Art director's note: this page is genuinely close to finished — restrained,
  on-system, nothing fighting for attention, and the hero screenshot is doing
  real work (it's the only place actual product data appears). If I had to
  push it one step further, I'd give the three feature cards slightly more
  differentiation — right now they're three identical grey blocks in a row,
  which is correct but a little flat. A subtle top-border accent on one card,
  or an icon per card, would give the eye a second stop after the hero.

## Files in this audit
- `report.md` — this report
- `probe-results.json` — raw `scripts/probe.js` output for 375 / 768 / 1440px
- `clean-375.png`, `clean-768.png`, `clean-1440.png` — full-page screenshots
  used for the craft pass

## What now?
1. Acknowledge
2. Audit different scope (specify which)
3. Write something else (free text)

```jarvis-gate
{"options":[
  {"id":"acknowledge","label":"Acknowledge","style":"success","response":"acknowledged"},
  {"id":"different_scope","label":"Audit different scope","ask":"Which files, directories, or URLs should we audit next?"}
]}
```
