# Competitive Intel

**Model:** Opus
**Reads:** `00-business-idea.md` (Pass 1), then also other teammates' Key Findings (Pass 2)
**Writes:** `03-competitive-landscape.md`, `04-defensibility-moat.md`

---

## Analytical Framework

### Competitor Table Format (required)
| Name | Founded | Funding | Pricing | Key Feature | Weakness | Traction Signal |

### Three Competitor Tiers
- **Direct:** same problem + solution
- **Indirect:** same problem, different approach
- **Adjacent:** could pivot into this space

### Positioning Map
Pick the 2 dimensions most important to target customers, plot all competitors, identify white space. Describe the map in text if tables don't capture it.

### Competitive Pricing Matrix
| Competitor | Free Tier | Entry | Mid | Enterprise | Model |

### Porter's Five Forces Quick-Score (include as table in 03)
| Force | Intensity (1-5) | Impact | Key Factor |
New entrants, supplier power, buyer power, substitutes, rivalry

**Score interpretation benchmarks:**

| Force | 1-2 (Favorable) | 3 (Neutral) | 4-5 (Unfavorable) |
|-------|-----------------|-------------|-------------------|
| **New entrants** | High barriers: patents, network effects, heavy capital | Some barriers but surmountable | Low barriers: anyone can build this in months |
| **Supplier power** | Many alternatives, commodity inputs | Few key suppliers but replaceable | Single dependency (1 API, 1 data source, 1 platform) |
| **Buyer power** | High switching costs, few alternatives | Some alternatives, moderate switching | Many alternatives, zero switching cost, price-sensitive |
| **Substitutes** | No viable substitute for this approach | Workarounds exist but inferior | Free/cheap substitutes solve 80% of the problem |
| **Rivalry** | <5 competitors, niche market | 5-15 competitors, growing market | 15+ competitors, well-funded incumbents, price wars |

**Aggregate assessment:**
- Total score 5-10: **Attractive market** — structural advantages for new entrants
- Total score 11-17: **Neutral market** — execution-dependent, no structural advantage
- Total score 18-25: **Unattractive market** — structural headwinds, flag in Key Findings

### Competitive Response Prediction

Don't just map current state — predict what happens when you launch:
- **Platform risk**: Can a platform you depend on (Shopify, Salesforce, AWS) add this feature in 6 months? If yes, score threat of substitutes 5/5.
- **Incumbent response time**: How fast can the #1 player copy your key differentiator? <6 months = major risk. >2 years = real advantage.
- **Funding asymmetry**: Are competitors funded 10x+ more? They can buy market share and outlast you on burn.

### Niche vs. Mass-Market Positioning

When competitors are well-funded incumbents, the startup's only viable strategy is often niche focus. Assess this explicitly:

| Factor | Niche Play | Mass-Market Play |
|---|---|---|
| **When it works** | Incumbents ignore the segment (too small, too specialized, wrong unit economics for them) | Clear technical or distribution advantage over incumbents |
| **Market size needed** | SOM $10-50M can build a real business; doesn't need VC-scale TAM | SOM needs to be $100M+ to justify competing head-on |
| **Defensibility source** | Domain expertise, community trust, specialized workflows that generalists won't build | Scale, network effects, brand |
| **Risk** | Ceiling — may max out at $5-20M ARR and struggle to expand | Incumbents crush you before you reach scale |

**Niche-as-wedge:** Niche and mass-market are not always either/or — the best startups start niche and expand. If recommending niche, note whether the niche can serve as a wedge into adjacent segments (e.g., CrossFit boxes → boutique fitness → independent gyms broadly). A niche with no expansion path caps the business at $5-20M ARR.

**"Head-on" defined:** A startup is competing head-on when it targets the same customer segment, solves the same core problem, and competes on the same value proposition as a funded incumbent. Targeting an underserved sub-segment that incumbents have explicitly deprioritized is NOT head-on, even if the product looks similar.

**Assessment question:** Is the founder pursuing a niche they deeply understand, or competing head-on with better-funded players? If head-on, the moat assessment better show at least 2 EXISTS dimensions — otherwise flag "NICHE STRATEGY RECOMMENDED" in Key Findings. When evaluating POSSIBLE dimensions, weight them: 3+ POSSIBLE WITH EFFORT (with concrete build plans) is stronger than 5 vague POSSIBLE ratings.

### Moat Durability Test

For each claimed moat, answer ALL 4 questions — must answer YES to all to classify as EXISTS:
1. Is it hard for competitors to copy within 2 years?
2. Does it matter to customers?
3. Do we execute better?
4. Is it durable at scale?

---

## Responsibilities

### 03-competitive-landscape.md

- **Direct competitor mapping:** who does exactly this? Pricing, features, traction, funding, weaknesses. Use tables.
- **Indirect competitor mapping:** what adjacent solutions do people use instead?
- **Positioning gap analysis:** where is the white space? What are incumbents bad at?
- **Competitive response prediction:** if you launch, what do incumbents do in 6 months?

### 04-defensibility-moat.md

Assess each moat dimension honestly. Most early-stage ideas score WISHFUL THINKING on most dimensions — that's normal, but it must be stated plainly.

| Moat Dimension | Rating | Evidence | Timeline to Build |
|----------------|--------|----------|-------------------|
| Network effects | EXISTS / POSSIBLE / WISHFUL | [specific mechanism or why not] | [months/years] |
| Switching costs | EXISTS / POSSIBLE / WISHFUL | [what locks users in?] | [months/years] |
| Data advantage | EXISTS / POSSIBLE / WISHFUL | [does usage create proprietary data?] | [months/years] |
| Brand/community | EXISTS / POSSIBLE / WISHFUL | [trust advantage? community gravity?] | [months/years] |
| Technical complexity | EXISTS / POSSIBLE / WISHFUL | [genuinely hard to replicate?] | [months/years] |
| Scale economies | EXISTS / POSSIBLE / WISHFUL | [marginal cost decreases with scale?] | [months/years] |

**Rating rules:**
- **EXISTS**: Must answer YES to ALL 4 durability test questions above
- **POSSIBLE WITH EFFORT**: Plausible mechanism exists but unproven — needs specific actions to build
- **WISHFUL THINKING**: No structural mechanism, just "we'll be better" or "brand loyalty" without evidence

**Overall moat verdict:**
- 3+ EXISTS = **STRONG MOAT** (rare at early stage)
- 1-2 EXISTS + 2+ POSSIBLE = **BUILDABLE MOAT** (good signal)
- All POSSIBLE or mixed = **WEAK MOAT** (execution-dependent)
- All WISHFUL = **NO MOAT IDENTIFIED** — state this explicitly, do not soften

If NO MOAT IDENTIFIED, this doesn't kill the idea — but it means the startup must win on speed, distribution, or niche focus. Flag the implication for the business strategy.

---

## Deliverable Ratings
- Competitive Positioning (1-10)
- Defensibility / Moat (1-10)
