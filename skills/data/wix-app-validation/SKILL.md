---
name: wix-app-validation
description: "Validates Wix CLI applications are ready and working by running a sequential workflow of build, preview, and e2e tests using Playwright MCP. Use when testing app readiness, verifying runtime errors, checking UI rendering, or before releases. Triggers include validate, test, e2e, check, verify, ready, working, runtime errors, UI check, preview test, build test, smoke test."
---

# Wix App Validation

Validates Wix CLI applications through a four-step sequential workflow: package installation, build, preview, and e2e testing.

## Non-Matching Intents

Do NOT use this skill for:

- **Creating new extensions** → Use `wix-dashboard-page`, `wix-embedded-script`, etc.
- **Deploying to production** → This is for validation/testing only
- **Unit testing** → This skill performs e2e/integration testing

## Validation Workflow

Execute these steps sequentially. Stop and report errors if any step fails.

### Step 1: Package Installation

Ensure all dependencies are installed before proceeding with the build.

**Detect package manager:**
- Check for `package-lock.json` → use `npm`
- Check for `yarn.lock` → use `yarn`
- Check for `pnpm-lock.yaml` → use `pnpm`
- Default to `npm` if no lock file is found

**Run installation command:**

```bash
# For npm
npm install

# For yarn
yarn install

# For pnpm
pnpm install
```

**Success criteria:**
- Exit code 0
- All dependencies installed successfully
- No missing peer dependencies warnings (unless expected)
- `node_modules` directory exists and contains expected packages

**On failure:** Report the installation errors and stop validation. Common issues:
- Network connectivity problems
- Corrupted lock files
- Version conflicts
- Missing Node.js or package manager

### Step 2: Build Validation

Run the build command and check for compilation errors:

```bash
npx wix build
```

**Success criteria:**
- Exit code 0
- No TypeScript errors
- No missing dependencies

**On failure:** Report the specific compilation errors and stop validation.

### Step 3: Preview Deployment

Start the preview server:

```bash
npx wix preview
```

**Success criteria:**
- Preview server starts successfully
- Preview URLs are generated (both site and dashboard)

**URL extraction:** Parse the terminal output to find both preview URLs. Look for patterns like:
- Site preview: `Site preview: https://...` or `Site URL: https://...`
- Dashboard preview: `Dashboard preview: https://...` or `Preview URL: https://...` or `Your app is available at: https://...`

Extract both URLs as they will be used in Step 4 for testing.

**On failure:** Report the preview startup errors and stop validation.

### Step 4: E2E Testing with Playwright MCP

Once the preview URL is available, use Playwright MCP tools to validate the application.

See [Playwright MCP Reference](references/PLAYWRIGHT_MCP.md) for complete tool documentation.

#### 4.1 Test Site Preview and All Extensions

Test both the site preview and all dashboard page extensions. Parse the preview output to identify:
- **Site preview URL**: The main site URL (typically shown as "Site preview" or similar)
- **Dashboard preview URL**: The base URL for dashboard pages

**A. Test Site Preview**

1. **Navigate to the site preview URL:**
   ```
   Tool: playwright__browser-navigate
   Args: { "url": "<site-preview-url>" }
   ```

2. **Wait for the page to load completely** before proceeding to validation steps (4.2-4.6).

3. **Run validation steps 4.2-4.6** to validate the site preview.

**B. Test All Dashboard Page Extensions**

Discover all dashboard page extensions from `src/extensions.ts` and test each one. For each extension:

1. **Navigate to the extension URL:**
   - Base dashboard preview URL: `<dashboard-preview-url>`
   - Extension routePath: from `routePath` property in each extension definition
   - Full URL: `<dashboard-preview-url>/<routePath>`
   - Example: If dashboard preview URL is `https://preview.wix.com/...` and routePath is `"offers"`, navigate to `https://preview.wix.com/.../offers`

   ```
   Tool: playwright__browser-navigate
   Args: { "url": "<dashboard-preview-url>/<routePath>" }
   ```

2. **Wait for the page to load completely** before proceeding to validation steps (4.2-4.6).

3. **Run validation steps 4.2-4.6** for each extension to ensure all dashboard pages are validated.

**Common dashboard page extensions to test:**
- Root page (routePath: `""` or `"/"`)
- Dashboard pages with any routePath value
- Nested routes with multiple path segments

**Note:** Only test dashboard page extensions (`extensions.dashboardPage`). Skip data extensions and embedded scripts for this validation step.

#### 4.2 Check for Runtime Errors

```
Tool: playwright__browser-console-messages
Args: {}
```

**Check for:**
- `console.error` messages
- Uncaught exceptions
- Failed network requests
- React/framework errors

#### 4.3 Validate Backend API Calls

Check that all backend API calls are successful and not returning error status codes.

```
Tool: playwright__browser-network-requests
Args: {}
```

**Validate API responses:**
- Check all network requests for status codes
- **Critical failures:** Any 500 (Internal Server Error) responses from backend APIs
- **Warning:** 4xx responses (client errors) - note but may be expected in some cases
- **Success:** 200-299 status codes are acceptable
- Filter requests to only check API endpoints (typically `/api/` or backend service URLs)

**Check for:**
- No 500 errors from backend APIs
- No 502 (Bad Gateway) or 503 (Service Unavailable) errors
- Failed requests to Wix backend services
- Timeout errors on API calls

**On failure:** Report:
- Which API endpoint(s) failed
- HTTP status code(s) received
- Request URL and method
- Response body if available (may contain error details)

**Note:** This validation should be performed after the page has fully loaded and all API calls have completed. Wait for network activity to settle before checking.

#### 4.4 Capture Accessibility Snapshot

```
Tool: playwright__browser-snapshot
Args: {}
```

**Validate:**
- Expected UI elements are present
- Page structure is correct
- No broken or missing components

#### 4.5 Take Screenshot (Optional)

```
Tool: playwright__browser-take-screenshot
Args: { "fullPage": true }
```

Capture visual evidence of the rendered page state.

#### 4.6 Execute Custom Validations (If Needed)

```
Tool: playwright__browser-evaluate
Args: { "function": "() => { /* validation code */ }" }
```

Use for custom runtime checks like:
- Verifying specific DOM elements exist
- Checking application state
- Validating data loading

## Validation Report

After completing all steps, provide a summary:

**Pass:**
- Dependencies: ✓ All packages installed successfully
- Build: ✓ Compiled successfully
- Preview: ✓ Running at [URL]
- E2E: ✓ All previews tested successfully
  - Site Preview: ✓ No runtime errors, UI renders correctly, all API calls successful
  - Dashboard Extensions:
    - [Extension 1]: ✓ No runtime errors, UI renders correctly, all API calls successful
    - [Extension 2]: ✓ No runtime errors, UI renders correctly, all API calls successful
    - [Extension N]: ✓ No runtime errors, UI renders correctly, all API calls successful

**Fail:**
- Identify which step failed
- Identify which preview/extension(s) failed (if applicable)
- Provide specific error messages
- Suggest remediation steps

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Package installation fails | Missing lock file, network issues, or corrupted node_modules | Delete `node_modules` and lock file, then reinstall |
| Build fails with TS errors | Type mismatches | Fix TypeScript errors in source |
| Preview fails to start | Port conflict or config issue | Check `wix.config.json` |
| Console errors in preview | Runtime exceptions | Check browser console output |
| Backend API 500 errors | Server-side errors in API routes | Check API route handlers, server logs, and error handling |
| UI not rendering | Component errors | Review component code and imports |
