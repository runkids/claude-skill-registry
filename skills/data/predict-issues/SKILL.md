---
name: predict-issues
description: Proactive problem identification through code analysis and pattern detection
disable-model-invocation: false
---

# Predictive Code Analysis  

I'll analyze your codebase to predict potential problems before they impact your project.

## Strategic Thinking Process

<think>
To make accurate predictions, I need to consider:

1. **Pattern Recognition**
   - Which code patterns commonly lead to problems?
   - Are there growing complexity hotspots?
   - Do I see anti-patterns that will cause issues at scale?
   - Are there ticking time bombs (hardcoded values, assumptions)?

2. **Risk Assessment Framework**
   - Likelihood: How probable is this issue to occur?
   - Impact: How severe would the consequences be?
   - Timeline: When might this become a problem?
   - Effort: How hard would it be to fix now vs later?

3. **Common Problem Categories**
   - Performance: O(n²) algorithms, memory leaks, inefficient queries
   - Maintainability: High complexity, poor naming, tight coupling
   - Security: Input validation gaps, exposed secrets, weak auth
   - Scalability: Hardcoded limits, single points of failure

4. **Prediction Strategy**
   - Start with highest risk areas (critical path code)
   - Look for patterns that break at 10x, 100x scale
   - Check for technical debt accumulation
   - Identify brittleness in integration points
</think>

**Token Optimization:**
- ✅ Grep-before-Read for pattern detection (no speculative reads)
- ✅ Glob for file structure analysis (no file reads)
- ✅ Progressive disclosure (critical → high → medium → low)
- ✅ Focus area flags (--performance, --security, --maintainability, --scalability)
- ✅ Default to git diff scope (changed files + dependencies)
- ✅ Caching issue patterns and hotspot analysis
- ✅ Early exit when no high-risk patterns found - saves 85%
- **Expected tokens:** 1,200-3,500 (vs. 3,000-5,000 unoptimized) - **50-60% reduction**
- **Optimization status:** ✅ Optimized (Phase 2 Batch 3B, 2026-01-26)

**Caching Behavior:**
- Cache location: `.claude/cache/predict-issues/`
- Caches: Known issue patterns, complexity hotspots, dependency risks
- Cache validity: Until codebase structure changes significantly
- Shared with: `/review`, `/security-scan`, `/complexity-reduce` skills

**Usage:**
- `predict-issues` - Analyze changed files (default, 1,200-2,000 tokens)
- `predict-issues all` - Full codebase analysis (3,000-3,500 tokens)
- `predict-issues --performance` - Performance issues only (800-1,500 tokens)
- `predict-issues --security` - Security risks only (800-1,500 tokens)
- `predict-issues --maintainability` - Code quality issues (1,000-2,000 tokens)

Based on this analysis framework, I'll use native tools for comprehensive analysis:
- **Grep tool** to search for problematic patterns (no file reads)
- **Glob tool** to analyze file structures and growth (no file reads)
- **Read tool** to examine complex functions and hotspots (only after Grep identifies specific risks)

I'll examine:
- Code complexity trends and potential hotspots
- Performance bottleneck patterns forming
- Maintenance difficulty indicators
- Architecture stress points and scaling issues
- Error handling gaps

For each prediction, I'll:
- Show specific code locations with file references
- Explain why it's likely to cause future issues
- Estimate potential timeline and impact
- Suggest preventive measures with priority levels

When I find multiple issues, I'll create a todo list for systematic review and prioritization.

Analysis areas:
- Functions approaching complexity thresholds
- Files with high change frequency (potential hotspots)
- Dependencies with known issues or update requirements
- Performance patterns that don't scale
- Code duplication leading to maintenance issues

After analysis, I'll ask: "How would you like to track these predictions?"
- Create todos: I'll add items to track resolution progress
- Create GitHub issues: I'll generate properly formatted issues with details
- Summary only: I'll provide actionable report without task creation

**Important**: I will NEVER:
- Add "Created by Claude" or any AI attribution to issues
- Include "Generated with Claude Code" in descriptions
- Modify repository settings or permissions
- Add any AI/assistant signatures or watermarks

Predictions will include:
- Risk level assessment (Critical/High/Medium/Low)
- Estimated timeline for potential issues
- Specific remediation recommendations
- Impact assessment on project goals

This helps prevent problems before they impact your project, saving time and maintaining code quality proactively.