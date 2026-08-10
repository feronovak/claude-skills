# Skill Dependency Check

**When team-lead runs:** after Phase 0 (project setup), before EXECUTION MODE selection.

The team-lead checks which optional enhancement skills are installed. These skills significantly improve output quality in their domains — the built-in methodology is solid but the specialized skills are deeper.

Where a skill below is installed, **it owns its area** and the built-in methodology defers to it. Two rulebooks for one job is worse than either alone: they drift, and nobody can say which the output was judged against.

## How to Check

Look for these skills in the available skills list. Match on the exact names — a
skill installed under a different name than the one listed is a miss, not a hit.

### Design

| Skill | Used By | Enhancement | Required? |
|-------|---------|-------------|-----------|
| `interface-design:init` | designer | Design system creation with production-grade tokens and patterns | recommended |
| `interface-design:audit` | visual-design-reviewer | Deep visual audit with design system violation detection | recommended |
| `interface-design:critique` | visual-design-reviewer | Design craft critique — catches "looks default" problems | recommended |
| `frontend-design` | designer | Component design with distinctive, non-generic visual identity | recommended |
| `design-police` | visual-design-reviewer | Binary pass/fail gate — measures the live page at multiple viewports rather than reading the source | recommended |

`frontend-design` and `design-police` are not alternatives. The first is generative and fires while the designer works; the second is a gate and fires after the engineer ships. Install both where possible, and run them in that order.

### Engineering method

| Skill | Used By | Enhancement | Required? |
|-------|---------|-------------|-----------|
| `superpowers:test-driven-development` | engineer | Tests written before implementation, not after | recommended |
| `superpowers:systematic-debugging` | engineer | Root-cause discipline when the build breaks, instead of patching symptoms | recommended |
| `superpowers:verification-before-completion` | engineer, qa-reviewer | Evidence before any "done" claim — the failure mode Phase 3 exists to catch | recommended |
| `superpowers:requesting-code-review` | qa-reviewer | Structured pre-merge review with explicit acceptance criteria | recommended |
| `webapp-testing` | qa-reviewer | Browser-driven testing of the running app, beyond unit and integration layers | recommended |

Where the `superpowers:*` skills are present, `references/engineer.md` and `references/qa-reviewer.md` keep their **deliverables** and hand over their **method**. The reference files say what must exist; superpowers says how it gets built and how it gets verified.

### Project and review

| Skill | Used By | Enhancement | Required? |
|-------|---------|-------------|-----------|
| `project-standard` | engineer, deployment-readiness-reviewer | Owns repo documentation, release flow and git hygiene — README, ADRs, runbook, `.env.example`, one-backlog rule — and ships a checker that verifies them | recommended |
| `seo-aeo-best-practices` | seo-reviewer | Technical SEO + AEO — metadata, Open Graph, sitemaps, JSON-LD, AI answer surfaces | recommended |
| `/security-review` | code-quality-reviewer | Security review of the branch's pending changes, beyond checklist review | **required for FULL & SERIOUS BET** |
| `security-guidance` | code-quality-reviewer | Hook-driven security prompts during the build, not only at review time | recommended |

`/security-review` is a built-in Claude Code command, not a plugin skill — it needs no installation and the requirement above is satisfied by default. Check it is callable rather than looking for it in the skills list.

Where `project-standard` is installed, it is the standard for repo hygiene and the deployment-readiness-reviewer verifies against its checker rather than against a list in this skill. See `references/devops.md` § 5.

## Present to User

Report what was found, grouped, with recommendations for missing critical skills:

```
Skill check:
  design       ✅ interface-design   ❌ frontend-design   ✅ design-police
  engineering  ✅ superpowers        ❌ webapp-testing
  project      ✅ project-standard   ❌ seo-aeo-best-practices
  security     ✅ /security-review   ❌ security-guidance
```

## Critical Skill Recommendations

If any of these three is missing, strongly recommend installation. Each covers capability the built-in methodology cannot fully replicate.

### `superpowers` (HIGH impact — engineering method)

This changes how the engineer and qa-reviewer work, not what they deliver. Without it, the engineer follows the reference file's checklist and writes tests after the code; a "done" claim rests on the engineer's own assessment. With it, tests come first, a broken build gets a root-cause pass instead of a patch, and no completion claim is made without a command and its output behind it. The difference is a build that has been verified vs one that has been asserted — which is the exact failure Phase 3's reviewers spend their budget catching.

Install: `/plugin marketplace add anthropics/claude-plugins-official` then `/plugin install superpowers@claude-plugins-official`

### `interface-design` (HIGH impact — design system + visual review)

This skill transforms how the designer creates your design system. Without it, the designer follows a solid checklist — picks colors, sets typography, defines spacing. With it, the designer explores your product's domain, rejects generic defaults explicitly, builds a token architecture where every visual value traces to intent, and runs 4 craft tests (Swap, Squint, Signature, Token) before delivering. The visual reviewer also uses it to catch design system violations and "looks default" problems that a checklist audit will miss. The difference is a design system that looks *intentional* vs one that looks *professional but templated*.

Install: `/plugin marketplace add Dammyjay93/interface-design` then `/plugin install interface-design@interface-design`

### `frontend-design` (HIGH impact — component distinctiveness)

This skill pushes components from "well-structured" to "memorable." Without it, the designer specs components with correct anatomy, variants, and states — functional and clean. With it, the designer commits to a bold aesthetic direction, uses distinctive typography instead of safe defaults, applies spatial composition (asymmetry, negative space, density variation), and designs motion that reinforces the product's personality. The difference is components that could belong to any app vs components someone would screenshot and share.

Install: `/plugin marketplace add anthropics/claude-plugins-official` then `/plugin install frontend-design@claude-plugins-official`

## Recommendation Format

Present like this:

```
⚠️  Three skills are missing that significantly affect output quality:

1. superpowers — the build gets verified instead of asserted
   /plugin marketplace add anthropics/claude-plugins-official
   /plugin install superpowers@claude-plugins-official

2. interface-design — makes design systems intentional, not templated
   /plugin marketplace add Dammyjay93/interface-design
   /plugin install interface-design@interface-design

3. frontend-design — makes components distinctive, not generic
   /plugin marketplace add anthropics/claude-plugins-official
   /plugin install frontend-design@claude-plugins-official

Without them, the build will use solid built-in methodology (covers
design principles, anti-patterns, craft tests, a test checklist) but the
output won't match what these specialized skills produce.

Options:
  a) Install now (recommended — takes ~30 seconds each)
  b) Proceed without — built-in methodology will be used
  c) Skip all external skills — built-in only
```

The user may:
- **Install recommended skills** → wait, then re-check
- **Proceed as-is** → use whatever is available, built-in for the rest
- **Skip all external skills** → use only built-in methodology

Store the result as `{enhanced_skills}` — pass this to teammates so they know which path to take. A teammate whose area is owned by an installed skill must be told which one, so it defers rather than running both.
