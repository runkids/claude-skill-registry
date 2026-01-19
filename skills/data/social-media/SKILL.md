---
name: social-media
description: Manages social media content creation and posting across LinkedIn, Twitter/X, Facebook, and Instagram. Use when creating posts, scheduling content, managing social media strategy, or analyzing engagement.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Social Media Skill

This skill provides comprehensive social media management for the Personal AI Employee, including content creation, scheduling, and cross-platform posting.

## Supported Platforms

| Platform | Max Length | Optimal Post Times | Key Features |
|----------|------------|-------------------|--------------|
| LinkedIn | 3000 chars | Tue-Thu, 9am-12pm | Professional, B2B, long-form |
| Twitter/X | 280 chars | Mon-Fri, 12pm-3pm | Concise, hashtags, threads |
| Facebook | 63,206 chars | Wed-Fri, 1pm-4pm | Community, engagement |
| Instagram | 2200 chars | Mon-Fri, 11am-1pm | Visual-first, hashtags |

## Content Types

1. **Thought Leadership** - Industry insights, expertise sharing
2. **Business Updates** - Announcements, milestones
3. **Engagement** - Questions, polls, discussions
4. **Promotional** - Products, services, offers
5. **Curated** - Sharing relevant third-party content

## Post Format

```markdown
---
type: social_post
platform: linkedin
status: draft
scheduled_time: 2026-01-08T10:00:00Z
campaign: [optional]
---

[Post content here]

**Hashtags**: #tag1 #tag2 #tag3

**Image**: [path or description]
```

## Content Strategy

### Weekly Mix
- 40% Educational/Value
- 30% Engagement
- 20% Promotional
- 10% Curated

## Reference

For platform-specific guidelines, see [reference.md](reference.md)

For post examples, see [examples.md](examples.md)
