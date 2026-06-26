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
- **Will they rationally respond at all?** Speed-to-copy is not the only question. If matching your model would damage the incumbent's *existing* business (cannibalize high-margin revenue, create channel conflict), they may rationally choose NOT to respond even though they technically could — that is Counter-Positioning. Feed this into 04's Counter-Positioning Test; do not score it here as "easily copied → no moat."
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

### Defensibility Framework: Helmer's 7 Powers

Assess durable defensibility with Hamilton Helmer's **7 Powers** — the canonical strategy framework for *why differential returns persist*. This is firm-level advantage and complements Porter's Five Forces above (Porter = is the industry attractive; 7 Powers = does THIS company hold a defensible position within it). Use both.

**The two-part test every Power must pass — no exceptions:**
1. **Benefit** — does it improve cash flow via *higher prices*, *lower costs*, or *lower capital intensity*?
2. **Barrier** — is there a concrete reason existing AND potential competitors *cannot or will not* arbitrage that benefit away?

**A benefit with no barrier is a feature, not a Power.** Most "moats" founders pitch (a slick UI, being cheaper, "our tech is hard") are benefits anyone can copy — score them WISHFUL.

**The 7 Powers** (Barrier = why competitors can't arbitrage it | when a startup can establish it):

| Power | What it is | Barrier | Establishable |
|---|---|---|---|
| **Scale Economies** | Unit cost falls as volume rises | A challenger must win equal share to reach equal cost — gain share at a loss | Takeoff |
| **Network Economies** | Product value rises as the installed base grows | A smaller rival delivers less value and must vastly outspend to close the gap | Takeoff |
| **Counter-Positioning** | Newcomer adopts a superior business model the incumbent will NOT copy because copying damages the incumbent's existing business | The incumbent's *own rational choice* not to respond (collateral damage to their core) | **Origination → Takeoff** |
| **Switching Costs** | Customer loses value by moving to an alternative | A rival must compensate the customer for the switching loss to win them | Takeoff |
| **Branding** | Durable attribution of higher value to an identical offering, from accumulated trust/history | Years of consistent history + uncertainty reduction that money can't shortcut | Stability (slow) |
| **Cornered Resource** | Preferential access to a coveted asset (exclusive license/patent, locked-in unique talent, exclusive data/supply) | The resource is fixed and exclusive — competitors simply can't obtain it | Any stage, if genuinely secured |
| **Process Power** | Embedded organizational processes yielding lower cost / better product | Hysteresis — replicable only through a long, sustained, hard-to-observe org effort (e.g. Toyota) | Stability (slow) |

**Counter-Positioning is the startup-vs-incumbent Power** and the one most often missed. When a startup undercuts or out-models an incumbent, do NOT reflexively rule "they can just copy it → no moat." Run the Counter-Positioning Test (below) — sometimes the correct, defensible answer is *"the incumbent rationally will not respond."*

**Stage gate (prospective discipline):** Most Powers can only be *established* at takeoff or stability — not at origination. For a pre-launch / early idea, only **Counter-Positioning** and **Cornered Resource** are available *now*; Scale, Network, Switching, Branding, and Process are *earnable later* and rate POSSIBLE-at-best today. Crediting a pre-launch idea with an EXISTS network-effects or brand Power is almost always WISHFUL — flag it.

### Counter-Positioning Test (run whenever a startup undercuts/out-models an incumbent)

The framework's most important and most-missed judgment. Do NOT default to "copyable = no moat." Answer in order:

1. **Superior model?** Is the newcomer's model genuinely better (lower cost / better fit) for the target segment — not just a price cut funded by burning cash?
2. **Collateral damage?** If the incumbent copied it, what would they lose in their *existing* business — cannibalized high-margin revenue, channel conflict, margin compression on their core?
3. **Damage > new-segment value?** If the collateral damage to the incumbent exceeds what the new segment is worth to them, they will *rationally choose not to respond* → **Counter-Positioning EXISTS against that incumbent.** This is a Power, not a "reversible pricing choice."
4. **Partial response available?** Can the incumbent *partially* respond (ring-fence a tier, cap a fee, spin a sub-brand) to limit damage while still competing? A clean partial response weakens the barrier → POSSIBLE, not EXISTS.
5. **Scope it — Powers are competitor-specific.** Counter-positioning protects against the INCUMBENT (who has a business to protect). It gives ZERO protection against a same-model *startup twin* with no legacy business to cannibalize. If the real threat is a funded startup copy, say so plainly.

State each Power's verdict *relative to a named competitor type* (incumbents / startup twins / platform owners). Blurring all competitors together is the classic defensibility error.

---

## Responsibilities

### 03-competitive-landscape.md

- **Direct competitor mapping:** who does exactly this? Pricing, features, traction, funding, weaknesses. Use tables.
- **Indirect competitor mapping:** what adjacent solutions do people use instead?
- **Positioning gap analysis:** where is the white space? What are incumbents bad at?
- **Competitive response prediction:** if you launch, what do incumbents do in 6 months?

### 04-defensibility-moat.md

Assess defensibility using the 7 Powers framework above. **Most early-stage ideas have ZERO-to-ONE Power — that is the expected, healthy finding, not a failure.** Name the one real (or credibly buildable) Power, or state NO POWER IDENTIFIED plainly. Do NOT manufacture Powers to fill rows.

Produce the assessment as a table. List Powers that are EXISTS, POSSIBLE WITH EFFORT, or a WISHFUL claim the founder is actively making; you need not list all 7 if most are trivially absent — close with "Remaining Powers: none applicable" instead of padding:

| Power | Rating | Benefit (cash-flow lever) | Barrier (why competitors can't/won't arbitrage) | Defends against | When establishable |
|---|---|---|---|---|---|
| [Power] | EXISTS / POSSIBLE WITH EFFORT / WISHFUL | [higher price / lower cost / lower capital] | [the specific barrier, or "none — copyable"] | [incumbents / startup twins / all] | [now / takeoff / stability] |

If a startup-undercuts-incumbent dynamic exists, include the **Counter-Positioning Test** (5 questions above) as a short numbered block — this is where the real defensibility judgment lives for most challenger startups.

**Rating rules:**
- **EXISTS** — passes BOTH the Benefit and Barrier test *today* (or on a credible, founder-articulated near-term path). For Counter-Positioning, the incumbent's collateral damage must plausibly exceed the new-segment value.
- **POSSIBLE WITH EFFORT** — credible mechanism + concrete build path, but not yet established (e.g. scale economies that need ~10K users; brand that needs years). Stage-gated Powers on an early idea cap here.
- **WISHFUL THINKING** — a benefit with no barrier, or a Power the company's stage cannot yet support.

**Overall Power verdict:**
- **2+ Powers EXISTS** = **STRONG** (rare at early stage)
- **1 EXISTS, or 1-2 credible POSSIBLE with a concrete path** = **EMERGENT / BUILDABLE POWER** (good early signal)
- **All POSSIBLE-but-vague or mixed** = **WEAK** — execution- and speed-dependent
- **All WISHFUL / none** = **NO POWER IDENTIFIED** — state this explicitly, do not soften

If NO POWER IDENTIFIED, this doesn't kill the idea — but the startup must win on speed, distribution, or niche focus, and brand/process/scale become things to *build*, not things it has. **Weight to the strategy lens:** a venture-track idea needs a credible path to at least one Power; a bootstrap/niche idea can be a healthy business with NO Power at all (a defended niche substitutes for a structural moat). Flag the implication for whichever lens applies (see 11).

---

## Deliverable Ratings
- Competitive Positioning (1-10)
- Defensibility / Moat (1-10)
