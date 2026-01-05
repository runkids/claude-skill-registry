---
name: readability-scorer
description: Assess text readability using multiple metrics. Execute Python script for detailed readability analysis. Use when evaluating text complexity, comprehension level, or audience fit.
---

# Readability Scorer

I assess how easy text is to read and understand for different audiences.

## How to Use This Skill

When analyzing text readability, execute the readability scorer script:

```bash
python /home/ywatanabe/dev/agent-patterns/.claude/skills/readability-scorer/run.py "text to analyze"
```

The script returns JSON results with readability scores, audience fit, and improvement suggestions.

## What I Measure

### Readability Metrics
- **Flesch Reading Ease**: 0-100 scale (higher = easier)
- **Flesch-Kincaid Grade Level**: U.S. school grade equivalent
- **Average Sentence Length**: Words per sentence
- **Average Word Length**: Syllables per word
- **Complex Words**: Percentage of 3+ syllable words

### Structural Analysis
- Sentence variety (simple, compound, complex)
- Paragraph length and structure
- Use of transition words
- Logical flow and organization

### Vocabulary Assessment
- Technical jargon usage
- Common vs. rare words
- Active vs. passive voice ratio
- Concrete vs. abstract language

### Audience Fit
- Recommended audience (general public, professionals, experts)
- Education level required
- Domain expertise needed

## When This Skill Activates

Activate when user requests:
- "Check readability" or "reading level"
- "Is this too complex/simple?"
- "What audience is this for?"
- "Simplify this text" or "make more accessible"
- Any request about comprehension difficulty

## Analysis Process

1. **Calculate Metrics**: Compute readability scores
2. **Analyze Structure**: Evaluate sentence and paragraph patterns
3. **Assess Vocabulary**: Identify complex/technical terms
4. **Determine Audience Fit**: Match to reader profiles
5. **Provide Recommendations**: Suggest improvements

## Output Format

Provide structured readability report:

**Readability Scores**:
- Flesch Reading Ease: [Score] ([Interpretation])
- Flesch-Kincaid Grade: [Level] ([Equivalent])
- Overall Assessment: [Very Easy/Easy/Moderate/Difficult/Very Difficult]

**Structural Analysis**:
- Average sentence length: [X words] ([Assessment])
- Sentence variety: [Good/Needs improvement]
- Paragraph structure: [Assessment]
- Logical flow: [Clear/Confusing]

**Vocabulary Analysis**:
- Complex words: [X%]
- Technical jargon: [Examples]
- Passive voice: [X%]
- Recommendations: [Specific suggestions]

**Audience Fit**:
- Best suited for: [Audience description]
- Education level: [Grade level or equivalent]
- Domain expertise: [None/Basic/Intermediate/Advanced]

**Improvement Suggestions**:
- Specific recommendations to improve readability
- Examples of simplifications

## Example Analysis

**Input**: "The implementation of our sophisticated algorithmic framework necessitates comprehensive documentation to facilitate subsequent modifications and enhancements."

**Output**:
```
Readability Scores:
- Flesch Reading Ease: 12 (Very Difficult)
- Flesch-Kincaid Grade: 18+ (College graduate level)
- Overall Assessment: Very Difficult

Structural Analysis:
- Average sentence length: 19 words (Long)
- Single complex sentence - needs variety
- Heavy noun stacking

Vocabulary Analysis:
- Complex words: 65%
- Technical jargon: "algorithmic framework"
- Passive voice: 0% (good)
- Unnecessarily complex: "implementation", "necessitates", "facilitate", "subsequent"

Audience Fit:
- Best suited for: Technical experts
- Education level: College graduate+
- Domain expertise: Advanced programming/CS

Improvement Suggestions:
1. Break into multiple sentences
2. Replace complex words:
   - "implementation" → "use"
   - "necessitates" → "requires" or "needs"
   - "facilitate" → "enable" or "help"
   - "subsequent" → "future" or "later"

Simplified version:
"Our algorithm framework needs good documentation. This will help us make changes and improvements later."

New scores:
- Flesch Reading Ease: 72 (Fairly Easy)
- Grade Level: 7th grade
```

## Tone

- Educational and constructive
- Data-driven
- Audience-aware
- Practical recommendations
