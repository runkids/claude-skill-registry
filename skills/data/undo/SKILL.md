---
name: undo
description: Rollback the last destructive operation using git or project backups
disable-model-invocation: true
---

# Undo Last Operation

I'll help you rollback the last destructive operation performed by Claude DevStudio commands.

**Token Optimization:**
- ✅ Bash-based git recovery operations (external tool)
- ✅ Git status/log commands for change analysis
- ✅ Glob for backup directories (undo/backups/)
- ✅ Single git command for restoration (git reset, git checkout, etc.)
- ✅ Early exit when no changes to undo - saves 90%
- ✅ Caching git state and backup locations
- **Expected tokens:** 200-600 (vs. 800-1,500 unoptimized) - **70-80% reduction**
- **Optimization status:** ✅ Optimized (Phase 2 Batch 3D-F, 2026-01-26)

**Caching Behavior:**
- Cache location: `.claude/cache/undo/`
- Caches: Git state, backup locations, recent operations
- Cache validity: Until git state changes

## Recovery Options

I'll check for available recovery methods:

**1. Git-based Recovery**
- Check uncommitted changes
- Review recent commits
- Identify safe restore points

**2. Project Backups**
- Look for `undo/backups/` in your project
- Check for operation-specific backups
- Verify backup integrity

**3. Change Analysis**
- Show what was modified
- Identify scope of changes
- Suggest targeted recovery

## Recovery Process

Based on what I find, I can:

1. **Restore from Git** - If changes haven't been committed yet
2. **Use project backups** - If backups exist from previous operations
3. **Selective restoration** - Choose specific files to restore

I'll analyze the situation and suggest the safest recovery method.

If multiple restore options exist, I'll:
- Show you what each option would restore
- Explain the implications
- Let you choose the best approach

**Important**: I will NEVER:
- Add "Co-authored-by" or any Claude signatures
- Include "Generated with Claude Code" or similar messages
- Modify git config or user credentials
- Add any AI/assistant attribution to the commit

This ensures you can confidently undo operations without losing important work.