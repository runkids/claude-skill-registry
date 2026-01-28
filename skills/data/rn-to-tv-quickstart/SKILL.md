---
name: rn-to-tv-quickstart
displayName: "RN to TV Quick Start"
description: "Quick start guide for experienced React Native developers transitioning to TV app development. Covers Fire OS, Android TV, Apple TV (tvOS), Vega OS, and Web TV platforms. Focuses on what's different from mobile: spatial navigation, remote controls, focus management, and 10-foot UI patterns. Skip the basics - get your first TV app running fast."
keywords: ["getting-started", "quickstart", "mobile-to-tv", "transition", "first-tv-app", "new-to-tv", "beginner-tv", "setup-guide", "react-native-tv"]
author: "Giovanni Laquidara"
---

# React Native to TV: Quick Start Guide

You know React Native. Here's what's different for TV.

**Official Docs:**
- Expo TV: https://docs.expo.dev/guides/building-for-tv/
- Vega SDK: https://developer.amazon.com/docs/vega/latest/build-apps-overview.html

---

## The Big 5 Differences from Mobile

### 1. No Touch - Everything is Remote/D-pad

On mobile: Users tap buttons
On TV: Users navigate with D-pad (up/down/left/right) + select

```typescript
// Mobile: TouchableOpacity, Pressable just work
// TV: You need spatial navigation

import { useFocusable } from 'react-tv-space-navigation';

const TVButton = ({ onPress, children }) => {
  const { ref, focused } = useFocusable({ onEnterPress: onPress });

  return (
    <View ref={ref} style={[styles.button, focused && styles.focused]}>
      {children}
    </View>
  );
};
```

**Key library**: [react-tv-space-navigation](https://github.com/bamlab/react-tv-space-navigation)

### 2. Focus is King

Every interactive element MUST have a visible focus state. Users can't tap what they can't see.

```typescript
const styles = StyleSheet.create({
  button: {
    padding: 16,
    backgroundColor: '#333',
  },
  // CRITICAL: Always show what's focused
  focused: {
    backgroundColor: '#555',
    borderWidth: 3,
    borderColor: '#fff',
    transform: [{ scale: 1.05 }],
  },
});
```

### 3. 10-Foot UI (Bigger Everything)

Users sit 10 feet away. What works on mobile is too small.

| Element | Mobile | TV |
|---------|--------|-----|
| Body text | 14-16px | 24-32px |
| Buttons | 44px height | 60-80px height |
| Touch targets | 44x44px | 80x80px+ |
| Margins | 16px | 48px+ |

### 4. Safe Zones (TV Overscan)

TVs crop edges. Keep content away from borders.

```typescript
const safeZones = {
  horizontal: 48,  // Left/right padding
  vertical: 27,    // Top/bottom padding
};
```

### 5. Landscape Only

TV apps are always landscape. Configure in app.json:
```json
{ "expo": { "orientation": "landscape" } }
```

---

## Platform Quick Reference

| Platform | Technology | Remote Events |
|----------|------------|---------------|
| Android TV | Expo + react-native-tvos | KeyEvent |
| Apple TV | Expo + react-native-tvos | TVEventHandler |
| Fire TV FOS | Expo + react-native-tvos | KeyEvent |
| Fire TV Vega | Amazon Vega SDK | Kepler TVEventHandler |
| Web TV | React Native Web | Keyboard events |

---

## Prerequisites

### For Android TV / Fire TV (Fire OS)
- Node.js LTS (macOS or Linux)
- Android Studio Iguana or later
- Android SDK API 31+ with TV system image
- Android TV emulator configured

### For Apple TV (tvOS)
- Node.js LTS on macOS
- Xcode 16+
- tvOS SDK 17+ (install via `xcodebuild -downloadAllPlatforms`)

### For Fire TV Vega OS
- Amazon Vega SDK installed (see Vega section below)

---

## Complete Project Setup

This guide creates a production-ready monorepo structure supporting all TV platforms.

> **Claude will ask for your app name and package ID when setting up.**

### Step 1: Create Monorepo Structure

```bash
# Create project root
mkdir <PROJECT_NAME> && cd <PROJECT_NAME>

# Initialize Yarn
yarn init -y
yarn set version stable

# Create directory structure
mkdir -p apps packages/shared-ui/src
```

### Step 2: Configure Root package.json

Create `package.json`:
```json
{
  "name": "@<PROJECT_NAME>/monorepo",
  "version": "1.0.0",
  "private": true,
  "packageManager": "yarn@4.5.0",
  "workspaces": [
    "apps/*",
    "packages/*"
  ],
  "scripts": {
    "dev": "yarn workspace @<PROJECT_NAME>/expo-multi-tv start",
    "dev:android": "yarn workspace @<PROJECT_NAME>/expo-multi-tv android",
    "dev:ios": "yarn workspace @<PROJECT_NAME>/expo-multi-tv ios",
    "dev:web": "yarn workspace @<PROJECT_NAME>/expo-multi-tv web",
    "dev:vega": "yarn workspace @<PROJECT_NAME>/vega start",
    "build:vega": "yarn workspace @<PROJECT_NAME>/vega build",
    "lint:all": "yarn workspaces foreach -pt run lint",
    "typecheck": "yarn workspaces foreach -pt run typecheck"
  },
  "resolutions": {
    "metro-source-map": "0.80.12"
  }
}
```

> **CRITICAL**: The `metro-source-map` resolution fixes babel plugin errors in monorepos.

### Step 3: Create Shared TypeScript Config

Create `tsconfig.base.json`:
```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "CommonJS",
    "lib": ["ES2021"],
    "jsx": "react-native",
    "strict": true,
    "moduleResolution": "node",
    "allowSyntheticDefaultImports": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true
  }
}
```

### Step 4: Create Root Babel Config

Create `babel.config.js`:
```javascript
const path = require('path');

module.exports = function (api) {
  api.cache(true);

  let reanimatedPlugin;
  try {
    reanimatedPlugin = require.resolve('react-native-reanimated/plugin', {
      paths: [path.join(__dirname, 'apps/expo-multi-tv/node_modules')]
    });
  } catch (e) {
    reanimatedPlugin = null;
  }

  return {
    presets: ['babel-preset-expo'],
    plugins: reanimatedPlugin ? [reanimatedPlugin] : [],
  };
};
```

### Step 5: Create Expo TV App

```bash
cd apps

# Create Expo TV project
npx create-expo-app@latest expo-multi-tv -e with-tv

cd expo-multi-tv
```

Update `apps/expo-multi-tv/package.json`:
```json
{
  "name": "@<PROJECT_NAME>/expo-multi-tv",
  "dependencies": {
    "@<PROJECT_NAME>/shared-ui": "*"
  }
}
```

Create `apps/expo-multi-tv/metro.config.js`:
```javascript
const { getDefaultConfig } = require('expo/metro-config');
const path = require('path');

const projectRoot = __dirname;
const workspaceRoot = path.resolve(projectRoot, '../..');

const config = getDefaultConfig(projectRoot);

config.watchFolders = [workspaceRoot];
config.resolver.nodeModulesPaths = [
  path.resolve(projectRoot, 'node_modules'),
  path.resolve(workspaceRoot, 'node_modules'),
];

module.exports = config;
```

### Step 6: Add Vega App (Fire TV Vega OS)

```bash
# Create and enter vega directory first (files generate in current directory)
mkdir -p apps/vega
cd apps/vega

# Generate Vega project
vega project generate -n <APP_NAME> --template helloWorld

npm install
```

Update `apps/vega/package.json`:
```json
{
  "name": "@<PROJECT_NAME>/vega",
  "dependencies": {
    "@<PROJECT_NAME>/shared-ui": "*"
  }
}
```

Create `apps/vega/metro.config.js`:
```javascript
const path = require('path');
const { getDefaultConfig, mergeConfig } = require('@react-native/metro-config');

const projectRoot = __dirname;
const workspaceRoot = path.resolve(projectRoot, '../..');

const config = {
  watchFolders: [workspaceRoot],
  resolver: {
    nodeModulesPaths: [
      path.resolve(projectRoot, 'node_modules'),
      path.resolve(workspaceRoot, 'node_modules'),
    ],
    sourceExts: ['kepler.tsx', 'kepler.ts', 'tsx', 'ts', 'js', 'jsx', 'json'],
  },
};

module.exports = mergeConfig(getDefaultConfig(__dirname), config);
```

### Step 7: Create Shared UI Package

Create `packages/shared-ui/package.json`:
```json
{
  "name": "@<PROJECT_NAME>/shared-ui",
  "version": "1.0.0",
  "main": "src/index.ts",
  "types": "src/index.ts",
  "peerDependencies": {
    "react": "*",
    "react-native": "*"
  }
}
```

Create `packages/shared-ui/tsconfig.json`:
```json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "./dist"
  },
  "include": ["src/**/*"]
}
```

Create `packages/shared-ui/src/index.ts`:
```typescript
// Theme
export * from './theme';

// Components
export * from './components/FocusablePressable';

// Hooks
export * from './hooks/useScale';
```

### Step 8: Create Theme System

Create `packages/shared-ui/src/theme/index.ts`:
```typescript
export const colors = {
  primary: '#E50914',
  background: '#141414',
  card: '#2F2F2F',
  text: '#FFFFFF',
  textSecondary: '#B3B3B3',
};

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};

export const safeZones = {
  horizontal: 48,
  vertical: 27,
};
```

### Step 9: Create useScale Hook

Create `packages/shared-ui/src/hooks/useScale.ts`:
```typescript
import { Dimensions } from 'react-native';

const BASE_WIDTH = 1920;
const BASE_HEIGHT = 1080;

export const useScale = () => {
  const { width, height } = Dimensions.get('window');
  const scaleWidth = width / BASE_WIDTH;
  const scaleHeight = height / BASE_HEIGHT;
  const scale = Math.min(scaleWidth, scaleHeight);

  return {
    scale: (size: number) => size * scale,
    width,
    height,
  };
};
```

### Step 10: Create FocusablePressable Component

Create `packages/shared-ui/src/components/FocusablePressable.tsx`:
```typescript
import React from 'react';
import { View, StyleSheet, ViewStyle } from 'react-native';
import { useFocusable } from 'react-tv-space-navigation';

interface FocusablePressableProps {
  children: React.ReactNode;
  onPress?: () => void;
  style?: ViewStyle;
  focusedStyle?: ViewStyle;
}

export const FocusablePressable: React.FC<FocusablePressableProps> = ({
  children,
  onPress,
  style,
  focusedStyle,
}) => {
  const { ref, focused } = useFocusable({
    onEnterPress: onPress,
  });

  return (
    <View
      ref={ref}
      style={[
        styles.container,
        style,
        focused && styles.focused,
        focused && focusedStyle,
      ]}
    >
      {children}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 16,
  },
  focused: {
    borderWidth: 3,
    borderColor: '#fff',
    transform: [{ scale: 1.05 }],
  },
});
```

### Step 11: Install Dependencies and Run

```bash
# From project root
cd ../..
yarn install

# Run on platforms
yarn dev:android    # Android TV / Fire TV FOS
yarn dev:ios        # Apple TV
yarn dev:web        # Web TV
yarn dev:vega       # Fire TV Vega OS
```

---

## Final Project Structure

```
<PROJECT_NAME>/
├── apps/
│   ├── expo-multi-tv/      # Android TV, Apple TV, Fire TV FOS, Web
│   │   ├── App.tsx         # Main app entry point
│   │   ├── app.json
│   │   ├── metro.config.js
│   │   └── package.json
│   └── vega/               # Fire TV Vega OS
│       ├── App.tsx
│       ├── metro.config.js
│       └── package.json
├── packages/
│   └── shared-ui/          # Shared components & utilities
│       ├── src/
│       │   ├── components/
│       │   ├── hooks/
│       │   ├── theme/
│       │   └── index.ts
│       ├── package.json
│       └── tsconfig.json
├── babel.config.js
├── package.json
├── tsconfig.base.json
└── yarn.lock
```

---

## Platform-Specific File Resolution

Metro bundler automatically resolves platform files:
- `.kepler.ts/tsx` - Fire TV Vega OS (highest priority for Vega)
- `.android.ts/tsx` - Android TV & Fire TV Fire OS
- `.ios.ts/tsx` - Apple TV (tvOS)
- `.web.ts/tsx` - Web platforms
- `.ts/tsx` - Default/shared implementation

**Example:**
```
RemoteControlManager.android.ts  → Android TV / Fire TV FOS
RemoteControlManager.ios.ts      → Apple TV
RemoteControlManager.kepler.ts   → Fire TV Vega
```

---

## Build Commands

### Expo TV App (Android TV, Apple TV, Fire TV FOS, Web)

```bash
yarn dev:android    # Run on Android TV emulator
yarn dev:ios        # Run on Apple TV simulator
yarn dev:web        # Run in browser

# Production builds
npx expo build:android
npx expo build:ios
npx expo export --platform web
```

### Vega App (Fire TV Vega OS)

```bash
yarn dev:vega       # Start Metro for Vega

# Build VPKG
vega build --arch armv7 --buildType release     # Fire TV Stick
vega build --arch aarch64 --buildType release   # Fire TV (ARM64)
vega build --arch x86_64 --buildType debug      # Virtual devices

# Deploy
vega device list
vega install --vpkg build/armv7-release/<APP_NAME>.vpkg
vega run --packageId <PACKAGE_ID>
```

---

## Common Mistakes (Don't Do These)

### ❌ Using Pressable without Focus Management
```typescript
// WRONG
<Pressable onPress={handlePress}><Text>Click</Text></Pressable>

// RIGHT - Use FocusablePressable from shared-ui
<FocusablePressable onPress={handlePress}><Text>Select</Text></FocusablePressable>
```

### ❌ Forgetting Safe Zones
```typescript
// WRONG - Content at edges
<View style={{ position: 'absolute', top: 0, left: 0 }}>

// RIGHT
<View style={{ position: 'absolute', top: 27, left: 48 }}>
```

### ❌ Small Touch Targets
```typescript
// WRONG - Too small for TV
<View style={{ width: 44, height: 44 }} />

// RIGHT
<View style={{ width: 80, height: 80 }} />
```

---

## Testing Your TV App

### Android TV
```bash
# In Android Studio: Tools > Device Manager > Create Device > TV
yarn dev:android
```

### Apple TV
```bash
# In Xcode: Window > Devices and Simulators > Simulators
yarn dev:ios
```

### Web (with keyboard)
```bash
yarn dev:web
# Navigate with arrow keys, Enter to select
```

### Physical Devices
- Android TV: Enable developer mode, connect via ADB
- Fire TV: Enable ADB debugging in Settings
- Apple TV: Connect via Xcode

---

## Next Steps

1. **Add screens** - Create screens in `packages/shared-ui/src/screens/`
2. **Add navigation** - Set up React Navigation in shared-ui
3. **Add video player** - Use react-native-video (Expo) or VideoView (Vega)
4. **Handle remote events** - Create platform-specific RemoteControlManagers
5. **Test on real hardware** - Emulators don't show real performance

## Need More?

- **Full knowledge base**: Use the `multi-tv-builder` skill
- **Apple TV issues**: Use the `apple-tv-troubleshooter` skill
- **Movie/TV data API**: Use the `tmdb-integration` skill

## Reference Implementation

For a complete working example with all features implemented:
- **Sample repo**: https://github.com/AmazonAppDev/react-native-multi-tv-app-sample

Use this as a reference to see advanced patterns like video playback, navigation, and remote control handling.
