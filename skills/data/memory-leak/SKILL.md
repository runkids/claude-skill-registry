---
name: memory-leak
description: Memory leak detection and analysis for Node.js, Python, and browsers
disable-model-invocation: false
---

# Memory Leak Detection & Analysis

I'll help you detect, analyze, and fix memory leaks across your application stack.

Arguments: `$ARGUMENTS` - runtime environment (node/python/browser) or specific files

## Session Intelligence

I'll maintain memory profiling sessions for tracking leaks over time:

**Session Files (in current project directory):**
- `memory-leak/profile.md` - Memory analysis and findings
- `memory-leak/state.json` - Profiling data and progress
- `memory-leak/snapshots/` - Heap snapshots and memory dumps

**IMPORTANT:** Session files are stored in a `memory-leak` folder in your current project root

**Auto-Detection:**
- If session exists: Compare with previous profiles
- If no session: Perform initial memory analysis
- Commands: `resume`, `analyze`, `compare`, `new`

## Phase 1: Runtime Detection & Setup

### Extended Thinking for Memory Analysis

For complex memory leak scenarios, I'll use extended thinking to understand patterns:

<think>
When analyzing memory leaks:
- Closure scopes that unintentionally retain references
- Event listener accumulation without cleanup
- Cache implementations without size limits or TTL
- Circular references preventing garbage collection
- Large object graphs held in memory
- Module-level state accumulation
- Timer/interval leaks from abandoned subscriptions
- DOM node retention in Single Page Applications
</think>

**Triggers for Extended Analysis:**
- Long-running server applications
- Real-time data processing systems
- Browser applications with complex state
- Applications with significant memory growth over time

I'll automatically detect your runtime environment:

**Node.js Detection:**
```bash
# Check for Node.js project
if [ -f "package.json" ]; then
    echo "Node.js project detected"
    node_version=$(node --version 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo "Node.js $node_version available"
        # Check for profiling tools
        npm list --depth=0 | grep -E "(heapdump|clinic|memwatch|node-inspect)"
    fi
fi
```

**Python Detection:**
```bash
# Check for Python project
if [ -f "requirements.txt" ] || [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
    echo "Python project detected"
    python_version=$(python3 --version 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo "$python_version available"
        # Check for profiling modules
        python3 -c "import tracemalloc, memory_profiler" 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "Memory profiling modules available"
        fi
    fi
fi
```

**Browser Detection:**
```bash
# Check for frontend project
if [ -f "package.json" ]; then
    if grep -qE "(react|vue|angular|svelte)" package.json; then
        echo "Frontend framework detected"
        echo "Browser memory profiling available via Chrome DevTools"
    fi
fi
```

## Phase 2: Memory Profiling Setup

Based on detected environment, I'll configure appropriate profiling:

### Node.js Memory Profiling

**Built-in Inspector:**
```javascript
// Enable heap profiling
node --inspect --expose-gc your-app.js

// Programmatic heap snapshot
const v8 = require('v8');
const fs = require('fs');

function takeHeapSnapshot(filename) {
    const snapshotStream = v8.writeHeapSnapshot();
    console.log(`Heap snapshot written to ${snapshotStream}`);
    return snapshotStream;
}

// Take snapshots at intervals
setInterval(() => {
    takeHeapSnapshot(`memory-leak/snapshots/heap-${Date.now()}.heapsnapshot`);
}, 60000);
```

**Heapdump Integration:**
```javascript
const heapdump = require('heapdump');
const path = require('path');

// Trigger on signal
process.on('SIGUSR2', () => {
    const filename = path.join(
        'memory-leak/snapshots',
        `heap-${Date.now()}.heapsnapshot`
    );
    heapdump.writeSnapshot(filename, (err, filepath) => {
        if (err) console.error(err);
        else console.log(`Heap snapshot written to ${filepath}`);
    });
});
```

**Memory Usage Monitoring:**
```javascript
function monitorMemory() {
    const usage = process.memoryUsage();
    return {
        timestamp: new Date().toISOString(),
        rss: Math.round(usage.rss / 1024 / 1024) + ' MB',
        heapTotal: Math.round(usage.heapTotal / 1024 / 1024) + ' MB',
        heapUsed: Math.round(usage.heapUsed / 1024 / 1024) + ' MB',
        external: Math.round(usage.external / 1024 / 1024) + ' MB',
        arrayBuffers: Math.round(usage.arrayBuffers / 1024 / 1024) + ' MB'
    };
}

// Log memory every minute
setInterval(() => {
    console.log('Memory usage:', JSON.stringify(monitorMemory()));
}, 60000);
```

### Python Memory Profiling

**tracemalloc (Built-in):**
```python
import tracemalloc
import linecache

def start_memory_tracking():
    tracemalloc.start()

def take_memory_snapshot():
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    print("[ Top 10 memory consuming lines ]")
    for stat in top_stats[:10]:
        print(stat)

    return snapshot

def compare_snapshots(snapshot1, snapshot2):
    top_stats = snapshot2.compare_to(snapshot1, 'lineno')

    print("[ Top 10 memory growth areas ]")
    for stat in top_stats[:10]:
        print(stat)
```

**memory_profiler:**
```python
from memory_profiler import profile

@profile
def potentially_leaky_function():
    # Function to analyze
    pass

# Run with: python -m memory_profiler your_script.py
```

**objgraph for Reference Tracking:**
```python
import objgraph
import gc

def analyze_object_growth():
    # Show most common types
    objgraph.show_most_common_types()

    # Track object growth
    objgraph.show_growth()

    # Find reference chains keeping objects alive
    roots = objgraph.get_leaking_objects()
    print(f"Found {len(roots)} potentially leaked objects")
```

### Browser Memory Profiling

**Chrome DevTools Integration:**
I'll guide you through browser memory analysis:

1. **Heap Snapshot Workflow:**
   - Take snapshot before action
   - Perform suspected leaky operation
   - Take snapshot after action
   - Compare snapshots for retained objects

2. **Allocation Timeline:**
   - Record allocation timeline
   - Perform operations
   - Identify object allocations that weren't freed

3. **Memory Panel Analysis:**
   - Monitor memory usage in real-time
   - Identify memory spikes and growth trends
   - Track garbage collection effectiveness

**Common Browser Leak Patterns:**
```javascript
// Pattern 1: Event listener leaks
class LeakyComponent {
    constructor() {
        // BAD: Never removed
        window.addEventListener('resize', this.handleResize);
    }

    // FIX: Cleanup in destroy
    destroy() {
        window.removeEventListener('resize', this.handleResize);
    }
}

// Pattern 2: Timer leaks
function leakyFunction() {
    // BAD: Interval never cleared
    setInterval(() => {
        console.log('Running...');
    }, 1000);
}

// Pattern 3: Detached DOM nodes
let cache = [];
function cacheElement() {
    // BAD: Keeps DOM nodes in memory after removal
    cache.push(document.getElementById('temp'));
}
```

## Phase 3: Leak Detection Analysis

I'll analyze memory patterns to identify leaks:

**Detection Strategies:**

1. **Heap Growth Analysis:**
   - Monitor heap size over time
   - Identify continuous growth without GC recovery
   - Compare heap snapshots

2. **Retained Object Analysis:**
   - Find objects that should be garbage collected
   - Trace retention paths
   - Identify unexpected references

3. **Circular Reference Detection:**
   - Scan for circular reference patterns
   - Check for manual cleanup requirements
   - Suggest WeakMap/WeakRef solutions

4. **Event Listener Auditing:**
   - Count active event listeners
   - Match add/remove pairs
   - Find orphaned listeners

**Analysis Output:**
```markdown
# Memory Leak Analysis Report

## Executive Summary
- **Environment**: Node.js 20.10.0
- **Analysis Duration**: 30 minutes
- **Leak Detected**: YES
- **Severity**: HIGH
- **Memory Growth**: 45 MB/hour

## Leak Sources Identified

### 1. Event Listener Accumulation
- **Location**: `src/services/WebSocketService.js:45`
- **Issue**: Socket event listeners not removed on disconnect
- **Impact**: ~2 MB per connection
- **Retention Path**: `EventEmitter -> handler -> closure -> largeDataBuffer`

### 2. Cache Without Limits
- **Location**: `src/cache/ResponseCache.js:23`
- **Issue**: Unbounded in-memory cache
- **Impact**: ~15 MB/hour growth
- **Retention Path**: `Map -> CacheEntry -> responseBody`

### 3. Circular References
- **Location**: `src/models/User.js:67`
- **Issue**: Parent-child circular references
- **Impact**: Prevents GC, accumulates 5 MB/hour
- **Retention Path**: `User -> friends[] -> User`

## Recommendations
[Detailed fix recommendations...]
```

## Phase 4: Integration with Performance Profiling

**Cross-Skill Integration:**
```bash
# When memory leaks impact performance
/memory-leak analyze    # Detect memory issues
/performance-profile    # Check CPU/runtime impact
```

I'll coordinate analysis across both dimensions:
- Memory leaks causing GC pressure
- Performance degradation from memory churn
- Optimization opportunities from profiling data

## Phase 5: Leak Remediation

I'll help fix identified leaks systematically:

**Fix Pattern 1: Proper Cleanup**
```javascript
// BEFORE: Leak
class Component {
    constructor() {
        this.timer = setInterval(this.update, 1000);
        window.addEventListener('resize', this.handleResize);
    }
}

// AFTER: Fixed
class Component {
    constructor() {
        this.timer = setInterval(this.update, 1000);
        this.handleResize = this.handleResize.bind(this);
        window.addEventListener('resize', this.handleResize);
    }

    destroy() {
        clearInterval(this.timer);
        window.removeEventListener('resize', this.handleResize);
        this.timer = null;
    }
}
```

**Fix Pattern 2: Bounded Caches**
```javascript
// BEFORE: Unbounded
const cache = new Map();

function cacheResponse(key, data) {
    cache.set(key, data);
}

// AFTER: LRU Cache with limits
class LRUCache {
    constructor(maxSize = 100) {
        this.cache = new Map();
        this.maxSize = maxSize;
    }

    set(key, value) {
        if (this.cache.size >= this.maxSize) {
            const firstKey = this.cache.keys().next().value;
            this.cache.delete(firstKey);
        }
        this.cache.set(key, value);
    }
}
```

**Fix Pattern 3: WeakRef for Circular References**
```javascript
// BEFORE: Strong circular reference
class User {
    constructor(name) {
        this.name = name;
        this.friends = [];
    }

    addFriend(user) {
        this.friends.push(user);
        user.friends.push(this); // Circular reference
    }
}

// AFTER: WeakRef to break cycle
class User {
    constructor(name) {
        this.name = name;
        this.friends = [];
    }

    addFriend(user) {
        this.friends.push(new WeakRef(user));
        user.friends.push(new WeakRef(this));
    }

    getFriends() {
        return this.friends
            .map(ref => ref.deref())
            .filter(friend => friend !== undefined);
    }
}
```

**Fix Pattern 4: Cleanup in Python**
```python
# BEFORE: Leak
class DataProcessor:
    def __init__(self):
        self.cache = {}
        self.connections = []

    def process(self, data):
        self.cache[data.id] = data  # Never cleaned

# AFTER: Context manager and cleanup
class DataProcessor:
    def __init__(self, max_cache_size=1000):
        self.cache = {}
        self.connections = []
        self.max_cache_size = max_cache_size

    def process(self, data):
        if len(self.cache) >= self.max_cache_size:
            # Remove oldest
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]

        self.cache[data.id] = data

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    def cleanup(self):
        self.cache.clear()
        for conn in self.connections:
            conn.close()
        self.connections.clear()
```

## Phase 6: Verification & Monitoring

After applying fixes, I'll verify the leak is resolved:

**Verification Process:**
1. Take baseline memory snapshot
2. Run application under load
3. Monitor memory growth over time
4. Compare with pre-fix behavior
5. Validate no new leaks introduced

**Long-term Monitoring Setup:**
```javascript
// Production memory monitoring
const monitoring = {
    interval: 300000, // 5 minutes
    threshold: 500 * 1024 * 1024, // 500 MB

    start() {
        setInterval(() => {
            const usage = process.memoryUsage();

            if (usage.heapUsed > this.threshold) {
                console.warn('Memory threshold exceeded', {
                    heapUsed: Math.round(usage.heapUsed / 1024 / 1024) + ' MB',
                    timestamp: new Date().toISOString()
                });

                // Optional: trigger alert or heap dump
            }
        }, this.interval);
    }
};
```

## Context Continuity

**Session Resume:**
When you return and run `/memory-leak` or `/memory-leak resume`:
- Load previous analysis and snapshots
- Compare current memory with baseline
- Show trend analysis
- Continue from last checkpoint

**Progress Example:**
```
RESUMING MEMORY LEAK ANALYSIS
├── Initial heap size: 125 MB
├── Current heap size: 180 MB
├── Growth rate: 9 MB/hour
├── Leaks fixed: 2 of 4
├── Next: Circular reference in User model

Comparing heap snapshots...
```

## Practical Examples

**Start Analysis:**
```
/memory-leak                    # Auto-detect runtime
/memory-leak node               # Node.js specific
/memory-leak python             # Python specific
/memory-leak browser            # Browser guidance
/memory-leak src/services/      # Analyze specific path
```

**Session Control:**
```
/memory-leak resume      # Continue analysis
/memory-leak analyze     # Run new profiling
/memory-leak compare     # Compare snapshots
/memory-leak status      # Check current state
```

## Safety Guarantees

**Protection Measures:**
- Git checkpoint before fixes
- Non-invasive profiling
- No production impact from analysis
- Snapshot data stays local

**Important:** I will NEVER:
- Profile production without permission
- Modify profiling in way that impacts performance
- Expose sensitive data in snapshots
- Add AI attribution to commits

## Skill Integration

When appropriate for memory issues:
- `/performance-profile` - Cross-reference with CPU usage
- `/test` - Verify fixes don't break functionality
- `/review` - Code review for leak patterns
- `/commit` - Safe commit of memory fixes

## Profiling Tools Reference

**Node.js:**
- Built-in: `--inspect`, `--expose-gc`, `v8.writeHeapSnapshot()`
- heapdump: Heap snapshot on demand
- clinic: Comprehensive profiling suite
- memwatch-next: Memory leak detection
- node-inspect: Interactive debugging

**Python:**
- Built-in: `tracemalloc`, `gc` module
- memory_profiler: Line-by-line profiling
- objgraph: Object reference tracking
- pympler: Advanced memory analysis
- guppy3: Heap analysis

**Browser:**
- Chrome DevTools Memory Panel
- Firefox Developer Tools Memory Tool
- Heap snapshots
- Allocation timeline
- Performance monitor

## Token Budget Optimization

To stay within 3,500-5,500 token budget:
- **Focus analysis on detected issues only**
- **Use compact reporting format**
- **Defer detailed profiling to manual review**
- **Provide actionable fixes over theory**
- **Batch similar leak patterns**

## What I'll Actually Do

1. **Detect runtime** - Auto-identify Node.js/Python/Browser
2. **Profile systematically** - Use appropriate tools for platform
3. **Identify leaks** - Extended thinking for complex patterns
4. **Provide fixes** - Concrete code changes
5. **Verify resolution** - Confirm leaks eliminated
6. **Monitor ongoing** - Setup long-term tracking

I'll help you eliminate memory leaks and establish monitoring to prevent future issues.

---

**Credits:**
- Inspired by Node.js profiling best practices
- Chrome DevTools Memory Profiling Guide
- Python memory_profiler documentation
- obra/superpowers debugging methodology
- Production memory leak patterns from real-world applications
