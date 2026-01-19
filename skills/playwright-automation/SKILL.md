---
name: playwright
description: Browser automation using Playwright (Firefox, Chromium, WebKit). Supports ARM64 where Chrome doesn't work. Provides page navigation, content extraction, screenshots, and interactive actions.
metadata: {"clawdbot":{"emoji":"🎭","requires":{"bins":["python3"],"pip":["playwright"]}}}
---

# Playwright - Browser Automation

Browser automation using Playwright. Works on ARM64 with Firefox when Chrome isn't available.

## Setup

**Playwright is already installed:**
```bash
pip install playwright
python3 -m playwright install firefox  # Already done
```

## Commands

### Basic Operations
```bash
uv run {baseDir}/scripts/cli.py navigate "https://example.com"
uv run {baseDir}/scripts/cli.py content "https://example.com"
uv run {baseDir}/scripts/cli.py title "https://example.com"
```

### Screenshot
```bash
uv run {baseDir}/scripts/cli.py screenshot "https://example.com" --output /tmp/page.png
```

### Interactive Actions
```bash
uv run {baseDir}/scripts/cli.py click "https://example.com" --selector ".button"
uv run {baseDir}/scripts/cli.py type "https://example.com" --selector "#input" --text "hello"
uv run {baseDir}/scripts/cli.py scroll "https://example.com" --direction down
```

### Find Elements
```bash
uv run {baseDir}/scripts/cli.py find "https://example.com" --selector "a"
uv run {baseDir}/scripts/cli.py links "https://example.com"
```

### Multi-step Tasks
```bash
uv run {baseDir}/scripts/cli.py task "
1. Go to https://example.com
2. Click the 'More' link
3. Extract the title
"
```

### Full Page Snapshot
```bash
uv run {baseDir}/scripts/cli.py snapshot "https://example.com" --format ai
```

## Examples

### Research Task
```bash
# Get clean content from a page
uv run {baseDir}/scripts/cli.py content "https://github.com/MillionthOdin16/clawd-demo-site"

# Take a screenshot
uv run {baseDir}/scripts/cli.py screenshot "https://demo.bradarr.com" --output /tmp/demo.png
```

### Automation Script
```python
from playwright.async_api import async_playwright
import asyncio

async def run_task():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        page = await browser.new_page()
        
        # Navigate
        await page.goto("https://example.com")
        
        # Interact
        await page.click(".selector")
        await page.fill("#input", "text")
        
        # Extract
        title = await page.title()
        content = await page.content()
        
        await browser.close()
        return title, content

# Run the async function
asyncio.run(run_task())
```

## Why Playwright Over Chrome?

| Feature | Playwright (Firefox) | Chrome CDP |
|---------|---------------------|------------|
| ARM64 Support | ✅ Yes | ❌ No |
| Firefox | ✅ Works | ❌ Not supported |
| Chromium | ⚠️ Limited | ✅ Full |
| Screenshots | ✅ Yes | ✅ Yes |
| Multi-browser | ✅ 3 engines | Chrome only |

## When to Use

| Task | Tool | Why |
|------|------|-----|
| Simple content extraction | **r.jina.ai** (curl) | No browser needed, faster |
| Interactive/JavaScript pages | **playwright** | Renders JS, can click/type |
| Screenshots | **playwright** | Full page capture |
| Quick URL to markdown | **r.jina.ai** | `curl https://r.jina.ai/http://url` |

## See Also

- **Full workflow guide:** `memory/WORKFLOW.md` - Decision tree for when to use playwright vs r.jina.ai
- **Browser automation:** `memory/BROWSER-AUTOMATION.md` - Clawdbot browser vs browser-use vs playwright

## Notes

- Uses Firefox by default (works on ARM64)
- Headless mode for server environments
- Install other browsers: `python3 -m playwright install chromium webkit`
- For complex tasks, create a Python script

## Files

- `scripts/cli.py` - Main CLI tool
- `memory/PLAYWRIGHT-TASKS.md` - Task examples (create as needed)
