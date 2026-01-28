---
name: write-plan
description: Create detailed implementation plans with task breakdown
disable-model-invocation: true
---

# Implementation Plan Writer

I'll create comprehensive implementation plans with task breakdowns, timelines, and success criteria.

Arguments: `$ARGUMENTS` - feature description, requirements, or planning focus

## Planning Philosophy

Based on **obra/superpowers** planning methodology:
- Break work into concrete, testable tasks
- Clear acceptance criteria for each task
- Identify dependencies and blockers
- Estimate complexity honestly
- Plan for validation and testing

**Token Optimization:**
- ✅ Grep to understand codebase structure (100 tokens vs 4,000+ reading all files)
- ✅ Focused file reading (only architecture-relevant files)
- ✅ Caching project patterns and conventions
- ✅ Template-based plan structure (no repeated boilerplate)
- ✅ Incremental planning (one phase at a time)
- ✅ Progressive detail (high-level → detailed only if needed)
- **Expected tokens:** 1,200-3,000 (vs. 3,000-5,000 unoptimized)
- **Optimization status:** ✅ Optimized (Phase 2 Batch 2, 2026-01-26)

**Caching Behavior:**
- Cache location: `.claude/cache/plans/project-patterns.json`
- Caches: Project conventions, architecture patterns, common tasks
- Cache validity: 7 days or until major structure changes
- Shared with: `/brainstorm`, `/execute-plan`, `/understand` skills

## Phase 1: Requirements Analysis

First, let me understand what we're planning:

```bash
#!/bin/bash
# Gather context for implementation planning

echo "=== Implementation Planning Context ==="
echo ""

# 1. Project structure (token-efficient with Grep)
echo "Project Structure:"
if [ -d "src" ]; then
    find src -type d -maxdepth 2 | head -10
elif [ -d "lib" ]; then
    find lib -type d -maxdepth 2 | head -10
else
    ls -d */ 2>/dev/null | head -5
fi

# 2. Technology stack
echo ""
echo "Tech Stack:"
if [ -f "package.json" ]; then
    grep -E '"(react|vue|angular|next|express)"' package.json | head -5
    echo "  Framework: JavaScript/TypeScript"
elif [ -f "requirements.txt" ]; then
    grep -E '(django|flask|fastapi)' requirements.txt | head -3
    echo "  Framework: Python"
elif [ -f "go.mod" ]; then
    echo "  Framework: Go"
fi

# 3. Existing patterns
echo ""
echo "Existing Patterns:"
if [ -d "tests" ] || [ -d "test" ]; then
    echo "  ✓ Test coverage present"
fi
if [ -f ".github/workflows" ] || [ -f ".gitlab-ci.yml" ]; then
    echo "  ✓ CI/CD configured"
fi
if [ -f "docker-compose.yml" ]; then
    echo "  ✓ Docker setup available"
fi

# 4. Similar features for reference
echo ""
echo "Similar features (for pattern matching):"
find . -type f -name "*.js" -o -name "*.ts" -o -name "*.py" | head -10
```

Now let me create the implementation plan structure:

## Phase 2: Plan Structure

I'll create a comprehensive plan document:

```markdown
# Implementation Plan: [Feature Name]

**Created**: [timestamp]
**Status**: Planning | In Progress | Completed
**Complexity**: Low | Medium | High | Very High
**Estimated Effort**: [X hours/days]

## 1. Executive Summary

**Goal**: [One sentence description of what we're building]

**Value Proposition**:
- **User Benefit**: [How this helps users]
- **Business Benefit**: [How this helps the business]
- **Technical Benefit**: [How this improves the system]

**Success Criteria**:
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

## 2. Requirements

### Functional Requirements
1. **[Requirement 1]**
   - Description: [detailed description]
   - Priority: Must Have | Should Have | Nice to Have
   - Acceptance Criteria: [how we know it's done]

2. **[Requirement 2]**
   - Description: [detailed description]
   - Priority: Must Have | Should Have | Nice to Have
   - Acceptance Criteria: [how we know it's done]

### Non-Functional Requirements
- **Performance**: [targets and constraints]
- **Security**: [security requirements]
- **Scalability**: [scale targets]
- **Accessibility**: [a11y requirements]
- **Browser Support**: [compatibility requirements]

### Out of Scope
- [Explicitly what we're NOT doing]
- [Deferred to future iterations]

## 3. Technical Design

### Architecture Overview
```
[ASCII diagram or description of architecture]

┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Frontend  │─────▶│   Backend   │─────▶│  Database   │
└─────────────┘      └─────────────┘      └─────────────┘
```

### Components
1. **[Component 1 Name]**
   - **Responsibility**: [what it does]
   - **Dependencies**: [what it depends on]
   - **Interface**: [public API]
   - **Location**: [file path]

2. **[Component 2 Name]**
   - **Responsibility**: [what it does]
   - **Dependencies**: [what it depends on]
   - **Interface**: [public API]
   - **Location**: [file path]

### Data Models
```typescript
// User model example
interface User {
  id: string;
  email: string;
  name: string;
  createdAt: Date;
}
```

### API Endpoints
- `POST /api/users` - Create new user
  - Request: `{ email, name }`
  - Response: `{ user, token }`
  - Errors: 400 (invalid), 409 (duplicate)

### Database Schema
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## 4. Task Breakdown

### Phase 1: Foundation (Estimated: X hours)
**Goal**: Set up basic structure

- [ ] **Task 1.1**: Create database schema
  - **Effort**: 1 hour
  - **Acceptance**: Migration runs successfully
  - **Dependencies**: None
  - **Assigned to**: TBD

- [ ] **Task 1.2**: Create base models
  - **Effort**: 2 hours
  - **Acceptance**: Models have full test coverage
  - **Dependencies**: Task 1.1
  - **Assigned to**: TBD

- [ ] **Task 1.3**: Set up API routes
  - **Effort**: 1 hour
  - **Acceptance**: Routes return 404 with proper structure
  - **Dependencies**: Task 1.2
  - **Assigned to**: TBD

### Phase 2: Core Implementation (Estimated: X hours)
**Goal**: Implement main functionality

- [ ] **Task 2.1**: Implement user creation logic
  - **Effort**: 3 hours
  - **Acceptance**: Users can be created with validation
  - **Dependencies**: Task 1.3
  - **Assigned to**: TBD

- [ ] **Task 2.2**: Add authentication
  - **Effort**: 4 hours
  - **Acceptance**: JWT tokens generated and validated
  - **Dependencies**: Task 2.1
  - **Assigned to**: TBD

### Phase 3: Frontend Integration (Estimated: X hours)
**Goal**: Build user interface

- [ ] **Task 3.1**: Create registration form
  - **Effort**: 2 hours
  - **Acceptance**: Form validates input and submits
  - **Dependencies**: Task 2.1
  - **Assigned to**: TBD

- [ ] **Task 3.2**: Add login page
  - **Effort**: 2 hours
  - **Acceptance**: Users can login and receive token
  - **Dependencies**: Task 2.2
  - **Assigned to**: TBD

### Phase 4: Testing & Validation (Estimated: X hours)
**Goal**: Ensure quality and correctness

- [ ] **Task 4.1**: Write unit tests
  - **Effort**: 4 hours
  - **Acceptance**: 80%+ code coverage
  - **Dependencies**: All above tasks
  - **Assigned to**: TBD

- [ ] **Task 4.2**: Write integration tests
  - **Effort**: 3 hours
  - **Acceptance**: All user flows tested
  - **Dependencies**: Task 4.1
  - **Assigned to**: TBD

- [ ] **Task 4.3**: Manual QA testing
  - **Effort**: 2 hours
  - **Acceptance**: No critical bugs found
  - **Dependencies**: Task 4.2
  - **Assigned to**: TBD

### Phase 5: Documentation & Deployment (Estimated: X hours)
**Goal**: Prepare for release

- [ ] **Task 5.1**: Write API documentation
  - **Effort**: 2 hours
  - **Acceptance**: All endpoints documented with examples
  - **Dependencies**: Task 4.3
  - **Assigned to**: TBD

- [ ] **Task 5.2**: Update user documentation
  - **Effort**: 1 hour
  - **Acceptance**: Users can follow guide to use feature
  - **Dependencies**: Task 5.1
  - **Assigned to**: TBD

- [ ] **Task 5.3**: Deploy to staging
  - **Effort**: 1 hour
  - **Acceptance**: Feature works in staging environment
  - **Dependencies**: Task 5.2
  - **Assigned to**: TBD

- [ ] **Task 5.4**: Production deployment
  - **Effort**: 1 hour
  - **Acceptance**: Feature live in production
  - **Dependencies**: Task 5.3, stakeholder approval
  - **Assigned to**: TBD

## 5. Dependencies & Blockers

### External Dependencies
- [ ] [Service/API] availability
- [ ] [Library/package] compatibility verified
- [ ] [Infrastructure] provisioned

### Internal Dependencies
- [ ] [Team/person] approval needed
- [ ] [Other feature] must be completed first
- [ ] [Design/specs] finalized

### Potential Blockers
- **Risk**: [description of risk]
  - **Impact**: High | Medium | Low
  - **Mitigation**: [how to prevent/handle]

## 6. Testing Strategy

### Unit Tests
- Test all business logic functions
- Mock external dependencies
- Target: 80%+ coverage

### Integration Tests
- Test API endpoints end-to-end
- Test database interactions
- Test authentication flows

### Manual Testing
- [ ] Happy path testing
- [ ] Error handling testing
- [ ] Edge case testing
- [ ] Performance testing
- [ ] Security testing

### Test Data
```javascript
// Sample test data
const testUser = {
  email: 'test@example.com',
  name: 'Test User'
};
```

## 7. Deployment Plan

### Pre-Deployment Checklist
- [ ] All tests passing
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] Database migrations tested
- [ ] Feature flags configured (if applicable)
- [ ] Monitoring/alerting set up

### Deployment Steps
1. Merge feature branch to main
2. Run database migrations
3. Deploy backend services
4. Deploy frontend changes
5. Verify deployment
6. Enable feature (if behind flag)
7. Monitor metrics

### Rollback Plan
1. Disable feature flag (if applicable)
2. Revert deployment
3. Rollback database migration (if needed)
4. Notify stakeholders

## 8. Success Metrics

### Key Performance Indicators (KPIs)
- **Adoption**: [target % of users using feature]
- **Performance**: [target response time]
- **Reliability**: [target uptime/error rate]
- **User Satisfaction**: [target satisfaction score]

### Monitoring
- **Metrics to track**: [list of metrics]
- **Alerts to set**: [alert conditions]
- **Dashboard**: [link to dashboard]

## 9. Timeline

**Week 1**: Phase 1 + Phase 2
**Week 2**: Phase 3 + Phase 4
**Week 3**: Phase 5 + Buffer

**Milestones**:
- [Date]: Backend API complete
- [Date]: Frontend integration complete
- [Date]: Testing complete
- [Date]: Production deployment

## 10. Team & Communication

### Roles
- **Developer**: [name/TBD]
- **Reviewer**: [name/TBD]
- **QA**: [name/TBD]
- **Product Owner**: [name/TBD]

### Communication Plan
- **Daily standups**: Progress updates
- **Weekly demos**: Show working features
- **Slack channel**: #feature-[name]
- **Documentation**: [wiki/confluence link]

## 11. Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Database migration fails | High | Low | Test thoroughly in staging |
| Performance issues | Medium | Medium | Load testing before launch |
| Integration complexity | Medium | High | Incremental integration |

## 12. Future Enhancements

**Phase 2 (Future)**:
- [Enhancement 1]
- [Enhancement 2]

**Technical Debt**:
- [Known limitations]
- [Areas for improvement]

## 13. Approval

- [ ] Product Owner approval
- [ ] Technical Lead approval
- [ ] Security review (if needed)
- [ ] Architecture review (if needed)

**Approved by**: _______________
**Date**: _______________
```

## Phase 3: Plan Generation

Based on your requirements, I'll generate the complete plan:

```bash
#!/bin/bash
# Generate implementation plan

create_implementation_plan() {
    local feature_name="$1"
    local plan_file="IMPLEMENTATION_PLAN.md"

    echo "Creating implementation plan for: $feature_name"

    # Generate plan with template
    cat > "$plan_file" << EOF
# Implementation Plan: $feature_name

Generated: $(date +%Y-%m-%d)

[Plan content as per template above]
EOF

    echo "Plan created: $plan_file"
    echo ""
    echo "Next steps:"
    echo "1. Review and refine the plan"
    echo "2. Get stakeholder approval"
    echo "3. Break into git issues/tickets"
    echo "4. Begin implementation"
}

create_implementation_plan "$ARGUMENTS"
```

## Task Breakdown Best Practices

**Good Task Characteristics:**
- ✅ Small enough to complete in 1-4 hours
- ✅ Has clear acceptance criteria
- ✅ Can be tested independently
- ✅ Has defined dependencies
- ✅ Measurable completion

**Bad Task Characteristics:**
- ❌ Too vague ("implement feature")
- ❌ Too large (multi-day tasks)
- ❌ No clear completion criteria
- ❌ Hidden dependencies

## Estimation Guidelines

**Complexity Factors:**
- **Simple**: Well-known patterns, minimal dependencies (1-2 hours)
- **Medium**: Some new patterns, moderate integration (3-6 hours)
- **Complex**: New patterns, significant integration (1-2 days)
- **Very Complex**: Novel solutions, major architecture changes (3-5 days)

**Buffer Rules:**
- Add 20% buffer for unknowns
- Add 30% buffer for external dependencies
- Add 50% buffer for legacy system integration

## Integration Points

This skill works well with:
- `/brainstorm` - Convert brainstorm ideas to implementation plan
- `/scaffold` - Generate code from the plan
- `/session-start` - Track implementation progress
- `/docs` - Document the implementation

## Practical Examples

**Create Plan:**
```bash
/write-plan "user authentication system"
/write-plan "add payment processing"
/write-plan "implement real-time notifications"
```

**Export to Issues:**
```bash
# Convert plan tasks to GitHub issues
convert_to_issues() {
    grep "^- \[ \]" IMPLEMENTATION_PLAN.md | while read -r task; do
        gh issue create --title "$task" --body "From implementation plan"
    done
}
```

## What I'll Actually Do

1. **Analyze requirements** - Understand what you want to build
2. **Gather context** - Use Grep to understand existing codebase
3. **Design architecture** - Plan technical approach
4. **Break down tasks** - Create concrete, testable tasks
5. **Estimate effort** - Realistic time estimates
6. **Identify risks** - Plan mitigation strategies
7. **Define success** - Clear acceptance criteria

**Important:** I will NEVER:
- Skip requirements analysis
- Create vague or untestable tasks
- Ignore dependencies and risks
- Add AI attribution

The plan will be comprehensive, actionable, and ready for immediate implementation.

**Credits:** Planning methodology based on [obra/superpowers](https://github.com/obra/superpowers) task breakdown principles and agile project management best practices.
