# Claude Skills Registry

<p align="center">
  <img src="https://img.shields.io/badge/Skills-29,000+-purple?style=flat-square" alt="Skills">
  <img src="https://img.shields.io/badge/Updated-Daily-green?style=flat-square" alt="Updated">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square" alt="License">
</p>

> The most comprehensive Claude Code skills registry - **29,000+ skills indexed**

## What is this?

The largest searchable index of Claude Code skills, aggregated from GitHub and community sources. Use with the [sk CLI](https://github.com/majiayu000/caude-skill-manager) for fast skill discovery and installation.

## Highlights

- **29,000+ Skills** - The most comprehensive collection available
- **12 Categories** - Development, Testing, DevOps, Design, and more
- **Daily Updates** - Automated crawling and validation
- **Quality Indexed** - Metadata, descriptions, and star counts

## Using the Registry

```bash
# Install sk first
go install github.com/majiayu000/caude-skill-manager@latest

# Search skills (uses this registry)
sk search testing
sk search pdf
sk search --popular

# Install a skill
sk install anthropics/skills/docx
```

## Registry Structure

```
skill-registry/
├── registry.json       # Main index (all skills)
├── sources/            # Individual source configs
│   ├── anthropic.json  # Official Anthropic skills
│   ├── community.json  # Community skills
│   └── awesome.json    # Curated awesome skills
├── categories/         # Category-based indexes
│   ├── documents.json
│   ├── development.json
│   └── ...
└── scripts/            # Update scripts
    └── update.py
```

## Adding Your Skill

### Option 1: Submit via Issue

1. Open an [issue](https://github.com/majiayu000/skill-registry/issues/new)
2. Use the "Add Skill" template
3. Provide: repo URL, name, description, category

### Option 2: Submit via PR

1. Fork this repo
2. Add your skill to `sources/community.json`:

```json
{
  "name": "your-skill-name",
  "repo": "your-username/your-repo",
  "path": "optional/path/to/skill",
  "description": "What your skill does",
  "category": "development",
  "tags": ["testing", "automation"]
}
```

3. Submit a PR

## Categories

| Category | Count | Description |
|----------|-------|-------------|
| `development` | 11,185 | Development tools, frameworks, workflows |
| `data` | 4,242 | Data processing, analysis, databases |
| `design` | 3,894 | UI/UX design, frontend, styling |
| `testing` | 2,966 | Testing, QA, automation |
| `devops` | 2,073 | DevOps, CI/CD, infrastructure |
| `documents` | 1,973 | Document creation/editing (docx, pdf, pptx) |
| `productivity` | 1,088 | Productivity and automation |
| `product` | 818 | Product management, planning |
| `security` | 501 | Security, auditing, compliance |
| `marketing` | 339 | Marketing, content, SEO |

## API

The registry can be accessed directly via raw GitHub URLs:

```bash
# Full registry
curl https://raw.githubusercontent.com/majiayu000/claude-skill-registry/main/registry.json

# Specific category
curl https://raw.githubusercontent.com/majiayu000/claude-skill-registry/main/categories/development.json
```

## Auto-Updates

This registry is automatically updated daily via GitHub Actions:
- Fetches latest skill metadata from GitHub
- Validates SKILL.md files exist
- Updates star counts and descriptions
- Removes dead/invalid skills

## License

MIT License - see [LICENSE](LICENSE) for details.
