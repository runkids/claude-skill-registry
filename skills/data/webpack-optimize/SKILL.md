---
name: webpack-optimize
description: Webpack/Vite/esbuild configuration optimization for build performance
disable-model-invocation: false
---

# Webpack & Build Tool Optimizer

I'll analyze your build configuration and provide optimization recommendations to improve build speed and bundle size.

Arguments: `$ARGUMENTS` - specific build tool or focus area (e.g., "webpack", "vite", "production")

## Strategic Analysis Process

<think>
Build tool optimization requires careful consideration:

1. **Current State Analysis**
   - What bundler is being used? (Webpack, Vite, esbuild, Rollup, Parcel)
   - What's the current build time and bundle size?
   - Are there obvious inefficiencies (no caching, poor splitting)?
   - What's the project type? (SPA, MPA, SSR, library)

2. **Optimization Opportunities**
   - Bundle splitting and code splitting strategies
   - Tree shaking configuration effectiveness
   - Module resolution optimization
   - Plugin efficiency and redundancy
   - Loader configuration improvements
   - Caching strategies (filesystem cache, persistent cache)

3. **Risk Assessment**
   - Breaking production builds with aggressive optimization
   - Introducing bugs through code splitting
   - Cache invalidation issues
   - Development experience degradation
   - Third-party plugin compatibility

4. **Implementation Strategy**
   - Priority 1: Safe caching improvements (filesystem cache)
   - Priority 2: Code splitting and lazy loading
   - Priority 3: Plugin optimization
   - Priority 4: Advanced tree shaking
   - Priority 5: Experimental features
</think>

## Phase 1: Build Tool Detection

**MANDATORY FIRST STEPS:**
1. Detect which build tool is in use
2. Locate configuration files
3. Analyze current build performance baseline
4. Identify obvious inefficiencies

Let me detect your build tool and analyze configuration:

```bash
# Detect build tool
BUILD_TOOL=""
CONFIG_FILE=""

if [ -f "webpack.config.js" ] || [ -f "webpack.config.ts" ]; then
    BUILD_TOOL="webpack"
    CONFIG_FILE="webpack.config.js"
    echo "Detected: Webpack"
elif [ -f "vite.config.js" ] || [ -f "vite.config.ts" ]; then
    BUILD_TOOL="vite"
    CONFIG_FILE=$(ls vite.config.* 2>/dev/null | head -n1)
    echo "Detected: Vite"
elif [ -f "esbuild.config.js" ] || [ -f "esbuild.config.mjs" ]; then
    BUILD_TOOL="esbuild"
    CONFIG_FILE=$(ls esbuild.config.* 2>/dev/null | head -n1)
    echo "Detected: esbuild"
elif [ -f "rollup.config.js" ] || [ -f "rollup.config.mjs" ]; then
    BUILD_TOOL="rollup"
    CONFIG_FILE=$(ls rollup.config.* 2>/dev/null | head -n1)
    echo "Detected: Rollup"
else
    # Check package.json for build tools
    if grep -q "\"webpack\"" package.json 2>/dev/null; then
        BUILD_TOOL="webpack"
        echo "Detected: Webpack (via package.json)"
    elif grep -q "\"vite\"" package.json 2>/dev/null; then
        BUILD_TOOL="vite"
        echo "Detected: Vite (via package.json)"
    else
        echo "No build tool detected"
        exit 1
    fi
fi

echo "Build Tool: $BUILD_TOOL"
echo "Config File: $CONFIG_FILE"
```

## Phase 2: Performance Baseline

I'll establish current performance metrics:

**Build Time Measurement:**
- Development build time
- Production build time
- Hot reload performance
- Cache hit rates

**Bundle Analysis:**
- Total bundle size
- Individual chunk sizes
- Duplicate dependencies
- Unused code percentage
- Tree shaking effectiveness

I'll analyze your build configuration for:
- Plugin usage and efficiency
- Loader configurations
- Code splitting strategy
- Caching configuration
- Source map settings
- Minification settings

## Phase 3: Optimization Recommendations

Based on detected build tool, I'll provide targeted optimizations:

### Webpack Optimizations

**Caching Improvements:**
- Enable persistent filesystem cache
- Configure cache invalidation properly
- Optimize module and chunk hashing
- Use cache groups for vendor splitting

**Code Splitting:**
- Implement intelligent split chunks configuration
- Configure runtime chunk extraction
- Set up dynamic imports for route-based splitting
- Optimize chunk size limits

**Performance Enhancements:**
- Configure thread-loader for parallel processing
- Optimize module resolution (resolve.modules)
- Use esbuild-loader for faster transpilation
- Enable faster source map options (cheap-module-source-map)
- Configure tree shaking side effects

**Plugin Optimization:**
- Remove redundant plugins
- Use production-optimized plugins only
- Configure TerserPlugin efficiently
- Optimize CSS extraction and minification

### Vite Optimizations

**Build Configuration:**
- Optimize dependency pre-bundling
- Configure build target appropriately
- Enable CSS code splitting
- Optimize chunk size warnings

**Development Experience:**
- Configure HMR boundaries
- Optimize server options
- Use native esbuild transforms
- Configure proxy efficiently

**Production Optimizations:**
- Configure Rollup output options
- Enable advanced minification
- Optimize asset inlining thresholds
- Configure manual chunks for better caching

### esbuild Optimizations

**Performance Tuning:**
- Configure splitting strategy
- Optimize tree shaking
- Use incremental builds
- Configure platform target
- Enable metafile for analysis

## Phase 4: Implementation Plan

I'll create prioritized optimization steps:

**Quick Wins (Immediate Impact):**
1. Enable filesystem caching
2. Update to latest build tool version
3. Remove unused plugins/loaders
4. Configure basic code splitting

**Medium-Term Improvements:**
1. Implement route-based code splitting
2. Optimize vendor chunk strategy
3. Configure aggressive tree shaking
4. Enable build parallelization

**Advanced Optimizations:**
1. Implement dynamic imports throughout
2. Configure sophisticated cache groups
3. Enable experimental features
4. Optimize for specific deployment targets

## Phase 5: Validation & Measurement

After applying optimizations, I'll verify improvements:

**Performance Metrics:**
- Measure new build times
- Compare bundle sizes
- Verify cache effectiveness
- Check hot reload speed

**Quality Assurance:**
- Ensure production build works
- Verify no runtime errors
- Check code splitting works correctly
- Validate source maps function
- Test development experience

## Configuration Examples

I'll provide specific configuration snippets for your build tool:

**Webpack Cache Configuration:**
```javascript
{
  cache: {
    type: 'filesystem',
    buildDependencies: {
      config: [__filename]
    }
  }
}
```

**Split Chunks Optimization:**
```javascript
{
  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          priority: 10
        }
      }
    }
  }
}
```

## Token Optimization Strategy

**Efficient Analysis:**
- Use Grep to find configuration patterns quickly
- Read only relevant config sections
- Cache project structure analysis
- Focus on high-impact optimizations first
- Avoid reading entire dependency tree

**Targeted Recommendations:**
- Provide build-tool-specific advice only
- Skip irrelevant optimization categories
- Focus on detected pain points
- Reference documentation links instead of inline explanations

## Integration Points

**Synergistic Skills:**
- `/bundle-analyze` - Detailed bundle composition analysis
- `/performance-profile` - Runtime performance measurement
- `/cache-strategy` - Application-level caching strategies
- `/lazy-load` - Implement code splitting patterns

Suggests `/bundle-analyze` when:
- Bundle size is the primary concern
- Need detailed dependency analysis
- Want visualization of bundle composition

Suggests `/cache-strategy` when:
- Runtime performance is a concern
- Application needs caching layer
- Service worker strategies needed

## Safety Mechanisms

**Protection Measures:**
- Create git checkpoint before config changes
- Back up existing configuration files
- Test build in development first
- Validate production build works
- Provide rollback instructions

**Validation Steps:**
1. Run development build
2. Test hot reload functionality
3. Run production build
4. Verify bundle integrity
5. Test deployed application

**Rollback Procedure:**
```bash
# Restore previous configuration
git checkout HEAD -- webpack.config.js
# Rebuild with original config
npm run build
```

## Common Optimization Scenarios

**Scenario 1: Slow Build Times**
- Enable persistent caching
- Use faster transpilers (esbuild-loader)
- Parallelize processing (thread-loader)
- Optimize module resolution paths

**Scenario 2: Large Bundle Size**
- Implement code splitting
- Configure tree shaking properly
- Analyze and remove duplicate dependencies
- Use dynamic imports aggressively

**Scenario 3: Poor Cache Efficiency**
- Configure content-based hashing
- Separate vendor and runtime chunks
- Use long-term caching strategies
- Optimize chunk splitting boundaries

## Expected Results

**Build Performance:**
- 30-70% faster development builds
- 20-50% faster production builds
- 80-95% cache hit rates after warmup
- Sub-second hot reload times

**Bundle Optimization:**
- 15-40% smaller bundle sizes
- Better chunk distribution
- Improved long-term caching
- Faster initial page loads

## Error Handling

If optimization introduces issues:
- I'll explain what went wrong
- Identify which optimization caused the problem
- Provide specific fix or rollback steps
- Suggest alternative optimization approaches
- Ensure builds remain functional

## Important Notes

**I will NEVER:**
- Break production builds
- Add AI attribution to config files
- Remove critical build plugins
- Modify package.json without confirmation
- Enable experimental features without warning

**Best Practices:**
- Test optimizations incrementally
- Measure before and after performance
- Document configuration changes
- Keep build tool versions updated
- Monitor production bundle sizes

## Credits

**Inspired by:**
- [Webpack Performance Guide](https://webpack.js.org/guides/build-performance/)
- [Vite Performance Best Practices](https://vitejs.dev/guide/performance.html)
- [esbuild Documentation](https://esbuild.github.io/)
- Web performance optimization community practices
- Build tool benchmarking research

This skill helps you achieve optimal build performance without sacrificing development experience or production reliability.
