# Design Principles

The foundation. Every other rule file is a specific application of these principles. When a rule seems arbitrary, trace it back here - that's where the "why" lives.

## The Core Insight

Most bad design isn't ugly. It's random. Random spacing, random font sizes, random colors, random alignment. Following a system - any system - prevents this. The rules in this skill exist to detect randomness and enforce system.

## CRAP Principles (Robin Williams, "The Non-Designer's Design Book")

Four principles that cover ~80% of what makes design look professional. Every visual check in this skill maps back to one of these.

### Contrast

If two things are different, make them VERY different. No almost-the-same.

- Heading vs body: size ratio must be at least 1.2x (type scale rule). If it's 1.05x, your eye can't tell them apart - is it a heading or big body text?
- Primary CTA vs secondary: different color, weight, or size. If two buttons look similar, neither has priority.
- Text vs background: APCA Lc thresholds exist because "slightly different" isn't readable.

**How to check:** At arm's length, or squinting at the screenshot - can you tell which elements are different levels of importance? If everything looks the same weight, contrast has failed.

**FAIL if:** Visual hierarchy test fails - no clear primary focal point, headings indistinguishable from body, CTA looks like other buttons.

### Repetition

Repeat visual elements throughout. Same color for the same purpose. Same spacing between the same types of elements. Same font size for the same level of heading.

This is why design tokens exist. Tokens ARE repetition encoded as system.

- Spacing scale: every gap comes from the same set of values
- Type scale: every size follows the same mathematical ratio
- Color palette: every color is pre-defined, not picked per-element
- Shadow scale: every elevation uses the same shadow set

**How to check:** Count unique values. If there are 47 different font sizes, 23 different spacing values, and 15 colors that aren't in any palette - repetition has failed.

**FAIL if:** Design token compliance below 70%. More than 12 distinct colors. Font sizes not on a modular scale.

### Alignment

Every element should have a visual connection to something else on the page. Nothing placed arbitrarily. Invisible lines connect elements.

- Left edges align. Right edges align. Centers align.
- Grid columns create alignment tracks.
- Text containers share the same max-width.
- Elements in a row have consistent vertical alignment.

**How to check:** Draw vertical lines through the left edges of major elements. Do they snap to a grid? Or is every element at a slightly different x-position?

**FAIL if:** Elements that should align don't. Content widths vary randomly. No visible grid structure.

### Proximity

Related items close together. Unrelated items far apart. The space BETWEEN groups must be larger than the space WITHIN groups.

This is the most violated principle. Headers closer to the paragraph below them than the paragraph above. Labels with more space to their input than to the previous field's input. Card contents evenly spaced with no grouping.

- Section spacing (48-128px) > component spacing (16-32px) > element spacing (4-12px)
- A heading's margin-bottom must be smaller than its margin-top (it belongs to the content below, not above)
- Items in a list are closer to each other than to items outside the list

**How to check:** For any element, is it visually closer to the things it's related to? Or is spacing uniform everywhere, making everything feel like one undifferentiated block?

**FAIL if:** Uniform spacing everywhere with no visual grouping. Header equidistant from content above and below. Section breaks not visually clear.

## Gestalt Principles (Perceptual Psychology)

Not opinions - tested human perception. These explain WHY the CRAP rules work.

### Proximity (Gestalt)

The brain groups close objects as related. This is the perceptual science behind the CRAP Proximity principle.

**Implication:** Spacing is information. Changing the gap between elements changes their perceived relationship. Two 8px gaps and one 24px gap creates two groups - even with no borders or backgrounds.

### Similarity

The brain groups same-looking things as related. Same color = same category. Same size = same importance. Same shape = same function.

**Implication:** If two buttons look identical but do different things (one is primary, one is secondary), the user can't tell the difference. Contrast required.

### Continuity

Eyes follow lines and curves. They follow the direction things point.

**Implication:** Alignment works because the eye follows the invisible vertical line created by aligned left edges. Breaking alignment breaks the line, and the eye stumbles.

### Closure

The brain completes incomplete shapes. You don't need a full border - a partial line or shadow implies the boundary.

**Implication:** You don't need heavy borders on cards. A subtle shadow or single-side border is enough. Over-bordering makes the design feel caged and heavy.

### Figure-Ground

Something must be foreground, something must be background. The brain needs to separate layers.

**Implication:** Visual hierarchy. If everything is at the same visual "layer" (same size, color, weight), the brain can't parse what to look at first. The 60-30-10 color rule enforces figure-ground: 60% recedes, 10% jumps forward.

## How These Map to the Rule Files

| Principle | Enforced by |
|-----------|------------|
| Contrast | `design-tokens.md` type scale (size ratio), `color.md` APCA (color contrast), `anti-patterns.md` hierarchy check |
| Repetition | `design-tokens.md` all token rules (spacing, type, color, shadow, radius) |
| Alignment | `layout.md` grid system, max-width, margins |
| Proximity | `layout.md` section/component spacing, `typography.md` vertical rhythm |
| Similarity (Gestalt) | `design-tokens.md` consistent tokens for same-function elements |
| Continuity (Gestalt) | `layout.md` alignment and grid |
| Closure (Gestalt) | `design-tokens.md` shadow scale (elevation not borders) |
| Figure-Ground (Gestalt) | `color.md` 60-30-10 proportion, hierarchy |

## The Randomness Test

Quick gut-check before running detailed rules. Extract from the page:
1. All unique font sizes - are they on a mathematical scale, or random?
2. All unique spacing values - are they multiples of 4 or 8, or random?
3. All unique colors - are they from a limited palette, or random?
4. All alignments - do elements snap to a grid, or random?

If 3+ of these are "random" - the page has no design system. Individual rule violations are symptoms; randomness is the disease.
