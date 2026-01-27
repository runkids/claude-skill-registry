---
name: performance-profile
description: Performance profiling and bottleneck detection for Node.js, Python, and browser apps
disable-model-invocation: false
---

# Performance Profiling & Bottleneck Detection

I'll profile your application to identify performance bottlenecks and provide optimization recommendations.

**Supported Environments:**
- Node.js profiling (--inspect, clinic.js)
- Browser performance (Chrome DevTools)
- Python profiling (cProfile, line_profiler)
- Bottleneck identification
- Memory leak detection
- Optimization recommendations

**Token Optimization:**
- Uses Grep for targeted file search (300-500 tokens)
- Reads only performance-critical files (1000-1500 tokens)
- Structured analysis framework (800-1200 tokens)
- Expected: 3,000-5,000 tokens total

**Arguments:** `$ARGUMENTS` - optional: `node|python|browser` or specific file/route to profile

## Extended Thinking for Performance Analysis

<think>
Performance profiling requires understanding:
- CPU-bound vs I/O-bound operations
- Synchronous vs asynchronous bottlenecks
- Memory allocation patterns
- Database query performance
- Network latency impacts
- Bundle size and loading performance

Complex scenarios:
- Multi-threaded applications
- Distributed systems
- Microservice latency
- Real-time applications
- Large dataset processing
- Memory leaks over time
</think>

## Phase 1: Environment Detection

I'll detect the runtime environment and available profiling tools:

```bash
#!/bin/bash
# Performance Profiling - Environment Detection

echo "=== Performance Profiling Setup ==="
echo ""

# Create profiling directory
mkdir -p .claude/profiling
PROFILE_DIR=".claude/profiling"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
REPORT="$PROFILE_DIR/profile-$TIMESTAMP.md"

detect_runtime() {
    local runtime=""

    # Check for Node.js
    if [ -f "package.json" ]; then
        if command -v node >/dev/null 2>&1; then
            runtime="nodejs"
            NODE_VERSION=$(node --version)
            echo "✓ Node.js detected: $NODE_VERSION"
        fi
    fi

    # Check for Python
    if [ -f "requirements.txt" ] || [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
        if command -v python >/dev/null 2>&1; then
            runtime="python"
            PYTHON_VERSION=$(python --version)
            echo "✓ Python detected: $PYTHON_VERSION"
        elif command -v python3 >/dev/null 2>&1; then
            runtime="python"
            PYTHON_VERSION=$(python3 --version)
            echo "✓ Python detected: $PYTHON_VERSION"
        fi
    fi

    # Check for browser-based app
    if [ -f "package.json" ]; then
        if grep -q "\"react\"\|\"vue\"\|\"angular\"\|\"svelte\"" package.json; then
            if [ -z "$runtime" ]; then
                runtime="browser"
            else
                runtime="$runtime,browser"
            fi
            echo "✓ Frontend framework detected - browser profiling available"
        fi
    fi

    echo "$runtime"
}

RUNTIME=$(detect_runtime)

if [ -z "$RUNTIME" ]; then
    echo "❌ Unable to detect runtime environment"
    echo ""
    echo "Supported environments:"
    echo "  - Node.js applications"
    echo "  - Python applications"
    echo "  - Browser-based applications (React, Vue, Angular, Svelte)"
    exit 1
fi

echo ""
echo "Environment: $RUNTIME"
```

## Phase 2: Install Profiling Tools

I'll check and install necessary profiling tools:

```bash
echo ""
echo "=== Installing Profiling Tools ==="

install_profiling_tools() {
    case "$RUNTIME" in
        *nodejs*)
            echo "Setting up Node.js profiling tools..."

            # Check for clinic.js
            if ! npm list -g clinic >/dev/null 2>&1; then
                echo "Installing clinic.js (performance profiling suite)..."
                echo "  npm install -g clinic"
                echo ""
                echo "Clinic.js tools:"
                echo "  - clinic doctor   - Diagnose performance issues"
                echo "  - clinic flame    - CPU flame graphs"
                echo "  - clinic bubbleprof - Async operations"
                echo "  - clinic heapprofiler - Memory profiling"
            else
                echo "✓ clinic.js already installed"
            fi

            # Check for autocannon (benchmarking)
            if ! npm list -g autocannon >/dev/null 2>&1; then
                echo ""
                echo "Installing autocannon (HTTP benchmarking)..."
                echo "  npm install -g autocannon"
            else
                echo "✓ autocannon already installed"
            fi

            echo ""
            echo "Node.js profiling methods available:"
            echo "  1. Built-in --inspect flag"
            echo "  2. clinic.js suite"
            echo "  3. Chrome DevTools"
            ;;

        *python*)
            echo "Setting up Python profiling tools..."

            # Check for profiling packages
            if ! python -c "import cProfile" 2>/dev/null; then
                echo "cProfile not available (should be in stdlib)"
            else
                echo "✓ cProfile available (built-in)"
            fi

            # Check for line_profiler
            if ! python -c "import line_profiler" 2>/dev/null; then
                echo ""
                echo "Install line_profiler for line-by-line profiling:"
                echo "  pip install line_profiler"
            else
                echo "✓ line_profiler available"
            fi

            # Check for memory_profiler
            if ! python -c "import memory_profiler" 2>/dev/null; then
                echo ""
                echo "Install memory_profiler for memory analysis:"
                echo "  pip install memory_profiler"
            else
                echo "✓ memory_profiler available"
            fi

            echo ""
            echo "Python profiling methods available:"
            echo "  1. cProfile (CPU profiling)"
            echo "  2. line_profiler (line-by-line)"
            echo "  3. memory_profiler (memory usage)"
            ;;

        *browser*)
            echo "Browser profiling setup..."
            echo ""
            echo "Browser profiling tools:"
            echo "  1. Chrome DevTools Performance tab"
            echo "  2. Lighthouse CI"
            echo "  3. webpack-bundle-analyzer"
            echo "  4. React DevTools Profiler"

            # Check for bundle analyzer
            if [ -f "package.json" ]; then
                if ! grep -q "webpack-bundle-analyzer" package.json; then
                    echo ""
                    echo "Install webpack-bundle-analyzer:"
                    echo "  npm install --save-dev webpack-bundle-analyzer"
                fi
            fi
            ;;
    esac
}

install_profiling_tools
```

## Phase 3: Node.js Profiling

For Node.js applications, I'll set up and run profiling:

```bash
if [[ "$RUNTIME" == *"nodejs"* ]]; then
    echo ""
    echo "=== Node.js Performance Profiling ==="

    # Create profiling scripts
    cat > "$PROFILE_DIR/profile-node.sh" << 'NODEPROFILE'
#!/bin/bash
# Node.js Performance Profiling

echo "Node.js Profiling Options:"
echo ""
echo "1. CPU Profiling (clinic doctor)"
echo "2. Flame Graph (clinic flame)"
echo "3. Async Operations (clinic bubbleprof)"
echo "4. Memory Profiling (clinic heapprofiler)"
echo "5. Built-in V8 Profiler (--prof)"
echo "6. HTTP Load Testing (autocannon)"
echo ""

# Option 1: Clinic Doctor (comprehensive diagnosis)
clinic_doctor() {
    echo "Running clinic doctor..."
    echo "This will start your app and collect performance data"
    echo ""

    # Find entry point
    ENTRY=$(node -p "require('./package.json').main || 'index.js'")

    clinic doctor -- node "$ENTRY"

    echo ""
    echo "✓ Profile complete! Opening report in browser..."
}

# Option 2: Flame Graph
clinic_flame() {
    echo "Running clinic flame..."
    echo "Generating CPU flame graph"
    echo ""

    ENTRY=$(node -p "require('./package.json').main || 'index.js'")

    clinic flame -- node "$ENTRY"

    echo ""
    echo "✓ Flame graph generated!"
}

# Option 3: Async Operations
clinic_bubble() {
    echo "Running clinic bubbleprof..."
    echo "Analyzing async operations"
    echo ""

    ENTRY=$(node -p "require('./package.json').main || 'index.js'")

    clinic bubbleprof -- node "$ENTRY"

    echo ""
    echo "✓ Async analysis complete!"
}

# Option 4: V8 Profiler
v8_profiler() {
    echo "Running V8 profiler..."
    echo ""

    ENTRY=$(node -p "require('./package.json').main || 'index.js'")

    node --prof "$ENTRY"

    # Process the profile
    PROFILE=$(ls isolate-*.log | head -1)
    if [ -n "$PROFILE" ]; then
        node --prof-process "$PROFILE" > processed-profile.txt
        echo "✓ Profile processed: processed-profile.txt"
    fi
}

# Option 5: HTTP Load Test
http_load_test() {
    echo "HTTP Load Testing with autocannon"
    echo ""
    read -p "Enter URL to test (e.g., http://localhost:3000): " URL
    read -p "Duration in seconds (default: 10): " DURATION
    DURATION=${DURATION:-10}

    echo ""
    echo "Running load test..."
    autocannon -d $DURATION "$URL"
}

# Main menu
case "${1:-1}" in
    1) clinic_doctor ;;
    2) clinic_flame ;;
    3) clinic_bubble ;;
    4) clinic_heapprofiler -- node $(node -p "require('./package.json').main || 'index.js'") ;;
    5) v8_profiler ;;
    6) http_load_test ;;
    *) echo "Invalid option" ;;
esac
NODEPROFILE

    chmod +x "$PROFILE_DIR/profile-node.sh"
    echo "✓ Created Node.js profiling script: $PROFILE_DIR/profile-node.sh"

    # Identify potential bottlenecks in code
    echo ""
    echo "Scanning for potential performance issues..."

    # Check for synchronous blocking operations
    SYNC_BLOCKING=$(grep -r "readFileSync\|writeFileSync\|execSync" \
        --include="*.js" --include="*.ts" \
        --exclude-dir=node_modules \
        --exclude-dir=dist \
        . 2>/dev/null | wc -l)

    if [ "$SYNC_BLOCKING" -gt 0 ]; then
        echo "⚠️  Found $SYNC_BLOCKING synchronous blocking operations"
        echo "   Consider using async versions (readFile, writeFile, exec)"
    fi

    # Check for missing await
    MISSING_AWAIT=$(grep -r "^\s*async.*function" \
        --include="*.js" --include="*.ts" \
        --exclude-dir=node_modules \
        . 2>/dev/null | wc -l)

    echo "💡 Async functions found: $MISSING_AWAIT"
    echo "   Verify all async calls use await or proper promise handling"

    # Check for large dependencies
    echo ""
    echo "Analyzing bundle size..."
    if [ -f "package.json" ]; then
        DEPS_COUNT=$(cat package.json | jq '.dependencies | length' 2>/dev/null || echo "N/A")
        echo "  Dependencies: $DEPS_COUNT"

        # Suggest bundle analyzer
        echo ""
        echo "To analyze bundle size:"
        echo "  npm install --save-dev webpack-bundle-analyzer"
        echo "  # Add to webpack config and run build"
    fi
fi
```

## Phase 4: Python Profiling

For Python applications, I'll set up profiling:

```bash
if [[ "$RUNTIME" == *"python"* ]]; then
    echo ""
    echo "=== Python Performance Profiling ==="

    cat > "$PROFILE_DIR/profile-python.sh" << 'PYTHONPROFILE'
#!/bin/bash
# Python Performance Profiling

echo "Python Profiling Options:"
echo ""
echo "1. cProfile (CPU profiling)"
echo "2. line_profiler (line-by-line)"
echo "3. memory_profiler (memory usage)"
echo ""

# Option 1: cProfile
cpu_profile() {
    echo "Running cProfile..."
    echo ""

    # Find main Python file
    if [ -f "main.py" ]; then
        ENTRY="main.py"
    elif [ -f "app.py" ]; then
        ENTRY="app.py"
    else
        read -p "Enter Python file to profile: " ENTRY
    fi

    python -m cProfile -o profile.stats "$ENTRY"

    # Analyze profile
    python << 'ANALYZE'
import pstats
from pstats import SortKey

p = pstats.Stats('profile.stats')
print("\n=== Top 20 Functions by Cumulative Time ===")
p.sort_stats(SortKey.CUMULATIVE).print_stats(20)

print("\n=== Top 20 Functions by Total Time ===")
p.sort_stats(SortKey.TIME).print_stats(20)
ANALYZE

    echo ""
    echo "✓ Profile saved to: profile.stats"
}

# Option 2: line_profiler
line_profile() {
    echo "Using line_profiler..."
    echo ""
    echo "Add @profile decorator to functions you want to profile"
    echo "Example:"
    echo "  @profile"
    echo "  def slow_function():"
    echo "      pass"
    echo ""

    read -p "Enter Python file with @profile decorators: " ENTRY

    kernprof -l -v "$ENTRY"
}

# Option 3: memory_profiler
memory_profile() {
    echo "Using memory_profiler..."
    echo ""
    echo "Add @profile decorator to functions you want to profile"
    echo ""

    read -p "Enter Python file with @profile decorators: " ENTRY

    python -m memory_profiler "$ENTRY"
}

case "${1:-1}" in
    1) cpu_profile ;;
    2) line_profile ;;
    3) memory_profile ;;
    *) echo "Invalid option" ;;
esac
PYTHONPROFILE

    chmod +x "$PROFILE_DIR/profile-python.sh"
    echo "✓ Created Python profiling script: $PROFILE_DIR/profile-python.sh"

    # Identify potential bottlenecks
    echo ""
    echo "Scanning for potential performance issues..."

    # Check for list comprehensions that could be generators
    LIST_COMP=$(grep -r "\[.*for .* in .*\]" \
        --include="*.py" \
        --exclude-dir=venv \
        --exclude-dir=env \
        . 2>/dev/null | wc -l)

    echo "💡 List comprehensions found: $LIST_COMP"
    echo "   Consider using generators for large datasets"

    # Check for database queries without indexing hints
    DB_QUERIES=$(grep -r "SELECT.*FROM\|\.filter(\|\.get(" \
        --include="*.py" \
        . 2>/dev/null | wc -l)

    if [ "$DB_QUERIES" -gt 0 ]; then
        echo "💡 Database queries found: $DB_QUERIES"
        echo "   Ensure proper indexing and use select_related/prefetch_related"
    fi
fi
```

## Phase 5: Browser Profiling

For frontend applications, I'll set up browser profiling:

```bash
if [[ "$RUNTIME" == *"browser"* ]]; then
    echo ""
    echo "=== Browser Performance Profiling ==="

    cat > "$PROFILE_DIR/profile-browser.md" << 'BROWSERPROFILE'
# Browser Performance Profiling Guide

## Chrome DevTools Performance Profiling

1. **Open Chrome DevTools**
   - F12 or Right-click → Inspect
   - Go to "Performance" tab

2. **Record Performance**
   - Click Record button (circle)
   - Interact with your app (navigate, click, scroll)
   - Click Stop

3. **Analyze Results**
   - Look for long tasks (> 50ms)
   - Identify JavaScript execution time
   - Check layout/reflow operations
   - Analyze network waterfall

4. **Key Metrics**
   - FCP (First Contentful Paint) - < 1.8s
   - LCP (Largest Contentful Paint) - < 2.5s
   - TBT (Total Blocking Time) - < 200ms
   - CLS (Cumulative Layout Shift) - < 0.1

## Lighthouse Audit

```bash
# Install Lighthouse CLI
npm install -g lighthouse

# Run audit
lighthouse http://localhost:3000 --view

# Or programmatically
npx lighthouse http://localhost:3000 --output html --output-path ./lighthouse-report.html
```

## Bundle Analysis

### Webpack Bundle Analyzer

```bash
npm install --save-dev webpack-bundle-analyzer

# Add to webpack.config.js
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = {
  plugins: [
    new BundleAnalyzerPlugin()
  ]
}

# Run build
npm run build
```

### Vite Bundle Analysis

```bash
npm install --save-dev rollup-plugin-visualizer

# Add to vite.config.js
import { visualizer } from 'rollup-plugin-visualizer';

export default {
  plugins: [
    visualizer({ open: true })
  ]
}

# Run build
npm run build
```

## React Profiler

```jsx
import { Profiler } from 'react';

function onRenderCallback(
  id, phase, actualDuration, baseDuration, startTime, commitTime
) {
  console.log(`${id} took ${actualDuration}ms to render`);
}

<Profiler id="MyComponent" onRender={onRenderCallback}>
  <MyComponent />
</Profiler>
```

## Common Performance Issues

### 1. Unnecessary Re-renders
- Use React.memo() for expensive components
- Implement shouldComponentUpdate or use useMemo
- Avoid inline function definitions in JSX

### 2. Large Bundle Size
- Code splitting with React.lazy()
- Tree shaking unused code
- Analyze and remove large dependencies

### 3. Unoptimized Images
- Use WebP format
- Implement lazy loading
- Add proper width/height attributes

### 4. Too Many Network Requests
- Bundle similar resources
- Use HTTP/2 multiplexing
- Implement resource hints (preload, prefetch)

### 5. Blocking JavaScript
- Defer non-critical scripts
- Use async attribute
- Move scripts to bottom of body

## Optimization Checklist

- [ ] Bundle size < 200KB (gzipped)
- [ ] First load < 3 seconds
- [ ] Images optimized and lazy-loaded
- [ ] Code split by route
- [ ] Critical CSS inlined
- [ ] Font loading optimized
- [ ] Service worker for caching
- [ ] Compression enabled (gzip/brotli)
BROWSERPROFILE

    echo "✓ Created browser profiling guide: $PROFILE_DIR/profile-browser.md"

    # Check for performance anti-patterns
    echo ""
    echo "Scanning for performance anti-patterns..."

    # Check for console.log in production
    CONSOLE_LOGS=$(grep -r "console\.log\|console\.debug" \
        --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx" \
        --exclude-dir=node_modules \
        . 2>/dev/null | wc -l)

    if [ "$CONSOLE_LOGS" -gt 10 ]; then
        echo "⚠️  Found $CONSOLE_LOGS console.log statements"
        echo "   Remove or use conditional logging for production"
    fi

    # Check for large images
    if [ -d "public" ] || [ -d "static" ] || [ -d "assets" ]; then
        echo ""
        echo "Checking for large images..."
        find public static assets -type f \( -name "*.jpg" -o -name "*.png" -o -name "*.jpeg" \) -size +500k 2>/dev/null | while read img; do
            SIZE=$(du -h "$img" | cut -f1)
            echo "  ⚠️  Large image: $img ($SIZE)"
        done
    fi
fi
```

## Phase 6: Generate Performance Report

I'll create a comprehensive performance analysis report:

```bash
echo ""
echo "=== Generating Performance Report ==="

cat > "$REPORT" << EOF
# Performance Profile Report

**Generated:** $(date)
**Runtime:** $RUNTIME
**Project:** $(basename $(pwd))

---

## Profiling Setup

### Environment

- **Runtime:** $RUNTIME
- **Node Version:** ${NODE_VERSION:-N/A}
- **Python Version:** ${PYTHON_VERSION:-N/A}

### Tools Available

EOF

# Add tool-specific sections
if [[ "$RUNTIME" == *"nodejs"* ]]; then
    cat >> "$REPORT" << 'EOF'

#### Node.js Profiling Tools

- clinic.js suite (doctor, flame, bubbleprof, heapprofiler)
- V8 built-in profiler (--prof)
- Chrome DevTools inspector
- autocannon (HTTP benchmarking)

**Run profiling:**
```bash
./claude/profiling/profile-node.sh 1  # Clinic doctor
./claude/profiling/profile-node.sh 2  # Flame graph
./claude/profiling/profile-node.sh 6  # Load test
```

EOF
fi

if [[ "$RUNTIME" == *"python"* ]]; then
    cat >> "$REPORT" << 'EOF'

#### Python Profiling Tools

- cProfile (CPU profiling)
- line_profiler (line-by-line analysis)
- memory_profiler (memory usage)

**Run profiling:**
```bash
./claude/profiling/profile-python.sh 1  # cProfile
./claude/profiling/profile-python.sh 2  # line_profiler
```

EOF
fi

if [[ "$RUNTIME" == *"browser"* ]]; then
    cat >> "$REPORT" << 'EOF'

#### Browser Profiling Tools

- Chrome DevTools Performance
- Lighthouse CI
- webpack-bundle-analyzer
- React DevTools Profiler

**See guide:**
```bash
cat .claude/profiling/profile-browser.md
```

EOF
fi

cat >> "$REPORT" << 'EOF'

---

## Quick Wins

### Immediate Optimizations

1. **Enable Compression**
   - gzip/brotli compression
   - Reduce bundle size by 60-80%

2. **Code Splitting**
   - Split by route
   - Lazy load heavy components
   - Reduce initial load time

3. **Optimize Images**
   - Use WebP format
   - Lazy loading
   - Proper sizing

4. **Remove Unnecessary Dependencies**
   - Audit package.json
   - Replace heavy libraries with lighter alternatives
   - Tree shake unused code

5. **Database Query Optimization**
   - Add proper indexes
   - Use connection pooling
   - Implement caching

---

## Performance Monitoring

### Continuous Monitoring

- Set up Lighthouse CI in your pipeline
- Monitor Core Web Vitals
- Track bundle size over time
- Profile in production

### Recommended Tools

- [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci)
- [bundlesize](https://github.com/siddharthkp/bundlesize)
- [clinic.js](https://clinicjs.org/)
- [New Relic](https://newrelic.com/) or [Datadog](https://www.datadoghq.com/)

---

## Next Steps

- [ ] Run profiling session
- [ ] Identify top 3 bottlenecks
- [ ] Implement optimizations
- [ ] Measure improvements
- [ ] Add performance budgets to CI
- [ ] Set up continuous monitoring

---

## Resources

- [Web.dev Performance](https://web.dev/performance/)
- [Node.js Performance Guide](https://nodejs.org/en/docs/guides/simple-profiling/)
- [Python Performance Tips](https://wiki.python.org/moin/PythonSpeed/PerformanceTips)
- [Chrome DevTools Performance](https://developer.chrome.com/docs/devtools/performance/)

EOF

echo "✓ Created performance report: $REPORT"
```

## Summary

```bash
echo ""
echo "=== ✓ Performance Profiling Setup Complete ==="
echo ""
echo "🎯 Runtime Environment: $RUNTIME"
echo ""
echo "📁 Generated files:"
echo "  - $REPORT"

if [[ "$RUNTIME" == *"nodejs"* ]]; then
    echo "  - $PROFILE_DIR/profile-node.sh"
fi

if [[ "$RUNTIME" == *"python"* ]]; then
    echo "  - $PROFILE_DIR/profile-python.sh"
fi

if [[ "$RUNTIME" == *"browser"* ]]; then
    echo "  - $PROFILE_DIR/profile-browser.md"
fi

echo ""
echo "🚀 Quick Start:"
echo ""

if [[ "$RUNTIME" == *"nodejs"* ]]; then
    echo "Node.js Profiling:"
    echo "  $PROFILE_DIR/profile-node.sh 1  # Comprehensive diagnosis"
    echo "  $PROFILE_DIR/profile-node.sh 2  # CPU flame graph"
    echo "  $PROFILE_DIR/profile-node.sh 6  # HTTP load test"
    echo ""
fi

if [[ "$RUNTIME" == *"python"* ]]; then
    echo "Python Profiling:"
    echo "  $PROFILE_DIR/profile-python.sh 1  # CPU profiling"
    echo "  $PROFILE_DIR/profile-python.sh 2  # Line-by-line"
    echo ""
fi

if [[ "$RUNTIME" == *"browser"* ]]; then
    echo "Browser Profiling:"
    echo "  lighthouse http://localhost:3000 --view"
    echo "  cat $PROFILE_DIR/profile-browser.md  # Full guide"
    echo ""
fi

echo "📊 Performance Analysis Workflow:"
echo ""
echo "1. Establish baseline performance"
echo "   - Run profiling on current code"
echo "   - Record key metrics (response time, memory, CPU)"
echo ""
echo "2. Identify bottlenecks"
echo "   - Find slowest functions/routes"
echo "   - Check database queries"
echo "   - Analyze bundle size"
echo ""
echo "3. Optimize iteratively"
echo "   - Fix highest-impact issues first"
echo "   - Re-profile after each change"
echo "   - Measure improvement"
echo ""
echo "4. Set performance budgets"
echo "   - Bundle size limits"
echo "   - Response time targets"
echo "   - Memory usage constraints"
echo ""
echo "💡 Common Bottlenecks:"
echo "  - Synchronous blocking operations"
echo "  - N+1 database queries"
echo "  - Large bundle sizes"
echo "  - Unoptimized images"
echo "  - Missing caching"
echo "  - Inefficient algorithms"
echo ""
echo "🔗 Integration Points:"
echo "  - /debug-root-cause - Investigate performance issues"
echo "  - /test - Add performance tests"
echo "  - /ci-setup - Add performance budgets to CI"
echo ""
echo "View full report: cat $REPORT"
```

## Best Practices

**Profiling Strategy:**
- Profile in production-like environment
- Use representative workloads
- Run multiple samples for accuracy
- Focus on 80/20 rule (biggest bottlenecks first)
- Measure before and after optimizations

**Common Optimizations:**
- Cache frequently accessed data
- Use connection pooling for databases
- Implement lazy loading
- Optimize database queries with indexes
- Use CDN for static assets
- Enable compression
- Minimize bundle size

**Performance Budgets:**
- Set and enforce limits on bundle size
- Target response times for critical paths
- Monitor memory usage patterns
- Track Core Web Vitals (LCP, FID, CLS)

**Credits:** Performance profiling methodology based on Node.js profiling guide, Python performance documentation, Chrome DevTools documentation, and Web.dev performance best practices. Clinic.js integration patterns from NearForm. Lighthouse CI guidance from Google Chrome team.
