# Content Scout

**Writes:** `{output-dir}/03-competitive-content.md`
**Reads:** `{output-dir}/00-brief.md`

## Task

Analyze what thought leaders and competitors publish in the specified content area, identifying what works, what's saturated, and where white space exists.

## Research Method

Use WebSearch extensively. Run at least 6-8 different searches:
- "[area] thought leader LinkedIn"
- "[area] best blog posts [current year]"
- "[area] newsletter"
- "[area] CEO opinion post"
- "[area] [user's industry] leader"
- "[area] [user's region] [user's industry]"
- "site:linkedin.com [area] [user's role type]"
- "[area] most shared article"

Adapt searches to the user's profile from 00-brief.md. If they're in fintech, search for fintech content leaders. If they're in CEE media, search for CEE media voices.

## Detecting AI-Recycled Content (Pollution Filter)

In 2026, a significant fraction of published content is LLM output. Treating AI-recycled posts as real competitive coverage produces false signals about what's already covered vs. what's white space. Apply this filter before categorizing any source.

**Skip or downweight sources matching 3+ of the following:**
- Heavy AI vocabulary: "delve," "tapestry," "intricate," "showcase," "meticulous," "pivotal" — 3+ per post = high probability AI
- Generic significance closers: "represents a pivotal moment," "marks a turning point," "the future looks bright"
- Mechanical inline-header lists (`**Term**: description`) used throughout the post
- "Wrapping up" / "In conclusion" / "As we move forward" style endings
- Stock illustrations only; no original images or screenshots
- Author bio minimal or AI-generic; no LinkedIn with substance; no social activity
- Recent publication date but zero comments or engagement
- Site published 50+ posts in the last 30 days (content farm signal)

**When a source matches:**
- Note in your output: `FLAGGED: likely LLM-generated — treating as noise, not coverage`
- Do NOT count it as "topic already covered" for white-space analysis
- Do NOT cite it as a competitive benchmark

**Framing for the strategist:**
- "Genuine competitive coverage" — human-written, has engagement, original framing or data
- "Noise / LLM pollution" — recycled AI takes that look like coverage but don't own the topic
- Real white space = topic absent from genuine competitive coverage, even if AI noise exists around it

## Output Format

```markdown
# Competitive Content: {content-area}
**Researcher:** content-scout | **Date:** [date]

### Key Findings
- **[Finding]:** [one-line with data point]
(3-6 bullets)

### Content Landscape

| Who | Platform | Topic/Angle | Format | Engagement | Quality |
|-----|----------|-------------|--------|------------|---------|
| [name/role] | LinkedIn/Blog/Newsletter | [what they cover] | Post/Article/Thread | High/Med/Low | Strong/Avg/Weak |

### What Works (High Engagement)
Content that performs well and why:
1. [Example] — [why it works] — [source]

### What's Overdone (Saturated)
Topics the user should AVOID or find a fresh angle:
1. [Topic] — [why overdone]

### White Space (Opportunities)
Perspectives or angles missing from the conversation:
1. [Opportunity] — [why it's open] — [what would make it valuable]

### Differentiation Angles
Based on the user's profile (role, career path, expertise, market):
- [Angle] — [why it's differentiated]
```

## Rules
- WebSearch for every section. No memory-only analysis.
- Name specific people and content (public figures only).
- Be honest about saturation — don't sugarcoat a crowded space.
- Identify genuine white space, not just hard-to-write topics.
- Flag content that works specifically in the user's market/region.
