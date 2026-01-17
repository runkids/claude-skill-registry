---
name: react-native
description: React Native mobile development with core components, navigation, and platform-specific patterns
license: MIT
compatibility: opencode
---

# React Native Skill

Comprehensive patterns and best practices for React Native mobile development.

## What I Know

### Project Structure

```
src/
├── components/
│   ├── common/          # Reusable UI components
│   └── features/        # Feature-specific components
├── screens/             # Screen components
├── navigation/          # Navigation configuration
├── hooks/               # Custom hooks
├── services/            # API services
├── store/               # State management
├── utils/               # Helper functions
├── constants/           # App constants
├── types/               # TypeScript types
├── assets/              # Images, fonts, etc.
└── theme/               # Colors, fonts, spacing
```

### Core Components

**View & Text**
```tsx
import { View, Text, StyleSheet } from 'react-native'

export function UserProfile() {
  return (
    <View style={styles.container}>
      <Text style={styles.name}>John Doe</Text>
      <Text style={styles.email}>john@example.com</Text>
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#fff',
  },
  name: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#000',
  },
  email: {
    fontSize: 16,
    color: '#666',
    marginTop: 4,
  },
})
```

**ScrollView & FlatList**
```tsx
import { ScrollView, FlatList } from 'react-native'

// ScrollView for small lists
export function ScrollContent() {
  return (
    <ScrollView>
      {[1, 2, 3, 4, 5].map(item => (
        <View key={item} style={{ height: 100, marginBottom: 10 }} />
      ))}
    </ScrollView>
  )
}

// FlatList for large/unknown lists (preferred)
export function ListContent() {
  const data = Array.from({ length: 100 }, (_, i) => ({ id: i, title: `Item ${i}` }))

  return (
    <FlatList
      data={data}
      keyExtractor={(item) => item.id.toString()}
      renderItem={({ item }) => (
        <View style={{ padding: 16 }}>
          <Text>{item.title}</Text>
        </View>
      )}
      ItemSeparatorComponent={() => <View style={{ height: 1, backgroundColor: '#eee' }} />}
      ListEmptyComponent={<Text>No items</Text>}
      onRefresh={handleRefresh}
      refreshing={isRefreshing}
    />
  )
}
```

**Pressable & TouchableOpacity**
```tsx
import { Pressable, Text, StyleSheet } from 'react-native'

export function Button({ onPress, title }: { onPress: () => void; title: string }) {
  return (
    <Pressable
      onPress={onPress}
      style={({ pressed }) => [
        styles.button,
        pressed && styles.buttonPressed,
      ]}
    >
      <Text style={styles.buttonText}>{title}</Text>
    </Pressable>
  )
}

const styles = StyleSheet.create({
  button: {
    backgroundColor: '#007AFF',
    padding: 16,
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonPressed: {
    backgroundColor: '#0056CC',
  },
  buttonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
})
```

**Image**
```tsx
import { Image, View } from 'react-native'

export function ImageExample() {
  return (
    <View>
      {/* Local image */}
      <Image
        source={require('../assets/logo.png')}
        style={{ width: 100, height: 100 }}
      />

      {/* Remote image with caching */}
      <Image
        source={{ uri: 'https://example.com/image.jpg' }}
        style={{ width: 200, height: 200 }}
        resizeMode="cover"
      />

      {/* With loading and error */}
      <Image
        source={{ uri: imageUrl }}
        style={{ width: '100%', height: 200 }}
        defaultSource={require('../assets/placeholder.png')}
      />
    </View>
  )
}
```

**TextInput**
```tsx
import { TextInput, View, Text } from 'react-native'
import { useState } from 'react'

export function FormInput() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  return (
    <View>
      <TextInput
        value={email}
        onChangeText={setEmail}
        placeholder="Email"
        keyboardType="email-address"
        autoCapitalize="none"
        style={styles.input}
      />

      <TextInput
        value={password}
        onChangeText={setPassword}
        placeholder="Password"
        secureTextEntry
        style={styles.input}
      />
    </View>
  )
}

const styles = StyleSheet.create({
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
  },
})
```

**ActivityIndicator**
```tsx
import { ActivityIndicator, View } from 'react-native'

export function LoadingSpinner({ size = 'large' as const }) {
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <ActivityIndicator size={size} color="#007AFF" />
    </View>
  )
}
```

### Navigation (React Navigation)

**Stack Navigation**
```tsx
// navigation/AppNavigator.tsx
import { NavigationContainer } from '@react-navigation/native'
import { createStackNavigator } from '@react-navigation/stack'
import { HomeScreen } from '../screens/HomeScreen'
import { DetailsScreen } from '../screens/DetailsScreen'

const Stack = createStackNavigator()

export function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="Home"
        screenOptions={{
          headerStyle: { backgroundColor: '#007AFF' },
          headerTintColor: '#fff',
          headerTitleStyle: { fontWeight: 'bold' },
        }}
      >
        <Stack.Screen name="Home" component={HomeScreen} options={{ title: 'Home' }} />
        <Stack.Screen
          name="Details"
          component={DetailsScreen}
          options={({ route }) => ({ title: route.params.title })}
        />
      </Stack.Navigator>
    </NavigationContainer>
  )
}
```

**Tab Navigation**
```tsx
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs'
import { HomeScreen } from '../screens/HomeScreen'
import { ProfileScreen } from '../screens/ProfileScreen'
import { SettingsScreen } from '../screens/SettingsScreen'

const Tab = createBottomTabNavigator()

export function TabNavigator() {
  return (
    <Tab.Navigator
      screenOptions={{
        tabBarActiveTintColor: '#007AFF',
        tabBarInactiveTintColor: '#999',
      }}
    >
      <Tab.Screen
        name="Home"
        component={HomeScreen}
        options={{
          tabBarIcon: ({ color, size }) => <HomeIcon color={color} size={size} />,
        }}
      />
      <Tab.Screen name="Profile" component={ProfileScreen} />
      <Tab.Screen name="Settings" component={SettingsScreen} />
    </Tab.Navigator>
  )
}
```

**Drawer Navigation**
```tsx
import { createDrawerNavigator } from '@react-navigation/drawer'

const Drawer = createDrawerNavigator()

export function DrawerNavigator() {
  return (
    <Drawer.Navigator
      screenOptions={{
        drawerStyle: { width: 280 },
        drawerPosition: 'left',
      }}
    >
      <Drawer.Screen name="Home" component={HomeScreen} />
      <Drawer.Screen name="Profile" component={ProfileScreen} />
    </Drawer.Navigator>
  )
}
```

**Navigation Helper Functions**
```tsx
// navigation/useNavigation.ts
import { useNavigation as useReactNavigation } from '@react-navigation/native'
import type { StackNavigationProp } from '@react-navigation/stack'

export function useNavigation() {
  return useReactNavigation<StackNavigationProp<any>>
}

// Usage in component
export function MyComponent() {
  const navigation = useNavigation()

  const navigateToDetails = () => {
    navigation.navigate('Details', { id: 123, title: 'My Details' })
  }

  const goBack = () => {
    navigation.goBack()
  }

  const replace = () => {
    navigation.replace('Login')
  }

  return <Button onPress={navigateToDetails} title="Go to Details" />
}
```

### State Management

**Context API**
```tsx
// store/AuthContext.tsx
import { createContext, useContext, useState, ReactNode } from 'react'

interface AuthContextType {
  user: User | null
  login: (email: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)

  const login = async (email: string, password: string) => {
    const userData = await api.login(email, password)
    setUser(userData)
  }

  const logout = () => {
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within AuthProvider')
  return context
}
```

**Zustand (Simple Store)**
```tsx
// store/useStore.ts
import create from 'zustand'

interface UserStore {
  user: User | null
  setUser: (user: User) => void
  clearUser: () => void
}

export const useUserStore = create<UserStore>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  clearUser: () => set({ user: null }),
}))
```

### Custom Hooks

**useAsync (Data Fetching)**
```tsx
// hooks/useAsync.ts
import { useState, useEffect } from 'react'

export function useAsync<T>(
  asyncFunction: () => Promise<T>,
  dependencies: any[] = []
) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    let isMounted = true

    const fetchData = async () => {
      try {
        setLoading(true)
        const result = await asyncFunction()
        if (isMounted) setData(result)
      } catch (err) {
        if (isMounted) setError(err as Error)
      } finally {
        if (isMounted) setLoading(false)
      }
    }

    fetchData()

    return () => { isMounted = false }
  }, dependencies)

  return { data, loading, error }
}
```

**useLocalStorage**
```tsx
// hooks/useLocalStorage.ts
import { useState, useEffect } from 'react'
import AsyncStorage from '@react-native-async-storage/async-storage'

export function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(initialValue)

  useEffect(() => {
    AsyncStorage.getItem(key).then(stored => {
      if (stored !== null) setValue(JSON.parse(stored))
    })
  }, [key])

  const setStoredValue = async (newValue: T) => {
    setValue(newValue)
    await AsyncStorage.setItem(key, JSON.stringify(newValue))
  }

  return [value, setStoredValue] as const
}
```

### Platform-Specific Code

**Platform Module**
```tsx
import { Platform, StyleSheet, StatusBar } from 'react-native'

export function PlatformComponent() {
  return (
    <View style={styles.container}>
      <StatusBar barStyle={Platform.OS === 'ios' ? 'dark-content' : 'light-content'} />
      <Text>Running on {Platform.OS}</Text>

      {Platform.OS === 'ios' && <Text>iOS specific component</Text>}
      {Platform.OS === 'android' && <Text>Android specific component</Text>}
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: Platform.OS === 'ios' ? 44 : 0, // iOS notch handling
  },
})
```

**Platform.select()**
```tsx
import { Platform } from 'react-native'

const styles = StyleSheet.create({
  container: {
    ...Platform.select({
      ios: { shadowColor: '#000', shadowOffset: { width: 0, height: 2 } },
      android: { elevation: 4 },
    }),
  },
})

const component = Platform.select({
  ios: () => require('./IOSComponent'),
  android: () => require('./AndroidComponent'),
})()
```

### Styling

**StyleSheet**
```tsx
import { StyleSheet } from 'react-native'

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    padding: 16,
  },
  text: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    lineHeight: 24,
  },
  // Flexbox
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  centered: {
    justifyContent: 'center',
    alignItems: 'center',
  },
})
```

**Theme System**
```tsx
// theme/colors.ts
export const Colors = {
  light: {
    primary: '#007AFF',
    secondary: '#5856D6',
    background: '#FFFFFF',
    text: '#000000',
    border: '#E5E5E5',
  },
  dark: {
    primary: '#0A84FF',
    secondary: '#5E5CE6',
    background: '#000000',
    text: '#FFFFFF',
    border: '#333333',
  },
}

// theme/useTheme.ts
import { useColorScheme } from 'react-native'

export function useTheme() {
  const colorScheme = useColorScheme()
  return Colors[colorScheme === 'dark' ? 'dark' : 'light']
}
```

### API Integration

**API Service**
```tsx
// services/api.ts
const BASE_URL = 'https://api.example.com'

export const api = {
  async get<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${BASE_URL}${endpoint}`)
    if (!response.ok) throw new Error('API Error')
    return response.json()
  },

  async post<T>(endpoint: string, data: any): Promise<T> {
    const response = await fetch(`${BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    if (!response.ok) throw new Error('API Error')
    return response.json()
  },
}
```

**Axios with Interceptors**
```tsx
// services/axios.ts
import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'https://api.example.com',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
})

// Request interceptor for auth
apiClient.interceptors.request.use(
  (config) => {
    const token = AsyncStorage.getItem('token')
    if (token) config.headers.Authorization = `Bearer ${token}`
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle auth error
    }
    return Promise.reject(error)
  }
)
```

### Permissions

**React Native Permissions**
```tsx
import { check, request, PERMISSIONS, RESULTS } from 'react-native-permissions'

export async function requestLocationPermission() {
  const permission = Platform.OS === 'ios'
    ? PERMISSIONS.IOS.LOCATION_WHEN_IN_USE
    : PERMISSIONS.ANDROID.ACCESS_FINE_LOCATION

  const result = await check(permission)

  if (result === RESULTS.GRANTED) return true

  const requestResult = await request(permission)
  return requestResult === RESULTS.GRANTED
}
```

### Safe Area View

**Safe Area Handling**
```tsx
import { SafeAreaView, useSafeAreaInsets } from 'react-native-safe-area-context'

export function SafeScreen() {
  const insets = useSafeAreaInsets()

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: '#fff' }}>
      <View style={{ paddingTop: insets.top, paddingBottom: insets.bottom }}>
        {/* Content */}
      </View>
    </SafeAreaView>
  )
}
```

### Common Pitfalls

1. **Not using FlatList** → Use FlatList instead of ScrollView with map for long lists
2. **Missing key prop** → Always provide unique key for list items
3. **Inline styles** → Use StyleSheet.create for performance
4. **Forgetting platform differences** → Test on both iOS and Android
5. **Not handling SafeArea** → Use SafeAreaView for notched devices
6. **State updates on unmounted components** → Clean up effects properly
7. **Blocking main thread** → Offload heavy computations
8. **Not optimizing images** → Use proper image sizes and formats

### Best Practices

1. **Use TypeScript** → Type safety catches bugs early
2. **Component organization** → Keep components small and focused
3. **Custom hooks** → Extract reusable logic
4. **Navigation types** → Type your navigation props
5. **Platform considerations** → Handle iOS/Android differences
6. **Performance** → Use FlatList, avoid inline functions
7. **Accessibility** → Add accessibilityLabel and hints
8. **Error handling** → Handle API errors gracefully
9. **Security** → Secure sensitive data with Keychain/Keystore
10. **Testing** → Write unit and E2E tests with Detox

## Version Notes

### Supported Versions
- **Recommended:** React Native 0.80+ (latest stable)
- **Minimum:** React Native 0.70+ (New Architecture ready)

### Version Summary

| Version | Release Date | Key Features |
|---------|--------------|--------------|
| 0.83 | Dec 2025 | New Architecture default, improved perf, Hermes enhancements |
| 0.80+ | 2025 | New Architecture stable, App Registry changes |
| 0.76 | Nov 2024 | New Architecture stable, Systrace improvements |
| 0.74 | 2024 | React 18.2, improved Metro, Yoga 3.0 |
| 0.72 | 2023 | New Architecture alpha, improved dark mode |

### Recent Breaking Changes

#### React Native 0.80 → 0.83
<!-- 🆕 v0.83: New Architecture default -->
```tsx
// v0.83+: New Architecture enabled by default
// No config changes needed for new projects
// Legacy projects can still opt-out
```

<!-- 🔄 v0.80+: App Registry changes -->
```tsx
// v0.80+: New registration API
import { registerRootComponent } from 'expo'

// Before: AppRegistry.registerComponent('app', () => App)
// Now: registerRootComponent(App)
```

#### React Native 0.76 → 0.80
<!-- 🆕 v0.76: New Architecture stable -->
```bash
# v0.76+: New Architecture (Fabric/TurboModules) is stable
# Enable in gradle properties:
# NewArchitectureEnabled=true

# v0.80+: Enabled by default, no flag needed
```

<!-- 🆕 v0.76: Hermes improvements -->
```bash
# v0.76+: Hermes is the default and only supported engine
# Significant performance improvements
# Better debugging support
```

<!-- 🔄 v0.76: Yoga 3.0 -->
```tsx
// v0.76+: Yoga 3.0 with improved layout
// Better handling of complex layouts
// Reduced layout passes
```

#### React Native 0.74 → 0.76
<!-- 🆕 v0.74: React 18.2 built-in -->
```tsx
// v0.74+: React 18.2 features available
import { StrictMode } from 'react'

export default function App() {
  return (
    <StrictMode>
      {/* Your app */}
    </StrictMode>
  )
}
```

<!-- 🔄 v0.74: Metro improvements -->
```js
// metro.config.js - v0.74+ simplified
const { getDefaultConfig } = require('@react-native/metro-config')

const config = getDefaultConfig(__dirname)
module.exports = config
```

### Version Callouts by Feature

**Core Components**
<!-- ✅ v0.70+: All core components stable -->
```tsx
// Stable across versions
import { View, Text, ScrollView, FlatList } from 'react-native'

export function App() {
  return (
    <View>
      <Text>Hello</Text>
      <FlatList data={items} renderItem={renderItem} />
    </View>
  )
}
```

**React Navigation**
<!-- ✅ v0.70+: Navigation patterns stable -->
```tsx
// Stable navigation across versions
import { NavigationContainer } from '@react-navigation/native'
import { createStackNavigator } from '@react-navigation/stack'

// All navigation patterns work consistently
```

**New Architecture**
<!-- 🔄 v0.76: Stable release -->
<!-- 🆕 v0.80+: Default enabled -->
```tsx
// v0.76+: Can opt-in to New Architecture
// v0.80+: Enabled by default for new projects

// Fabric (New Renderer)
// TurboModules (New Native Module System)

// Most apps work without code changes
```

**Hermes Engine**
<!-- ✅ v0.70+: Hermes default -->
<!-- 🚫 v0.76+: JSC deprecated -->
```bash
# v0.70+: Hermes is default engine
# v0.76+: Hermes is the ONLY supported engine
# No need for configuration
```

**Safe Area Context**
<!-- ✅ v0.70+: SafeAreaView stable -->
```tsx
// Stable across versions
import { SafeAreaView } from 'react-native-safe-area-context'

export function Screen() {
  return (
    <SafeAreaView style={{ flex: 1 }}>
      {/* Content */}
    </SafeAreaView>
  )
}
```

**Animated API**
<!-- ✅ v0.70+: Animated stable -->
<!-- 🆕 v0.76+: Performance improvements -->
```tsx
// v0.76+: Better performance with New Architecture
import { Animated, Easing } from 'react-native'

const fadeAnim = useRef(new Animated.Value(0)).current

Animated.timing(
  fadeAnim,
  {
    toValue: 1,
    duration: 300,
    easing: Easing.ease,
  }
).start()
```

**Pressable**
<!-- ✅ v0.70+: Pressable stable -->
```tsx
// Stable across versions (preferred over TouchableOpacity)
import { Pressable, Text } from 'react-native'

export function Button({ onPress, title }) {
  return (
    <Pressable onPress={onPress}>
      <Text>{title}</Text>
    </Pressable>
  )
}
```

**FlatList**
<!-- ✅ v0.70+: FlatList stable -->
<!-- 🆕 v0.76+: Improved performance -->
```tsx
// v0.76+: Better performance with New Architecture
import { FlatList } from 'react-native'

export function List({ data }) {
  return (
    <FlatList
      data={data}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => <Item data={item} />}
      onRefresh={handleRefresh}
      refreshing={isRefreshing}
    />
  )
}
```

### Upgrade Recommendations

**From 0.74 to 0.76:**
1. Run `npx react-native upgrade`
2. Enable New Architecture in android/gradle.properties
3. Update iOS Podfile
4. Test Hermes thoroughly
5. Review deprecated APIs

**From 0.76 to 0.80:**
1. Run `npx react-native upgrade`
2. Update App Registry usage
3. Enable New Architecture if not already
4. Test all third-party libraries
5. Update to React Native 0.80 compatible libraries

**From 0.80 to 0.83:**
1. Run `npx react-native upgrade`
2. Verify New Architecture is working
3. Test on both iOS and Android
4. Check for any performance regressions
5. Update development tools

### Minimum Requirements by Version

| Version | Node | iOS | Android | Xcode | Gradle |
|---------|------|-----|---------|-------|--------|
| 0.83 | 18+ | 13+ | API 21+ | 15+ | 8.0+ |
| 0.80 | 18+ | 13+ | API 21+ | 15+ | 8.0+ |
| 0.76 | 18+ | 13+ | API 21+ | 15+ | 7.5+ |
| 0.74 | 18+ | 12+ | API 21+ | 14+ | 7.4+ |

### Deprecation Timeline

**Removed in 0.80+:**
- Legacy App Registry (use registerRootComponent)
- Old Linking API (use new Linking API)
- AsyncStorage from core (use @react-native-async-storage/async-storage)

**Removed in 0.76+:**
- JavaScript Core (JSC) - Hermes only
- WebView from core (use react-native-webview)
- NetInfo from core (use @react-native-community/netinfo)

**Future Deprecations (0.85+):**
- Watch for Animation API updates
- Check for Navigation changes
- Review Metro config requirements

---

*Part of SuperAI GitHub - Centralized OpenCode Configuration*
