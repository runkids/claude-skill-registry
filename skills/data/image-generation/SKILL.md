---
name: image-generation
description: Generate detailed AI image prompts for website assets using Imagen 3 (Nano Bana Pro). Use when creating infographics, diagrams, icons, maps, comparison visuals, or any generated imagery for websites. Triggers on "generate image", "create visual", "image prompt", "infographic", "diagram", "icon set".
allowed-tools: Read, Write, Edit, Glob, Grep
---

# AI Image Generation Skill

Generate production-ready prompts for Google Imagen 3 (Nano Bana Pro) optimized for website assets.

## When to Use

- Creating infographics (timelines, processes, comparisons)
- Technical diagrams (medical, architectural, educational)
- Icon sets (differentiators, features, services)
- Maps (locations, travel times, geographic)
- Data visualizations (charts, statistics, comparisons)
- Comparison visuals (vs pages, before/after concepts)
- Educational illustrations (how things work)

## When NOT to Use

- Real photography (products, people, locations)
- Client-provided assets
- Screenshots or UI mockups
- Logos (should be vector/designed)

## Prompt Structure

Every prompt must include:

```
**Filename:** `descriptive-name.png`
**Used on:** [page names]
**Dimensions:** [width x height]px

**Prompt:**
[Detailed generation prompt]
```

## Prompt Formula

```
[Subject/Content] + [Style] + [Layout] + [Colors] + [Typography] + [Quality] + [Avoid]
```

### 1. Subject/Content
Be extremely specific about what the image shows:
- Exact elements to include
- Relationships between elements
- Text/labels to display
- Data to visualize

### 2. Style
Define the aesthetic:
- "Premium medical illustration"
- "Luxury brand infographic"
- "Editorial map design"
- "Clean icon set"
- "Technical diagram"

### 3. Layout
Describe composition:
- "Horizontal timeline left to right"
- "Two-column comparison"
- "Circular arrangement"
- "Grid of 4 equal icons"
- "Map with concentric rings"

### 4. Colors
Always specify exact colors:
```
Primary: #HEXCODE
Accent: #HEXCODE
Background: white/cream/gradient
Text: charcoal/navy
```

### 5. Typography
Specify text treatment:
- "Clean sans-serif labels"
- "Elegant serif headers"
- "Minimal, only essential text"

### 6. Quality
Define output requirements:
- "Ultra-high resolution"
- "Sharp lines, no artifacts"
- "Print and web ready"
- "Medical publication quality"

### 7. Avoid
Explicitly state what NOT to include:
- "No cartoon style"
- "No clip art"
- "No stock photo aesthetic"
- "No busy backgrounds"
- "No text overlapping elements"

## Client Brand Integration

Before generating prompts, check for client brand file:
- `clients/[client]/brand-colors.md`
- `clients/[client]/image-prompts.md` (existing prompts)

If no brand file exists, ask for:
1. Primary brand color (hex)
2. Accent color (hex)
3. Style preference (clinical, luxury, modern, corporate)
4. Industry context

## Image Categories & Templates

### 1. Process/Timeline Infographic

```
**Prompt:**
Premium horizontal infographic showing [X]-step [process name].

Style: [Luxury/Corporate/Medical] aesthetic. Clean [white/colored] background.

Layout: [X] equally spaced [circular/square] containers connected by [line/arrows].

Step 1 - "[Label]"
- Icon: [Specific icon description]
- Color: [Primary] on white

[Repeat for each step]

Connecting element: [Thin gold line / Dotted arrow / Gradient bar] connecting all steps.

Typography: [Step titles in charcoal, numbers in accent color].

Quality: Editorial infographic, suitable for premium publication.

Avoid: Corporate clip-art, busy backgrounds, inconsistent icon weights.
```

### 2. Comparison Visual

```
**Prompt:**
Side-by-side comparison infographic for [Option A] vs [Option B].

Style: Premium comparison layout, balanced presentation. Clean white background.

Layout: Two columns with center dividing element.

Left Column - "[Option A]"
- [Key point 1 with icon]
- [Key point 2 with icon]
- [Key highlight/badge]

Right Column - "[Option B]"
- [Key point 1 with icon]
- [Key point 2 with icon]
- [Key highlight/badge]

Center element: Elegant vertical divider with "vs" in [accent color] circle.

Bottom: "[Balanced insight statement]"

Color palette: [Primary] for Option A accents, neutral gray for Option B, [accent] for shared elements.

Quality: Premium comparison chart, luxury buyer's guide aesthetic.
```

### 3. Geographic Map

```
**Prompt:**
Elegant map of [Region] showing [location/business name] with [travel times/coverage/connections].

Style: Premium cartographic design, editorial travel magazine aesthetic. Not Google Maps style.

Map coverage: [Countries/regions visible]. Water in soft blue-gray, land in muted [green/beige].

Key elements:
1. [Main location] marked with prominent [accent color] pin/marker
2. [Concentric rings / Connection lines] showing [travel zones / service areas]

Indicators:
- [City 1]: [icon], "[time/distance]"
- [City 2]: [icon], "[time/distance]"
[Repeat as needed]

Color palette: Muted sage for land, soft blue-gray for water, [accent] for markers, [primary] for text.

Typography: Elegant [serif/sans-serif] for location names.

Quality: Luxury travel publication quality. Sophisticated, not cluttered.
```

### 4. Technical/Medical Diagram

```
**Prompt:**
[Technical/Medical] illustration showing [concept/process/anatomy].

Style: Premium [medical/technical] illustration, educational but elegant. Clean white background.

Main illustration:
- [Primary element with detailed description]
- [Secondary elements]
- [Relationships/connections between elements]

Callout labels in clean sans-serif:
- "[Label 1]"
- "[Label 2]"
[Repeat as needed]

[Optional] Inset/detail view: [Description of zoomed or alternate view]

Color palette: [Appropriate colors for subject], [accent] for labels, [primary] for key elements.

Quality: Medical textbook meets luxury editorial. Detailed but accessible.

Avoid: Grotesque/scary imagery, overly clinical sterility, inconsistent detail levels.
```

### 5. Icon Set

```
**Prompt:**
Set of [X] premium icons representing [theme/category].

Style: Luxury brand iconography, consistent weight and style. [Line art / Subtle filled / Duotone].

Icon 1 - "[Concept]"
- Visual: [Specific icon description]
- Feel: [Emotion/association]

[Repeat for each icon]

Consistency requirements:
- All icons same [line weight / fill style]
- Equal visual weight
- Same level of detail
- Cohesive family appearance

Color: All icons in [primary color] with optional [accent] elements. Consistent [X]px stroke if line art.

Quality: Luxury hotel or premium financial services icon quality. Timeless, not trendy.

Avoid: Inconsistent weights, overly detailed vs simple mix, trendy effects.
```

### 6. Data Visualization

```
**Prompt:**
[Chart type] visualizing [data/comparison/statistics].

Style: Premium data visualization, [publication/brand] aesthetic.

Data to show:
- [Data point 1]: [value]
- [Data point 2]: [value]
[Repeat as needed]

Visual treatment:
- [Bar heights / Pie segments / Line trajectory] accurately representing data
- [Legend / Labels] positioned [location]
- [Highlight treatment] for key data point

Color palette: [Colors for each data series], [accent] for highlights.

Typography: Clean, minimal. Data labels in [size] [font style].

Quality: Financial Times / Economist chart quality. Clear hierarchy, no chartjunk.

Avoid: 3D effects, gradient fills, excessive grid lines, decorative elements.
```

## Dimension Guidelines

| Image Type | Recommended Size | Aspect Ratio |
|------------|------------------|--------------|
| Hero/Banner | 1600 x 600px | 8:3 |
| Infographic (horizontal) | 1400 x 500px | ~3:1 |
| Infographic (vertical) | 600 x 1200px | 1:2 |
| Comparison visual | 1400 x 700px | 2:1 |
| Map | 1200 x 900px | 4:3 |
| Icon set (row) | 1200 x 300px | 4:1 |
| Individual icon | 200 x 200px | 1:1 |
| Technical diagram | 1200 x 800px | 3:2 |
| Square social | 1080 x 1080px | 1:1 |

## Output Format

When generating prompts, output as:

```markdown
## [Image Name]

**Filename:** `kebab-case-name.png`
**Used on:** [page1], [page2]
**Dimensions:** [W] x [H]px
**Priority:** [Tier 1/2/3]

**Prompt:**
```
[Full detailed prompt]
```

**Notes:** [Any implementation notes]
```

## Quality Checklist

Before finalizing any prompt:

- [ ] Specific dimensions included
- [ ] Brand colors specified with hex codes
- [ ] Style clearly defined (not generic)
- [ ] Layout/composition described
- [ ] All text/labels specified exactly
- [ ] Typography treatment noted
- [ ] Quality standard referenced
- [ ] "Avoid" section included
- [ ] Suitable for both web and print

## Example: Complete Prompt

```markdown
## Recovery Timeline Infographic

**Filename:** `recovery-timeline-12-months.png`
**Used on:** hair-transplant
**Dimensions:** 1600 x 600px
**Priority:** Tier 1

**Prompt:**
Elegant horizontal timeline infographic showing hair transplant recovery from Day 1 to Month 12.

Style: Premium luxury medical aesthetic. Clean white background with subtle texture. Timeline as elegant horizontal line with gold (#c9a86c) accent.

Layout: 5 stages arranged left to right, evenly spaced along timeline.

Stage 1 - "Day 1-7"
- Small scalp illustration showing mild redness
- Label below: "Initial Healing"

Stage 2 - "Weeks 2-4"
- Scalp showing shedding phase
- Label: "Shock Shedding (Normal)"

Stage 3 - "Months 2-3"
- Clean scalp, minimal visible change
- Label: "Dormant Phase"

Stage 4 - "Months 4-6"
- New wispy growth emerging
- Label: "New Growth Begins"

Stage 5 - "Months 9-12"
- Full density, natural appearance
- Label: "Final Results"

Visual: Each stage as top-down head silhouette in charcoal gray. Hair in deep navy (#1a2744). Progressive density increase from stage 4.

Connecting element: Thin gold (#c9a86c) line connecting stages with subtle directional flow.

Typography: Clean sans-serif. Stage labels in charcoal. Time periods in gold.

Badge: Small "99% Graft Survival" in gold near final stage.

Quality: Editorial infographic suitable for premium medical publication.

Avoid: Cartoon style, clinical sterility, inconsistent illustration styles, busy backgrounds.

**Notes:** This image is referenced by multiple pages. Ensure it works as standalone and in context.
```

## Integration with Pages

When adding image placeholders to markdown pages, use format:

```markdown
**Image:** `[filename.png]` `Alt: [Descriptive alt text for accessibility]`
```

## Reference

- See `clients/[client]/image-prompts.md` for client-specific prompts
- See `clients/fuegenix/image-prompts.md` for complete example library
