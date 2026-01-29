---
name: screen
description: Generate Expo Router screens and navigation following established patterns. Use when creating new screens, pages, routes, layouts, tab navigation, or navigation structures.
---

# Screen Generator

Generate Expo Router screens following established patterns.

## Directory Structure

```
src/app/
├── _layout.tsx              # Root layout (providers, theme)
├── index.tsx                # Entry point (/)
├── home.tsx                 # Home screen (/home)
├── +not-found.tsx           # 404 fallback
├── (auth)/                  # Auth route group
│   ├── _layout.tsx
│   ├── onboarding.tsx
│   └── login.tsx
├── (main)/                  # Main app route group
│   ├── _layout.tsx          # Layout with providers
│   ├── index.tsx
│   ├── [id].tsx             # Dynamic route
│   └── components/          # Screen-specific components
│       ├── Setup/
│       ├── Details/
│       └── Insights/
├── (settings)/
│   ├── _layout.tsx
│   └── index.tsx
└── (modal)/
    └── event/
        └── [id].tsx
```

## Root Layout Pattern

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

const screenOptions = {
  headerShown: false,
  contentStyle: { backgroundColor: 'hsl(var(--background))' },
};

export default function RootLayout() {
  const colorScheme = useColorScheme();
  const [fontsLoaded] = useFonts({
    // Your fonts
  });

  useEffect(() => {
    if (fontsLoaded) {
      SplashScreen.hideAsync();
    }
  }, [fontsLoaded]);

  if (!fontsLoaded) return null;

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <PortalProvider>
        <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
          <AuthenticationGuard>
            <Stack screenOptions={screenOptions}>
              <Stack.Screen name="index" />
              <Stack.Screen name="home" />
              <Stack.Screen name="(auth)" />
              <Stack.Screen name="(main)" />
              <Stack.Screen name="(settings)" />
            </Stack>
          </AuthenticationGuard>
          <TermsAcceptanceModal />
          <Toast />
        </ThemeProvider>
      </PortalProvider>
    </GestureHandlerRootView>
  );
}
```

## Group Layout with Context Provider

```tsx
import React from 'react';
import { Stack } from 'expo-router';

import { AppContextProvider } from '@/context/AppContextProvider';
import { KeyboardAwareWrapper } from '@/components';

export default function MainLayout() {
  return (
    <AppContextProvider>
      <KeyboardAwareWrapper>
        <Stack
          screenOptions={{
            headerShown: false,
            contentStyle: { backgroundColor: 'hsl(var(--background))' },
          }}
        >
          <Stack.Screen name="index" />
          <Stack.Screen name="new-item" />
          <Stack.Screen name="[id]" />
        </Stack>
      </KeyboardAwareWrapper>
    </AppContextProvider>
  );
}
```

## Tab Navigation Layout

```tsx
import React from 'react';
import { Tabs } from 'expo-router';
import { Home, List, Settings, Map, User } from 'lucide-react-native';

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: 'hsl(var(--primary))',
        tabBarInactiveTintColor: 'hsl(var(--muted-foreground))',
        tabBarStyle: {
          backgroundColor: 'hsl(var(--background))',
          borderTopColor: 'hsl(var(--border))',
        },
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          tabBarIcon: ({ color, size }) => <Home color={color} size={size} />,
        }}
      />
      <Tabs.Screen
        name="list"
        options={{
          title: 'List',
          tabBarIcon: ({ color, size }) => <List color={color} size={size} />,
        }}
      />
      <Tabs.Screen
        name="settings"
        options={{
          title: 'Settings',
          tabBarIcon: ({ color, size }) => <Settings color={color} size={size} />,
        }}
      />
    </Tabs>
  );
}
```

## Screen with Custom Tab Component

```tsx
import React, { useState } from 'react';
import { View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { SceneMap } from 'react-native-tab-view';

import { Tab } from '@/components';
import SetupTab from './components/Setup';
import ScheduleTab from './components/Schedule';
import InsightsTab from './components/Insights';

const routes = [
  { key: 'setup', title: 'Setup' },
  { key: 'schedule', title: 'Schedule' },
  { key: 'insights', title: 'Insights' },
];

const renderScene = SceneMap({
  setup: SetupTab,
  schedule: ScheduleTab,
  insights: InsightsTab,
});

const TabbedScreen = () => {
  const [activeTabIndex, setActiveTabIndex] = useState(0);

  return (
    <SafeAreaView className="flex-1 bg-background">
      <View className="px-4 pt-4">
        <Tab
          activeTabIndex={activeTabIndex}
          routes={routes}
          onTabPress={setActiveTabIndex}
          variant="rounded"
        />
      </View>
      {renderScene({ route: routes[activeTabIndex] })}
    </SafeAreaView>
  );
};

export default TabbedScreen;
```

## Screen Template

```tsx
import React from 'react';
import { View, Text, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';

import { Button, BackButton } from '@/components';

const MyScreen = () => {
  const router = useRouter();

  return (
    <SafeAreaView className="flex-1 bg-background">
      <BackButton />
      <ScrollView className="flex-1 px-4 pt-20">
        <Text className="text-2xl font-bold text-foreground">Screen Title</Text>
        {/* Content */}
        <Button
          title="Next"
          onPress={() => router.push('/next-screen')}
          className="mt-4"
        />
      </ScrollView>
    </SafeAreaView>
  );
};

export default MyScreen;
```

## Dynamic Route Screen

```tsx
import React, { useEffect } from 'react';
import { View, Text, ActivityIndicator } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useLocalSearchParams, useRouter } from 'expo-router';

import { BackButton } from '@/components';
import { useMyStore } from '@/store/useMyStore';

const DetailScreen = () => {
  const router = useRouter();
  const { id } = useLocalSearchParams<{ id: string }>();
  const { item, loadItem, isLoading } = useMyStore();

  useEffect(() => {
    if (id) {
      loadItem(id);
    }
  }, [id]);

  if (isLoading) {
    return (
      <SafeAreaView className="flex-1 items-center justify-center bg-background">
        <ActivityIndicator size="large" color="hsl(var(--primary))" />
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView className="flex-1 bg-background">
      <BackButton />
      <View className="flex-1 px-4 pt-20">
        <Text className="text-2xl font-bold text-foreground">{item?.title}</Text>
      </View>
    </SafeAreaView>
  );
};

export default DetailScreen;
```

## Navigation Methods

```tsx
import { useRouter, useLocalSearchParams, useSegments } from 'expo-router';

const router = useRouter();

// Push
router.push('/profile');
router.push('/(main)/details');
router.push(`/(main)/${id}`);
router.push({ pathname: '/(main)/[id]', params: { id: '123' } });

// Replace
router.replace('/home');

// Back
router.back();

// Params
const { id } = useLocalSearchParams<{ id: string }>();

// Segments
const segments = useSegments();
```

## Route Groups

```
(auth)/     - Authentication flows (login, register, onboarding)
(main)/     - Main app screens
(tabs)/     - Tab navigation
(settings)/ - Settings screens
(modal)/    - Modal presentations
```

## Checklist

- [ ] Screen in `src/app/` with correct routing
- [ ] Route group `(groupName)/` if needed
- [ ] Layout `_layout.tsx` with providers
- [ ] `SafeAreaView` from `react-native-safe-area-context`
- [ ] NativeWind classes for styling
- [ ] `BackButton` for navigable screens
- [ ] Loading state with `ActivityIndicator`
- [ ] Dynamic params typed: `useLocalSearchParams<{ id: string }>`
