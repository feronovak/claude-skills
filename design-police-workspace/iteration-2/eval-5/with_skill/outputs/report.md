# Design Police — Orbit Console

## VERDICT: FAIL (18 failures)

Coverage: all three routes in the app audited at 375px, 768px, 1440px —
`/login` (public), `/dashboard` (auth), `/team` (auth). This is the full
route list per `README.md`; nothing skipped. Signed in via the documented
dev magic-link flow (`POST /login` → link printed to dev-server console →
`GET` the link) to reach the two protected routes, per `tests/README.md`.
Source read for all three page templates plus `server.js`.

---

### BLOCKER

FAIL [Proximity] /dashboard (all viewports) - the "3 NEW" pill sits on top of the "Deploy to production" button and covers 40% of its label; the button reads " to production" — `public/dashboard.html:78-81`, `.pill` positioned `top:12px; left:20px` over `.deploy`

FAIL [Semantic HTML] /team - the "Remove" action on all three rows is a `<span onclick>`, not a `<button>`; a destructive, irreversible action is unreachable by keyboard and has no confirmation step — `public/team.html:69,76,83`

FAIL [Contrast] /dashboard - all 4 metric labels ("Uptime, 30 days", "Median deploy", "Failed this week", "Open incidents"): `#b9bfca` on white, 14px/400, Lc 34.8 (floor 75) — unreadable — `public/dashboard.html:31` `.metric .label`

FAIL [Contrast] /dashboard - "3 NEW" pill text: white on `#ff5a1f`, 12px/700, Lc -62.4 (floor 70); the same element is also below the 14px type-size floor for any UI text — `public/dashboard.html:44-48` `.pill`

FAIL [Contrast] /team - the note line ("TODO: replace initials…"): `#b9bfca` on `#f6f7fa`, 13px/400, Lc 30 (floor 75) — unreadable — `public/team.html:42` `.note`

FAIL [Contrast] /team - Role column text ("Owner", "Maintainer", "Developer" and access levels): `#6b7280` on white, 13px/400, Lc 73.6 (floor 75) — just under the floor — `public/team.html:36` `.role`

FAIL / (visual) /dashboard - broken image: `/charts/uptime-30d.png` 404s — `public/dashboard.html:76`

FAIL / (visual) /team - placeholder copy shipped to production: "TODO: replace initials with real avatars once the uploader ships" — `public/team.html:88`

FAIL [Alignment] /team (all viewports) - all three email addresses are clipped mid-domain with no ellipsis and no `title` attribute: `frantisek.novak@ringier-slovakia.sk` (285px of text in a 180px box), `michal.hrncar@ringier-slovakia.sk` (271px), `zuzana.kovacova@ringier-slovakia.sk` (298px) — the reader can't tell there's more, and can't recover the value by hovering — `public/team.html:32-35` `td.email span`

FAIL / (layout) /team 375px - horizontal scrollbar; the table doesn't reflow at mobile width and content exceeds the viewport

FAIL / (touch) /team 375px - the three "Remove" links are 53×27px, below the 44×44px minimum for a destructive control — `public/team.html:38-41` `.remove`

FAIL / (touch) /dashboard 375px - the environment-switch button is 32×32px, below the 44×44px minimum — `public/dashboard.html:50-53` `.env-switch`

### DEFECT

FAIL [Repetition] /team - 8 distinct off-scale spacing values: 3, 11, 13, 15, 19, 21, 27, 29px, none of them multiples of 4 — spacing compliance on this page is 16%, versus 93-100% on `/login` and `/dashboard`. The page ignores the 4px scale the other two routes establish. `public/team.html:21,22,23,27,39,42`

FAIL [Typography] /team - font size 13px used throughout the table (`th`, `.role`, `.remove`, `.note`) — below the 14px floor for UI text

FAIL [Typography] /team - table headers are uppercase with default (0) letter-spacing; needs 0.05-0.12em tracking — `public/team.html:28` `th`

FAIL src/dashboard.html:29 - `.metric { transition: all 0.2s ease; }` — must list properties explicitly, not `all`

FAIL src/team.html:93 - `console.log("removing member", id)` shipped in the production `removeMember` handler

FAIL [Repetition] /dashboard, /team - two ungoverned greys doing the same "muted/secondary text" job (`#b9bfca` and `#6b7280`), neither of which is `/login`'s `--ink-2` (`#3e4552`). Neither route reuses `/login`'s `:root` token set (`--s2`…`--s7`, `--ink-2`) at all — each re-declares its own smaller, inconsistent palette.

### POLISH (not counted)

- `/team` `.hint` (Lc 68.8/floor 68), `th` (Lc 73.6/floor 70), `.remove` (Lc 77.6/floor 75) all clear their floor but sit under target — tightening these would remove the "barely passing" feel of the whole page.
- `/dashboard` `.env-switch` padding (1px/6px) is off-scale but only 2 distinct values — below the 4-value threshold, not worth a DEFECT on its own.
- Art director's note: `/dashboard` and `/team` both end in a large expanse of unstyled background below a short content block — no footer, no secondary content, no visual anchor. Next to `/login`'s tightly composed card, the two signed-in screens read unfinished rather than restrained.
- `/login` is clean end to end — proper design tokens, on-scale spacing and type, real focus-visible states, correct floor/target contrast, no anti-patterns at any viewport. It's the reference the other two pages should be brought up to, not rebuilt from scratch.

---

**What now?**
1. 🔧 Fix blockers now
2. 🎯 Fix specific items (cite line numbers or rule tags)
3. 🔁 Re-audit the same scope
4. 📝 Note for later (write to docs/design-debt.md)
5. ⚠️ Acknowledge — won't fix, continue
6. ✏️ Write something else (free text)

```jarvis-gate
{"options":[
  {"id":"fix_critical","label":"🔧 Fix blockers now","style":"success","response":"fix every BLOCKER from the verdict above; leave DEFECT and POLISH items for later"},
  {"id":"fix_specific","label":"🎯 Fix specific items","ask":"Which specific failures should we fix? (cite line numbers or rule tags)"},
  {"id":"reaudit","label":"🔁 Re-audit","response":"re-run the audit on the same scope and produce a new verdict"},
  {"id":"defer","label":"📝 Note for later","response":"note all failures in docs/design-debt.md (create if missing) and continue without fixing now"},
  {"id":"acknowledge_wontfix","label":"⚠️ Acknowledge (won't fix)","style":"danger","response":"acknowledged — will not fix; continue"}
]}
```
