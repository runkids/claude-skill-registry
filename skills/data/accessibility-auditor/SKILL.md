---
activation_code: ACCESSIBILITY_AUDITOR_V1
phase: [7, 9, 10]
version: 1.0.0
description: |
  Validates WCAG 2.1/2.2 accessibility compliance using automated testing
  and MCP browser tools for accessibility tree inspection.
---

# Accessibility Auditor Skill

## Activation Method

This skill activates when:
- UI components are ready for accessibility validation
- Integration testing requires a11y compliance check
- E2E validation includes accessibility assessment

Activation trigger: `[ACTIVATE:ACCESSIBILITY_AUDITOR_V1]`

## What This Skill Does

Automates accessibility compliance validation:

- **WCAG 2.1 AA compliance** checking (minimum requirement)
- **WCAG 2.2 AAA** checks for enhanced accessibility
- **Accessibility tree inspection** via MCP browser tools
- **Keyboard navigation** validation
- **Screen reader compatibility** assessment
- **Color contrast** analysis
- **Focus management** verification

## MCP Browser Tools Required

```yaml
required_tools:
  - browser_navigate: Navigate to pages for testing
  - browser_snapshot: Get accessibility tree (primary tool)
  - browser_press_key: Test keyboard navigation
  - browser_evaluate: Run axe-core in browser
  - browser_take_screenshot: Document accessibility issues
```

## Accessibility Tree Inspection

The `browser_snapshot` tool returns the accessibility tree, which provides:

- Element roles (button, link, heading, etc.)
- Accessible names and descriptions
- ARIA attributes
- Focus order
- Interactive element states

## Execution Flow

```
Stage 1: Automated Scanning
         - browser_navigate to each page
         - browser_evaluate to run axe-core
         - Collect WCAG violations

Stage 2: Accessibility Tree Analysis
         - browser_snapshot for each page
         - Analyze roles and names
         - Verify heading hierarchy
         - Check landmark regions

Stage 3: Keyboard Navigation Testing
         - browser_press_key (Tab) through page
         - Verify focus visibility
         - Test Enter/Space activation
         - Check escape key behavior

Stage 4: Color Contrast Validation
         - Extract color values
         - Calculate contrast ratios
         - Flag AA/AAA violations

Stage 5: Report Generation
         - Create accessibility audit report
         - Categorize by WCAG criteria
         - Prioritize by impact
```

## WCAG Criteria Checked

### Level A (Minimum)
- [ ] 1.1.1 Non-text Content (alt text)
- [ ] 1.3.1 Info and Relationships (semantic HTML)
- [ ] 1.4.1 Use of Color (not sole indicator)
- [ ] 2.1.1 Keyboard (all functionality)
- [ ] 2.4.1 Bypass Blocks (skip links)
- [ ] 3.1.1 Language of Page
- [ ] 4.1.1 Parsing (valid HTML)
- [ ] 4.1.2 Name, Role, Value (ARIA)

### Level AA (Required)
- [ ] 1.4.3 Contrast Minimum (4.5:1 text)
- [ ] 1.4.4 Resize Text (200% without loss)
- [ ] 1.4.10 Reflow (responsive without scroll)
- [ ] 2.4.6 Headings and Labels
- [ ] 2.4.7 Focus Visible
- [ ] 3.2.3 Consistent Navigation
- [ ] 3.2.4 Consistent Identification

### Level AAA (Enhanced)
- [ ] 1.4.6 Contrast Enhanced (7:1 text)
- [ ] 2.4.9 Link Purpose (link only)
- [ ] 2.4.10 Section Headings

## Integration with axe-core

```javascript
// Injected via browser_evaluate
const axe = require('axe-core');
const results = await axe.run(document, {
  runOnly: {
    type: 'tag',
    values: ['wcag2a', 'wcag2aa', 'wcag21aa']
  }
});
return results.violations;
```

## Keyboard Navigation Checklist

| Key | Expected Behavior |
|-----|-------------------|
| Tab | Move to next focusable element |
| Shift+Tab | Move to previous focusable element |
| Enter | Activate buttons and links |
| Space | Activate buttons, toggle checkboxes |
| Escape | Close modals, cancel operations |
| Arrow keys | Navigate within components (menus, tabs) |

## Output Report Format

```markdown
## Accessibility Audit Report

### Summary
- Total Issues: {count}
- Critical (A violations): {count}
- Serious (AA violations): {count}
- Moderate (AAA violations): {count}

### Critical Issues (Must Fix)

#### [A] Missing Alt Text
- **Location**: img.hero-image
- **Impact**: Screen readers cannot describe image
- **Fix**: Add descriptive alt attribute

#### [A] Keyboard Trap
- **Location**: .modal-dialog
- **Impact**: Users cannot escape modal with keyboard
- **Fix**: Add Escape key handler and focus trap

### Serious Issues (Should Fix)

#### [AA] Insufficient Contrast
- **Location**: .subtle-text
- **Ratio**: 3.2:1 (requires 4.5:1)
- **Fix**: Darken text color to #595959

### Recommendations
{Prioritized remediation steps}
```

## Output Signals

| Signal | Condition |
|--------|-----------|
| `ACCESSIBILITY_PASSED` | No A or AA violations |
| `ACCESSIBILITY_WARNING` | Only AAA violations |
| `ACCESSIBILITY_FAILED` | A or AA violations found |

## Human Gate

Critical accessibility issues trigger a human gate:

```
╔═══════════════════════════════════════════════════════════════════════╗
║  ACCESSIBILITY AUDIT: ISSUES FOUND                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  WCAG Level A Violations: 3 (CRITICAL)                                ║
║  WCAG Level AA Violations: 7 (SERIOUS)                                ║
║                                                                        ║
║  These issues MUST be resolved before deployment.                      ║
║                                                                        ║
║  View full report: .accessibility/audit-report.html                    ║
║                                                                        ║
║  [F] FIX ISSUES  [W] WAIVER (with justification)                      ║
╚═══════════════════════════════════════════════════════════════════════╝
```

## Integration Points

- **Phase 7 (TDD)**: Validate component accessibility during implementation
- **Phase 9 (Integration)**: Check page-level accessibility
- **Phase 10 (E2E)**: Final accessibility validation before production
