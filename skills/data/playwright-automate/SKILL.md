---
name: playwright-automate
description: Browser automation workflows with Playwright MCP integration
disable-model-invocation: true
---

# Playwright Browser Automation

I'll help you automate browser tasks using Playwright for testing, screenshots, PDFs, and workflow automation.

Arguments: `$ARGUMENTS` - automation task (screenshot, pdf, scrape, test) or specific URL/workflow

## Automation Capabilities

**Common Workflows:**
- Browser testing and validation
- Screenshot capture (full page, specific elements)
- PDF generation from web pages
- Web scraping and data extraction
- Form automation and submissions
- Performance monitoring

**Token Optimization:**
- Quick tool detection (100 tokens)
- Minimal file operations (300 tokens)
- Expected: 2,500-4,000 tokens

## Phase 1: Prerequisites Check

```bash
#!/bin/bash
# Check Playwright installation and setup

check_playwright() {
    echo "=== Playwright Setup Check ==="
    echo ""

    # Check for Playwright installation
    if [ -f "package.json" ]; then
        if grep -q "@playwright/test" package.json; then
            echo "✓ Playwright detected in package.json"
            PLAYWRIGHT_INSTALLED=true
        else
            echo "⚠️  Playwright not found in package.json"
            PLAYWRIGHT_INSTALLED=false
        fi
    else
        echo "⚠️  No package.json found"
        PLAYWRIGHT_INSTALLED=false
    fi

    # Check if Playwright CLI is available
    if command -v playwright &> /dev/null; then
        echo "✓ Playwright CLI available"
        playwright --version
    else
        echo "⚠️  Playwright CLI not in PATH"
    fi

    # Check for Playwright MCP server
    if [ -f "$HOME/.claude/config.json" ]; then
        if grep -q "playwright" "$HOME/.claude/config.json"; then
            echo "✓ Playwright MCP server configured"
            MCP_CONFIGURED=true
        else
            echo "⚠️  Playwright MCP server not configured"
            MCP_CONFIGURED=false
        fi
    fi

    echo ""

    # Offer installation if needed
    if [ "$PLAYWRIGHT_INSTALLED" = false ]; then
        echo "Would you like to install Playwright?"
        echo "  1. npm install --save-dev @playwright/test"
        echo "  2. npx playwright install"
        echo ""
    fi

    if [ "$MCP_CONFIGURED" = false ]; then
        echo "For MCP integration, run: /mcp-setup playwright"
        echo ""
    fi
}

check_playwright
```

## Phase 2: Automation Type Detection

Based on your request, I'll determine the automation workflow:

```bash
#!/bin/bash
# Parse automation request

parse_automation_request() {
    local args="$1"

    case "$args" in
        *screenshot*|*capture*|*snap*)
            TASK="screenshot"
            ;;
        *pdf*|*print*|*save*)
            TASK="pdf"
            ;;
        *scrape*|*extract*|*data*)
            TASK="scrape"
            ;;
        *test*|*e2e*|*verify*)
            TASK="test"
            ;;
        *form*|*submit*|*fill*)
            TASK="form"
            ;;
        *monitor*|*performance*|*perf*)
            TASK="performance"
            ;;
        *)
            TASK="interactive"
            ;;
    esac

    echo "Automation task: $TASK"
}

parse_automation_request "$ARGUMENTS"
```

## Phase 3: Screenshot Automation

Generate automated screenshot workflows:

```typescript
// scripts/playwright-screenshot.ts
import { chromium, FullConfig } from '@playwright/test';

async function captureScreenshots(config: ScreenshotConfig) {
  const browser = await chromium.launch({
    headless: true
  });

  const context = await browser.newContext({
    viewport: config.viewport || { width: 1920, height: 1080 }
  });

  const page = await context.newPage();

  try {
    // Navigate to URL
    await page.goto(config.url, { waitUntil: 'networkidle' });

    // Wait for specific element if provided
    if (config.waitForSelector) {
      await page.waitForSelector(config.waitForSelector, { timeout: 10000 });
    }

    // Capture full page screenshot
    if (config.fullPage) {
      await page.screenshot({
        path: config.outputPath || 'screenshot-full.png',
        fullPage: true
      });
      console.log(`✓ Full page screenshot saved: ${config.outputPath}`);
    }

    // Capture specific element
    if (config.elementSelector) {
      const element = page.locator(config.elementSelector);
      await element.screenshot({
        path: config.elementOutputPath || 'screenshot-element.png'
      });
      console.log(`✓ Element screenshot saved: ${config.elementOutputPath}`);
    }

    // Capture multiple viewports (responsive)
    if (config.responsive) {
      const viewports = [
        { name: 'mobile', width: 375, height: 667 },
        { name: 'tablet', width: 768, height: 1024 },
        { name: 'desktop', width: 1920, height: 1080 }
      ];

      for (const viewport of viewports) {
        await page.setViewportSize({ width: viewport.width, height: viewport.height });
        await page.screenshot({
          path: `screenshot-${viewport.name}.png`
        });
        console.log(`✓ ${viewport.name} screenshot saved`);
      }
    }

  } finally {
    await context.close();
    await browser.close();
  }
}

// Configuration interface
interface ScreenshotConfig {
  url: string;
  viewport?: { width: number; height: number };
  waitForSelector?: string;
  fullPage?: boolean;
  elementSelector?: string;
  outputPath?: string;
  elementOutputPath?: string;
  responsive?: boolean;
}

// Example usage
const config: ScreenshotConfig = {
  url: process.env.URL || 'http://localhost:3000',
  fullPage: true,
  responsive: true,
  outputPath: 'screenshots/homepage.png'
};

captureScreenshots(config).catch(console.error);
```

**Bash wrapper for easy execution:**

```bash
#!/bin/bash
# screenshot-automation.sh

screenshot_page() {
    local url="$1"
    local output="${2:-screenshot.png}"

    echo "Capturing screenshot of: $url"

    npx playwright screenshot \
        --browser chromium \
        --full-page \
        --output "$output" \
        "$url"

    if [ $? -eq 0 ]; then
        echo "✓ Screenshot saved: $output"
        echo "  Size: $(du -h "$output" | cut -f1)"
    else
        echo "❌ Screenshot failed"
        exit 1
    fi
}

# Multi-viewport capture
screenshot_responsive() {
    local url="$1"
    local base_name="${2:-screenshot}"

    echo "Capturing responsive screenshots..."

    # Mobile
    npx playwright screenshot \
        --browser chromium \
        --viewport-size 375,667 \
        --output "${base_name}-mobile.png" \
        "$url"

    # Tablet
    npx playwright screenshot \
        --browser chromium \
        --viewport-size 768,1024 \
        --output "${base_name}-tablet.png" \
        "$url"

    # Desktop
    npx playwright screenshot \
        --browser chromium \
        --viewport-size 1920,1080 \
        --full-page \
        --output "${base_name}-desktop.png" \
        "$url"

    echo "✓ Responsive screenshots complete"
    ls -lh ${base_name}-*.png
}

# Execute based on arguments
case "$1" in
    single)
        screenshot_page "$2" "$3"
        ;;
    responsive)
        screenshot_responsive "$2" "$3"
        ;;
    *)
        echo "Usage: $0 {single|responsive} <url> [output]"
        ;;
esac
```

## Phase 4: PDF Generation

Generate PDFs from web pages:

```typescript
// scripts/playwright-pdf.ts
import { chromium } from '@playwright/test';

async function generatePDF(config: PDFConfig) {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    await page.goto(config.url, { waitUntil: 'networkidle' });

    // Wait for dynamic content
    if (config.waitForSelector) {
      await page.waitForSelector(config.waitForSelector);
    }

    // Add delay for full rendering
    if (config.delayMs) {
      await page.waitForTimeout(config.delayMs);
    }

    // Generate PDF
    await page.pdf({
      path: config.outputPath || 'output.pdf',
      format: config.format || 'A4',
      printBackground: true,
      margin: config.margin || {
        top: '20px',
        right: '20px',
        bottom: '20px',
        left: '20px'
      },
      displayHeaderFooter: config.headerFooter || false,
      headerTemplate: config.headerTemplate,
      footerTemplate: config.footerTemplate
    });

    console.log(`✓ PDF generated: ${config.outputPath}`);

  } finally {
    await context.close();
    await browser.close();
  }
}

interface PDFConfig {
  url: string;
  outputPath?: string;
  format?: 'Letter' | 'Legal' | 'A4' | 'A3';
  waitForSelector?: string;
  delayMs?: number;
  margin?: { top: string; right: string; bottom: string; left: string };
  headerFooter?: boolean;
  headerTemplate?: string;
  footerTemplate?: string;
}

// CLI execution
const url = process.argv[2] || 'http://localhost:3000';
const output = process.argv[3] || 'output.pdf';

generatePDF({ url, outputPath: output }).catch(console.error);
```

## Phase 5: Web Scraping

Automated data extraction:

```typescript
// scripts/playwright-scrape.ts
import { chromium } from '@playwright/test';
import * as fs from 'fs';

async function scrapeData(config: ScrapeConfig) {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    await page.goto(config.url, { waitUntil: 'networkidle' });

    // Wait for content
    await page.waitForSelector(config.contentSelector, { timeout: 10000 });

    // Extract data
    const data = await page.evaluate((selectors) => {
      const results: any = {};

      Object.entries(selectors).forEach(([key, selector]) => {
        const elements = document.querySelectorAll(selector as string);
        results[key] = Array.from(elements).map(el => ({
          text: el.textContent?.trim(),
          html: el.innerHTML,
          attributes: Array.from(el.attributes).reduce((acc, attr) => {
            acc[attr.name] = attr.value;
            return acc;
          }, {} as Record<string, string>)
        }));
      });

      return results;
    }, config.selectors);

    // Save results
    const output = {
      url: config.url,
      timestamp: new Date().toISOString(),
      data
    };

    fs.writeFileSync(
      config.outputPath || 'scraped-data.json',
      JSON.stringify(output, null, 2)
    );

    console.log(`✓ Data scraped and saved: ${config.outputPath}`);
    console.log(`  Extracted ${Object.keys(data).length} data sets`);

  } finally {
    await context.close();
    await browser.close();
  }
}

interface ScrapeConfig {
  url: string;
  contentSelector: string;
  selectors: Record<string, string>;
  outputPath?: string;
}

// Example usage
const config: ScrapeConfig = {
  url: process.argv[2] || 'http://localhost:3000',
  contentSelector: 'main',
  selectors: {
    titles: 'h1, h2, h3',
    paragraphs: 'p',
    links: 'a[href]',
    images: 'img[src]'
  },
  outputPath: 'scraped-data.json'
};

scrapeData(config).catch(console.error);
```

## Phase 6: Form Automation

Automated form filling and submission:

```typescript
// scripts/playwright-form.ts
import { chromium } from '@playwright/test';

async function automateForm(config: FormConfig) {
  const browser = await chromium.launch({
    headless: config.headless !== false
  });

  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    await page.goto(config.url, { waitUntil: 'networkidle' });

    // Fill form fields
    for (const [selector, value] of Object.entries(config.fields)) {
      await page.fill(selector, String(value));
      console.log(`✓ Filled field: ${selector}`);
    }

    // Handle checkboxes
    if (config.checkboxes) {
      for (const selector of config.checkboxes) {
        await page.check(selector);
        console.log(`✓ Checked: ${selector}`);
      }
    }

    // Handle radio buttons
    if (config.radioButtons) {
      for (const selector of config.radioButtons) {
        await page.check(selector);
        console.log(`✓ Selected radio: ${selector}`);
      }
    }

    // Handle dropdowns
    if (config.selects) {
      for (const [selector, value] of Object.entries(config.selects)) {
        await page.selectOption(selector, value);
        console.log(`✓ Selected option: ${selector} = ${value}`);
      }
    }

    // Take screenshot before submit
    if (config.screenshotBeforeSubmit) {
      await page.screenshot({ path: 'form-before-submit.png' });
    }

    // Submit form
    if (config.submitSelector) {
      await page.click(config.submitSelector);
      await page.waitForLoadState('networkidle');
      console.log('✓ Form submitted');

      // Take screenshot after submit
      if (config.screenshotAfterSubmit) {
        await page.screenshot({ path: 'form-after-submit.png' });
      }

      // Verify success
      if (config.successSelector) {
        const success = await page.locator(config.successSelector).isVisible();
        if (success) {
          console.log('✓ Form submission successful');
        } else {
          console.log('⚠️  Success indicator not found');
        }
      }
    }

  } finally {
    await context.close();
    await browser.close();
  }
}

interface FormConfig {
  url: string;
  fields: Record<string, string | number>;
  checkboxes?: string[];
  radioButtons?: string[];
  selects?: Record<string, string>;
  submitSelector?: string;
  successSelector?: string;
  screenshotBeforeSubmit?: boolean;
  screenshotAfterSubmit?: boolean;
  headless?: boolean;
}

// Example
const config: FormConfig = {
  url: 'http://localhost:3000/contact',
  fields: {
    'input[name="name"]': 'Test User',
    'input[name="email"]': 'test@example.com',
    'textarea[name="message"]': 'This is an automated test message'
  },
  checkboxes: ['input[name="newsletter"]'],
  submitSelector: 'button[type="submit"]',
  successSelector: '.success-message',
  screenshotAfterSubmit: true
};

automateForm(config).catch(console.error);
```

## Phase 7: Performance Monitoring

Monitor page performance metrics:

```typescript
// scripts/playwright-performance.ts
import { chromium, devices } from '@playwright/test';

async function measurePerformance(url: string) {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext(devices['Desktop Chrome']);
  const page = await context.newPage();

  try {
    // Start performance monitoring
    await page.goto(url, { waitUntil: 'networkidle' });

    // Collect performance metrics
    const metrics = await page.evaluate(() => {
      const perfData = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
      const paintMetrics = performance.getEntriesByType('paint');

      return {
        dns: perfData.domainLookupEnd - perfData.domainLookupStart,
        tcp: perfData.connectEnd - perfData.connectStart,
        request: perfData.responseStart - perfData.requestStart,
        response: perfData.responseEnd - perfData.responseStart,
        dom: perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart,
        load: perfData.loadEventEnd - perfData.loadEventStart,
        total: perfData.loadEventEnd - perfData.fetchStart,
        firstPaint: paintMetrics.find(m => m.name === 'first-paint')?.startTime || 0,
        firstContentfulPaint: paintMetrics.find(m => m.name === 'first-contentful-paint')?.startTime || 0
      };
    });

    // Web Vitals
    const vitals = await page.evaluate(() => {
      return new Promise((resolve) => {
        let lcp = 0;
        let fid = 0;
        let cls = 0;

        // Largest Contentful Paint
        new PerformanceObserver((list) => {
          const entries = list.getEntries();
          const lastEntry = entries[entries.length - 1] as any;
          lcp = lastEntry.renderTime || lastEntry.loadTime;
        }).observe({ entryTypes: ['largest-contentful-paint'] });

        // Cumulative Layout Shift
        new PerformanceObserver((list) => {
          for (const entry of list.getEntries()) {
            if (!(entry as any).hadRecentInput) {
              cls += (entry as any).value;
            }
          }
        }).observe({ entryTypes: ['layout-shift'] });

        setTimeout(() => {
          resolve({ lcp, fid, cls });
        }, 5000);
      });
    });

    console.log('=== Performance Metrics ===');
    console.log('');
    console.log('Navigation Timing:');
    console.log(`  DNS Lookup:     ${metrics.dns.toFixed(2)}ms`);
    console.log(`  TCP Connect:    ${metrics.tcp.toFixed(2)}ms`);
    console.log(`  Request:        ${metrics.request.toFixed(2)}ms`);
    console.log(`  Response:       ${metrics.response.toFixed(2)}ms`);
    console.log(`  DOM Processing: ${metrics.dom.toFixed(2)}ms`);
    console.log(`  Load Event:     ${metrics.load.toFixed(2)}ms`);
    console.log(`  Total:          ${metrics.total.toFixed(2)}ms`);
    console.log('');
    console.log('Paint Metrics:');
    console.log(`  First Paint:              ${metrics.firstPaint.toFixed(2)}ms`);
    console.log(`  First Contentful Paint:   ${metrics.firstContentfulPaint.toFixed(2)}ms`);
    console.log('');
    console.log('Web Vitals:');
    console.log(`  LCP (Largest Contentful Paint): ${(vitals as any).lcp.toFixed(2)}ms`);
    console.log(`  CLS (Cumulative Layout Shift):  ${(vitals as any).cls.toFixed(4)}`);

    // Performance assessment
    console.log('');
    console.log('Assessment:');
    if (metrics.total < 3000) {
      console.log('  ✓ Excellent load time');
    } else if (metrics.total < 5000) {
      console.log('  ⚠️  Good load time, room for improvement');
    } else {
      console.log('  ❌ Slow load time, optimization needed');
    }

  } finally {
    await context.close();
    await browser.close();
  }
}

const url = process.argv[2] || 'http://localhost:3000';
measurePerformance(url).catch(console.error);
```

## Phase 8: Package Scripts

Add automation scripts to package.json:

```bash
#!/bin/bash
# Add Playwright automation scripts to package.json

add_automation_scripts() {
    echo "Add these scripts to your package.json:"
    echo ""
    cat << 'EOF'
  "scripts": {
    "playwright:screenshot": "ts-node scripts/playwright-screenshot.ts",
    "playwright:pdf": "ts-node scripts/playwright-pdf.ts",
    "playwright:scrape": "ts-node scripts/playwright-scrape.ts",
    "playwright:form": "ts-node scripts/playwright-form.ts",
    "playwright:perf": "ts-node scripts/playwright-performance.ts"
  }
EOF
    echo ""
}

add_automation_scripts
```

## Practical Examples

**Screenshot capture:**
```bash
/playwright-automate screenshot https://example.com
/playwright-automate screenshot --responsive --output screenshots/
```

**PDF generation:**
```bash
/playwright-automate pdf https://example.com/docs
/playwright-automate pdf --format A4 --output documentation.pdf
```

**Web scraping:**
```bash
/playwright-automate scrape https://example.com
/playwright-automate scrape --selector ".products" --output data.json
```

**Form automation:**
```bash
/playwright-automate form contact-form.config.json
/playwright-automate test-submission
```

**Performance monitoring:**
```bash
/playwright-automate performance https://example.com
```

## Best Practices

**Automation Guidelines:**
- ✅ Use explicit waits (waitForSelector, waitForLoadState)
- ✅ Handle errors gracefully with try-catch
- ✅ Set reasonable timeouts
- ✅ Clean up browser instances
- ✅ Respect robots.txt and rate limits (for scraping)

**Anti-Patterns:**
- ❌ Hard-coded delays (use waitFor instead)
- ❌ No error handling
- ❌ Ignoring GDPR/privacy concerns
- ❌ Excessive scraping requests

## Integration Points

- `/e2e-generate` - Generate E2E tests with Playwright
- `/test` - Run Playwright tests alongside unit tests
- `/mcp-setup` - Configure Playwright MCP server
- `/ci-setup` - Add Playwright automation to CI pipeline

## What I'll Actually Do

1. **Detect setup** - Check Playwright installation
2. **Understand task** - Determine automation type
3. **Generate scripts** - Create TypeScript automation code
4. **Execute safely** - Run with proper error handling
5. **Document results** - Provide clear output and logs

**Important:** I will NEVER:
- Scrape sites without respecting robots.txt
- Automate without rate limiting
- Ignore privacy and security concerns
- Add AI attribution

All browser automation will be safe, ethical, and well-documented.

**Credits:** Based on Playwright browser automation best practices and MCP Playwright server integration patterns.
