---
name: deploy
description: Deploy or release the project. Use when releasing a new version.
allowed-tools: Read, Edit, Bash
---

# Deploy Skill

Steps to deploy/release a new version.

## Pre-Deploy Checklist

- [ ] All tests pass
- [ ] Linting/type checks pass (if applicable)
- [ ] CHANGELOG.md updated with version changes
- [ ] README.md updated if needed
- [ ] All changes committed

## Version Update

Update version in ALL relevant locations:

Common locations:
- `pyproject.toml` / `package.json` / `Cargo.toml`
- Source code version constant (e.g., `__version__`)
- Documentation

## General Deploy Steps

```bash
# 1. Verify tests pass
# Run your project's test command

# 2. Update version numbers (see above)

# 3. Update CHANGELOG.md
# Add new section for this version

# 4. Build/package (project-specific)
# e.g., python -m build, npm run build, cargo build --release

# 5. Publish (project-specific)
# e.g., twine upload, npm publish, cargo publish

# 6. Git tag and push
git add -A
git commit -m "Release vX.Y.Z: Description"
git tag vX.Y.Z
git push origin main --tags
```

## Post-Deploy

1. Verify deployment:
   - Check package registry (PyPI, npm, crates.io)
   - Test installation from registry

2. Update CONTINUITY.md:
   - Mark deploy task as DONE
   - Add session log entry with release URL
   - Update CURRENT STATE version

## Version Numbering (SemVer)

- **X.Y.Z**
- **X** (Major): Breaking changes
- **Y** (Minor): New features (backward compatible)
- **Z** (Patch): Bug fixes

## Troubleshooting

**Build fails**: Check dependencies, run clean build
**Upload fails**: Check credentials/API keys
**Tests fail**: Fix tests before deploying
