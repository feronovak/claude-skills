# Skill Dependency Check

**When team-lead runs:** after Phase 0 (project setup), before EXECUTION MODE selection.

The team-lead checks which optional enhancement skills are installed. These skills significantly improve output quality in their domains — the built-in methodology is solid but the specialized skills are deeper.

## How to Check

Look for these skills in the available skills list:

| Skill | Used By | Enhancement | Required? |
|-------|---------|-------------|-----------|
| `interface-design:init` | designer | Design system creation with production-grade tokens and patterns | recommended |
| `interface-design:audit` | visual-design-reviewer | Deep visual audit with design system violation detection | recommended |
| `interface-design:critique` | visual-design-reviewer | Design craft critique — catches "looks default" problems | recommended |
| `frontend-design` | designer | Component design with distinctive, non-generic visual identity | recommended |
| `seo-technical-optimization` | seo-reviewer | Technical SEO analysis (meta, structured data, Core Web Vitals) | recommended |
| `security-scanning:security-sast` | code-quality-reviewer | Static analysis security scanning beyond checklist review | **required for FULL & SERIOUS BET** |

## Present to User

Report what was found, with recommendations for missing critical skills:

```
Skill check:
  ✅ interface-design — installed (designer + visual reviewer will use it)
  ❌ frontend-design — not installed
  ✅ security-scanning — installed (code reviewer will use it)
  ❌ seo-technical-optimization — not installed
```

## Critical Skill Recommendations

If either of these two skills is missing, strongly recommend installation. They cover design capabilities that the built-in methodology cannot fully replicate.

### `interface-design` (HIGH impact — design system + visual review)

This skill transforms how the designer creates your design system. Without it, the designer follows a solid checklist — picks colors, sets typography, defines spacing. With it, the designer explores your product's domain, rejects generic defaults explicitly, builds a token architecture where every visual value traces to intent, and runs 4 craft tests (Swap, Squint, Signature, Token) before delivering. The visual reviewer also uses it to catch design system violations and "looks default" problems that a checklist audit will miss. The difference is a design system that looks *intentional* vs one that looks *professional but templated*.

Install: `claude install-skill anthropic/interface-design`

### `frontend-design` (HIGH impact — component distinctiveness)

This skill pushes components from "well-structured" to "memorable." Without it, the designer specs components with correct anatomy, variants, and states — functional and clean. With it, the designer commits to a bold aesthetic direction, uses distinctive typography instead of safe defaults, applies spatial composition (asymmetry, negative space, density variation), and designs motion that reinforces the product's personality. The difference is components that could belong to any app vs components someone would screenshot and share.

Install: `claude install-skill anthropic/frontend-design`

## Recommendation Format

Present like this:

```
⚠️  Two skills are missing that significantly affect design quality:

1. interface-design — makes design systems intentional, not templated
   Install: claude install-skill anthropic/interface-design

2. frontend-design — makes components distinctive, not generic
   Install: claude install-skill anthropic/frontend-design

Without them, the build will use solid built-in methodology (covers
design principles, anti-patterns, craft tests) but the output won't
match what these specialized skills produce.

Options:
  a) Install now (recommended — takes ~30 seconds each)
  b) Proceed without — built-in methodology will be used
  c) Skip all external skills — built-in only
```

The user may:
- **Install recommended skills** → wait, then re-check
- **Proceed as-is** → use whatever is available, built-in for the rest
- **Skip all external skills** → use only built-in methodology

Store the result as `{enhanced_skills}` — pass this to teammates so they know which path to take.
