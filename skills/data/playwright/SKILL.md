---
name: playwright
description: Browser automation with Playwright MCP. Test pages, fill forms, take screenshots, check responsive design, validate UX, test login flows. Use when user wants to test websites or automate browser interactions.
---

# Playwright Browser Automation (MCP)

Browser automation via Playwright MCP server for testing and automation.

## Available Tools

- `browser_navigate` - Navigate to URL
- `browser_snapshot` - Get page accessibility snapshot with element refs
- `browser_take_screenshot` - Capture screenshot
- `browser_click` - Click element by ref
- `browser_type` - Type text (appends to existing)
- `browser_fill` - Fill input (clears first, then types)
- `browser_wait_for` - Wait for text or selector
- `browser_resize` - Resize viewport or emulate device

## Workflow

1. **Navigate** to the target URL using `browser_navigate`
2. **Snapshot** to see page structure and element refs using `browser_snapshot`
3. **Interact** using element refs from snapshot (`browser_click`, `browser_fill`)
4. **Screenshot** to capture results using `browser_take_screenshot`

## Quick Start

```
# Navigate to page
skill_mcp(skill_name="playwright", tool_name="browser_navigate", arguments='{"url": "https://example.com"}')

# Get page structure with element refs
skill_mcp(skill_name="playwright", tool_name="browser_snapshot")

# Click element (use ref from snapshot)
skill_mcp(skill_name="playwright", tool_name="browser_click", arguments='{"element": "Submit button", "ref": "e123"}')

# Fill input field
skill_mcp(skill_name="playwright", tool_name="browser_fill", arguments='{"element": "Email", "ref": "e456", "text": "test@example.com"}')

# Take screenshot
skill_mcp(skill_name="playwright", tool_name="browser_take_screenshot", arguments='{"filename": "/tmp/result.png"}')
```

## Examples

### Test Responsive Design

```
# Navigate
skill_mcp(skill_name="playwright", tool_name="browser_navigate", arguments='{"url": "http://localhost:3000"}')

# Desktop
skill_mcp(skill_name="playwright", tool_name="browser_resize", arguments='{"width": 1920, "height": 1080}')
skill_mcp(skill_name="playwright", tool_name="browser_take_screenshot", arguments='{"filename": "/tmp/desktop.png"}')

# Mobile
skill_mcp(skill_name="playwright", tool_name="browser_resize", arguments='{"device": "iPhone 13"}')
skill_mcp(skill_name="playwright", tool_name="browser_take_screenshot", arguments='{"filename": "/tmp/mobile.png"}')
```

### Fill a Form

```
# Navigate to form
skill_mcp(skill_name="playwright", tool_name="browser_navigate", arguments='{"url": "http://localhost:3000/contact"}')

# Get element refs
skill_mcp(skill_name="playwright", tool_name="browser_snapshot")

# Fill fields (use refs from snapshot)
skill_mcp(skill_name="playwright", tool_name="browser_fill", arguments='{"element": "Name", "ref": "e12", "text": "John Doe"}')
skill_mcp(skill_name="playwright", tool_name="browser_fill", arguments='{"element": "Email", "ref": "e34", "text": "john@example.com"}')

# Submit
skill_mcp(skill_name="playwright", tool_name="browser_click", arguments='{"element": "Submit", "ref": "e56"}')

# Wait for confirmation
skill_mcp(skill_name="playwright", tool_name="browser_wait_for", arguments='{"text": "Thank you", "timeout": 5000}')
```

## Tips

- **Always snapshot first** to get element refs before interacting
- **Use descriptive element names** in click/fill for clarity
- **Save screenshots to /tmp** for easy access
- **Use device presets** for accurate mobile emulation
- **Chain wait_for** after navigation for dynamic pages

## Server Options

For advanced usage, modify `mcp.json`:

```json
{
  "playwright": {
    "command": "npx",
    "args": ["@playwright/mcp@latest", "--headless", "--browser=firefox"],
    "includeTools": ["browser_navigate", "browser_snapshot", "..."]
  }
}
```

Common options:

- `--headless` - Run without visible browser
- `--browser=chrome|firefox|webkit` - Choose browser
- `--device="iPhone 13"` - Emulate device

> **Note**: This skill loads 8 essential tools. For full 17+ tools (tabs, PDF, evaluate, drag), modify `mcp.json` to add more tools to `includeTools`.
