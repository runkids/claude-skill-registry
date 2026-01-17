---
name: logging
description: Implement structured logging with log levels, formatting, and debugging. Use when adding logs to applications or debugging issues.
---

# 📋 Logging Skill

## Log Levels

| Level | When to Use |
|-------|-------------|
| ERROR | Failures that need attention |
| WARN | Potential issues, degraded |
| INFO | Normal operations |
| DEBUG | Detailed debugging |
| TRACE | Very detailed (rarely) |

---

## JavaScript Logging

### Console with Labels
```javascript
const log = {
  error: (...args) => console.error('[ERROR]', new Date().toISOString(), ...args),
  warn: (...args) => console.warn('[WARN]', new Date().toISOString(), ...args),
  info: (...args) => console.log('[INFO]', new Date().toISOString(), ...args),
  debug: (...args) => console.debug('[DEBUG]', new Date().toISOString(), ...args)
};

// Usage
log.info('Upload started', { file: 'video.mp4', size: 1024 });
log.error('Upload failed', { error: err.message });
```

### Structured Logger
```javascript
class Logger {
  constructor(name, level = 'info') {
    this.name = name;
    this.levels = ['error', 'warn', 'info', 'debug'];
    this.minLevel = this.levels.indexOf(level);
  }

  _log(level, message, data = {}) {
    if (this.levels.indexOf(level) > this.minLevel) return;
    
    const entry = {
      timestamp: new Date().toISOString(),
      level: level.toUpperCase(),
      logger: this.name,
      message,
      ...data
    };
    
    console[level === 'error' ? 'error' : 'log'](JSON.stringify(entry));
  }

  error(msg, data) { this._log('error', msg, data); }
  warn(msg, data) { this._log('warn', msg, data); }
  info(msg, data) { this._log('info', msg, data); }
  debug(msg, data) { this._log('debug', msg, data); }
}

const logger = new Logger('uploader', 'debug');
logger.info('Processing file', { filename: 'video.mp4' });
```

---

## Python Logging

```python
import logging

# Setup
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)

logger = logging.getLogger('psi-engine')

# Usage
logger.info('Agent spawned', extra={'agent_id': 'agent_001'})
logger.error('Task failed', exc_info=True)  # Include stack trace
```

---

## Chrome Extension Logging

```javascript
// Filter Auto Accept logs
function log(msg, data = {}) {
  console.log(
    '%c[AA v30]%c ' + msg,
    'color: #10b981; font-weight: bold',
    'color: inherit',
    data
  );
}

// Remote logging (to server)
function remoteLog(level, message, data) {
  fetch('/api/logs', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ level, message, data, timestamp: Date.now() })
  }).catch(() => {}); // Silent fail
}
```

---

## Best Practices

| ✅ Do | ❌ Don't |
|-------|---------|
| Include context (ids, values) | Log sensitive data |
| Use appropriate level | Use console.log everywhere |
| Structure as JSON | Log entire objects |
| Add timestamps | Leave debug logs in prod |
| Log errors with stack | Ignore error logging |

---

## Debug Patterns

```javascript
// Conditional debug
const DEBUG = process.env.DEBUG === 'true';
if (DEBUG) console.log('Detail:', data);

// Performance timing
console.time('upload');
await uploadFile(file);
console.timeEnd('upload');

// Group related logs
console.group('Upload Process');
console.log('File:', file.name);
console.log('Size:', file.size);
console.groupEnd();
```
