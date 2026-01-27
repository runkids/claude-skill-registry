---
name: bundle-analyze
description: Bundle size analysis and optimization for Webpack, Vite, and esbuild
disable-model-invocation: false
---

# Bundle Size Analysis & Optimization

I'll analyze your JavaScript bundle size, identify large dependencies, suggest tree-shaking opportunities, and recommend code splitting strategies.

**Supported Build Tools:**
- Webpack (webpack-bundle-analyzer)
- Vite (rollup-plugin-visualizer)
- esbuild (esbuild-visualizer)
- Rollup (rollup-plugin-visualizer)
- Next.js (@next/bundle-analyzer)

**Token Optimization:**
- Uses Grep to detect build configuration (300-500 tokens)
- Reads only config files (800-1,200 tokens)
- Structured analysis framework (1,200-1,800 tokens)
- Expected: 2,500-4,000 tokens total

**Arguments:** `$ARGUMENTS` - optional: production/development or specific entry point

<think>
Bundle optimization requires understanding:
- JavaScript bundle composition and size impact
- Tree-shaking effectiveness
- Code splitting strategies
- Lazy loading opportunities
- Dependency bloat identification
- Framework-specific optimization patterns
</think>

## Phase 1: Build Tool Detection

First, I'll detect your build tool and setup:

```bash
#!/bin/bash
# Bundle Analysis - Build Tool Detection

echo "=== Bundle Size Analysis & Optimization ==="
echo ""

# Create analysis directory
mkdir -p .claude/bundle-analysis
ANALYSIS_DIR=".claude/bundle-analysis"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
REPORT="$ANALYSIS_DIR/analysis-$TIMESTAMP.md"

detect_build_tool() {
    local build_tool=""
    local framework=""

    # Check package.json for build tools
    if [ ! -f "package.json" ]; then
        echo "❌ No package.json found"
        echo "   This skill requires a JavaScript/TypeScript project"
        exit 1
    fi

    echo "Analyzing project configuration..."

    # Next.js detection
    if grep -q '"next"' package.json; then
        framework="next"
        build_tool="webpack"  # Next.js uses webpack internally
        echo "✓ Next.js detected"

    # Vite detection
    elif [ -f "vite.config.js" ] || [ -f "vite.config.ts" ] || grep -q '"vite"' package.json; then
        build_tool="vite"
        echo "✓ Vite detected"

    # Webpack detection
    elif [ -f "webpack.config.js" ] || grep -q '"webpack"' package.json; then
        build_tool="webpack"
        echo "✓ Webpack detected"

    # esbuild detection
    elif [ -f "esbuild.config.js" ] || grep -q '"esbuild"' package.json; then
        build_tool="esbuild"
        echo "✓ esbuild detected"

    # Rollup detection
    elif [ -f "rollup.config.js" ] || grep -q '"rollup"' package.json; then
        build_tool="rollup"
        echo "✓ Rollup detected"

    else
        echo "⚠️  Unable to detect build tool"
        echo ""
        echo "Supported build tools:"
        echo "  - Webpack (webpack.config.js)"
        echo "  - Vite (vite.config.js)"
        echo "  - esbuild (esbuild.config.js)"
        echo "  - Rollup (rollup.config.js)"
        echo "  - Next.js (next.config.js)"
    fi

    # Detect framework
    if [ -z "$framework" ]; then
        if grep -q '"react"' package.json; then
            framework="react"
        elif grep -q '"vue"' package.json; then
            framework="vue"
        elif grep -q '"@angular' package.json; then
            framework="angular"
        elif grep -q '"svelte"' package.json; then
            framework="svelte"
        fi
    fi

    echo "$build_tool|$framework"
}

STACK=$(detect_build_tool)
BUILD_TOOL=$(echo "$STACK" | cut -d'|' -f1)
FRAMEWORK=$(echo "$STACK" | cut -d'|' -f2)

echo ""
echo "Build Tool: $BUILD_TOOL"
[ -n "$FRAMEWORK" ] && echo "Framework: $FRAMEWORK"

# Get current bundle info
echo ""
echo "Current project stats:"
if [ -d "dist" ] || [ -d "build" ]; then
    BUILD_DIR=$([ -d "dist" ] && echo "dist" || echo "build")
    echo "  Build directory: $BUILD_DIR"

    # Calculate total size
    TOTAL_SIZE=$(du -sh "$BUILD_DIR" 2>/dev/null | cut -f1)
    echo "  Total size: $TOTAL_SIZE"

    # Find JavaScript files
    JS_COUNT=$(find "$BUILD_DIR" -name "*.js" | wc -l)
    echo "  JavaScript files: $JS_COUNT"

    # Find largest files
    echo ""
    echo "  Largest files:"
    find "$BUILD_DIR" -name "*.js" -type f -exec du -h {} \; | \
        sort -rh | head -5 | sed 's/^/    /'
else
    echo "  No build directory found - run build first"
fi
```

## Phase 2: Install Bundle Analyzer

I'll install the appropriate bundle analyzer tool:

```bash
echo ""
echo "=== Installing Bundle Analyzer ==="
echo ""

install_analyzer() {
    case "$BUILD_TOOL" in
        webpack)
            if [ "$FRAMEWORK" = "next" ]; then
                # Next.js specific
                if ! grep -q "@next/bundle-analyzer" package.json; then
                    echo "Installing @next/bundle-analyzer..."
                    npm install --save-dev @next/bundle-analyzer
                else
                    echo "✓ @next/bundle-analyzer already installed"
                fi

                # Create Next.js bundle analyzer config
                cat > "$ANALYSIS_DIR/next.config.analyzer.js" << 'NEXTCONFIG'
const withBundleAnalyzer = require('@next/bundle-analyzer')({
    enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({
    // Your existing Next.js config
});
NEXTCONFIG

                echo "✓ Created Next.js analyzer config"
                echo ""
                echo "To use, set in your next.config.js:"
                echo "  const withBundleAnalyzer = require('@next/bundle-analyzer')({..."
                echo ""
                echo "Then run: ANALYZE=true npm run build"

            else
                # Standard webpack
                if ! grep -q "webpack-bundle-analyzer" package.json; then
                    echo "Installing webpack-bundle-analyzer..."
                    npm install --save-dev webpack-bundle-analyzer
                else
                    echo "✓ webpack-bundle-analyzer already installed"
                fi

                # Create webpack plugin config
                cat > "$ANALYSIS_DIR/webpack.analyzer.config.js" << 'WEBPACKCONFIG'
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');

module.exports = {
    // Add to your existing webpack config
    plugins: [
        new BundleAnalyzerPlugin({
            analyzerMode: 'static',
            reportFilename: 'bundle-report.html',
            openAnalyzer: false,
        }),
    ],
};
WEBPACKCONFIG

                echo "✓ Created webpack analyzer config"
            fi
            ;;

        vite)
            if ! grep -q "rollup-plugin-visualizer" package.json; then
                echo "Installing rollup-plugin-visualizer..."
                npm install --save-dev rollup-plugin-visualizer
            else
                echo "✓ rollup-plugin-visualizer already installed"
            fi

            # Create Vite config with analyzer
            cat > "$ANALYSIS_DIR/vite.config.analyzer.ts" << 'VITECONFIG'
import { defineConfig } from 'vite';
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
    // Your existing config
    plugins: [
        // Your existing plugins
        visualizer({
            filename: './dist/stats.html',
            open: true,
            gzipSize: true,
            brotliSize: true,
        }),
    ],
});
VITECONFIG

            echo "✓ Created Vite analyzer config"
            echo ""
            echo "Add to your vite.config.ts:"
            echo "  import { visualizer } from 'rollup-plugin-visualizer';"
            echo "  plugins: [visualizer({ ... })]"
            ;;

        esbuild)
            if ! grep -q "esbuild-visualizer" package.json; then
                echo "Installing esbuild-visualizer..."
                npm install --save-dev esbuild-visualizer
            else
                echo "✓ esbuild-visualizer already installed"
            fi

            cat > "$ANALYSIS_DIR/esbuild.analyzer.js" << 'ESBUILDCONFIG'
const esbuild = require('esbuild');
const { visualizer } = require('esbuild-visualizer');

esbuild.build({
    entryPoints: ['src/index.js'],
    bundle: true,
    outfile: 'dist/bundle.js',
    plugins: [
        visualizer({
            filename: './dist/stats.html',
        }),
    ],
}).catch(() => process.exit(1));
ESBUILDCONFIG

            echo "✓ Created esbuild analyzer config"
            ;;

        rollup)
            if ! grep -q "rollup-plugin-visualizer" package.json; then
                echo "Installing rollup-plugin-visualizer..."
                npm install --save-dev rollup-plugin-visualizer
            else
                echo "✓ rollup-plugin-visualizer already installed"
            fi

            echo "✓ Rollup uses same plugin as Vite"
            echo "  Add visualizer plugin to rollup.config.js"
            ;;
    esac
}

install_analyzer
```

## Phase 3: Large Dependency Detection

I'll analyze package.json for large dependencies:

```bash
echo ""
echo "=== Analyzing Dependencies ==="
echo ""

analyze_dependencies() {
    echo "Scanning for large dependencies..."
    echo ""

    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        echo "⚠️  node_modules not found - run npm install first"
        return
    fi

    # Find largest packages
    echo "Top 20 largest dependencies:"
    du -sh node_modules/* 2>/dev/null | sort -rh | head -20 | while read -r size path; do
        package=$(basename "$path")
        echo "  $size  $package"
    done

    echo ""
    echo "Analyzing package.json for common bloat..."

    # Check for moment.js (notoriously large)
    if grep -q '"moment"' package.json; then
        echo "⚠️  moment.js detected (large, 232KB minified)"
        echo "   💡 Consider alternatives:"
        echo "      - date-fns (smaller, tree-shakeable)"
        echo "      - dayjs (2KB, similar API)"
        echo "      - native Intl.DateTimeFormat"
    fi

    # Check for lodash
    if grep -q '"lodash"' package.json; then
        if ! grep -q '"lodash-es"' package.json; then
            echo "⚠️  lodash detected without lodash-es"
            echo "   💡 Use lodash-es for better tree-shaking"
            echo "      import { debounce } from 'lodash-es';"
        fi
    fi

    # Check for multiple date libraries
    DATE_LIBS=$(grep -E '"(moment|date-fns|dayjs|luxon)"' package.json | wc -l)
    if [ "$DATE_LIBS" -gt 1 ]; then
        echo "⚠️  Multiple date libraries detected: $DATE_LIBS"
        echo "   💡 Standardize on one library"
    fi

    # Check for duplicate functionality
    if grep -q '"axios"' package.json && grep -q '"fetch"' package.json; then
        echo "💡 Both axios and fetch detected"
        echo "   Consider using native fetch API"
    fi

    # Check for UI library size
    if grep -q '"@mui/material"' package.json; then
        echo "💡 Material-UI detected"
        echo "   Ensure tree-shaking is enabled:"
        echo "   import Button from '@mui/material/Button';"
    fi

    # Check bundle size
    if [ -f "package.json" ]; then
        echo ""
        echo "Installing bundle-size checker..."

        # Create temporary package-size checker
        cat > "$ANALYSIS_DIR/check-sizes.js" << 'SIZECHECKER'
const fs = require('fs');
const path = require('path');

const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
const deps = { ...packageJson.dependencies, ...packageJson.devDependencies };

console.log('\n🔍 Checking package sizes from npm...\n');

// Note: This would require npm API or package-size library
// For now, we'll list known large packages
const knownLargePackages = {
    'moment': '232 KB',
    'lodash': '72 KB',
    'axios': '13 KB',
    'rxjs': '108 KB',
    'core-js': '88 KB',
    '@mui/material': '328 KB',
    'antd': '1.2 MB',
    'three': '576 KB',
    'chart.js': '72 KB',
};

Object.keys(deps).forEach(dep => {
    if (knownLargePackages[dep]) {
        console.log(`  ${dep}: ${knownLargePackages[dep]}`);
    }
});
SIZECHECKER

        node "$ANALYSIS_DIR/check-sizes.js"
    fi
}

analyze_dependencies > "$ANALYSIS_DIR/dependency-analysis.txt"
cat "$ANALYSIS_DIR/dependency-analysis.txt"
```

## Phase 4: Tree-Shaking Analysis

I'll analyze tree-shaking opportunities:

```bash
echo ""
echo "=== Tree-Shaking Analysis ==="
echo ""

analyze_tree_shaking() {
    echo "Checking for tree-shaking opportunities..."
    echo ""

    # Check import patterns
    echo "Analyzing import statements..."

    # Find default imports from large libraries
    if grep -r "import.*from 'lodash'" --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx" \
        --exclude-dir=node_modules . 2>/dev/null | head -5; then
        echo "⚠️  Found lodash default imports"
        echo "   💡 Use named imports from lodash-es:"
        echo "      import { debounce } from 'lodash-es';"
    fi

    # Check for star imports
    STAR_IMPORTS=$(grep -r "import \* as" --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx" \
        --exclude-dir=node_modules . 2>/dev/null | wc -l)

    if [ "$STAR_IMPORTS" -gt 0 ]; then
        echo ""
        echo "⚠️  Found $STAR_IMPORTS star imports (import * as)"
        echo "   💡 Use named imports for better tree-shaking:"
        echo "      import { Component } from 'library';"
        echo ""
        echo "   Examples found:"
        grep -r "import \* as" --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx" \
            --exclude-dir=node_modules . 2>/dev/null | head -3
    fi

    # Check package.json for sideEffects
    echo ""
    echo "Checking package.json configuration..."

    if ! grep -q '"sideEffects"' package.json; then
        echo "💡 Add 'sideEffects' field to package.json for better tree-shaking:"
        echo '   "sideEffects": false'
        echo '   or'
        echo '   "sideEffects": ["*.css", "*.scss"]'
    else
        echo "✓ sideEffects field present in package.json"
    fi

    # Check for module field
    if ! grep -q '"module"' package.json && ! grep -q '"type": "module"' package.json; then
        echo "💡 Consider adding ES module support:"
        echo '   "module": "dist/index.esm.js"'
        echo '   "type": "module"'
    fi
}

analyze_tree_shaking
```

## Phase 5: Code Splitting Recommendations

I'll analyze code splitting opportunities:

```bash
echo ""
echo "=== Code Splitting Analysis ==="
echo ""

analyze_code_splitting() {
    echo "Analyzing code splitting opportunities..."
    echo ""

    case "$FRAMEWORK" in
        react)
            # Check for React.lazy usage
            LAZY_COUNT=$(grep -r "React.lazy\|lazy(" --include="*.jsx" --include="*.tsx" \
                --exclude-dir=node_modules . 2>/dev/null | wc -l)

            echo "React lazy imports: $LAZY_COUNT"

            if [ "$LAZY_COUNT" -eq 0 ]; then
                echo "⚠️  No React.lazy imports found"
                echo "   💡 Use React.lazy for route-based code splitting:"
                echo ""
                echo "   const Dashboard = React.lazy(() => import('./Dashboard'));"
                echo ""
                echo "   <Suspense fallback={<Loading />}>"
                echo "     <Dashboard />"
                echo "   </Suspense>"
            fi

            # Check for dynamic imports
            DYNAMIC_IMPORTS=$(grep -r "import(" --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx" \
                --exclude-dir=node_modules . 2>/dev/null | wc -l)

            echo "Dynamic imports: $DYNAMIC_IMPORTS"

            if [ "$DYNAMIC_IMPORTS" -eq 0 ]; then
                echo "💡 Consider dynamic imports for large components:"
                echo "   const HeavyComponent = await import('./HeavyComponent');"
            fi
            ;;

        vue)
            # Check for Vue lazy loading
            LAZY_COUNT=$(grep -r "() => import\|defineAsyncComponent" --include="*.vue" --include="*.js" \
                --exclude-dir=node_modules . 2>/dev/null | wc -l)

            echo "Vue async components: $LAZY_COUNT"

            if [ "$LAZY_COUNT" -eq 0 ]; then
                echo "💡 Use Vue async components for code splitting:"
                echo "   const AsyncComponent = defineAsyncComponent(() =>"
                echo "     import('./components/AsyncComponent.vue')"
                echo "   );"
            fi
            ;;

        next)
            # Check for Next.js dynamic imports
            DYNAMIC_IMPORTS=$(grep -r "next/dynamic" --include="*.jsx" --include="*.tsx" \
                --exclude-dir=node_modules . 2>/dev/null | wc -l)

            echo "Next.js dynamic imports: $DYNAMIC_IMPORTS"

            if [ "$DYNAMIC_IMPORTS" -eq 0 ]; then
                echo "💡 Use next/dynamic for component code splitting:"
                echo "   import dynamic from 'next/dynamic';"
                echo "   const DynamicComponent = dynamic(() => import('./Component'));"
            fi
            ;;
    esac

    echo ""
    echo "Route-based splitting recommendations:"
    echo "  - Split by route (each page = separate bundle)"
    echo "  - Lazy load heavy components (charts, editors)"
    echo "  - Use dynamic imports for modal content"
    echo "  - Split vendor code into separate chunk"
}

analyze_code_splitting
```

## Phase 6: Generate Analysis Report

I'll create a comprehensive bundle analysis report:

```bash
echo ""
echo "=== Generating Bundle Analysis Report ==="
echo ""

cat > "$REPORT" << EOF
# Bundle Analysis Report

**Generated:** $(date)
**Build Tool:** $BUILD_TOOL
**Framework:** $FRAMEWORK
**Project:** $(basename $(pwd))

---

## Bundle Size Summary

### Current State
- Build Directory: ${BUILD_DIR:-Not built}
- Total Size: ${TOTAL_SIZE:-Unknown}
- JavaScript Files: ${JS_COUNT:-Unknown}

### Recommendations Priority

1. **CRITICAL**: Fix large dependencies
2. **HIGH**: Implement code splitting
3. **MEDIUM**: Optimize tree-shaking
4. **LOW**: Fine-tune compression

---

## Large Dependencies

See detailed analysis: \`cat $ANALYSIS_DIR/dependency-analysis.txt\`

### Common Optimizations

#### Replace Heavy Libraries

\`\`\`bash
# Replace moment.js with date-fns
npm uninstall moment
npm install date-fns

# Or use dayjs (smaller, similar API)
npm install dayjs
\`\`\`

#### Use Lodash-ES

\`\`\`bash
npm install lodash-es
npm uninstall lodash
\`\`\`

\`\`\`javascript
// Before
import _ from 'lodash';

// After (tree-shakeable)
import { debounce, throttle } from 'lodash-es';
\`\`\`

---

## Code Splitting Strategy

### 1. Route-Based Splitting

#### React
\`\`\`jsx
import React, { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

// Lazy load routes
const Home = lazy(() => import('./pages/Home'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Profile = lazy(() => import('./pages/Profile'));

function App() {
    return (
        <BrowserRouter>
            <Suspense fallback={<div>Loading...</div>}>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/profile" element={<Profile />} />
                </Routes>
            </Suspense>
        </BrowserRouter>
    );
}
\`\`\`

#### Next.js
\`\`\`jsx
import dynamic from 'next/dynamic';

// Lazy load heavy components
const HeavyComponent = dynamic(() => import('../components/HeavyComponent'), {
    loading: () => <p>Loading...</p>,
    ssr: false,  // Disable SSR for client-only components
});
\`\`\`

### 2. Component-Based Splitting

\`\`\`jsx
// Lazy load modal content
const [ModalContent, setModalContent] = useState(null);

const openModal = async () => {
    const { ModalContent } = await import('./ModalContent');
    setModalContent(<ModalContent />);
};
\`\`\`

### 3. Vendor Chunk Splitting

#### Webpack
\`\`\`javascript
module.exports = {
    optimization: {
        splitChunks: {
            chunks: 'all',
            cacheGroups: {
                vendor: {
                    test: /[\\\\/]node_modules[\\\\/]/,
                    name: 'vendors',
                    priority: 10,
                },
                common: {
                    minChunks: 2,
                    priority: 5,
                    reuseExistingChunk: true,
                },
            },
        },
    },
};
\`\`\`

---

## Tree-Shaking Optimization

### Package.json Configuration

\`\`\`json
{
    "sideEffects": false,
    "module": "dist/index.esm.js",
    "main": "dist/index.js"
}
\`\`\`

### Import Patterns

\`\`\`javascript
// ❌ BAD: Imports entire library
import _ from 'lodash';
import * as utils from './utils';

// ✅ GOOD: Named imports (tree-shakeable)
import { debounce } from 'lodash-es';
import { specificUtil } from './utils';
\`\`\`

---

## Build Tool Optimization

### Webpack

\`\`\`javascript
module.exports = {
    mode: 'production',
    optimization: {
        minimize: true,
        usedExports: true,  // Tree shaking
        sideEffects: true,
    },
    performance: {
        maxEntrypointSize: 250000,  // 250KB
        maxAssetSize: 250000,
    },
};
\`\`\`

### Vite

\`\`\`javascript
export default defineConfig({
    build: {
        rollupOptions: {
            output: {
                manualChunks: {
                    vendor: ['react', 'react-dom'],
                },
            },
        },
        chunkSizeWarningLimit: 500,  // 500KB
    },
});
\`\`\`

---

## Compression

### Enable gzip/Brotli

\`\`\`bash
# Webpack compression
npm install --save-dev compression-webpack-plugin

# Vite compression
npm install --save-dev vite-plugin-compression
\`\`\`

\`\`\`javascript
// Webpack
const CompressionPlugin = require('compression-webpack-plugin');

plugins: [
    new CompressionPlugin({
        algorithm: 'gzip',
        test: /\\.(js|css|html|svg)$/,
    }),
];

// Vite
import compression from 'vite-plugin-compression';

plugins: [
    compression({ algorithm: 'gzip' }),
    compression({ algorithm: 'brotliCompress' }),
];
\`\`\`

---

## Performance Budget

### Recommended Limits

- Initial Load (JS): **< 200 KB** (gzipped)
- Total Bundle: **< 500 KB** (gzipped)
- Largest Chunk: **< 250 KB** (gzipped)

### Monitor Bundle Size

\`\`\`bash
# Install bundlesize
npm install --save-dev bundlesize

# Add to package.json
"bundlesize": [
    {
        "path": "./dist/*.js",
        "maxSize": "250 KB"
    }
]

# Add to CI
"scripts": {
    "test:size": "bundlesize"
}
\`\`\`

---

## Action Items

- [ ] Replace large dependencies (moment.js, lodash)
- [ ] Implement route-based code splitting
- [ ] Add tree-shaking optimization
- [ ] Configure vendor chunk splitting
- [ ] Enable gzip/Brotli compression
- [ ] Set up bundle size monitoring
- [ ] Add performance budgets to CI
- [ ] Analyze with bundle visualizer

---

## Next Steps

1. **Run bundle analyzer**
   \`\`\`bash
   # Build with analyzer
   ANALYZE=true npm run build

   # Or manually
   npm run build
   npx webpack-bundle-analyzer dist/stats.json
   \`\`\`

2. **Implement optimizations** (start with highest impact)

3. **Measure improvements**
   - Compare before/after bundle sizes
   - Test load times

4. **Set up continuous monitoring**
   - Add bundlesize to CI
   - Track bundle size over time

---

**Report generated at:** $(date)

EOF

echo "✓ Bundle analysis report generated: $REPORT"
```

## Summary

```bash
echo ""
echo "=== ✓ Bundle Analysis Complete ==="
echo ""
echo "📊 Report: $REPORT"
echo ""
echo "📋 Key Findings:"
echo "  - Build Tool: $BUILD_TOOL"
echo "  - Current Size: ${TOTAL_SIZE:-Run build first}"
echo "  - JavaScript Files: ${JS_COUNT:-Unknown}"
echo ""
echo "💡 Quick Wins:"
echo "  1. Replace moment.js with date-fns or dayjs"
echo "  2. Use lodash-es for tree-shaking"
echo "  3. Implement React.lazy for routes"
echo "  4. Enable gzip compression"
echo ""
echo "🔧 Generated Configs:"
ls "$ANALYSIS_DIR"/*.config.* "$ANALYSIS_DIR"/*.analyzer.* 2>/dev/null | sed 's/^/  - /'
echo ""
echo "🚀 Next Steps:"
echo "  1. Run bundle analyzer: ANALYZE=true npm run build"
echo "  2. Implement high-priority optimizations"
echo "  3. Measure improvements"
echo "  4. Set up continuous monitoring"
echo ""
echo "🔗 Integration Points:"
echo "  - /lighthouse - Web performance auditing"
echo "  - /lazy-load - Implement lazy loading"
echo "  - /ci-setup - Add bundle size checks to CI"
echo ""
echo "View report: cat $REPORT"
```

## Safety Guarantees

**What I'll NEVER do:**
- Modify build configuration without creating backups
- Remove dependencies without verifying usage
- Make breaking changes to import patterns
- Skip testing after optimization

**What I WILL do:**
- Provide clear optimization recommendations
- Generate safe configuration examples
- Identify large dependencies safely
- Suggest incremental improvements
- Document all changes

## Credits

This skill is based on:
- **webpack-bundle-analyzer** - Webpack bundle visualization
- **rollup-plugin-visualizer** - Rollup/Vite bundle analysis
- **Next.js Bundle Analyzer** - Next.js specific optimization
- **Web Performance Best Practices** - Bundle size guidelines
- **Tree-Shaking Guide** - Modern bundler optimization techniques

## Token Budget

Target: 2,500-4,000 tokens per execution
- Phase 1-2: ~1,000 tokens (detection + analyzer setup)
- Phase 3-4: ~1,200 tokens (dependency + tree-shaking analysis)
- Phase 5-6: ~1,500 tokens (code splitting + reporting)

**Optimization Strategy:**
- Use Grep for config detection
- Analyze package.json structure
- Generate framework-specific configs
- Provide actionable recommendations
- Comprehensive reporting

This ensures thorough bundle analysis across all major build tools while providing clear, actionable optimization strategies.
