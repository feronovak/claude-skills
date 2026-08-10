---
name: design-police
description: "Use when reviewing any web UI for quality - after building web pages, web apps, components, or layouts. Triggers: \"review UI\", \"check design\", \"audit page\", \"validate frontend\", \"design police\", \"does this look good\", \"check my site\". Also use proactively after building or modifying any web interface, even if not explicitly asked. Inspects source code AND live pages via Playwright at multiple viewports. Binary pass/fail - any anti-pattern = FAIL. This skill judges the rendered interface. Do NOT use for auditing a repository's documentation, release flow or git hygiene (project-standard), or for making an interface distinctive in the first place (frontend-design) - it measures a page that already exists, and never designs one."
version: "1.0"
authors: Fero Novak <https://feronovak.com>
---

# Design Police

Binary pass/fail audit of web interfaces. Reads source files AND inspects live
pages via Playwright (computed styles, screenshots). Any anti-pattern is a
failure.

## How to Run

### 1. Determine Scope

`$ARGUMENTS` = files, directories, or URLs to review. If empty, review all files
changed in the current branch vs main.

Then decide **which routes** you are auditing, before you audit anything. A
verdict on "the app" derived from one page is a false statement about every
other page — and it is the failure mode that makes this audit untrustworthy on
real projects.

- List the routes in scope (router files, `pages/`/`app/` dirs, nav links, the
  README).
- If there are more than ~6, pick a covering set — one per distinct layout, plus
  every route the change actually touched — and **name the ones you skipped.**
- Record what you audited. The verdict header states coverage explicitly.

### 2. Get the page running

The live audit is the point. Source alone cannot see a badge covering a button,
text clipped mid-word, or a 404'd image — those only exist once rendered. Do not
skip to a code-only verdict because nothing happened to be running.

In order:
1. Already-running dev server? Use it.
2. Otherwise start it — `npm run dev` / `pnpm dev` / the README's command — in
   the background, wait for the port, and stop it when you're done.
3. Static site with a build step: build, then serve the output.

**If the route is behind auth**, get in. This is normal and expected on real
apps, and giving up here is what turns a real audit into a source-only
rubber-stamp:
- a test/seed account in `.env.example`, fixtures, or the E2E setup
- the project's own Playwright `storageState` / auth helper (check `tests/`)
- a dev-only login route or magic-link printed to the dev-server console
- setting the session cookie directly

**If you genuinely cannot reach a route, that route is UNAUDITED, not passing.**
Say so in the verdict, name the route, and say what blocked you. Never let an
unreachable page be silently counted as clean.

### 3. Code Audit

Read each source file. Check against the code-level rules. Every violation is a
FAIL item.

### 4. Live Audit

For each route in scope, at 375px, 768px, and 1440px:

**A. Run the probe.** Pass the entire contents of `scripts/probe.js` as the
`function` argument to Playwright's `browser_evaluate`. It returns one JSON
object with contrast (correct APCA, both polarities, with the floor for each
element), spacing, type scale, touch targets, real rendered line lengths,
clipped text, occluded text, broken images, and placeholder copy.

Use it rather than writing your own extraction. Not for convenience — for
correctness and comparability. Hand-rolled APCA drops the polarity branch or the
soft-clamp and quietly mis-scores every light-on-dark button; a line-length
estimate of `offsetWidth / (fontSize * 0.5)` measures the container rather than
the text and overshoots by 20–40%. Two runs of this audit should produce the
same numbers for the same page, and they only will if the measurement is the
same code every time.

Read the probe's own thresholds before overriding one. In particular `floor` vs
`target` on contrast: **fail on `floor`, note on `target`** (see color.md).

**B. Take screenshots** at each viewport, then run the **craft pass** in
`rules/craft.md`. This is where "passed every rule but still looks bad" gets
caught — the numbers cannot see a missing focal point, an inverted hierarchy, or
a grid with one orphaned card.

### 5. Verdict

```
PASS - 0 failures found
FAIL - N failures found
```

The verdict is binary and it is the product. No warnings, no hedging, no
"consider" — a thing is a failure or it is not reported as one.

Suggestions exist in exactly one place: the POLISH section, which never counts
toward the total and never changes PASS to FAIL. That fence is what keeps the
verdict worth trusting — the developer can act on the failures without first
sorting your opinions out of them.

State coverage on the verdict line: which routes were audited, which were
skipped, which were unreachable.

**Order failures by severity.** A flat list of 27 items where "Lorem ipsum is
live on the page" sits below "margin is 18px not 16px" is unreadable, and the
developer fixes the wrong things first. Three bands:

| band | meaning |
|---|---|
| **BLOCKER** | users are hurt or misled now — text unreadable below floor, controls occluded or clipped, broken images, placeholder copy shipped, destructive action not keyboard-reachable, horizontal scroll, touch targets below 44px on mobile |
| **DEFECT** | real and wrong, not stopping anyone today — off-scale spacing values, missing image dimensions, `transition: all`, uppercase without tracking, line length over 80ch |
| **POLISH** | judgement calls — never affects the verdict, **hard cap 3 lines** |

Craft findings are BLOCKER or POLISH only, never DEFECT — see craft.md. An
uneven last row in a responsive grid is arithmetic, not a defect.

BLOCKER and DEFECT both count toward the FAIL total. POLISH never does.

**POLISH is capped at 3 lines and holds taste only.** Two rules keep it from
turning into a second report:

- *Judgement, not measurements.* "Six elements clear their floor but sit under
  target" is the numbers restated with no decision attached — it reads as
  padding and it is where the section goes to die. If a measurement mattered it
  was a failure; if it did not, it does not need a line.
- *Three lines, ranked.* Uncapped, this section grows until nobody reads it,
  and it is often read on a phone. If you have a fourth thing to say, it was
  not worth saying.

Collapse repeats. One line reading "9 distinct off-scale spacing values: 3, 5,
6, 7, 9, 13, 21, 23, 26px" beats 27 lines naming each element — it is the same
information and it is one fix.

**If Playwright is genuinely unavailable** (no browser in the environment, not
merely "no server was running"): run the code audit only, and put
`LIVE AUDIT NOT RUN` in the verdict header. A source-only pass is not a PASS —
say which checks did not happen.

### 6. Post-Verdict Gate

After the verdict, present BOTH a numbered list (for terminal users) AND a
`jarvis-gate` block (Discord buttons in JARVIS; hidden noise in terminal).

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

**On FAIL:** prioritize fixing. Default option is to fix blockers inline.

```
**What now?**
1. 🔧 Fix blockers now
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
  {"id":"fix_critical","label":"🔧 Fix blockers now","style":"success","response":"fix every BLOCKER from the verdict above; leave DEFECT and POLISH items for later"},
  {"id":"fix_specific","label":"🎯 Fix specific items","ask":"Which specific failures should we fix? (cite line numbers or rule tags)"},
  {"id":"reaudit","label":"🔁 Re-audit","response":"re-run the audit on the same scope and produce a new verdict"},
  {"id":"defer","label":"📝 Note for later","response":"note all failures in docs/design-debt.md (create if missing) and continue without fixing now"},
  {"id":"acknowledge_wontfix","label":"⚠️ Acknowledge (won't fix)","style":"danger","response":"acknowledged — will not fix; continue"}
]}
```
````

Terminal users reply with the number or free text. Discord users tap a button or
type a reply.

## Output Format

```
## VERDICT: FAIL (9 failures)
Coverage: /, /settings, /billing audited. /admin/* skipped (same layout as /settings).
          /invoices/:id UNAUDITED — needs a seeded invoice, no fixture found.

### BLOCKER

FAIL [Proximity] /settings 375px - "Save changes" is 40% covered by the PRO badge; the button reads " changes"
FAIL [Contrast] /settings - .value email + workspace: #9aa1ad on #fff, 14px/400, Lc 50.8 (floor 75) - unreadable
FAIL [Alignment] /settings - email clipped mid-word: 339px of text in a 140px box, no ellipsis
FAIL / - hero image 404s (/img/hero-datacenter.jpg)
FAIL / - Lorem ipsum paragraph and a "TODO: add author bio" line are live on the page
FAIL src/settings.tsx:161 - destructive "Delete account" is a <div onclick>, not keyboard reachable

### DEFECT

FAIL [Repetition] /settings - 9 distinct off-scale spacing values: 3, 5, 6, 7, 9, 13, 21, 23, 26px
FAIL [Repetition] / 1440px - body line length 168ch (max 80); no max-width on the text container
FAIL src/settings.tsx:32 - transition: all (must list properties)

### POLISH (not counted, max 3)

- [Craft] The three feature cards use 24px internal padding but 12px between them, so they read as one block rather than three
- Art director's note: every surface is the same white; one tinted band would give the page a spine
```

Note what is absent from that POLISH block: no list of elements sitting between
floor and target. Those were measured, they were not failures, and restating
them would push the one observation worth reading off the bottom of a phone
screen.

Principle tags: `[Contrast]`, `[Repetition]`, `[Alignment]`, `[Proximity]`,
`[Craft]`. These tell the developer which fundamental principle is violated, not
just which threshold was missed.

## Rules

Load `principles.md` and `anti-patterns.md` every time. Load the others when the
page has the thing they govern — there is no value in reading the dark-mode
rules for a page with no dark mode.

- `rules/principles.md` - **READ FIRST.** CRAP + Gestalt - the WHY behind every rule. Use this to explain failures.
- `rules/anti-patterns.md` - Instant-fail patterns (the blocklist)
- `rules/craft.md` - The visual judgement pass: focal point, hierarchy, grouping, orphans. Catches what thresholds cannot.
- `rules/design-tokens.md` - Spacing scale, type scale, color palette, shadows (THE CORE - enforces Repetition)
- `rules/typography.md` - Font pairing, type scale, line length/height, heading proximity, text color hierarchy, spacing
- `rules/typography-presets.md` - Content-type presets: editorial, marketing, e-commerce, docs, dashboard. Load to judge whether the typography suits the content type — an editorial measure on a dashboard is a real finding. Not a menu to recommend from; POLISH is 3 lines, not a redesign.
- `rules/color.md` - APCA contrast floors vs targets, palette limits, 60-30-10, dark mode
- `rules/layout.md` - Grid, max-width, margins, density, responsive, aspect ratios (enforces Alignment + Proximity)
- `rules/interaction.md` - Forms, touch, animation, hover, navigation
- `rules/accessibility.md` - Semantic HTML, ARIA, keyboard, focus (lower priority)
- `rules/performance.md` - CLS, LCP, lazy loading, virtualization

Priority order: principles > anti-patterns > design-tokens > craft > typography >
color > layout > interaction > performance > accessibility.

When reporting failures, cite which principle is violated alongside the specific
threshold. This helps the developer understand not just what's wrong but why it
matters.

Any match in `rules/anti-patterns.md` = automatic FAIL regardless of context.

## Scripts

- `scripts/probe.js` - the computed-style probe. Pass its whole contents to
  `browser_evaluate`. Returns contrast (APCA, both polarities, floor + target
  per element), spacing scale, type scale, touch targets, real rendered line
  length, clipped text, occluded text, broken images, missing image dimensions,
  and placeholder copy.
