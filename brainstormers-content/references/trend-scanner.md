# Trend Scanner

**Writes:** `{output-dir}/01-trending-topics.md`
**Reads:** `{output-dir}/00-brief.md`

## Task

Find 8-12 hot/trending topics in the specified content area, evaluated for relevance to the user's profile.

## Research Method

Use WebSearch extensively. Run at least 6-8 different searches:
- "[area] trends [current year]"
- "[area] news this week"
- "[area] news this month"
- "[area] LinkedIn viral post"
- "[area] debate controversy"
- "[area] data report [current year]"
- "[area] [user's industry/region]" (from profile in 00-brief.md)
- "[area] conference keynote [current year]"

Do not rely on a single query. Cast a wide net.

## Output Format

```markdown
# Trending Topics: {content-area}
**Researcher:** trend-scanner | **Date:** [date]

### Heat Map

| # | Topic | Heat | Recency | User Relevance | Source |
|---|-------|------|---------|----------------|--------|
| 1 | [topic] | HOT/WARM/EMERGING | [days old] | HIGH/MED/LOW | [source] |

### Topic Details
For each topic (3-5 lines max):
#### [N]. [Topic Title]
- **What's happening:** [1-2 sentences with specific facts/data]
- **Why it's hot:** [what's driving conversation]
- **User angle:** [connection to their role/experience, or "NO CLEAR CONNECTION"]
- **Source:** [URL or publication]

### Gaps Spotted
[Topics expected but NOT found trending]
```

## Heat Classification Thresholds

Don't guess heat — use evidence:

| Heat | Criteria | Typical Age |
|------|----------|-------------|
| **HOT** | Multiple major outlets covering it; active LinkedIn/X debate; new data just released; industry reaction happening now | 0-14 days |
| **WARM** | Growing discussion; 1-2 major sources; audience starting to ask about it; conference buzz | 14-45 days |
| **EMERGING** | Early signals; niche sources only; no mainstream coverage yet; could go hot in 2-4 weeks | 14-60 days |
| **STALE** | Peak conversation passed; most takes already published; audience fatigue visible | 60+ days |

**User Relevance scoring:**
- **HIGH**: Direct connection to their role/expertise — they've done this, decided this, managed this
- **MED**: Adjacent experience — they've seen this at their company or industry but haven't led it
- **LOW**: Awareness only — they know about it but can't speak from experience

Mark LOW honestly. A topic the user can't speak about authentically is useless even if HOT — the content-strategist will filter it out via the Authenticity gate.

## Rules
- WebSearch for EVERY topic. No memory-only topics.
- Prioritize last 7-30 days. Flag anything older than 60 days as STALE.
- Rate User Relevance honestly based on the profile in 00-brief.md: LOW if they have no direct experience.
- Include at least 2 topics specific to the user's industry/region if they exist.
- Cite sources for every topic.
