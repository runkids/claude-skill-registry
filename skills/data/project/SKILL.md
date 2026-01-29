---
name: project
description: Set up project structure and architecture following established patterns. Use when scaffolding new features, setting up new directories, or understanding the codebase architecture.
---

# Project Structure Guide

Complete project architecture following established patterns.

## Full Directory Structure

```
src/
├── app/                          # Expo Router (screens & navigation)
│   ├── _layout.tsx              # Root layout with providers
│   ├── index.tsx                # Entry point
│   ├── home.tsx                 # Home screen
│   ├── +not-found.tsx           # 404 fallback
│   ├── (auth)/                  # Auth route group
│   │   ├── _layout.tsx
│   │   ├── onboarding.tsx
│   │   └── login.tsx
│   ├── (main)/                  # Main feature route group
│   │   ├── _layout.tsx
│   │   ├── index.tsx
│   │   ├── new-item.tsx
│   │   ├── [id].tsx             # Dynamic route
│   │   └── components/          # Screen-specific components
│   │       ├── Setup/
│   │       ├── Details/
│   │       └── Insights/
│   └── (settings)/
│       ├── _layout.tsx
│       └── index.tsx
│
├── components/                   # Reusable UI components
│   ├── index.ts                 # Barrel exports
│   ├── Button/
│   │   └── index.tsx
│   ├── Input/
│   │   └── index.tsx
│   ├── Tab/
│   ├── Picker/
│   ├── DatePicker/
│   ├── TimePicker/
│   ├── Toast/
│   ├── BackButton/
│   ├── BottomSheetWrapper/
│   ├── KeyboardAwareWrapper/
│   ├── AuthenticationGuard/
│   ├── TermsAcceptanceModal/
│   └── FeatureSpecific/         # Complex components
│       ├── index.tsx
│       └── components/
│           └── SubComponent/
│
├── store/                        # Zustand state management
│   ├── index.ts                 # Store exports
│   ├── useMainStore.ts          # Main domain store
│   ├── useAppSettingsStore.ts   # App settings
│   └── useBiometricAuthStore.ts # Biometric auth
│
├── types/                        # TypeScript types
│   ├── local.ts                 # Local storage types
│   ├── domain.ts                # Domain types
│   └── store.ts                 # Store types
│
├── schema/                       # Zod validation schemas
│   └── feature.ts               # Feature schemas + defaults
│
├── hooks/                        # Custom React hooks
│   ├── use-color-scheme.ts
│   ├── use-color-scheme.web.ts  # Web-specific
│   ├── use-theme-color.ts
│   └── useFeatureHook.ts
│
├── lib/                          # Utilities & services
│   ├── utils.ts                 # General utilities (cn, formatters)
│   ├── store-utils.ts           # Store migrations & preprocessing
│   ├── notifications.ts         # Push notification setup
│   └── services/                # External service integrations
│       ├── api.ts
│       └── analytics.ts
│
├── context/                      # React Context (for non-persistent state)
│   └── AppContextProvider/
│       └── index.tsx
│
├── constants/                    # App constants
│   ├── theme.ts                 # SHADOWS, ANIMATION_DURATION
│   ├── common.ts                # URLs, versions, feature flags
│   └── message.ts               # Validation messages
│
├── assets/                       # Static assets
│   ├── images/
│   └── fonts/
│
└── global.css                   # Tailwind CSS + theme variables
```

## Key Files

### Root Layout (`src/app/_layout.tsx`)

```tsx
import React, { useEffect } from 'react';
import { useFonts } from 'expo-font';
import { Stack } from 'expo-router';
import * as SplashScreen from 'expo-splash-screen';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { ThemeProvider, DarkTheme, DefaultTheme } from '@react-navigation/native';
import { PortalProvider } from '@gorhom/bottom-sheet';

import { useColorScheme } from '@/hooks/use-color-scheme';
import { AuthenticationGuard, Toast, TermsAcceptanceModal } from '@/components';

import '../global.css';

SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
  const colorScheme = useColorScheme();
  const [fontsLoaded] = useFonts({ /* fonts */ });

  useEffect(() => {
    if (fontsLoaded) SplashScreen.hideAsync();
  }, [fontsLoaded]);

  if (!fontsLoaded) return null;

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <PortalProvider>
        <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
          <AuthenticationGuard>
            <Stack screenOptions={{ headerShown: false }} />
          </AuthenticationGuard>
          <TermsAcceptanceModal />
          <Toast />
        </ThemeProvider>
      </PortalProvider>
    </GestureHandlerRootView>
  );
}
```

### Global CSS (`src/global.css`)

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --background: 0 0% 100%;
  --foreground: 222 47% 11%;
  --card: 0 0% 100%;
  --primary: 174 35% 45%;
  --primary-foreground: 0 0% 100%;
  --secondary: 210 40% 96%;
  --secondary-foreground: 222 47% 11%;
  --muted: 210 40% 96%;
  --muted-foreground: 215 16% 47%;
  --destructive: 0 84% 60%;
  --destructive-foreground: 0 0% 100%;
  --border: 214 32% 91%;
}

.dark {
  --background: 222 47% 11%;
  --foreground: 210 40% 98%;
  --card: 222 47% 15%;
  --primary: 174 35% 50%;
  --muted-foreground: 215 20% 65%;
  --border: 217 33% 25%;
}
```

### Theme Constants (`src/constants/theme.ts`)

```tsx
export const SHADOWS = {
  calm: {
    shadowColor: '#292F3C',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.06,
    shadowRadius: 12,
    elevation: 3,
  },
  calmLg: { /* larger */ },
  calmXl: { /* even larger */ },
  none: { /* no shadow */ },
} as const;

export const ANIMATION_DURATION = {
  fast: 150,
  normal: 300,
  slow: 500,
} as const;
```

### Common Constants (`src/constants/common.ts`)

```tsx
export const MODAL_ANIMATION_DURATION = 300;
export const TERMS_VERSION = '01-01-2026';
export const TERMS_URL = 'https://yourapp.com/terms';
export const PRIVACY_URL = 'https://yourapp.com/privacy';
```

### Utils (`src/lib/utils.ts`)

```tsx
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export const cn = (...inputs: ClassValue[]) => twMerge(clsx(inputs));

export const formatCurrency = (amount: number, currency: string) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount);
};
```

### Component Index (`src/components/index.ts`)

```tsx
// UI Components
export { default as Button, type ButtonProps } from './Button';
export { default as Input } from './Input';
export { default as Tab, type Route } from './Tab';
export { default as Picker, type PickerOption } from './Picker';
export { default as DatePicker } from './DatePicker';
export { default as TimePicker } from './TimePicker';
export { default as Toast, showErrorToast } from './Toast';
export { default as BackButton } from './BackButton';

// Layout Components
export { default as BottomSheetWrapper } from './BottomSheetWrapper';
export { default as KeyboardAwareWrapper } from './KeyboardAwareWrapper';

// App Components
export { default as AuthenticationGuard } from './AuthenticationGuard';
export { default as TermsAcceptanceModal } from './TermsAcceptanceModal';
```

### Store Index (`src/store/index.ts`)

```tsx
export { useMainStore } from './useMainStore';
export { useAppSettingsStore } from './useAppSettingsStore';
export { useBiometricAuthStore } from './useBiometricAuthStore';
```

## New Feature Scaffolding

When adding a new feature, create:

1. **Types** (`src/types/feature.ts`)
2. **Schema** (`src/schema/feature.ts`)
3. **Store** (`src/store/useFeatureStore.ts`)
4. **Screens** (`src/app/(feature)/`)
5. **Components** (`src/components/Feature/` or `src/app/(feature)/components/`)

## Dependencies

```json
{
  "dependencies": {
    "expo": "~54.0.0",
    "expo-router": "~6.0.0",
    "react": "19.x",
    "react-native": "0.81.x",
    "nativewind": "^4.0.0",
    "zustand": "^5.0.0",
    "@react-native-async-storage/async-storage": "^2.0.0",
    "@gorhom/bottom-sheet": "^5.0.0",
    "react-native-reanimated": "^3.0.0",
    "react-native-gesture-handler": "^2.0.0",
    "react-native-safe-area-context": "^5.0.0",
    "react-hook-form": "^7.0.0",
    "@hookform/resolvers": "^3.0.0",
    "zod": "^3.0.0",
    "lucide-react-native": "^0.450.0",
    "react-native-svg": "^15.0.0",
    "react-native-modal": "^13.0.0",
    "@react-native-community/datetimepicker": "^8.0.0",
    "react-native-toast-message": "^2.0.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.0.0"
  }
}
```

## Tailwind Config (`tailwind.config.js`)

```js
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  presets: [require('nativewind/preset')],
  theme: {
    extend: {
      colors: {
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        card: 'hsl(var(--card))',
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))',
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))',
        },
        border: 'hsl(var(--border))',
      },
    },
  },
};
```

## Architecture Principles

1. **Local-First**: All data persisted to AsyncStorage
2. **Domain Stores**: Separate Zustand stores per domain
3. **Context for Transient State**: React Context for screen-level state
4. **File-Based Routing**: Expo Router with route groups
5. **NativeWind Styling**: Tailwind CSS with CSS variables
6. **Type Safety**: TypeScript + Zod validation
7. **Component Composition**: Small, focused components
8. **Barrel Exports**: Clean imports via index files
