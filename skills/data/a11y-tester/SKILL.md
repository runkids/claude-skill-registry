---
name: a11y-tester
description: Run automated accessibility tests on URLs or HTML content using axe-core engine to WCAG 2.2 AA standards. Use this skill when users want to test website accessibility, find WCAG violations, audit pages for accessibility issues, check if sites are accessible, or analyze HTML for accessibility problems. Output can be raw violations or formatted issues (delegates to a11y-issue-writer). Triggers on requests like "test accessibility", "check for WCAG violations", "audit this URL", "is this page accessible", or "find accessibility issues".
---

# Accessibility Tester

Run automated accessibility testing using axe-core and output violations in raw format or as formatted issues.

## Prerequisites: Playwright MCP Setup

Before running accessibility tests, you need the Playwright MCP (Model Context Protocol) server configured in VS Code. This provides the browser automation tools needed to test web pages.

### Initial Setup (First-Time Users)

If you don't have Playwright MCP set up, follow these steps:

1. **Install the Playwright extension** (if not already installed):
   - Open Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`)
   - Search for and run: **Extensions: Install Extensions**
   - Search for "Playwright" and install the official extension

2. **Add the Playwright MCP server**:
   - Open Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`)
   - Run: **MCP: Browse MCP Servers**
   - Search for "Playwright" and add it
   
   **OR** manually add via:
   - Run: **MCP: Add Server...**
   - Follow prompts to add Playwright MCP

3. **Verify MCP access** (if needed):
   - Ensure **chat.mcp.access** setting allows MCP server access
   - Ensure **chat.mcp.autostart** is enabled for automatic startup

### Quick Check

To verify Playwright MCP is available, look for these tools in your chat context:
- `mcp_playwright_browser_navigate`
- `mcp_playwright_browser_evaluate`
- `mcp_playwright_browser_snapshot`

If these tools are not available, you need to complete the setup above.

## Output Options

This skill provides two output modes:

1. **Raw violations** - Return the axe-core violations array as JSON for programmatic use or further processing
2. **Formatted issues** - Delegate to the **a11y-issue-writer** skill to format violations as standardized, JIRA-ready issue reports

**When to use each:**
- **Raw violations**: When requested explicitly, for debugging, or when called by other skills (e.g., orchestrator)
- **Formatted issues**: When users request "write issues", "create tickets", or want actionable bug reports

**Note:** The a11y-issue-writer skill requires the accessibility-issues-template-mcp server. See the a11y-issue-writer skill documentation for details.

## Testing Workflow

1. **Navigate to URL**: Use `mcp_playwright_browser_navigate` to load the page
2. **Run axe-core**: Use `mcp_playwright_browser_evaluate` to inject and run axe-core
3. **Output results** - Choose based on request:
   - **Option A: Raw violations** - Return the violations array with summary statistics
   - **Option B: Formatted issues** - Delegate to **a11y-issue-writer** skill to format violations as standardized issue reports
4. **Present results**: Output a summary table followed by violations (raw) or formatted issues (via a11y-issue-writer)

## Expected Output Format

### Raw Violations Output

When outputting raw violations (not delegating to a11y-issue-writer), return:

```markdown
# Accessibility Test Results: [Site Name]

**URL Tested:** https://example.com  
**Date:** [Current Date]  
**Tool:** Axe-core 4.8.4 via Playwright  
**Browser:** Chromium  
**Operating System:** Windows

## Summary Statistics

| Metric | Count |
|--------|-------|
| **Violations** | X |
| **Passes** | X |
| **Incomplete** | X |
| **Inapplicable** | X |

## Violations

[Return the violations array as formatted JSON or summarized table]
```

This format is ideal for:
- Programmatic consumption by other skills
- Debugging test results
- Integration with CI/CD pipelines

### Formatted Issues Output

When delegating to **a11y-issue-writer** skill, follow this workflow:

1. Run axe-core and collect violations
2. Delegate to a11y-issue-writer: "Format these violations as standardized issue reports"
3. The a11y-issue-writer skill will output the full formatted issues

Present results in this order:

### 1. Report Header
```
# Accessibility Test Report: [Site Name]

**URL Tested:** https://example.com  
**Date:** [Current Date]  
**Tool:** Axe-core 4.8.4 via Playwright  
**Browser:** Chromium  
**Operating System:** Windows
```

### 2. Summary Tables
```
## Summary

| Metric | Count |
|--------|-------|
| **Total Violations** | X issues |
| **Rules Failed** | X |
| **Rules Passed** | X |
| **Needs Review** | X |

### Issues by Severity

| Severity | Count | WCAG Level |
|----------|-------|------------|
| **Critical** | X | A |
| **Severe** | X | AA |
| **Minor** | X | Best Practice |

### Issues by Type

| Rule ID | Description | Impact | Count |
|---------|-------------|--------|-------|
| `rule-id` | Description | Impact | X |
```

### 3. Formatted Issues
After the summary, output each issue using the full template format (see Issue Output Format below).

### 4. Recommendations Summary
```
## Recommendations Summary

| Priority | Action |
|----------|--------|
| **High** | Description of fix |
| **Low** | Description of fix |
```

## Step 1: Navigate to the Page

```
mcp_playwright_browser_navigate(url: "https://example.com")
```

## Step 2: Run Axe-core via Browser Evaluate

Use `mcp_playwright_browser_evaluate` with this function to inject axe-core and run the analysis:

```javascript
async () => {
  // Load axe-core if not already present
  if (typeof axe === 'undefined') {
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.8.4/axe.min.js';
    document.head.appendChild(script);
    await new Promise((resolve, reject) => {
      script.onload = resolve;
      script.onerror = reject;
    });
  }
  // Run axe and return results
  const results = await axe.run();
  return { 
    violations: results.violations, 
    passes: results.passes.length, 
    incomplete: results.incomplete.length 
  };
}
```

This returns JSON with a `violations` array for output or delegation.

## Step 3: Output Results

### Option A: Raw Violations

For raw output, present the violations array with summary statistics:

```json
{
  "violations": [
    {
      "id": "color-contrast",
      "impact": "serious",
      "tags": ["wcag2aa", "wcag143"],
      "description": "Ensures the contrast between foreground and background colors meets WCAG 2 AA contrast ratio thresholds",
      "help": "Elements must have sufficient color contrast",
      "helpUrl": "https://dequeuniversity.com/rules/axe/4.8/color-contrast",
      "nodes": [{ /* node data from axe */ }]
    }
  ],
  "passes": 42,
  "incomplete": 3,
  "inapplicable": 18
}
```

This is useful when:
- Called by the orchestrator skill that will process violations further
- User explicitly requests raw data
- Violations will be fed into another tool or script

### Option B: Formatted Issues (Delegate to a11y-issue-writer)

For formatted issue output, **delegate to the a11y-issue-writer skill**:

**Delegation workflow:**
1. Collect axe-core violations from Step 2
2. Pass violations to a11y-issue-writer: "Format these [X] violations as standardized accessibility issue reports"
3. Include context (URL, browser, OS) for the a11y-issue-writer to use
4. The a11y-issue-writer skill will:
   - Call `format_axe_violation` from the accessibility-issues-template-mcp
   - Output complete, JIRA-ready issue reports
   - Include all required sections (severity, steps to reproduce, code examples, etc.)

**Example delegation:**
```
"I found 5 violations. Delegating to a11y-issue-writer skill to format these as standardized issue reports:
- color-contrast (2 instances)
- label (1 instance) 
- button-name (2 instances)

Context: URL https://example.com, Browser: Chromium, OS: Windows"
```

The a11y-issue-writer skill handles all formatting, template retrieval, and validation.

**When to delegate:**
- User requests "write issues", "create tickets", or "format as JIRA"
- User wants actionable bug reports
- Output will go into an issue tracking system

**When to output raw violations:**
- Called by orchestrator skill (orchestrator decides next steps)
- User explicitly requests raw data
- Output will be consumed programmatically

See the **a11y-issue-writer** skill documentation for details on issue formatting and templates.

## Optional: Enrich Results with MCP Servers

After running axe-core tests, you can enrich results by querying accessibility MCP servers:

### WCAG Mapping (wcag-mcp)
```
wcag-mcp: get-criterion("4.1.2")
→ Returns full SC details, understanding docs, techniques
```

### Component Patterns (magentaa11y-mcp)
```
magentaa11y-mcp: get_web_component("button")
→ Returns acceptance criteria and developer notes
```

### User Impact (a11y-personas-mcp)
```
a11y-personas-mcp: get-personas(["blindness-screen-reader-nvda"])
→ Returns persona details showing who is affected
```

## Notes

- Use Playwright browser tools (`mcp_playwright_browser_navigate` + `mcp_playwright_browser_evaluate`) to run axe-core
- Axe-core is injected from CDN: `https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.8.4/axe.min.js`
- **Two output modes**: Raw violations (default) or formatted issues (via delegation to a11y-issue-writer)
- **Delegation model**: This skill runs tests and collects violations; a11y-issue-writer formats them as issues
- Axe-core catches ~30-40% of issues; combine with manual review of `mcp_playwright_browser_snapshot` for comprehensive testing
- **Always output a summary first**, then the violations/issues
- When delegating to a11y-issue-writer, provide complete context (URL, browser, OS, violations array)
