---
name: user-interview
description: Conduct structured user interviews for product research, requirements gathering, or feedback collection. Use when conducting interviews, gathering user feedback, or doing user research.
---

# User Interview Skill

## Overview
Conduct effective user interviews to gather insights, validate assumptions, and understand user needs through structured questioning and active listening.

## Quick Start
When conducting an interview:
1. Prepare interview guide based on research goals
2. Start with warm-up questions
3. Use open-ended questions
4. Practice active listening
5. Document insights systematically

## Interview Structure

### Pre-Interview Setup
```markdown
## Interview Preparation Checklist
- [ ] Define research objectives
- [ ] Create interview guide
- [ ] Prepare consent forms if needed
- [ ] Test recording equipment
- [ ] Review participant background
- [ ] Prepare backup questions
```

### Interview Guide Template

#### Opening (5 minutes)
```markdown
1. Introduction and rapport building
   - Thank participant for their time
   - Explain interview purpose
   - Confirm recording permission
   - Set expectations (duration, topics)

2. Warm-up questions
   - "Tell me a bit about yourself and your role"
   - "How long have you been [relevant context]?"
   - "What does a typical day look like for you?"
```

#### Core Questions (30-40 minutes)

##### Understanding Current State
```markdown
## Current Workflow/Experience
- "Walk me through how you currently [specific task]"
- "What tools do you use for [activity]?"
- "How often do you [perform this task]?"
- "Who else is involved in this process?"

## Pain Points Discovery
- "What's the most frustrating part about [current solution]?"
- "Tell me about a time when [process] didn't work as expected"
- "If you had a magic wand, what would you change?"
- "What workarounds have you created?"
```

##### Exploring Needs
```markdown
## Uncovering Requirements
- "What would make [task] easier for you?"
- "How would you know if [solution] was successful?"
- "What's most important to you when [doing task]?"
- "What would prevent you from using [proposed solution]?"

## Priority Assessment
- "On a scale of 1-10, how important is [feature]?"
- "If you could only have three improvements, what would they be?"
- "What would you trade off to get [desired feature]?"
```

#### Closing (5 minutes)
```markdown
1. Final thoughts
   - "Is there anything else you'd like to share?"
   - "What haven't I asked that I should have?"

2. Next steps
   - Explain what happens with the feedback
   - Provide contact for follow-up questions
   - Thank participant again
```

## Question Techniques

### Open-Ended Questions
Transform closed questions into open ones:
- ❌ "Do you like the current system?"
- ✅ "How do you feel about the current system?"

- ❌ "Is this feature useful?"
- ✅ "How might you use this feature?"

### The 5 Whys
Dig deeper into root causes:
```
User: "I don't use the reporting feature"
Q1: Why don't you use it?
A1: "It's too complicated"
Q2: Why is it complicated?
A2: "Too many options I don't understand"
Q3: Why don't you understand them?
A3: "They use technical jargon"
Q4: Why is that a problem?
A4: "I need to ask IT for help each time"
Q5: Why do you need IT help?
A5: "I'm afraid I'll break something"
→ Root cause: Fear of making mistakes due to unclear UI
```

### Follow-Up Prompts
- "Tell me more about that..."
- "Can you give me an example?"
- "What happened next?"
- "How did that make you feel?"
- "Why is that important to you?"

## Active Listening Techniques

### Verbal Cues
- "Mm-hmm", "I see", "Interesting"
- Paraphrase: "So what I'm hearing is..."
- Summarize: "Let me make sure I understand..."
- Clarify: "When you say X, do you mean..."

### Non-Verbal Cues
- Maintain appropriate silence
- Allow thinking time
- Don't interrupt
- Show engagement through body language

## Documentation Methods

### Real-Time Notes Template
```markdown
# Interview Notes - [Participant ID] - [Date]

## Participant Info
- Role:
- Experience:
- Context:

## Key Insights
### Pain Points
1. [Issue]: "[Quote]"
   - Impact:
   - Frequency:
   - Current workaround:

### Needs/Desires
1. [Need]: "[Quote]"
   - Priority: High/Medium/Low
   - Use case:

### Surprises/Unexpected
- [Observation]: "[Quote]"

## Action Items
- [ ] Follow up on [topic]
- [ ] Research [mentioned tool/process]
- [ ] Share [requested information]
```

### Post-Interview Processing
```python
# scripts/process_interview.py
def process_interview_notes(transcript_file: str):
    """Extract insights from interview transcript."""

    insights = {
        "pain_points": [],
        "needs": [],
        "quotes": [],
        "themes": []
    }

    # Parse transcript
    with open(transcript_file, 'r') as f:
        content = f.read()

    # Extract key quotes (marked with quotation marks)
    import re
    quotes = re.findall(r'"([^"]+)"', content)
    insights["quotes"] = quotes

    # Identify pain point indicators
    pain_indicators = ["frustrat", "difficult", "problem", "issue", "struggle", "annoying", "waste"]
    for indicator in pain_indicators:
        if indicator in content.lower():
            # Extract surrounding context
            # Add to pain_points

    # Identify needs/wants
    need_indicators = ["wish", "would like", "need", "want", "hope", "if only", "should"]
    # Similar extraction logic

    return insights
```

## Interview Analysis

### Affinity Mapping
```markdown
## Affinity Map Structure

### Theme 1: [Workflow Efficiency]
- P1: "Switching between tools wastes 30% of my time"
- P3: "I have 5 different logins just to complete one task"
- P5: "Integration would save hours weekly"

### Theme 2: [Learning Curve]
- P2: "Training new team members takes weeks"
- P4: "Documentation is scattered everywhere"
- P6: "No one knows all the features"

### Theme 3: [Communication Gaps]
- P1: "I don't know what other teams are working on"
- P3: "Updates get lost in email"
- P5: "We duplicate work constantly"
```

### Persona Development
```markdown
## Persona: [Efficient Emily]

### Demographics
- Role: Project Manager
- Experience: 5 years
- Tech comfort: Moderate
- Team size: 8-10 people

### Goals
1. Deliver projects on time
2. Keep team aligned
3. Minimize administrative work

### Frustrations
1. Tool fragmentation
2. Manual status updates
3. Lack of visibility

### Quote
"I spend more time updating spreadsheets than actually managing projects"

### Needs
- Automated reporting
- Single source of truth
- Real-time collaboration
```

## Common Interview Mistakes to Avoid

### Leading Questions
- ❌ "Don't you think this feature would be helpful?"
- ✅ "How would you approach this situation?"

### Assumptive Questions
- ❌ "When you use our competitor's product..."
- ✅ "What solutions have you tried for this?"

### Multiple Questions
- ❌ "How often do you use this, and why, and what features do you like?"
- ✅ Ask one question at a time

### Solution-Focused Too Early
- ❌ Starting with "Would you use a tool that..."
- ✅ First understand the problem space

## Interview Synthesis

### Insights Report Template
```markdown
# User Interview Insights Report

## Executive Summary
- Participants: [number]
- Date range: [dates]
- Key finding: [one sentence]

## Methodology
- Interview type: [structured/semi-structured]
- Duration: [average time]
- Participant criteria: [selection criteria]

## Key Findings

### Finding 1: [Title]
**Evidence**: Mentioned by 7/10 participants
**Quote**: "Most representative quote"
**Implication**: What this means for the product
**Recommendation**: Suggested action

### Finding 2: [Title]
[Similar structure]

## Themes
1. **[Theme]**: [Description] ([X] participants)
2. **[Theme]**: [Description] ([X] participants)

## Recommendations
### High Priority
1. [Action based on strong evidence]

### Medium Priority
1. [Action based on moderate evidence]

### Future Exploration
1. [Areas needing more research]

## Appendix
- Interview guide
- Participant demographics
- Raw notes available at: [location]
```

## Bundled Resources
- `templates/interview_guide.md`: Customizable interview template
- `templates/consent_form.md`: Interview consent template
- `scripts/process_interview.py`: Transcript analysis tool
- `scripts/synthesize.py`: Multi-interview synthesis
- `examples/`: Sample interviews and insights