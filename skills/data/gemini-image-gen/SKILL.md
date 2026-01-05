---
name: gemini-image-gen
description: Generate and edit images using Google's Gemini API (gemini-3-pro-image-preview model). Use when users request (1) Generating images from text prompts, (2) Editing existing images with AI instructions, (3) Creating images with specific styles or templates, (4) Generating multiple variations of images, (5) Creating images with reference images for style consistency, (6) Any image generation task mentioning Gemini, Google AI, or requiring professional image output. Supports aspect ratios (1:1, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9), 7 style templates (3 glass styles, 4 other creative styles), reference images (up to 14), and batch processing.
---

# Gemini Image Generation Skill

Generate and edit professional images using Google's Gemini API with support for style templates, reference images, and batch processing.

## Overview

This skill enables image generation and editing through Google's `gemini-3-pro-image-preview` model. It provides:

- **Text-to-Image generation** - Create images from text descriptions
- **Image editing** - Modify existing images with text instructions
- **Style templates** - Apply consistent styling using markdown templates with `{subject}` placeholders
- **Reference images** - Use up to 14 reference images for style/composition guidance
- **Batch processing** - Generate multiple variations in a single command
- **Aspect ratio control** - Choose from 8 aspect ratios for different use cases

Use this skill when users request image creation, editing, or generation tasks involving Google's Gemini AI.

## Prerequisites & Setup

### API Key Acquisition

1. Visit https://aistudio.google.com/apikey
2. Sign in with your Google account
3. Create a new API key
4. Copy the key immediately

**Note:** Paid tier is recommended to avoid rate limits in production.

### API Key Configuration

**Option 1: Environment Variable (Recommended)**

```bash
# Linux/macOS - add to ~/.bashrc or ~/.zshrc
export GOOGLE_AI_API_KEY="your_key_here"

# Windows PowerShell - add to $PROFILE
$env:GOOGLE_AI_API_KEY="your_key_here"
```

**Option 2: .env File (Project-specific)**

Create a `.env` file in the user's working directory:

```
GOOGLE_AI_API_KEY=your_key_here
```

The script automatically loads `.env` files using python-dotenv.

### Installing uv (Package Manager)

This skill requires `uv` for dependency management:

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or on macOS
brew install uv
```

### Installing Dependencies

**Dependencies install automatically on first run!**

When you first use the skill, it will detect missing dependencies and run `uv sync` automatically. You'll see:

```
Installing required dependencies... (one-time setup)
Dependencies installed successfully!
Please run the command again.
```

**Manual installation (optional):**

```bash
cd <skill-dir>/scripts
uv sync
```

This installs:
- `google-genai>=1.0.0` (Gemini API client)
- `python-dotenv>=1.0.0` (environment variable loading)
- `pillow>=10.0.0` (image processing)

**Note:** Python 3.10 or higher is required.

## Core Workflow

### Path Resolution

Always use absolute paths to the skill directory when invoking the script:

```bash
# You will resolve <skill-dir> to the actual installation path
uv run python <skill-dir>/scripts/main.py <args>
```

Output files are saved relative to the **user's current working directory**.

### Basic Command Structure

```bash
uv run python <skill-dir>/scripts/main.py <output> <prompts...> [OPTIONS]
```

**Arguments:**
- `<output>` - Output file path (e.g., `images/output.png`, `images/icon.png`)
- `<prompts...>` - One or more subject prompts

**Default Output Location:** Images are saved to `images/` folder in the project root

**Options:**
- `--style <path>` or `-s` - Path to style template `.md` file
- `--edit <path>` or `-e` - Edit existing image instead of generating
- `--ref <path>` or `-r` - Reference image (repeatable, up to 14 total)
- `--aspect <ratio>` or `-a` - Aspect ratio (default: 1:1)

### Decision Tree: Generate vs Edit

**Generate new image:**
- User wants to create something from scratch
- Use prompts to describe the desired image
- Optionally use `--style` and `--ref`

**Edit existing image:**
- User has an image to modify
- Use `--edit <image-path>`
- Provide prompt describing the changes
- Optionally use `--ref` for style guidance

## Command Reference

### Basic Generation

```bash
uv run python <skill-dir>/scripts/main.py images/sunset.png \
  "A vibrant sunset over mountain peaks with orange and purple sky" \
  --aspect 16:9
```

**Output:** Creates `images/sunset.png` in project root

### Using Bundled Style Templates

```bash
# Purple glass 3D style
uv run python <skill-dir>/scripts/main.py images/rocket.png "rocket" \
  --style <skill-dir>/assets/styles/purple_glass_3d.md

# Neon wireframe style
uv run python <skill-dir>/scripts/main.py images/gear.png "gear" \
  --style <skill-dir>/assets/styles/neon_wireframe.md

# Gold metallic 3D style
uv run python <skill-dir>/scripts/main.py images/cube.png "cube" \
  --style <skill-dir>/assets/styles/gold_metallic_3d.md
```

**What happens:**
- Template loads with full prompt template
- `{subject}` placeholder replaced with your subject
- Full prompt used for generation

**Output:** Styled image matching the template aesthetic in `images/` folder

### Batch Processing (Multiple Subjects)

```bash
uv run python <skill-dir>/scripts/main.py images/icon.png \
  "cube" "sphere" "pyramid" "cylinder" \
  --style <skill-dir>/assets/styles/emerald_glass_3d.md
```

**Output:** Creates `images/icon_1.png`, `images/icon_2.png`, `images/icon_3.png`, `images/icon_4.png` in emerald glass style

### Image Editing

```bash
uv run python <skill-dir>/scripts/main.py logo_edited.png \
  "Change the background to solid blue (#0066CC)" \
  --edit logo.png
```

**Requirements:**
- `logo.png` must exist in current directory (or provide full path)
- Edit prompt describes the desired change

**Output:** Creates `logo_edited.png` with modified background

### Using Reference Images

```bash
uv run python <skill-dir>/scripts/main.py gear.png \
  "A gear icon matching the style of the reference" \
  --ref example.png
```

**Use case:** Match style/aesthetics of an existing image

**With bundled examples:**
```bash
uv run python <skill-dir>/scripts/main.py icon.png "CPU chip" \
  --ref <skill-dir>/assets/styles/purple_glass_3d/examples/1.png
```

### Aspect Ratio Selection

**Note:** The default aspect ratio is **1:1** (square). Specify `--aspect` to use a different ratio.

```bash
# YouTube thumbnail
uv run python <skill-dir>/scripts/main.py thumbnail.png \
  "AI coding tutorial thumbnail with vibrant colors" \
  --aspect 16:9

# Instagram post
uv run python <skill-dir>/scripts/main.py insta_post.png \
  "Product photo on clean white background" \
  --aspect 1:1

# Vertical video
uv run python <skill-dir>/scripts/main.py story.png \
  "Mobile-first vertical design" \
  --aspect 9:16
```

### Maximum Consistency (Template + References)

```bash
uv run python <skill-dir>/scripts/main.py icon.png "database" \
  --style <skill-dir>/assets/styles/amber_glass_3d.md \
  --ref <skill-dir>/assets/styles/amber_glass_3d/examples/1.png \
  --ref <skill-dir>/assets/styles/amber_glass_3d/examples/2.png
```

**Result:** Highest possible consistency with established style

## Style Templates

### Using Bundled Templates

This skill includes **14 professional style templates**:

**Glass Styles (3D frosted glass with rim lighting):**
1. **purple_glass_3d.md** - Royal purple (#7C3AED) glass with violet rim lighting
2. **emerald_glass_3d.md** - Deep emerald (#059669) glass with lime green rim lighting
3. **amber_glass_3d.md** - Rich amber (#D97706) glass with golden rim lighting

**Other Styles:**
4. **neon_wireframe.md** - Hot pink/cyan glowing wireframe outlines on black
5. **gold_metallic_3d.md** - Brushed gold metal (#D4AF37) with warm highlights
6. **minimalist_flat.md** - Soft pastel flat 2D design on white background
7. **gradient_holographic.md** - Iridescent purple-pink-cyan gradients on white

Usage:
```bash
--style <skill-dir>/assets/styles/purple_glass_3d.md
--style <skill-dir>/assets/styles/neon_wireframe.md
--style <skill-dir>/assets/styles/gold_metallic_3d.md
```

### Creating Custom Templates

Create a `.md` file with this structure:

```markdown
# My Style Name

## Prompt Template

```
Your detailed prompt here with {subject} placeholder.
All styling, colors, materials described explicitly.
Background treatment, lighting, composition specified.
```
```

**Key requirements:**
- Include `{subject}` placeholder where the variable content goes
- Be explicit about colors (use hex codes)
- Describe materials, lighting, and composition
- List prohibitions (NO gradients, NO text, etc.)

**Example custom template:**
```markdown
## Prompt Template

```
Premium photograph of {subject}. Professional studio lighting with soft shadows. Clean white background (#FFFFFF). High-resolution DSLR quality. NO text, NO graphics, NO distractions.
```
```

### Template Path Resolution

**Bundled templates:**
```bash
--style <skill-dir>/assets/styles/purple_glass_3d.md
--style <skill-dir>/assets/styles/neon_wireframe.md
--style <skill-dir>/assets/styles/gold_metallic_3d.md
```

**User's custom template:**
```bash
--style ./my-styles/custom-style.md
--style /absolute/path/to/template.md
```

### How Templates Work

The script:
1. Reads the template file
2. Finds the code block after `## Prompt Template`
3. Replaces `{subject}` with your provided subject
4. Uses the complete prompt for generation

**Example:**
- Template: `"Premium 3D {subject} made of glass"`
- Your subject: `"cube"`
- Final prompt: `"Premium 3D cube made of glass"`

## Reference Images

### When to Use References

**Style consistency:**
- Match aesthetics of existing images
- Maintain brand visual identity
- Replicate specific rendering technique

**Composition guidance:**
- Specific layout or arrangement
- Particular perspective or angle
- Element positioning requirements

**Content specification:**
- Exact shapes or icons to include
- Specific objects to emulate
- Visual elements to incorporate

### Important: WHAT vs HOW

**Reference images define WHAT:**
- Specific shapes, icons, symbols
- Objects and elements to include
- Compositional layout and arrangement

**Text prompts define HOW:**
- Visual style and aesthetics
- Material properties (glass, metal, etc.)
- Colors, lighting, rendering technique
- Background treatment

### Reference Image Limits

- **Maximum:** 14 reference images per request
- **Edit mode:** 13 references + 1 main image = 14 total
- **More isn't always better:** Start with 1-2, add more only if consistency requires it

### Using Bundled Examples

Each style template includes 3 example images for reference consistency:

```bash
# Purple glass examples
--ref <skill-dir>/assets/styles/purple_glass_3d/examples/1.png
--ref <skill-dir>/assets/styles/purple_glass_3d/examples/2.png
--ref <skill-dir>/assets/styles/purple_glass_3d/examples/3.png

# Neon wireframe examples
--ref <skill-dir>/assets/styles/neon_wireframe/examples/1.png

# Gold metallic examples
--ref <skill-dir>/assets/styles/gold_metallic_3d/examples/1.png
```

Use these to maintain consistency with your chosen style.

### Multiple References

```bash
uv run python <skill-dir>/scripts/main.py output.png "rocket" \
  --ref example1.png \
  --ref example2.png \
  --ref example3.png \
  --style <skill-dir>/assets/styles/gradient_holographic.md
```

**Priority:** Earlier references have stronger influence on the output.

## Error Handling

### Missing API Key

**Error message:**
```
Error: GOOGLE_AI_API_KEY not found in environment
Create a .env file with: GOOGLE_AI_API_KEY=your_key_here
Get your API key from: https://aistudio.google.com/apikey
```

**Your response:**
1. Provide step-by-step API key setup instructions
2. Offer to create `.env` file in user's working directory
3. Link to API key acquisition URL
4. Remind about paid tier recommendation

### Invalid Aspect Ratio

**Error message:**
```
error: argument --aspect/-a: invalid choice: '5:3'
```

**Your response:**
1. Show the valid aspect ratios: 1:1, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
2. Suggest the closest match to what user requested
3. Explain use cases for the recommended ratio

### File Not Found

**Error message:**
```
Error: Input image not found: logo.png
```

**Your response:**
1. Verify the filename with the user
2. Check if file is in current directory
3. Suggest using absolute path if needed
4. Offer to list image files in current directory

### Too Many Reference Images

**Script behavior:** Uses first 14 references, ignores rest

**Your response:**
1. Inform user of the 14-image limit
2. Ask which references to prioritize if more than 14 provided
3. Explain that earlier references have stronger influence

### Module Import Errors

**Error message:**
```
ModuleNotFoundError: No module named 'google.genai'
```

**Your response:**
1. This shouldn't happen (auto-install should catch it)
2. If it does, the script will show: "Installing required dependencies..."
3. User should run the command again after auto-install completes
4. If auto-install fails, guide user to run manually: `cd <skill-dir>/scripts && uv sync`

### API Quota Exceeded

**Error message:**
```
google.api_core.exceptions.ResourceExhausted: 429 Quota exceeded
```

**Your response:**
1. Explain free tier limits have been reached
2. Suggest upgrading to paid tier: https://aistudio.google.com/
3. Offer to retry after a brief delay
4. Recommend checking usage dashboard

### Python Version Error

**Error message:**
```
requires-python = >=3.10
```

**Your response:**
1. Inform user Python 3.10+ is required
2. Check current version: `python --version`
3. Provide upgrade instructions for their platform

## Output Management

### Output Path Handling

**Default output location:**
```bash
images/output.png      → ./images/output.png
images/icon.png        → ./images/icon.png
```

**Absolute paths:**
```bash
/home/user/projects/output.png → Exact location specified
```

**Directory creation:** The script automatically creates the `images/` directory and any parent directories if they don't exist.

### Batch Processing Outputs

**Single subject → Single file:**
```bash
# Input
uv run python <skill-dir>/scripts/main.py images/output.png "cube"

# Output
images/output.png
```

**Multiple subjects → Numbered files:**
```bash
# Input
uv run python <skill-dir>/scripts/main.py images/icon.png "cube" "sphere" "pyramid"

# Output
images/icon_1.png (cube)
images/icon_2.png (sphere)
images/icon_3.png (pyramid)
```

### Informing the User

Always tell the user:
1. Where the image(s) were saved
2. The filename(s) created
3. For batch processing, which file corresponds to which subject

**Example response:**
```
I've generated 3 emerald glass icons:
- images/icon_1.png (cube)
- images/icon_2.png (sphere)
- images/icon_3.png (pyramid)

All files are in the images/ folder.
```

## Advanced Usage

### Iterative Refinement with Style Consistency

Use successful outputs as references for subsequent generations:

```bash
# First generation
uv run python <skill-dir>/scripts/main.py icon_v1.png "gear" \
  --style <skill-dir>/assets/styles/purple_glass_3d.md

# If result is good, use it as reference for related icons
uv run python <skill-dir>/scripts/main.py icon_v2.png "cog" \
  --style <skill-dir>/assets/styles/purple_glass_3d.md \
  --ref icon_v1.png
```

### Combining Templates and Multiple References

```bash
uv run python <skill-dir>/scripts/main.py output.png "circuit board" \
  --style <skill-dir>/assets/styles/neon_wireframe.md \
  --ref <skill-dir>/assets/styles/neon_wireframe/examples/1.png \
  --ref <skill-dir>/assets/styles/neon_wireframe/examples/2.png \
  --ref <skill-dir>/assets/styles/neon_wireframe/examples/3.png
```

**Use case:** Maximum consistency for brand-critical assets

### Gradient Degradation Warning

**Important:** Avoid gradients if you plan to iterate on outputs.

Gradients compound compression artifacts through multiple generations. For iterative workflows:
1. Use **solid backgrounds** for elements you'll refine
2. Generate gradients/atmospherics **last** (single-pass only)
3. Or generate background separately and composite externally

**See:** `references/best_practices.md` for detailed explanation and examples

### Additional Resources

For detailed information, consult the reference files:

**API Capabilities** (`references/api_capabilities.md`):
- Complete aspect ratio guide with use cases
- Reference image limits and best practices
- API authentication and rate limits
- Error codes and troubleshooting
- Response structure details

**Best Practices** (`references/best_practices.md`):
- Style consistency techniques
- Prompt engineering principles
- Gradient degradation lesson (with showcase examples)
- Background generation strategies
- Reference image techniques (WHAT vs HOW)
- Batch processing patterns
- Template design guidelines

## Aspect Ratio Quick Reference

| Ratio | Use Case | Example |
|-------|----------|---------|
| 1:1 | Social media, icons, profiles | Instagram grid, app icons |
| 3:4 | Portrait photos, prints | Traditional portrait |
| 4:3 | Landscape photos, presentations | Older monitors, prints |
| 4:5 | Instagram portrait posts | Taller feed presence |
| 5:4 | Instagram landscape posts | Landscape feed |
| 9:16 | Vertical video, stories | TikTok, IG Stories |
| 16:9 | YouTube, presentations, monitors | Thumbnails, slides |
| 21:9 | Ultra-wide, cinematic | YouTube banners, headers |

**Default aspect ratio:** 1:1 (square)

**Decision making:**
- **YouTube thumbnail?** → 16:9
- **Instagram post?** → 1:1 or 4:5
- **Profile picture?** → 1:1
- **Vertical video?** → 9:16
- **Presentation?** → 16:9
- **Square icon?** → 1:1
- **Cinematic/banner?** → 21:9

## Usage Examples Summary

### Most Common Patterns

```bash
# 1. Basic generation with style
uv run python <skill-dir>/scripts/main.py images/icon.png "database" \
  --style <skill-dir>/assets/styles/purple_glass_3d.md

# 2. Batch generation with different style
uv run python <skill-dir>/scripts/main.py images/icon.png \
  "cube" "sphere" "pyramid" \
  --style <skill-dir>/assets/styles/gold_metallic_3d.md

# 3. Edit existing image
uv run python <skill-dir>/scripts/main.py images/edited.png \
  "Change background to white" \
  --edit images/original.png

# 4. With reference for consistency
uv run python <skill-dir>/scripts/main.py images/icon.png "gear" \
  --style <skill-dir>/assets/styles/neon_wireframe.md \
  --ref <skill-dir>/assets/styles/neon_wireframe/examples/1.png

# 5. Custom aspect ratio with flat style
uv run python <skill-dir>/scripts/main.py images/thumbnail.png \
  "Tutorial thumbnail with code editor" \
  --style <skill-dir>/assets/styles/minimalist_flat.md \
  --aspect 16:9
```

## Workflow Tips

1. **First-time setup:** Dependencies auto-install on first run (no manual setup needed!)
2. **API key:** Verify `GOOGLE_AI_API_KEY` is set before generation
3. **Path resolution:** Always use absolute paths to skill directory
4. **Output location:** Images save to user's current working directory
5. **Error messages:** Parse script output for clear error indications
6. **Consistency:** Use templates + references for maximum style consistency
7. **Iteration:** Use solid backgrounds if you plan to iterate (avoid gradients)
8. **Batch processing:** Generate similar assets together for efficiency

## Security Reminders

- Never commit `.env` files to version control
- Add `.env` to `.gitignore`
- Use environment variables for production deployments
- Rotate API keys periodically
- Monitor API usage in Google AI Studio dashboard
