---
name: github
description: Automation of GitHub tasks using the gh CLI and REST API. Includes pagination strategies, payload construction, and rate limit management. Triggers: github, gh-cli, github-api, rate-limit, pagination, pull-request.
---

# GitHub API and CLI

## Overview
Managing GitHub at scale requires moving beyond the web UI to the `gh` CLI and the REST API. This skill focuses on high-efficiency operations like bulk querying with pagination and managing API quotas.

## When to Use
- **Bulk Operations**: Fetching all issues or PRs across a large repository.
- **CI/CD Automation**: Creating issues or comments programmatically.
- **Compliance/Auditing**: Checking rate limits or repository permissions.

## Decision Tree
1. Is it a standard task (e.g., creating a PR, checking issue status)? 
   - YES: Use `gh` CLI commands.
2. Do you need custom data fields or specific API endpoints? 
   - YES: Use `gh api` with `--jq`.
3. Are there more than 100 results? 
   - YES: Use `--paginate` and `--slurp`.

## Workflows

### 1. Bulk Querying with Pagination
1. Construct a `gh api` call to a list endpoint (e.g., `repos/{owner}/{repo}/issues`).
2. Add the `--paginate` flag to ensure all pages are fetched.
3. Use `--slurp` to group results and `--jq` to filter for specific fields like `.[] | {title, user: .user.login}`.

### 2. Automated Issue Creation
1. Run `gh auth login` to establish credentials.
2. Define the issue payload using `-f title="Bug Report"` and `-f body=@issue_template.md`.
3. Execute the POST request to `repos/{owner}/{repo}/issues` using the `gh` CLI.

### 3. Handling API Rate Limits
1. Query the rate limit status using `gh api rate_limit`.
2. Inspect the `X-RateLimit-Reset` header in response objects to determine when the quota refreshes.
3. Implement exponential backoff in scripts when a 403 Forbidden (rate limited) status is encountered.

## Non-Obvious Insights
- **Magic Type Conversion**: In the `gh` CLI, the `-F/--field` flag automatically converts literals like `true`, `false`, `null`, and integers to their JSON types.
- **User-Agent Requirement**: All direct REST API requests MUST include a valid `User-Agent` header, or GitHub will reject them.
- **Path Placeholders**: Using `{owner}`, `{repo}`, and `{branch}` in `gh api` arguments automatically pulls values from the local repository context.

## Evidence
- "In --paginate mode, all pages of results will sequentially be requested until there are no more pages..." - [gh CLI Docs](https://cli.github.com/manual/gh_api)
- "All API requests must include a valid User-Agent header... Requests with no User-Agent header will be rejected." - [GitHub Docs](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting)
- "Placeholder values {owner}, {repo}, and {branch} in the endpoint argument will get replaced with values from the repository..." - [gh CLI Docs](https://cli.github.com/manual/gh_api)

## Scripts
- `scripts/github_tool.py`: Python wrapper for rate limit checking and pagination.
- `scripts/github_tool.js`: Node.js script using the `gh` CLI for bulk querying.

## Dependencies
- `gh` (GitHub CLI)
- `jq` (Recommended for processing JSON outputs)

## References
- [references/README.md](references/README.md)