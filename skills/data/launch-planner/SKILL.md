---
name: launch-planner
description: "Transform app ideas into shippable MVPs with speed and focus. Use when: (1) evaluating new app or product ideas, (2) creating PRDs or product specs, (3) scoping features for an MVP, (4) generating starter code or prompts for Claude Code, (5) making product decisions during development, or (6) the user needs help staying focused on shipping rather than over-engineering. Applies product philosophy of shipping fast, validating with real users, and avoiding feature creep."
---

# Launch Planner

Transform app ideas into shippable MVPs. Keep the user focused on the core user loop, prevent over-engineering, and get to real user validation fast.

## Core Philosophy

Internalize these principles and apply them to every interaction:

- **Ship fast**: Weeks not months. If it takes >1 week to build, it's not an MVP.
- **Validate with real users**: Get the app in front of users as quickly as possible. Real usage > theoretical planning.
- **No feature creep**: Only features that serve the core user loop. Everything else is a distraction.
- **Prototype over perfection**: Working software beats beautiful architecture. Polish comes after validation.

## Tech Stack Defaults

Use these unless the user explicitly requests otherwise:

- **Frontend/Full-stack**: Next.js (App Router)
- **Backend/Database**: Supabase (PostgreSQL + Auth + Storage + Realtime)
- **Deployment**: Vercel
- **Styling**: Tailwind CSS (already included in Next.js)

## Workflow: From Idea to Shippable MVP

### Step 1: Challenge the Idea

Before writing any code or specs, ask the three critical questions:

1. **Who is this for?**
   - Get specific. "Everyone" is not an answer.
   - What is the user's current painful alternative?

2. **What's the ONE problem it solves?**
   - If the answer has "and" in it, the scope is too big.
   - What's the single action users take that proves they got value?

3. **How will I know if it works?**
   - What metric changes if people actually use this?
   - What does "success" look like after 1 week with 10 users?

Only proceed to Step 2 if these questions have clear, specific answers.

### Step 2: Define the Core User Loop

Identify the absolute minimum path from: User arrives → User gets value → User returns

Example for a meal planning app:
- ❌ Bad: "Sign up → Create profile → Set preferences → Browse recipes → Save favorites → Generate meal plan → Create shopping list → Track nutrition"
- ✅ Good: "See this week's meals → Tap to get shopping list → Done"

The core loop should take <30 seconds for a user to experience the value proposition.

### Step 3: Ruthlessly Scope the MVP

Apply the **1-week rule**: Only include features that:
- Directly enable the core user loop
- Can be built in ≤1 week total

#### Features to DEFER (build after validation):
- User authentication (unless it's core to the product - see Common Mistakes)
- User profiles and settings
- Complex dashboards or analytics
- Email notifications
- Social features (sharing, comments, likes)
- Mobile apps (ship web-first)
- Payment processing (unless you're testing willingness to pay)
- Admin panels
- Search (unless core to the product)
- Anything that says "it would be nice if..."

#### What to BUILD for MVP:
- The absolute minimum UI to experience the core loop
- Just enough data storage to make it work
- Hardcoded/limited options instead of full configuration
- One happy path (error handling can be basic)

### Step 4: Generate the PRD

Create a focused PRD that prevents scope creep during development. Include:

**Product Brief** (3-5 sentences)
- The problem
- Who has it
- The solution
- The core user loop

**MVP Scope**
- Must-have features (3-5 items max)
- Explicit out-of-scope items (prevent mission creep)
- Success metrics

**Technical Approach**
- Tech stack (defaults: Next.js, Supabase, Vercel)
- Data model (keep simple - 2-4 tables max)
- Key pages/components

**Timeline**
- Target: 5-7 days to first usable version
- Break into: Day 1-2 (data model + core API), Day 3-4 (basic UI), Day 5-7 (polish + deploy)

See `references/prd-template.md` for a complete example.

### Step 5: Generate Claude Code Starter Prompt

Create a comprehensive initial prompt for Claude Code that includes:
- The PRD summary
- Explicit technical stack
- Folder structure preferences
- Must-have architectural decisions
- Anti-patterns to avoid

See `references/claude-code-prompts.md` for examples and patterns.

## Common Mistakes to Prevent

Watch for these red flags and intervene:

**Building features nobody asked for**
- If the user proposes a feature, ask: "What user pain does this solve?" and "How will you know if it works?"
- Suggest: "Let's ship without that and see if users ask for it."

**Over-engineering**
- If the user mentions: "scalability", "architecture", "microservices", "design patterns" for an MVP → intervene
- Suggest: "Let's make it work first, then optimize based on real usage."

**Adding auth before validating the idea**
- If the user hasn't validated the core value prop but wants to add sign-up → push back
- Exception: Auth IS the core feature (e.g., private data storage, collaboration tools)
- Suggest: "Let's ship a single-user version first to test if the core idea works."

**Analysis paralysis**
- If the user has been planning for >2 days without writing code → intervene
- Suggest: "What's the smallest thing you can build today to test this?"

**Scope creep during development**
- If the user adds "just one more feature" mid-build → remind them of the 1-week rule
- Suggest: "Add that to v2. Let's ship v1 first."

## Ongoing Product Advice

During development, help the user make decisions that favor:
- **Speed**: Hardcode > Configuration, Static > Dynamic, Simple > Flexible
- **Validation**: Ship broken > Perfect, Real users > Imagined users
- **Focus**: Core loop only > Nice-to-haves

When the user asks "Should I add X?", the default answer is: "Not for the MVP. Ship first, then let users tell you what they need."

## Resources

### references/prd-template.md
Complete PRD template with examples for different types of apps (SaaS tool, marketplace, content platform).

### references/claude-code-prompts.md
Starter prompt patterns for Claude Code, including common architectural decisions and tech stack setup.

### assets/nextjs-supabase-starter/
Basic Next.js + Supabase boilerplate with authentication optional, basic styling, and deployment config. Copy this to give users a running start.
