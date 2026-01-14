---
name: reactive-md
description: Literate UI/UX for product teams - accelerate from idea to working prototype in minutes using markdown with embedded interactive React components. Use for fast iteration and async collaboration on product specs, wireframes, user flows, feature demos, and design documentation. Replaces Figma/Storybook with executable specs in version control.
license: MIT
metadata:
  version: "1.0.0"
  public-docs-commit: "7d03f60"
  public-docs-repo: "https://github.com/million-views/reactive-md"
---

# Reactive MD

Generate functional markdown documents with embedded interactive React components for product design collaboration.

## When to Use This Skill

Use reactive-md when the user asks to create:

**Primary Use Cases:**
- Product specs with working prototypes
- Design system documentation with live examples
- User flow wireframes and interactive demos
- Feature prototypes, concept exploration, and visual demos
- A/B tests, dashboards, component galleries
- Interactive documentation and living specifications

**Workflow**: Check if a recipe exists for the request (see Working with Recipes). Adapt existing recipes when available.

**Aliases**: "live doc", "prototype", "POC", "interactive spec" all refer to reactive-md documents.

## Core Capabilities

Reactive-md documents support:

**Two Preview Modes:**
1. **Static Preview** (Markdown Preview): Offline, bundled packages only, server-side rendering
2. **Interactive Preview** (`Cmd+K P`): Browser-based webview, supports CDN packages and platform APIs

**Live Fences (CRITICAL):**

**When to use `live` annotation:**
- User wants to **see/interact** with the component
- Creating a working demo or prototype
- Showing how something works in practice
- All primary use cases (prototypes, concept exploration, specs, wireframes, demos)

**When to use regular fences (no `live`):**
- Explaining **how** something works (discourse about the code)
- Showing anti-patterns or broken examples
- Comparing different approaches side-by-side
- Code snippets that are incomplete or won't run standalone

**Syntax:**
- `` ```jsx live `` - JavaScript + JSX components (executable)
- `` ```tsx live `` - TypeScript + JSX components (executable)
- `` ```css live `` - CSS stylesheets (executable)
- `` ```jsx `` - Code examples for discussion (non-executable)
- `` ```tsx `` - Code snippets for illustration (non-executable)
- `` ```css `` - CSS snippets for illustration (non-executable)

**Default behavior:** When in doubt, use `live` - reactive-md's purpose is interactive demos.

**File Types:**
- Markdown (`.md`) - Primary document only (entry point)
- JSX/TSX (`.jsx`, `.tsx`) - Can be inline (`jsx live` blocks) OR external files (imported)
- CSS (`.css`) - Can be inline (`css live` blocks) OR external files (imported)
- JSON (`.json`) - Data files (imported or used inline)

**Hot Module Reload:** Edit `.jsx`, `.tsx`, `.css`, `.json` → preview updates automatically

## Package & Data Loading

**Common packages available:**
- Bundled (always): `dayjs`, `motion/react`, `lucide-react`, `clsx`, `uuid`, `es-toolkit`
- CDN (Interactive Preview): `@heroicons/react`, `zustand`, `jotai`, `tailwind-merge`, `react-hook-form`
- Known broken: `recharts`, `swr`, `@tanstack/react-query` → Use native SVG/Canvas

**Data loading:**
- ✅ Local JSON files: `import data from './data.json' with { type: 'json' };`
- ✅ Remote APIs: `fetch('https://api.example.com/data')`
- ❌ Fetch local files at runtime: Blocked by webview security

**For React import rules (CRITICAL):** Read [references/GUIDE.md § React Imports](references/GUIDE.md#react-imports)
**For package details:** Read [references/GUIDE.md § Package and Dependency Management](references/GUIDE.md#package-and-dependency-management)
**For data loading patterns:** Read [references/GUIDE.md § Data Files](references/GUIDE.md#data-files)

## Platform APIs

Interactive Preview (`Cmd+K P`) supports:
- ✅ `localStorage`, `sessionStorage`, timers, remote `fetch()`, `Canvas`
- ❌ WebSockets, Service Workers, local file `fetch()` (use `import` instead)

## Design Systems

**Choose ONE styling approach per document:**

### Option A: Reactive-md Design System (Recommended for most use cases)

Two fidelity levels:
- **Wireframe** - Low-fidelity structural mockups
- **Elementary** - High-fidelity themeable components (light/dark mode support)

Both use the same architecture: import tokens + component classes, then use pre-built classes in JSX.

**Import pattern (CRITICAL - use BEFORE components):**

```css live
/* Wireframe variant */
@import '../recipes/design-systems/wireframe/tokens.css';
@import '../recipes/design-systems/reactive-md.css';
```

```css live
/* Elementary variant */
@import '../recipes/design-systems/elementary/tokens.css';
@import '../recipes/design-systems/reactive-md.css';
```

**What you get:**
- **tokens.css** - CSS custom properties (`--c-primary`, `--s-3`, `--r-btn`)
- **reactive-md.css** - Component classes (`.wf-btn`, `.wf-card`, `.wf-hero`, `.wf-features`)

**Usage:** Use component classes from reactive-md.css: `<button className="wf-btn primary">`. Do NOT invent utilities like `className="bg-[var(--c-primary)]"` - use existing `.wf-btn` with modifiers (`.primary`, `.secondary`, `.action`).

### Option B: Tailwind CSS (Quick prototyping without recipes)

Utility-first framework via CDN. No imports needed, no CSS custom properties, no component classes.

**Usage:** Pure Tailwind utilities only: `<button className="bg-blue-500 px-4 py-2 rounded">`. Do NOT mix with reactive-md system.

**NEVER mix systems.** Pick homegrown OR Tailwind, not both.

**For component class lists:** Read [recipes/design-systems/elementary/tokens.md](recipes/design-systems/elementary/tokens.md) or [recipes/design-systems/wireframe/tokens.md](recipes/design-systems/wireframe/tokens.md)
**For dashboard layouts:** Read [recipes/design-systems/use-cases/dashboards.md](recipes/design-systems/use-cases/dashboards.md)
**For dark mode implementation:** Read [recipes/feature-concepts/dark-mode-toggle/spec.md](recipes/feature-concepts/dark-mode-toggle/spec.md)

## File Organization

### Single File (Inline Code)

**When:** Simple concepts (< 50 lines total)

✅ **With helper components** - Wrap in parent function
✅ **Without helpers** - Pure JSX at top level
❌ **Don't mix** helper functions with top-level JSX (ambiguous entry point)

### Folder Structure

**When:** Complex features (> 50 lines)

```
feature-name/
  spec.md              (primary document)
  Component.jsx        (extracted component)
  styles.css           (shared styles)
  data.json            (mock data)
```

**Naming:** Kebab-case, hierarchical context (e.g., `checkout-flow-payment-form.jsx`)

**For complete patterns and examples:** Read [references/GUIDE.md § Component Structure Best Practices](references/GUIDE.md#component-structure-best-practices)

## Working with Recipes

**Recipes are optional examples** to speed up common tasks. Use them when they fit the request.

**Recipe categories:** PRD templates, Wireframes, User journeys, Feature concepts, UI catalog, Case studies

**How to use:**
1. **If request matches known pattern** → Load relevant recipe from [references/use-cases.md](references/use-cases.md)
2. **Adapt, don't copy** → Modify to user's specific needs
3. **Otherwise** → Apply design system principles and create from scratch

**When recipes are missing:** Acknowledge the gap, offer alternatives (Tailwind for quick prototyping), never mix styling paradigms.

## Document Structure

**Standard pattern:** Problem → Solution → Live Code → Next Steps

Use short live fences that import from files. Include semantic headings and prose explaining intent.

## Clarifying Questions

When context is ambiguous, ASK instead of guessing:

- **Scope**: "Make a dashboard" → Ask purpose (analytics? admin? monitoring?) and data
- **Styling**: "Create a form" → Ask Tailwind (quick) vs CSS vars (brandable)
- **File context**: User says "improve this" → Check which file is open or selected

## Refusal Boundaries

Reactive-md is a powerful prototyping tool. Refuse only when requests require infrastructure or services outside the extension's scope.

### What Reactive-MD CAN Do

Complex interactive UIs, real API integration, error handling, authentication UI, data persistence (localStorage), form validation, complex state management.

### Refuse: Infrastructure & Backend

**Triggers:** Deploy, CI/CD, Docker, cloud platforms, backend implementation, databases, auth services, test frameworks.

**Response template:**
```
🚫 [Infrastructure/Backend/Testing] Boundary

Reactive-md prototypes run in VS Code, not production infrastructure.

This prototype CAN demonstrate: [UI/UX flow, API integration, interactive behavior]

To productionize: Graduate to proper project with infrastructure tooling.
```

## Quality Standards

Good output must:

1. ✅ **Use existing recipes** - Adapt proven templates
2. ✅ **Preserve design systems** - Keep imports from recipes
3. ✅ **Run without errors** - Code executes in preview
4. ✅ **Follow conventions** - File organization, naming
5. ✅ **Respect boundaries** - Refuse infrastructure/backend only
6. ✅ **Embrace capabilities** - Use fetch, error handling, complex state
7. ✅ **Complete structure** - Problem → Solution → Code → Next Steps

## Reference Documentation

**[GUIDE.md](references/GUIDE.md)** - Troubleshooting, constraints, patterns
**[use-cases.md](references/use-cases.md)** - Recipe catalog, job-to-recipe mapping

**Recipe Directories:** prd-templates, design-systems, user-journeys, feature-concepts, ui-catalog, case-studies

## Success Criteria

**Primary success**: User goes from idea to working prototype in < 10 minutes.

**Key outcomes**:
1. Iterate fast (minutes, not days)
2. Communicate visually (executable specs vs static mocks)
3. Collaborate async (version-controlled `.md` files)
4. Make decisions faster (working prototypes resolve debates)
5. Ship confident specs (living documentation shows exact behavior)

**Goal:** Make reactive-md the fastest path from product idea to shared understanding.
