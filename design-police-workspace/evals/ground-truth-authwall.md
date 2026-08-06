# Ground truth — `authwall` fixture (eval-5)

Project: `fixtures/authwall` — "orbit-console". Dev server on `127.0.0.1:8877`,
**not running** when the eval starts. Every defect below was verified by direct
measurement through an authenticated Playwright session before the eval ran.

## What this fixture tests

Two things the earlier fixtures could not:

1. **The auth wall.** `/dashboard` and `/team` 302 to `/login` without a session
   cookie. There is no password — sign-in is a magic link, and in development
   the link is printed **only to the dev server's stdout**. Getting in requires:
   start the server → `POST /login` → read the link out of the server console →
   open it → carry the `sid` cookie. Documented in `README.md` and
   `tests/README.md`; the seeded address is in `.env.example`.
2. **Route coverage.** The two protected routes carry *different* defects. An
   audit that reaches only `/dashboard` misses the entire `T` set and vice
   versa. `/login` is deliberately clean, so a run that never gets past it sees
   a tidy page — and must not report that as a passing app.

## Correct outcomes

| outcome | verdict |
|---|---|
| Signed in, audited `/dashboard` + `/team` | FAIL, both defect sets found |
| Could not sign in | Must report `/dashboard` + `/team` as **UNAUDITED**, never PASS |
| Audited `/login` only and issued an app-level verdict | **wrong** — the failure this fixture exists to catch |

## `/login` — public, clean

No planted defects. On-scale spacing, type scale 16/25, `:focus-visible`
defined, labelled input, real `<button>`, explicit transition properties.

## `/dashboard` — auth required

| id | class | defect | measured |
|----|-------|--------|----------|
| D1 | VISUAL | "3 NEW" pill covers the primary button's own label — it reads "3 NEW to production" | occlusion 40%, `button.deploy` covered by `span.pill` |
| D2 | VISUAL | deployment chart 404s | `/charts/uptime-30d.png` → 404 |
| D3 | COMPUTED | metric labels nearly invisible | `.metric .label` `#b9bfca` on `#fff`, 14px/400, Lc 34.8 (floor 75), ×4 |
| D4 | COMPUTED | pill text below the size floor and under contrast floor | 12px, Lc −62.4 (floor 70) |
| D5 | COMPUTED | env-switch below touch minimum | `.env-switch` 32×32 (min 44×44) |
| D6 | CODE | `transition: all 0.2s ease` on `.metric` | confirmed |
| D7 | CODE | chart `img` missing `width`/`height` | confirmed |

Spacing on this page is deliberately near-clean (2 distinct off-scale values,
under the >4 threshold) — flagging spacing here would be a false positive.

## `/team` — auth required

| id | class | defect | measured |
|----|-------|--------|----------|
| T1 | VISUAL | `TODO: replace initials with real avatars…` live on the page | confirmed |
| T2 | VISUAL | all three emails clipped mid-word, no ellipsis, no `title` | 285/271/298px of text in a 180px box |
| T3 | COMPUTED | horizontal scroll at 375px — the table overflows the viewport | `scrollWidth > innerWidth` |
| T4 | COMPUTED | 8 distinct off-scale spacing values | 3, 11, 13, 15, 19, 21, 27, 29px |
| T5 | COMPUTED | text below the 14px floor | `th`, `td.role`, `.remove`, `.note` all 13px |
| T6 | COMPUTED | `.note` unreadable; `td.role` under floor | `.note` Lc 30 (floor 75); `td.role` Lc 73.6 (floor 75) |
| T7 | COMPUTED | uppercase headers with no letter-spacing | 4 × `th` |
| T8 | CODE | destructive "Remove" is a `<span onclick>` — not keyboard reachable | 3 occurrences |
| T9 | CODE | `console.log("removing member", id)` shipped | confirmed |

## Probe bug found while building this

`uppercaseNoTracking` never fired: unset `letter-spacing` computes to the
keyword `normal`, and `parseFloat('normal')` is `NaN`, which fails every
comparison silently. Fixed — T7 is detected now. Worth remembering that any
CSS length can arrive as a keyword.
