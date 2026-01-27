---
name: pipeline-monitor
description: Track build success rates and identify flaky tests from CI logs
disable-model-invocation: false
---

# CI/CD Pipeline Monitor

I'll analyze your CI/CD pipeline metrics, track build success rates, identify flaky tests, and provide performance trend analysis.

Arguments: `$ARGUMENTS` - pipeline platform (github, gitlab, circle), time range, or specific build numbers

## Monitoring Philosophy

- **Data-Driven Insights**: Identify trends, not just failures
- **Flaky Test Detection**: Find tests that fail inconsistently
- **Performance Tracking**: Monitor build duration over time
- **Success Rate Metrics**: Track reliability trends
- **Multi-Platform**: Support GitHub Actions, GitLab CI, CircleCI, Jenkins

**Token Optimization:**
- Platform detection via bash (200 tokens)
- CI log parsing with grep (500 tokens)
- Statistical analysis without file reading
- Expected: 2,000-3,500 tokens

## Phase 1: Pipeline Detection

First, I'll detect your CI/CD platform:

```bash
#!/bin/bash
# Detect CI/CD platform and configuration

detect_ci_platform() {
    echo "=== CI/CD Platform Detection ==="
    echo ""

    CI_PLATFORM=""
    CI_CONFIG=""

    # GitHub Actions
    if [ -d ".github/workflows" ]; then
        CI_PLATFORM="github-actions"
        CI_CONFIG=$(find .github/workflows -name "*.yml" -o -name "*.yaml" | head -1)
        echo "✓ Detected: GitHub Actions"
        echo "  Config: $CI_CONFIG"

    # GitLab CI
    elif [ -f ".gitlab-ci.yml" ]; then
        CI_PLATFORM="gitlab-ci"
        CI_CONFIG=".gitlab-ci.yml"
        echo "✓ Detected: GitLab CI"
        echo "  Config: $CI_CONFIG"

    # CircleCI
    elif [ -f ".circleci/config.yml" ]; then
        CI_PLATFORM="circleci"
        CI_CONFIG=".circleci/config.yml"
        echo "✓ Detected: CircleCI"
        echo "  Config: $CI_CONFIG"

    # Jenkins
    elif [ -f "Jenkinsfile" ]; then
        CI_PLATFORM="jenkins"
        CI_CONFIG="Jenkinsfile"
        echo "✓ Detected: Jenkins"
        echo "  Config: $CI_CONFIG"

    # Travis CI
    elif [ -f ".travis.yml" ]; then
        CI_PLATFORM="travis"
        CI_CONFIG=".travis.yml"
        echo "✓ Detected: Travis CI"
        echo "  Config: $CI_CONFIG"

    # Azure Pipelines
    elif [ -f "azure-pipelines.yml" ]; then
        CI_PLATFORM="azure-pipelines"
        CI_CONFIG="azure-pipelines.yml"
        echo "✓ Detected: Azure Pipelines"
        echo "  Config: $CI_CONFIG"

    else
        echo "⚠️  No CI/CD configuration detected"
        echo "Supported platforms: GitHub Actions, GitLab CI, CircleCI, Jenkins"
        exit 1
    fi

    echo ""
    echo "$CI_PLATFORM|$CI_CONFIG"
}

CI_INFO=$(detect_ci_platform)
CI_PLATFORM=$(echo "$CI_INFO" | cut -d'|' -f1)
CI_CONFIG=$(echo "$CI_INFO" | cut -d'|' -f2)
```

## Phase 2: Build History Analysis

<think>
When analyzing CI/CD pipelines:
- Build success rates reveal stability trends
- Flaky tests appear as intermittent failures
- Build duration increases indicate performance degradation
- Failed builds often cluster around specific changes
- Success rates vary by branch (main vs feature branches)
- Time-of-day patterns may indicate resource contention
</think>

I'll fetch and analyze recent build history:

```bash
#!/bin/bash
# Fetch build history from CI platform

fetch_build_history() {
    local platform="$1"
    local limit="${2:-50}"

    echo "=== Fetching Build History ==="
    echo ""

    case "$platform" in
        github-actions)
            # Use GitHub CLI to fetch workflow runs
            if command -v gh &> /dev/null; then
                echo "Fetching last $limit GitHub Actions runs..."
                gh run list --limit "$limit" --json status,conclusion,name,createdAt,updatedAt,databaseId > /tmp/ci_builds.json

                # Parse and display summary
                TOTAL=$(jq length /tmp/ci_builds.json)
                SUCCESS=$(jq '[.[] | select(.conclusion=="success")] | length' /tmp/ci_builds.json)
                FAILURE=$(jq '[.[] | select(.conclusion=="failure")] | length' /tmp/ci_builds.json)
                SUCCESS_RATE=$(echo "scale=2; $SUCCESS * 100 / $TOTAL" | bc)

                echo "Total runs: $TOTAL"
                echo "Successful: $SUCCESS ($SUCCESS_RATE%)"
                echo "Failed: $FAILURE"
                echo "✓ Build history fetched"
            else
                echo "⚠️  gh CLI not installed. Install: https://cli.github.com/"
                exit 1
            fi
            ;;

        gitlab-ci)
            # Use GitLab CLI to fetch pipelines
            if command -v glab &> /dev/null; then
                echo "Fetching last $limit GitLab CI pipelines..."
                glab ci list --per-page "$limit" --output json > /tmp/ci_builds.json

                # Parse and display summary
                TOTAL=$(jq length /tmp/ci_builds.json)
                SUCCESS=$(jq '[.[] | select(.status=="success")] | length' /tmp/ci_builds.json)
                FAILURE=$(jq '[.[] | select(.status=="failed")] | length' /tmp/ci_builds.json)
                SUCCESS_RATE=$(echo "scale=2; $SUCCESS * 100 / $TOTAL" | bc)

                echo "Total pipelines: $TOTAL"
                echo "Successful: $SUCCESS ($SUCCESS_RATE%)"
                echo "Failed: $FAILURE"
                echo "✓ Build history fetched"
            else
                echo "⚠️  glab CLI not installed. Install: https://gitlab.com/gitlab-org/cli"
                exit 1
            fi
            ;;

        circleci)
            # Use CircleCI API
            if [ ! -z "$CIRCLE_TOKEN" ]; then
                echo "Fetching last $limit CircleCI builds..."
                PROJECT_SLUG=$(git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/')

                curl -s "https://circleci.com/api/v2/project/github/$PROJECT_SLUG/pipeline?limit=$limit" \
                    -H "Circle-Token: $CIRCLE_TOKEN" > /tmp/ci_builds.json

                echo "✓ Build history fetched"
            else
                echo "⚠️  CIRCLE_TOKEN not set. Set environment variable."
                exit 1
            fi
            ;;

        *)
            echo "⚠️  Build history fetching not implemented for $platform"
            echo "Manual analysis required"
            ;;
    esac

    echo ""
}

fetch_build_history "$CI_PLATFORM" 50
```

## Phase 3: Success Rate Analysis

I'll analyze build success trends over time:

```bash
#!/bin/bash
# Analyze build success rates and trends

analyze_success_rates() {
    echo "=== Success Rate Analysis ==="
    echo ""

    if [ ! -f "/tmp/ci_builds.json" ]; then
        echo "⚠️  No build data available"
        return
    fi

    # Overall statistics
    echo "Overall Statistics:"
    TOTAL=$(jq length /tmp/ci_builds.json)
    SUCCESS=$(jq '[.[] | select(.conclusion=="success" or .status=="success")] | length' /tmp/ci_builds.json)
    FAILURE=$(jq '[.[] | select(.conclusion=="failure" or .status=="failed")] | length' /tmp/ci_builds.json)
    IN_PROGRESS=$(jq '[.[] | select(.conclusion=="in_progress" or .status=="running")] | length' /tmp/ci_builds.json)

    SUCCESS_RATE=$(echo "scale=2; $SUCCESS * 100 / $TOTAL" | bc)

    echo "  Total builds: $TOTAL"
    echo "  Successful: $SUCCESS ($SUCCESS_RATE%)"
    echo "  Failed: $FAILURE"
    echo "  In progress: $IN_PROGRESS"
    echo ""

    # Trend analysis (last 10 vs previous 40)
    echo "Trend Analysis:"
    RECENT_SUCCESS=$(jq '[.[:10] | .[] | select(.conclusion=="success" or .status=="success")] | length' /tmp/ci_builds.json)
    RECENT_RATE=$(echo "scale=2; $RECENT_SUCCESS * 100 / 10" | bc)

    PREVIOUS_SUCCESS=$(jq '[.[10:] | .[] | select(.conclusion=="success" or .status=="success")] | length' /tmp/ci_builds.json)
    PREVIOUS_TOTAL=$((TOTAL - 10))
    PREVIOUS_RATE=$(echo "scale=2; $PREVIOUS_SUCCESS * 100 / $PREVIOUS_TOTAL" | bc)

    echo "  Last 10 builds: $RECENT_RATE%"
    echo "  Previous builds: $PREVIOUS_RATE%"

    TREND_DIFF=$(echo "scale=2; $RECENT_RATE - $PREVIOUS_RATE" | bc)
    if (( $(echo "$TREND_DIFF > 0" | bc -l) )); then
        echo "  Trend: ✓ Improving (+$TREND_DIFF%)"
    elif (( $(echo "$TREND_DIFF < 0" | bc -l) )); then
        echo "  Trend: ⚠️  Declining ($TREND_DIFF%)"
    else
        echo "  Trend: Stable"
    fi
    echo ""

    # Success rate by workflow/job
    echo "Success Rate by Workflow:"
    jq -r '.[] | "\(.name // "unknown")|\(.conclusion // .status)"' /tmp/ci_builds.json | \
        awk -F'|' '{workflows[$1]++; if($2=="success") success[$1]++}
                    END {for(w in workflows) printf "  %s: %.0f%% (%d/%d)\n", w, (success[w]/workflows[w])*100, success[w], workflows[w]}' | \
        sort -t: -k2 -n
    echo ""
}

analyze_success_rates
```

## Phase 4: Flaky Test Detection

I'll identify tests that fail inconsistently:

```bash
#!/bin/bash
# Detect flaky tests from CI logs

detect_flaky_tests() {
    echo "=== Flaky Test Detection ==="
    echo ""

    # Download recent failed build logs
    echo "Analyzing failed builds for test failures..."

    # Extract test failures from logs (GitHub Actions)
    if [ "$CI_PLATFORM" = "github-actions" ]; then
        # Get failed run IDs
        FAILED_RUNS=$(jq -r '.[] | select(.conclusion=="failure") | .databaseId' /tmp/ci_builds.json | head -20)

        # Track test failures across runs
        > /tmp/test_failures.txt

        for run_id in $FAILED_RUNS; do
            echo "Checking run $run_id..."

            # Download logs and extract test failures
            gh run view "$run_id" --log 2>/dev/null | \
                grep -E "(FAIL|FAILED|Error:|AssertionError|Test failed)" | \
                grep -oP '(test_\w+|it\(["\x27][^\)]+|describe\(["\x27][^\)]+)' >> /tmp/test_failures.txt || true
        done

        if [ -s /tmp/test_failures.txt ]; then
            echo ""
            echo "Test Failure Frequency:"

            # Count occurrences and identify flaky tests
            sort /tmp/test_failures.txt | uniq -c | sort -rn | head -20 | while read count test; do
                # Tests that fail sometimes (not always) are flaky
                TOTAL_RUNS=$(echo "$FAILED_RUNS" | wc -l)
                FAILURE_RATE=$(echo "scale=2; $count * 100 / $TOTAL_RUNS" | bc)

                if (( $(echo "$count > 1 && $FAILURE_RATE < 80" | bc -l) )); then
                    echo "  ⚠️  FLAKY: $test (failed $count/$TOTAL_RUNS times, $FAILURE_RATE%)"
                else
                    echo "  $test (failed $count times)"
                fi
            done

            echo ""
            echo "Recommendations:"
            echo "- Investigate flaky tests marked with ⚠️"
            echo "- Check for race conditions, timing dependencies"
            echo "- Review test isolation and cleanup"
            echo "- Consider retry logic or increased timeouts"
        else
            echo "✓ No test failures detected in recent runs"
        fi
    else
        echo "⚠️  Flaky test detection not yet implemented for $CI_PLATFORM"
        echo "Manual log analysis required"
    fi

    echo ""
}

detect_flaky_tests
```

## Phase 5: Performance Trend Analysis

I'll track build duration and performance:

```bash
#!/bin/bash
# Analyze build performance and duration trends

analyze_build_performance() {
    echo "=== Build Performance Analysis ==="
    echo ""

    if [ ! -f "/tmp/ci_builds.json" ]; then
        echo "⚠️  No build data available"
        return
    fi

    # Calculate build durations
    echo "Build Duration Statistics:"

    # Extract durations (GitHub Actions)
    if [ "$CI_PLATFORM" = "github-actions" ]; then
        jq -r '.[] | "\(.createdAt)|\(.updatedAt)"' /tmp/ci_builds.json | while IFS='|' read created updated; do
            if [ ! -z "$created" ] && [ ! -z "$updated" ]; then
                START=$(date -d "$created" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%S" "$created" +%s 2>/dev/null || echo 0)
                END=$(date -d "$updated" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%S" "$updated" +%s 2>/dev/null || echo 0)
                DURATION=$((END - START))
                echo $DURATION
            fi
        done > /tmp/build_durations.txt

        if [ -s /tmp/build_durations.txt ]; then
            # Calculate statistics
            AVG_DURATION=$(awk '{sum+=$1; count++} END {printf "%.0f", sum/count}' /tmp/build_durations.txt)
            MIN_DURATION=$(sort -n /tmp/build_durations.txt | head -1)
            MAX_DURATION=$(sort -n /tmp/build_durations.txt | tail -1)

            # Convert to human readable
            echo "  Average: $(($AVG_DURATION / 60))m $(($AVG_DURATION % 60))s"
            echo "  Fastest: $(($MIN_DURATION / 60))m $(($MIN_DURATION % 60))s"
            echo "  Slowest: $(($MAX_DURATION / 60))m $(($MAX_DURATION % 60))s"

            # Trend analysis
            RECENT_AVG=$(head -10 /tmp/build_durations.txt | awk '{sum+=$1; count++} END {printf "%.0f", sum/count}')
            PREVIOUS_AVG=$(tail -n +11 /tmp/build_durations.txt | awk '{sum+=$1; count++} END {printf "%.0f", sum/count}')

            echo ""
            echo "Performance Trend:"
            echo "  Last 10 builds: $(($RECENT_AVG / 60))m $(($RECENT_AVG % 60))s"
            echo "  Previous builds: $(($PREVIOUS_AVG / 60))m $(($PREVIOUS_AVG % 60))s"

            DIFF=$((RECENT_AVG - PREVIOUS_AVG))
            if [ $DIFF -gt 30 ]; then
                echo "  Trend: ⚠️  Slowing down (+$(($DIFF / 60))m $(($DIFF % 60))s)"
                echo ""
                echo "  Recommendations:"
                echo "  - Review recently added dependencies"
                echo "  - Check for increased test count"
                echo "  - Consider caching strategies"
                echo "  - Profile slow steps"
            elif [ $DIFF -lt -30 ]; then
                echo "  Trend: ✓ Improving (-$((-$DIFF / 60))m $((-$DIFF % 60))s)"
            else
                echo "  Trend: Stable"
            fi
        fi
    fi

    echo ""
}

analyze_build_performance
```

## Phase 6: Failure Pattern Analysis

I'll identify common failure patterns:

```bash
#!/bin/bash
# Analyze failure patterns and root causes

analyze_failure_patterns() {
    echo "=== Failure Pattern Analysis ==="
    echo ""

    if [ ! -f "/tmp/ci_builds.json" ]; then
        echo "⚠️  No build data available"
        return
    fi

    FAILED_COUNT=$(jq '[.[] | select(.conclusion=="failure" or .status=="failed")] | length' /tmp/ci_builds.json)

    if [ $FAILED_COUNT -eq 0 ]; then
        echo "✓ No recent failures detected"
        echo ""
        return
    fi

    echo "Analyzing $FAILED_COUNT failed builds..."

    # Common failure categories
    > /tmp/failure_categories.txt

    # Get failed run IDs and analyze logs
    FAILED_RUNS=$(jq -r '.[] | select(.conclusion=="failure" or .status=="failed") | .databaseId // .id' /tmp/ci_builds.json | head -10)

    for run_id in $FAILED_RUNS; do
        if [ "$CI_PLATFORM" = "github-actions" ]; then
            gh run view "$run_id" --log 2>/dev/null | while read line; do
                # Categorize failures
                if echo "$line" | grep -qi "timeout\|timed out"; then
                    echo "timeout" >> /tmp/failure_categories.txt
                elif echo "$line" | grep -qi "out of memory\|oom"; then
                    echo "memory" >> /tmp/failure_categories.txt
                elif echo "$line" | grep -qi "network error\|connection refused\|ECONNREFUSED"; then
                    echo "network" >> /tmp/failure_categories.txt
                elif echo "$line" | grep -qi "npm ERR\|pip error\|cargo error"; then
                    echo "dependency" >> /tmp/failure_categories.txt
                elif echo "$line" | grep -qi "test.*fail\|assertion"; then
                    echo "test" >> /tmp/failure_categories.txt
                elif echo "$line" | grep -qi "lint\|format"; then
                    echo "lint" >> /tmp/failure_categories.txt
                fi
            done
        fi
    done

    if [ -s /tmp/failure_categories.txt ]; then
        echo ""
        echo "Failure Categories:"
        sort /tmp/failure_categories.txt | uniq -c | sort -rn | while read count category; do
            case "$category" in
                timeout)
                    echo "  ⏱️  Timeout issues: $count occurrences"
                    echo "     → Consider increasing timeout limits"
                    ;;
                memory)
                    echo "  💾 Memory issues: $count occurrences"
                    echo "     → Review memory-intensive operations"
                    ;;
                network)
                    echo "  🌐 Network issues: $count occurrences"
                    echo "     → Add retry logic for network calls"
                    ;;
                dependency)
                    echo "  📦 Dependency issues: $count occurrences"
                    echo "     → Lock dependency versions"
                    ;;
                test)
                    echo "  🧪 Test failures: $count occurrences"
                    echo "     → Review test stability"
                    ;;
                lint)
                    echo "  ✨ Lint/format issues: $count occurrences"
                    echo "     → Run linter before commit"
                    ;;
            esac
        done
    fi

    echo ""
}

analyze_failure_patterns
```

## Phase 7: Comprehensive Report

I'll generate a comprehensive monitoring report:

```bash
#!/bin/bash
# Generate comprehensive pipeline monitoring report

generate_monitoring_report() {
    echo "========================================"
    echo "CI/CD PIPELINE MONITORING REPORT"
    echo "========================================"
    echo ""
    echo "Generated: $(date)"
    echo "Platform: $CI_PLATFORM"
    echo "Analysis Period: Last 50 builds"
    echo ""

    # Summary from previous analyses
    if [ -f "/tmp/ci_builds.json" ]; then
        TOTAL=$(jq length /tmp/ci_builds.json)
        SUCCESS=$(jq '[.[] | select(.conclusion=="success" or .status=="success")] | length' /tmp/ci_builds.json)
        FAILURE=$(jq '[.[] | select(.conclusion=="failure" or .status=="failed")] | length' /tmp/ci_builds.json)
        SUCCESS_RATE=$(echo "scale=2; $SUCCESS * 100 / $TOTAL" | bc)

        echo "HEALTH SCORE: $SUCCESS_RATE%"

        if (( $(echo "$SUCCESS_RATE >= 90" | bc -l) )); then
            echo "Status: ✓ HEALTHY"
        elif (( $(echo "$SUCCESS_RATE >= 70" | bc -l) )); then
            echo "Status: ⚠️  NEEDS ATTENTION"
        else
            echo "Status: ❌ CRITICAL"
        fi

        echo ""
        echo "KEY METRICS:"
        echo "  Success rate: $SUCCESS_RATE%"
        echo "  Total builds: $TOTAL"
        echo "  Failed builds: $FAILURE"

        if [ -f "/tmp/build_durations.txt" ]; then
            AVG_DURATION=$(awk '{sum+=$1; count++} END {printf "%.0f", sum/count}' /tmp/build_durations.txt)
            echo "  Avg duration: $(($AVG_DURATION / 60))m $(($AVG_DURATION % 60))s"
        fi

        echo ""
        echo "RECOMMENDATIONS:"

        if [ $FAILURE -gt $((TOTAL / 4)) ]; then
            echo "  ⚠️  High failure rate - investigate failing builds"
        fi

        if [ -f "/tmp/test_failures.txt" ] && [ -s "/tmp/test_failures.txt" ]; then
            FLAKY_COUNT=$(sort /tmp/test_failures.txt | uniq -c | awk '$1 > 1 && $1 < 15 {count++} END {print count+0}')
            if [ $FLAKY_COUNT -gt 0 ]; then
                echo "  ⚠️  $FLAKY_COUNT flaky tests detected - see details above"
            fi
        fi

        echo ""
    fi

    echo "========================================"
}

generate_monitoring_report
```

## Integration with Other Skills

**Workflow Integration:**
- After failed builds → `/debug-systematic`
- Before releases → `/release-automation` (check build health)
- During development → `/test` (local testing)
- For CI setup → `/ci-setup`

**Skill Suggestions:**
- High failure rate → `/test-coverage`, `/test-antipatterns`
- Flaky tests found → `/test-async`
- Performance degradation → `/bundle-analyze`, `/lighthouse`

## Practical Examples

**Monitor default platform:**
```bash
/pipeline-monitor              # Auto-detect and analyze
```

**Specific platform:**
```bash
/pipeline-monitor github       # GitHub Actions
/pipeline-monitor gitlab       # GitLab CI
/pipeline-monitor circle       # CircleCI
```

**Custom time range:**
```bash
/pipeline-monitor --last 100   # Last 100 builds
/pipeline-monitor --days 7     # Last 7 days
```

**Focus on specific metrics:**
```bash
/pipeline-monitor --flaky      # Focus on flaky test detection
/pipeline-monitor --performance # Focus on performance trends
```

## What Gets Analyzed

**Metrics Tracked:**
- Build success/failure rates
- Build duration and trends
- Flaky test identification
- Failure pattern analysis
- Performance degradation
- Workflow-specific metrics

**Platforms Supported:**
- GitHub Actions (via gh CLI)
- GitLab CI (via glab CLI)
- CircleCI (via API with token)
- Jenkins (manual log analysis)
- Travis CI (basic support)
- Azure Pipelines (basic support)

## Safety Guarantees

**What I'll NEVER do:**
- Modify CI/CD configuration files
- Trigger builds or deployments
- Cancel running builds
- Delete build history
- Modify workflow settings

**What I WILL do:**
- Read-only analysis of build data
- Statistical trend analysis
- Actionable recommendations
- Clear reporting with context

## Credits

This skill integrates:
- **GitHub CLI** - GitHub Actions integration
- **GitLab CLI** - GitLab CI integration
- **CircleCI API** - CircleCI integration
- **Statistical Analysis** - Trend detection algorithms

## Token Budget

Target: 2,000-3,500 tokens per execution
- Phase 1-2: ~600 tokens (detection, fetch)
- Phase 3-4: ~800 tokens (success rates, flaky tests)
- Phase 5-6: ~800 tokens (performance, patterns)
- Phase 7: ~500 tokens (reporting)

**Optimization Strategy:**
- Platform detection via bash (no file reading)
- API/CLI calls for build data (minimal tokens)
- Statistical analysis without full log parsing
- Grep for specific error patterns
- Summary-based reporting

This ensures comprehensive pipeline monitoring while maintaining efficiency and token budget compliance.
