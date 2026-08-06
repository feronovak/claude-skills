# Ground truth — planted defects

Every defect below was verified present by direct measurement (Playwright
`evaluate` + screenshot) before any eval was run. Fixtures are served at
`http://127.0.0.1:8811/` from `fixtures/`.

Classification:
- **VISUAL** — invisible to computed-style checks. Only a screenshot or a
  targeted DOM probe catches it. This is the class the skill was reported to miss.
- **COMPUTED** — findable by reading computed styles.
- **CODE** — findable by reading the source file.

---

## eval-1 `article` — editorial page (Astro/Ghost shape)

| id | class | defect | measured |
|----|-------|--------|----------|
| A1 | VISUAL | hero image 404s, renders as broken/empty | `/img/hero-datacenter.jpg` → 404 |
| A2 | VISUAL | Lorem ipsum placeholder paragraph shipped in body | present |
| A3 | VISUAL | `TODO: add author bio + newsletter CTA` visible on page | present |
| A4 | COMPUTED | body text has no `max-width` → line length far past limit | ~154ch (1387px @ 18px) at 1440px |
| A5 | COMPUTED | byline/tag colour too light | `#b4b4b4` on `#fff` = APCA Lc 41 (min 75) |
| A6 | COMPUTED | no type hierarchy — h1/h2/body nearly identical | h1 21px, h2 19px, body 18px |
| A7 | CODE | hero `img` missing `width`/`height` | confirmed |
| A8 | COMPUTED | nav links below touch minimum on mobile | 31px tall (min 44); RSS 29x31 |

Near-miss (must NOT be flagged): `target="_blank"` on the RSS link is legitimate —
it points to `example.com`, an external host. Flagging it is a false positive.

## eval-2 `app` — settings screen (Next.js product shape)

| id | class | defect | measured |
|----|-------|--------|----------|
| B1 | VISUAL | `PRO` badge sits on top of the Save button, hiding the word "Save" | 40x19px overlap; button reads " changes" |
| B2 | VISUAL | email + workspace values clipped mid-word by a fixed 140px box | text 339px in a 140px box |
| B3 | VISUAL | avatar image 404s, and `alt=""` means nothing renders at all | `/avatars/fnovak.png` → 404 |
| B4 | COMPUTED | icon buttons below touch minimum | 28x28 (min 44x44) |
| B5 | COMPUTED | spacing off any 4px scale | 23, 13, 21, 9, 14px |
| B6 | CODE | destructive "Delete this account" is a `div` with `onclick` | not keyboard reachable |
| B7 | CODE | `outline: none` with no `:focus-visible` replacement | 2 occurrences |
| B8 | CODE | `transition: all` | 1 occurrence |
| B9 | CODE | `maximum-scale=1` in viewport meta — blocks pinch zoom | confirmed |
| B10 | CODE | `console.log` shipped | confirmed |
| B11 | CODE | avatar `img` missing `width`/`height` | confirmed |
| B12 | COMPUTED | badge font-size below 14px floor | 11px |
| B13 | COMPUTED | uppercase heading with default letter-spacing | `.card h2` |

## eval-3 `clean` — control, no planted defects

Verified clean at 375px and 1440px: spacing all on 4px scale, type scale
16/20/25/39, zero APCA failures, zero touch-target failures, no line over 80ch,
no overflow, no broken images, no placeholder text, `:focus-visible` defined,
image has `width`/`height`/`alt`, no `transition: all`, no `!important`.

**Correct verdict: PASS.** Every FAIL reported here is a false positive.

---

## What each eval measures

- **Visual recall** (A1–A3, B1–B3): the reported "misses real problems" failure.
- **Live-audit evidence**: did the run actually navigate a browser and screenshot
  at more than one viewport, or did it audit source only and assert a verdict?
- **Computed recall** (A4–A6, A8, B4–B5, B12–B13)
- **Code recall** (A7, B6–B11)
- **False-positive rate**: FAIL count on `clean` (target 0) + the RSS near-miss.
