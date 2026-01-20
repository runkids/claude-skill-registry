---
name: new-project
description: Create a new project page to showcase research projects, side projects, or open-source work. Use when adding portfolio items.
allowed-tools: Write, Bash(mkdir:*)
---

# Adding a New Project

## Instructions

When creating a project page:

1. **Generate the slug**:
   - Use the project name, lowercase with hyphens
   - Example: "flame-benchmark" or "ml-toolkit"

2. **Create directory structure**:
   ```
   projects/<slug>/
   ├── index.qmd
   └── featured.png   (project thumbnail/screenshot)
   ```

3. **Create index.qmd with frontmatter**:
   ```yaml
   ---
   title: "Project Name"
   description: "One-line description for listings"
   date: YYYY-MM-DD
   categories: [Research, Open Source, Tool, etc.]
   image: featured.png

   # Project links
   github: "https://github.com/username/repo"
   demo: "https://demo-url.com"
   docs: "https://docs-url.com"

   # Project status
   status: "Active"  # Active, Completed, Archived, In Development

   # Technologies used
   tech: [Python, PyTorch, React, etc.]

   # Featured on homepage?
   featured: true
   ---
   ```

4. **Structure the content**:
   ```markdown
   Brief project overview (2-3 sentences)...

   ## Overview

   More detailed description of what the project does and why it matters.

   ## Features

   - Key feature 1
   - Key feature 2
   - Key feature 3

   ## Getting Started

   ```bash
   pip install project-name
   ```

   ## Links

   - [GitHub Repository](https://github.com/...)
   - [Documentation](https://...)
   - [Live Demo](https://...)

   ## Related Publications

   If applicable, link to related papers.
   ```

## Project Categories

Common categories:
- `Research` - Academic research projects
- `Open Source` - Open-source tools/libraries
- `Tool` - Utilities and developer tools
- `Demo` - Interactive demonstrations
- `Data` - Datasets or data projects
- `Web` - Web applications
- `ML` - Machine learning projects

## Featured Image Guidelines

- Size: 1200x630px (social sharing friendly)
- Format: PNG for screenshots, JPG for photos
- Content: Screenshot, diagram, or project logo
- Keep under 500KB

## Example

**File**: `projects/flame/index.qmd`

```yaml
---
title: "FLAME"
description: "Financial Language Model Evaluation framework for benchmarking LLMs"
date: 2024-03-01
categories: [Research, ML, Open Source]
image: featured.png
github: "https://github.com/gmatlin/flame"
status: "Active"
tech: [Python, PyTorch, Hugging Face]
featured: true
---

FLAME is a comprehensive evaluation framework designed to assess the capabilities
of large language models on financial domain tasks...
```
