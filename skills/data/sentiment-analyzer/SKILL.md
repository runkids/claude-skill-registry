---
name: sentiment-analyzer
description: Analyze emotional tone, sentiment polarity, and psychological impact of text. Execute Python script for detailed sentiment analysis. Use when analyzing mood, attitude, or emotional content.
---

# Sentiment Analyzer

I analyze the emotional tone and psychological impact of text.

## How to Use This Skill

When analyzing emotional content, execute the sentiment analyzer script:

```bash
python /home/ywatanabe/dev/agent-patterns/.claude/skills/sentiment-analyzer/run.py "text to analyze"
```

The script returns JSON results with sentiment scores, detected tones, and emotional themes.

## What I Analyze

### Sentiment Dimensions
- **Polarity**: Positive, negative, neutral, mixed
- **Intensity**: Strength of emotion (mild, moderate, strong)
- **Subjectivity**: Objective facts vs. subjective opinions
- **Emotional Tone**: Joy, anger, sadness, fear, surprise, disgust, trust

### Psychological Aspects
- **Voice & Attitude**: Authoritative, friendly, aggressive, passive
- **Persuasion Techniques**: Appeals to emotion, logic, credibility
- **Emotional Triggers**: Words/phrases that evoke strong feelings
- **Overall Mood**: Optimistic, pessimistic, neutral, balanced

### Audience Impact
- How text likely makes readers feel
- Potential emotional reactions
- Alignment with intended message
- Persuasiveness for target audience

## When This Skill Activates

Activate when user requests:
- "Analyze sentiment" or "check emotional tone"
- "How does this sound?" or "what's the mood?"
- "Is this too negative/positive?"
- "Analyze psychological impact"
- Any request about emotional aspects

## Analysis Process

1. **Identify Sentiment Markers**: Emotional words, phrases, punctuation
2. **Assess Polarity**: Overall positive/negative/neutral balance
3. **Measure Intensity**: Strength of emotional expression
4. **Detect Tone**: Dominant emotional characteristics
5. **Evaluate Impact**: Likely reader response

## Output Format

Provide structured sentiment report:

**Overall Sentiment**:
- Polarity: [Positive/Negative/Neutral/Mixed]
- Intensity: [Mild/Moderate/Strong]
- Dominant Emotion: [Primary emotional tone]

**Detailed Analysis**:
- Positive elements: [Specific examples]
- Negative elements: [Specific examples]
- Neutral/factual elements: [Specific examples]

**Emotional Triggers**:
- Powerful phrases and their emotional impact
- Words that evoke strong feelings

**Tone Characteristics**:
- Voice: [Authoritative/Friendly/Casual/Formal]
- Attitude: [Optimistic/Pessimistic/Balanced]
- Subjectivity: [Highly subjective/Mostly objective]

**Audience Impact**:
- Likely reader emotions
- Persuasiveness assessment
- Alignment with intent

## Example Analysis

**Input**: "Our revolutionary product absolutely transforms your workflow! Say goodbye to tedious manual tasks forever. You'll wonder how you ever managed without it."

**Output**:
```
Overall Sentiment:
- Polarity: Strongly Positive
- Intensity: Strong
- Dominant Emotion: Excitement / Enthusiasm

Detailed Analysis:
Positive Elements:
- "revolutionary" - innovation, breakthrough
- "absolutely transforms" - powerful change
- "forever" - permanence, reliability

Emotional Triggers:
- "Say goodbye to tedious manual tasks" - relief from pain point
- "You'll wonder how you ever managed" - creates FOMO

Tone Characteristics:
- Voice: Marketing/promotional, enthusiastic
- Attitude: Very optimistic, confident
- Subjectivity: Highly subjective with strong claims

Audience Impact:
- Likely creates excitement and curiosity
- May feel overly promotional to skeptical readers
- Effective for marketing-receptive audience
- Consider toning down for professional/technical audiences
```

## Tone

- Objective and analytical
- Psychologically informed
- Balanced perspective
- Contextual awareness
