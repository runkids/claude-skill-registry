---
name: browser-extension
description: Cross-browser extension development with manifest V3, TypeScript, and modern APIs
license: MIT
compatibility: opencode
---

# Browser Extension Skill

Comprehensive patterns and best practices for cross-browser extension development with Manifest V3.

## What I Know

### Project Structure

```
src/
├── manifest.json           # Extension manifest
├── background/             # Service workers (background scripts)
│   └── service-worker.ts
├── content/               # Content scripts
│   ├── script.ts
│   └── styles.css
├── popup/                 # Extension popup UI
│   ├── index.html
│   ├── popup.tsx
│   └── styles.css
├── options/               # Options/settings page
│   ├── index.html
│   └── options.tsx
├── sidepanel/             # Side panel (Chrome 114+)
│   ├── index.html
│   └── sidepanel.tsx
├── devtools/              # DevTools panels
│   ├── main.html
│   └── main.ts
├── icons/                 # Extension icons (16, 48, 128)
└── shared/                # Shared utilities
    ├── types.ts
    └── utils.ts
```

### Manifest V3

**Basic Manifest**
```json
{
  "manifest_version": 3,
  "name": "My Extension",
  "version": "1.0.0",
  "description": "Description of my extension",
  "icons": {
    "16": "icons/icon16.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  },
  "action": {
    "default_popup": "popup/index.html",
    "default_icon": {
      "16": "icons/icon16.png",
      "48": "icons/icon48.png"
    }
  },
  "permissions": [
    "storage",
    "activeTab",
    "scripting"
  ],
  "host_permissions": [
    "https://api.example.com/*"
  ],
  "background": {
    "service_worker": "background/service-worker.js"
  },
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content/script.js"],
      "css": ["content/styles.css"]
    }
  ]
}
```

**Manifest with MV3 Features**
```json
{
  "manifest_version": 3,
  "name": "Advanced Extension",
  "version": "1.0.0",
  "description": "Advanced browser extension",
  "icons": {
    "16": "icons/icon16.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  },
  "action": {
    "default_popup": "popup/index.html",
    "default_title": "Click to open"
  },
  "permissions": [
    "storage",
    "tabs",
    "activeTab",
    "scripting",
    "alarms",
    "notifications"
  ],
  "host_permissions": [
    "https://*/*",
    "http://localhost:*/*"
  ],
  "background": {
    "service_worker": "background/service-worker.js",
    "type": "module"
  },
  "content_scripts": [
    {
      "matches": ["https://example.com/*"],
      "js": ["content/content.js"],
      "run_at": "document_idle"
    }
  ],
  "side_panel": {
    "default_path": "sidepanel/index.html"
  },
  "options_page": "options/index.html",
  "devtools_page": "devtools/index.html",
  "web_accessible_resources": [
    {
      "resources": ["assets/*", "icons/*"],
      "matches": ["<all_urls>"]
    }
  ]
}
```

### Content Scripts

**Basic Content Script**
```ts
// content/content.ts
console.log('Content script loaded!')

// Inject UI into page
function createWidget() {
  const widget = document.createElement('div')
  widget.id = 'my-extension-widget'
  widget.innerHTML = `
    <div class="widget-container">
      <button id="widget-btn">Click me</button>
    </div>
  `
  document.body.appendChild(widget)

  document.getElementById('widget-btn')?.addEventListener('click', () => {
    chrome.runtime.sendMessage({ action: 'widget-clicked' })
  })
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', createWidget)
} else {
  createWidget()
}

// Listen for messages from background/popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'getPageData') {
    const data = {
      title: document.title,
      url: window.location.href,
    }
    sendResponse(data)
  }
  return true // For async response
})
```

**Programmatic Content Script Injection**
```ts
// In background or popup
async function injectContentScript(tabId: number) {
  try {
    await chrome.scripting.executeScript({
      target: { tabId },
      files: ['content/content.js'],
    })
  } catch (error) {
    console.error('Failed to inject content script:', error)
  }
}
```

### Background Service Worker

**Service Worker**
```ts
// background/service-worker.ts
console.log('Service worker starting...')

// Handle extension installation
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    console.log('Extension installed')
    // Set default settings
    chrome.storage.local.set({
      settings: { enabled: true, theme: 'dark' }
    })
  } else if (details.reason === 'update') {
    console.log('Extension updated')
  }
})

// Handle messages from content scripts and popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  switch (message.action) {
    case 'getData':
      handleGetData().then(sendResponse)
      return true // Keep channel open for async response

    case 'widget-clicked':
      console.log('Widget was clicked!')
      break
  }
})

// Handle alarms
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'sync-data') {
    syncData()
  }
})

// Tab updates
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    console.log('Tab loaded:', tab.url)
  }
})

async function handleGetData() {
  const result = await chrome.storage.local.get(['data'])
  return result.data || null
}

function syncData() {
  // Sync logic here
}

// Create context menu
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: 'my-menu',
    title: 'My Extension Action',
    contexts: ['selection', 'link'],
  })
})

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'my-menu') {
    console.log('Context menu clicked:', info.selectionText)
  }
})
```

### Popup

**Popup HTML**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Extension</title>
  <link rel="stylesheet" href="popup.css">
</head>
<body>
  <div id="app">
    <h1>My Extension</h1>
    <button id="action-btn">Do Something</button>
  </div>
  <script src="popup.js"></script>
</body>
</html>
```

**Popup Script**
```ts
// popup/popup.ts
document.addEventListener('DOMContentLoaded', () => {
  const actionBtn = document.getElementById('action-btn')

  actionBtn?.addEventListener('click', async () => {
    // Get current tab
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true })

    if (tab.id) {
      // Send message to content script
      chrome.tabs.sendMessage(tab.id, { action: 'highlight' })

      // Or inject script
      await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: highlightElements,
      })
    }
  })
})

// Function to be injected
function highlightElements() {
  document.querySelectorAll('p').forEach(p => {
    p.style.background = 'yellow'
  })
}

// Load settings
chrome.storage.local.get(['settings'], (result) => {
  console.log('Settings:', result.settings)
})
```

### Options Page

**Options with React**
```tsx
// options/options.tsx
import { useEffect, useState } from 'react'
import { createRoot } from 'react-dom/client'

interface Settings {
  enabled: boolean
  theme: 'light' | 'dark'
}

function OptionsApp() {
  const [settings, setSettings] = useState<Settings>({
    enabled: true,
    theme: 'light',
  })

  useEffect(() => {
    // Load settings
    chrome.storage.local.get(['settings'], (result) => {
      if (result.settings) {
        setSettings(result.settings)
      }
    })
  }, [])

  const saveSettings = () => {
    chrome.storage.local.set({ settings })
  }

  return (
    <div className="options-container">
      <h1>Extension Options</h1>
      <label>
        <input
          type="checkbox"
          checked={settings.enabled}
          onChange={(e) => setSettings({ ...settings, enabled: e.target.checked })}
        />
        Enable extension
      </label>
      <select
        value={settings.theme}
        onChange={(e) => setSettings({ ...settings, theme: e.target.value as any })}
      >
        <option value="light">Light</option>
        <option value="dark">Dark</option>
      </select>
      <button onClick={saveSettings}>Save</button>
    </div>
  )
}

const container = document.getElementById('app')
if (container) {
  createRoot(container).render(<OptionsApp />)
}
```

### Storage API

**chrome.storage**
```ts
// Local storage (unlimited)
await chrome.storage.local.set({ key: 'value' })
const result = await chrome.storage.local.get(['key'])

// Sync storage (syncs across devices, 100KB limit)
await chrome.storage.sync.set({ preferences: { theme: 'dark' } })
const syncData = await chrome.storage.sync.get(['preferences'])

// Listen for changes
chrome.storage.onChanged.addListener((changes, areaName) => {
  if (areaName === 'local' && changes.key) {
    console.log('Key changed:', changes.key.newValue)
  }
})

// Session storage (in-memory, cleared on browser close)
await chrome.storage.session.set({ tempData: 'value' })
```

### Messaging API

**Communication Patterns**
```ts
// From content script to background
chrome.runtime.sendMessage({ action: 'getData' }, (response) => {
  console.log('Response:', response)
})

// From background to content script
chrome.tabs.sendMessage(tabId, { action: 'update' })

// From popup to background
chrome.runtime.sendMessage({ action: 'openOptions' })

// Broadcast to all content scripts
chrome.runtime.sendMessage({ action: 'broadcast', data: 'hello' })

// Long-lived connection (port)
const port = chrome.runtime.connect({ name: 'my-connection' })
port.postMessage({ action: 'init' })
port.onMessage.addListener((msg) => console.log(msg))
```

### Cross-Browser Compatibility

**Browser Detection**
```ts
// Get the browser API
const browserAPI = (() => {
  if (typeof chrome !== 'undefined' && chrome.runtime) {
    return chrome
  }
  if (typeof browser !== 'undefined' && browser.runtime) {
    return browser
  }
  throw new Error('Browser API not available')
})()

// Use browserAPI instead of chrome/browser
browserAPI.runtime.sendMessage({ action: 'test' })
```

**Polyfill with webextension-polyfill**
```ts
import browser from 'webextension-polyfill'

// Works across Chrome, Firefox, Edge, Safari
browser.storage.local.set({ key: 'value' })
browser.tabs.query({ active: true })
```

**Manifest Differences**
```json
// Firefox supports some extra features
{
  "browser_specific_settings": {
    "gecko": {
      "id": "extension@example.com",
      "strict_min_version": "109.0"
    }
  }
}
```

### TypeScript Setup

**tsconfig.json**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "lib": ["ES2020", "DOM"],
    "types": ["chrome"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "moduleResolution": "node",
    "resolveJsonModule": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}
```

**Chrome Types**
```bash
npm install --save-dev @types/chrome
```

**Custom Type Definitions**
```ts
// types/index.d.ts
declare global {
  interface Window {
    myExtensionData?: {
      version: string
    }
  }
}

// Message types
interface Message {
  action: string
  data?: unknown
}

interface WidgetClickMessage extends Message {
  action: 'widget-clicked'
  element: string
}

chrome.runtime.onMessage.addListener(
  (message: Message, sender, sendResponse) => {
    if (message.action === 'widget-clicked') {
      const msg = message as WidgetClickMessage
      console.log(msg.element)
    }
  }
)
```

### Build Setup

**Vite Config**
```ts
// vite.config.ts
import { defineConfig } from 'vite'
import { crx } from '@crxjs/vite-plugin'
import manifest from './manifest.json'

export default defineConfig({
  plugins: [
    crx({ manifest }),
  ],
  build: {
    rollupOptions: {
      input: {
        popup: 'src/popup/index.html',
        options: 'src/options/index.html',
        background: 'src/background/service-worker.ts',
        content: 'src/content/content.ts',
      },
    },
  },
})
```

**Webpack Config**
```js
// webpack.config.js
const path = require('path')
const CopyPlugin = require('copy-webpack-plugin')

module.exports = {
  entry: {
    popup: path.resolve(__dirname, 'src/popup/popup.ts'),
    background: path.resolve(__dirname, 'src/background/service-worker.ts'),
    content: path.resolve(__dirname, 'src/content/content.ts'),
  },
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].js',
    clean: true,
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js'],
  },
  plugins: [
    new CopyPlugin({
      patterns: [
        { from: 'public', to: '.' },
        { from: 'src/manifest.json', to: 'manifest.json' },
      ],
    }),
  ],
}
```

### Debugging

**Chrome DevTools**
```bash
# Open background script console
1. Go to chrome://extensions
2. Enable Developer Mode
3. Click "service worker" link

# Debug popup
1. Right-click popup icon
2. Select "Inspect"

# Debug content script
1. Open page DevTools (F12)
2. Check Sources > Content scripts
```

### Common Pitfalls

1. **Not handling async properly** → Always handle promises and callbacks
2. **Missing permissions** → Add required permissions in manifest
3. **CSP violations** → Be careful with inline scripts
4. **Service worker limitations** → No DOM access, terminates when idle
5. **Cross-browser differences** → Test on all target browsers
6. **MV2 to MV3 migration** → Use chrome.scripting instead of tabs.executeScript
7. **Not cleaning up** → Remove listeners and connections

### Best Practices

1. **Use Manifest V3** → Required for Chrome Web Store
2. **TypeScript** → Type safety catches errors early
3. **Minimal permissions** → Only request what you need
4. **Content Security Policy** → Secure your extension
5. **Error handling** → Handle all edge cases
6. **Background persistence** → Service workers can terminate
7. **Cross-browser testing** → Test on Chrome, Firefox, Edge, Safari
8. **Extension security** → Validate all inputs
9. **User privacy** → Don't collect unnecessary data
10. **Regular updates** → Keep dependencies and manifest updated

---

*Part of SuperAI GitHub - Centralized OpenCode Configuration*
