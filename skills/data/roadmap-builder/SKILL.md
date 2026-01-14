---
name: roadmap-builder
description: Product roadmap prioritization and feature decision framework. Use when the user needs help deciding what to build next, evaluating feature ideas, prioritizing their backlog, challenging feature requests, planning their product roadmap, or when they ask questions like "should I build this feature?", "what should I work on next?", "help me prioritize", "is this feature worth building?", or when discussing product strategy and feature decisions.
---

# Roadmap Builder

Ruthlessly focused product roadmap prioritization that keeps you building what matters.

## Core Philosophy

Build for real users, not imaginary ones. Ship fast, validate with usage, iterate based on data. Every feature must justify its existence.

## Prioritization Framework

### Impact vs Effort Matrix

Always evaluate features on two dimensions:

**Impact**: Will this meaningfully move core metrics? (Retention, revenue, growth)
**Effort**: Engineering time, complexity, maintenance burden

**Priority order:**
1. High Impact, Low Effort → Build immediately
2. High Impact, High Effort → Plan carefully, phase if possible
3. Low Impact, Low Effort → Build only if quick wins needed
4. Low Impact, High Effort → Never build

### Category Hierarchy

When multiple features compete, prioritize in this order:

1. **Retention** - Keep existing users engaged and coming back
2. **Core Features** - Essential functionality for the primary use case
3. **Monetization** - Features that directly generate revenue
4. **Growth** - Features that attract new users

## Stage-Based Rules

The stage of your product fundamentally changes what you should build.

### Pre-Launch Stage

**ONLY build core loop features. Nothing else.**

Core loop = The essential user journey that delivers your product's primary value.

Do NOT build:
- Analytics dashboards
- Admin panels
- Settings pages
- Edge case features
- "Nice to have" features
- Onboarding flows (beyond bare minimum)
- Social sharing
- Notifications

Build ONLY:
- Features required for a user to complete the core action
- Absolute minimum authentication/signup
- The simplest version that delivers value

**Decision rule**: If removing this feature means users can't experience the core value proposition, build it. Otherwise, wait.

### Post-Launch Stage

**ONLY build features users explicitly request.**

Post-launch validation requirements:
- At least 3 different users asked for it
- Users describe a specific problem, not a solution
- You can articulate the underlying need in one sentence

Do NOT build based on:
- Your assumptions
- Competitor features
- "It would be cool if..."
- Imagined future use cases

**Decision rule**: Has a real user with a paid account (or active usage) explicitly requested this feature? If no, don't build it.

### Growth Phase

**Focus on features that reduce churn or increase sharing.**

Prioritize features that:
- Reduce drop-off in critical flows
- Make the product more viral/shareable
- Increase activation of dormant users
- Strengthen retention of power users

Avoid:
- New user acquisition features (unless sharing/referral)
- Optimization of non-critical flows
- Features for hypothetical new user segments

**Decision rule**: Will this feature directly impact churn rate or drive organic growth? If no, reconsider.

## Feature Validation Questions

Before building ANY feature, answer these questions honestly:

### 1. Does this serve the core use case?

If the feature is tangential to your product's main value proposition, it's a distraction.

**Test**: Can you explain how this feature directly supports the primary reason users come to your product?

### 2. Will users actually use this or just say they want it?

Users often request solutions without understanding their real problem. They're great at identifying pain points but terrible at prescribing solutions.

**Test**: Can you identify the underlying problem the user is trying to solve? Is there a simpler solution?

**Red flag**: User says "It would be cool if..." or "You should add..." without describing a specific problem they experienced.

### 3. Can we fake it first to validate demand?

Before building, test if users actually want it with minimal effort:

- Manual processes (do it by hand first)
- Wizard of Oz testing (fake the feature, deliver manually)
- Simple prototypes or mockups
- Feature announcement (see if users respond)

**Test**: What's the absolute minimum viable way to test if users will actually use this?

## Red Flags

### Feature Creep

**Symptoms:**
- Adding features because they're "cool" or "modern"
- Building because competitors have it
- Scope expanding during development
- Feature list growing faster than user requests

**Antidote**: Every feature must trace back to a specific user problem and measurable impact.

### Premature Optimization

**Symptoms:**
- Building scalability before you have scale problems
- Optimizing features few users touch
- Adding complexity for theoretical future needs
- Building infrastructure "just in case"

**Antidote**: Build for current reality, not imagined future. Optimize when metrics show it matters.

### Building for Imaginary Users

**Symptoms:**
- "Users will probably want..."
- "When we have enterprise clients..."
- "Future users might need..."
- Designing for a persona that doesn't exist yet

**Antidote**: Only build for users you can name. If you can't point to 3+ real users who need this, don't build it.

## Decision Workflow

Use this workflow when evaluating any feature request:

### Step 1: Identify the Stage

What stage is your product in?
- Pre-launch → Apply pre-launch rules
- Post-launch → Apply post-launch rules  
- Growth phase → Apply growth rules

### Step 2: Source Validation

Who requested this feature?
- Real users with context → Continue evaluation
- Internal team assumption → Challenge strongly
- Competitor feature → Ask "Do OUR users need this?"

### Step 3: Impact Assessment

Map to category hierarchy:
- Does it improve retention?
- Is it core functionality?
- Does it drive revenue?
- Does it enable growth?

Estimate realistic impact on key metrics.

### Step 4: Effort Calibration

Be brutally honest about effort:
- Engineering time (include testing, edge cases)
- Maintenance burden (ongoing support)
- Complexity added to the product

### Step 5: Validation Test

Can you validate demand without building it first?
- If yes → Do the validation test first
- If no → Is the impact high enough to justify risk?

### Step 6: Make the Decision

**Build if:**
- Passes stage-based rules
- High or medium impact
- Reasonable effort
- Can't easily validate demand without building
- At least 3 real users requested it (post-launch)

**Don't build if:**
- Fails stage-based rules
- Low impact regardless of effort
- Imaginary users or assumptions
- Can validate with a fake/manual version first

**Defer if:**
- High impact but very high effort → Break into phases
- Medium impact, medium effort → Wait for more demand
- Unclear impact → Run validation experiment first

## Output Format

When advising on features, always provide:

1. **Recommendation**: Build now / Don't build / Defer / Validate first
2. **Reasoning**: Which rules and questions led to this decision
3. **Key Concerns**: Specific red flags or risks identified
4. **Alternative**: If recommending against, suggest what to focus on instead
5. **Validation Test**: If applicable, describe how to test demand without building

## Challenging Effectively

When a feature doesn't pass the framework, challenge constructively:

- Acknowledge the user's intent or underlying problem
- Explain which specific rule or red flag triggered concern
- Ask clarifying questions about impact and validation
- Suggest lighter-weight alternatives or validation approaches
- Redirect to higher-priority opportunities

**Example:**
"I understand wanting to add social sharing, but let's pause on that. We're in the pre-launch stage, and this doesn't serve the core loop. Real question: Can users complete your core action end-to-end right now? If not, that's what needs attention. Social sharing can be tested post-launch with a simple 'Share' button that copies a link - no engineering needed."

## Keeping Roadmap Focused

**Weekly check**: Review roadmap against these questions:
- What stage are we in? Are we following stage rules?
- Which category (Retention/Core/Monetization/Growth) are most items in?
- How many items are user-requested vs. internally generated?
- Are we building for real users or imaginary ones?

**Monthly audit**: Identify and cut:
- Items violating stage-based rules
- Low-impact features lingering in backlog
- Features with no clear validation path
- Scope creep that accumulated during planning

**Quarterly reset**: Revisit priorities from scratch:
- Has the stage changed?
- What did users actually request this quarter?
- What does retention/revenue data say matters?
- What can we cut that we thought was important?

## Remember

- Ship fast, validate with real usage, iterate based on data
- Real users beat imaginary users every time
- Features are liabilities until proven otherwise
- "No" is a complete sentence
- The best roadmap is the shortest one that delivers measurable impact
