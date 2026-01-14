---
name: moodle-accessibility-audit
description: Accessibility auditing for Moodle following WCAG 2.1 AA and EN 301 549. Use when checking accessibility compliance, fixing accessibility issues, or implementing accessible UI patterns.
---

# Moodle Accessibility Audit

Ensure Moodle plugins meet WCAG 2.1 AA and EU accessibility requirements.

## When to Use This Skill

- Auditing plugin accessibility
- Fixing accessibility issues
- Implementing accessible forms
- ARIA attribute usage

See [reference.md](reference.md) for complete checklist.

## Quick Checks

### Forms
```html
<label for="username">Username</label>
<input type="text" id="username" name="username" aria-describedby="username-help">
<span id="username-help" class="form-text">Enter your login name</span>
```

### Images
```html
<img src="chart.png" alt="Sales chart showing 20% growth in Q4">
```

### Interactive Elements
```html
<button type="button" aria-expanded="false" aria-controls="menu-content">
    Menu
</button>
```

## Key Requirements

- **Color contrast**: 4.5:1 minimum for text
- **Focus visible**: All interactive elements
- **Keyboard navigation**: Tab order logical
- **Screen reader**: Meaningful labels
- **Touch targets**: 44×44px minimum
